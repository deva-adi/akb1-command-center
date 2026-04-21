# DATA INGESTION GUIDE — AKB1 Command Center v5.2

**Version:** 5.2 | **Date:** 2026-04-16
**Author:** Adi Kompalli | AKB1 Framework

---

## Overview

The AKB1 Command Center v5.2 ingests data through four modes:

1. **Demo Data** — Pre-loaded NovaTech Solutions portfolio (5 programmes × 12 months). Instant.
2. **Guided Onboarding Wizard** — Step-by-step: base currency + fiscal year → delivery methodology per project → programmes → first KPIs → dashboard. 15 minutes.
3. **Excel (.xlsx) or CSV Upload with Auto-Mapping** — Drag-and-drop Excel or CSV, map columns visually, save mapping for reuse. Pre-flight validation + import snapshot for rollback. 30-60 minutes.
4. **Manual Entry + REST API** — Forms for ad-hoc data, full REST API for automation.

All data flows into SQLite WAL mode (`/data/akb1.db` inside Docker volume) and triggers real-time validation and composite score recalculation. Every import creates a snapshot in `data_import_snapshots` for one-click rollback.

---

## Mode 1: Demo Data

### What's Pre-loaded

The demo ships with a complete narrative portfolio — NovaTech Solutions:

| Programme | Revenue | Team | Key Problem | Months |
|-----------|---------|------|-------------|--------|
| Phoenix Platform Modernization | ₹10M | 25 | CPI 0.81, scope creep, margin compressed | 12 |
| Atlas Cloud Migration | ₹8M | 18 | Razor-thin margin (8%), attrition risk | 12 |
| Sentinel Quality Engineering | ₹5M | 12 | AI pilot: velocity +14%, defects 1.15x | 12 |
| Orion Data Platform | ₹12M | 30 | Cash cow but bench tax absorbing ₹1.4M | 12 |
| Titan Digital Commerce | ₹6M | 15 | SLA breaches, 25% attrition, CSAT dropping | 12 |

Each programme includes: monthly KPI snapshots, sprint data, financial data, risk register, EVM data, AI metrics (for Sentinel), resource pool, bench tracking, customer satisfaction scores, and loss exposure records.

### Reset Behaviour

```bash
# macOS / Linux
./scripts/seed.sh

# Windows (PowerShell)
docker compose exec backend python -m app.seed.reset

# Via API (any OS)
curl -X POST http://localhost:9001/api/v1/import/reset-demo
```

