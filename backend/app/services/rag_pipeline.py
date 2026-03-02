from typing import List, Dict, Any, Optional, AsyncGenerator
import time
import uuid
import httpx
from app.core.config import settings
from app.core.logging import logger
from app.services.vector_store import vector_store
from app.services.embeddings import embedding_service
from app.models.schemas import QueryRequest, QueryResponse, RetrievedChunk


class RAGPipeline:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER  # "openai", "ollama", or "huggingface"
        
        if self.provider == "openai":
            from openai import AsyncOpenAI
            self.llm_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.LLM_MODEL
        elif self.provider == "ollama":
            self.ollama_url = settings.OLLAMA_URL
            self.model = settings.LLM_MODEL
        elif self.provider == "huggingface":
            self.hf_api_key = settings.HUGGINGFACE_API_KEY
            self.model = settings.LLM_MODEL
    
    async def query(self, request: QueryRequest) -> QueryResponse:
        """Execute RAG pipeline"""
        start_time = time.time()
        query_id = str(uuid.uuid4())
        
        try:
            # Step 1: Generate query embedding
            query_embedding = await embedding_service.embed_query(request.query)
            
            # Step 2: Retrieve relevant chunks
            top_k = request.top_k * 2 if request.use_reranking else request.top_k
            results = await vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                filters=request.filters
            )
            
            # Step 3: Rerank if enabled
            if request.use_reranking and len(results) > request.top_k:
                results = await self._rerank(request.query, results, request.top_k)
            
            # Step 4: Generate answer
            context = self._build_context(results)
            answer = await self._generate_answer(request.query, context)
            
            # Step 5: Format response
            sources = [
                RetrievedChunk(
                    content=r["text"],
                    score=r["score"],
                    doc_id=r["metadata"].get("doc_id", ""),
                    chunk_id=r["id"],
                    metadata=r["metadata"]
                )
                for r in results[:request.top_k]
            ]
            
            processing_time = time.time() - start_time
            
            return QueryResponse(
                answer=answer,
                sources=sources,
                query_id=query_id,
                processing_time=processing_time,
                retrieval_method="hybrid" if request.use_reranking else "dense"
            )
        
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            raise
    
    async def query_stream(
        self,
        request: QueryRequest
    ) -> AsyncGenerator[str, None]:
        """Execute RAG pipeline with streaming response"""
        try:
            # Retrieve context
            query_embedding = await embedding_service.embed_query(request.query)
            results = await vector_store.search(
                query_embedding=query_embedding,
                top_k=request.top_k,
                filters=request.filters
            )
            
            context = self._build_context(results)
            
            # Stream answer
            async for chunk in self._generate_answer_stream(request.query, context):
                yield chunk
        
        except Exception as e:
            logger.error(f"Error in streaming pipeline: {e}")
            raise
    
    async def _rerank(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Rerank results using cross-encoder (simplified version)"""
        # In production, use Cohere Rerank or a cross-encoder model
        # For now, return top results by score
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
    
    def _build_context(self, results: List[Dict[str, Any]]) -> str:
        """Build context from retrieved chunks"""
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[{i}] {result['text']}")
        return "\n\n".join(context_parts)
    
    async def _generate_answer(self, query: str, context: str) -> str:
        """Generate answer using LLM"""
        try:
            if self.provider == "openai":
                return await self._generate_openai(query, context)
            elif self.provider == "ollama":
                return await self._generate_ollama(query, context)
            elif self.provider == "huggingface":
                return await self._generate_huggingface(query, context)
        except Exception as e:
            logger.error(f"Error generating answer: {e}", exc_info=True)
            raise
    
    async def _generate_openai(self, query: str, context: str) -> str:
        """Generate with OpenAI"""
        prompt = self._build_prompt(query, context)
        response = await self.llm_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Answer questions based on the provided context. If the context doesn't contain relevant information, say so."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    async def _generate_ollama(self, query: str, context: str) -> str:
        """Generate with Ollama (free, local)"""
        try:
            prompt = self._build_prompt(query, context)
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"You are a helpful AI assistant. Answer based on context.\n\n{prompt}",
                        "stream": False
                    }
                )
                response.raise_for_status()
                return response.json()["response"]
        except Exception as e:
            logger.error(f"Ollama generation error: {e}", exc_info=True)
            raise
    
    async def _generate_huggingface(self, query: str, context: str) -> str:
        """Generate with Hugging Face (free API)"""
        prompt = self._build_prompt(query, context)
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api-inference.huggingface.co/models/{self.model}",
                headers=headers,
                json={
                    "inputs": f"You are a helpful AI assistant. Answer based on context.\n\n{prompt}",
                    "parameters": {"max_new_tokens": 500, "temperature": 0.7}
                },
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return result[0]["generated_text"] if isinstance(result, list) else result["generated_text"]
    
    async def _generate_answer_stream(
        self,
        query: str,
        context: str
    ) -> AsyncGenerator[str, None]:
        """Generate answer with streaming"""
        try:
            prompt = self._build_prompt(query, context)
            
            stream = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Answer questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
            raise
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build prompt for LLM"""
        return f"""Context information:
{context}

Question: {query}

Please provide a comprehensive answer based on the context above. Include relevant details and cite sources using [1], [2], etc."""


rag_pipeline = RAGPipeline()
