# AKB1 Command Center — Run Book

**Audience:** Adi (primary operator) · any future contributor who clones the repo
**Goal:** Boot the dashboard from a cold Mac in ≤ 3 minutes and keep it reachable as a daily driver.

---

## TL;DR — every time you sit down

```bash
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
docker compose up -d
open http://localhost:9000
```

That's it. The backend seeds on first boot; subsequent boots reuse the SQLite volume.

To stop:

```bash
docker compose down
```

Data persists (SQLite volume `akb1-data`). Use `down -v` only when you want a clean slate.

---

## 1. Prerequisites (one-time setup)

| Tool | Install | Verify |
|---|---|---|
| Docker Desktop | `brew install --cask docker` (or download from docker.com) | `docker info` shows a server version |
| Git | `xcode-select --install` | `git --version` |
| GitHub CLI (optional — only for PRs) | `brew install gh` → `gh auth login` | `gh auth status` |
| Node 20 (optional — only for frontend dev outside Docker) | `brew install node@20` | `node --version` → `v20.x` |
| Python 3.12 (optional — only for backend dev outside Docker) | `brew install python@3.12` | `python3.12 --version` |

Ports **9000** and **9001** must be free on `127.0.0.1`. If another app is using them, edit `.env` (see §5).

---

## 2. Daily workflow

### 2.1 Start the stack

```bash
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
docker compose up -d
```

`up -d` puts the containers in the background. First run takes ~90 s (build); subsequent runs take ~5 s.

### 2.2 Check health

```bash
docker ps | grep akb1                      # two containers, status "healthy"
curl http://localhost:9000/health            # {"status":"healthy","version":"5.2.0","tables":44}
```

### 2.3 Open in the browser

```bash
open http://localhost:9000                   # macOS default browser
```

Useful deep-links:

| URL | What it shows |
|---|---|
| `http://localhost:9000/` | Executive Overview (Tab 1) |
| `http://localhost:9000/kpi` | KPI Studio (Tab 2) |
| `http://localhost:9000/delivery?programme=PHOENIX` | Delivery Health pre-filtered to Phoenix |
| `http://localhost:9000/customer?programme=ORION` | Customer Intelligence on Orion |
| `http://localhost:9001/docs` | FastAPI Swagger UI (auto-generated) |

### 2.4 Stop the stack

```bash
docker compose down                          # keeps the data volume
docker compose down -v                       # also drops the volume (will re-seed next run)
```

---

## 3. Auto-start on login (macOS)

Copy the provided LaunchAgent into your user agents directory and load it once:

```bash
mkdir -p ~/Library/LaunchAgents
cp scripts/com.akb1.dashboard.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/com.akb1.dashboard.plist
```

After that, every time you log in macOS will run `docker compose up -d` in the project folder automatically. Stops/starts Docker Desktop itself? Launchctl retries once Docker is available (delay configurable in the plist).

Disable it temporarily:

```bash
launchctl unload ~/Library/LaunchAgents/com.akb1.dashboard.plist
```

Re-enable:

```bash
launchctl load -w ~/Library/LaunchAgents/com.akb1.dashboard.plist
```

Uninstall completely:

```bash
launchctl unload ~/Library/LaunchAgents/com.akb1.dashboard.plist
rm ~/Library/LaunchAgents/com.akb1.dashboard.plist
```

LaunchAgent logs land in `/tmp/akb1-launch.log` — first place to look if the autostart misbehaves.

---

## 4. Common operations

### 4.1 Refresh demo data (re-seed)

```bash
docker compose down -v                       # drop the volume
docker compose up -d                         # backend detects empty DB and re-seeds
```

Rebuild the images first if you've pulled new backend code:

```bash
docker compose build backend frontend
docker compose up -d
```

### 4.2 View live logs

```bash
docker compose logs -f backend               # tail backend (structlog JSON)
docker compose logs -f frontend              # nginx access log
docker compose logs -f                       # both
```

### 4.3 Run a one-off backend shell

```bash
docker compose exec backend sh               # UID 1001 (non-root) — read-only FS, /tmp is writable
# …or SQL:
docker compose exec backend python -c "
import sqlite3; c = sqlite3.connect('/data/akb1.db'); print(c.execute('select count(*) from programs').fetchone())
"
```

### 4.4 Export a DB snapshot

```bash
./scripts/export-db.sh                       # writes a timestamped .db to ./backups/
```

### 4.5 Pull updates from GitHub

