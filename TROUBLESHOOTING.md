# Troubleshooting Guide

## Common Issues and Solutions

### 🐳 Docker Issues

#### Docker not running
**Symptom**: `Cannot connect to the Docker daemon`

**Solution**:
```bash
# Check Docker status
docker info

# Start Docker Desktop (Windows/Mac)
# Or start Docker service (Linux)
sudo systemctl start docker
```

#### Port already in use
**Symptom**: `Bind for 0.0.0.0:6333 failed: port is already allocated`

**Solution**:
```bash
# Find process using the port
# Windows
netstat -ano | findstr :6333

# Mac/Linux
lsof -i :6333

# Kill the process or change port in docker-compose.yml
```

#### Services not starting
**Symptom**: Container exits immediately

**Solution**:
```bash
# Check logs
docker-compose logs qdrant
docker-compose logs redis
docker-compose logs postgres

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose down
docker-compose up -d --build
```

### 🔧 Backend Issues

#### Module not found
**Symptom**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### OpenAI API error
**Symptom**: `AuthenticationError: Incorrect API key`

**Solution**:
1. Check `.env` file exists in backend/
2. Verify `OPENAI_API_KEY` is set correctly
3. Ensure no extra spaces or quotes
4. Check API key is valid at platform.openai.com
5. Verify you have credits in your account

#### Qdrant connection error
**Symptom**: `ConnectionError: Cannot connect to Qdrant`

**Solution**:
```bash
# Check if Qdrant is running
docker-compose ps

# Check Qdrant logs
docker-compose logs qdrant

# Restart Qdrant
docker-compose restart qdrant

# Verify URL in .env
QDRANT_URL=http://localhost:6333
```

#### Port 8000 already in use
**Symptom**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000

# Kill process or use different port
uvicorn app.main:app --reload --port 8001
```

#### Import errors
**Symptom**: `ImportError: cannot import name 'X' from 'Y'`

**Solution**:
```bash
# Check Python version (need 3.10+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### 🎨 Frontend Issues

#### npm install fails
**Symptom**: `npm ERR! code ERESOLVE`

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Or use legacy peer deps
npm install --legacy-peer-deps
```

#### Port 5173 already in use
**Symptom**: `Port 5173 is in use`

**Solution**:
```bash
# Kill process on port 5173
# Windows
netstat -ano | findstr :5173

# Mac/Linux
lsof -i :5173

# Or change port in vite.config.ts
server: {
  port: 5174
}
```

#### Build fails
**Symptom**: TypeScript errors during build

**Solution**:
```bash
# Check TypeScript version
npx tsc --version

# Clear build cache
rm -rf dist node_modules/.vite

# Rebuild
npm run build
```

#### API calls fail
**Symptom**: `Network Error` or CORS errors

**Solution**:
1. Verify backend is running on port 8000
2. Check proxy configuration in vite.config.ts
3. Verify CORS settings in backend
4. Check browser console for details
5. Try accessing API directly: http://localhost:8000/docs

### 📄 Document Processing Issues

#### Upload fails
**Symptom**: `500 Internal Server Error` on upload

**Solution**:
1. Check file size (< 10MB recommended)
2. Verify file format is supported
3. Check backend logs for details
4. Ensure Qdrant is running
5. Verify OpenAI API key is valid

#### PDF extraction fails
**Symptom**: Empty text from PDF

**Solution**:
1. Check if PDF is text-based (not scanned image)
2. Try different PDF
3. Check backend logs
4. Consider using OCR for scanned PDFs

#### Slow processing
**Symptom**: Upload takes very long

**Solution**:
1. Check file size
2. Reduce chunk size in .env
3. Check system resources
4. Monitor backend logs
5. Consider async processing

### 🔍 Query Issues

#### No results returned
**Symptom**: Empty sources array

**Solution**:
1. Verify documents are uploaded
2. Check Qdrant has data:
   ```bash
   curl http://localhost:6333/collections/documents
   ```
3. Try different query
4. Increase top_k parameter
5. Check vector store logs

#### Irrelevant results
**Symptom**: Results don't match query

**Solution**:
1. Enable reranking: `use_reranking: true`
2. Increase top_k for more options
3. Rephrase query to be more specific
4. Check document quality
5. Adjust chunk size

#### Slow queries
**Symptom**: Response time > 5 seconds

**Solution**:
1. Check Qdrant performance
2. Reduce top_k
3. Enable caching (Redis)
4. Check network latency
5. Monitor OpenAI API response time

#### LLM errors
**Symptom**: Error generating answer

**Solution**:
1. Check OpenAI API status
2. Verify API key and credits
3. Check rate limits
4. Try different model
5. Reduce context size

### 🗄️ Database Issues

#### Qdrant errors
**Symptom**: Vector store operations fail

**Solution**:
```bash
# Check Qdrant health
curl http://localhost:6333/health

