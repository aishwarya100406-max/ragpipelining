from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List
import json
from app.models.schemas import (
    QueryRequest, QueryResponse, DocumentMetadata,
    HealthResponse, MetricsResponse
)
from app.services.document_processor import document_processor
from app.services.embeddings import embedding_service
from app.services.vector_store import vector_store
from app.services.rag_pipeline import rag_pipeline
from app.core.logging import logger

router = APIRouter()


@router.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return []


@router.post("/upload", response_model=DocumentMetadata)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Upload and process a document"""
    try:
        # Read file content
        content = await file.read()
        
        # Process document
        chunks, metadatas, doc_type = await document_processor.process_file(
            file_content=content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        # Generate embeddings
        embeddings = await embedding_service.embed_texts(chunks)
        
        # Store in vector database
        chunk_ids = await vector_store.add_documents(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        # Return metadata
        doc_id = metadatas[0]["doc_id"]
        return DocumentMetadata(
            doc_id=doc_id,
            filename=file.filename,
            doc_type=doc_type,
            size=len(content),
            chunks_count=len(chunks),
            uploaded_at=metadatas[0]["uploaded_at"],
            metadata={"chunk_ids": chunk_ids[:5]}
        )
    
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG pipeline"""
    try:
        response = await rag_pipeline.query(request)
        return response
    except Exception as e:
        logger.error(f"Error querying documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/stream")
async def query_documents_stream(request: QueryRequest):
    """Query documents with streaming response"""
    try:
        async def generate():
            async for chunk in rag_pipeline.query_stream(request):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Error in streaming query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document and its chunks"""
    try:
        await vector_store.delete_by_doc_id(doc_id)
        return {"message": f"Document {doc_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check vector store
        stats = await vector_store.get_stats()
        qdrant_healthy = stats.get("total_points", 0) >= 0
        
        return HealthResponse(
            status="healthy" if qdrant_healthy else "degraded",
            version="1.0.0",
            services={
                "qdrant": qdrant_healthy,
                "openai": True  # Simplified check
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            services={"qdrant": False, "openai": False}
        )


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get system metrics"""
    try:
        stats = await vector_store.get_stats()
        
        return MetricsResponse(
            total_documents=0,  # Would track in DB
            total_chunks=stats.get("total_points", 0),
            total_queries=0,  # Would track in DB
            avg_response_time=0.0,  # Would calculate from logs
            cache_hit_rate=0.0  # Would track cache stats
        )
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