```bash
git pull                                     # fast-forward
docker compose build                         # rebuild changed images
docker compose up -d --force-recreate        # apply new images
```

### 4.6 Switch display currency

Use the **Base** dropdown in the top-right of the dashboard (`USD / INR / GBP / EUR`). All amounts recompute using seeded FX rates (USD = 1.0 anchor). Rate source is marked `seed` — see §6 for a live-refresh follow-up.

---

## 5. Configuration (`.env`)

Copy `.env.example` to `.env` and override whatever you need. Common knobs:

| Var | Default | Why change it |
|---|---|---|
| `FRONTEND_PORT` | `9000` | Another service squatting on 9000 |
| `BACKEND_PORT` | `9001` | Another service squatting on 9001 |
| `SEED_DEMO_DATA` | `true` | Set `false` on cold-boots after the DB is populated |
| `DATABASE_URL` | `sqlite+aiosqlite:////data/akb1.db` | Point at a mounted path for backup/restore |
| `CORS_ORIGINS` | `http://localhost:9000,http://127.0.0.1:9000` | Add a reverse-proxy host |
| `LOG_LEVEL` | `info` | `debug` when chasing a bug |

Changes require `docker compose up -d --force-recreate` to take effect.

---

## 6. Troubleshooting

| Symptom | Most likely cause | Fix |
|---|---|---|
| "Network Error" on the dashboard and `/health` is green | You opened a different hostname than the nginx proxy expects | Use `localhost` or `127.0.0.1` exactly — both are now CORS-allowed |
| `docker compose up` hangs on pull | Network / Docker Hub throttle | Wait, or `docker compose build --pull=false` |
| Backend container is "unhealthy" | Seed failed on first run (usually a schema change you ran in a previous version) | `docker compose down -v && docker compose up -d` |
| Port 9000 or 9001 in use | Another service | Edit `.env` to pick free ports, `docker compose up -d --force-recreate` |
| Charts render blank after a base-currency change | Stale React Query cache | Cmd+Shift+R to hard reload |
| FX rates look stale | They are seeded 2026-04-20, not live | Manual edit via `docker compose exec backend python -c …` or wait for the planned `/currency/refresh` endpoint |
| Daily backup is empty | `scripts/export-db.sh` permissions | `chmod +x scripts/*.sh` |

Dig deeper:

```bash
docker compose ps --format 'table {{.Service}}\t{{.Status}}\t{{.Ports}}'
docker logs akb1-backend --tail 100
curl -s http://localhost:9001/health | jq
curl -s http://localhost:9000/api/v1/programmes | jq length
```

---

## 7. Developer mode (outside Docker)

Only needed when you're iterating on code with hot reload.

### 7.1 Backend

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
SEED_DEMO_DATA=true DATABASE_URL=sqlite+aiosqlite:///data/akb1.db uvicorn app.main:app --reload --port 9001
```

Run the test suite: `pytest` · lint: `ruff check app tests` · coverage: `pytest --cov=app`

### 7.2 Frontend

```bash
cd frontend
npm install
npm run dev        # Vite on http://127.0.0.1:9000 with HMR
```

`npm run build` for the production bundle · `npm run lint` · `npm test` for Vitest.

---

## 8. Security reminders

- The default compose file **binds every port to `127.0.0.1`**. The dashboard is not reachable from the LAN. If you want LAN access, drop the `127.0.0.1:` prefix in `docker-compose.yml` **and** terminate TLS via the Caddy overlay (`docker compose -f docker-compose.yml -f docker-compose.proxy.yml up -d`).
- Containers run as UID 1001, read-only root filesystem, `cap_drop: ALL`. Don't undo these without reading `docs/SECURITY_GUIDE.md` §10.
- `.env` is git-ignored. Never commit secrets. If you enable API-key auth (`API_KEY_ENABLED=true`), store only the SHA-256 hash in `API_KEY_HASH`, never the plaintext key.

---

## 9. Links

| Thing | Where |
|---|---|
| GitHub repo | https://github.com/deva-adi/akb1-command-center |
| OpenAPI docs | http://localhost:9001/docs |
| Architecture | `docs/ARCHITECTURE.md` |
| Wireframes | `docs/WIREFRAMES.md` |
| Formulas | `docs/FORMULAS.md` |
| Demo walkthrough | `docs/DEMO_GUIDE.md` |
| Security posture | `docs/SECURITY_GUIDE.md` |
| Contributor guide | `docs/CONTRIBUTING.md` |
