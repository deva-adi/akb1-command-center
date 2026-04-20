#!/usr/bin/env bash
# Cold-start smoke: bring the stack up from scratch and time how long it
# takes before /health and /api/v1/programmes respond.
#
# Target per docs/ROADMAP.md: dashboard usable in under 3 minutes.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

START=$(date +%s)

echo "==> docker compose down -v (clean slate)"
docker compose down -v >/dev/null 2>&1 || true

echo "==> docker compose build"
docker compose build >/dev/null

echo "==> docker compose up -d"
docker compose up -d >/dev/null

echo "==> Waiting for backend /health…"
for i in $(seq 1 90); do
  if curl -fs http://127.0.0.1:9001/health >/dev/null 2>&1; then
    HEALTHY_AT=$(date +%s)
    break
  fi
  sleep 2
done

if [ -z "${HEALTHY_AT:-}" ]; then
  echo "Backend never became healthy within 3 minutes."
  docker compose logs backend | tail -40
  exit 1
fi

echo "==> Waiting for programmes seed…"
for i in $(seq 1 30); do
  count=$(curl -fs http://127.0.0.1:9000/api/v1/programmes 2>/dev/null | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
  if [ "${count:-0}" -ge 1 ]; then
    SEEDED_AT=$(date +%s)
    break
  fi
  sleep 2
done

END=$(date +%s)
BACKEND_DELTA=$((HEALTHY_AT - START))
SEED_DELTA=$((SEEDED_AT - START))
TOTAL=$((END - START))

echo
echo "==> Cold-start summary"
echo "Backend healthy    : ${BACKEND_DELTA}s after start"
echo "Programmes seeded  : ${SEED_DELTA}s after start"
echo "Total wall clock   : ${TOTAL}s"

if [ "$TOTAL" -gt 180 ]; then
  echo
  echo "WARNING: cold-start exceeded the 3-minute target."
  exit 2
fi
echo "PASS: dashboard usable in under 3 minutes."
