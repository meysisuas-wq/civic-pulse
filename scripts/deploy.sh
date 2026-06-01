#!/bin/bash
set -euo pipefail
echo "Starting CivicPulse deployment..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required"; exit 1; }
echo "Building containers..."
docker-compose build
echo "Starting database..."
docker-compose up -d postgres redis
sleep 5
echo "Running migrations..."
docker-compose run --rm api python -m alembic upgrade head
echo "Seeding database..."
docker-compose run --rm api python src/db/seeds.py
echo "Starting services..."
docker-compose up -d
echo "Deployment complete! API: http://localhost:8000"
