@echo off
echo Starting Advanced RAG Pipeline...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker first.
    exit /b 1
)

REM Start infrastructure services
echo Starting infrastructure services (Qdrant, Redis, PostgreSQL)...
docker-compose up -d

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 5 /nobreak >nul

REM Check if backend .env exists
if not exist "backend\.env" (
    echo Backend .env file not found. Creating from example...
    copy "backend\.env.example" "backend\.env"
    echo Please edit backend\.env and add your API keys!
    echo Then run this script again.
    exit /b 1
)

echo Infrastructure services started!
echo.
echo Next steps:
echo.
echo 1. Backend setup (Terminal 1):
echo    cd backend
echo    python -m venv venv
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo    uvicorn app.main:app --reload --port 8000
echo.
echo 2. Frontend setup (Terminal 2):
echo    cd frontend
echo    npm install
echo    npm run dev
echo.
echo 3. Access the application:
echo    Frontend: http://localhost:5173
echo    Backend API: http://localhost:8000/docs
echo    Qdrant: http://localhost:6333/dashboard
echo.
echo Happy coding!
