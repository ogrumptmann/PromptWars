#!/bin/bash
# Run all tests locally before committing
# This script runs tests in Docker containers

set -e  # Exit on error

echo "🧪 Running all tests..."
echo ""

echo "📦 Backend Tests..."
docker-compose exec -T backend python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=80
echo "✅ Backend tests passed!"
echo ""

echo "🎨 Frontend Tests..."
docker-compose exec -T frontend npm test -- --run
echo "✅ Frontend tests passed!"
echo ""

echo "🎉 All tests passed! Ready to commit."

