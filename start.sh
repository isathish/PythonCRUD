#!/bin/bash

echo "🚀 Starting Advanced CRUD System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚢 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ System is up and running!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop system:   docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
