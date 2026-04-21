#!/usr/bin/env bash
# AKB1 Command Center — autostart helper.
# Intended to be called by the macOS LaunchAgent at login.
#
# 1. Wait for the Docker daemon (Docker Desktop may still be starting).
# 2. docker compose up -d from the repo directory.
# 3. Wait for /health to respond.
# 4. Open the dashboard in the default browser.
#
# Safe to invoke manually for testing:
#     ./scripts/autostart.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

# Homebrew + system binaries on PATH so this runs cleanly from launchctl.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

log()  { printf '[akb1-autostart] %s\n' "$*"; }

log "Waiting for Docker daemon…"
for i in $(seq 1 30); do
  if docker info >/dev/null 2>&1; then
    log "Docker up after ${i} attempt(s)."
    break
  fi
  sleep 3
done

if ! docker info >/dev/null 2>&1; then
  log "Docker Desktop never came up. Bailing."
  exit 1
fi

log "docker compose up -d"
docker compose up -d

log "Waiting for backend /health…"
for i in $(seq 1 60); do
  if curl -fs http://127.0.0.1:9001/health >/dev/null 2>&1; then
    log "Backend healthy after ${i} attempt(s)."
    break
  fi
  sleep 2
done

if ! curl -fs http://127.0.0.1:9001/health >/dev/null 2>&1; then
  log "Backend failed to come healthy in time. Check 'docker logs akb1-backend'."
  exit 2
fi

# Give the frontend nginx a moment to start serving.
sleep 1
log "Opening dashboard http://localhost:9000"
/usr/bin/open "http://localhost:9000" >/dev/null 2>&1 || true

log "Done."
