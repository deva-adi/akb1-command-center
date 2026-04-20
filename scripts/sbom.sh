#!/usr/bin/env bash
# Generate CycloneDX SBOMs for the backend (Python) and frontend (Node).
# Output lands in ../sbom/ with a timestamped copy + a stable latest.json.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SBOM_DIR="$REPO_DIR/sbom"
mkdir -p "$SBOM_DIR"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

echo "==> Backend SBOM (CycloneDX Python)"
if ! "$REPO_DIR/backend/.venv/bin/python" -c "import cyclonedx_py" 2>/dev/null; then
  echo "Installing cyclonedx-py into backend venv..."
  "$REPO_DIR/backend/.venv/bin/pip" install --quiet "cyclonedx-bom>=4.0.0"
fi
cd "$REPO_DIR/backend"
./.venv/bin/cyclonedx-py requirements \
  --output-format JSON \
  --output-file "$SBOM_DIR/backend-sbom-$STAMP.json" \
  requirements.txt
cp "$SBOM_DIR/backend-sbom-$STAMP.json" "$SBOM_DIR/backend-sbom.json"

echo "==> Frontend SBOM (CycloneDX npm)"
cd "$REPO_DIR/frontend"
npx --yes @cyclonedx/cyclonedx-npm \
  --output-file "$SBOM_DIR/frontend-sbom-$STAMP.json" \
  --output-format JSON
cp "$SBOM_DIR/frontend-sbom-$STAMP.json" "$SBOM_DIR/frontend-sbom.json"

echo "==> Done. Artifacts:"
ls -la "$SBOM_DIR"
