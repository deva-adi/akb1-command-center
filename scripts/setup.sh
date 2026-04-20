#!/bin/bash
# AKB1 Command Center v5.0 — First-time setup
# Usage: ./scripts/setup.sh

set -e

echo "=== AKB1 Command Center v5.0 — Setup ==="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed."
    echo "Install Docker Desktop: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose is not available."
    exit 1
fi

echo "[1/4] Checking Docker..."
docker --version
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo "[2/4] Creating .env from .env.example..."
    cp .env.example .env
    echo "  Created .env — edit if you need to change ports"
else
    echo "[2/4] .env already exists, skipping..."
fi
echo ""

# Build
echo "[3/4] Building Docker images (this may take a few minutes on first run)..."
docker-compose build
echo ""

# Start
echo "[4/4] Starting services..."
docker-compose up -d
echo ""

# Wait for health
echo "Waiting for backend health check..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:9001/health > /dev/null 2>&1; then
        echo ""
        echo "=== AKB1 Command Center is running! ==="
        echo ""
        echo "  Dashboard:  http://localhost:9000"
        echo "  API Docs:   http://localhost:9001/docs"
        echo "  Health:     http://localhost:9001/health"
        echo ""
        echo "Demo data has been pre-loaded with 5 programmes."
        echo "To stop: docker-compose down"
        echo "To reset demo data: ./scripts/seed.sh"
        exit 0
    fi
    sleep 2
done

echo "ERROR: Backend did not become healthy in 60 seconds."
echo "Check logs: docker-compose logs backend"
exit 1
