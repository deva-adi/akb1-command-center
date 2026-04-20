# AKB1 Command Center v5.2 — Claude Code Build Guide

**Created:** 2026-04-17 | **Author:** Adi Kompalli | **Status:** Pre-Build Reference

---

## Why Claude Code for the Build Phase

| Capability | Claude Code (CLI/Desktop) | Claude Cowork |
|---|---|---|
| Run `docker compose build` live | ✅ Native terminal | ❌ No Docker daemon |
| Git commit/branch/push to GitHub | ✅ Direct git access | ❌ Sandbox copies only |
| Run pytest, npm test, linters | ✅ Immediate feedback | ⚠️ Limited sandbox |
| Edit → test → fix iteration cycle | ✅ Sub-second | ❌ Multi-step copy |
| Access Mac filesystem directly | ✅ Your actual system | ❌ Mounted snapshot |
| Start/stop Docker containers | ✅ Full control | ❌ Not available |
| Frontend dev server (Vite HMR) | ✅ localhost access | ❌ Not available |
| Multi-file refactors + validation | ✅ Edit + run in one loop | ⚠️ Edit only, no run |

**Verdict:** Cowork was the right tool for documentation lockdown. Claude Code is the right tool for the build phase. Keep Cowork for doc updates, verification reports, LinkedIn content, and job search.

---

## OPTION A: Claude Code in iTerm2 (Primary — Recommended)

### Prerequisites

- macOS with iTerm2 installed
- Anthropic account: Pro, Max, Team, or Enterprise (free plan does not include Claude Code)
- Node.js 18+ (for npm method) OR curl (for native binary)
- Docker Desktop running (for build phase)
- Git configured with GitHub access

### Step 1 — Install Claude Code

Open iTerm2 and run ONE of these methods:

**Method 1 — Native Binary (Recommended)**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Method 2 — npm**
```bash
npm install -g @anthropic-ai/claude-code
```

> ⚠️ Do NOT use `sudo npm install -g` — causes permission issues and security risks.

### Step 2 — Verify Installation

```bash
claude doctor
```

This checks your installation, authentication, and environment. Fix any issues it reports before proceeding.

### Step 3 — Authenticate

```bash
claude
```

First run will open your browser for authentication. Log in with your Anthropic account. Once authenticated, you'll see the Claude Code prompt.

### Step 4 — Navigate to the AKB1 Project

```bash
cd ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5
```

### Step 5 — Start Claude Code in Project Context

```bash
claude
```

Claude Code automatically reads the directory structure and any CLAUDE.md / .claude files in the project. It will have full context of your codebase.

### Step 6 — Set Up Project Instructions (One-Time)

Create a CLAUDE.md at the project root so Claude Code knows the project conventions:

```bash
cat > CLAUDE.md << 'EOF'
# AKB1 Command Center v5.2

## Build Context
- Docker-containerized delivery intelligence platform
- Tech: FastAPI (Python 3.12) + React 18 + Vite + Tailwind CSS + shadcn/ui + SQLite WAL
- Ports: 9000 (frontend/nginx) / 9001 (backend/uvicorn)
- 44 database tables, 45 formulas, 58 CTO questions, 11 tabs
- Target: github.com/deva-adi/akb1-command-center

## Key Files
- docs/ARCHITECTURE.md — 20 sections, complete design specification
- docs/WIREFRAMES.md — 11 tab wireframes
- docs/SECURITY_GUIDE.md — 4-tier auth, OWASP mapped
- docs/MASTER_CHECKLIST.md — Sections A–R build gates
- docker-compose.yml — hardened, localhost-bound
- backend/requirements.txt — with security deps

## Build Rules
- Implement from ARCHITECTURE.md — do not redesign
- 4 iterations: I-1 Foundation → I-2 Core → I-3 Advanced → I-4 Polish
- AKB1 brand: Navy #1B2A4A / Ice Blue #D5E8F0 / Amber #F59E0B
- Non-root Docker, read-only fs, cap_drop ALL
- All changes must keep docs in sync
EOF
```

### Step 7 — Build Workflow (Daily Pattern)

```
# Start session
cd ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5
claude

# Inside Claude Code, you can now say things like:
> Read ARCHITECTURE.md Section 5 and create all 44 database table schemas in backend/app/models/
> Build the Docker containers and fix any errors
> Run the backend tests and show me failures
> Create the FastAPI router for /api/v1/programmes endpoint
> Set up the React project with Vite, Tailwind, and shadcn/ui
> Git commit the foundation layer with a descriptive message
```

### Step 8 — Key Claude Code Commands (In-Session)

