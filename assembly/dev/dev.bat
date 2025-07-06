@echo off
echo 🚀 Starting TalentTrek Development Environment with Auto-Reload...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Stop any existing containers
echo 🛑 Stopping any existing containers...
docker-compose -f assembly/dev/docker-compose.dev.yml down 2>nul

REM Build and start development environment
echo 📦 Building development containers...
docker-compose -f assembly/dev/docker-compose.dev.yml build

if errorlevel 1 (
    echo ❌ Build failed. Please check the error messages above.
    pause
    exit /b 1
)

echo 🔥 Starting services with auto-reload...
docker-compose -f assembly/dev/docker-compose.dev.yml up

echo.
echo ✅ Development environment started!
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:8000
echo 📊 API Docs: http://localhost:8000/docs
echo.
echo 💡 Changes to your code will automatically reload!
echo 🛑 Press Ctrl+C to stop the development environment
pause 