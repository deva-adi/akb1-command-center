# Changelog

All notable changes to **AKB1 Command Center** are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is calendar-style because this is a solo-maintained portfolio build, not a library.

## 2026-04-22 — v5.6 (Drill-fidelity audit + BHARAT programme)

### Principle enforced
Every card value must reconcile to the rows that compose it. Clicking "120 completed points" must show stories whose `story_points` sum to exactly 120 — no more, no less. H1–H8 below catalogue the eight places where that principle was violated in v5.5.4 and are now fixed.

### Added — new data model
- `phase_deliverables` table (#46) — deliverable-level records per Waterfall phase. Columns: `phase_id`, `project_id`, `title`, `description`, `deliverable_type` (doc | artefact | sign-off | build | review), `owner`, `planned_end`, `actual_end`, `status` (Pending | In Progress | Completed | Blocked), `effort_days_planned`, `effort_days_actual`, `evidence_link`, `notes`.
- `GET /api/v1/phase-deliverables?project_id=X&phase_id=Y` — new read endpoint with phase-grouped ordering.
- `PhaseDeliverable` SQLAlchemy model + `PhaseDeliverableOut` Pydantic schema.

### Added — new programme seed
- **Bharat Digital Spine (BHARAT)** — Indian-themed demo programme added to exercise every tab end-to-end.
  - Client: Ministry of Digital Infrastructure · BAC ₹12.5M · 28 people · INR.
  - `BHARAT-UPI` (Waterfall, Light AI) — UPI 2.0 core modernisation · 6 phases × 22 deliverables.
  - `BHARAT-CITIZEN` (Scrum, Heavy AI) — Swayam citizen mobile app · 8 sprints × 53 backlog items.
  - Fully seeded: 24 EVM snapshots, 7 milestones, 7 risks, 6 CSAT months, 7 expectation dimensions, 6 actions, 3 SLA incidents, 4 commercial scenarios, 4 loss categories, 4 rate cards, 3 CRs, 8 dual velocity rows, 3 blend rules, 3 AI assignments, 31 AI usage rows, 3 trust scores, 5 overrides, 8 SDLC rows, 8 AI code metrics.
  - Every sprint's planned / completed / AI-assisted card value equals exactly the sum of filtered backlog items (Adi's 120/140 rule verified).

### Fixed — H1 (BUG)
Kanban top-strip cards (Throughput, WIP, Cycle p50, Blocked) opened the week drill panel unfiltered when a specific metric was clicked. Now they pre-select the metric cell and apply its formula filter via a new `initialMetric` prop on `FlowDrillPanel`. A `useEffect` re-syncs `activeMetric` when `initialMetric` changes so clicking a different top-card while the panel is open retargets cleanly.

### Fixed — H2 (BUG)
Kanban Blocked-time card drilled to items whose `rework_hours` sum does not equal the card value, because per-item `blocked_hours` is not captured in `backlog_items`. Added an amber **Data note** banner (via new `dataNote` field on the FORMULAS entry) that surfaces the gap honestly: "Blocked time is stored as a weekly aggregate — per-item blocker attribution isn't captured in backlog_items today, so the list below shows in-progress items as the nearest proxy." No fake column, no silent mismatch.

### Fixed — H3 (BUG)
SmartOps "Bench cost ₹X (Y FTE on bench)" card scrolled to the resource pool but didn't filter it. Now sets `resourceStatusFilter="Bench"` and displays a clearable filter pill in the resource-pool header. Separated `programmeResources` (drives bench count on card) from `visibleResources` (respects the chip) so the headline number stays stable when the chip toggles.

### Fixed — H4 (GAP)
AI Governance override log had no click-to-filter UX. Added per-override-type and per-outcome filter chips in the card header; card subtitle reports filtered count. The chips persist until explicitly cleared.

### Fixed — H5 (GAP)
Customer Intelligence action items and SLA incident ledger were expand-only. Actions now support status + priority chips; SLA ledger supports priority + breach/met chips. Both sections show filtered count in the subtitle.

### Fixed — H6 (GAP)
Risk Audit top-4 KPI cards (Open risks, Controls tracked, Audit entries, Risk exposure) previously only scrolled or cross-navigated. Now:
- **Open risks** → toggles a special `__open__` status filter on the register.
- **Risk exposure** → toggles expected-loss ranking of the register.
- **Audit entries** → scrolls and resets any active table filter.
- **Controls tracked** → cross-navs to AI tab with programme context preserved.
- A clearable filter banner in the register header summarises all active filters (status / severity / ranking).

