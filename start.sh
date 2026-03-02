#!/bin/bash

echo "🚀 Starting Advanced RAG Pipeline..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start infrastructure services
echo "📦 Starting infrastructure services (Qdrant, Redis, PostgreSQL)..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Backend .env file not found. Creating from example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your API keys!"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Infrastructure services started!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Backend setup (Terminal 1):"
echo "   cd backend"
echo "   python -m venv venv"
echo "   source venv/bin/activate  # Windows: venv\\Scripts\\activate"
echo "   pip install -r requirements.txt"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. Frontend setup (Terminal 2):"
echo "   cd frontend"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000/docs"
echo "   Qdrant: http://localhost:6333/dashboard"
echo ""
echo "🎉 Happy coding!"
