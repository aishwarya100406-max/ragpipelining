# Setup Guide

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Docker and Docker Compose
- OpenAI API key

## Step-by-Step Setup

### 1. Start Infrastructure Services

Start Qdrant, Redis, and PostgreSQL:

```bash
docker-compose up -d
```

Verify services are running:
```bash
docker-compose ps
```

### 2. Backend Setup

Navigate to backend directory:
```bash
cd backend
```

Create virtual environment:
```bash
python -m venv venv
```

Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

Create environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Frontend Setup

Navigate to frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

### 4. Run the Application

Terminal 1 - Backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### 5. Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

## Testing the System

1. Upload a document (PDF, DOCX, or TXT)
2. Wait for processing to complete
3. Go to Chat tab
4. Ask questions about your document
5. View metrics in the Metrics tab

## Troubleshooting

### Qdrant Connection Error
- Ensure Docker is running
- Check if Qdrant container is up: `docker-compose ps`
- Restart services: `docker-compose restart`

### OpenAI API Error
- Verify your API key in `.env`
- Check your OpenAI account has credits
- Ensure no typos in the key

### Port Already in Use
- Backend: Change port in `uvicorn` command
- Frontend: Change port in `vite.config.ts`

### Module Not Found
- Backend: Ensure virtual environment is activated
- Frontend: Run `npm install` again

## Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Use proper secrets management
3. Set up SSL/TLS certificates
4. Configure proper CORS origins
5. Use production-grade database
6. Set up monitoring and logging
7. Configure rate limiting
8. Use a process manager (PM2, systemd)

## Advanced Configuration

### Custom Embedding Model
Edit `backend/.env`:
```
EMBEDDING_MODEL=text-embedding-3-large
```

### Adjust Chunk Size
Edit `backend/.env`:
```
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

### Enable Cohere Reranking
Add Cohere API key to `.env`:
```
COHERE_API_KEY=your-cohere-key
```

## Support

For issues or questions, check:
- API logs in terminal
- Browser console for frontend errors
- Docker logs: `docker-compose logs`
