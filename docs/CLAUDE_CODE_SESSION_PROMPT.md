# AKB1 COMMAND CENTER v5.2 — CLAUDE CODE BUILD SESSION PROMPT

**Purpose:** Paste this entire prompt into a new Claude Code session in iTerm2. It contains ALL context needed to build the application from locked documentation, set up GitHub, and execute the build.

---

## COPY EVERYTHING BELOW THIS LINE INTO CLAUDE CODE

---

You are building AKB1 Command Center v5.2 — a Docker-containerized, open-source delivery intelligence platform. The ENTIRE design phase is COMPLETE and LOCKED. 19 documentation files exist with full specifications. Your job is to IMPLEMENT from these docs — never redesign.

## WHO I AM

Adi Kompalli — Senior Delivery & Program Manager, ~20 years enterprise software, Hyderabad India. This app is my portfolio showcase for Director/CTO-track roles. Target repo: github.com/deva-adi/akb1-command-center (public, MIT license). GitHub username: deva-adi. Email: deva.adi@gmail.com.

## WHAT THE APP IS

A portfolio delivery dashboard that answers 58 CTO/CIO/CEO questions about programme health, financial performance, AI governance, and operational risk — driven entirely by user data.

**Tech Stack:** FastAPI (Python 3.12) + React 18 + Vite + Tailwind CSS + shadcn/ui (Radix) + Recharts + ECharts (Kanban CFD) + SQLite WAL + Docker Compose + Alembic migrations + structlog + NumPy/scipy (forecasting) + pandas + openpyxl (Excel import)

**Ports:** 9000 (frontend/nginx) / 9001 (backend/uvicorn) — isolated from my other apps (8080/8502/8503)

**Key numbers:** 44 database tables, 45 formulas, 58 CTO questions, 11 tabs, 15 CSV templates, 5 demo programmes × 12 months, 4-tier security architecture

**Brand palette:** Navy #1B2A4A / Ice Blue #D5E8F0 / Amber #F59E0B / Success Green #10B981 / Danger Red #EF4444 / White #FFFFFF

## MAC FOLDER STRUCTURE — CRITICAL PATHS

```
~/Documents/Claude/
├── Cowork/Projects/
│   └── AKB1 Base — Chief of Staff/           ← Cowork workspace (docs live here)
│       └── 16_AKB1_Command_Center_v5/        ← ALL locked documentation
│           ├── README.md                       (590 lines — full project README)
│           ├── SECURITY.md                     (vulnerability disclosure policy)
│           ├── LICENSE                          (MIT)
│           ├── .gitignore
│           ├── .env.example
│           ├── Caddyfile                       (reverse proxy + security headers)
│           ├── docker-compose.yml              (hardened — localhost-bound, non-root, read-only)
│           ├── docker-compose.proxy.yml        (Caddy overlay for Tier 1 auth)
│           ├── backend/
│           │   ├── Dockerfile                  (multi-stage Python 3.12-slim)
│           │   ├── requirements.txt            (with security deps: slowapi, itsdangerous, passlib)
│           │   └── app/                        (stub __init__.py files in api/, models/, seed/, services/)
│           ├── frontend/
│           │   ├── Dockerfile                  (multi-stage node:20-alpine + nginx:alpine)
│           │   └── nginx.conf
│           ├── scripts/
│           │   ├── setup.sh
│           │   ├── seed.sh
│           │   └── export-db.sh
│           ├── .github/workflows/ci.yml        (backend test + frontend lint + Docker build)
│           └── docs/
│               ├── ARCHITECTURE.md             (96K — 20 sections, THE master spec)
│               ├── WIREFRAMES.md               (38K — 11 tab wireframes)
│               ├── FORMULAS.md                 (65K — 45 formulas with worked examples)
│               ├── CTO_QUESTIONS.md            (67K — 58 questions mapped to tabs/formulas)
│               ├── SECURITY_GUIDE.md           (35K — 4-tier auth, OWASP mapped, 20 sections)
│               ├── DATA_INGESTION.md           (31K — CSV/Excel import, validation, rollback)
│               ├── EARLY_ADOPTER_FAQ.md        (84K — comprehensive FAQ)
│               ├── DEMO_GUIDE.md               (26K — NovaTech demo walkthrough)
│               ├── MASTER_CHECKLIST.md         (22K — Sections A-R + Q security, build gates)
│               ├── ROADMAP.md                  (28K — 4 iterations + horizon)
│               ├── PRODUCTION_SDLC.md          (16K — 7-phase lifecycle)
│               ├── TECH_STACK_BENCHMARK.md     (19K — stack comparison)
│               ├── CONTRIBUTING.md             (18K — contributor guide)
│               ├── VERIFICATION_REPORT_2026-04-16.md  (10K — security verification)
│               └── csv-templates/              (15 CSV files — data import templates)
│                   ├── programmes.csv, projects.csv, sprints.csv
│                   ├── kpi_monthly.csv, financials.csv, evm_monthly.csv
│                   ├── risks.csv, resources.csv, bench.csv, losses.csv
│                   ├── change_requests.csv, ai_metrics.csv, ai_tools.csv
│                   ├── flow_metrics.csv, project_phases.csv
│
└── Claude_Code/Projects/                      ← Claude Code CLI workspace
    └── akb1-command-center/                   ← CREATE THIS — the actual build repo
```

