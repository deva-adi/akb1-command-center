# AKB1 Command Center — Daily Operations Guide

## Quick Reference

| Item | Value |
|---|---|
| Dashboard URL | http://localhost:9000 |
| Backend API | http://localhost:9001 |
| Health check | http://127.0.0.1:9001/health |
| Repo path | `~/Documents/Claude/Claude_Code/Projects/akb1-command-center` |
| Backend container | `akb1-backend` |
| Frontend container | `akb1-frontend` |
| Data volume | `akb1-data` → `/data/akb1.db` |

---

## 1. Normal Daily Startup (Automatic)

A macOS LaunchAgent fires on every login and brings the stack up automatically.

**What it does:**
1. Waits up to 90 s for Docker Desktop daemon to be ready
2. Runs `docker compose up -d` from the repo root
3. Polls `http://127.0.0.1:9001/health` up to 60 times (2 s apart)
4. Opens `http://localhost:9000` in your default browser once the backend is healthy

**Expected result:** Browser opens to the Executive Overview within ~60–90 s of login.

**LaunchAgent location:**
```
~/Library/LaunchAgents/com.akb1.dashboard.plist
```

---

## 2. Manual Startup (When Autostart Didn't Fire)

If the browser didn't open automatically or you restarted the machine without triggering the LaunchAgent:

```bash
# Step 1 — make sure Docker Desktop is running
open -a Docker
# Wait ~15 s until the whale icon in the menu bar stops animating

# Step 2 — go to the repo
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center

# Step 3 — start the stack
docker compose up -d

# Step 4 — wait for the backend to be healthy
curl -s http://127.0.0.1:9001/health
# Expected: {"status":"ok"} (repeat until you see this)

# Step 5 — open the dashboard
open http://localhost:9000
```

To run the autostart script manually (mirrors what the LaunchAgent does):

```bash
bash ~/Documents/Claude/Claude_Code/Projects/akb1-command-center/scripts/autostart.sh
```

---

## 3. Verifying the Stack Is Healthy

```bash
# Container status (both should show "Up" and "healthy" or "running")
docker ps --filter "name=akb1"

# Backend health endpoint
curl -s http://127.0.0.1:9001/health

# Quick log tail for both containers
docker logs --tail 20 akb1-backend
docker logs --tail 20 akb1-frontend
```

**Healthy output from `docker ps`:**
```
CONTAINER ID   IMAGE             STATUS
xxxxxxxxxxxx   akb1-frontend     Up 2 minutes
xxxxxxxxxxxx   akb1-backend      Up 2 minutes (healthy)
```

---

## 4. Troubleshooting — Common Failure Modes

---

### 4.1 Docker Desktop Not Running

**Symptom:** `docker ps` returns `Cannot connect to the Docker daemon`.

**Fix:**
```bash
open -a Docker
# Wait 10–15 s for the daemon to start, then retry
docker compose up -d
```

---

### 4.2 Containers Not Starting / Exited Immediately

**Symptom:** `docker ps` shows no `akb1-*` containers, or they exit within seconds.

**Diagnose:**
```bash
docker compose logs
# or individually:
docker logs akb1-backend
docker logs akb1-frontend
```

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| Port 9000 or 9001 already in use | `lsof -i :9000 -i :9001` → kill the blocking process, then `docker compose up -d` |
| Missing `.env` or bad config | Check `docker compose config` for errors |
| Corrupted image layer | `docker compose build --no-cache && docker compose up -d` |

---

### 4.3 Backend Container Keeps Restarting

**Symptom:** `akb1-backend` is listed but restarts every few seconds.

**Diagnose:**
```bash
docker logs akb1-backend --tail 50
```

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| Database file corrupt | See section 4.6 (DB recovery) |
| Alembic migration failure | `docker compose run --rm akb1-backend alembic upgrade head` |
| Python import error | `docker compose build akb1-backend && docker compose up -d akb1-backend` |

---

### 4.4 Frontend Loads But Shows Blank Page or JS Errors

**Symptom:** `http://localhost:9000` opens but the React app doesn't render.

**Diagnose:**
```bash
# Check nginx logs
docker logs akb1-frontend --tail 30

# Open browser DevTools → Console tab for JS errors
```

**Fixes:**

```bash
# Rebuild frontend image (picks up any new code)
docker compose build akb1-frontend
docker compose up -d akb1-frontend
```

---

### 4.5 Port Conflict on 9000 or 9001

**Symptom:** `docker compose up` fails with `address already in use`.

