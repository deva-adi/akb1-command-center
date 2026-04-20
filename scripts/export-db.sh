#!/bin/bash
# AKB1 Command Center v5.0 — Export database to CSV
# Usage: ./scripts/export-db.sh [output_dir]

set -e

OUTPUT_DIR="${1:-./exports/$(date +%Y-%m-%d)}"
mkdir -p "$OUTPUT_DIR"

echo "=== AKB1 Command Center — Database Export ==="
echo "Exporting to: $OUTPUT_DIR"
echo ""

curl -s http://localhost:9001/api/v1/export/workspace -o "$OUTPUT_DIR/workspace_export.json"

echo "Exported workspace to: $OUTPUT_DIR/workspace_export.json"
echo ""
echo "To import this backup later:"
echo "  curl -X POST http://localhost:9001/api/v1/import/workspace -d @$OUTPUT_DIR/workspace_export.json -H 'Content-Type: application/json'"
