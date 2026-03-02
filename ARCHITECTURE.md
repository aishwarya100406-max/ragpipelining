# System Architecture

## Overview

This RAG pipeline implements a production-grade retrieval-augmented generation system with hybrid search capabilities, multi-format document processing, and real-time monitoring.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐             │
│  │   Chat   │  │  Upload  │  │   Metrics    │             │
│  └──────────┘  └──────────┘  └──────────────┘             │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              RAG Pipeline Service                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐      │  │
│  │  │  Query   │→ │Retrieval │→ │  Generation  │      │  │
│  │  │Processing│  │ & Rerank │  │    (LLM)     │      │  │
│  │  └──────────┘  └──────────┘  └──────────────┘      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Document Processing Service                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐      │  │
│  │  │  Extract │→ │  Chunk   │→ │   Embed      │      │  │
│  │  │   Text   │  │   Text   │  │  (OpenAI)    │      │  │
│  │  └──────────┘  └──────────┘  └──────────────┘      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐ ┌──────▼──────┐ ┌───────▼────────┐
│    Qdrant      │ │    Redis    │ │   PostgreSQL   │
│ Vector Store   │ │    Cache    │ │   Metadata     │
└────────────────┘ └─────────────┘ └────────────────┘
```

## Components

### Frontend Layer

**Technology**: React 18 + TypeScript + Vite + TailwindCSS

**Components**:
- `ChatInterface`: Real-time Q&A with streaming support
- `DocumentUpload`: Drag-and-drop file upload with progress
- `MetricsDashboard`: System health and performance metrics
- `Sidebar`: Navigation between views

**Features**:
- Responsive design with glass-morphism effects
- Real-time updates using React Query
- Markdown rendering for responses
- Source citation display

### Backend Layer

**Technology**: FastAPI + Python 3.10+

**Services**:

1. **Document Processor**
   - Extracts text from PDF, DOCX, TXT, Markdown, Code
   - Chunks text using RecursiveCharacterTextSplitter
   - Maintains document metadata

2. **Embedding Service**
   - Generates embeddings using OpenAI API
   - Batch processing for efficiency
   - Configurable model selection

3. **Vector Store**
   - Qdrant client wrapper
   - CRUD operations for documents
   - Filtered search capabilities

4. **RAG Pipeline**
   - Query processing and expansion
   - Hybrid retrieval (dense + sparse)
   - Optional reranking
   - LLM-based answer generation
   - Streaming response support

### Data Layer

**Qdrant Vector Database**:
- Stores document embeddings
- Cosine similarity search
- Metadata filtering
- Horizontal scalability

**Redis**:
- Query result caching
- Session management
- Rate limiting

**PostgreSQL**:
- Document metadata
- User queries history
- Analytics data

## Data Flow

### Document Upload Flow

```
1. User uploads file
2. Backend receives file
3. Extract text based on file type
4. Split text into chunks
5. Generate embeddings for chunks
6. Store embeddings + metadata in Qdrant
7. Return document metadata to user
```

### Query Flow

```
1. User submits query
2. Generate query embedding
3. Search Qdrant for similar chunks
4. (Optional) Rerank results
5. Build context from top chunks
6. Generate answer using LLM
7. Stream response to user
8. Display sources with citations
```

## Key Design Decisions

### Why Qdrant?
- High-performance vector search
- Built-in filtering
- Easy deployment
- Good Python SDK

### Why FastAPI?
- Async support for better performance
- Automatic API documentation
- Type safety with Pydantic
- Easy to test and maintain

### Why React Query?
- Automatic caching
- Background refetching
- Optimistic updates
- Error handling

### Chunking Strategy
- RecursiveCharacterTextSplitter for semantic coherence
- 1000 token chunks with 200 token overlap
- Preserves context across boundaries

### Embedding Model
- text-embedding-3-small for cost-efficiency
- 1536 dimensions
- Good balance of quality and speed

## Scalability Considerations

### Horizontal Scaling
- Stateless backend allows multiple instances
- Load balancer distributes requests
- Qdrant supports clustering

### Caching Strategy
- Redis caches frequent queries
- Embedding cache reduces API calls
- Result cache improves response time

### Async Processing
- Background tasks for document processing
- Celery for long-running jobs
- Non-blocking I/O throughout

## Security

- API key validation
- CORS configuration
- Input sanitization
- Rate limiting (planned)
- File type validation
- Size limits on uploads

## Monitoring

- Structured JSON logging
- Prometheus metrics export
- Health check endpoints
- Performance tracking
- Error alerting (planned)

## Future Enhancements

1. **Advanced Retrieval**
   - HyDE (Hypothetical Document Embeddings)
   - Multi-query retrieval
   - Parent-child document relationships

2. **Reranking**
   - Cohere Rerank integration
   - Cross-encoder models
   - Custom reranking logic

3. **Multi-Modal**
   - Image understanding
   - Table extraction
   - Chart analysis

4. **Evaluation**
   - Automated testing
   - A/B testing framework
   - Quality metrics dashboard

5. **User Management**
   - Authentication
   - User-specific document collections
   - Access control

6. **Advanced Features**
   - Conversational memory
   - Multi-turn dialogue
   - Query suggestions
   - Document summarization
