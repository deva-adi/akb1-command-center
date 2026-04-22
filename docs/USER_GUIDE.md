# AKB1 Command Center — User Guide

**Version:** 5.6 | **Audience:** CTO, Associate Director, Delivery Lead, CFO, Account Director
**Last Updated:** 2026-04-22 | **Author:** Adi Kompalli

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Installation Prerequisites & Tech Stack](#2-installation-prerequisites--tech-stack)
3. [Quick Start](#3-quick-start)
4. [Data Ingestion — Complete Guide](#4-data-ingestion--complete-guide)
5. [Navigation Guide](#5-navigation-guide)
6. [Tab 1 — Executive Overview](#6-tab-1--executive-overview)
7. [Tab 2 — Programme Portfolio](#7-tab-2--programme-portfolio)
8. [Tab 3 — Delivery Health](#8-tab-3--delivery-health)
9. [Tab 4 — Velocity & Flow](#9-tab-4--velocity--flow)
10. [Tab 5 — Margin & EVM](#10-tab-5--margin--evm)
11. [Tab 6 — Customer Intelligence](#11-tab-6--customer-intelligence)
12. [Tab 7 — AI Governance](#12-tab-7--ai-governance)
13. [Tab 8 — Smart Ops](#13-tab-8--smart-ops)
14. [Tab 9 — Risk & Audit](#14-tab-9--risk--audit)
15. [Tab 10 — Reports & Exports](#15-tab-10--reports--exports)
16. [Tab 11 — Data Hub & Settings](#16-tab-11--data-hub--settings)
17. [Formula Reference & Universal Formula Reveal (v5.4)](#17-formula-reference--universal-formula-reveal-v54)
18. [Data Management](#18-data-management)
19. [Appendix — Glossary](#19-appendix--glossary)
4. [Tab 1 — Executive Overview](#4-tab-1--executive-overview)
5. [Tab 2 — Delivery Health](#5-tab-2--delivery-health)
6. [Tab 3 — Velocity & Flow](#6-tab-3--velocity--flow)
7. [Tab 4 — Margin & EVM](#7-tab-4--margin--evm)
8. [Tab 5 — Customer Intelligence](#8-tab-5--customer-intelligence)
9. [Tab 6 — AI Governance](#9-tab-6--ai-governance)
10. [Tab 7 — Risk & Audit](#10-tab-7--risk--audit)
11. [Tab 8 — Smart Ops](#11-tab-8--smart-ops)
12. [Tab 9 — KPI Studio](#12-tab-9--kpi-studio)
13. [Tab 10 — Data Hub](#13-tab-10--data-hub)
14. [Tab 11 — Reports](#14-tab-11--reports)
15. [Data Management](#15-data-management)
16. [Formula Reference](#16-formula-reference)
17. [Appendix — Glossary](#17-appendix--glossary)

---

---

## 2. Installation Prerequisites & Tech Stack

### System Requirements

Before installing AKB1 Command Center, ensure your machine meets these requirements:

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| RAM | 4 GB | 8 GB |
| Disk Space | 2 GB free | 5 GB free |
| CPU | 2 cores | 4 cores |
| Operating System | macOS 12+, Windows 10 (WSL2), Ubuntu 20.04+ | macOS 14+, Windows 11, Ubuntu 22.04 |

### Required Software

#### 1. Docker Desktop (Mandatory)

Docker Desktop bundles everything needed to run the application containers.

| Platform | Download | Version |
|----------|---------|---------|
| macOS (Apple Silicon) | [Docker Desktop for Mac (Apple Silicon)](https://www.docker.com/products/docker-desktop/) | 4.25+ |
| macOS (Intel) | [Docker Desktop for Mac (Intel)](https://www.docker.com/products/docker-desktop/) | 4.25+ |
| Windows | [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) | 4.25+ (requires WSL2) |
| Linux | [Docker Engine + Compose plugin](https://docs.docker.com/engine/install/) | 24.0+ |

**Verify installation:**
```bash
docker --version            # Should show Docker version 24.x or later
docker compose version      # Should show Docker Compose version 2.x or later
```

**Windows prerequisite:** Enable WSL 2 (Windows Subsystem for Linux 2) before installing Docker Desktop:
```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart machine, then install Docker Desktop
```

#### 2. Git (Recommended)

Required to clone the repository. Alternatively, download the ZIP from GitHub.

```bash
# macOS (via Homebrew)
brew install git

# macOS (via Xcode Command Line Tools)
xcode-select --install

# Windows
# Download from https://git-scm.com/download/win

# Ubuntu/Debian
sudo apt update && sudo apt install git
```

**Verify:** `git --version`

#### 3. Web Browser

Any modern browser works. Tested on:
- Google Chrome 120+
- Mozilla Firefox 121+
- Apple Safari 17+
- Microsoft Edge 120+

---

### Technology Stack (What Runs Inside the Containers)

You do **not** need to install any of these manually — they are all bundled inside the Docker containers. This table is for reference only.

#### Frontend Container (Port 9000)

| Component | Technology | Version |
|-----------|-----------|---------|
| UI Framework | React | 18.3 |
| Build Tool | Vite | 5.x |
| CSS Framework | Tailwind CSS | 3.4 |
| Component Library | shadcn/ui (Radix UI) | 0.8 |
| Charts | Recharts | 2.x |
| CFD Charts | Apache ECharts | 5.x |
| State (Server) | TanStack React Query | 5.x |
| State (Client) | Zustand | 4.x |
| Icons | Lucide React | 0.4 |
| HTTP Client | Axios | 1.x |
| Web Server | Nginx | 1.25 (Alpine) |
| Language | TypeScript | 5.x |

#### Backend Container (Port 9001)

| Component | Technology | Version |
|-----------|-----------|---------|
| API Framework | FastAPI | 0.111 |
| Language | Python | 3.12 |
| Data Validation | Pydantic v2 | 2.7 |
| Settings Management | Pydantic Settings | 2.x |
| ORM | SQLAlchemy | 2.0 |
| Database | SQLite (WAL mode) | 3.45 |
| Migrations | Alembic | 1.13 |
| Excel Import | openpyxl | 3.1 |
| CSV/Data Processing | pandas | 2.2 |
| Structured Logging | structlog | 24.x |
| ASGI Server | Uvicorn | 0.29 |
| Rate Limiting | slowapi | 0.1 |
| Scientific Forecast | NumPy + SciPy | 1.26 / 1.13 |
| FX Rates API | frankfurter.dev (external) | — |

#### Docker Build Specifications

```yaml
# Backend Dockerfile — Multi-stage build
FROM python:3.12-slim AS builder
  # Installs all Python dependencies into /install
FROM python:3.12-slim AS runtime
  # Non-root user: appuser (UID 1001)
  # Read-only filesystem: yes (except /data and /tmp)
  # Dropped capabilities: ALL
  # Exposed port: 9001

# Frontend Dockerfile — Multi-stage build  
FROM node:20-alpine AS builder
  # Builds React app with Vite → /app/dist
FROM nginx:1.25-alpine AS runtime
  # Serves static files + proxies /api to backend
  # Exposed port: 80 (mapped to host 9000)
```

#### docker-compose.yml Service Summary

```yaml
services:
  backend:
    build: ./backend
    ports: ["127.0.0.1:9001:9001"]   # Localhost-only — not network-accessible
    volumes: ["akb1_data:/data"]      # SQLite database persistent volume
    healthcheck: GET /health every 30s
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports: ["127.0.0.1:9000:80"]     # Localhost-only
    depends_on: [backend]
    restart: unless-stopped
```

---

## 1. Executive Summary

### What This Application Does

AKB1 Command Center is a delivery intelligence platform that gives leadership a single, real-time view across an entire portfolio of software delivery programmes. It aggregates data from projects running on any delivery methodology — Scrum, Kanban, SAFe, Waterfall, or hybrid — and presents it at five levels of granularity: Portfolio, Programme, Project, Sprint/Week, and Story/Task.

The platform is built for the reality of enterprise IT services delivery: multi-client, multi-currency, multi-methodology, with teams distributed across geographies. It answers the questions that senior leaders ask but rarely get straight answers to: Is the portfolio making or losing money? Which programmes are at risk? Is AI adoption actually improving productivity? Which clients are likely to churn?

### The Business Problem It Solves

Enterprise delivery organisations lose margin in ways that are rarely visible until it is too late: scope that was delivered but not billed, bench resources carrying cost with no allocation, AI tools generating code that increases rework rather than reducing it, and client satisfaction eroding quietly until renewal conversation collapses. Each of these problems is measurable. AKB1 measures all of them, in one place, with formulas that trace back to first principles.

### Who It Is For

| Persona | Primary Tab | Key Question |
|---------|-------------|-------------|
| CEO / COO | Tab 1 — Executive Overview | Portfolio status for the board |
| CFO / Account Director | Tab 4 — Margin & EVM | Where is margin leaking? |
| CTO / CIO | Tab 6 — AI Governance | Are AI tools trustworthy? |
| Delivery Head | Tab 2 — Delivery Health | Which programmes are at risk? |
| Programme Manager | Tab 2 — Delivery Health | Is this sprint on track? |
| Agile Coach / RTE | Tab 3 — Velocity & Flow | Is AI velocity real? |
| Account VP | Tab 5 — Customer Intelligence | Which clients will renew? |
| PMO / Compliance | Tab 7 — Risk & Audit | RAID posture and audit readiness |
| Operations Head | Tab 8 — Smart Ops | What early-warning scenarios are firing? |

### Technology Summary

- **Frontend:** React 18 + Vite + Tailwind CSS + shadcn/ui, served on port 9000
- **Backend:** FastAPI (Python 3.12) + SQLAlchemy 2.0, served on port 9001
- **Database:** SQLite WAL mode, 46 tables (v5.6 added `phase_deliverables`), volume-mounted at `/data/akb1.db`
- **Deployment:** Docker Compose, non-root containers, read-only filesystem, localhost-bound ports
- **Charts:** ECharts (interactive, clickable, drill-down capable)

---

---

## 4. Data Ingestion — Complete Guide

### Overview: 4 Ways to Get Data In

| Method | Best For | Time to First Data |
|--------|---------|-------------------|
| **Demo Data** | Exploration and evaluation | Instant |
| **CSV/Excel Upload** | Bulk historical data, migrations | 15–30 min |
| **REST API** | Automated pipelines, tool integrations | 1–4 hours |
| **Manual Entry** | Ad-hoc corrections, small datasets | Per entry |

---

### What Data Can You Load?

The application accepts data across 15 entity types. Load only what you have — everything else degrades gracefully with default values.

| Priority | Entity | Minimum for meaningful dashboard |
|----------|--------|----------------------------------|
| **Essential** | Programmes | Yes — everything depends on this |
| **Essential** | KPI Monthly | Yes — drives Tab 1 tiles and trends |
| High | EVM Monthly | Needed for Tab 5 (Margin & EVM) |
| High | Sprints | Needed for Tab 3A (Scrum delivery health) |
| High | Financials | Needed for margin waterfall |
| Medium | Flow Metrics | Needed for Tab 3B (Kanban view) |
| Medium | Project Phases | Needed for Tab 3C (Waterfall view) |
| Medium | Risks | Needed for Tab 9 (Risk & Audit) |
| Optional | AI Metrics | Needed for Tab 7 (AI Governance) |
| Optional | Resources / Bench | Needed for utilisation and bench cost |

**Minimum viable setup:** Load `programmes.csv` + `kpi_monthly.csv` and you have a working Tab 1 Executive Overview within 15 minutes.

---

### Where to Upload Data

All data uploads are done from **Tab 11 — Data Hub & Settings**, accessible from the navigation bar on the right.

Within Tab 11:
- **Guided Onboarding Wizard** — step-by-step first-time setup
- **CSV/Excel Upload Panel** — drag-and-drop file upload with column mapping
- **Import Ledger** — history of all past imports with one-click rollback per import
- **Manual Settings** — base currency, fiscal year, locale, organisation name

---

### CSV Upload Step-by-Step

1. Navigate to **Tab 11 → Data Hub**
2. Select the **entity type** from the dropdown (e.g. `programmes`, `kpi_monthly`, `sprints`)
3. **Drag and drop** your `.csv` or `.xlsx` file onto the upload zone, or click to browse
4. A **column mapping preview** appears — verify that your column headers map to the expected fields (the app auto-detects common header names)
5. Review the **pre-flight validation** — any errors in data types, missing required fields, or referential integrity issues are flagged before import
6. Click **Commit** to apply the import
7. The import appears in the **Import Ledger** with a timestamp and row count
8. If you need to undo: click **Rollback** on any ledger entry

**Commit/Rollback safety:** Every import creates a snapshot in the `data_import_snapshots` table. Rolling back an import reverses only that specific batch — other imports are unaffected.

---

### CSV Template Reference

Download templates from `docs/csv-templates/` in the repository. Each template includes:
- A header row with exact column names
- 2–3 sample rows demonstrating correct data format
- Inline comments (in a separate `_notes.txt`) explaining each column

| Template File | Entity | Key Columns | Frequency |
|--------------|--------|-------------|-----------|
| `programmes.csv` | Programme registry | `code, name, client, budget, revenue, currency, start_date, end_date, status` | One-time setup |
| `projects.csv` | Projects under programmes | `programme_code, project_name, delivery_methodology, team_size, start_date` | One-time setup |
| `kpi_monthly.csv` | Monthly KPI snapshots | `programme_code, metric_name, value, month, currency` | Monthly |
| `evm_monthly.csv` | Earned Value data | `project_id, month, planned_value, earned_value, actual_cost, bac` | Monthly |
| `sprints.csv` | Sprint data (Scrum) | `project_id, sprint_number, planned_points, completed_points, velocity, defects, rework_hours, ai_assisted_points` | Per sprint |
| `financials.csv` | Revenue and cost | `programme_code, month, revenue, cost, gross_margin, currency` | Monthly |
| `risks.csv` | Risk register | `programme_code, title, category, probability, impact, owner, status, mitigation` | Weekly–Monthly |
| `ai_tools.csv` | AI tool registry | `tool_name, vendor, category, licence_cost, status` | Quarterly |
| `ai_metrics.csv` | AI code quality | `project_id, sprint_number, ai_acceptance_rate, ai_rework_rate, time_saved_hours` | Per sprint |
| `resources.csv` | Resource pool | `programme_code, name, role, grade, utilisation_pct, cost_per_day, currency` | Monthly |
| `bench.csv` | Bench cost | `resource_id, bench_start, bench_end, daily_cost, allocation_pct` | Monthly |
| `flow_metrics.csv` | Kanban flow | `project_id, week_ending, throughput, wip_avg, cycle_p50, cycle_p85, lead_time, blocked_count` | Weekly |
| `project_phases.csv` | Waterfall phases | `project_id, phase_name, phase_sequence, planned_start, planned_end, actual_start, actual_end, gate_status, gate_approver, percent_complete` | Per phase |
| `customer_satisfaction.csv` | CSAT/NPS data | `programme_code, survey_date, csat_score, nps_score, renewal_probability, surveyed_by` | Per survey |
| `change_requests.csv` | Change request log | `project_id, cr_number, title, status, value, billing_status, approved_date` | Per CR |

---

### Importing from External Tools

#### From Jira

Jira exports sprint and backlog data in CSV format via its built-in export functions.

**Exporting Sprint Data from Jira:**

1. In Jira, open your **Board** → click **Reports** → select **Sprint Report**
2. Click **Export** (top-right) → select **CSV**
3. The export contains: `Sprint Name`, `Issue Key`, `Summary`, `Story Points`, `Status`, `Assignee`, `Labels`

**Column Mapping (Jira → AKB1):**

| Jira Column | AKB1 Column | Notes |
|-------------|-------------|-------|
| Sprint Name | `sprint_number` | Extract the sprint number from the name (e.g. "Sprint 14" → 14) |
| Story Points | `planned_points` (if Planned) or `completed_points` (if Done) | Filter by status |
| Story Points (Done) | `completed_points` | SUM of story points where Status = Done |
| Epic Link / Label | — | Use to identify AI-assisted items → populate `ai_assisted_points` |
| Flagged items | `rework_hours` | Items flagged as "impediment" or labelled "rework" |
| Bug issue type | `defects` | COUNT of issues with type = Bug within the sprint |

**Jira Advanced Export (JQL + CSV):**

For bulk historical export, use Jira's Issue Navigator:
1. Go to **Issues → Search for Issues**
2. Switch to **Advanced** (JQL) and enter:
   ```
   project = "YOUR_PROJECT" AND sprint in openSprints() ORDER BY created DESC
   ```
3. Click **Export → Export Excel CSV (current fields)**
4. In the export dialog, select the fields: `Sprint`, `Story Points`, `Status`, `Issue Type`, `Labels`, `Assignee`

**Preparing the Jira export for AKB1:**

Open the downloaded CSV in Excel or Google Sheets and:
1. Add a `project_id` column (match to your AKB1 project)
2. Create a `sprint_number` column (extract number from sprint name)
3. Add `velocity` column = SUM of story points for completed items per sprint
4. Add `defects` column = COUNT of Bug-type items per sprint
5. Save as `sprints.csv` and upload to Tab 11

---

#### From Azure DevOps (ADO)

**Exporting Work Items from ADO:**

1. Navigate to **Boards → Work Items**
2. Create a query that filters by Sprint/Iteration and Team
3. Click **Column Options** → add: `Story Points`, `State`, `Assigned To`, `Area Path`, `Tags`, `Iteration Path`
4. Click **Export to CSV** from the toolbar

**ADO Velocity Report export:**

1. Go to **Analytics → Velocity** for your team
2. Download the underlying data via the OData endpoint:
   ```
   https://analytics.dev.azure.com/{org}/{project}/_odata/v3.0-preview/WorkItemRevisions?
   $filter=TeamSK eq '{team_id}' and WorkItemType eq 'User Story'
   &$select=IterationSK,StoryPoints,State,CompletedWork
   ```

**Column Mapping (ADO → AKB1):**

| ADO Column | AKB1 Column |
|-----------|-------------|
| Iteration Path (last segment) | `sprint_number` |
| Story Points (sum, State=Closed) | `completed_points` |
| Story Points (sum, all) | `planned_points` |
| Tags containing "AI" or "Copilot" | `ai_assisted_points` |
| Work Item Type = Bug | `defects` |

---

#### From ServiceNow (ITSM / SLA Data)

**Exporting SLA incidents:**

1. Navigate to **Incidents → All Incidents**
2. Filter by: `Assignment Group`, `Opened At` (date range), `Priority`
3. Click **Export → Excel** or **Export → CSV**
4. Use the SLA report: **Reports → SLA** → export breach data

**Relevant columns for AKB1:**

| ServiceNow Column | AKB1 Usage |
|-------------------|-----------|
| `u_programme_code` | Match to programme |
| `priority` | Risk severity |
| `sla_breached` | SLA incident count |
| `resolved_at - opened_at` | Resolution time |
| `reopened_count` | Rework indicator |

---

#### From SAP (Financial Data)

**Exporting project financials from SAP PS:**

1. Use transaction **CJ13** (Project Information System) or **CJI3** (Actual costs)
2. Filter by WBS element and cost centre
3. Export via **ALV → Spreadsheet**

**SAP fields to map:**

| SAP Field | AKB1 Column |
|-----------|-------------|
| Plan Costs | `planned_value` (EVM) |
| Actual Costs | `actual_cost` (EVM) |
| Revenue | `revenue` (financials) |
| Cost Centre Group | `programme_code` |

---

#### From Microsoft Project / MS Excel Tracker

If you track programmes in an Excel spreadsheet or MS Project:

1. In MS Project: **File → Export → Save As → Excel Workbook** → choose "Selected Data" → map fields to AKB1 columns
2. In Excel: rename your columns to match AKB1 template headers (no transformation needed if names match exactly)
3. Save as `.xlsx` or `.csv` — both formats are supported for upload

---

### Data Preparation Checklist

Before uploading, verify:

- [ ] All dates are in `YYYY-MM-DD` format (e.g. `2026-04-01`)
- [ ] Currency codes use ISO 4217 (e.g. `INR`, `USD`, `GBP`, `EUR`)
- [ ] Programme codes match exactly — `programme_code` in child tables must match the `code` column in programmes.csv
- [ ] Numeric fields use decimal notation (not commas): `1234567.89` not `1,234,567.89`
- [ ] Percentages stored as decimals (0.75 = 75%) OR whole numbers depending on the column — check the template
- [ ] No blank rows in the middle of the file (trailing blank rows are fine)
- [ ] Header row is row 1 — no metadata rows above it
- [ ] File encoding is UTF-8 (Excel: File → Save As → choose CSV UTF-8)

---

## 3. Quick Start

### Accessing the Application

1. Ensure Docker Desktop is running on your machine.
2. In the project directory, start the stack:
   ```bash
   docker compose up -d
   ```
3. Open your browser and navigate to: `http://localhost:9000`
4. The application opens directly on Tab 1 (Executive Overview). No login is required in the default configuration.

### First-Time Setup

On first load with no data, the application shows a guided onboarding wizard:

1. Select your base currency (INR, USD, EUR, GBP, AUD, SGD, or any ISO 4217 code) and fiscal year.
2. Enter your organisation name and number format preference.
3. Add your first programme (name, code, budget, revenue, team size).
4. The dashboard renders immediately.

### Loading Demo Data

To explore the application with a complete, realistic dataset before entering your own data:

```bash
# macOS / Linux
./scripts/seed.sh

# Windows (PowerShell)
docker compose exec backend python -m app.seed.reset

# Via REST API
curl -X POST http://localhost:9001/api/v1/import/reset-demo
```

The demo dataset is the NovaTech Solutions portfolio: five active programmes across 12 months of history, covering healthcare, fintech, logistics, and data engineering — including an AI-augmented programme (Sentinel) and a distressed programme (Titan) to illustrate all alert states.

> **Warning:** Resetting to demo data wipes all existing data in the application.

### API Documentation

The backend exposes a self-documenting Swagger UI at: `http://localhost:9001/docs`

---

## 3. Navigation Guide

### Screen Layout

The application uses a persistent left-side navigation rail (Navy `#1B2A4A`) with the active tab highlighted. The top bar shows the currently selected base currency, fiscal year, and last-sync timestamp. A footer shows the application version and repository link.

### Tab Hierarchy and Relationships

```
PORTFOLIO LEVEL (Tab 1 — Executive Overview)
│  Portfolio health RAG, revenue, margin, avg CPI across all programmes
│
├── PROGRAMME LEVEL (Tab 2 — Delivery Health)
│   │  Per-programme drill panel from Tab 1 leads here
│   │  Methodology-adaptive: Scrum / Kanban / Waterfall views
│   │
│   ├── Sprint drill → Story/Task list (L5)
│   └── Kanban flow drill → Work item table (L5)
│
├── FINANCIAL LEVEL (Tab 4 — Margin & EVM)
│   │  7-category margin waterfall
│   └── Rate-card drift and change requests
│
├── VELOCITY INTELLIGENCE (Tab 3 — Velocity & Flow)
│   │  AI vs Traditional velocity comparison
│   └── Per-project dual velocity charts
│
├── CLIENT LEVEL (Tab 5 — Customer Intelligence)
│   │  CSAT, NPS, renewal probability
│   └── Expectation compliance radar
│
├── AI GOVERNANCE (Tab 6 — AI Governance)
│   │  Trust score, acceptance rate, tool catalogue
│   └── Override log and governance controls
│
├── RISK & COMPLIANCE (Tab 7 — Risk & Audit)
│   │  RAID register, risk exposure chart
│   └── Audit readiness scorecard
│
├── OPERATIONS INTELLIGENCE (Tab 8 — Smart Ops)
│   │  Forward-looking scenario alerts
│   └── Resource pool and bench cost
│
├── KPI MANAGEMENT (Tab 9 — KPI Studio)
│   │  Define, view, and track custom KPIs
│   └── Formula modal and trend charts
│
├── DATA INGESTION (Tab 10 — Data Hub)
│   │  CSV upload, template downloads, import history
│   └── One-click rollback to prior import
│
└── REPORTING (Tab 11 — Reports)
    └── QBR briefs, delivery reports, audit packages
```

### Universal Interaction Patterns

These patterns work consistently across all tabs:

| Interaction | How to Trigger | What Happens |
|-------------|---------------|-------------|
| Formula reveal | Click the Eye (👁) icon on any metric card | Modal shows formula, business description, interpretation guidance, and traffic-light thresholds |
| Drill-down | Click any bar, line, or data point on a chart | Panel or modal opens showing the next level of detail |
| Programme filter | Click a RAG badge or programme row | Current tab refilters to show only that programme's data |
| Hover tooltip | Hover over any numeric value | Shows local currency value, base currency equivalent, formula name |
| Export | Every chart has a context menu (three dots) | Download as PNG, CSV, or JSON |
| Cross-tab navigation | Click a MetricCard, accordion row, or expanded section nav chip | Navigates to the related tab pre-filtered to `?programme=CODE` |
| L5 row expand | Click any work item row in a FlowDrillPanel or SprintDrillPanel | Row expands inline showing all item fields; click again to collapse |
| Expanded section links | Expand any phase, milestone, scenario, CR, or audit row | Bottom of expanded section shows "Open in: Tab X \| Tab Y" chips |

### v5.6 — Drill-Fidelity Audit + Bharat Programme (8 fixes + new table + new programme)

**New in v5.6** (drill-fidelity principle — every card value must reconcile to the rows that compose it):

**Bug fixes H1–H3** (card value drilled to an unfiltered or mismatched list):
- **H1 · Kanban top-strip drill pre-filter**: Throughput / WIP / Cycle p50 / Blocked summary cards opened the week panel but didn't select the clicked metric. Now they pre-select the metric cell and apply its formula filter (Throughput → completed items, WIP → in-progress, Cycle → completed, Blocked → in-progress). Wired via a new `initialMetric` prop on the FlowDrillPanel.
- **H2 · Kanban Blocked card honest data note**: Blocked time is a weekly aggregate — per-item attribution isn't in `backlog_items`. The drill now shows an amber Data-note banner explaining the list is a proxy (in-progress items) and individual `rework_hours` won't sum to the card value. No fake column; no silent mismatch.
- **H3 · SmartOps Bench-cost card filter**: Clicking "Bench cost ₹X" scrolled to the resource pool but showed every resource. Now sets `resourceStatusFilter="Bench"` and shows a clearable filter pill in the pool header. `programmeResources` (drives bench count on card) is kept separate from `visibleResources` (respects chip) so the headline number stays stable when the chip toggles.

**Gap closures H4–H6 + H8** (cards / rows that cross-navigated without carrying context):
- **H4 · AI Governance override log filter chips**: Added per-override-type and per-outcome filter chips in the card header. Subtitle reports filtered count. Addresses "I can see 10 overrides but can't slice them by type or outcome".
- **H5 · Customer Intelligence filter chips**: Action items gain status + priority chips; SLA incident ledger gains priority + breach/met chips. Both sections show filtered count in the subtitle.
- **H6 · Risk Audit top cards pre-filter**: The 4 top KPI cards now actually pre-filter the register. Open-risks toggles an `__open__` status filter; Risk exposure toggles expected-loss ranking. Clearable filter banner in the register header summarises active filters.
- **H8 · Risk Audit compliance row programme context**: Compliance-scorecard rows cross-navigated to AI tab without the programme filter. Now they carry `?programme=` when a programme is active.

**H7 · Waterfall L5 data-model expansion** (closes the only remaining L5 gap):
- New `phase_deliverables` table (#46) — deliverable-level records per Waterfall phase with status (Pending / In Progress / Completed / Blocked), owner, planned/actual dates, planned/actual effort days, evidence link, and notes.
- New API endpoint `/api/v1/phase-deliverables?project_id=X&phase_id=Y`.
- Inside each expanded Waterfall phase, users now see an L5 deliverables table with status filter chips and a **reconcile banner** that compares the phase header's `percent_complete` against both count-based (items completed / total items) and effort-weighted (completed effort days / total planned effort days) completion. The banner flags mismatches only when BOTH views disagree with the header by more than 10 points — acknowledging that real-world `percent_complete` is usually effort-weighted, not count-based.
- TTN-STORE (NovaTech's Waterfall project) seeded with 24 deliverables across 6 phases.

**New programme — Bharat Digital Spine (BHARAT)**:
- Indian-themed end-to-end demo programme added to exercise every tab with fresh data.
- Client: Ministry of Digital Infrastructure · BAC ₹12.5M · 28 people · INR.
- Two projects: `BHARAT-UPI` (Waterfall, UPI 2.0 core modernisation, Light AI — 6 phases × 22 deliverables) and `BHARAT-CITIZEN` (Scrum, Swayam citizen mobile app, Heavy AI — 8 sprints × 53 backlog items).
- Seeded across every supporting table: 24 EVM snapshots, 7 milestones, 7 risks, 6 customer-satisfaction months, 7 expectation dimensions, 6 customer actions, 3 SLA incidents, 4 commercial scenarios, 4 loss categories, 4 rate-card rows, 3 change requests, 8 dual-velocity rows, 3 blend-rule gates, 3 AI tool assignments, 31 AI usage rows, 3 trust scores, 5 override-log entries, 8 SDLC metrics, 8 AI code metrics.
- **Every BHARAT-CITIZEN sprint card reconciles exactly** to the filtered backlog items (planned / completed / AI-assisted) — Adi's "click 120, see 120" rule is provably correct against this seed.

### v5.5.4 — Accessibility + Dead-End Fix (2 fixes)

- **Margin & EVM — Waterfall drill table row keyboard accessibility (BUG-G1)**: Waterfall breakdown rows always rendered with `role="button"` + `tabIndex={0}` even when no programme was associated, making them keyboard-focusable dead ends. Fixed by adding `tabIndex={prog ? 0 : -1}` so Tab skips rows with no programme.
- **Margin & EVM — Change Request "Open in" buttons always navigate (BUG-G2)**: The `→ Delivery Health` and `→ Risk Register` buttons in the CR expanded section used `if (prog) navigate(...)` with no fallback, silently doing nothing when the programme lookup failed. Fixed with fallback navigation to `/delivery` and `/raid` respectively.

### v5.5.3 — Accessibility Fix (1 fix)

**Fix in v5.5.3** (third audit pass — 1 accessibility issue found and fixed):

- **AI Governance — Trust composite score badge keyboard accessibility (BUG-F1)**: When a trust score badge has no associated programme (e.g. the dataset contains a trust record with a null `program_id`), the badge rendered as a `<button>` that was still reachable via the keyboard Tab key, had no `aria-label`, and its `onClick` was a no-op. Fixed by adding `tabIndex={-1}` on the button when `prog` is null, so keyboard navigation skips it entirely. Badge buttons with a valid programme remain fully keyboard-accessible with their `aria-label` and Tab focus intact.

### v5.5.2 — Complete Drill-Down Connectivity (35 fixes total)

**Additional fixes in v5.5.2** (second audit pass — 6 bugs found and fixed):

- **Delivery Health — EVM strip (eac, tcpi, % complete)**: The 3 remaining EVM MetricCards that were display-only are now wired. All 5 EVM strip cards navigate to Margin & EVM with programme context.
- **Delivery Health — Sprint drill panel (burndown_pct, shortfall)**: The burndown % and shortfall MetricCards inside the SprintDrillPanel now open the story table. Burndown % → shows completed stories; Shortfall → shows all planned stories.
- **Delivery Health — Waterfall phase/milestone MetricCards (HTML fix)**: Phase completion, schedule variance, and milestone slip MetricCards were nested inside `<button>` elements — invalid HTML that caused the Eye icon to trigger the accordion expand. Restructured to use `<div role="button">` for accordion rows so MetricCards are independent.
- **Velocity & Flow — Blend-rule gate fallback**: Gate row onClick silently did nothing if programme code lookup returned undefined. Now always navigates — to `/delivery?programme=CODE` if found, or `/delivery` as fallback.
- **Risk & Audit — Audit Readiness Scorecard programme context**: All 7 dimension rows (Financial Controls, AI Governance, Risk Management, Change Management, Quality Assurance, Process Adherence, Data Integrity) now preserve the active `?programme=CODE` query parameter when navigating to the destination tab.

### v5.5.1 — Complete Drill-Down Connectivity (29 fixes total)

**Additional fixes in v5.5.1** (applied after initial v5.5 release):

- **Delivery Health — Scrum summary cards**: The 4 L3 MetricCards (last sprint, velocity, defects, rework hours) are now fully wired. The last-sprint card opens the SprintDrillPanel inline; velocity and rework cards navigate to Velocity & Flow; the defects card navigates to Risk & Audit.
- **Delivery Health — Kanban summary cards**: The 4 L3 MetricCards (throughput, WIP, cycle P50, blocked) now open the FlowDrillPanel for the most recent week inline — keeping you in context rather than navigating away.
- **Smart Ops — Bench cost card**: The `bench_cost` summary MetricCard now smooth-scrolls to the Resource pool table below when clicked.
- **Customer Intelligence — Communication tracker tiles**: The 4 tiles (Meetings this month, Action items open, Closed, Escalations open) are now interactive. The first three scroll to the Action items section; the Escalations tile navigates to Risk & Audit with programme context.

### v5.5 — Complete Drill-Down Connectivity

Every element in the dashboard that displays a number now has at least one of the following actions:

1. **Navigate with context** — clicking a MetricCard or chart element navigates to the most relevant tab pre-filtered to the current programme (e.g. CPI card → Margin & EVM for the same programme).
2. **Expand inline** — accordion rows (phases, milestones, scenarios, override log, tool catalogue, audit trail) expand to show full detail without leaving the page.
3. **Cross-tab chip** — expanded sections include one or more "Open in: Tab Name" navigation chips at the bottom.
4. **Scroll to section** — summary cards that link to content on the same page (e.g. "Audit entries" on Risk & Audit) scroll smoothly to the relevant section.

The full drill chain from any KPI number is:

```
Portfolio summary (L1)
  → Programme breakdown panel (L2)
    → Programme detail / phase / sprint (L3)
      → Sprint / week / phase detail panel (L4)
        → Individual work items (L5, inline expand)
          → [L6] Note: live issue tracker link shown for external escalation
```

Cross-tab links available at every level carry the `?programme=CODE` URL parameter so the destination tab opens pre-filtered — no need to re-select the programme.

---

## 4. Tab 1 — Executive Overview

**URL:** `/` | **Primary Persona:** CEO, COO, Board

### Purpose

This tab is the pre-board portfolio snapshot. It is designed to be open on a screen when a senior leader arrives at a meeting and needs to brief the room in 90 seconds. Everything critical is visible above the fold.

### What Is on Screen

#### Portfolio Health Block
Three RAG-coded counters: Green (programmes on track), Amber (programmes needing attention), Red (programmes in distress). Below the counters, the total active programme count.

#### Financials Block
- Revenue (sum of all realised revenue across active programmes, FX-converted to base currency)
- Average Gross Margin (%)
- Revenue Leakage (total quantified margin loss)
- Forecast accuracy (Mean Absolute Percentage Error of last 3 months)

#### Delivery Block
- On-time percentage (programmes within schedule tolerance)
- Budget adherence percentage (programmes within ±5% of planned cost)
- Quality score (composite of defect leakage, CSAT, SLA compliance)
- Portfolio NPS (rolling 90-day)

#### Three KPI Tiles
Large-format tiles showing the three most board-visible metrics:
1. Portfolio Revenue (realised YTD)
2. Blended Margin (revenue-weighted average gross margin)
3. Average CPI (mean Cost Performance Index across active programmes)

Each tile has an Eye icon. Clicking it reveals the formula behind the number.

#### 12-Month Margin Trend Chart
Line chart showing revenue and margin over the trailing 12 months. Click any month on the line to see which programme was the largest contributor or drag that month.

#### Programme Status Table
Sortable table of all active programmes with columns: Name, Methodology, RAG, CPI, SPI, Margin, NPS. Click any row to navigate to the Delivery Health tab filtered to that programme.

#### Top Risks Card
The five highest-severity open risks across the portfolio, each with a severity badge. Click any risk to navigate to the Risk & Audit tab with that risk in focus.

#### Narrative Commentary
AI-generated weekly commentary (2–3 paragraphs) interpreting the numbers: what improved, what deteriorated, what needs a decision this week.

### Metrics on This Tab

| Metric | Formula | Green Threshold | Red Threshold |
|--------|---------|----------------|--------------|
| portfolio_revenue | SUM(revenue_recognised × FX_rate) across active programmes | Growing YoY | Declining two consecutive months |
| blended_margin | WEIGHTED_AVG(gross_margin, weight=revenue) across programmes | 38–48% | < 32% |
| avg_cpi | MEAN(latest_cpi) across active programmes | ≥ 1.0 | < 0.95 |
| on_time_pct | COUNT(on_schedule) / COUNT(total) × 100 | ≥ 85% | < 70% |
| portfolio_nps | % Promoters − % Detractors, rolling 90 days | ≥ +30 | < 0 |

### Drill-Down Flows

- **Click a RAG bucket** (e.g., the Red counter) → Programme Status Table refilters to show only Red programmes
- **Click a programme row** in the table → navigates to Delivery Health tab, scoped to that programme
- **Click a KPI Tile** → L2 Drill Panel opens showing per-programme breakdown table for that metric
- **Click a month on the Trend Chart** → Detail panel shows programme-level breakdown for that month
- **Click a Top Risk item** → Risk & Audit tab, that risk highlighted

### Real-World Scenario

You are preparing for a board meeting. Tab 1 shows: 12 Green, 4 Amber, 1 Red. Avg CPI is 0.97 (Amber — slightly below 1.0). Blended margin is 26.4% (below the 38% Green threshold). You click the CPI tile: the L2 drill panel shows that two programmes are pulling the average down (Fintech at 0.88 and Public Sector at 0.92). You click the Fintech row and navigate to Delivery Health to investigate. You now have your first 90 seconds of board narrative ready.

---

## 5. Tab 2 — Delivery Health

**URL:** `/delivery` | **Primary Persona:** Programme Manager, Delivery Head

### Purpose

This tab provides project-level delivery management visibility. It is methodology-adaptive: Scrum projects show sprint boards and velocity charts, Kanban projects show cumulative flow and cycle-time charts, Waterfall projects show phase timelines with gate status. An EVM strip runs across the top of all views.

### Sub-Views

#### A) Scrum View (default for Scrum and SAFe projects)

**Sprint Ledger:** Table of all sprints — number, dates, planned points, completed points, velocity, defects found, defects fixed, rework hours, AI-assisted points.

**Planned vs Completed Bar Chart:** Side-by-side bar chart per sprint. Hovering a bar shows the burndown percentage for that sprint. Clicking a bar opens the Sprint Drill Panel (L4 → L5): a story-level table for that sprint showing each backlog item, its assignee, points, status, AI flag, defects, and rework hours.

**Velocity Trend Chart:** Rolling velocity over the last 8 sprints with a 3-sprint moving average reference line.

**Quality Chart:** Rework hours and defect count per sprint, on the same time axis as velocity — enabling direct correlation between AI adoption and quality outcomes.

**Dual Velocity Chart (AI-Augmented Projects):** When `is_ai_augmented = true` on the project, an additional chart appears comparing AI-assisted story velocity to non-AI-assisted story velocity. The parity line shows where the two should be equal; the divergence above or below indicates net AI impact on throughput.

#### B) Kanban View

**Cumulative Flow Diagram (CFD):** Stacked area chart (ECharts) over 8 weeks, with one band per workflow stage (Backlog, In Progress, Review, Done). Expanding bands in the In Progress area indicate WIP accumulation. Narrowing bands indicate flow improvement. Click any week to see the work item table for that period.

**Cycle-Time Percentile Chart:** Scatter plot of individual item cycle times with three horizontal reference lines: p50 (median), p85 (SLA commitment line), p95 (outlier threshold). Items above the p95 line are highlighted red.

**WIP Aging Heatmap:** Items currently in progress, colour-coded by age relative to the team's p50 and p85 cycle time benchmarks: Green (below p50), Amber (p50 to p85), Red (above p85 — aging).

**Flow Drill Panel (L4 → L5):** Clicking any chart point opens the work item table for that week, showing each item's title, current stage, age in days, assignee, and aging status.

#### C) Waterfall View

**Phase Timeline:** Horizontal Gantt-style chart with planned phase bars (grey) and actual phase bars (coloured by status). Gate indicators appear at phase boundaries.

**Phase Variance Table:** Planned vs. actual days per phase, with variance in days and RAG status. Gate approval status per phase: Passed, Failed, Conditional, Pending.

**Milestones Tracker:** List of key milestones with planned and actual dates and slip magnitude.

#### D) EVM Strip (Always Visible)

Five EVM metric cards always displayed at the top of the Delivery Health tab, regardless of methodology sub-view:

| Card | Metric | Green | Red |
|------|--------|-------|-----|
| CPI | EV / AC | ≥ 1.0 | < 0.95 |
| SPI | EV / PV | ≥ 0.95 | < 0.90 |
| EAC | BAC / CPI | ≤ BAC | > BAC |
| TCPI | (BAC−EV) / (BAC−AC) | 0.90–1.10 | < 0.85 or > 1.15 |
| % Complete | EV / BAC × 100 | On trajectory | Behind trajectory |

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| burndown_pct | completed_points / planned_points × 100 | ≥ 85% | < 70% |
| velocity | completed_points / sprint_duration_weeks | Within ±10% of 3-sprint avg | Drop > 20% WoW |
| shortfall | planned_points − completed_points | ≤ 10% of planned | > 20% of planned |
| rework_hours | Actual hours in rework tasks | < 10% of total hours | > 15% |
| throughput | COUNT(items completed in week) | Stable or trending up | Falling 3 consecutive weeks |
| cycle_p50 | 50th percentile of (done_date − in_progress_date) | ≤ SLA | > SLA |
| cycle_p85 | 85th percentile of cycle time | ≤ SLA | > SLA × 1.2 |
| lead_time | Mean of (done_date − created_date) | ≤ 2× cycle_p50 | > 3× cycle_p50 |
| wip | Current items in progress | ≤ WIP limit | > WIP limit |
| phase_completion | actual_pct / planned_pct | ≥ 95% | < 85% |
| schedule_variance_days | actual_end − planned_end | ≤ 3 days | > 10 days |
| milestone_slip | Days past milestone due date | 0 | > 5 days |

### Drill-Down Flows

- **Scrum: Click a bar** in the Planned vs Completed chart → Sprint Drill Panel opens with L5 story table
- **Scrum: Click a velocity point** → Sprint summary modal with contributing stories
- **Kanban: Click a CFD week** → Work item table for that week (L5)
- **Kanban: Click a scatter point** → Item detail: title, assignee, cycle time breakdown, blockers
- **Waterfall: Click a phase bar** → Phase detail: gates, approvers, notes, milestone list

### Real-World Scenario

CPI is 0.88 on the Phoenix programme (Red). Navigate to Tab 2, select Phoenix. The Velocity Trend chart shows velocity dropped from 85 SP to 62 SP over the last three sprints. Click Sprint 22 on the Planned vs Completed chart. The L5 story table reveals that 14 of 28 stories are flagged `is_ai_assisted = true` and have an average of 6.2 rework hours each, compared to 1.8 rework hours for non-AI stories. This is an AI quality problem, not a capacity problem. Navigate to Tab 3 (Velocity & Flow) to quantify the quality parity gap.

---

## 6. Tab 3 — Velocity & Flow

**URL:** `/velocity` | **Primary Persona:** Agile Coach, Release Train Engineer, CTO

### Purpose

This tab answers a specific, high-stakes question: is AI-augmented velocity real, or is the uplift being consumed by rework, defect remediation, and quality degradation? It is the evidence base for AI investment decisions.

### What Is on Screen

#### Aggregate Stats (4 Metric Cards)
- **Combined Velocity:** Story points per sprint across all active Scrum projects
- **AI Adoption Rate:** Percentage of story points flagged as AI-assisted
- **Quality Parity:** Ratio of AI rework rate to non-AI rework rate (1.0 = parity, < 1.0 = AI is cleaner)
- **Merge-Eligible Sprints:** Count of sprints where quality parity ≥ 0.90 AND AI adoption ≥ threshold

#### Dual Velocity Chart (Per Project)
For each AI-augmented project, a side-by-side bar chart showing:
- Standard velocity (non-AI stories per sprint)
- AI raw velocity (AI stories per sprint, unadjusted)
- AI adjusted velocity (AI stories × quality parity ratio)

A parity line runs across the chart. When the AI adjusted velocity bar stays consistently above the standard velocity bar, AI is delivering verified uplift.

#### Blend-Rule Gates Table
Six gates that must all pass for an AI velocity sprint to be counted as "verified" uplift:

| Gate | Check | Target |
|------|-------|--------|
| Code generation acceptance | AI-suggested lines kept after review | ≥ 90% |
| Regression protection | No new regressions introduced | 0 |
| Test pass rate | Automated test suite pass rate | ≥ 95% |
| Defect leakage | Defects escaping to QA | ≤ 1% of completed items |
| Cycle time | Cycle time vs. non-AI baseline | ≤ baseline + 20% |
| Productivity | Net verified uplift | ≥ 10% above standard velocity |

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| standard_velocity | Completed non-AI story points / sprint | Stable trend | Declining 3 sprints |
| ai_raw_velocity | Completed AI-assisted points / sprint | — | — |
| ai_adjusted_velocity | ai_raw_velocity × quality_parity_ratio | ≥ standard_velocity | < standard_velocity |
| quality_parity | 1 − (AI_rework_rate / non_AI_rework_rate) | ≥ 0.90 | < 0.75 |
| merge_eligible | quality_parity ≥ 0.90 AND ai_adoption ≥ threshold | Qualifying sprint | Failing either gate |
| ai_rework_points | Story points requiring rework on AI-assisted stories | < 5% of AI points | > 15% of AI points |

### Drill-Down Flows

- **Click a project bar** → Sprint-level breakdown for that project, showing gate pass/fail per sprint
- **Click a gate row** in the gates table → Detail panel showing which sprints failed this gate and why

### Real-World Scenario

The Sentinel programme reports +34% velocity uplift from AI. Tab 3 shows: AI adjusted velocity is only +18% above standard velocity because quality parity is 0.82 (AI stories have 22% higher rework rate). Three of the last 8 sprints were merge-eligible. The evidence is now clear: the team is overclaiming AI velocity by 16 percentage points due to rework. The recommendation: tighten code review gates and measure again over 4 sprints before using AI velocity numbers in a client proposal.

---

## 7. Tab 4 — Margin & EVM

**URL:** `/margin` | **Primary Persona:** CFO, Account Director, Delivery Head

### Purpose

This tab shows where margin is being lost and by how much. It is the CFO's tab: every number here connects to a line item in the P&L, and the 7-category leakage breakdown makes it possible to assign accountability and corrective action to each loss.

### What Is on Screen

#### 4 Summary Metric Cards
- **Gross Margin:** (Revenue − Direct Labour) / Revenue × 100
- **Contribution Margin:** (Revenue − Direct Labour − Variable Overhead) / Revenue × 100
- **Portfolio Margin:** Blended gross margin across all active programmes
- **Net Margin:** (Revenue − All Costs) / Revenue × 100

#### 4-Layer Margin Waterfall Chart
A vertical bar chart starting from the contracted margin and showing each deduction layer:
1. Contracted margin (the signed number)
2. Less: scope creep absorbed (uncosted)
3. Less: rate concessions given post-signature
4. Less: bench drag (cost of non-billable bench resources)
5. Less: defect rework (hours spent fixing rather than building)
6. Less: FX slippage (currency movement against fixed-price contracts)
7. Less: unbilled change requests
8. Less: tool and infrastructure overruns
9. Realised margin (the actual delivered number)

#### 7 Delivery Loss Categories Chart
Horizontal bar chart showing the INR/USD/currency value of each of the 7 loss categories above, with RAG coding. Clicking a category opens a detail table showing the individual loss events that make up the total.

#### Rate-Card Drift Table
Comparison of planned resource billing rates vs. actual rates, by role and programme. Drift = (actual_rate − planned_rate) / planned_rate. Positive drift means you are billing more than planned (good). Negative drift means a concession was given.

#### Change Requests Ledger
Table of all change requests with: date, description, effort hours, billable status, processing cost, and margin impact. Filter by billable vs. absorbed to quantify the cost of uncontrolled scope.

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| gross_margin | (Revenue − Direct Labour Cost) / Revenue × 100 | 40–55% | < 30% |
| contribution_margin | (Revenue − Direct Labour − Variable Overhead) / Revenue × 100 | 25–40% | < 15% |
| portfolio_margin | SUM(gross_profit) / SUM(revenue) × 100 across programmes | 38–48% | < 32% |
| net_margin | (Revenue − All Costs) / Revenue × 100 | 15–25% | < 10% |
| EAC | BAC / CPI | ≤ BAC | > BAC |
| VAC | BAC − EAC | ≥ 0 | < −(5% of BAC) |
| rate_drift | (actual_rate − planned_rate) / planned_rate | > 0% | < −5% |

### Drill-Down Flows

- **Click a waterfall layer** → Loss event detail table for that loss category
- **Click a loss category bar** → Individual loss events: date, programme, amount, mitigation status
- **Click a change request row** → Full CR detail: description, approval chain, billing outcome

### Real-World Scenario

Portfolio margin is showing 26.4% against a 31% contracted target. The waterfall chart shows the largest single leakage is scope creep at −1.2%. Click that waterfall layer. The detail table shows three programmes with unrecovered absorbed scope: Phoenix (₹38L), Atlas (₹14L), Titan (₹6L). Phoenix is the priority. Navigate to its CR ledger — 11 change requests in the last quarter, 7 of which are marked "absorbed." The account director now has specific numbers to take into the next commercial review with the client.

---

## 8. Tab 5 — Customer Intelligence

**URL:** `/ci` | **Primary Persona:** CRO, Account VP, Delivery Head

### Purpose

This tab tracks client health and renewal risk. It makes the quantitative case for account health management: CSAT and NPS as leading indicators, renewal probability as the lagging outcome, and the expectation gap radar as the diagnostic for where intervention is needed.

### What Is on Screen

#### 4 Metric Cards
- **CSAT:** Rolling 30-day average survey score (1–10 scale)
- **NPS:** Net Promoter Score, rolling 90 days (% Promoters minus % Detractors)
- **Open Escalations:** Count of active escalations across the portfolio
- **Renewal Probability:** Composite model score for the selected programme (0–100)

#### CSAT / NPS / Renewal Trend Chart
Line chart showing all three metrics over a 12-month rolling period. Divergence between CSAT trend and NPS trend is significant: a client can score delivery well (CSAT) while still being unlikely to recommend (NPS), indicating a satisfaction-but-not-delight gap that affects renewal.

#### Expectation Compliance Radar
A 7-dimension radar chart showing the gap between what the client stated they expect and what is being measured as delivered, across:
1. Speed (delivery cadence vs. client expectation)
2. Cost (budget adherence vs. client tolerance)
3. Quality (defect rate vs. client zero-defect commitment)
4. Scope flexibility (change request turnaround)
5. Communication (steering meeting frequency vs. commitment)
6. Innovation (AI and improvement proposals)
7. Governance (transparency, real-time visibility)

Each dimension is scored −2 (severe gap) to +2 (exceeding expectation). A Gap Index sums all dimensions: −14 (worst) to +14 (best).

#### Communication Tracker
Table of scheduled vs. held steering meetings, QBRs, and executive touchpoints. Missed governance meetings are a leading indicator of renewal risk.

#### Action Items List
Open action items from the most recent steering meeting, with owner, due date, and status.

#### SLA Incident Ledger
Table of SLA breaches with severity, duration, resolution time, and penalty exposure.

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| csat | AVG(survey_score 1–10) rolling 30 days | ≥ 8.0 | < 7.0 |
| nps | % Promoters (9–10) − % Detractors (0–6) | ≥ +30 | < 0 |
| open_escalations | COUNT(escalations WHERE status='open') | 0 | ≥ 3 |
| renewal_probability | Weighted composite: CSAT × 0.30 + DHI × 0.25 + Escalation Score × 0.20 + Communication Score × 0.15 + Innovation Score × 0.10 | ≥ 80 | < 60 |

### Drill-Down Flows

- **Click a trend line point** → Month-level detail: individual survey responses, escalation events, meeting attendance
- **Click a radar dimension** → Detail panel for that dimension: evidence, gap narrative, suggested actions
- **Click an action item** → Full action detail with history

### Real-World Scenario

Renewal probability for Titan Digital Commerce is 38% (Red). The radar shows the largest gap is on speed (client expects weekly feature releases, actual cadence is monthly) and communication (8 of 12 scheduled steering meetings were held). CSAT is 6.8 and falling. The recommended playbook: request an executive sponsor meeting within 7 days, reset the communication cadence, and publish a velocity improvement plan with sprint-by-sprint commitments. Without this intervention, renewal probability will likely fall below 30% within 60 days.

---

## 9. Tab 6 — AI Governance

**URL:** `/ai` | **Primary Persona:** CTO, CIO, Head of Engineering

### Purpose

This tab is the audit artefact for AI tool usage across the portfolio. Board-level scrutiny of AI exposure is increasing. This tab provides the evidence that AI tools are governed, that their outputs are reviewed, that failures are logged, and that the productivity claims made in steering meetings are substantiated by data.

### What Is on Screen

#### 4 Metric Cards
- **AI Tools:** Count of active AI tools across the portfolio
- **Time Saved:** SUM(estimated manual hours − actual AI-assisted hours) in the current period
- **Acceptance Rate:** COUNT(AI suggestions accepted) / COUNT(AI suggestions generated) × 100
- **AI Spend:** Total AI tool licensing cost in the current period

#### Trust Composite Radar Chart
A 6-factor radar chart per programme showing the dimensions of AI trustworthiness:
1. **Quality Parity:** AI output quality vs. human baseline
2. **Acceptance Rate:** Proportion of AI suggestions kept after review
3. **Security Pass Rate:** AI-generated code cleared by security scanning
4. **Explainability:** Degree to which AI decisions/outputs can be explained
5. **Bias / Fairness:** Known bias incidents in AI-generated outputs
6. **Compliance:** AI tool usage compliant with client data agreements

#### AI Productivity Bar Chart
Side-by-side comparison per programme: time to complete equivalent tasks with and without AI assistance. This is not the same as velocity — it measures absolute time savings, not story points.

#### Governance Controls Table
Five governance control categories with compliance status:
1. Data provenance (all AI inputs traceable to approved data sources)
2. Model registry (all AI tools registered with version, vendor, risk tier)
3. Approval workflow (AI-generated artefacts reviewed before production)
4. Monitoring / drift (AI output quality monitored over time)
5. Kill-switch (ability to disable AI tooling per project without breaking delivery)

#### Override Log
Table of cases where AI-generated output was overridden by a human reviewer, with rationale and outcome classification (positive override, negative override, neutral). This log is the audit trail regulators increasingly require.

#### Tool Catalogue
List of all AI tools in use: tool name, vendor, category (code generation, testing, documentation, analysis), licence type, cost per seat, programmes using it, and risk tier (1–3).

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| trust_score | WEIGHTED_AVG(quality_parity × 0.40, acceptance_rate × 0.30, security_pass_rate × 0.30) | ≥ 70 | < 50 |
| acceptance_rate | COUNT(accepted) / COUNT(generated) × 100 | ≥ 80% | < 60% |
| time_saved | SUM(estimated_manual_hours − actual_hours) WHERE is_ai_assisted | Positive and growing | Negative or declining |
| ai_cost_benefit | (time_saved × blended_rate) / (ai_tool_cost + ai_rework_cost) | ≥ 2.0 | < 1.0 |

### Drill-Down Flows

- **Click a radar point** → Dimension detail: contributing data points, trend, evidence
- **Click a governance control row** → Control detail: evidence items, last review date, owner
- **Click a tool in the catalogue** → Tool usage breakdown: which projects, which sprints, acceptance and rework rates

### Real-World Scenario

The AI Trust Score for Phoenix is 52 (Amber, trending toward Red). The radar shows Security Pass Rate at 61% — AI-generated code is failing security scans at a high rate. The override log shows 14 overrides in the last 6 weeks, 11 classified as "negative override" (reviewer found a meaningful problem in the AI output). The action: engage the security team to review the specific Copilot configuration for Phoenix, add a mandatory security gate to the CI pipeline for AI-flagged files, and suspend AI-assisted work on security-sensitive modules until the pass rate exceeds 85%.

---

## 10. Tab 7 — Risk & Audit

**URL:** `/raid` | **Primary Persona:** PMO, Compliance, Delivery Head

### Purpose

This tab is the RAID (Risks, Assumptions, Issues, Decisions) register combined with compliance tracking and audit readiness. It supports both operational risk management (weekly review) and compliance audit preparation (quarterly).

### What Is on Screen

#### 4 Metric Cards
- **Open Risks:** Count of risks with status 'open' and review date within 14 days
- **Controls Tracked:** Count of active governance controls being monitored
- **Audit Entries:** Total entries in the audit trail log
- **Risk Exposure:** SUM(probability × impact × residual_factor) across all open risks

#### Risk Register Table
Sortable and filterable table with columns: ID, Title, Category, Probability (H/M/L), Impact (H/M/L), Exposure (currency value), Owner, Status, Review Date. Clicking a row expands a detail panel showing mitigation plan, history, linked issues, and related decisions.

#### Risk Exposure Bar Chart
Horizontal bar chart ranking programmes by total risk exposure. Clicking a programme bar drills to that programme's risk list.

#### Compliance Scorecard
Table of governance requirements with compliance percentage. Typical categories: change management adherence, steering meeting cadence, CR approval process, data handling compliance, AI tool approval status.

#### Audit Trail
Append-only chronological log of all significant events in the system: data imports, configuration changes, risk status changes, escalation opens and closes, CPI threshold breaches. This is the primary evidence for an audit team.

#### Audit Readiness Scorecard
Percentage score (0–100%) showing how complete the audit evidence package is. Items below 100% show which evidence files need re-uploading or which controls need a recent review date.

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| open_risks | COUNT(risks WHERE status='open' AND review_date ≤ TODAY + 14d) | 0 high-severity open | Any Sev-1 open > 7 days |
| risk_exposure | SUM(probability × impact × residual_factor) across open risks | Decreasing trend | Increasing week-over-week |
| audit_readiness | (Complete evidence items / Total required items) × 100 | ≥ 90% | < 75% |

### Drill-Down Flows

- **Click a risk row** → Full RAID detail: mitigation plan, owner, review history, linked issues, decisions
- **Click a risk exposure bar** → Programme risk list, sorted by exposure
- **Click an audit trail entry** → Full entry detail: who, what, when, linked data

### Real-World Scenario

Audit readiness is showing 78% (below the 90% Green threshold). Three controls need evidence re-upload. Clicking the compliance scorecard reveals: the data provenance control for the AI governance domain has an evidence file dated 90 days ago (stale) and the change management adherence control is missing the last two months of CR approval records. The PMO lead now has a specific two-item action list to reach audit readiness before the scheduled external review in 10 days.

---

## 11. Tab 8 — Smart Ops

**URL:** `/smart-ops` | **Primary Persona:** Operations Head, Delivery Head

### Purpose

This tab runs forward-looking scenario simulations across the portfolio and surfaces alerts before problems become crises. Unlike the other tabs which show what has happened, Smart Ops shows what is likely to happen if current trends continue.

### What Is on Screen

#### 4 Metric Cards
- **Active Alerts:** Count of scenario simulations currently in a breach state
- **Mitigating:** Count of alerts where a mitigation action has been acknowledged and is in progress
- **Financial Impact:** Total exposure (currency) of all active alerts
- **Bench Cost:** SUM(daily_rate × bench_days) for all currently benched resources

#### Scenario Alerts List (Expandable)
Each scenario has a name, trigger condition, affected programmes, RAG status, and breach detail. The default 8 scenarios monitored:

1. **Margin Erosion:** Gross margin declining > 2% WoW for any programme
2. **Velocity Collapse:** Sprint velocity declining > 15% WoW for two consecutive sprints
3. **Bench Drift:** Portfolio bench percentage crossing 12% (the loaded-cost threshold)
4. **Customer Dissatisfaction:** CSAT dropping below 7.5 or NPS dropping below +20
5. **AI Trust Drop:** AI Trust Score declining > 5 points WoW for any programme
6. **CPI Cliff:** CPI crossing below 0.90 and EAC now exceeding BAC
7. **Schedule Risk:** SPI below 0.85 with less than 30% programme remaining
8. **Renewal Risk:** Renewal probability dropping below 60% with contract expiry within 180 days

Clicking an alert expands it to show: the data that triggered it, the rate of change, the projected outcome if no action is taken (days until breach of a more severe threshold), and a suggested response.

#### Resource Pool Table (Expandable)
Current view of all resources, showing: name, role, current allocation, programme, bench days, daily rate, and bench cost to date. Filter by "Benched" to see only unallocated resources.

### Metrics on This Tab

| Metric | Formula | Green | Red |
|--------|---------|-------|-----|
| scenario_alerts | COUNT(scenario_simulations WHERE outcome='breach') | 0 | Any Sev-1 alert |
| bench_cost | SUM(daily_rate × bench_days) WHERE status='benched' | < ₹3,000/day equivalent | > ₹6,000/day equivalent |
| bench_pct | bench_headcount / total_headcount × 100 | < 10% | > 15% |

### Drill-Down Flows

- **Click a scenario alert** → Detail panel: triggering data, trend, projected outcome, suggested response playbook
- **Click a resource row** → Resource profile: allocation history, skills, programme fit for upcoming ramp-ups

### Real-World Scenario

Two alerts are active: Margin Erosion on FinCo (−4.8% WoW) and Bench Drift (11.8%, threshold is 12%). The Bench Drift alert is Amber, not yet Red, but the trend shows it will cross 12% in 4 days if no allocation changes are made. The resource pool table shows 4 FTE on bench with a daily cost of ₹28,000/day. Clicking the alert shows two upcoming project ramp-ups — one for Phoenix (needs 2 senior developers in 3 weeks) and one for Atlas (needs a QA lead in 5 weeks). The ops lead now has a specific match to make: allocate the two bench senior developers to Phoenix's ramp-up and eliminate the bench exposure before it triggers a Red alert.

---

## 12. Tab 9 — KPI Studio

**URL:** `/kpi` | **Primary Persona:** PMO, Delivery Head, Analytics Lead

### Purpose

KPI Studio lets users define, view, and track custom KPIs that are specific to their organisation or client commitments. Unlike the metrics on other tabs (which are fixed by the data model), KPI Studio KPIs are fully user-defined with custom formulas, units, categories, and thresholds.

### What Is on Screen

#### KPI Library Sidebar
Tree-structured list of all KPI definitions, organised by category (Delivery, Financial, People, Quality, AI, Customer, Custom). Clicking a KPI loads its trend chart and latest values.

#### KPI Trend Chart
Line chart of the selected KPI's historical values with:
- Reference lines at Green and Red thresholds
- A forecast line (dashed) for the next 3 periods, based on linear regression
- Forecast Confidence percentage displayed on the chart (R² × 100)
- Confidence band around the forecast line — wider band indicates lower R²

#### Latest Values Table
Table showing each programme's latest snapshot value for the selected KPI, with trend indicator (improving, stable, deteriorating) and days since last update.

#### Formula Modal
Clicking any KPI definition (or the Eye icon) opens a modal showing: KPI name, category, formula expression, unit, Green threshold, Red threshold, description, and last updated date. This modal is read-only; to edit, navigate to the KPI definition in the sidebar's edit mode.

### Notes on KPI Studio Data

KPI Studio reads from `KpiDefinition` records stored in the backend database. Each definition has: `kpi_code`, `name`, `formula`, `unit`, `category`, `green_threshold`, `red_threshold`, and `description`. Snapshot values are stored in `kpi_snapshots` (one row per programme per KPI per month). This is the correct table for the `kpi_monthly.csv` import — see Section 15.

---

## 13. Tab 10 — Data Hub

**URL:** `/data` | **Primary Persona:** Admin, PMO Data Manager

### Purpose

Data Hub is the import interface for bringing external data into the application. It supports CSV upload, template downloads, and import history with one-click rollback.

### What Is on Screen

#### Programme Selector
Dropdown to scope the import to a specific programme. Some imports (e.g., `backlog_items.csv`) are project-scoped; the programme selector filters the project list.

#### Import Template Downloads
Download links for all 16 CSV templates with headers and sample rows. Templates are in `docs/csv-templates/`.

#### CSV Upload
Drag-and-drop upload zone (max 50 MB). After file selection:
1. Auto-mapper suggests column → field mappings with confidence scores
2. User confirms or adjusts mappings
3. Pre-flight validation runs before any data is written
4. Validation report shown (warnings do not block; errors block)
5. Confirm import → snapshot created

#### Import History Log
Chronological list of all imports with: timestamp, filename, row count, affected tables, status (committed / failed / rolled back). Each committed import has a Rollback button. Clicking Rollback shows a confirmation modal listing the tables and row counts that will be reverted, then executes the rollback.

---

## 14. Tab 11 — Reports

**URL:** `/reports` | **Primary Persona:** All

### Purpose

Reports generates printable and exportable delivery summaries for steering committees, QBR meetings, board presentations, and audit submissions.

### Available Report Types

| Report | Format | Content |
|--------|--------|---------|
| Executive PDF | PDF | Tab 1 snapshot: RAG, financials, delivery, top risks, narrative |
| Board PowerPoint | PPTX | Slide deck: portfolio health, programme summaries, key decisions |
| EVM Export | XLSX | Full EVM data: PV, EV, AC, CPI, SPI, EAC, VAC, TCPI per programme |
| QBR Brief | PDF | Per-programme: delivery performance, customer health, risks, next steps |
| Audit Package | ZIP | Full governance evidence package: controls, AI audit trail, override log, data lineage |
| CSV Bundle | ZIP | All raw data as CSVs for external analysis |
| JSON Snapshot | JSON | Complete workspace export for backup or migration |

---

## 15. Data Management

### Data Hierarchy

All data in AKB1 is organised across five levels. Understanding this hierarchy is essential for knowing which CSV template to use and in what order to import.

```
L1 Portfolio     — Aggregate across all programmes
L2 Programme     — programmes.csv (name, code, BAC, revenue, team_size)
L3 Project       — projects.csv (references programme via program_code)
L4 Sprint/Week   — sprints.csv or flow_metrics.csv (references project)
L5 Story/Task    — backlog_items.csv (references project + sprint)
```

### Import Order

When loading from scratch, import in this exact order to satisfy foreign key constraints:

1. `programmes.csv`
2. `projects.csv`
3. All other templates (any order)

### CSV Templates Summary

| Template | Primary Use | Required Columns |
|----------|-------------|-----------------|
| programmes.csv | Create programme records (L2) | name, code, start_date, bac, revenue, team_size |
| projects.csv | Create project records (L3) | program_code, name, code, start_date, bac, team_size |
| kpi_monthly.csv | Monthly KPI snapshots (Tab 9) | programme_code, kpi_code, snapshot_date, value |
| evm_monthly.csv | EVM snapshots (Tab 4) | program_code, snapshot_date, planned_value, earned_value, actual_cost |
| sprints.csv | Sprint data for Scrum/SAFe (Tab 2) | program_code, sprint_number, planned_points, completed_points |
| backlog_items.csv | Story-level data for L5 drill-down | project_code, sprint_number, title, story_points, status, assignee |
| flow_metrics.csv | Kanban flow metrics (Tab 2B) | project_code, period_start, period_end, throughput_items, cycle_time_p50 |
| project_phases.csv | Waterfall phase timeline (Tab 2C) | project_code, phase_name, phase_sequence, planned_start, planned_end |
| risks.csv | Risk register (Tab 7) | program_code, title, probability, impact, severity, status |
| financials.csv | Revenue and cost data (Tab 4) | program_code, snapshot_date, planned_revenue, actual_revenue, planned_cost, actual_cost |
| resources.csv | Resource pool (Tab 8) | name, role, role_tier, current_program_code, utilization_pct |
| bench.csv | Bench tracking (Tab 8) | program_code, snapshot_date, planned_headcount, actual_headcount, bench_headcount |
| ai_tools.csv | AI tool catalogue (Tab 6) | name, vendor, category |
| ai_metrics.csv | AI usage metrics (Tab 6) | program_code, sprint_number, ai_lines_generated, ai_defect_count, ai_test_coverage_pct |
| change_requests.csv | CR ledger (Tab 4) | program_code, cr_date, cr_description, effort_hours, cr_value |
| losses.csv | Margin loss events (Tab 4) | program_code, snapshot_date, loss_category, amount |

### backlog_items.csv — Column Detail

This is the most detailed import template and enables the full L5 story-level drill-down in Tab 2.

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| project_code | string | Yes | Must match a code in projects.csv |
| sprint_number | integer | Yes | Must match a sprint in sprints.csv for this project |
| title | string | Yes | Story/task name, max 200 characters |
| story_points | integer | Yes | Fibonacci values typical: 1, 2, 3, 5, 8, 13, 21 |
| status | string | Yes | `completed`, `carried_over`, `added`, `in_progress`, `planned`, `blocked` |
| assignee | string | Yes | Full name as in your tracking system |
| item_type | string | No | `story` (default), `bug`, `task`, `spike` |
| is_ai_assisted | boolean | No | `true`/`false`/`1`/`0`. Default: false |
| defects_raised | integer | No | Bugs found during this item. Default: 0 |
| rework_hours | decimal | No | Hours in rework. Default: 0.0 |
| priority | string | No | `critical`, `high`, `medium`, `low` |

### kpi_monthly.csv — Column Detail

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| programme_code | string | Yes | Must match a code in programmes.csv |
| kpi_code | string | Yes | Must match a KpiDefinition record (e.g., `CPI`, `UTIL`, `MARGIN`) |
| snapshot_date | date | Yes | YYYY-MM-DD format. Typically end of month. |
| value | decimal | Yes | The KPI value. Units depend on KPI definition. |
| notes | string | No | Optional commentary on this snapshot. |

### Data Refresh Cadence

| Data Type | Recommended Cadence | Why |
|-----------|--------------------|----|
| Sprint data | End of each sprint (bi-weekly) | Velocity and defects are sprint-scoped |
| KPI snapshots | Monthly | Most KPIs are month-end measurements |
| EVM snapshots | Monthly | Aligns with financial reporting cycle |
| Risk register | Weekly | Risks change frequently |
| Customer satisfaction | Monthly or per survey | CSAT/NPS are periodic measurements |
| AI metrics | Per sprint | Aligns with sprint cadence |
| Resource / bench | Monthly | Aligns with HR reporting |

### Resetting to Demo Data

The demo dataset provides a complete, realistic portfolio for exploration and training. Resetting wipes all existing data.

```bash
# macOS / Linux
./scripts/seed.sh

# Windows (PowerShell)
docker compose exec backend python -m app.seed.reset

# Via API
curl -X POST http://localhost:9001/api/v1/import/reset-demo
```

### Backup and Restore

```bash
# Export full workspace
curl -s http://localhost:9001/api/v1/export/workspace -o workspace_export.json

# Restore from backup
curl -X POST http://localhost:9001/api/v1/import/workspace \
  -d @workspace_export.json \
  -H 'Content-Type: application/json'
```

The backend automatically backs up the SQLite database daily to `/data/backups/` inside the Docker volume (30-day retention). Configure in Tab 10 → Settings.

---

## 16. Formula Reference

Complete reference of all 45 formulas in v5.2, with formula expression, Green threshold, and Red threshold.

### EVM and Cost Performance

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 1 | BAC | Master budget agreement amount | Locked in signed SOW | Not approved |
| 7 | CPI | EV / AC | ≥ 1.0 | < 0.95 |
| 8 | EV (Earned Value) | (Work Completed % / 100) × BAC | EV ≥ PV | EV significantly < PV |
| 9 | EAC | BAC / CPI | ≤ BAC | > BAC |
| 10 | ETC | EAC − Actual Cost to Date | ≤ Remaining Budget | > Remaining Budget |
| 11 | TCPI | (BAC − EV) / (BAC − AC) | 0.90–1.10 | < 0.85 or > 1.15 |
| 12 | VAC | BAC − EAC | ≥ 0 | < −(5% of BAC) |
| 13 | SPI | EV / PV | ≥ 0.95 | < 0.90 |
| 33 | Closeout Variance | BAC − Final Actual Cost | ≥ 0 | < −(5% of BAC) |
| 34 | Schedule Variance (SV) | EV − PV | ≥ 0 | < 0 (and CV < 0 simultaneously) |
| 34 | Cost Variance (CV) | EV − AC | ≥ 0 | < 0 (and SV < 0 simultaneously) |

### Margin and Revenue

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 14 | Gross Margin % | (Revenue − Direct Labour) / Revenue × 100 | 40–55% | < 30% |
| 15 | Contribution Margin % | (Revenue − Direct Labour − Variable Overhead) / Revenue × 100 | 25–40% | < 15% |
| 16 | Portfolio Margin % | SUM(gross_profit) / SUM(revenue) × 100 | 38–48% | < 32% |
| 17 | Net Margin % | (Revenue − All Costs) / Revenue × 100 | 15–25% | < 10% |
| 25 | Revenue Leakage % | Loss Hours / Total Billable Hours × 100 | 2–5% | > 10% |
| 26 | Scope Absorption Cost | Loss Hours × Blended Cost/Hour | < 1% contract value | > 2% contract value |
| 27 | CR Processing Cost | CR Count × Avg Review Hours × Blended Rate | < 0.5% contract value | > 1.5% contract value |
| 28 | Revenue Realisation % | Realized Revenue / Committed Revenue × 100 | ≥ 90% | < 80% |

### Resource and Utilisation

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 2 | Blended Cost/Hour | (SUM(Headcount × Rate × 1.35)) / Total Billable Hours | 1.8–2.3 USD/hr | > 2.8 or < 1.2 |
| 3 | Loaded Cost/Resource | Base Rate × 1.35 × Hours/Month | ≤ Billable Revenue/Resource | > Billable Revenue |
| 4 | Billable Hours/Year | (365 − Weekends − Holidays − Leave − Admin) × 8 | 1,700–1,850 hrs | > 2,000 or < 1,400 |
| 5 | Overhead Allocation % | Programme Overhead / Direct Labour × 100 | 25–40% | > 50% or < 15% |
| 6 | Contingency % | Contingency Reserve / BAC × 100 | 10–15% | < 5% or > 25% |
| 18 | HRIS Utilisation % | Billable Hours Logged / (Allocation % × Available Hours) × 100 | 85–100% | < 75% or > 105% |
| 19 | RM Utilisation % | Allocated FTE / Available FTE × 100 | 85–95% | < 75% or > 98% |
| 20 | Billing Utilisation % | Hours Billed / Total Billable Hours Worked × 100 | 95–100% | < 90% |
| 21 | Utilisation Waterfall Loss | Available Hours − Billable Hours − Absorption Hours | < 10% total loss | > 15% |
| 22 | Shadow Allocation Cost | Bench FTE × Loaded Cost × Shadow Allocation % | > 30% offset | < 15% offset |
| 23 | Bench Runway | Available Bench Budget / Daily Bench Burn | > 30 days | < 15 days |
| 24 | Daily Bench Burn | (Bench FTE × Loaded Cost/Month) / 20 Working Days | < ₹3,000/day equiv. | > ₹6,000/day equiv. |

### Quality and Velocity

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 29 | Sprint Leakage % | (Planned − Completed) / Planned × 100 | 5–15% | > 20% |
| 30 | Rework % | Rework Hours / Total Delivery Hours × 100 | 5–10% | > 15% |
| 31 | AI Quality-Adjusted Velocity | Velocity × (1 + AI Quality Uplift %) × (1 − Rework %) | ≥ Planned trend | Declining trend |

### Portfolio Health

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 35 | Portfolio Health Index (PHI) | SUM(Programme DHI × Programme BAC) / Total BAC | > 90 | < 75 |
| 36 | Weighted Portfolio CPI | SUM(Programme CPI × Programme BAC) / Total BAC | ≥ 1.0 | < 0.95 |
| 37 | Delivery Health Index (DHI) | (0.35 × CPI) + (0.35 × SPI) + (0.15 × Quality/100) + (0.15 × Utilisation %) × 100 | > 85 | < 70 |

### Customer Intelligence

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 38 | Renewal Probability | (CSAT × 0.30) + (DHI × 0.25) + (Escalation Score × 0.20) + (Communication Score × 0.15) + (Innovation Score × 0.10) | ≥ 80 | < 60 |

### AI Governance

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 32 | AI Trust Score | (Adoption × 0.30) + (Quality Uplift × 0.25) + (Velocity Uplift × 0.25) + (Cost Avoidance × 0.20) − Failure Penalty | 70–100 | < 50 |
| 39 | AI Cost-Benefit Ratio | (Time Saved × Blended Rate) / (AI Tool Cost + AI Rework Cost) | ≥ 2.0 | < 1.0 |

### Flow Metrics (Kanban)

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 42 | Kanban Throughput | COUNT(items moved to Done in period) | Stable or trending up | Drop > 25% for 2 weeks |
| 43 | Cycle Time p50 | 50th percentile of (Done Date − In Progress Date) | ≤ SLA commitment | > SLA |
| 43 | Cycle Time p85 | 85th percentile of cycle time | ≤ SLA commitment | > SLA × 1.2 |
| 43 | Cycle Time p95 | 95th percentile of cycle time | Outlier reference | > 3× p50 |
| 44 | Lead Time Avg | Mean of (Done Date − Created Date) | ≤ 2× cycle p50 | > 3× cycle p50 |
| 45 | WIP Aging | TODAY − In Progress Date, categorised vs. p50 / p85 | ≤ 10% of WIP items Red | > 25% of WIP items Red |

### Forecasting

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 40 | Forecast Confidence | R² × 100 from linear regression on last 6–12 data points | ≥ 70% | < 40% |

### Multi-Currency

| # | Metric | Formula | Green | Red |
|---|--------|---------|-------|-----|
| 41 | Currency Conversion | Local Amount × Exchange Rate (effective date) | All projects have rates < 30 days old | Any rate > 90 days stale |

---

## 17. Appendix — Glossary

| Term | Definition |
|------|-----------|
| **AC (Actual Cost)** | Total cash spent on a programme to date, regardless of what has been delivered. |
| **BAC (Budget at Completion)** | The total approved budget for a programme as signed in the contract or SOW. |
| **Bench** | Resources that are employed but not currently allocated to a billable programme. Bench resources carry loaded cost without generating revenue. |
| **Blended Margin** | Revenue-weighted average gross margin across all active programmes. Programmes with higher revenue have proportionally more influence on the blended figure. |
| **Burndown** | The rate at which story points are completed within a sprint, tracked daily against the ideal straight-line completion trajectory. |
| **CFD (Cumulative Flow Diagram)** | A stacked area chart showing how many work items are in each stage of the workflow over time. Expanding bands between stages indicate flow constraints. |
| **CPI (Cost Performance Index)** | EV / AC. A ratio showing how much value is being delivered per unit of money spent. CPI = 1.0 means exactly on budget; CPI > 1.0 means under budget (more value per dollar); CPI < 1.0 means over budget. |
| **CR (Change Request)** | A formal request to change the agreed scope, schedule, or cost of a programme. Uncontrolled CRs that are absorbed without billing adjustment are a primary source of margin leakage. |
| **CSAT (Customer Satisfaction Score)** | Average rating from client satisfaction surveys on a 1–10 scale. Rolling 30-day window. |
| **Cycle Time** | The elapsed time from when an item moves to "In Progress" status to when it moves to "Done." Measures the speed of active work, not queue time. |
| **DHI (Delivery Health Index)** | A composite score (0–100) for a single programme, combining CPI, SPI, quality, and utilisation. The building block for PHI. Formula: (0.35 × CPI) + (0.35 × SPI) + (0.15 × Quality/100) + (0.15 × Utilisation %). |
| **EAC (Estimate at Completion)** | The forecasted total cost of the programme based on current CPI. EAC = BAC / CPI. If CPI < 1.0, EAC > BAC (projected cost overrun). |
| **ETC (Estimate to Complete)** | How much more money is needed to finish the programme. ETC = EAC − AC to date. |
| **EV (Earned Value)** | The monetary value of the work actually completed, expressed as a percentage of BAC. EV = (% complete × BAC). Measures progress independently of cost. |
| **EVM (Earned Value Management)** | The discipline of measuring project performance by comparing EV (what was done) against PV (what was planned) and AC (what was spent). CPI, SPI, EAC, TCPI, and VAC are all EVM metrics. |
| **FX (Foreign Exchange)** | Currency conversion. In AKB1, all portfolio-level aggregations convert local-currency amounts to the base currency using dated exchange rates from the `currency_rates` table. |
| **Lead Time** | The total elapsed time from when a work item is created (request received) to when it is completed. Includes queue time plus cycle time. Measures the client's experience of delivery speed. |
| **NPS (Net Promoter Score)** | Percentage of survey respondents scoring 9–10 (Promoters) minus percentage scoring 0–6 (Detractors). Ranges from −100 to +100. Correlates with contract renewal probability. |
| **PHI (Portfolio Health Index)** | Weighted composite score (0–100) of portfolio health across all programmes, weighted by BAC. PHI = SUM(Programme DHI × Programme BAC) / Total BAC. |
| **PV (Planned Value)** | The monetary value of work that was supposed to be completed by the current date, according to the original plan. PV = (planned % complete × BAC). |
| **RAID** | Risks, Assumptions, Issues, Decisions. The four categories of items tracked in a programme's governance register. |
| **RAG** | Red / Amber / Green. A traffic-light status system. Green = on track. Amber = needs attention. Red = in distress, requires escalation. |
| **Rework** | Hours spent fixing or redoing work that was delivered incorrectly. High rework rates indicate quality problems and directly erode margin. |
| **SPI (Schedule Performance Index)** | EV / PV. A ratio showing how much progress has been made relative to the plan. SPI = 1.0 means exactly on schedule; SPI > 1.0 means ahead of schedule; SPI < 1.0 means behind schedule. |
| **Sprint** | A fixed-length iteration (typically 2 weeks) used in Scrum methodology. Story points planned and completed per sprint are the primary delivery metrics for Scrum projects. |
| **TCPI (To-Complete Performance Index)** | The cost efficiency required going forward to complete the programme within remaining budget. TCPI = (BAC − EV) / (BAC − AC). A TCPI > 1.15 means the remaining work must be delivered at an unrealistically higher efficiency than current performance. |
| **Throughput** | In Kanban, the number of work items completed in a defined period (usually per week). Analogous to story point velocity for Scrum. |
| **VAC (Variance at Completion)** | The expected dollar difference between the original budget and the forecasted final cost. VAC = BAC − EAC. Positive VAC = savings; negative VAC = projected overrun. |
| **Velocity** | Story points completed per sprint. Normalised velocity accounts for sprint length variations. AI-adjusted velocity accounts for the quality cost of AI-generated code. |
| **WIP (Work in Progress)** | Items currently being actively worked on. High WIP relative to team capacity is a leading indicator of cycle time inflation and delivery unpredictability. |
| **WIP Limit** | A Kanban policy that caps the number of items allowed in any workflow stage simultaneously. Enforcing WIP limits reduces multitasking and improves flow efficiency. |

---

---

## 17. Formula Reference & Universal Formula Reveal (v5.4)

### How to Access Any Formula Instantly

Every metric in the dashboard — KPI tiles, summary cards, drill panels, waterfall charts, sprint stats, flow metrics, EVM cells, Waterfall phase rows — has a small **Eye icon** (👁) in the top-right corner of the metric card.

**Click the Eye icon** to expand an inline formula panel showing:

| Panel Section | What You See |
|--------------|-------------|
| **Formula** | The exact calculation (e.g. `Earned Value (EV) / Actual Cost (AC)`) |
| **What it measures** | Plain-English explanation of what the number represents |
| **How to use it** | Actionable guidance: when to escalate, what to do, what the number means for real decisions |
| **Thresholds** | Green / Amber / Red boundaries with exact cutoff values |

Click the Eye icon again to close the panel.

### Why This Matters

In most dashboards, numbers are black boxes. A CPI of 0.87 means nothing to a stakeholder who doesn't know what CPI is. With the formula reveal:
- A programme manager can explain any metric to a client on the spot
- A CFO can verify a margin figure without asking the delivery team
- A new joiner understands the dashboard within minutes
- Every steering committee question has an answer that traces back to a formula

### Metric Domains and Count

| Domain | Count | Tab |
|--------|-------|-----|
| Sprint (Scrum) | 9 metrics | Tab 3A — Delivery Health |
| Flow (Kanban) | 6 metrics | Tab 3B — Delivery Health |
| Earned Value Management | 5 metrics | Tab 5 — Margin & EVM |
| Dual Velocity | 7 metrics | Tab 4 — Velocity & Flow |
| Margin | 4 metrics | Tab 5 — Margin & EVM |
| Customer Intelligence | 4 metrics | Tab 6 — Customer Intelligence |
| AI Governance | 3 metrics | Tab 7 — AI Governance |
| Smart Ops | 4 metrics | Tab 8 — Smart Ops |
| Risk | 2 metrics | Tab 9 — Risk & Audit |
| Portfolio (KPI tiles) | 3 metrics | Tab 1 — Executive Overview |
| Waterfall | 3 metrics | Tab 3C — Delivery Health |
| **Total** | **55+** | **All tabs** |

---

**AKB1 Command Center v5.6**
**Maintained by:** Adi Kompalli | deva.adi@gmail.com
**New in v5.6:** Drill-fidelity audit pass — 8 fixes (H1–H8) + new `phase_deliverables` L5 table (46 tables total) + new Indian-themed BHARAT programme seeded end-to-end with exact click-to-slice reconciliation.
**New in v5.5.4:** 2 fixes — MarginEvm waterfall row keyboard dead-end (BUG-G1) and CR "Open in" buttons fallback navigation (BUG-G2).
**New in v5.5.3:** Accessibility fix — AI Governance trust badge buttons with null programme now have tabIndex={-1} so keyboard Tab skips them.
**New in v5.5.2:** 6 additional drill-down fixes — EVM strip, sprint drill panel, Waterfall button-inside-button fix, VelocityFlow fallback, RiskAudit programme context.
**New in v5.5.1:** 4 additional drill-down fixes — Scrum/Kanban summary cards, bench cost scroll, CI communication tracker tiles.
**New in v5.5:** Complete Drill-Down Connectivity — 25 dead-end fixes across all 11 tabs. Every number navigates, expands, or cross-links.
**New in v5.4:** Universal Formula Reveal — Eye icon on every metric, 55+ inline definitions, 10 audit bugs fixed
**Repository:** github.com/deva-adi/akb1-command-center
**API Documentation:** http://localhost:9001/docs
