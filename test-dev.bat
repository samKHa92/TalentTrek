@echo off
echo 🧪 Testing TalentTrek Development Environment...

echo.
echo 📦 Building development containers...
docker-compose -f docker-compose.dev.yml build

echo.
echo 🔥 Starting development environment...
docker-compose -f docker-compose.dev.yml up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo 🔍 Checking service status...
docker-compose -f docker-compose.dev.yml ps

echo.
echo 📊 Checking logs...
docker-compose -f docker-compose.dev.yml logs --tail=20

echo.
echo ✅ Test complete! Check the logs above for any errors.
echo 🌐 Frontend should be available at: http://localhost:5173
echo 🔧 Backend should be available at: http://localhost:8000
pause 