**Warning:** Reset wipes ALL existing data (including any data you've uploaded) and restores the demo dataset.

### When to Use
- First-time exploration (understand what each tab shows)
- Training sessions and demos
- Testing CSV uploads without risking real data

---

## Mode 2: Guided Onboarding Wizard

### Purpose
Solve the cold-start problem. A first-time user should see their own data on the dashboard within 15 minutes.

### Workflow

| Step | What You Do | Time |
|------|------------|------|
| 1 | Select base currency (any ISO 4217: INR, USD, EUR, GBP, AUD, SGD...) + fiscal year (Apr–Mar / Jan–Dec / Oct–Sep / Custom) + industry preset | 1 min |
| 2 | Enter organisation name + number format (Indian / US / European) + date format | 30 sec |
| 3 | Add your programmes (name, code, BAC, revenue, team size — minimum 1) | 3-5 min |
| 4 | Add projects under each programme — set `delivery_methodology` per project (Scrum / Kanban / Waterfall / SAFe / Hybrid) | 2-3 min |
| 5 | Add your first KPI snapshot (CPI, utilisation, margin for each programme — 1 month minimum) | 3-5 min |
| 6 | See your dashboard | Instant |

### Industry Presets

| Setting | Indian IT Services | US Consulting | European MSP | Custom |
|---------|-------------------|---------------|-------------|--------|
| Currency | INR (₹) | USD ($) | EUR (€) | Your choice |
| Gross Margin target | 35-45% | 40-55% | 30-40% | Editable |
| Billing Utilisation target | 71-76% | 65-72% | 60-68% | Editable |
| Loaded Cost range | ₹50K-₹120K | $80K-$200K | €60K-€150K | Editable |
| Bench % healthy | 10-15% | 8-12% | 12-18% | Editable |
| Attrition benchmark | 15-22% | 12-18% | 8-15% | Editable |
| Offshore ratio default | 0.65 | 0.40 | 0.30 | Editable |

All presets are stored in `app_settings` and fully editable in Tab 11 (Data Hub & Settings) after initial setup.

### Minimum Viable Data

The dashboard renders meaningful charts with just **2 data inputs:**

1. **Programmes** — name, code, BAC, revenue, team_size
2. **KPI Monthly** — program_code, snapshot_date, CPI value, utilisation, margin

Everything else gracefully degrades: "No data yet — upload [template name] to see this section."

---

## Mode 3: Excel (.xlsx) or CSV Upload with Auto-Mapping (UPDATED in v5.2)

### Supported File Formats

| Format | Engine | Notes |
|--------|--------|-------|
| `.xlsx` (Excel) | openpyxl + pandas | **Recommended.** Native Excel import — no "Save As CSV" step needed. Reads first sheet by default; multi-sheet support planned for v5.3. |
| `.csv` | pandas | Comma, semicolon, tab, or pipe delimited. Auto-detected. |

### Excel Preparation Guide

Before uploading an Excel file, check these common pitfalls:

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Merged cells | openpyxl reads merged cells as NaN except the top-left cell | Unmerge all cells before export |
| Hidden columns | Hidden columns are still read by openpyxl | Unhide and review, or delete unwanted columns |
| Formulas vs. values | openpyxl reads cell values (not formulas) by default — correct for AKB1 | No action needed |
| Date formatting | Excel serial dates may not parse correctly | Format date columns as Text or YYYY-MM-DD before export |
| Header row not in row 1 | Auto-mapper expects headers in the first row | Move or delete rows above the header |
| Sheet name | Reads the first sheet only | Move your data to Sheet1, or rename the target sheet |
| File size | Max 50 MB | Split large files by programme or time period |

### Upload Workflow

1. Navigate to **Tab 11 (Data Hub & Settings) → Data Upload**
2. Drag-and-drop your `.xlsx` or `.csv` file (max 50 MB)
3. **Auto-Mapping:** The app reads your column headers and suggests matches:
   ```
   Your column "Programme Name"  → programs.name       [95% confidence]
   Your column "Budget"          → programs.bac        [82% confidence]
   Your column "Actual Spend"    → evm_snapshots.actual_cost  [Suggested: verify]
   Your column "% Complete"      → evm_snapshots.percent_complete [90%]
   Your column "Risk Count"      → [No match — skip or create custom]
   ```
4. Confirm or adjust mappings
5. **Mapping saved** — next time you upload the same format, it auto-applies
6. **Pre-flight validation:** Data types, required fields, referential integrity, value ranges checked before any data touches the database
7. Review validation report (green = pass, amber = warning, red = block)
8. Confirm import → **snapshot created** in `data_import_snapshots` for one-click rollback

### Import Safety (NEW in v5.2)

- **Pre-flight validation** runs BEFORE data is written: type checks, required field checks, FK reference checks, range checks
- **Import snapshot** saved to `data_import_snapshots` table with timestamp, file hash, row count, and affected tables
- **One-click rollback** to any prior snapshot from Tab 11 → Import History
- **Duplicate detection** on composite keys — duplicates rejected with clear error messages
- **Original file preserved** — AKB1 never modifies your source file

### 16 CSV/Excel Templates

Templates with headers + 2-3 sample rows are in `docs/csv-templates/`:

| # | Template | Maps To | Required Columns | Optional Columns |
|---|----------|---------|-----------------|------------------|
| 1 | **programmes.csv** | programs | name, code, start_date, bac, revenue, team_size | client, end_date, status, offshore_ratio, delivery_model, currency_code |
| 2 | **projects.csv** | projects | program_code, name, code, start_date, bac, team_size | end_date, revenue, tech_stack, is_ai_augmented, ai_augmentation_level, **delivery_methodology** |
| 3 | **kpi_monthly.csv** | kpi_snapshots | program_code, snapshot_date, kpi_code, value | trend, notes |
| 4 | **evm_monthly.csv** | evm_snapshots | program_code, snapshot_date, planned_value, earned_value, actual_cost | project_code, bac, percent_complete |
| 5 | **risks.csv** | risks | program_code, title, probability, impact, severity, status | project_code, category, owner, mitigation_plan, description |
| 6 | **sprints.csv** | sprint_data | program_code, sprint_number, planned_points, completed_points | project_code, start_date, end_date, defects_found, defects_fixed, rework_hours, team_size, ai_assisted_points, **iteration_type**, **estimation_unit** |
| 7 | **backlog_items.csv** (**NEW v5.3**) | backlog_items | project_code, sprint_number, title, story_points, status, assignee | item_type, is_ai_assisted, defects_raised, rework_hours, priority |
| 8 | **financials.csv** | commercial_scenarios | program_code, snapshot_date, planned_revenue, actual_revenue, planned_cost, actual_cost | project_code, gross_margin_pct, contribution_margin_pct, portfolio_margin_pct, net_margin_pct, **currency** |
| 9 | **ai_tools.csv** | ai_tools | name, vendor, category | version, license_type, cost_per_seat, status |
| 10 | **ai_metrics.csv** | ai_code_metrics | program_code, sprint_number, ai_lines_generated, ai_defect_count, ai_test_coverage_pct | project_code, ai_lines_accepted, ai_review_rejection_pct, human_defect_count, human_test_coverage_pct |
| 11 | **resources.csv** | resource_pool | name, role, role_tier, current_program_code, utilization_pct | current_project_code, skill_set, bench_days, loaded_cost_annual, status |
| 12 | **bench.csv** | bench_tracking | program_code, snapshot_date, planned_headcount, actual_headcount, bench_headcount | loaded_cost_per_head, shadow_allocation_cost, allocation_method |
| 13 | **change_requests.csv** | scope_creep_log | program_code, cr_date, cr_description, effort_hours, cr_value | project_code, processing_cost, status, margin_impact, is_billable |
| 14 | **losses.csv** | loss_exposure | program_code, snapshot_date, loss_category, amount | percentage_of_revenue, detection_method, mitigation_status |
| 15 | **flow_metrics.csv** | flow_metrics | project_code, period_start, period_end, throughput_items, cycle_time_p50 | wip_avg, wip_limit, cycle_time_p85, cycle_time_p95, lead_time_avg, blocked_time_hours |
| 16 | **project_phases.csv** | project_phases | project_code, phase_name, phase_sequence, planned_start, planned_end | actual_start, actual_end, percent_complete, gate_status, gate_approver, gate_date, notes |

> **Bold columns** (`delivery_methodology`, `iteration_type`, `estimation_unit`, `currency`) are new in v5.2 for SDLC framework and multi-currency support.

---

## Understanding the Data Hierarchy (5 Levels)

AKB1 is designed with a strict bottom-up data architecture. Every aggregate number on the dashboard is composed from lower-level records, and you can drill into each level to see the raw data.

```
Level 1 — Portfolio
    Aggregate across all programmes. Example: "Total portfolio CPI = 0.87"

    Level 2 — Programme
        Per-programme breakdown. Example: "Phoenix CPI 0.81 / Atlas CPI 0.93"

        Level 3 — Project
            Delivery tab filtered by project. Example: "PHOE-CBM sprints"

            Level 4 — Sprint
                Sprint aggregate. Example: "Sprint 24: planned=90, completed=68, velocity=68"

                Level 5 — Story / Task / Bug / Spike
                    Individual backlog items. Example:
                    "Payment Orchestration Layer — 13pts — Arjun Kumar — completed — 11h rework"
                    "CBDC Integration Module — 22pts — Lakshmi Iyer — carried_over"
```

### How L5 (backlog_items) connects to L4 (sprint_data)

The database enforces this invariant:

```
sum(story_points WHERE status IN ('completed', 'added'))  ==  sprint_data.completed_points
sum(story_points WHERE status != 'added')                 ==  sprint_data.planned_points
```

`status = 'added'` represents stories added mid-sprint (not in the original plan) — this is how AI-augmented teams like SNTL-AUTO show velocity > planned (e.g., completed=92 against planned=70).

### What to upload for each level

| You want to see... | Upload this | Minimum data |
|--------------------|------------|--------------|
| Portfolio KPIs & margins | programmes.csv + kpi_monthly.csv | 1 programme + 1 month KPIs |
| Sprint velocity charts | sprints.csv | 1 project + 1 sprint |
| Story-level drill-down | backlog_items.csv | project_code + sprint_number + title + story_points + status |
| Kanban flow metrics | flow_metrics.csv | 1 Kanban project + 4 weeks |
| EVM & cost tracking | evm_monthly.csv | 1 programme + 1 EVM snapshot |
| Risk register | risks.csv | 1 programme + 1 risk |

### backlog_items.csv — detailed column guide

| Column | Type | Required | Values / Notes |
|--------|------|----------|----------------|
| `project_code` | string | ✅ | Must match a code in projects.csv (e.g., `PHOE-CBM`) |
| `sprint_number` | integer | ✅ | Must match a sprint in sprints.csv for the same project |
| `title` | string | ✅ | Story / task name (max 200 chars) |
| `story_points` | integer | ✅ | Fibonacci values typical: 1, 2, 3, 5, 8, 13, 21 |
| `status` | string | ✅ | `completed` — done this sprint; `carried_over` — not done, rolls to next; `added` — added mid-sprint and completed (explains AI over-delivery) |
| `assignee` | string | ✅ | Full name as it appears in your org (e.g., "Arjun Kumar") |
| `item_type` | string | ❌ | `story` (default) / `bug` / `task` / `spike` |
| `is_ai_assisted` | boolean | ❌ | `true` / `false` / `1` / `0`. Default: false |
| `defects_raised` | integer | ❌ | Number of bugs/defects found during this item. Default: 0 |
| `rework_hours` | decimal | ❌ | Hours spent on rework for this item. Default: 0.0 |
| `priority` | string | ❌ | `critical` / `high` / `medium` / `low` |

### Validation rules for backlog_items

Before import, the system checks:
1. `project_code` exists in projects table
2. `sprint_number` exists in sprint_data for that project
3. `sum(story_points WHERE status != 'added')` within ±5% of `sprint_data.planned_points` (warning, not block)
4. `sum(story_points WHERE status IN ('completed','added'))` within ±5% of `sprint_data.completed_points` (warning, not block)
5. `assignee` free text — no FK constraint (team members aren't a separate table yet)
6. `story_points` range 0–99 (warning if above)

The ±5% tolerance is intentional: real data is messy and partial uploads are valid. The warning appears in the import report but does not block the import.

### Column Naming Convention

The Command Center uses `program_code` (not `programme_id`) as the join key across all CSVs. This must match the `code` field in your programmes.csv exactly.

Example: If your programme is coded `PHX` in programmes.csv, then all related CSVs must use `program_code = PHX`.

### Import Order

If loading from scratch, import in this order to satisfy foreign key relationships:

1. **programmes.csv** (creates programme records)
2. **projects.csv** (references programmes)
3. Everything else (references programmes and optionally projects)

### Handling Messy Data

**My column names don't match the templates:**
The CSV Auto-Mapper handles this. It uses fuzzy matching to suggest mappings. "Budget" → `bac`, "Actual Cost" → `actual_cost`, "Programme Name" → `name`. Adjust any incorrect suggestions and save the mapping.

**My dates are in DD/MM/YYYY format:**
The importer auto-detects common date formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, DD-Mon-YYYY. If detection fails, the validation report will flag the issue.

**I have extra columns the system doesn't recognise:**
Extra columns are safely ignored. The auto-mapper shows them as "[No match — skip]". Your original data is never modified.

**My CSV uses semicolons instead of commas:**
The importer auto-detects delimiters: comma, semicolon, tab, pipe.

---

## Mode 4: Manual Entry + REST API

### Manual Entry Forms

Tab 11 (Data Hub & Settings) provides web forms for each entity type:
- Create/Edit Programme
- Create/Edit Project
- Log Monthly KPI Snapshot
- Log EVM Snapshot
- Register Risk
- Log Sprint Data
- Enter Financial Data
- Register AI Tool
- Log AI Metrics
- Add Resource to Pool
- Log Change Request
- Record Delivery Loss
- Enter Customer Satisfaction Survey

Each form has real-time validation, auto-complete for programme/project codes, and immediate dashboard refresh.

### REST API

Full API documentation is auto-generated at `http://localhost:9001/docs` (Swagger/OpenAPI).

**Base URL:** `http://localhost:9001/api/v1/`

#### Core Endpoints

```bash
# Programmes + Projects
GET    /programs                          # List all programmes
GET    /programs/{id}                     # Get single programme
GET    /programs/{id}/projects            # List projects under programme
POST   /programs                          # Create programme
POST   /projects                          # Create project
PUT    /programs/{id}                     # Update programme
PUT    /projects/{id}                     # Update project

# KPIs
GET    /kpis                              # List KPI definitions
GET    /kpis/{program_id}/snapshots       # Get KPI history for programme
GET    /kpis/{program_id}/forecasts       # Get forecasts (NEW)
POST   /kpis/snapshots                    # Create KPI snapshot

# EVM (NEW)
GET    /evm/{program_id}                  # Get EVM data for programme
POST   /evm/snapshots                     # Create EVM snapshot

# Risks
GET    /risks                             # List all risks
GET    /risks/{program_id}               # Risks for programme
POST   /risks                             # Create risk
PUT    /risks/{id}                        # Update risk

# Sprints
GET    /sprints/{program_id}             # Sprint history for programme
POST   /sprints                           # Create sprint record

# Financials
GET    /financials/{program_id}          # Financial data for programme
POST   /financials                        # Create financial record

# AI Governance
GET    /ai/tools                          # List AI tools
GET    /ai/trust-scores/{program_id}     # Trust scores for programme
GET    /ai/metrics/{program_id}          # AI metrics for programme
GET    /ai/comparison/{program_id}       # AI vs Traditional comparison (NEW)
POST   /ai/override-log                   # Log AI override

# Smart Ops
GET    /smartops/alerts                   # Active alerts (NEW)
GET    /smartops/executions               # Scenario execution history
POST   /smartops/acknowledge/{id}        # Acknowledge alert (NEW)

# Customer Intelligence (NEW)
GET    /customer/{program_id}            # Customer data for programme
POST   /customer/satisfaction             # Log satisfaction survey
GET    /customer/{program_id}/renewal-score  # Get renewal probability

# Narratives (NEW)
GET    /narratives/portfolio              # Portfolio summary narrative
GET    /narratives/{program_id}          # Programme narrative
GET    /narratives/qbr-brief/{program_id} # QBR brief narrative

# Reports (NEW)
GET    /reports/qbr/{program_id}         # Printable QBR PDF
GET    /reports/audit-package             # Audit evidence ZIP

# Data Management
POST   /import/csv                        # Upload CSV
POST   /import/csv/auto-map              # Auto-map CSV columns (NEW)
POST   /import/reset-demo                 # Reset to demo data
GET    /export/workspace                  # Export all data as JSON
POST   /import/workspace                  # Import from export

# Settings
GET    /settings                          # Get all settings
PUT    /settings                          # Update settings
POST   /settings/locale                   # Set locale/currency (NEW)
```

#### Example: Create a Programme via API

```bash
curl -X POST http://localhost:9001/api/v1/programs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phoenix Platform Modernization",
    "code": "PHX",
    "client": "Global Banking Corp",
    "start_date": "2025-01-15",
    "end_date": "2026-12-31",
    "bac": 6800000,
    "revenue": 10000000,
    "team_size": 25,
    "offshore_ratio": 0.65,
    "delivery_model": "T&M",
    "currency_code": "INR"
  }'
```

#### Example: Post a KPI Snapshot

```bash
curl -X POST http://localhost:9001/api/v1/kpis/snapshots \
  -H "Content-Type: application/json" \
  -d '{
    "program_id": 1,
    "kpi_id": 7,
    "snapshot_date": "2026-03-01",
    "value": 0.81,
    "trend": "declining",
    "notes": "CPI dropped due to 3 uncontrolled CRs"
  }'
```

#### Example: Automated Ingestion Script (Python)

```python
import requests
import csv
from datetime import datetime

API_BASE = "http://localhost:9001/api/v1"

# Read your exported Jira sprint data
with open("jira_sprint_export.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        payload = {
            "program_id": 1,  # Map your Jira project to Command Center programme ID
            "sprint_number": int(row["Sprint"]),
            "start_date": row["Start Date"],
            "end_date": row["End Date"],
            "planned_points": int(row["Committed"]),
            "completed_points": int(row["Completed"]),
            "defects_found": int(row.get("Bugs Created", 0)),
            "ai_assisted_points": int(row.get("AI Points", 0))
        }
        resp = requests.post(f"{API_BASE}/sprints", json=payload)
        print(f"Sprint {payload['sprint_number']}: {resp.status_code}")
```

---

## New in v5.2: Kanban Flow Metrics Template Walkthrough

### When to Use
Use `flow_metrics.csv` when your project uses **Kanban** (or any methodology tracking flow rather than sprints). Set `delivery_methodology = 'Kanban'` on the project in `projects.csv`.

### Template Structure

```csv
project_code,period_start,period_end,throughput_items,wip_avg,wip_limit,cycle_time_p50,cycle_time_p85,cycle_time_p95,lead_time_avg,blocked_time_hours
DATAOPS-001,2026-03-01,2026-03-07,7,14.2,18,3.4,6.4,9.1,9.2,4.5
```

### Column Guide

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| project_code | Yes | Text | Must match `code` in projects.csv |
| period_start | Yes | Date (YYYY-MM-DD) | Start of measurement period (usually weekly) |
| period_end | Yes | Date (YYYY-MM-DD) | End of measurement period |
| throughput_items | Yes | Integer | Items completed in the period |
| cycle_time_p50 | Yes | Decimal (days) | Median cycle time (50th percentile) |
| wip_avg | No | Decimal | Average work-in-progress items during period |
| wip_limit | No | Integer | Team's WIP limit policy |
| cycle_time_p85 | No | Decimal (days) | 85th percentile cycle time |
| cycle_time_p95 | No | Decimal (days) | 95th percentile cycle time |
| lead_time_avg | No | Decimal (days) | Average lead time (request → delivery) |
| blocked_time_hours | No | Decimal | Total hours items were blocked |

### What Tab 3B Shows
- **Cumulative Flow Diagram** (ECharts): stacked area chart showing items in each workflow stage over time
- **WIP Aging Heatmap**: items currently in progress, coloured by age (green < p50, amber p50–p85, red > p85)
- **Throughput Trend**: weekly throughput with 4-week moving average
- **Cycle Time Scatter Plot**: each item plotted by completion date vs. cycle time, with p50/p85/p95 lines

### How to Collect This Data
- **Jira Kanban:** Board Settings → Control Chart → export to CSV, or use Jira REST API (`/rest/agile/1.0/board/{boardId}/issue`)
- **Azure DevOps:** Analytics → Cumulative Flow → export, or OData query
- **Trello:** Use Butler + export, or third-party plugin (Corrello, Screenful)
- **Manual:** Track weekly: count items moved to Done, note WIP count, calculate cycle times from "In Progress" → "Done" timestamps

---

## New in v5.2: Waterfall Project Phases Template Walkthrough

### When to Use
Use `project_phases.csv` when your project uses **Waterfall** (or any phase-gate methodology). Set `delivery_methodology = 'Waterfall'` on the project in `projects.csv`.

### Template Structure

```csv
project_code,phase_name,phase_sequence,planned_start,planned_end,actual_start,actual_end,percent_complete,gate_status,gate_approver,gate_date,notes
RETAILCO-POS,Requirements,1,2025-06-01,2025-07-31,2025-06-01,2025-07-29,100,passed,J.Wilson,2025-08-01,On time
```

### Column Guide

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| project_code | Yes | Text | Must match `code` in projects.csv |
| phase_name | Yes | Text | Phase name (Requirements, Design, Development, Testing, UAT, Deployment, etc.) |
| phase_sequence | Yes | Integer | Order (1, 2, 3...). Determines timeline layout. |
| planned_start | Yes | Date | Baselined phase start |
| planned_end | Yes | Date | Baselined phase end |
| actual_start | No | Date | When phase actually started (blank if not started) |
| actual_end | No | Date | When phase actually ended (blank if in progress or not started) |
| percent_complete | No | Integer (0-100) | Current % completion |
| gate_status | No | Text | `pending`, `passed`, `failed`, `conditional` |
| gate_approver | No | Text | Name of gate review approver |
| gate_date | No | Date | Date gate review occurred |
| notes | No | Text | Variance notes, blockers, dependencies |

### What Tab 3C Shows
- **Milestone Timeline**: horizontal bar chart with planned (grey) vs. actual (coloured by status) phase durations
- **Phase Variance Table**: planned vs. actual days per phase, variance in days, red/amber/green status
- **Gate Approval Status**: badges per phase (passed ✅ / failed ❌ / conditional ⚠️ / pending ⏳)
- **Critical Path Indicator**: highlights phases where slip cascades to project end date

### How to Collect This Data
- **MS Project:** File → Export → CSV, then map columns
- **Smartsheet:** Export to Excel, select milestone columns
- **Primavera P6:** Activities → Export → CSV (filter to Level 1 phases)
- **Manual:** Create one row per phase with your planned dates, update actuals as phases progress

---

## Data Sources — How to Get Data From Your Existing Tools

### From Jira (Step-by-Step)

**For Scrum/SAFe teams → sprints.csv:**
1. Open your Jira project → Board → Sprint Report
2. Select the completed sprint
3. Note: Committed = `planned_points`, Completed = `completed_points`, Bugs Created = `defects_found`
4. Export or manually record into `sprints.csv`
5. Set `iteration_type = 'Sprint'` and `estimation_unit = 'StoryPoints'`

**For Kanban teams → flow_metrics.csv:**
1. Open your Jira Kanban board → Board → Control Chart
2. Set time range to one week
3. Record throughput (items moved to Done), average cycle time
4. For WIP: count items in "In Progress" columns at week start and end, average
5. Repeat weekly

**Via Jira REST API (automation):**
```bash
# Scrum sprint report
curl -u user:token "https://your-jira.atlassian.net/rest/agile/1.0/sprint/{sprintId}/report" | jq '.completedIssues | length'

# Kanban board issues (last 7 days)
curl -u user:token "https://your-jira.atlassian.net/rest/agile/1.0/board/{boardId}/issue?jql=status%20changed%20to%20Done%20after%20-7d"
```

### From Azure DevOps (Step-by-Step)

**For Scrum teams → sprints.csv:**
1. Navigate to Boards → Sprints → select iteration
2. View Sprint Burndown → note Planned vs. Completed story points
3. Export via Analytics → Iteration Summary
4. Map: Planned → `planned_points`, Completed → `completed_points`

**For Kanban teams → flow_metrics.csv:**
1. Navigate to Boards → Analytics → Cumulative Flow Diagram
2. Export data for weekly periods
3. Map: Items completed per week → `throughput_items`, average lead time → `lead_time_avg`

**Via ADO REST API:**
```bash
# Sprint capacity and work items
curl -u :pat "https://dev.azure.com/{org}/{project}/_apis/work/teamsettings/iterations/{iterationId}/workitems?api-version=7.0"
```

### From ServiceNow

| ServiceNow Data | Command Center Template | Step-by-Step |
|-----------------|------------------------|--------------|
| Incident export | SLA incidents via API | System → Export → select incident table → CSV. Map: Number → incident_id, Priority → priority, Opened → reported_at, Resolved → resolved_at |
| SLA performance report | kpi_monthly.csv | Navigate to SLA → Performance Analytics → Export metric as CSV. Map SLA Met % → kpi_code "SLA_COMP" |

### From SAP/Oracle/Tally (Financial Data)

| ERP Data | Command Center Template | Step-by-Step |
|----------|------------------------|--------------|
| Monthly P&L | financials.csv | Extract project-level P&L report for the month. Map: Budget → planned_revenue, Actuals → actual_revenue/actual_cost. Include `currency` column for multi-currency support. |
| Headcount report | resources.csv / bench.csv | HR module → Headcount by cost centre → Export. Map: FTE count, allocation %, bench status |
| Rate card | rate_cards via API | Extract role-level billing rates. POST to `/api/v1/rate-cards` |

### From HRIS (Utilisation)

| HRIS Data | Command Center Template | Mapping |
|-----------|------------------------|---------|
| Monthly utilisation report | utilization_detail via API | HRIS util, RM util, billing util + gap breakdown |

### From SurveyMonkey/Qualtrics (Customer)

| Survey Data | Command Center Template | Mapping |
|-------------|------------------------|---------|
| CSAT survey results | customer_satisfaction via API | Overall score → csat_score (1-10), NPS question → nps_score (-100 to +100) |
| Open-text themes | Manual entry in Tab 6 (Customer Intelligence) | positive_themes, concern_themes (JSON arrays) |

---

## Data Refresh & Recalculation

### Immediate (Synchronous)

On any data change (CSV upload, manual entry, API POST):
- CPI, SPI, TCPI, VAC, EAC recompute
- DHI (Delivery Health Index) recomputes
- AI Trust Score recomputes
- Margin layers recalculate
- Loss exposure updates
- Renewal probability recalculates
- Narrative cache invalidates and regenerates

### Background (Every 15 Minutes)

- Smart Ops evaluates all 8 detection scenarios
- Forecast engine updates predictions (if new data since last run)
- Alert badges update on Tab 1 ticker

### Recommended Cadence

| Data Type | Cadence | Why |
|-----------|---------|-----|
| Sprint data | End of each sprint (bi-weekly) | Velocity, defects, rework are sprint-scoped |
| KPI snapshots | Monthly | Most KPIs are month-end measurements |
| EVM snapshots | Monthly | Aligns with financial reporting |
| Financial data | Monthly | Revenue and cost are monthly |
| Risk register | Weekly | Risks change frequently |
| Customer satisfaction | Monthly or per survey | CSAT/NPS are periodic |
| AI metrics | Per sprint | Aligns with sprint cadence |
| Resource/bench | Monthly | Aligns with HR/RM reporting |

### Dashboard Auto-Refresh

The frontend polls the backend every 60 seconds for new data. After a CSV upload or API POST, charts update within 60 seconds without manual browser refresh.

### Duplicate Handling

The import system checks for duplicates based on composite keys:
- KPI snapshots: (program_id + snapshot_date + kpi_id) — duplicates rejected
- EVM snapshots: (program_id + snapshot_date) — duplicates rejected
- Sprint data: (program_id + sprint_number) — duplicates rejected
- To update existing data, use PUT API endpoints

---

## Troubleshooting

### Common Upload Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "Programme code not found: XYZ" | program_code in file doesn't match any programme | Import programmes.csv first; verify code matches exactly |
| "Invalid date format" | Date not in recognisable format | Use YYYY-MM-DD (preferred) or DD/MM/YYYY |
| "Duplicate record" | Same key combination already exists | Use PUT endpoint to update, or delete existing record first |
| "Column not mapped" | Auto-mapper couldn't match a header | Manually map in the mapping UI, or rename header to match template |
| "Value out of range" | Percentage > 100 or negative hours | Check your data for outliers before upload |
| "File too large" | File > 50 MB | Split into smaller files by programme or by time period |
| "Merged cells detected" (xlsx) | Excel file has merged cells | Unmerge all cells in Excel before upload |
| "No header row found" (xlsx) | Headers not in row 1 | Move or delete rows above the header row |
| "Multiple sheets detected" (xlsx) | Excel file has multiple sheets | Data is read from Sheet1 only; move data to Sheet1 or export the target sheet as a separate file |

### API Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 200 | Success | — |
| 201 | Created | — |
| 400 | Bad request | Check request body JSON format |
| 404 | Not found | Verify programme/project ID exists |
| 409 | Conflict (duplicate) | Record with same key already exists |
| 422 | Validation error | Check field types, required fields, value ranges |
| 500 | Server error | Check backend logs: `docker compose logs backend` (v2) or `docker-compose logs backend` (v1) |

---

## Data Export & Backup

### Export All Data

```bash
# macOS / Linux
./scripts/export-db.sh

# Windows (PowerShell)
Invoke-RestMethod -Uri "http://localhost:9001/api/v1/export/workspace" -OutFile workspace_export.json

# Via API (any OS with curl)
curl -s http://localhost:9001/api/v1/export/workspace -o workspace_export.json
```

### Import from Backup

```bash
# macOS / Linux
curl -X POST http://localhost:9001/api/v1/import/workspace \
  -d @workspace_export.json \
  -H 'Content-Type: application/json'

# Windows (PowerShell)
$body = Get-Content workspace_export.json -Raw
Invoke-RestMethod -Uri "http://localhost:9001/api/v1/import/workspace" -Method Post -Body $body -ContentType "application/json"
```

### Automated Daily Backup (NEW in v5.2)

The backend automatically backs up the SQLite database daily:
- **Retention:** 30 days (configurable in Tab 11 → Settings)
- **Location:** `/data/backups/` inside Docker volume
- **Manual trigger:** `./scripts/backup.sh` (Mac/Linux) or `docker compose exec backend python -m app.backup` (Windows)
- **Restore:** Copy backup file to `/data/akb1.db` and restart containers

### Import Rollback (NEW in v5.2)

Every data import creates a snapshot. To rollback:
1. Tab 11 → Import History → select the import to undo
2. Click "Rollback" → confirms affected tables and row counts
3. Data reverts to pre-import state

### Audit Package Export

Tab 9 (Risk & Audit) provides an "Export Audit Package" button that generates a dated ZIP containing:
- All governance controls with compliance percentages
- AI audit trail (every AI artifact with provenance, review status, production outcome)
- Override log with rationale and outcome classification
- Process compliance evidence (meetings held, action items)
- Data lineage snapshots (calculation chain for every dashboard number)

---

## Data Retention

| Data Type | Retention | Reason |
|-----------|-----------|--------|
| Active programme data | Indefinite (until deleted) | Operational |
| Completed programme data | Indefinite (user manages) | Audit trail |
| Demo data | Until reset | Non-production |
| Audit log | Indefinite (append-only) | Compliance |
| Narrative cache | Auto-invalidated on data change | Performance |
| Forecast cache | Regenerated on schedule | Freshness |

SQLite database persists in Docker volume. Survives container restarts. To permanently delete: `docker volume rm akb1-command-center_akb1-data`.

---

**Adi Kompalli — Architect & Designer | AKB1 v5.2 | 2026-04-16**