## STEP 0 — PROJECT FOLDER SETUP (DO THIS FIRST)

Before ANY code work, set up the Claude Code project workspace:

```bash
# 1. Create the Claude Code project folder
mkdir -p ~/Documents/Claude/Claude_Code/Projects/akb1-command-center

# 2. Copy ALL locked documentation from Cowork workspace to the new build folder
cp -R ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5/* ~/Documents/Claude/Claude_Code/Projects/akb1-command-center/
cp ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5/.gitignore ~/Documents/Claude/Claude_Code/Projects/akb1-command-center/
cp ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5/.env.example ~/Documents/Claude/Claude_Code/Projects/akb1-command-center/
cp -R ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5/.github ~/Documents/Claude/Claude_Code/Projects/akb1-command-center/
# Note: Do NOT copy .git — we will initialize fresh

# 3. Navigate to the build folder
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center

# 4. Launch Claude Code
claude
```

**This is where you paste the rest of this prompt into the Claude Code session.**

## STEP 1 — GITHUB REPOSITORY SETUP

### 1A. Create the GitHub Repository (Web)

Go to https://github.com/new and create:
- **Repository name:** akb1-command-center
- **Description:** Open-source delivery intelligence platform — 44 tables, 45 formulas, 58 CTO questions answered. Docker-containerized. FastAPI + React + SQLite.
- **Visibility:** Public
- **Initialize:** Do NOT add README, .gitignore, or license (we have our own)
- Click **Create repository**

### 1B. Initialize Local Repository and Push (Claude Code CLI)

Run these commands inside Claude Code or tell Claude Code to execute them:

