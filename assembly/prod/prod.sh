#!/bin/bash

echo "🚀 Starting TalentTrek Production Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose -f assembly/prod/docker-compose.yml down 2>/dev/null

# Build and start production environment
echo "📦 Building production containers..."
docker-compose -f assembly/prod/docker-compose.yml build

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi

echo "🔥 Starting production services..."
docker-compose -f assembly/prod/docker-compose.yml up -d

echo "✅ Production environment started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose -f env/prod/docker-compose.yml logs -f"
echo "   Stop services: docker-compose -f env/prod/docker-compose.yml down"
echo "   Restart services: docker-compose -f env/prod/docker-compose.yml restart"
echo ""
echo "🛑 To stop the production environment, run: docker-compose -f assembly/prod/docker-compose.yml down" 