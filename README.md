# AKB1 Command Center v5.5.3

**The open-source delivery intelligence platform that answers every question your CTO, CIO, or CEO would ask — driven entirely by your data.**

Built by an Associate Director - Delivery with ~20 years of enterprise IT experience. Not a toy dashboard — a real delivery operating system with **55+ formulas** (every one revealed inline via Eye icon), 7 loss detection categories, AI governance, predictive analytics, customer intelligence, proactive scenario detection, live SSE alerts, live FX rate refresh, dark/light mode, multi-currency support, and full SDLC framework compatibility (Scrum / Kanban / Waterfall / SAFe / Hybrid).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](docker-compose.yml)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
[![Docs](https://img.shields.io/badge/Docs-Complete-green)](docs/)

---

## What This Is

A Docker-containerized portfolio delivery dashboard that provides:

- **Financial Intelligence:** 4-layer margin analysis (Gross → Contribution → Portfolio → Net), 7 delivery loss categories with detection and prevention, rate card drift tracking, bench cost allocation, utilisation waterfall (3-system)
- **Earned Value Management:** CPI, SPI, EAC, TCPI, VAC — all with trend lines, worked examples, and 3-month predictive forecasts
- **AI Governance:** Trust scoring (6-factor composite), maturity model (5 levels), override logging, productivity tax, AI vs. Traditional team comparison (12 dimensions)
- **Dual Velocity Tracking:** Separate standard and AI-augmented velocity streams with a 6-gate confidence merge protocol
- **Customer Intelligence:** CSAT, NPS, 7-dimension expectation gap analysis, renewal probability scoring, escalation tracking
- **Predictive Analytics:** 3 forecast models (linear regression, weighted moving average, exponential smoothing) with confidence bands on every trend chart
- **Smart Ops:** 8 proactive detection scenarios that identify problems and propose actions — resource rebalancing, bench burn, margin leaks, AI drift, SLA breach prediction, CPI trajectory alerts, customer satisfaction drift, pyramid inversion
- **Audit & Compliance:** AI audit trail, governance control dashboard, data lineage, exportable audit package
- **Auto-Generated Narratives:** Template-based "so what?" summaries for every major metric — copy-paste ready for steering committees
- **58 CTO/CIO/CEO Questions Answered:** Every question a senior leader would ask maps to a specific dashboard section, formula, and data source
- **SDLC Framework Compatible:** Works with Scrum, Kanban, Waterfall, SAFe, and Hybrid methodologies — upload your data regardless of how your teams work
- **Multi-Currency Engine:** Base currency aggregation with live FX rate refresh via frankfurter.dev (INR, USD, EUR, GBP + any ISO 4217), fiscal year configuration, locale-aware number and date formatting
- **Live SSE Alerts Ticker:** Executive Overview shows a real-time scrollable chip strip of Active/Monitoring Smart Ops scenarios, pushed via Server-Sent Events every 10 s — no page refresh needed
- **Dark / Light Mode Toggle:** Sun/Moon button in the header; theme persisted to localStorage and applied instantly across all 11 tabs via Tailwind CSS `dark:` class strategy
- **Universal Formula Reveal (v5.4):** Every metric, KPI tile, and graph card now has an Eye icon — click it to instantly see the formula, what it measures, how to interpret it, and traffic-light thresholds. 55+ metric definitions across 11 domains. No more black-box numbers.

Ships with realistic demo data for **6 programmes** × 12 months (NovaTech Solutions narrative, including **Hercules** workload consolidation programme added in v5.3). Bring your own data via guided onboarding wizard, Excel (.xlsx) or CSV upload with auto-mapping, manual entry, or REST API. Every import creates an instant rollback snapshot. **First real data in 15 minutes.**

---

## Quick Start

### Prerequisites

- **Docker Desktop** (v4.25+ recommended) — [Install Docker](https://docs.docker.com/get-docker/)
  - Windows: Docker Desktop with WSL 2 backend enabled
  - macOS: Docker Desktop for Mac (Intel or Apple Silicon)
  - Linux: Docker Engine + Docker Compose plugin

### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center

# Start everything
./scripts/setup.sh

# Open the dashboard
open http://localhost:9000          # macOS
xdg-open http://localhost:9000     # Linux
```

### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center

# Start everything (Docker Compose v2 — bundled with Docker Desktop)
docker compose up -d --build

# Open the dashboard
Start-Process "http://localhost:9000"

# View API documentation
Start-Process "http://localhost:9001/docs"
```

> **Docker Compose syntax:** This project supports both `docker compose` (v2, recommended) and `docker-compose` (v1 legacy). All scripts detect which is available automatically.

The setup script checks Docker, builds containers, starts services, and waits for health check. Demo data is pre-loaded. **Time to first dashboard: ~3 minutes.**

**First real data in 15 minutes:** Use the guided onboarding wizard in Tab 11 (Data Hub & Settings) to set your base currency, fiscal year, add your programmes, and upload your first KPIs via Excel (.xlsx) or CSV.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | FastAPI (Python 3.12) + Pydantic v2 + Pydantic Settings | Auto-generated Swagger docs, async, type safety, validated config |
| Frontend | React 18 + Vite + Tailwind CSS + shadcn/ui (Radix) | Component model, fast builds, accessible primitives |
| Charts | Recharts (primary) + ECharts (Kanban CFD) | Rich chart ecosystem, cumulative flow diagrams |
| State | React Query + Zustand | Server-state caching, lightweight client store |
| Database | SQLite WAL mode (zero-config, volume-mounted) | Portable, single-file backup, concurrent reads, no setup |
| Migrations | Alembic + SQLAlchemy 2.0 | Versioned schema migrations, rollback support |
| Data Import | openpyxl + pandas | Native Excel (.xlsx) + CSV dual import with instant rollback |
| Live Data | SSE (`text/event-stream`) + EventSource | Real-time Smart Ops alerts on Tab 1 without WebSocket complexity |
| FX Rates | frankfurter.dev API | Live currency conversion, refreshed on demand |
| Theming | Tailwind `darkMode: "class"` + Zustand + localStorage | Persistent dark/light toggle, zero flash on reload |
| Container | Docker Compose (v1 + v2 compatible) | Single-command deployment, cross-platform |
| Logging | structlog | Structured JSON logging for observability |
| Forecast | NumPy + scipy (built-in) | Linear regression, moving averages — no ML overhead |
| Linting | Ruff + Black + MyPy | Fast lint, format, type checking |
| Testing | pytest + Vitest + Playwright + axe-core | Backend, frontend, E2E, and WCAG AA accessibility coverage |
| Port | 9000 (dashboard) / 9001 (API) | Isolated from existing apps |

For full benchmark against 18 open-source applications (Plausible, Grafana, Metabase, Focalboard, etc.): see [`docs/TECH_STACK_BENCHMARK.md`](docs/TECH_STACK_BENCHMARK.md).

---

## Dashboard Tabs (11)

| # | Tab | Purpose | Key Question |
|---|-----|---------|-------------|
| 1 | Executive Summary | Portfolio health, financials, delivery, 12-month trend, top 5 risks, this week's decisions, auto-narrative, **live SSE alerts ticker** | "How are we performing right now?" |
| 2 | Programme Portfolio | Programme cards with methodology badges (Scrum/Kanban/Waterfall/SAFe/Hybrid), SPI/CPI/NPS/Trust | "Which programmes need attention?" |
| 3 | Delivery Health | 3 sub-views: **3A** Scrum/SAFe (burndown, cumulative flow, SPI/CPI), **3B** Kanban (CFD, WIP aging, throughput/cycle time), **3C** Waterfall (milestone timeline, phase variance, gate approval) | "Are we on track?" |
| 4 | Velocity & Flow | Dual velocity chart (standard vs AI-augmented), 6-gate confidence merge protocol | "Is AI making us faster?" |
| 5 | Margin & EVM | Margin waterfall (7 loss categories), EVM panel (CPI/SPI/EAC/VAC/TCPI), multi-currency aggregation | "Are we making money?" |
| 6 | Customer Intelligence | CSAT, NPS, 7-dimension expectation gap, renewal probability, escalation log | "Is the customer happy? Will they renew?" |
| 7 | AI Governance | Trust score gauge (6-factor), maturity model (5 levels), 5-control framework, AI vs Traditional (12 dim) | "Can we trust AI output?" |
| 8 | Smart Ops | 8 proactive detection scenarios with financial impact + webhook alerts (email/Slack/Teams) | "What should I fix right now?" |
| 9 | Risk & Audit | RAID register, SLA incidents, governance maturity, AI audit trail, data lineage, exportable audit package | "What can go wrong? Are we audit-ready?" |
| 10 | Reports & Exports | Auto-generated narratives, steering committee packs, PDF/Excel export, scheduled reports | "Give me the board pack." |
| 11 | Data Hub & Settings | Guided onboarding wizard, drag-drop Excel/CSV upload, auto-mapper, **live commit + one-click rollback**, base currency, fiscal year, locale, backup/restore | "How do I get my data in?" |

For detailed wireframes of every tab with metric dictionaries: see [`docs/WIREFRAMES.md`](docs/WIREFRAMES.md).

---

## Data Ingestion (4 Modes)

### 1. Demo Data (Default)
Pre-loaded on first run. 5 programmes (NovaTech Solutions), 12 months of narrative-driven data. Reset via `./scripts/seed.sh`.

### 2. Guided Onboarding Wizard
Step-by-step: base currency + fiscal year → add programmes → set delivery methodology per project → upload first KPIs → see dashboard. Target: **15 minutes to first real data.**

### 3. Excel (.xlsx) or CSV Upload with Auto-Mapping + Commit/Rollback
Drag-and-drop Excel or CSV files — the app reads your headers, suggests column mappings with confidence scores, you confirm. Mapping saved for future uploads. Pre-flight validation checks data types, required fields, and referential integrity before import.

**Commit/Rollback workflow (Tab 11):**
1. Select entity type (`programmes`, `kpi_monthly`, or any registered type)
2. Choose your CSV file — a preview appears
3. Click **Commit** — rows are inserted, a snapshot is saved
4. If you need to undo, click **Rollback** on any ledger entry — the import is reversed instantly

Every import creates a snapshot (`data_import_snapshots` table) so you can roll back any import individually without affecting others.

| # | Template | What It Populates | Frequency |
|---|----------|-------------------|-----------|
| 1 | programmes.csv | Programme registry | One-time setup |
| 2 | projects.csv | Projects under programmes (incl. `delivery_methodology`) | One-time setup |
| 3 | kpi_monthly.csv | Monthly KPI values | Monthly |
| 4 | evm_monthly.csv | EVM data (PV, EV, AC) | Monthly |
| 5 | risks.csv | Risk register | Weekly-Monthly |
| 6 | sprints.csv | Sprint velocity + AI metrics (`iteration_type`, `estimation_unit`) | Per sprint |
| 7 | financials.csv | Revenue, cost, margin data (with `currency` column) | Monthly |
| 8 | ai_tools.csv | AI tool registry | Quarterly |
| 9 | ai_metrics.csv | AI code quality metrics | Per sprint |
| 10 | resources.csv | Resource pool | Monthly |
| 11 | bench.csv | Bench cost tracking | Monthly |
| 12 | change_requests.csv | Change request log | Per CR |
| 13 | losses.csv | Delivery loss tracking | Monthly |
| 14 | flow_metrics.csv | Kanban flow data (throughput, cycle time, WIP) | Weekly |
| 15 | project_phases.csv | Waterfall phase milestones + gate approvals | Per phase |

Templates with sample data are in `docs/csv-templates/`. Source-tool export walkthroughs (Jira, Azure DevOps, ServiceNow, SAP) are in [`docs/DATA_INGESTION.md`](docs/DATA_INGESTION.md).

### 4. REST API + Manual Entry
Full API at `/docs` (Swagger). POST data from any tool: Python scripts, Power Automate, Zapier, cron jobs. Manual forms in Tab 11 for ad-hoc entry.

### Minimum Viable Data
Just 2 files to see a meaningful dashboard: **programmes.csv** + **kpi_monthly.csv** (or the equivalent .xlsx). Everything else degrades gracefully with clear prompts.

---

## Data Hierarchy — 5-Level Drill-Down Architecture

Every number in the dashboard is traceable from portfolio level all the way down to the individual story or task that created it. The hierarchy works as follows:

```
Level 1 — Portfolio      All programmes combined (Executive Overview, KPI Trend, EVM Portfolio)
    └── Level 2 — Programme   Per-programme breakdown panel (inline drill from L1)
            └── Level 3 — Project    Delivery Health / Velocity / Kanban tabs (filtered by project)
                    └── Level 4 — Sprint     Sprint-level aggregate: velocity, planned pts, defects, rework
                            └── Level 5 — Story/Task   Individual backlog items with assignee, points, AI flag, defects
```

**How it works in practice:**

1. Click a KPI tile on the Executive Overview → see per-programme breakdown (L2)
2. Click a programme → navigate to Delivery Health tab filtered to that project (L3)
3. Click any bar in the "Planned vs completed" chart → Sprint L4 detail panel opens inline
4. Click "Planned points 90", "Velocity 85", "AI-assisted points", or "Rework hours" inside the L4 panel → the full story/task table expands (L5) showing every item, assignee, points, status, AI flag, and rework hours with totals that sum to the aggregate number you clicked

The backend computes all roll-ups: `sum(story_points WHERE status='completed' OR status='added') = sprint.completed_points`. The frontend queries `/api/v1/backlog-items?project_id=X&sprint_number=Y` and filters client-side by the metric clicked.

---

## Database Schema (45 Tables)

| Domain | Tables | Purpose |
|--------|--------|---------|
| Core (11) | programs, projects, kpi_definitions, kpi_snapshots, risks, risk_history, initiatives, sprint_data, **backlog_items**, commercial_scenarios, evm_snapshots | Main delivery data + story/task granularity |
| Extended (7) | milestones, sla_incidents, rate_cards, utilization_detail, customer_satisfaction, kpi_forecasts, narrative_cache | Predictive, customer, audit |
| AI Governance (8) | ai_tools, ai_tool_assignments, ai_usage_metrics, ai_code_metrics, ai_sdlc_metrics, ai_trust_scores, ai_governance_config, ai_override_log | AI tracking |
| Smart Ops (2) | resource_pool, scenario_executions | Proactive detection |
| Financial (3) | bench_tracking, scope_creep_log, loss_exposure | Loss tracking |
| Dual Velocity (2) | sprint_velocity_dual, sprint_velocity_blend_rules | AI velocity |
| System (6) | data_imports, app_settings, audit_log, currency_rates, data_import_snapshots, schema_version | Configuration, multi-currency, import rollback, migration versioning |
| Methodology (2) | flow_metrics, project_phases | Kanban flow, Waterfall gates |
| Security (2) | users, user_roles | Auth & RBAC stubs (populated when Tier 3 auth enabled) |
| v5.3 Column Additions | `backlog_items.status` values: `completed` \| `carried_over` \| `added` | AI over-delivery modelling (completed > planned) |

Schema migrations managed via Alembic. Full DDL: see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) Section 5.

---

## Universal Formula Reveal (v5.4)

Every metric in the dashboard — KPI tiles, summary cards, waterfall bars, drill panels, sprint stats, flow metrics — has an **Eye icon** in the top-right corner. Clicking it expands an inline panel showing:

| Panel Section | Content |
|--------------|---------|
| **Formula** | Exact calculation (e.g. `Earned Value (EV) / Actual Cost (AC)`) |
| **What it measures** | Plain-English explanation of what the number represents |
| **How to use it** | Actionable guidance — when to escalate, what thresholds mean, what to do |
| **Thresholds** | Green / Amber / Red band boundaries (e.g. CPI: Green ≥1.00, Amber 0.90–0.99, Red <0.90) |

**55+ metric definitions** across 11 domains, centrally defined in `frontend/src/lib/metrics.ts`:

| Domain | Metrics |
|--------|---------|
| Sprint (Scrum) | velocity, planned_points, completed_points, burndown_pct, shortfall, defects, rework_hours, ai_assisted_points, team_size |
| Flow (Kanban) | throughput, wip, cycle_p50, blocked, lead_time, flow_efficiency |
| EVM | cpi, spi, eac, tcpi, percent_complete |
| Dual Velocity | standard_velocity, ai_raw_velocity, ai_adjusted_velocity, quality_parity, ai_rework_points, combined_velocity, merge_eligible |
| Margin | gross_margin, blended_margin, contribution_margin, net_margin |
| Customer | csat, nps, open_escalations, renewal_probability |
| AI Governance | time_saved, acceptance_rate, ai_spend |
| Smart Ops | scenario_alerts, mitigating_scenarios, risk_exposure, bench_cost |
| Risk | open_risks |
| Portfolio (KPI tiles) | portfolio_revenue, avg_cpi |
| Waterfall | phase_completion, schedule_variance_days, milestone_slip |

No more black-box numbers — every stakeholder can understand exactly how a figure is calculated without leaving the screen.

---

## Formulas (55+)

Every formula is documented with definition, calculation, 2 worked examples, thresholds, and dashboard location. Categories:

- **Estimation (6):** BAC, Blended Cost, Loaded Cost, PERT, Contingency, EAC
- **Earned Value (6):** CPI, SPI, ETC, TCPI, VAC, Percent Complete
- **Financial (8):** Gross/Contribution/Portfolio/Net Margin, Shadow Bench Allocation, CR Processing Cost, Revenue Realisation, Rate Card Drift
- **Delivery Health (5):** Schedule Adherence, Scope Stability, Utilisation (True Billable), Quality Index, DHI
- **Sprint & Velocity (5):** Sprint Velocity, Sprint Leakage, Defect Density, Rework %, AI Quality-Adjusted Velocity
- **AI Governance (4):** AI Trust Score, AI Maturity, AI Override Rate, Net AI Productivity Gain
- **Loss Detection (3):** Attrition Knowledge Loss, SLA Penalty Exposure, Scope Creep Absorption
- **Predictive & Customer (3):** Renewal Probability, AI Cost-Benefit Ratio, Forecast Confidence
- **New in v5.2 (5):** Currency Conversion (base aggregation), Kanban Throughput, Cycle Time (p50/p85/p95), Lead Time, WIP Aging
- **New in v5.4 (10+):** AI Rework Points, Combined Velocity, Mitigating Scenarios, Open Escalations, Phase Completion, Schedule Variance Days, Milestone Slip, Bench Cost, Risk Exposure, Scenario Alerts — all with inline formula reveal

Full reference: see [`docs/FORMULAS.md`](docs/FORMULAS.md).

---

## 7 Delivery Loss Categories

| # | Loss | Formula | Typical Impact |
|---|------|---------|---------------|
| 1 | Bench Tax | Shadow Allocation = (Actual HC - Planned HC) × Loaded Cost × Alloc% | 3-8% margin |
| 2 | Scope Creep | Scope Absorption + CR Processing Cost | 2-5% margin |
| 3 | AI Productivity Tax | AI Rework Hours + Governance Overhead + Quality Gap | 1-3% capacity |
| 4 | Sprint Leakage | (Planned - Completed) / Planned × 100 | 10-25% per sprint |
| 5 | SLA Penalty Exposure | Breach Count × Penalty Rate × Monthly Bill | 1-2% per breach |
| 6 | Attrition Knowledge Loss | Hiring + Ramp + Productivity Gap | ₹300K+ per departure |
| 7 | Pyramid Inversion | Rate Card Drift × Total Billable Hours | 1-3% annual margin |

---

## AI Governance Framework

### AI Trust Score (6-Factor Composite)
```
Score = (Provenance × 0.20) + (Review × 0.25) + (Test Coverage × 0.20)
      + (Drift × 0.15) + (Override Rate × 0.10) + (Defect Rate × 0.10)
```

### Maturity Model (5 Levels)
| Level | Score | Description |
|-------|-------|-------------|
| Unaware | 0-20 | No governance |
| Ad-Hoc | 21-40 | Individual team rules |
| Managed | 41-60 | Documented policies |
| Governed | 61-80 | Systematic enforcement |
| Optimized | 81-100 | Continuous improvement |

### AI vs. Traditional Team Comparison (12 Dimensions)
Side-by-side comparison: raw velocity, quality-adjusted velocity, defect density, test coverage, code review rejection, estimation accuracy, rework %, cost per story point, time to market, governance overhead, trust score, net productivity gain.

### 5 Governance Controls
1. Mandatory human review for all AI-generated code
2. Separate quality metrics (AI vs. human)
3. Static analysis gates in CI/CD
4. Override logging with rationale
5. Sprint-level quality retros

---

## Dual Velocity Tracking

Standard sprint velocity does not capture AI productivity gains. This system maintains two parallel tracks:

- **Standard Track:** Story points from human work only
- **AI-Augmented Track:** Story points from AI-assisted work, quality-adjusted (raw minus rework)

Tracks merge into a single velocity only after passing all 6 confidence gates:
1. Minimum 8 sprints of AI data
2. AI velocity variance < 15% CoV
3. AI defect rate ≤ 1.2× human rate
4. AI rework trending down over 3 sprints
5. Human override rate in 10-30% healthy band
6. Delivery Director sign-off

---

## Smart Ops (8 Proactive Detection Scenarios)

| # | Scenario | Trigger | Proposed Action |
|---|----------|---------|----------------|
| 1 | Resource Rebalancing | Util imbalance > 25 points between programmes | Propose named resource transfer with impact calc |
| 2 | Bench Burn Prevention | Bench > 15 days, no pipeline | Flag for redeployment or managed exit |
| 3 | Margin Leak Detection | Any of 7 loss categories exceeds threshold | Quantify impact, suggest recovery |
| 4 | AI Governance Drift | Trust Score drops > 10 pts in 2 sprints | Flag tool, recommend intervention |
| 5 | SLA Breach Prediction | Trend predicts breach within 14 days | Predict breach probability, suggest staffing |
| 6 | CPI Trajectory Alert | CPI declining 3 months AND TCPI > 1.2 | Flag recovery-improbable, suggest scope reduction |
| 7 | Customer Satisfaction Drift | CSAT drops > 0.5 pts over 2 surveys | Flag relationship risk, surface complaint themes |
| 8 | Pyramid Inversion Alert | Blended rate drifts > 3% from planned for 2+ months | Flag rate card drift, show margin impact |

Background scheduler evaluates all triggers every 15 minutes. Active/Monitoring alerts are **pushed live via Server-Sent Events to the Tab 1 ticker** — no page refresh needed. Alert chips show status (Active = red, Monitoring = amber), scenario name, and financial impact.

---

## Predictive Analytics

Every trend chart shows historical actuals (solid line) + 3-month forecast (dashed line) with confidence band.

| KPI | Forecast Horizon | Alert Trigger |
|-----|-----------------|--------------|
| CPI | 3 months | Forecast < 0.85 |
| Margin | Quarter-end | Forecast below plan by > 3 points |
| Utilisation | 3 months | Forecast billing < 65% |
| SLA | 4 weeks | Trend predicts breach within 14 days |
| CSAT | Next survey | Forecast drop > 0.5 points |

---

## Customer Intelligence (NEW)

- CSAT + NPS tracking per programme (12-month trend)
- 7-dimension expectation gap analysis (Timeline, Quality, Communication, Innovation, Cost, Responsiveness, Stability)
- Escalation log with severity, resolution time, root cause
- Renewal probability: Weighted(CSAT 0.30, DHI 0.25, Escalation 0.20, Communication 0.15, Innovation 0.10)

---

## 58 CTO/CIO/CEO Questions Answered

| Category | Questions | Tab |
|----------|-----------|-----|
| Financial Performance | 12 | Tab 5 (Margin & EVM) |
| Delivery Health | 6 | Tabs 1, 3, 4 |
| Risk & Governance | 5 | Tab 9 (Risk & Audit) |
| AI Governance | 7 | Tab 7 (AI Governance) |
| Customer & Relationship | 6 | Tab 6 (Customer Intelligence) |
| Strategic & Operational | 6 | Tab 8 (Smart Ops) |
| Estimation & Planning | 4 | Tab 3 (Delivery Health) |
| People & Capacity | 4 | Tab 8 (Smart Ops) |
| Kanban & Flow (NEW) | 3 | Tab 3B (Kanban sub-view) |
| Waterfall & Milestones (NEW) | 2 | Tab 3C (Waterfall sub-view) |
| Multi-Currency & FY (NEW) | 3 | Tabs 5, 11 |

Full mapping: see [`docs/CTO_QUESTIONS.md`](docs/CTO_QUESTIONS.md).

---

## Localisation & Multi-Currency

### Industry Presets

| Setting | Indian IT Services | US Consulting | European MSP |
|---------|-------------------|---------------|-------------|
| Base Currency | INR (₹) | USD ($) | EUR (€) |
| Gross Margin target | 35-45% | 40-55% | 30-40% |
| Billing Utilisation target | 71-76% | 65-72% | 60-68% |
| Offshore ratio | 0.65 | 0.40 | 0.30 |
| Fiscal Year | Apr–Mar | Jan–Dec | Jan–Dec |

Industry presets load default thresholds. All values fully editable after setup.

### Multi-Currency Engine (v5.2) + Live FX Refresh (v5.3)

- **Base currency** set during onboarding (any ISO 4217 code: INR, USD, EUR, GBP, AUD, SGD, etc.)
- **Per-project local currency** stored alongside base currency equivalent
- **Live FX rates** via [frankfurter.dev](https://www.frankfurter.dev/) — click "Refresh Rates" in Tab 11 to pull the latest ECB exchange rates on demand
- **currency_rates** table with effective dates — auto-populated from live API or manual entry
- **Portfolio aggregation** always in base currency; drill-down shows local amounts
- Mixed-currency portfolio example: GBP £1.2M + EUR €3.4M + INR ₹28 Cr → aggregated in USD at configured rates

### Fiscal Year & Formatting

| Option | Choices |
|--------|---------|
| Fiscal Year | Apr–Mar (India), Jan–Dec (US/EU), Oct–Sep (US Federal), Custom |
| Number Format | Indian (12,34,567), US (1,234,567), European (1.234.567) |
| Date Format | DD-MMM-YYYY, MM/DD/YYYY, YYYY-MM-DD |

---

## SDLC Framework Compatibility (NEW in v5.2)

AKB1 does not force a single delivery methodology. Each project declares its `delivery_methodology` and the dashboard adapts automatically.

| Framework | What You Upload | What Tab 3 Shows | Key Metrics |
|-----------|----------------|-------------------|-------------|
| **Scrum** | sprints.csv (story points, velocity) | 3A: Sprint burndown, cumulative flow, SPI/CPI | Sprint velocity, defect leakage, burndown |
| **Kanban** | flow_metrics.csv (throughput, cycle time, WIP) | 3B: CFD, WIP aging heatmap, throughput trend | Throughput, cycle time p50/p85/p95, lead time |
| **Waterfall** | project_phases.csv (milestones, gates) | 3C: Milestone timeline, phase variance, gate status | Phase variance days, gate pass rate, % complete |
| **SAFe** | sprints.csv + programme-level mapping | 3A: PI-level view (ART=Programme, Feature=Project) | PI predictability, feature cycle time |
| **Hybrid** | Mix of above per project | Tabs adapt per project methodology | Blended portfolio view on Tab 1 |

---

## Demo Programmes (NovaTech Solutions)

| Programme | Revenue | Team | Key Challenge |
|-----------|---------|------|--------------|
| **Phoenix** — Core Banking Migration | ₹10M | 25 | CPI 0.81, scope creep, margin compressed to 14% |
| **Atlas** — Cloud Migration | ₹8M | 18 | Margin 8% after bench, one attrition from loss |
| **Sentinel** — AI Test Automation | ₹5M | 12 | AI pilot: velocity +14%, defects 1.15x |
| **Orion** — Data Platform | ₹12M | 30 | Cash cow but bench tax absorbing ₹1.4M |
| **Titan** — Digital Commerce | ₹6M | 15 | SLA breaches, 25% attrition, CSAT dropping |
| **Hercules** — Workload Consolidation | ₹9.5M | 22 | Multi-cloud infra + data lake + ITSM (Heavy AI) |

Each programme has a distinct problem. The demo data tells a story — it teaches you how to interpret the dashboard.

**Full 5-level drill-down** (v5.3+): Every number in the dashboard traces back to individual stories/tasks. Click any sprint bar, KPI card, or flow metric to drill to L5 — assignee, points, AI flag, defects, rework hours. 403 work items across 9 projects, all invariant-verified.

**Universal formula reveal** (v5.4): Every metric on every tab has an Eye icon. Click it to see the formula, plain-English meaning, interpretation guidance, and traffic-light thresholds — inline, no page navigation required.

---

## Project Structure

```
akb1-command-center/
├── README.md                    # This file (v5.4)
├── LICENSE (MIT)
├── CHANGELOG.md                 # SemVer release log
├── docker-compose.yml
├── Makefile                     # Common dev commands
├── .env.example
├── .gitignore
├── .github/
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/          # Bug report + feature request templates
│   └── PULL_REQUEST_TEMPLATE.md
├── SECURITY.md                  # Vulnerability disclosure policy (CVSS-aligned)
├── CODE_OF_CONDUCT.md
├── docker-compose.proxy.yml     # Caddy reverse proxy overlay (Tier 1 HTTPS + Basic Auth)
├── Caddyfile                    # Caddy config (TLS, security headers, auth)
├── docs/
│   ├── ARCHITECTURE.md          # Master design document (v5.2, 44 tables, 45 formulas)
│   ├── SECURITY_GUIDE.md        # Comprehensive security guide (4-tier auth, OWASP)
│   ├── DATA_INGESTION.md        # Complete ingestion guide (xlsx + CSV)
│   ├── FORMULAS.md              # 45 formulas with 2 worked examples each
│   ├── CTO_QUESTIONS.md         # 58 questions mapped to dashboard
│   ├── EARLY_ADOPTER_FAQ.md     # Comprehensive FAQ & guide (v1.2)
│   ├── WIREFRAMES.md            # ASCII wireframes for all 11 tabs + metric dictionaries
│   ├── TECH_STACK_BENCHMARK.md  # Benchmark vs 18 open-source apps
│   ├── PRODUCTION_SDLC.md       # 7-phase lifecycle + bug-fix discipline
│   ├── MASTER_CHECKLIST.md      # Pre-release verification register
│   ├── DEMO_GUIDE.md            # NovaTech narrative walkthrough
│   ├── ROADMAP.md               # Build phases + iteration plan
│   ├── CONTRIBUTING.md          # Contributor guide (Win/Mac/Linux)
│   ├── DAILY_OPS.md             # Daily startup, troubleshooting decision tree, LaunchAgent guide
│   ├── USER_GUIDE.md            # Production-grade user guide (v5.4, 9700 words, 17 sections)
│   ├── TEST_PLAN.md             # Full test plan (116 test cases, 10 bugs documented)
│   ├── postmortems/             # Public Sev-1 postmortems (YYYY-MM-DD-<slug>.md)
│   └── csv-templates/           # 15 CSV templates with sample data
│       ├── programmes.csv
│       ├── projects.csv
│       ├── ... (13 standard templates)
│       ├── flow_metrics.csv     # Kanban flow data (NEW)
│       └── project_phases.csv   # Waterfall milestones (NEW)
├── backend/
│   ├── Dockerfile               # Multi-stage build
│   ├── requirements.txt
│   ├── alembic/                 # Schema migrations
│   │   └── versions/
│   ├── app/
│   │   ├── api/                 # REST endpoint modules
│   │   ├── models/              # SQLAlchemy + Pydantic models
│   │   ├── services/            # Formula engine, forecasts, narratives, Smart Ops
│   │   ├── config.py            # Pydantic Settings
│   │   └── seed/                # Demo data generator
│   └── tests/                   # pytest unit + integration tests
├── frontend/
│   ├── Dockerfile               # Multi-stage build
│   ├── nginx.conf
│   ├── vite.config.ts
│   └── src/
│       ├── pages/               # 11 tab pages
│       ├── components/
│       │   └── ui/
│       │       ├── MetricCard.tsx   # Universal metric card with Eye icon formula reveal (v5.4)
│       │       ├── KpiTile.tsx      # KPI tile with formula reveal support (v5.4)
│       │       └── ...              # Badge, Card, Charts, etc.
│       ├── lib/
│       │   ├── metrics.ts       # 55+ metric definitions — formula, description, interpretation, thresholds
│       │   └── ...              # api.ts, format.ts, cn.ts
│       ├── stores/              # Zustand state (uiStore: currency, theme, fiscal year)
│       └── hooks/               # React Query hooks + useAlertsStream (SSE)
├── scripts/
│   ├── setup.sh                 # First-time setup (Mac/Linux)
│   ├── autostart.sh             # macOS LaunchAgent startup script
│   ├── seed.sh                  # Reset demo data
│   ├── backup.sh                # Manual backup trigger
│   └── export-db.sh             # Export workspace
└── .pre-commit-config.yaml      # Ruff + Black + MyPy hooks
```

---

## Documentation

| Document | What It Covers |
|----------|---------------|
| [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Complete system design — 11 tabs, 44 tables, 45 formulas, 58 questions, SDLC framework compatibility, multi-currency, security architecture |
| [`SECURITY_GUIDE.md`](docs/SECURITY_GUIDE.md) | 4-tier auth strategy, OWASP Top 10 mapping, container hardening, HTTPS, API keys, RBAC, rate limiting |
| [`WIREFRAMES.md`](docs/WIREFRAMES.md) | ASCII wireframes for every tab with metric dictionaries — evaluate before you install |
| [`TECH_STACK_BENCHMARK.md`](docs/TECH_STACK_BENCHMARK.md) | Layer-by-layer benchmark against 18 open-source apps (Plausible, Grafana, Metabase, Focalboard) |
| [`PRODUCTION_SDLC.md`](docs/PRODUCTION_SDLC.md) | 7-phase lifecycle, bug-fix process, defect taxonomy, build iteration plan |
| [`MASTER_CHECKLIST.md`](docs/MASTER_CHECKLIST.md) | Single consolidated pre-release verification register — every rule, constraint, scenario |
| [`EARLY_ADOPTER_FAQ.md`](docs/EARLY_ADOPTER_FAQ.md) | Market comparison, adoption scenarios, SDLC compatibility, multi-currency, Windows setup |
| [`FORMULAS.md`](docs/FORMULAS.md) | All 45 formulas with 2 worked examples each |
| [`CTO_QUESTIONS.md`](docs/CTO_QUESTIONS.md) | 58 questions mapped to tabs, charts, and data sources |
| [`DATA_INGESTION.md`](docs/DATA_INGESTION.md) | Excel/CSV templates, auto-mapping, source-tool walkthroughs (Jira/ADO/ServiceNow/SAP), API integration |
| [`DEMO_GUIDE.md`](docs/DEMO_GUIDE.md) | NovaTech narrative walkthrough |
| [`CONTRIBUTING.md`](docs/CONTRIBUTING.md) | Code style, PR process, testing, brand guidelines, Windows/Mac/Linux dev setup |
| [`ROADMAP.md`](docs/ROADMAP.md) | 4-iteration build plan, release gates, v5.4 horizon |
| [`DAILY_OPS.md`](docs/DAILY_OPS.md) | Daily startup guide, manual startup, health checks, troubleshooting decision tree, LaunchAgent management |
| [`USER_GUIDE.md`](docs/USER_GUIDE.md) | Production-grade user guide — all 11 tabs, every metric explained, real-world applicability, data insertion formats (9700 words) |
| [`TEST_PLAN.md`](docs/TEST_PLAN.md) | Full test coverage — 116 test cases, drill-down path verification, formula accuracy validation, 10 bugs documented and resolved |

---

## Data Safety & Backup

- **Pre-flight validation** on every import: data types, required fields, referential integrity
- **Import snapshots** (`data_import_snapshots` table): one-click rollback to any prior import state
- **Automated daily backup** of SQLite database (configurable retention, default 30 days)
- **Manual backup** via `./scripts/backup.sh` or API endpoint
- **SQLite WAL mode** for concurrent read performance and crash resilience
- **Schema migrations** via Alembic with `schema_version` table — safe upgrades, never lose data
- All data stays local in your Docker volume. **Nothing leaves your machine.**

---

## Security

AKB1 ships as a **localhost-first application** — the dashboard binds to `127.0.0.1:9000` by default and is not network-accessible. For team or cloud deployments, a progressive 4-tier security model provides enterprise-grade protection without forcing complexity on single-user installs.

| Tier | Mechanism | Use Case | Setup Time |
|------|-----------|----------|-----------|
| **0 — Localhost** (default) | `127.0.0.1` binding, rate limiting, input validation | Personal laptop, demo | Zero |
| **1 — Basic Auth + HTTPS** | Caddy/Nginx reverse proxy with bcrypt passwords | Team LAN, small office | 10 min |
| **2 — SSO (OAuth2 Proxy)** | Sidecar container + Google/Azure AD/Okta/Keycloak/GitHub | Corporate VPN, cloud VM | 30 min |
| **3 — Built-in OIDC** | Native auth with fine-grained RBAC (v5.4 roadmap) | SaaS, enterprise | Code change |

### What Ships at Tier 0 (Default)

- Localhost-only port binding (`127.0.0.1:9000`)
- Rate limiting via slowapi (60 reads/min, 10 writes/min per IP)
- Input validation via Pydantic v2 (all API endpoints)
- Parameterised SQL queries (SQLAlchemy — zero raw SQL)
- Non-root container user, read-only filesystem, dropped capabilities
- CORS locked to `http://localhost:9000`
- Structured JSON logging (no sensitive data in logs)
- Container image scanning (Trivy in CI, SBOM at release)

### Tier 1+ Quick Start (HTTPS + Basic Auth)

```bash
# Launch with Caddy reverse proxy (automatic HTTPS)
docker compose -f docker-compose.yml -f docker-compose.proxy.yml up -d
# Dashboard at https://localhost — edit Caddyfile to enable basicauth
```

### Tier 2 Quick Start (SSO)

```bash
# Launch with OAuth2 Proxy sidecar
export OAUTH2_CLIENT_ID="your-client-id"
export OAUTH2_CLIENT_SECRET="your-client-secret"
export OAUTH2_COOKIE_SECRET=$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64)
docker compose -f docker-compose.yml -f docker-compose.sso.yml up -d
```

Full security guide with OWASP Top 10 mapping, container hardening details, API key management, and IdP setup: [`docs/SECURITY_GUIDE.md`](docs/SECURITY_GUIDE.md). Vulnerability disclosure policy: [`SECURITY.md`](SECURITY.md).

---

## Accessibility

- **Target:** WCAG 2.1 AA compliance
- Keyboard navigation for all interactive elements
- ARIA labels and roles on charts and data tables
- Colour contrast ratios ≥ 4.5:1 (Navy/Ice Blue/Amber palette validated)
- Screen reader compatible data tables with row/column headers
- Reduced motion support for animations

---

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | Latest 2 major |
| Firefox | Latest 2 major |
| Safari | Latest 2 major |
| Edge | Latest 2 major |

---

## Upgrading

```bash
# Pull latest images and restart
docker compose pull && docker compose up -d

# Alembic auto-applies pending schema migrations on startup
# Your data is preserved — only schema evolves
```

---

## Contributing

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md). PRs welcome for:
- Additional loss categories and Smart Ops scenarios
- Chart type improvements and new visualisations
- CSV template expansions and source-tool connectors
- Localisation (new currencies, industry presets, fiscal years)
- Direct integrations (Jira, Azure DevOps, ServiceNow connectors)
- Accessibility improvements
- Windows-specific testing and fixes

---

## License

MIT License. Use it, fork it, adapt it. Attribution appreciated but not required.

---

## Author

**Adi Kompalli** — Associate Director - Delivery | ~20 years enterprise software delivery
- LinkedIn: [/in/adikompalli](https://linkedin.com/in/adikompalli)
- GitHub: [deva-adi](https://github.com/deva-adi)
- Framework: AKB1 v5.4

---

## Release History

| Version | Highlights |
|---------|-----------|
| **v5.5.3** | Accessibility fix: AI Governance trust composite badge buttons with null programme now have `tabIndex={-1}` — keyboard Tab skips no-op buttons. 151 test cases, 47 total bugs fixed. |
| **v5.5.2** | 6 additional drill-down fixes: EVM strip 3 dead cards; SprintDrillPanel burndown/shortfall; WaterfallView button-inside-button HTML fix; VelocityFlow blend-rule fallback; RiskAudit scorecard preserves `?programme=CODE`. 150 test cases, 46 total bugs fixed. |
| **v5.5.1** | 4 additional drill-down fixes: Scrum/Kanban L3 summary MetricCards wired; Smart Ops bench-cost card scrolls to Resource pool; Customer Intelligence Communication tracker Tiles are now interactive. 144 test cases, 40 total bugs fixed. |
| **v5.5** | Complete Drill-Down Connectivity — 25 dead-end fixes across all 11 tabs. Every MetricCard, chart, accordion row, and table row now navigates with `?programme=` context. L5 backlog/flow item rows expand inline. Cross-tab navigation links added to WaterfallView, ScrumView, KanbanView, ScenarioRow, CR rows, audit trail. |
| **v5.4** | Universal Formula Reveal — Eye icon on every metric, 55+ inline definitions (MetricCard + metrics.ts). 10 audit bugs fixed. USER_GUIDE.md + TEST_PLAN.md. |
| **v5.3** | Live FX rates (frankfurter.dev), CSV import commit + rollback (Tab 11), 6th programme (Hercules) |
| **v5.2** | Multi-currency engine, SDLC framework compatibility (Kanban/Waterfall sub-views), 44 tables, 45 formulas |
| **v5.1** | Dark/light mode, SSE alerts ticker, AI governance dashboard |
| **v5.0** | Initial public release — Executive Overview, 5 programmes, EVM, Smart Ops |

---

**All formulas, thresholds, and benchmarks are based on published industry standards (PMI PMBOK, Gartner, NASSCOM, SHRM) and real portfolio governance experience. Adapt all values to your specific context.**
