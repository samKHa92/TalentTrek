#!/bin/bash

echo "🚀 Starting TalentTrek Development Environment with Auto-Reload..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start development environment
echo "📦 Building development containers..."
docker-compose -f assembly/dev/docker-compose.dev.yml build

echo "🔥 Starting services with auto-reload..."
docker-compose -f assembly/dev/docker-compose.dev.yml up

echo "✅ Development environment started!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Changes to your code will automatically reload!"
echo "🛑 Press Ctrl+C to stop the development environment" 