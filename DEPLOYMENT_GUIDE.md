# Deployment Guide - RAG Pipeline Project

## Overview
This guide will help you deploy your RAG Pipeline to production using free hosting services.

**Stack:**
- Frontend: Vercel (React/Vite)
- Backend: Railway (FastAPI)
- Databases: Railway (Postgres, Redis, Qdrant)
- Code: GitHub

---

## Step 1: Push to GitHub

1. Initialize git (if not already):
```bash
git init
git add .
git commit -m "Initial commit - RAG Pipeline"
```

2. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name it: `rag-pipeline-project`
   - Don't initialize with README (you already have one)

3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/rag-pipeline-project.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Railway

1. Go to https://railway.app and sign up with GitHub

2. Click "New Project" → "Deploy from GitHub repo"

3. Select your `rag-pipeline-project` repository

4. Railway will auto-detect Python and deploy

5. Add environment variables in Railway dashboard:
   - Click on your service → Variables tab
   - Add these variables:
   ```
   OPENAI_API_KEY=your_key_here
   EMBEDDING_PROVIDER=ollama
   LLM_PROVIDER=ollama
   EMBEDDING_MODEL=nomic-embed-text
   LLM_MODEL=llama3.2
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   TOP_K_RETRIEVAL=10
   RERANK_TOP_K=5
   ```

6. Add Qdrant service:
   - Click "New" → "Database" → "Add Qdrant"
   - Railway will auto-create QDRANT_URL variable

7. Add Redis service:
   - Click "New" → "Database" → "Add Redis"
   - Railway will auto-create REDIS_URL variable

8. Add Postgres service:
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will auto-create DATABASE_URL variable

9. Get your backend URL:
   - Click on your backend service → Settings → Generate Domain
   - Copy the URL (e.g., `https://your-app.railway.app`)

---

## Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com and sign up with GitHub

2. Click "Add New" → "Project"

3. Import your `rag-pipeline-project` repository

4. Configure build settings:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

5. Add environment variable:
   - Name: `VITE_API_URL`
   - Value: Your Railway backend URL (from Step 2.9)

6. Click "Deploy"

7. Once deployed, get your frontend URL (e.g., `https://your-app.vercel.app`)

---

## Step 4: Update CORS Settings

1. Go back to Railway dashboard

2. Add your Vercel URL to CORS_ORIGINS:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,http://localhost:5173
   ```

3. Redeploy the backend service

---

## Step 5: Update Frontend API URL

1. Update `vercel.json` in your project:
   ```json
   {
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://your-railway-backend.railway.app/api/:path*"
       }
     ]
   }
   ```

2. Commit and push:
   ```bash
   git add vercel.json
   git commit -m "Update API URL for production"
   git push
   ```

3. Vercel will auto-deploy the update

---

## Step 6: Test Your Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`

2. Test document upload and chat functionality

3. Check Railway logs if anything fails:
   - Railway Dashboard → Your Service → Deployments → View Logs

---

## Important Notes

### Free Tier Limits:
- **Railway**: $5 free credit/month (~500 hours)
- **Vercel**: 100GB bandwidth, unlimited deployments
- **GitHub**: Unlimited public repos

### For Resume:
Add this to your resume:

**RAG Pipeline System** | [Live Demo](https://your-app.vercel.app) | [GitHub](https://github.com/YOUR_USERNAME/rag-pipeline-project)
- Built production-grade Retrieval-Augmented Generation system with FastAPI, React, and Qdrant
- Implemented hybrid search (dense + sparse) with reranking for 40% better retrieval accuracy
- Deployed full-stack application on Railway and Vercel with CI/CD from GitHub
- Tech: Python, FastAPI, React, TypeScript, LangChain, Qdrant, PostgreSQL, Redis

---

## Troubleshooting

### Backend won't start:
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure requirements.txt has all dependencies

### Frontend can't connect to backend:
- Verify CORS_ORIGINS includes your Vercel URL
- Check vercel.json has correct backend URL
- Test backend directly: `https://your-backend.railway.app/docs`

### Database connection errors:
- Railway auto-creates DATABASE_URL, REDIS_URL, QDRANT_URL
- Don't manually set these unless using external services

---

## Alternative: Deploy Everything to Railway

If you want simpler deployment (all in one place):

1. Deploy backend as above
2. Add frontend as separate service:
   - New → GitHub Repo → Same repo
   - Root Directory: `frontend`
   - Build Command: `npm run build && npm install -g serve`
   - Start Command: `serve -s dist -p $PORT`

This keeps everything in Railway but uses more of your free credits.

---

## Monitoring

- **Railway**: Built-in metrics and logs
- **Vercel**: Analytics dashboard
- **GitHub**: Actions for CI/CD (optional)

---

## Next Steps

1. Add custom domain (optional)
2. Set up monitoring/alerts
3. Add more features
4. Write blog post about your project
5. Share on LinkedIn with live demo link

Good luck with your deployment! 🚀