**Fix:**
```bash
# Find what is using the port
lsof -i :9000
lsof -i :9001

# Kill the process (replace PID)
kill -9 <PID>

# Retry
docker compose up -d
```

---

### 4.6 Database Issues (Corrupt / Missing Data)

**Check the DB is accessible:**
```bash
docker exec akb1-backend sqlite3 /data/akb1.db ".tables"
```

**Run migrations manually:**
```bash
docker compose run --rm akb1-backend alembic upgrade head
```

**Full reset (WARNING: deletes all data):**
```bash
docker compose down -v        # -v removes the akb1-data volume
docker compose up -d
# Re-seed if needed:
docker compose run --rm akb1-backend python scripts/seed.py
```

> **Data safety:** `docker compose down` (without `-v`) stops containers but keeps the `akb1-data` volume and all your data intact. Only add `-v` if you want a clean slate.

---

### 4.7 SSE Alerts Ticker Shows Nothing

**Symptom:** The Live Alerts bar on Executive Overview never populates.

**Check:**
```bash
# SSE endpoint should stream data
curl -N http://127.0.0.1:9001/api/v1/smart-ops/alerts/stream
# Expected: lines starting with "data: [...]" every 10 s

# nginx must proxy without buffering
docker logs akb1-frontend --tail 20
```

If nginx is buffering: confirm `frontend/nginx.conf` has the SSE-specific location block with `proxy_buffering off`, then rebuild the frontend image.

---

### 4.8 Theme / UI State Not Persisting Between Reloads

**Symptom:** Dark mode resets to light on every page refresh.

**Check:** Open browser DevTools → Application → Local Storage → `http://localhost:9000` → key `akb1-theme` should be `"dark"` or `"light"`.

If the key is missing, the store initialised but couldn't write. Clear site data and reload:
```
DevTools → Application → Storage → Clear site data
```

---

## 5. Full Stack Reset Procedure

Use this when nothing else works and you want a guaranteed clean state.

```bash
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center

# 1. Stop everything
docker compose down

# 2. (Optional) Remove images to force a clean rebuild
docker compose down --rmi local

# 3. Rebuild both images from scratch
docker compose build --no-cache

# 4. Start fresh
docker compose up -d

# 5. Verify
docker ps --filter "name=akb1"
curl -s http://127.0.0.1:9001/health

# 6. Open dashboard
open http://localhost:9000
```

---

## 6. Starting a Claude Code Session

After the stack is up and the dashboard is reachable:

```bash
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
claude
```

If you want Claude to resume from the last session plan, run:

```
Resume from docs/TOMORROW.md
```

---

## 7. Useful One-Liners

```bash
# Restart only the backend (faster than full restart)
docker compose restart akb1-backend

# Restart only the frontend/nginx
docker compose restart akb1-frontend

# Follow live backend logs
docker logs -f akb1-backend

# Follow live nginx access logs
docker logs -f akb1-frontend

# Inspect the SQLite DB from outside the container
docker run --rm -v akb1-data:/data alpine sh -c "apk add sqlite && sqlite3 /data/akb1.db '.tables'"

# Check disk space used by Docker
docker system df

# Remove dangling images/build cache (safe, won't delete running containers or volumes)
docker system prune -f
```

---

## 8. LaunchAgent Management

```bash
# Reload the LaunchAgent (after editing the plist)
launchctl unload ~/Library/LaunchAgents/com.akb1.dashboard.plist
launchctl load   ~/Library/LaunchAgents/com.akb1.dashboard.plist

# Trigger it manually right now
launchctl start com.akb1.dashboard

# Disable autostart permanently
launchctl unload -w ~/Library/LaunchAgents/com.akb1.dashboard.plist

# Re-enable autostart
launchctl load -w ~/Library/LaunchAgents/com.akb1.dashboard.plist

# Check if it is loaded
launchctl list | grep akb1
```

---

## 9. Decision Tree — "App Won't Come Up"

```
Is Docker Desktop running?
  NO → open -a Docker, wait 15 s, retry
  YES ↓

Are containers listed in `docker ps`?
  NO → docker compose up -d; check logs if it fails
  YES ↓

Is akb1-backend "healthy"?
  NO → docker logs akb1-backend; fix error shown; restart container
  YES ↓

Does curl http://127.0.0.1:9001/health return {"status":"ok"}?
  NO → backend process crashed; rebuild image
  YES ↓

Does http://localhost:9000 open in browser?
  NO → docker logs akb1-frontend; check port 9000 conflict
  YES ↓

Does the React app render?
  NO → open DevTools console; look for JS errors; rebuild frontend image
  YES → Stack is healthy ✓
```
