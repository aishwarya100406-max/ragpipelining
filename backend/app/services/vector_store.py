from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any, Optional
import uuid
from app.core.config import settings
from app.core.logging import logger


class VectorStore:
    def __init__(self):
        # Initialize Qdrant client with API key if provided
        qdrant_kwargs = {"url": settings.QDRANT_URL}
        if hasattr(settings, 'QDRANT_API_KEY') and settings.QDRANT_API_KEY:
            qdrant_kwargs["api_key"] = settings.QDRANT_API_KEY
        
        self.client = QdrantClient(**qdrant_kwargs)
        self.collection_name = settings.VECTOR_COLLECTION
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            # Determine embedding size based on provider and model
            if settings.EMBEDDING_PROVIDER == "huggingface":
                embedding_size = 384  # all-MiniLM-L6-v2
            elif settings.EMBEDDING_PROVIDER == "ollama":
                embedding_size = 768  # nomic-embed-text
            else:
                embedding_size = 1536  # OpenAI default
            
            if exists:
                # Check if existing collection has correct dimension
                info = self.client.get_collection(self.collection_name)
                if info.config.params.vectors.size != embedding_size:
                    logger.warning(f"Collection dimension mismatch. Deleting and recreating...")
                    self.client.delete_collection(self.collection_name)
                    exists = False
            
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=embedding_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name} with size {embedding_size}")
        except Exception as e:
            logger.error(f"Error ensuring collection: {e}")
            raise
    
    async def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]]
    ) -> List[str]:
        """Add documents to vector store"""
        try:
            ids = [str(uuid.uuid4()) for _ in texts]
            
            points = [
                PointStruct(
                    id=id_,
                    vector=embedding,
                    payload={
                        "text": text,
                        **metadata
                    }
                )
                for id_, text, embedding, metadata in zip(ids, texts, embeddings, metadatas)
            ]
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(ids)} documents to vector store")
            return ids
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            from qdrant_client.models import QueryRequest as QdrantQueryRequest, VectorParams as QdrantVectorParams
            
            search_filter = None
            if filters:
                conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                    for key, value in filters.items()
                ]
                search_filter = Filter(must=conditions)
            
            # Use search_points for older Qdrant or query for newer
            try:
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=top_k,
                    query_filter=search_filter
                )
            except AttributeError:
                # Fallback for different Qdrant version
                results = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_embedding,
                    limit=top_k,
                    query_filter=search_filter
                ).points
            
            return [
                {
                    "id": str(result.id),
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "metadata": {k: v for k, v in result.payload.items() if k != "text"}
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching: {e}", exc_info=True)
            raise
    
    async def delete_by_doc_id(self, doc_id: str):
        """Delete all chunks for a document"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="doc_id",
                            match=MatchValue(value=doc_id)
                        )
                    ]
                )
            )
            logger.info(f"Deleted document: {doc_id}")
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "total_points": info.points_count,
                "vectors_count": info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_points": 0, "vectors_count": 0}


vector_store = VectorStore()
