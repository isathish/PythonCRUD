#!/bin/bash

echo "🛑 Stopping Advanced CRUD System..."

docker-compose down

echo "✅ System stopped successfully!"
echo ""
echo "💡 To remove all data, run: docker-compose down -v"
