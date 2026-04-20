#!/bin/bash
# AKB1 Command Center v5.0 — Re-seed demo data
# Usage: ./scripts/seed.sh
# Warning: This wipes all existing data and re-seeds with demo data

set -e

echo "=== AKB1 Command Center — Re-seed Demo Data ==="
echo ""
echo "WARNING: This will delete all existing data and load demo data."
read -p "Continue? (y/N) " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Calling seed API endpoint..."
curl -X POST http://localhost:9001/api/v1/import/reset-demo \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "Demo data re-seeded. Refresh your dashboard at http://localhost:9000"
