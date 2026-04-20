#!/usr/bin/env bash
# Install the AKB1 Command Center LaunchAgent so the stack boots on login.
# macOS only. Idempotent.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_SRC="$REPO_DIR/scripts/com.akb1.dashboard.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.akb1.dashboard.plist"

if [ "$(uname)" != "Darwin" ]; then
  echo "This installer is macOS-only. See docs/RUN_BOOK.md §3 for Linux/systemd guidance (planned)."
  exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents"

# If a previous copy exists, unload it first so launchctl picks up the new version.
if launchctl list | grep -q com.akb1.dashboard; then
  launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

cp "$PLIST_SRC" "$PLIST_DEST"
launchctl load -w "$PLIST_DEST"

echo "AKB1 dashboard LaunchAgent installed."
echo "Logs → /tmp/akb1-launch.log"
echo "Disable → launchctl unload $PLIST_DEST"
