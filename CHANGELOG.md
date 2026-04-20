# Changelog

All notable changes to **AKB1 Command Center** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is calendar-style because this is a solo-maintained portfolio build, not a library.

## [Unreleased] — Iteration 4 (in flight)

### Added
- **Tab 10 Reports & Exports** (`/reports`): per-programme QBR PDF (ReportLab), portfolio-wide and per-programme audit evidence ZIP (JSON dumps + README), configurable 3-month forecast chart with three parallel models.
- `GET /api/v1/reports/qbr/{program_id}.pdf` and `/api/v1/reports/audit-package.zip` endpoints.
- `GET /api/v1/forecasts` — wraps `app/services/forecast.py` primitives (linear trend, weighted moving average, exponential smoothing) into an HTTP surface.
- ReportLab runtime dependency.

### Planned for the same iteration (see ROADMAP)
- Playwright E2E golden-path test
- axe-core accessibility pass across every tab
- CycloneDX SBOM for backend + frontend
- Cold-start timing script — clone → `docker compose up` → dashboard in under 3 minutes

---

## 2026-04-20 — Iteration 3d (PR #8)

### Added
- Shared `ProgrammeFilterBar` + `programmeCrossLinks` module. Retrofitted across Tabs 4–9 to standardise drill-up / drill-across / drill-through navigation.
- `?programme=CODE` filtering on Tab 8 (Smart Ops) and Tab 9 (Risk & Audit).
- Row-level leaf drill-down (inline expand) for change requests (Tab 5), customer actions + SLA incidents (Tab 6), scenarios + resources (Tab 8), risk register (Tab 9).
- `docs/RUN_BOOK.md` — daily workflow, URL deep-links, troubleshooting matrix, developer-mode, security reminders.
- `scripts/com.akb1.dashboard.plist` + `scripts/install-autostart.sh` — macOS LaunchAgent that brings the stack up on login.

## 2026-04-20 — Iteration 3c (PR #7)

### Added
- **Tab 8 Smart Ops** (`/smart-ops`): 8 proactive-detection scenarios, status filter, resource pool table.
- **Tab 9 Risk & Audit** (`/raid`): risk register, compliance scorecard, filtered audit trail with old→new diff, 7-dimension audit-readiness matrix.
- Seed: 8 `scenario_executions`, 10 `resource_pool` rows (2 bench), 8 representative `audit_log` entries.
- Endpoints: `/api/v1/smart-ops/scenarios`, `/smart-ops/resources`, `/audit`.

## 2026-04-20 — Iteration 3b (PR #6)

### Added
- **Tab 7 AI Governance** (`/ai`): 6-factor trust composite radar, productivity-tax comparison, governance controls table, override log, tool catalogue.
- 8 new AI endpoints (`/api/v1/ai/*`).
- Seed `app/seed/ai_data.py`: 5 tools, 9 assignments, ~35 usage rows, 12 code-metric sprint rows, 12 SDLC rows, 4 trust scores, 6 governance items, 5 overrides.

## 2026-04-20 — Iteration 3a (PR #5)

### Added
- **Tab 6 Customer Intelligence** (`/customer`): CSAT / NPS / Renewal trend, 7-dimension Expectation Gap radar, communication tracker, action items, SLA ledger.
- Endpoints: `/api/v1/customer/satisfaction`, `/customer/sla-incidents`.
- Seed: 60 `customer_satisfaction` rows (5 programmes × 12 months), 8 `sla_incidents` including 4 breaches.

## 2026-04-20 — Iteration 2c (PR #4)

### Added
- **Tab 4 Velocity & Flow** (`/velocity`) with dual-velocity chart and blend-rule gates.
- **Tab 5 Margin & EVM** (`/margin`) with 4-layer margin waterfall, 7-loss horizontal bars, rate-card drift table, change-request ledger.
- 6 endpoints: `/dual-velocity`, `/blend-rules`, `/commercial`, `/losses`, `/rate-cards`, `/change-requests`.
- Seed: 12 dual-velocity rows, 7 blend rules, 20 commercial scenarios, 13 losses, 15 rate-card rows, 6 change requests.

## 2026-04-20 — Iteration 2b (PR #3)

### Added
- **Tab 3 Delivery Health** (`/delivery`) as a methodology-adaptive view: Scrum (sprint burndown, velocity + rework, optional dual-velocity), Kanban (ECharts cumulative flow diagram, cycle-time percentiles), Waterfall (phase timeline with gates, milestone list).
- Common EVM strip (CPI / SPI / EAC / TCPI / % complete) + 12-month EVM trend.
- 5 new endpoints: `/sprints`, `/evm`, `/flow`, `/phases`, `/milestones`.
- Delivery seed: 18 Scrum sprints, 24 weeks of Kanban flow rows, 6 Waterfall phases, 72 EVM snapshots, 26 milestones.
- Drill navigation v1: breadcrumb component, programme rows clickable on Tab 1, clear-filter chips, prev/next project drill-across, cross-tab links between Delivery and KPI Studio, expandable sprint / phase / milestone rows.

## 2026-04-20 — Iteration 2a (PR #2)

### Added
- **Tab 2 KPI Studio** (`/kpi`): grouped KPI library, threshold-band trend chart, inline weight editor (optimistic + 422 rollback), latest-value RAG table, formula modal.
- Seed expanded 6 → 13 KPI definitions (Delivery, Quality, People, Commercial, AI).
- API: `?category=` filter, `PUT /kpi/definitions/{id}/weight`, single-definition GET, `kpi_id` snapshot filter.
- Multi-currency: `GET /api/v1/currency/rates`, `CurrencySelector` in top bar, conversion math anchored to USD (default currency switched from INR to USD). Seeded rates INR 83.50, GBP 0.79, EUR 0.93.
- CORS / same-origin: nginx now proxies `/api` + `/health`, so the browser always talks to a single origin.

## 2026-04-20 — Iteration 1 (PR #1)

### Added
- FastAPI backend with 44 SQLAlchemy 2.0 async models (matching ARCHITECTURE.md §5).
- SQLite WAL engine, structlog JSON logging, slowapi rate limiting, Alembic initial migration.
- NovaTech demo seeder: 5 programmes × 12 months, 6 projects, 6 KPI definitions, 5 risks, 7 customer expectations, 6 customer actions, app_settings defaults, currency rates.
- REST v1: `/health`, `/programmes` (+ nested projects), `/kpi/{definitions,snapshots}`, `/risks`, `/customer/{id}/expectations`, `/customer/{id}/actions`, `/settings`, `/import/csv/preview`.
- Vite 5 + React 18 + TypeScript + Tailwind with AKB1 brand tokens.
- Tab 1 Executive Overview, Tab 11 Data Hub & Settings.
- Docker compose hardening: localhost-bound ports, non-root UID 1001, `read_only: true`, `cap_drop: ALL`, tmpfs mounts.
- CI workflow (`.github/workflows/ci.yml`): backend-test (ruff + pytest coverage gate), frontend-lint (ESLint + Vitest + build), docker-build (compose smoke).

### Fixed during post-merge
- Async SQLite URL used 3-slash relative path, which collided with `read_only: true` inside the container — compose default now uses 4-slash absolute path to the mounted `/data` volume.
- `CORS_ORIGINS` JSON decode conflict on pydantic-settings: switched to comma-separated string + computed list property.
