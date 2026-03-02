# Advanced RAG Pipeline System

A production-grade Retrieval-Augmented Generation system with hybrid search, multi-modal support, and real-time monitoring.

## Features

- 🔍 Hybrid Search (Dense + Sparse + Reranking)
- 📄 Multi-format document processing (PDF, DOCX, TXT, Code)
- 🎨 Modern React + TypeScript frontend
- ⚡ FastAPI backend with async processing
- 🗄️ Qdrant vector database
- 📊 Real-time metrics and monitoring
- 🔄 Streaming responses
- 📈 Evaluation metrics dashboard

## Tech Stack

**Backend:**
- FastAPI
- LangChain
- Qdrant
- OpenAI/Cohere
- Celery + Redis

**Frontend:**
- React 18 + TypeScript
- Vite
- TailwindCSS
- Shadcn/ui
- React Query

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

### Setup

1. Clone and navigate to project:
```bash
cd rag-pipeline
```

2. Start services with Docker:
```bash
docker-compose up -d
```

3. Setup backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

4. Setup frontend:
```bash
cd frontend
npm install
```

5. Run backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

6. Run frontend:
```bash
cd frontend
npm run dev
```

Visit http://localhost:5173

## Environment Variables

Create `backend/.env`:
```
OPENAI_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
```

## API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Architecture

```
User Query → Query Processing → Hybrid Retrieval → Reranking → LLM → Response
```

## License

MIT
