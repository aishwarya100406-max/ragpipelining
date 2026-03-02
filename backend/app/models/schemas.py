from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CODE = "code"
    MARKDOWN = "markdown"


class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    size: int


class DocumentMetadata(BaseModel):
    doc_id: str
    filename: str
    doc_type: DocumentType
    size: int
    chunks_count: int
    uploaded_at: datetime
    metadata: Dict[str, Any] = {}


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)
    use_reranking: bool = True
    use_hyde: bool = False
    filters: Optional[Dict[str, Any]] = None


class RetrievedChunk(BaseModel):
    content: str
    score: float
    doc_id: str
    chunk_id: str
    metadata: Dict[str, Any] = {}


class QueryResponse(BaseModel):
    answer: str
    sources: List[RetrievedChunk]
    query_id: str
    processing_time: float
    retrieval_method: str


class StreamChunk(BaseModel):
    content: str
    done: bool = False


class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, bool]


class MetricsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    total_queries: int
    avg_response_time: float
    cache_hit_rate: float