```bash
# Initialize git
git init
git branch -M main

# Create CLAUDE.md for Claude Code context
cat > CLAUDE.md << 'HEREDOC'
# AKB1 Command Center v5.2

## Project Context
Docker-containerized delivery intelligence platform.
Tech: FastAPI (Python 3.12) + React 18 + Vite + Tailwind CSS + shadcn/ui + SQLite WAL + Docker Compose
Ports: 9000 (frontend/nginx) / 9001 (backend/uvicorn)
44 database tables, 45 formulas, 58 CTO questions, 11 tabs
Target: github.com/deva-adi/akb1-command-center (public, MIT)

## Architecture Source of Truth
- docs/ARCHITECTURE.md — 20 sections, 96K, the MASTER spec. Read this before implementing anything.
- docs/WIREFRAMES.md — 11 tab wireframes with component specs
- docs/FORMULAS.md — 45 formulas with worked examples
- docs/SECURITY_GUIDE.md — 4-tier auth, OWASP Top 10 mapped
- docs/MASTER_CHECKLIST.md — build gates, every item must pass before release

## Build Rules
- IMPLEMENT from docs — never redesign what is already specified
- 4 iterations: I-1 Foundation (Wk 1-2) → I-2 Core (Wk 3-4) → I-3 Advanced (Wk 5-6) → I-4 Polish (Wk 7-8)
- Brand: Navy #1B2A4A / Ice Blue #D5E8F0 / Amber #F59E0B
- Non-root Docker, read-only fs, cap_drop ALL, localhost-bound ports
- Conventional Commits format
- All changes must keep docs in sync
- pytest + Vitest for tests, Ruff + MyPy for linting
- Coverage target ≥ 70%

## Quality Gates Per PR
- Ruff + MyPy pass (zero errors)
- pytest + Vitest pass (coverage ≥ 70%)
- Conventional Commit message format
- No accessibility regressions (axe-core)

## Key Conventions
- Backend: FastAPI with Pydantic v2 models, SQLAlchemy 2.0, async where possible
- Frontend: React 18 functional components, Zustand for client state, React Query for server state
- Database: SQLite WAL mode, Alembic migrations, volume-mounted at /data/akb1.db
- Logging: structlog (JSON structured)
- Import: openpyxl + pandas for Excel/CSV dual import
HEREDOC

# Stage everything and make initial commit
git add -A
git commit -m "feat: initial project structure with locked documentation

Complete design phase artifacts for AKB1 Command Center v5.2:
- 16 documentation files (ARCHITECTURE, WIREFRAMES, FORMULAS, etc.)
- 15 CSV templates for data import
- Docker Compose with container hardening (CIS Docker Benchmark)
- CI/CD workflow (GitHub Actions)
- 4-tier security architecture documentation (OWASP mapped)
- Multi-stage Dockerfiles for backend (Python 3.12) and frontend (React/nginx)
- Caddy reverse proxy configuration

44 tables, 45 formulas, 58 CTO questions, 11 tabs designed.
Build phase begins with Iteration 1 (Foundation)."

# Connect to GitHub and push
git remote add origin https://github.com/deva-adi/akb1-command-center.git
git push -u origin main
```

### 1C. GitHub Desktop App Setup

After the CLI push, open **GitHub Desktop**:
1. File → Add Local Repository
2. Browse to `~/Documents/Claude/Claude_Code/Projects/akb1-command-center`
3. Click **Add Repository**
4. It will show the repo connected to `deva-adi/akb1-command-center` on GitHub
5. You can now use GitHub Desktop for visual diff review + PR management alongside Claude Code CLI

### 1D. Production-Grade GitHub Repository Configuration

After the initial push, configure on GitHub.com:

**Branch Protection (Settings → Branches → Add rule for `main`):**
- Require pull request reviews before merging: 0 approvals (solo maintainer, but keep PR workflow)
- Require status checks to pass: backend-test, frontend-lint, docker-build
- Require branches to be up to date before merging
- Do not allow bypassing settings

**Repository Settings:**
- About: "Open-source delivery intelligence platform — 44 tables, 45 formulas, 58 CTO questions. Docker. FastAPI + React + SQLite."
- Website: (leave blank until deployed)
- Topics: delivery-management, portfolio-dashboard, fastapi, react, docker, sqlite, earned-value, kpi-dashboard, program-management, devops
- Disable Wiki (docs/ folder is the wiki)
- Enable Issues
- Enable Discussions (for community)
- Disable Projects (overkill for solo)

