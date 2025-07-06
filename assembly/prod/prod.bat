@echo off
echo 🚀 Starting TalentTrek Production Environment...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Stop any existing containers
echo 🛑 Stopping any existing containers...
docker-compose -f assembly/prod/docker-compose.yml down 2>nul

REM Build and start production environment
echo 📦 Building production containers...
docker-compose -f assembly/prod/docker-compose.yml build

if errorlevel 1 (
    echo ❌ Build failed. Please check the error messages above.
    pause
    exit /b 1
)

echo 🔥 Starting production services...
docker-compose -f assembly/prod/docker-compose.yml up -d

if errorlevel 1 (
    echo ❌ Failed to start services. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Production environment started!
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📊 API Docs: http://localhost:8000/docs
echo.
echo 📋 Useful commands:
echo    View logs: docker-compose -f assembly/prod/docker-compose.yml logs -f
echo    Stop services: docker-compose -f assembly/prod/docker-compose.yml down
echo    Restart services: docker-compose -f assembly/prod/docker-compose.yml restart
echo.
echo 🛑 To stop the production environment, run: docker-compose -f assembly/prod/docker-compose.yml down
pause 