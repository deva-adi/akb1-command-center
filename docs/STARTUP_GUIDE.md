# AKB1 Command Center — Startup Guide

**Version:** 5.4 | **Last Updated:** 2026-04-21 | **Author:** Adi Kompalli

---

## Prerequisites Before Any Start

1. **Docker Desktop must be running** — look for the whale icon in your Mac menu bar.
   If it is not there, open Docker Desktop from Applications first and wait ~30 seconds for it to fully start.

2. **Terminal must be in the project folder** — always run commands from:
   ```
   /Users/adikompalli/Documents/Claude/Claude_Code/Projects/akb1-command-center
   ```

3. **Ports 9000 and 9001 must be free** — if something else is using them:
   ```bash
   lsof -i :9000 -i :9001   # see what's using the ports
   kill -9 <PID>             # kill the process blocking the port
   ```

---

## Option A — Normal Start (Containers Already Built)

Use this every day after the first setup.

```bash
# Step 1 — Navigate to the project folder
cd /Users/adikompalli/Documents/Claude/Claude_Code/Projects/akb1-command-center

# Step 2 — Start both containers
docker compose up -d

# Step 3 — Verify both are running
docker compose ps

# Step 4 — Open the dashboard
open http://localhost:9000
```

**Expected output from Step 3:**
```
NAME            STATUS
akb1-backend    Up (healthy)
akb1-frontend   Up
```

---

## Option B — Full Rebuild Start (After Code Changes / First Time)

Use this when you have pulled new code from GitHub or just cloned the repo.

```bash
# Step 1 — Navigate to the project folder
cd /Users/adikompalli/Documents/Claude/Claude_Code/Projects/akb1-command-center

# Step 2 — Pull latest code from GitHub
git pull origin main

# Step 3 — Stop any running containers first
docker compose down

# Step 4 — Rebuild images from scratch (includes all code changes)
docker compose build --no-cache

# Step 5 — Start the rebuilt containers
docker compose up -d

# Step 6 — Watch startup logs until "healthy" appears (optional, Ctrl+C to exit)
docker compose logs -f --tail=30

# Step 7 — Verify health
curl http://localhost:9001/health

# Step 8 — Open the dashboard
open http://localhost:9000
```

---

## Option C — Stop the Application

```bash
# Graceful stop (containers paused, data preserved)
docker compose stop

# Full teardown (containers removed, data volume preserved)
docker compose down
```

> **Note:** Data is always safe — it lives in a Docker volume (`akb1_data`), not inside the container. `docker compose down` never deletes your data.

---

## Option D — Check Logs / Troubleshoot

```bash
# View live logs from both containers
docker compose logs -f

# Backend logs only
docker compose logs -f backend

# Frontend logs only
docker compose logs -f frontend

# Check health status
curl http://localhost:9001/health

# Restart a single container (e.g. if backend crashes)
docker compose restart backend
```

---

## Option E — Reset to Demo Data

```bash
# Wipes all data and reloads the NovaTech demo dataset
docker compose exec backend python -m app.seed.reset
```

> **Warning:** This deletes all existing data and reloads the demo dataset. This action cannot be undone.

---

## Quick Reference Card

| What you want to do | Command |
|---------------------|---------|
| Start app (normal) | `docker compose up -d` |
| Start app (after code change) | `docker compose build --no-cache && docker compose up -d` |
| Stop app | `docker compose stop` |
| Stop + remove containers | `docker compose down` |
| Check running status | `docker compose ps` |
| View logs | `docker compose logs -f` |
| Restart backend only | `docker compose restart backend` |
| Check API health | `curl http://localhost:9001/health` |
| Open dashboard | `open http://localhost:9000` |
| Open API docs (Swagger) | `open http://localhost:9001/docs` |

---

## URLs

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:9000 |
| API (Swagger docs) | http://localhost:9001/docs |
| API health check | http://localhost:9001/health |

---

**AKB1 Command Center v5.4**
**Maintained by:** Adi Kompalli | deva.adi@gmail.com