| Command | What It Does |
|---|---|
| `/help` | Show all available commands |
| `/compact` | Compress conversation to free context window |
| `/clear` | Clear conversation history |
| `/cost` | Show token usage and cost for current session |
| `/doctor` | Check installation health |
| `/desktop` | Hand off current session to Claude Desktop app |
| `/review` | Review a pull request |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` or `/exit` | Exit Claude Code |

### Step 9 — Git + GitHub Workflow

```
# Inside Claude Code:
> Initialize git repo, create .gitignore from our template, make initial commit
> Create a feature branch for iteration-1-foundation
> After we finish, create a PR to main with a summary of changes
```

Claude Code can commit, push, create branches, and open PRs directly — no context switching needed.

### Step 10 — Docker Build Cycle

```
# Inside Claude Code:
> Run docker compose build and show me any errors
> Start the containers with docker compose up -d
> Check container logs for the backend service
> Run the health check endpoint at localhost:9001/health
> Tear down with docker compose down
```

---

## OPTION B: Claude Code in Claude Desktop App

### What It Is

The Claude Desktop app includes a built-in Claude Code runner — same engine as the CLI, but with a visual interface for reviewing diffs, managing multiple parallel tasks, and monitoring progress.

### Step 1 — Install/Update Claude Desktop App

Download from [claude.ai/download](https://claude.ai/download) if not already installed. Ensure you're on the latest version (check for updates in the app menu).

### Step 2 — Open Claude Code in the Desktop App

1. Open the Claude Desktop app
2. Look for the **Claude Code** option / terminal icon in the interface
3. Click to start a new Claude Code session
4. The Desktop app will use the same authentication as your logged-in account

### Step 3 — Set Working Directory

When starting a Claude Code session in the Desktop app:
1. Set the working directory to your project:
   ```
   ~/Documents/Claude/Cowork/Projects/AKB1 Base — Chief of Staff/16_AKB1_Command_Center_v5
   ```
2. The app will read CLAUDE.md and project context automatically

### Step 4 — Desktop App Advantages

| Feature | Benefit for AKB1 Build |
|---|---|
| Visual diff review | See file changes side-by-side before approving |
| Multiple parallel sessions | Run backend + frontend builds simultaneously |
| Task queue | Queue up build steps, review as they complete |
| PR status monitoring | Track GitHub PR status from the app |
| Session handoff | Start in iTerm2, hand off to Desktop with `/desktop` |

### Step 5 — Desktop Build Workflow

Same natural language commands as iTerm2 — the engine is identical:

```
> Read docs/ARCHITECTURE.md and scaffold the backend project structure
> Create all 44 SQLite table schemas from the architecture spec
> Build Docker containers and debug any failures
> Set up the React frontend with Vite + Tailwind + shadcn/ui
```

The difference is visual: you see diffs rendered, can approve/reject changes, and manage multiple sessions visually.

### Step 6 — Handoff Between iTerm2 and Desktop

**iTerm2 → Desktop:**
```
/desktop
```
This transfers your current session (with full context) to the Desktop app for visual review.

**Desktop → iTerm2:**
Continue work in iTerm2 by simply starting a new `claude` session in the same project directory. Claude Code reads the codebase state from disk, so context is preserved through the files themselves.

---

## Recommended Build Strategy for AKB1 v5.2

### Phase Allocation

| Phase | Tool | Why |
|---|---|---|
| I-1 Foundation (Docker+DB+Seed) | Claude Code (iTerm2) | Heavy Docker builds, schema creation, backend scaffolding |
| I-2 Core Dashboard (Tabs 2-5) | Claude Code (Desktop) | Visual diff review for React components, parallel frontend+backend |
| I-3 Advanced (Tabs 6-9) | Claude Code (iTerm2) | Complex formula engines, performance testing |
| I-4 Polish & Ship | Both | iTerm2 for CI/CD + tests, Desktop for PR review |
| Doc updates during build | Cowork | Cross-document consistency, verification reports |

### CLAUDE.md Already Exists in AKB1 Base

Your existing CLAUDE.md and auto-memory system in the AKB1 Base workspace will NOT be visible to Claude Code unless you're running it from within that directory. The Step 6 CLAUDE.md (above) should be placed inside the `16_AKB1_Command_Center_v5/` directory specifically for Claude Code context.

---

## Quick Reference Card

```
# Install (one-time)
curl -fsSL https://claude.ai/install.sh | bash

# Verify
claude doctor

# Start a session
cd ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5
claude

# Key shortcuts
Ctrl+C    → Cancel current operation
Ctrl+D    → Exit
/compact  → Free context window
/desktop  → Hand off to Desktop app
/cost     → Check token usage
/help     → All commands

# Auto-updates
Claude Code updates itself automatically on startup
```

---

*AKB1 v5.2 | Adi Kompalli — Architect & Designer | Confidential*