**Add files post-push (via Claude Code CLI):**
```bash
# CODE_OF_CONDUCT.md
# Use Contributor Covenant v2.1
curl -o CODE_OF_CONDUCT.md https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md

# Issue templates
mkdir -p .github/ISSUE_TEMPLATE
cat > .github/ISSUE_TEMPLATE/bug_report.yml << 'EOF'
name: Bug Report
description: Report a bug in AKB1 Command Center
labels: [bug]
body:
  - type: textarea
    id: description
    attributes:
      label: Describe the bug
      placeholder: A clear description of what the bug is
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      placeholder: What you expected to happen
    validations:
      required: true
  - type: dropdown
    id: browser
    attributes:
      label: Browser
      options:
        - Chrome
        - Firefox
        - Safari
        - Edge
        - Other
  - type: textarea
    id: environment
    attributes:
      label: Environment
      placeholder: |
        - OS: macOS / Windows / Linux
        - Docker version:
        - AKB1 version:
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.yml << 'EOF'
name: Feature Request
description: Suggest a new feature or improvement
labels: [enhancement]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem statement
      placeholder: What problem does this solve?
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      placeholder: How should this work?
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      placeholder: What else did you consider?
EOF

# Pull request template
cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
## Summary
<!-- What does this PR do? Link to issue if applicable. -->

## Changes
<!-- Bullet list of changes -->

## Testing
<!-- How was this tested? -->
- [ ] pytest passes
- [ ] Vitest passes
- [ ] Docker build succeeds
- [ ] Manual smoke test

## Checklist
- [ ] Conventional Commit message format
- [ ] No new linting errors (Ruff + MyPy)
- [ ] Docs updated if needed
- [ ] No hardcoded secrets
EOF

git add -A
git commit -m "chore: add CODE_OF_CONDUCT, issue templates, PR template

Production-grade GitHub repository setup:
- Contributor Covenant v2.1
- Bug report and feature request issue templates (YAML forms)
- Pull request template with testing checklist"

git push
```

## STEP 2 — BUILD ITERATION 1: FOUNDATION (Weeks 1-2)

**Scope:** Docker + Database (44 tables) + Seed data + API scaffolding + Security hardening + Tab 1 (Executive Overview) + Tab 11 (Data Hub & Settings)

**The source of truth is `docs/ARCHITECTURE.md`. Read sections 2, 3, 5 (all 44 table schemas), 15 (build plan) before writing any code.**

### 2A. Backend Foundation

```
Read docs/ARCHITECTURE.md Section 5 completely — it has all 44 CREATE TABLE statements.

Then build in this order:

1. backend/app/main.py — FastAPI app factory with:
   - CORS middleware (from env CORS_ORIGINS)
   - Rate limiting via slowapi (60 GET/min, 10 POST/min per IP)
   - Structured logging via structlog
   - Health endpoint: GET /health → {"status": "healthy", "version": "5.2.0", "tables": 44}
   - Startup event: create tables + seed demo data if SEED_DEMO_DATA=true
   - OpenAPI docs at /docs

2. backend/app/database.py — SQLAlchemy 2.0 async engine + session factory
   - SQLite WAL mode: PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;
   - Connection: DATABASE_URL from env (default: sqlite:///data/akb1.db)

3. backend/app/models/ — SQLAlchemy 2.0 ORM models for all 44 tables:
   - programmes.py (programmes table)
   - projects.py (projects table with delivery_methodology field)
   - sprints.py (sprint_data with iteration_type, estimation_unit)
   - kpi.py (kpi_definitions, kpi_snapshots, scoring_weights → merged into kpi_definitions)
   - financial.py (financials, rate_cards, evm_monthly, losses, currency_rates)
   - risk.py (risks, risk_history, assumptions, dependencies)
   - resource.py (resources, bench_tracking, utilization_detail)
   - customer.py (customer_satisfaction, customer_expectations, customer_actions, sla_incidents)
   - ai.py (ai_tools, ai_metrics, ai_governance_log, ai_override_log)
   - change.py (change_requests, change_impact)
   - initiative.py (initiatives, initiative_scores)
   - forecast.py (kpi_forecasts)
   - smart_ops.py (smart_ops_scenarios, smart_ops_alerts, smart_ops_actions)
   - milestone.py (milestones, milestone_dependencies)
   - narrative.py (narrative_templates, narrative_cache)
   - flow.py (flow_metrics — Kanban)
   - phase.py (project_phases — Waterfall)
   - settings.py (app_settings, data_import_log, data_import_snapshots, export_log, schema_version)
   - audit.py (audit_trail)
   - webhook.py (webhook_config, webhook_log)
   - auth.py (users, user_roles — stub tables)
   - commercial.py (commercial_scenarios)

4. backend/app/seed/ — Demo data seeder
   - Read docs/DEMO_GUIDE.md for NovaTech Solutions narrative
   - 5 programmes × 12 months of realistic data
   - Use the 15 CSV templates in docs/csv-templates/ as the data schema reference
   - seed.py: main seeder function called on startup when SEED_DEMO_DATA=true

5. backend/app/api/ — FastAPI routers
   - v1/programmes.py: CRUD for programmes + projects
   - v1/kpi.py: KPI definitions, snapshots, scoring
   - v1/health.py: health check
   - v1/settings.py: app settings, currency config
   - v1/import.py: CSV/Excel upload endpoint with validation

6. backend/app/services/ — Business logic layer
   - aggregation.py: 3-level metric aggregation (Project → Programme → Portfolio)
   - currency.py: multi-currency conversion engine
   - forecast.py: 3 forecast models (linear regression, weighted MA, exponential smoothing)
   - narrative.py: template-based narrative generation

7. Alembic setup:
   - alembic init backend/alembic
   - Initial migration creating all 44 tables
   - Migration for seed data
```