# Check collection
curl http://localhost:6333/collections/documents

# Restart Qdrant
docker-compose restart qdrant

# Check logs
docker-compose logs qdrant
```

#### Redis connection fails
**Symptom**: Cannot connect to Redis

**Solution**:
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
redis-cli ping

# Restart Redis
docker-compose restart redis
```

#### PostgreSQL issues
**Symptom**: Database connection errors

**Solution**:
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Connect to database
docker-compose exec postgres psql -U rag_user -d rag_db
```

### 🌐 Network Issues

#### CORS errors
**Symptom**: `Access-Control-Allow-Origin` error

**Solution**:
1. Check CORS_ORIGINS in backend/.env
2. Add frontend URL to allowed origins
3. Restart backend
4. Clear browser cache

#### Proxy not working
**Symptom**: API calls to /api fail

**Solution**:
1. Check vite.config.ts proxy settings
2. Verify backend is running
3. Check backend URL is correct
4. Restart frontend dev server

### 💾 Memory Issues

#### Out of memory
**Symptom**: Process killed or crashes

**Solution**:
1. Reduce chunk size
2. Process fewer documents at once
3. Increase system memory
4. Use pagination for large queries
5. Clear cache regularly

#### High memory usage
**Symptom**: System becomes slow

**Solution**:
1. Monitor with `docker stats`
2. Limit Docker memory
3. Optimize chunk sizes
4. Clear unused data
5. Restart services

### 🔐 Security Issues

#### API key exposed
**Symptom**: API key in git history

**Solution**:
1. Immediately rotate API key
2. Check .gitignore includes .env
3. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch .env" \
   --prune-empty --tag-name-filter cat -- --all
   ```
4. Force push (if safe)

#### Unauthorized access
**Symptom**: Unexpected API usage

**Solution**:
1. Rotate API keys
2. Implement rate limiting
3. Add authentication
4. Monitor access logs
5. Use API key restrictions

### 🧪 Testing Issues

#### Tests fail
**Symptom**: API tests return errors

**Solution**:
1. Verify all services are running
2. Check test data exists
3. Verify API endpoints
4. Check authentication
5. Review test logs

#### Inconsistent results
**Symptom**: Same query returns different results

**Solution**:
1. This is normal for LLMs (temperature > 0)
2. Set temperature to 0 for consistency
3. Use seed parameter if available
4. Cache results for identical queries

### 📱 Browser Issues

#### UI not loading
**Symptom**: Blank page or errors

**Solution**:
1. Check browser console (F12)
2. Clear browser cache
3. Hard refresh (Ctrl+Shift+R)
4. Try different browser
5. Check frontend dev server is running

#### Slow UI
**Symptom**: Laggy interface

**Solution**:
1. Close other tabs
2. Disable browser extensions
3. Clear browser cache
4. Check network tab for slow requests
5. Update browser

### 🔄 Update Issues

#### After git pull, errors occur
**Symptom**: New errors after updating code

**Solution**:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install

# Restart services
docker-compose down
docker-compose up -d
```

## Diagnostic Commands

### Check all services
```bash
# Docker services
docker-compose ps

# Backend health
curl http://localhost:8000/api/v1/health

# Qdrant health
curl http://localhost:6333/health

# Redis
redis-cli ping
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs qdrant
docker-compose logs redis

# Follow logs
docker-compose logs -f
```

### Check resources
```bash
# Docker stats
docker stats

# System resources
top  # Linux/Mac
taskmgr  # Windows
```

## Getting Help

If issues persist:

1. **Check logs**: Backend terminal, Docker logs, browser console
2. **Review documentation**: All .md files
3. **Test components**: Isolate the problem
4. **Search errors**: Google the exact error message
5. **Check versions**: Ensure compatible versions
6. **Clean install**: Remove and reinstall
7. **Ask for help**: Provide error logs and steps to reproduce

## Prevention Tips

1. **Regular updates**: Keep dependencies updated
2. **Monitor logs**: Check for warnings
3. **Backup data**: Regular backups of vector DB
4. **Test changes**: Test before deploying
5. **Document issues**: Keep track of solutions
6. **Use version control**: Commit working states
7. **Monitor resources**: Watch memory and CPU
8. **Validate inputs**: Check data before processing

## Emergency Recovery

If everything breaks:

```bash
# Nuclear option: Start fresh
docker-compose down -v
rm -rf backend/venv
rm -rf frontend/node_modules

# Rebuild
docker-compose up -d
cd backend && python -m venv venv && pip install -r requirements.txt
cd frontend && npm install

# Restart
# Backend: uvicorn app.main:app --reload
# Frontend: npm run dev
```

Remember: Most issues are configuration or environment related. Check the basics first! 🔍
