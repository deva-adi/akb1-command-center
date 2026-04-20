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