### 2B. Frontend Foundation

```
Read docs/WIREFRAMES.md for Tab 1 and Tab 11 component specs.

1. Initialize React project:
   cd frontend
   npm create vite@latest . -- --template react
   npm install tailwindcss @tailwindcss/vite postcss autoprefixer
   npm install @radix-ui/react-* (shadcn/ui primitives)
   npm install recharts echarts echarts-for-react
   npm install @tanstack/react-query zustand
   npm install axios lucide-react clsx tailwind-merge
   npm install -D vitest @testing-library/react @testing-library/jest-dom

2. Configure Tailwind with AKB1 brand tokens:
   Navy: #1B2A4A, Ice Blue: #D5E8F0, Amber: #F59E0B
   Success: #10B981, Danger: #EF4444

3. Build Tab 1: Executive Overview
   - Portfolio health score (DHI composite)
   - Programme cards with RAG status
   - Revenue vs Cost trend (12-month sparkline via Recharts)
   - Top 3 risks by financial impact
   - 5-number executive summary
   - Active alerts ticker
   - Auto-generated narrative summary
   - "Generate QBR Brief" button

4. Build Tab 11: Data Hub & Settings
   - Guided onboarding wizard (4 steps: base currency → fiscal year → add programmes → upload data)
   - CSV/Excel upload with drag-drop + auto-mapping
   - Data import history with rollback
   - App settings (currency, fiscal year, locale, industry preset)
   - Database backup/restore controls
```

### 2C. Docker & Integration

```
1. Update backend Dockerfile — harden per SECURITY_GUIDE.md §10:
   - Multi-stage build (already exists)
   - Add: RUN addgroup --system --gid 1001 akb1 && adduser --system --uid 1001 --ingroup akb1 akb1
   - Add: USER 1001
   - Remove: curl install (health check now uses Python urllib)

2. Update frontend Dockerfile:
   - Add non-root nginx user

3. Verify docker-compose.yml hardening:
   - 127.0.0.1 port binding ✓ (already done)
   - security_opt: no-new-privileges ✓
   - read_only: true ✓
   - cap_drop: ALL ✓
   - tmpfs mounts ✓

4. Test full stack:
   docker compose build
   docker compose up -d
   curl http://localhost:9001/health
   open http://localhost:9000

5. Create feature branch, commit, push, PR:
   git checkout -b feat/iteration-1-foundation
   git add -A
   git commit -m "feat: iteration 1 foundation — backend + frontend + Docker

   - 44 SQLAlchemy models matching ARCHITECTURE.md §5
   - FastAPI routes for programmes, KPIs, settings, import
   - Demo data seeder (NovaTech, 5 programmes × 12 months)
   - React 18 + Vite + Tailwind + shadcn/ui setup
   - Tab 1 (Executive Overview) + Tab 11 (Data Hub & Settings)
   - Rate limiting, structured logging, health check
   - Alembic migration for initial schema
   - Docker Compose with CIS Docker hardening"
   git push -u origin feat/iteration-1-foundation
   gh pr create --title "feat: Iteration 1 — Foundation" --body "..."
```

