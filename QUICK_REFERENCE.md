# Quick Reference Card

## 🚀 Quick Start (3 Steps)

```bash
# 1. Start services
docker-compose up -d

# 2. Backend (Terminal 1)
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI API key!
uvicorn app.main:app --reload

# 3. Frontend (Terminal 2)
cd frontend && npm install && npm run dev
```

**Access**: http://localhost:5173

## 📋 Essential Commands

### Docker
```bash
docker-compose up -d          # Start services
docker-compose ps             # Check status
docker-compose logs           # View logs
docker-compose down           # Stop services
docker-compose restart        # Restart all
```

### Backend
```bash
cd backend
source venv/bin/activate      # Activate venv (Mac/Linux)
venv\Scripts\activate         # Activate venv (Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install                   # Install dependencies
npm run dev                   # Development server
npm run build                 # Production build
npm run preview               # Preview build
```

## 🔑 Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
COHERE_API_KEY=your-cohere-key
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=10
```

## 🌐 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Main UI |
| Backend API | http://localhost:8000 | API Server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Qdrant | http://localhost:6333/dashboard | Vector DB |
| Redis | localhost:6379 | Cache |
| PostgreSQL | localhost:5432 | Database |

## 📡 API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Upload Document
```bash
POST /api/v1/upload
Content-Type: multipart/form-data
Body: file=@document.pdf
```

### Query
```bash
POST /api/v1/query
Content-Type: application/json
Body: {
  "query": "Your question",
  "top_k": 5,
  "use_reranking": true
}
```

### Get Metrics
```bash
GET /api/v1/metrics
```

### Delete Document
```bash
DELETE /api/v1/documents/{doc_id}
```

## 🎯 Common Tasks

### Upload a Document
1. Go to Upload tab
2. Drag file or click browse
3. Wait for processing
4. Check success message

### Ask a Question
1. Go to Chat tab
2. Type your question
3. Press Send or Enter
4. Review answer and sources

### Check System Health
1. Go to Metrics tab
2. View service status
3. Check statistics
4. Monitor performance

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Check if backend is running |
| 500 Error | Check backend logs |
| Upload fails | Verify file format and size |
| Slow queries | Check Qdrant performance |
| No API key | Add OPENAI_API_KEY to .env |
| Port in use | Change port or kill process |

## 📊 File Formats Supported

- ✅ PDF (.pdf)
- ✅ Word (.docx)
- ✅ Text (.txt)
- ✅ Markdown (.md)
- ✅ Python (.py)
- ✅ JavaScript (.js)
- ✅ TypeScript (.ts)
- ✅ And more code files

## ⚙️ Configuration

### Adjust Chunk Size
Edit `backend/.env`:
```
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

### Change Embedding Model
Edit `backend/.env`:
```
EMBEDDING_MODEL=text-embedding-3-large
```

### Change LLM Model
Edit `backend/.env`:
```
LLM_MODEL=gpt-4-turbo-preview
```

### Adjust Retrieval
Edit `backend/.env`:
```
TOP_K_RETRIEVAL=20
RERANK_TOP_K=5
```

## 🔍 Testing

### Quick API Test
```bash
curl http://localhost:8000/api/v1/health
```

### Upload Test
```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@sample-documents/sample.txt"
```

### Query Test
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "top_k": 3}'
```

## 📦 Project Structure

```
rag-pipeline/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # Routes
│   │   ├── core/     # Config
│   │   ├── models/   # Schemas
│   │   └── services/ # Business logic
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
└── docker-compose.yml
```

## 🎨 UI Navigation

- **Chat**: Ask questions about documents
- **Upload**: Add new documents
- **Metrics**: View system statistics

## 💡 Pro Tips

1. **Upload first**: Add documents before querying
2. **Be specific**: Clear questions get better answers
3. **Check sources**: Review citations for accuracy
4. **Use reranking**: Enable for better results
5. **Monitor metrics**: Track system performance
6. **Read logs**: Check for errors and warnings
7. **Test locally**: Verify before deploying
8. **Backup data**: Regular backups of vector DB

## 🔐 Security Checklist

- [ ] Add API keys to .env (not .env.example)
- [ ] Don't commit .env to git
- [ ] Use strong secrets in production
- [ ] Configure CORS properly
- [ ] Enable HTTPS in production
- [ ] Set up rate limiting
- [ ] Validate all inputs
- [ ] Monitor for anomalies

## 📚 Documentation Files

- `README.md` - Overview
- `SETUP.md` - Setup guide
- `ARCHITECTURE.md` - System design
- `API_TESTING.md` - API tests
- `DEPLOYMENT.md` - Deploy guide
- `EXAMPLE_QUERIES.md` - Sample queries
- `UI_GUIDE.md` - Interface guide
- `PROJECT_SUMMARY.md` - Complete summary

## 🆘 Getting Help

1. Check documentation files
2. Review error messages
3. Check logs (backend terminal)
4. Verify services are running
5. Test with sample document
6. Check API documentation
7. Review configuration

## 🎓 Learning Path

1. Start with README.md
2. Follow SETUP.md
3. Upload sample document
4. Try example queries
5. Explore API docs
6. Read ARCHITECTURE.md
7. Customize and extend

## ⚡ Performance Tips

- Use appropriate chunk sizes
- Enable caching (Redis)
- Optimize retrieval parameters
- Monitor response times
- Scale horizontally if needed
- Use CDN for frontend
- Implement rate limiting

## 🚢 Deployment Checklist

- [ ] Set ENVIRONMENT=production
- [ ] Use managed services (Qdrant Cloud, etc.)
- [ ] Configure SSL/TLS
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test thoroughly
- [ ] Document deployment
- [ ] Set up CI/CD

## 📞 Support Resources

- API Documentation: http://localhost:8000/docs
- Project Files: All .md files in root
- Sample Document: sample-documents/sample.txt
- Example Queries: EXAMPLE_QUERIES.md

---

**Remember**: This is a complete, production-ready system. Start simple, then customize! 🚀
