# After Reboot — Step-by-Step

**Audience:** You, after restarting the MacBook.
**Goal:** Get the AKB1 dashboard running in the browser and resume work on it inside Claude Code.

> **File location:** this file lives at
> `~/Documents/Claude/Claude_Code/Projects/akb1-command-center/docs/AFTER_REBOOT.md`.
> Full path you can copy-paste into Finder:
> `/Users/adikompalli/Documents/Claude/Claude_Code/Projects/akb1-command-center/docs/AFTER_REBOOT.md`.

---

## 0. One-time setup (do this ONCE, ever)

Skip this section if you already ran `./scripts/install-autostart.sh` at least once. If in doubt, re-running it is safe.

```bash
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
./scripts/install-autostart.sh
```

This installs the LaunchAgent at `~/Library/LaunchAgents/com.akb1.dashboard.plist`. From now on, every login will:
1. Wait for Docker Desktop to come up.
2. Run `docker compose up -d` in the repo folder.
3. Wait for the backend `/health` endpoint to respond.
4. Open `http://localhost:9000` in your default browser.

If Docker Desktop isn't set to start at login yet: **Docker Desktop → Settings → General → ✔ Start Docker Desktop when you sign in to your computer**.

---

## 1. What happens automatically when you turn on the Mac

You don't need to do anything. The sequence is:

| Step | Actor | What you see |
|---|---|---|
| A | macOS | You log in |
| B | macOS | Docker Desktop icon appears in the menu bar and starts the VM |
| C | LaunchAgent | Waits up to ~90s for Docker's daemon |
| D | LaunchAgent | Runs `docker compose up -d` |
| E | LaunchAgent | Waits for `GET /health` on port 9001 |
| F | LaunchAgent | Opens the dashboard in your default browser |

Expected total: about **60–90 seconds** from login to the dashboard tab popping up. (Cold-start measured at 26s once Docker is ready.)

If the browser doesn't open after ~2 minutes, check [Troubleshooting](#3-troubleshooting).

---

## 2. Working on the app in Claude Code — tomorrow

1. **Open Terminal** (Spotlight: `⌘ Space`, type "Terminal", Enter).
2. **Go to the project**:
   ```bash
   cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
   ```
3. **Confirm the stack is up** (should already be running from auto-start):
   ```bash
   docker ps --format 'table {{.Names}}\t{{.Status}}' | grep akb1
   # Expect:
   # akb1-frontend   Up X minutes
   # akb1-backend    Up X minutes (healthy)
   ```
   If it's not running:
   ```bash
   docker compose up -d
   ```
4. **Launch Claude Code** from the same directory:
   ```bash
   claude
   ```
   Claude Code will pick up `CLAUDE.md` in the repo and have the whole project context.
5. **Pull the latest from GitHub** (in case you committed from another machine):
   ```bash
   git pull
   ```
6. **Start a new branch for whatever you plan to do today**:
   ```bash
   git checkout -b feat/iteration-6-<short-description>
   ```
   Or continue an existing branch with `git checkout feat/...`.
7. **Tell Claude Code what you want to change.** Examples:
   - "Add a new KPI called Attrition Forecast to Tab 2."
   - "Investigate why the Orion programme shows renewal at 20%."
   - "Refactor the audit trail so INSERT/UPDATE/DELETE each get a separate page."
8. **Iterate, run tests, commit, push, PR** — Claude Code will guide through each step the way it has in previous sessions.

### URL cheat-sheet

| URL | Purpose |
|---|---|
| http://localhost:9000/ | Executive Overview (Tab 1) |
| http://localhost:9000/kpi | KPI Studio (Tab 2) |
| http://localhost:9000/delivery | Delivery Health (Tab 3) |
| http://localhost:9000/velocity | Velocity & Flow (Tab 4) |
| http://localhost:9000/margin | Margin & EVM (Tab 5) |
| http://localhost:9000/customer | Customer Intelligence (Tab 6) |
| http://localhost:9000/ai | AI Governance (Tab 7) |
| http://localhost:9000/smart-ops | Smart Ops (Tab 8) |
| http://localhost:9000/raid | Risk & Audit (Tab 9) |
| http://localhost:9000/reports | Reports & Exports (Tab 10) |
| http://localhost:9000/data-hub | Data Hub & Settings (Tab 11) |
| http://localhost:9001/docs | FastAPI Swagger (auto-generated) |

---

## 3. Troubleshooting

| Symptom | Fix |
|---|---|
| Browser never opens after ~2 min | `tail /tmp/akb1-launch.log` → see how far the auto-start got. |
| `docker info` errors with "daemon not running" | Open Docker Desktop manually. The LaunchAgent will retry in 5 min, or run `./scripts/autostart.sh` yourself. |
| Dashboard shows "Network Error" | Hard reload in browser (`⌘⇧R`). If it still fails: `docker compose logs backend \| tail -50`. |
| `docker compose` reports a port conflict on 9000 or 9001 | Something else is squatting on those ports. Either stop the other process or edit `.env` to move AKB1 to different ports. |
| LaunchAgent isn't running at all | `launchctl list \| grep akb1` should show it. If not, re-run `./scripts/install-autostart.sh`. |
| Want to disable auto-start temporarily | `launchctl unload ~/Library/LaunchAgents/com.akb1.dashboard.plist` |
| Want to re-enable | `launchctl load -w ~/Library/LaunchAgents/com.akb1.dashboard.plist` |
| Fresh demo data | `docker compose down -v && docker compose up -d` |

Deeper diagnostics are in [`docs/RUN_BOOK.md`](./RUN_BOOK.md).

---

## 4. When you want to STOP the stack

```bash
docker compose down          # keeps your data
docker compose down -v       # also wipes the DB volume (re-seed on next boot)
```

If you also want auto-start off:
```bash
launchctl unload ~/Library/LaunchAgents/com.akb1.dashboard.plist
```

---

## 5. Where everything is

```
~/Documents/Claude/Claude_Code/Projects/akb1-command-center/
├── docs/
│   ├── AFTER_REBOOT.md           ← this file
│   ├── RUN_BOOK.md                ← full operations reference
│   ├── ARCHITECTURE.md            ← design source of truth (locked)
│   ├── WIREFRAMES.md              ← every tab wireframe
│   ├── ROADMAP.md                 ← the 4 iterations + horizon
│   └── …
├── backend/                       ← FastAPI app + SQLAlchemy models
├── frontend/                      ← React + Vite + Tailwind
├── scripts/
│   ├── autostart.sh               ← LaunchAgent entry point
│   ├── com.akb1.dashboard.plist   ← LaunchAgent plist
│   ├── install-autostart.sh       ← one-liner installer
│   ├── cold-start-test.sh         ← timing harness
│   ├── sbom.sh                    ← CycloneDX SBOM generator
│   ├── setup.sh / seed.sh / export-db.sh
├── CHANGELOG.md                   ← every iteration summary
├── CLAUDE.md                      ← Claude Code project context
├── docker-compose.yml             ← hardened compose file
└── .env.example                   ← copy to .env to override defaults
```

---

## 6. Quick sanity check (30 seconds)

Paste this in Terminal any time you want to confirm everything is healthy:

```bash
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep akb1
curl -s http://localhost:9001/health | head -1
curl -s http://localhost:9000/api/v1/programmes | python3 -c "import json, sys; print('programmes=', len(json.load(sys.stdin)))"
```

Expected output:
```
akb1-frontend   Up X minutes
akb1-backend    Up X minutes (healthy)
{"status":"healthy","version":"5.2.0","tables":44}
programmes= 5
```

If all three lines print as expected, you're good — head to Claude Code and start building.