## STEP 3 — BUILD ITERATIONS 2-4 (Reference)

### I-2: Core Dashboard (Weeks 3-4)
- Tab 2: KPI Studio (13 KPIs, trend charts, scoring weights, formula reference modal)
- Tab 3A: Delivery Health — Scrum (sprint burndown, EVM, dual velocity)
- Tab 3B: Delivery Health — Kanban (CFD, WIP aging, throughput, cycle time via ECharts)
- Tab 3C: Delivery Health — Waterfall (milestone timeline, phase gates, variance)
- Tab 4: Velocity & Flow (methodology-adaptive views)
- Tab 5: Margin & EVM (4-layer margin, 7 loss categories, rate card drift, EAC/TCPI)
- Target: 35 of 58 CTO questions answered

### I-3: Advanced (Weeks 5-6)
- Tab 6: Customer Intelligence (CSAT, NPS, 7-dimension gap analysis, renewal scoring)
- Tab 7: AI Governance (6-factor trust score, 5-level maturity, override logging, productivity tax)
- Tab 8: Smart Ops (8 proactive detection scenarios, action proposals)
- Tab 9: Risk & Audit (audit trail, governance controls, data lineage, compliance dashboard)
- Target: 52 of 58 CTO questions answered

### I-4: Polish & Ship (Weeks 7-8)
- Tab 10: Reports & Exports (PDF/Excel export, QBR brief generator, audit package)
- Predictive analytics engine (3 forecast models with confidence bands)
- E2E tests (Playwright)
- WCAG 2.1 AA accessibility pass (axe-core)
- SBOM generation (CycloneDX)
- CHANGELOG.md
- Cold-start test (clone → `docker compose up` → dashboard in <3 min)
- All 58 CTO questions answered

## SECURITY IMPLEMENTATION SUMMARY (Already Documented)

All security is documented in `docs/SECURITY_GUIDE.md` (35K, 20 sections). Implement during build:

| Security Control | Implementation | Where |
|---|---|---|
| Localhost binding | `127.0.0.1:` port prefix | docker-compose.yml ✅ already done |
| Rate limiting | slowapi: 60 GET/min, 10 POST/min, 5 upload/min | backend/app/main.py |
| API key auth | Bearer `akb1_sk_{32hex}`, SHA-256 hashed storage | backend/app/middleware/auth.py |
| CORS | Configurable via CORS_ORIGINS env var | backend/app/main.py |
| Container hardening | Non-root (UID 1001), read-only fs, cap_drop ALL, no-new-privileges | Dockerfiles + docker-compose.yml |
| Input validation | Pydantic v2 models on all endpoints, parameterized SQL | All API routes |
| SQL injection prevention | SQLAlchemy ORM (parameterized), never raw SQL with user input | All database queries |
| XSS prevention | React auto-escapes, CSP headers via Caddyfile | Frontend + Caddyfile |
| Security headers | HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy | Caddyfile |
| Structured logging | structlog JSON, never log secrets/PII | backend throughout |
| RBAC stubs | users + user_roles tables (populated when auth enabled) | backend/app/models/auth.py |
| HTTPS | Caddy auto-TLS (Tier 1+) | docker-compose.proxy.yml + Caddyfile |
| OAuth2 Proxy | Sidecar pattern for SSO (Tier 2) | Documented in SECURITY_GUIDE.md §5 |