### Fixed — H7 (GAP)
WaterfallView had no L4 work-item drill. Now renders an L5 deliverables table inside each expanded phase with:
- Status filter chips (All / Completed / In Progress / Pending / Blocked) with per-status counts.
- Reconcile banner that compares phase header `percent_complete` against both count-based and effort-weighted completion. Warns only when BOTH disagree with the header by more than 10 points — respects the reality that real `percent_complete` is usually effort-weighted.
- Footer aggregates planned / actual effort days for the filtered subset.

### Fixed — H8 (GAP)
Risk Audit compliance-scorecard rows cross-navigated to AI tab without carrying the active programme filter. Now they do: `navigate(filteredProgramme ? '/ai?programme=' + code : '/ai')`.

### Seed — existing programmes
- TTN-STORE (NovaTech's Waterfall project) now has 24 deliverables seeded across its 6 phases (Requirements through Deploy), matching the v5.6 L5 drill.

### Quality Gates
- TypeScript compile: clean.
- Backend `py_compile`: clean on all updated files.
- Docker build: both containers healthy post-rebuild.
- Reconciliation smoke test: every BHARAT-CITIZEN sprint card exactly matches the derived sum from its backlog items (8/8 sprints, 24/24 reconciliations).

---

## 2026-04-21 — v5.3 (Iteration 5 complete — PRs #11 + #12)

### Added — I-5a: Live FX Rate Refresh
- `GET /api/v1/settings/fx-rates/refresh` — fetches latest ECB exchange rates from frankfurter.dev and upserts `currency_rates` table rows
- "Refresh Rates" button in Tab 11 Data Hub; shows last-refreshed timestamp

### Added — I-5b: CSV Commit + Rollback
- `POST /api/v1/import/csv/commit` (multipart: `entity_type` + file) — inserts rows and records a snapshot in `data_import_snapshots`
- `POST /api/v1/import/{id}/rollback` — reverses a specific import atomically
- `GET /api/v1/import/schemas` — returns expected columns per entity type
- Tab 11 UI: entity-type dropdown, Commit button, live import ledger with per-row Rollback button and success banner
- `docs/csv-templates/hercules-programme.csv` — sample CSV for the Hercules Workload Consolidation programme

### Added — I-5c: SSE Smart Ops Alerts Ticker
- `GET /api/v1/smart-ops/alerts/stream` — `text/event-stream` endpoint; pushes Active/Monitoring scenario payloads every 10 s using a fresh DB session per poll cycle
- nginx `location =` exact-match block with `proxy_buffering off`, `proxy_read_timeout 86400s`
- `useAlertsStream.ts` React hook (`EventSource`, auto-reconnects on error)
- `AlertsTicker.tsx` — horizontal scrollable chip strip on Tab 1 Executive Overview; WCAG AA compliant (`role="status"`, `aria-live="polite"`, keyboard-accessible scroll region)

### Added — I-5d: Dark / Light Mode Toggle
- `tailwind.config.js`: `darkMode: "class"` strategy
- `uiStore.ts`: `theme` field + `toggleTheme` action; persisted to `localStorage` key `akb1-theme`
- `ThemeToggle.tsx`: Sun/Moon icon button in header, toggles `dark` class on `<html>`
- `index.css`: dark-mode overrides for `.card`, `.btn-ghost`, `.kpi-*`, `.status-*`
- `Layout.tsx`, `Card.tsx`, `CardHeader.tsx`, `ExecutiveOverview.tsx`: `dark:` Tailwind variants on all surfaces

### Added — Operations
- `docs/DAILY_OPS.md` — step-by-step daily startup guide, manual startup procedure, health verification, 9 troubleshooting scenarios, LaunchAgent management, and decision tree

### Quality Gates
- pytest: 55/55 tests, coverage 70.22%
- vitest: 17/17
- Playwright E2E: 8/8 (including Hercules drill regression, axe-core WCAG AA)
- Ruff + MyPy: zero errors

---

## 2026-04-20 — Iteration 4b (PR #10)

### Added
- Playwright golden-path E2E test suite (8 scenarios)
- axe-core WCAG AA accessibility scan across all 11 tabs
- CycloneDX SBOM generation for backend + frontend at release
- Cold-start timing script — clone → `docker compose up` → dashboard in under 3 minutes

---

## 2026-04-20 — Iteration 4a (PR #9)

### Added
- **Tab 10 Reports & Exports** (`/reports`): per-programme QBR PDF (ReportLab), portfolio-wide and per-programme audit evidence ZIP (JSON dumps + README), configurable 3-month forecast chart with three parallel models.
- `GET /api/v1/reports/qbr/{program_id}.pdf` and `/api/v1/reports/audit-package.zip` endpoints.
- `GET /api/v1/forecasts` — wraps `app/services/forecast.py` primitives (linear trend, weighted moving average, exponential smoothing) into an HTTP surface.
- ReportLab runtime dependency.

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