## DOCKER-COMPOSE.YML (Already Locked — Reference)

```yaml
version: '3.8'
services:
  backend:
    build: {context: ./backend, dockerfile: Dockerfile}
    container_name: akb1-backend
    volumes: [akb1-data:/data]
    environment:
      - DATABASE_URL=sqlite:///data/akb1.db
      - SEED_DEMO_DATA=${SEED_DEMO_DATA:-true}
      - CORS_ORIGINS=${CORS_ORIGINS:-http://localhost:9000}
      - LOG_LEVEL=${LOG_LEVEL:-info}
      - API_KEY_ENABLED=${API_KEY_ENABLED:-true}
      - RATE_LIMIT_READ=${RATE_LIMIT_READ:-60/minute}
      - RATE_LIMIT_WRITE=${RATE_LIMIT_WRITE:-10/minute}
    ports: ["127.0.0.1:${BACKEND_PORT:-9001}:9001"]
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9001/health')"]
      interval: 30s, timeout: 10s, retries: 3, start_period: 15s
    restart: unless-stopped
    security_opt: [no-new-privileges:true]
    read_only: true
    tmpfs: [/tmp:noexec,nosuid,size=64m]
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE]

  frontend:
    build: {context: ./frontend, dockerfile: Dockerfile, args: [VITE_API_URL=${VITE_API_URL:-http://localhost:9001}]}
    container_name: akb1-frontend
    ports: ["127.0.0.1:${FRONTEND_PORT:-9000}:80"]
    depends_on: {backend: {condition: service_healthy}}
    restart: unless-stopped
    security_opt: [no-new-privileges:true]
    read_only: true
    tmpfs: [/tmp:noexec,nosuid,size=64m, /var/cache/nginx:noexec,nosuid,size=32m, /var/run:noexec,nosuid,size=1m]
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE, CHOWN, SETGID, SETUID]

volumes:
  akb1-data: {driver: local}
```

## BACKEND REQUIREMENTS.TXT (Already Locked — Reference)

```
# Core framework
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-multipart>=0.0.9

# Database & migrations
aiosqlite>=0.19.0
sqlalchemy>=2.0.25
alembic>=1.13.1

# Data processing
pandas>=2.1.0
openpyxl>=3.1.2

# Configuration & HTTP
python-dotenv>=1.0.0
httpx>=0.26.0

# Logging
structlog>=24.1.0

# Security & rate limiting
slowapi>=0.1.9
itsdangerous>=2.1.2
passlib[bcrypt]>=1.7.4
```

## CI/CD WORKFLOW (Already Locked — .github/workflows/ci.yml)

3 jobs: backend-test (Python 3.12 + pytest), frontend-lint (Node 20 + npm lint + build), docker-build (compose build + up + health check + down)

## HARD RULES — READ BEFORE EVERY SESSION

1. **IMPLEMENT from docs** — the design is locked. Don't redesign tables, formulas, or UI structure.
2. **Read ARCHITECTURE.md first** — it's the master spec. 96K, 20 sections. Read the relevant section before coding that feature.
3. **Conventional Commits** — `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`
4. **No secrets in code** — all config via environment variables
5. **Test as you go** — write tests alongside code, not after
6. **Keep docs in sync** — if implementation deviates from docs, update the docs
7. **Feature branches** — never commit directly to main. Branch → PR → merge.
8. **One iteration per PR** — large PRs are fine for iteration milestones
9. **Brand consistency** — Navy/Ice Blue/Amber everywhere. No off-brand colors.
10. **Accessibility** — WCAG 2.1 AA from the start, not bolted on at the end

## START HERE

Begin with Step 0 (folder setup), then Step 1 (GitHub + initial push), then Step 2A (backend foundation). Read `docs/ARCHITECTURE.md` Section 5 for all 44 table schemas before writing any model code. Ask me before making any architectural decisions that deviate from the documentation.

---
*AKB1 v5.2 | Adi Kompalli — Architect & Designer | Confidential*
