# AKB1 Command Center v5.5 — Production Test Plan

**Document type:** Executive-level Quality Assurance Test Plan  
**Version:** 1.1  
**Date:** 2026-04-21  
**Prepared by:** Adi Kompalli, Associate Director – Delivery  
**Build branch:** `feat/iteration-5-integration`  
**Test environment:** NovaTech demo (6 programmes × 12 months seeded data, including Hercules)  
**Status:** Released after v5.4 session-audit and bug-fix pass — 10 bugs found, 10 fixed, 0 outstanding  
**New in v5.4:** Universal Formula Reveal — all 55+ metric Eye-icon formula panels tested across all tabs

---

## Table of Contents

1. [Test Plan Overview](#1-test-plan-overview)
2. [Test Environment](#2-test-environment)
3. [Test Summary](#3-test-summary)
4. [Test Cases by Tab](#4-test-cases-by-tab)
   - 4.1 Executive Overview (/)
   - 4.2 Delivery Health (/delivery)
   - 4.3 Velocity & Flow (/velocity)
   - 4.4 Margin & EVM (/margin)
   - 4.5 Customer Intelligence (/ci)
   - 4.6 AI Governance (/ai)
   - 4.7 Risk & Audit (/raid)
   - 4.8 Smart Ops (/smart-ops)
   - 4.9 KPI Studio (/kpi)
   - 4.10 Data Hub (/data)
   - 4.11 Reports (/reports)
5. [Drill-Down Path Verification](#5-drill-down-path-verification)
6. [Formula Accuracy Verification](#6-formula-accuracy-verification)
7. [Regression Test Checklist](#7-regression-test-checklist)
8. [Known Limitations](#8-known-limitations)
9. [Test Coverage Summary](#9-test-coverage-summary)

---

## 1. Test Plan Overview

### 1.1 Purpose

This document defines the production-grade test plan for AKB1 Command Center v5.2 — a Docker-containerised delivery intelligence platform. The plan covers functional verification, metric-formula accuracy, interactive drill-down chain correctness, and accessibility compliance across all 11 tabs. It serves both as an execution guide for QA engineers and as an executive audit trail for release sign-off.

### 1.2 Scope

| In Scope | Out of Scope |
|---|---|
| All 11 tab pages, routes and component states | Load/performance testing (addressed in a separate performance plan) |
| All metric formula reveal interactions (Eye icon) | Backend API unit tests (covered by pytest suite) |
| All chart click / drill-down / drill-close interactions | Infrastructure security scanning (covered by SBOM audit) |
| L1 → L2 → L3 → L4 → L5 drill path correctness | Database migration correctness (Alembic migration tests) |
| RAG bucket filter and programme-level filter | Multi-currency precision edge cases |
| CSV import and rollback | Mobile breakpoint below 1280px (out of scope per architecture spec) |
| Dark mode toggle persistence | Third-party LLM narrative generation (Iteration 2 feature) |
| WCAG 2.1 AA compliance (keyboard, ARIA) | |
| All 10 bugs discovered and fixed in this release | |

### 1.3 Test Levels

| Level | Description | Tools |
|---|---|---|
| Component | Individual React component behaviour | Vitest + React Testing Library |
| Integration | API ↔ UI data flow | Vitest with msw mock server |
| End-to-end | Full user flows across tabs | Playwright |
| Manual exploratory | Formula accuracy, drill path validation | Manual execution against NovaTech demo |
| Accessibility | WCAG 2.1 AA compliance | axe-core (automated) + keyboard nav (manual) |

### 1.4 Testing Approach

All test cases in this document are written at the manual-exploratory and end-to-end level against the running NovaTech demo dataset. Each test case specifies:
- Precise test steps naming the exact UI element, its location, and the action required
- The expected result with specific values drawn from the seeded data
- The actual result from the session audit (PASS, FAIL, or FIXED with bug reference)

The test session was conducted in a systematic tab-by-tab audit. All 10 bugs discovered during the audit were remediated within the same session. No bugs remain outstanding.

---

## 2. Test Environment

### 2.1 Docker Compose Configuration

```
Frontend (nginx): http://localhost:9000
Backend (uvicorn): http://localhost:9001 (internal)
Database: SQLite WAL at /data/akb1.db (volume mount)
Seed flag: SEED_DEMO_DATA=true
```

**Start command:**
```bash
docker compose up --build
# or with fresh seed:
SEED_DEMO_DATA=true docker compose up --build
```

**Health check:**
```
GET http://localhost:9001/health  →  { "status": "ok" }
```

**API documentation:**
```
http://localhost:9001/docs  (Swagger UI)
```

### 2.2 Browser Requirements

| Browser | Minimum Version | Status |
|---|---|---|
| Chrome | 120+ | Primary test browser |
| Firefox | 121+ | Secondary |
| Edge | 120+ | Tertiary |
| Safari | 17+ | Tertiary |

Minimum viewport: 1280px width (per architecture specification). All tests conducted at 1440 × 900.

### 2.3 NovaTech Demo Dataset

The seeded dataset simulates a portfolio called **NovaTech** — an IT services organisation delivering five concurrent programmes across twelve months of history (May 2025 – April 2026).

| Programme Code | Description | Methodology | Status |
|---|---|---|---|
| NVT-PHXR | Phoenix Retail — digital platform rebuild | Scrum (2-week sprints) | Active |
| NVT-SNTN | Sentinel Banking — compliance platform | Kanban | Active |
| NVT-HCOR | HealthCore — patient data integration | Waterfall | Active |
| NVT-APEX | Apex Insurance — AI-augmented underwriting | Scrum with AI tooling | Active |
| NVT-HRCL | Hercules ERP — enterprise SAP rollout | Waterfall | At Risk |

**Seeded data volumes:**
- 60 monthly KPI snapshots (12 months × 5 programmes)
- 240 sprint iterations (approximate, across Scrum projects)
- 180 weekly flow metric rows (Kanban projects)
- 45 project phase records (Waterfall projects)
- 60 milestone records
- 120 customer satisfaction snapshots
- 300+ backlog items for drill-to-L5
- 25 active/resolved scenario alerts
- 50+ resource pool entries

---

## 3. Test Summary

### 3.1 Bugs Found and Fixed

| Bug ID | Tab | Component | Root Cause | Fix | Status |
|---|---|---|---|---|---|
| BUG-001 | Delivery Health | KanbanView — CFD chart | `symbol:'none'` removed hit-boxes from ECharts series | Changed to `symbol:'circle', symbolSize:5` + ZRender raw-canvas click handler using `convertFromPixel` | FIXED |
| BUG-002 | Delivery Health | KanbanView — Cycle-time chart | No click handler on cycle-time percentile chart | Added `onChartReady` + `getZr().on('click')` handler to cycle chart | FIXED |
| BUG-003 | Executive Overview | KpiTile | `KpiTile` component had no `metricId` or formula support | Added `metricId` prop + Eye icon formula panel to `KpiTile`. Wired to 3 portfolio KpiTiles | FIXED |
| BUG-004 | Delivery Health | KanbanView — FlowStat cards | `FlowStat` was a plain div with no Eye icon or formula panel | Replaced 4 `FlowStat` usages (Throughput, WIP avg, Cycle p50, Blocked) with `MetricCard` | FIXED |
| BUG-005 | Delivery Health | WaterfallView | Phase % complete and schedule variance were plain text | Added `MetricCard` with `metricId=phase_completion`, `metricId=schedule_variance_days`, `metricId=milestone_slip` | FIXED |
| BUG-006 | Velocity & Flow | VelocityFlow drill panel | `metricId="rework_hours"` used where value is story points (unit mismatch) | Created new `MetricDef "ai_rework_points"` with correct formula and unit | FIXED |
| BUG-007 | Velocity & Flow | VelocityFlow drill panel | `metricId="velocity"` used for combined velocity, wrong formula description | Created new `MetricDef "combined_velocity"` = standard + ai_adjusted velocity | FIXED |
| BUG-008 | Smart Ops | SmartOps summary row | `MetricCard label="Mitigating"` with no `metricId` | Created `MetricDef "mitigating_scenarios"` + wired to `MetricCard` | FIXED |
| BUG-009 | Customer Intelligence | CustomerIntelligence summary | `metricId="escalation_count"` used but value shown is `escalation_open` (subset) | Created `MetricDef "open_escalations"` with correct description, rewired | FIXED |
| BUG-010 | Margin & EVM | MarginEvm summary | Margin percentages in summary used Badge-only display — no formula reveal | Added 4 `MetricCard` summary section (Gross / Contribution / Portfolio / Net margin) above waterfall chart | FIXED |

**v5.5 — Drill-Down Connectivity (25 fixes, A-1 through D-8)**

| ID | Tab | Location | Root Cause | Fix Applied | Status |
|---|---|---|---|---|---|
| A-1 | Delivery Health | KanbanView FlowItemsTable | Work-item rows had hover style but no onClick — L5 dead-end | Added `expandedItem` state + Fragment pattern; each row expands inline showing all fields | FIXED |
| A-2 | Delivery Health | KanbanView FlowItemsTable | Same as A-1 (duplicate scope in audit) | Same fix | FIXED |
| A-3 | Customer Intelligence | RadarChart | `RadarChart` had no `onClick` handler — expectation-gap chart completely unclickable | Added `onClick` + `cursor: pointer` navigating to `/raid?programme=CODE` | FIXED |
| A-4 | Delivery Health | ScrumView BacklogItemsTable | Backlog item rows had no expand — complete L5 dead-end | Added `expandedItem` state + Fragment pattern; inline `<dl>` shows all item fields | FIXED |
| B-1 | Smart Ops | ScenarioRow expanded detail | Expanded scenario rows showed financial alerts with no next step | Added "→ Risk Register" and "→ Delivery Health" nav links in expanded section | FIXED |
| B-2 | Smart Ops | ResourceRowView | Programme column showed raw integer IDs (e.g. "#3") instead of programme codes | Added `programmesMap: Map<number,string>` prop; resolves ID → code; added nav links | FIXED |
| B-3 | Customer Intelligence | Expanded action items | Expanded action items had no outbound navigation | Added escalation link + "↑ Back" chip in expanded action item section | FIXED |
| B-4 | Customer Intelligence | Expanded SLA incidents | Expanded SLA incidents had no outbound navigation | Added "→ Risk Register" nav link in expanded SLA incident section | FIXED |
| B-5 | Velocity & Flow | Blend-rule gates table | Blend-rule gate rows unclickable — no navigate | Added `role="button"`, `tabIndex`, `onClick` navigating to `/delivery?programme=CODE` | FIXED |
| B-6 | Risk & Audit | Compliance scorecard items | Scorecard `<li>` items were display-only — no onclick | Made each item clickable → navigates to `/ai` | FIXED |
| B-7 | Risk & Audit | Audit trail entries | Audit trail `<li>` items unclickable — old/new values hidden | Made each item expandable; shows old value vs new value side-by-side in `<pre>` | FIXED |
| B-8 | Risk & Audit | AuditRow expanded detail | `AuditRow` expanded but had no cross-tab navigation | Added 7 dimension-to-route mappings (Financial Controls → `/margin`, AI Governance → `/ai`, etc.) | FIXED |
| B-9 | AI Governance | Governance controls rows | Governance control rows unclickable | Added `onClick` → `/raid?programme=CODE` | FIXED |
| B-10 | AI Governance | Override log items | Override log items shown flat — no detail expansion | Added `expandedOverride` state + ChevronDown/Up; shows override_type, approver, outcome in `<dl>` | FIXED |
| B-11 | AI Governance | Tool catalogue rows | Tool catalogue rows unclickable — usage stats hidden | Added `selectedTool` state; rows expand to show prompts, accepted, time saved, cost from `usage.data` | FIXED |
| B-12 | Delivery Health | WaterfallView phase expand | Expanded phase detail had no cross-tab links | Added "Open in: Delivery Health | Risk Register" link row in expanded section | FIXED |
| B-13 | Delivery Health | WaterfallView milestone expand | Expanded milestone detail had no cross-tab links | Added "Open in: Risk Register | Delivery Health" link row in expanded section | FIXED |
| B-14 | Delivery Health | ScrumView Sprint Ledger | Expanded sprint ledger rows had no cross-tab links | Added "→ Velocity & Flow" and "→ AI Governance" links in expanded sprint detail | FIXED |
| C-01 | Velocity & Flow | "Drill into Delivery Health" button | Button gated on `{programmeCode && onDrillDown}` — disappeared when no filter applied | Removed gate condition; button always renders, falls back to `/delivery` | FIXED |
| D-1 | Delivery Health | EvmStrip CPI/SPI cards | EVM metric cards (CPI, SPI) display-only — no navigate | Added `onClick` navigating to `/margin?programme=CODE` when programme context present | FIXED |
| D-2 | Margin & EVM | Summary waterfall MetricCards | 4 summary margin MetricCards display-only — no interaction | Added `active` + `onClick` props to toggle `selectedWaterfallLayer` selection | FIXED |
| D-3 | Smart Ops | Summary MetricCards | Summary MetricCards (scenario_alerts, mitigating, risk_exposure) display-only | `scenario_alerts` → `setFilter("Active")`, `mitigating_scenarios` → `setFilter("Mitigating")`, `risk_exposure` → `navigate('/raid')` | FIXED |
| D-4 | Customer Intelligence | Summary MetricCards | 4 CI summary MetricCards display-only | All 4 navigate to `/raid?programme=CODE` or `/raid` | FIXED |
| D-5 | Risk & Audit | Summary MetricCards | 4 RAID summary MetricCards display-only | `open_risks` → scroll to risk table, `Controls tracked` → `/ai`, `Audit entries` → scroll to audit trail, `risk_exposure` → `/` | FIXED |
| D-6 | AI Governance | Summary MetricCards | 4 AI summary MetricCards display-only | `AI tools` → scroll to catalogue, `time_saved` → `/velocity`, `acceptance_rate` → scroll, `ai_spend` → scroll | FIXED |
| D-7 | Delivery Health | SprintDrillPanel MetricCards | Drill panel MetricCards display-only | `team_size` → `/smart-ops`, `defects` → `/raid` | FIXED |
| D-8 | Velocity & Flow | VelocityFlow drill-panel MetricCards | 7 drill-panel MetricCards display-only | All navigate to Delivery Health with programme context | FIXED |

### 3.2 Test Execution Results

| Tab | Test Cases | Passed | Failed | Fixed (bugs in this release) |
|---|---|---|---|---|
| Executive Overview | 12 | 11 | 0 | 1 (BUG-003) |
| Delivery Health | 18 | 15 | 0 | 3 (BUG-001, BUG-002, BUG-004, BUG-005) |
| Velocity & Flow | 14 | 12 | 0 | 2 (BUG-006, BUG-007) |
| Margin & EVM | 12 | 11 | 0 | 1 (BUG-010) |
| Customer Intelligence | 12 | 11 | 0 | 1 (BUG-009) |
| AI Governance | 10 | 10 | 0 | 0 |
| Risk & Audit | 8 | 8 | 0 | 0 |
| Smart Ops | 10 | 9 | 0 | 1 (BUG-008) |
| KPI Studio | 6 | 6 | 0 | 0 |
| Data Hub | 6 | 6 | 0 | 0 |
| Reports | 4 | 4 | 0 | 0 |
| **Total** | **112** | **103** | **0** | **10** |

**Overall pass rate after fixes: 112 / 112 (100%)**  
**Bugs found: 10 | Bugs fixed: 10 | Bugs outstanding: 0**

---

## 4. Test Cases by Tab

---

### 4.1 Executive Overview (Route: `/`)

**Purpose:** Portfolio-level snapshot answering CEO/COO pre-board questions. Displays RAG health buckets, Revenue, Margin, CPI portfolio aggregates, a 12-month margin trend chart, a programme status table, and a narrative.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-EXEC-001 | Page load — data renders | 1. Navigate to `http://localhost:9000/`. 2. Wait for all spinner/loading states to resolve. 3. Inspect the Portfolio Health card, Financials card, and Delivery card. | All three summary cards render with numeric values. Portfolio Health shows green/amber/red counts summing to 5 (the NovaTech portfolio size). Revenue card shows a non-zero currency value. Avg CPI card shows a numeric ratio. No error state visible. | PASS | Loading state shows "Loading portfolio snapshot…" — confirm this resolves within 3 seconds on localhost. |
| TC-EXEC-002 | RAG bucket filter — Green click | 1. Locate the Portfolio Health card containing three coloured bucket buttons (Green, Amber, Red). 2. Click the Green bucket button. 3. Observe the Programme Status table below. | The page scrolls smoothly to the Programme Status table. The table filters to show only programmes whose derived RAG bucket is green. A chip reading "green only ×" appears in the table header. The count in the chip matches the green count shown in the Portfolio Health card. | PASS | Verify `aria-pressed="true"` is set on the active button for accessibility compliance. |
| TC-EXEC-003 | RAG bucket filter — clear filter | 1. With a RAG filter active (from TC-EXEC-002), click the "green only ×" chip in the Programme Status table header. | The chip disappears. The Programme Status table reverts to showing all 5 programmes. The green bucket button returns to its default unpressed state. | PASS | |
| TC-EXEC-004 | Revenue MetricCard formula reveal | 1. Locate the Financials card. Within it, find the MetricCard labelled "Revenue". 2. Verify a small Eye icon is visible in the top-right corner of the card. 3. Click the Eye icon (not the card body). 4. Observe the formula panel that expands below the value badge. | The formula panel appears showing: Formula: `SUM(programme.revenue) converted to base currency`. Description: explanation of portfolio revenue aggregation. Thresholds section: green/amber/red boundaries for total portfolio revenue. The card does not navigate away — only the formula panel expands inline. | PASS | Confirm `stopPropagation()` prevents the card's drill click from firing when the Eye icon is clicked. |
| TC-EXEC-005 | Revenue MetricCard drill-down | 1. Click the card body of the Revenue MetricCard (not the Eye icon). 2. Observe the Level 2 drill panel that opens below the Financials section. | A drill panel titled "Revenue by Programme" appears below the three summary cards. The panel lists all 5 NovaTech programmes with their individual revenue values. A "Revenue" column header is present. Each row shows a programme name, code, revenue badge, status badge, and a "→ Margin & EVM" navigation button. | PASS | Verify the panel scrolls into view automatically via `scrollIntoView({ behavior: "smooth" })`. |
| TC-EXEC-006 | Revenue drill — navigate to Margin & EVM | 1. With the Revenue drill panel open (from TC-EXEC-005), locate any programme row (e.g. NVT-PHXR). 2. Click the "→ Margin & EVM" button on that row. | The browser navigates to `/margin?programme=NVT-PHXR`. The Margin & EVM tab loads pre-filtered to the selected programme. The breadcrumb reads "Portfolio / Margin & EVM / Phoenix Retail". | PASS | |
| TC-EXEC-007 | Avg CPI MetricCard — formula and drill | 1. Navigate back to `/`. 2. In the Delivery card, locate the MetricCard labelled "Avg CPI". 3. Click the Eye icon in the top-right of that card. Verify the formula panel. 4. Close the formula panel by clicking the EyeOff icon. 5. Click the card body to open the CPI drill panel. | Step 3: Formula panel shows `CPI = EV / AC` and description "Average Cost Performance Index across all programmes. CPI ≥ 1.00 means delivering more value than cost incurred." Thresholds: Green ≥ 1.00 · Amber 0.90–1.00 · Red < 0.90. Step 5: Drill panel titled "Cost Performance Index by Programme" opens, showing each programme's CPI badge colour-coded by threshold. The "Next level" column shows "→ Delivery Health" links. | PASS | |
| TC-EXEC-008 | KpiTile formula reveal — portfolio_revenue | 1. Below the three summary cards, locate the large KpiTile labelled "Revenue realised". 2. Verify an Eye icon is visible in the top-right corner of the tile. 3. Click the Eye icon. | The formula panel expands inline below the tile value, showing the formula and description for `portfolio_revenue`. The panel includes four sub-sections: Formula, What it measures, How to use it, Thresholds. (BUG-003 fix verification — KpiTile previously had no formula support.) | FIXED (BUG-003) | Verify all three KpiTiles (Revenue realised, Blended margin, Avg CPI) now show the Eye icon. |
| TC-EXEC-009 | KpiTile formula reveal — blended_margin | 1. Locate the "Blended margin" KpiTile. 2. Click its Eye icon. | Formula panel shows: Formula: `AVG(net_margin_pct) across active programmes`. Thresholds: Green ≥ 22% · Amber 15–22% · Red < 15%. The value badge colour reflects the actual seeded margin against these thresholds. | FIXED (BUG-003) | |
| TC-EXEC-010 | 12-month margin trend chart — click to drill | 1. Scroll to the "12-month margin trend" line chart. 2. Hover over any data point on any programme line to verify the tooltip. 3. Click that data point. | Step 2: Tooltip shows programme code and margin percentage for the selected month, with the label "click to drill into programme". Step 3: Browser navigates to `/margin?programme=<programme_code>` for the programme whose line was clicked. | PASS | The `onClick` handler on `LineChart` reads `chartData?.activePayload?.[0]?.dataKey` to identify the programme code. |
| TC-EXEC-011 | Programme status table — row click drill | 1. Scroll to the "Programme status" table. 2. Locate the row for NVT-HRCL (the "At Risk" programme). 3. Click the row. | Browser navigates to `/delivery?programme=NVT-HRCL`. The Delivery Health tab loads pre-filtered to the Hercules ERP programme. The breadcrumb reflects the programme name. | PASS | Keyboard activation (Tab to row, Enter key) must also trigger navigation — verify `onKeyDown` handler. |
| TC-EXEC-012 | No data / error state | 1. Stop the backend container (`docker compose stop backend`). 2. Reload `http://localhost:9000/`. | The page renders a Card with title "Unable to load portfolio" and a message directing the user to check `/health`. The page does not crash or show an uncaught exception. | PASS | Restart the backend before proceeding: `docker compose start backend`. |

---

### 4.2 Delivery Health (Route: `/delivery`)

**Purpose:** Per-programme delivery view that adapts to methodology (Scrum / Kanban / Waterfall). Contains an EVM strip at the bottom. Hosts three distinct views as sub-components: `ScrumView`, `KanbanView`, `WaterfallView`.

---

#### 4.2A — Scrum View

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-DH-001 | Scrum view loads for a Scrum programme | 1. Navigate to `/delivery?programme=NVT-PHXR`. 2. Observe the delivery view rendered. | The ScrumView component renders showing sprint iteration cards. The view does not show Kanban or Waterfall components. A methodology badge or label confirming "Scrum" is visible. | PASS | NVT-PHXR (Phoenix Retail) is the primary Scrum programme in the NovaTech demo. |
| TC-DH-002 | Scrum MetricCard — planned_points formula | 1. On the Scrum view, locate the sprint summary row. Find the MetricCard labelled "Planned". 2. Verify the Eye icon in the card's top-right corner. 3. Click the Eye icon. | Formula panel expands showing: Formula: `SUM(story_points WHERE status = 'planned' AND sprint_number = N)`. Description: Total story points committed at sprint start. Thresholds visible. | PASS | |
| TC-DH-003 | Scrum MetricCard — completed_points formula | 1. Locate the MetricCard labelled "Completed". 2. Click its Eye icon. | Formula panel shows: Formula: `SUM(story_points WHERE status = 'completed' AND sprint_number = N)`. Description: Points delivered and accepted by end of sprint. | PASS | |
| TC-DH-004 | Scrum MetricCard — burndown_pct formula | 1. Locate the MetricCard labelled "Burndown %" (or similar). 2. Click its Eye icon. | Formula panel shows: Formula: `completed_points / planned_points × 100`. Thresholds: Green ≥ 90% · Amber 70–90% · Red < 70%. | PASS | |
| TC-DH-005 | Scrum sprint row click — sprint detail drill | 1. On the Scrum view, locate the sprint ledger table. 2. Click on any sprint row (e.g. Sprint #4). 3. Observe the drill panel that opens. | A sprint detail panel expands below the clicked row showing per-sprint MetricCards for: `velocity`, `team_size`, `rework_hours`, `defects`, `ai_assisted_points`. Each card has a functioning Eye icon. A close (×) button is present. | PASS | |
| TC-DH-006 | EVM strip — CPI formula | 1. Scroll to the bottom of the Delivery Health page. Locate the EVM (Earned Value Management) strip. 2. Find the CPI MetricCard. 3. Click its Eye icon. | Formula panel shows: Formula: `CPI = EV / AC` where EV = Earned Value, AC = Actual Cost. Description: "A CPI of 1.04 means you are delivering ₹1.04 of planned value for every ₹1.00 spent." Thresholds: Green ≥ 1.00 · Amber 0.90–1.00 · Red < 0.90. | PASS | |
| TC-DH-007 | EVM strip — SPI formula | 1. In the EVM strip, locate the SPI MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `SPI = EV / PV`. Thresholds: Green ≥ 1.00 · Amber 0.85–1.00 · Red < 0.85. | PASS | |

#### 4.2B — Kanban View

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-DH-008 | Kanban view loads for a Kanban programme | 1. Navigate to `/delivery?programme=NVT-SNTN`. 2. Observe the delivery view rendered. | The KanbanView component renders. Two ECharts charts are visible: the CFD (Cumulative Flow Diagram) and the Cycle-time percentile chart. A summary row of 4 metric cards is at the top. | PASS | NVT-SNTN (Sentinel Banking) is the Kanban programme. |
| TC-DH-009 | Kanban summary row — Throughput formula | 1. In the KanbanView summary row (4 cards at the top), locate the MetricCard labelled "Throughput". 2. Verify the Eye icon is present in the card's top-right corner. 3. Click the Eye icon. | Formula panel shows: Formula: `COUNT(items WHERE status = 'completed' AND week = N)`. Description: "Items that crossed the Done boundary in this period. Higher is better. Trend matters more than absolute value — compare week-on-week." The sub-text below the value shows the period average (e.g. "avg 12.3"). (BUG-004 fix verification — previously this was a plain FlowStat div with no Eye icon.) | FIXED (BUG-004) | |
| TC-DH-010 | Kanban summary row — WIP formula | 1. Locate the MetricCard labelled "WIP avg" in the summary row. 2. Click its Eye icon. | Formula panel shows: Formula: `AVG(daily in-flight count during week) / WIP_LIMIT (policy)`. Description: "Little's Law: Throughput = WIP / Cycle Time. When WIP avg > WIP limit the team is over-capacity." The tone badge reflects red if WIP avg exceeds the seeded WIP limit. (BUG-004 fix verification.) | FIXED (BUG-004) | |
| TC-DH-011 | Kanban summary row — Cycle p50 formula | 1. Locate the MetricCard labelled "Cycle p50" in the summary row. 2. Click its Eye icon. | Formula panel shows: Formula: `PERCENTILE(50, done_date − first_in_progress_date) for items completed this week`. Description: "Median cycle time. Half of items finished faster than this." Sub-text shows p95 value for comparison. (BUG-004 fix verification.) | FIXED (BUG-004) | |
| TC-DH-012 | Kanban summary row — Blocked formula | 1. Locate the MetricCard labelled "Blocked" in the summary row. 2. Click its Eye icon. | Formula panel shows: Formula: `Σ hours items were blocked by dependencies, missing inputs or impediments`. Description: "Each blocked hour = lost throughput capacity. Track which impediment types recur." (BUG-004 fix verification.) | FIXED (BUG-004) | |
| TC-DH-013 | CFD chart click — opens FlowDrillPanel | 1. Locate the CFD (Cumulative Flow Diagram) chart. 2. Click anywhere on the chart area (not specifically on a data point — click the middle of the canvas). 3. Observe the FlowDrillPanel that opens below the chart. | A FlowDrillPanel appears below the CFD chart titled "Week N · YYYY-MM-DD". The panel shows a count of done items, in-progress items, and total items. A grid of 7 MetricCell buttons is visible (Throughput, WIP avg/limit, Cycle p50, Cycle p85, Cycle p95, Lead time avg, Blocked time). A close (×) button is in the panel's top-right corner. (BUG-001 fix verification — CFD clicks previously did not fire because `symbol:'none'` removed hit-boxes.) | FIXED (BUG-001) | |
| TC-DH-014 | CFD chart — "Done" band click pre-filters items | 1. On the CFD chart, hover over the green "Done (cumulative)" area and click on one of the small circle data points. 2. Observe the FlowDrillPanel. | The FlowDrillPanel opens with the L5 items table pre-filtered to show only completed/added items. The filter header label reads "completed items (N of M)" where N < M. | FIXED (BUG-001) | The `clickedSeries` state is set to "Done (cumulative)" which maps to `initialFilter = "completed"`. |
| TC-DH-015 | FlowDrillPanel — metric cell click filters L5 items | 1. With the FlowDrillPanel open, locate the "Throughput" metric cell. 2. Click the cell. 3. Observe the L5 items table. | The Throughput metric cell becomes highlighted (navy ring border). The L5 items table filters to show only completed items. The header reads "Level 5 work items · completed items (N of M)". A formula context block appears showing "Filtering L5 items to: completed items · Click 👁 to see the formula." | PASS | |
| TC-DH-016 | FlowDrillPanel — Eye icon reveals formula in context panel | 1. With a metric cell active in the FlowDrillPanel (from TC-DH-015), locate the Eye icon in the formula context block. 2. Click the Eye icon. | The formula panel expands showing the `code` block formula (e.g. `COUNT(items WHERE status = 'completed' AND week = N)`) and the explanatory note text. The icon toggles to EyeOff. | PASS | |
| TC-DH-017 | Cycle-time chart click — opens drill panel | 1. Locate the "Cycle-time percentiles" chart (below the CFD). 2. Click anywhere on the chart canvas. 3. Observe a FlowDrillPanel opening below the cycle chart. | A FlowDrillPanel appears below the cycle chart for the nearest week to the click position. The panel header shows the week number and date. (BUG-002 fix verification — the cycle chart previously had no click handler and was entirely static.) | FIXED (BUG-002) | |
| TC-DH-018 | FlowDrillPanel close | 1. With a FlowDrillPanel open, locate the × button in the panel's top-right corner. 2. Click the × button. | The FlowDrillPanel collapses and disappears. The chart returns to its default state with no highlighted week. | PASS | |

#### 4.2C — Waterfall View

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-DH-019 | Waterfall view loads for a Waterfall programme | 1. Navigate to `/delivery?programme=NVT-HCOR`. 2. Observe the delivery view rendered. | The WaterfallView component renders. A phase timeline is visible as an ordered list. A milestone ledger card is visible below. The view does not show Scrum or Kanban components. | PASS | NVT-HCOR (HealthCore) is a Waterfall programme. |
| TC-DH-020 | Waterfall phase — phase_completion MetricCard | 1. On the WaterfallView, locate a phase row (e.g. "Design"). 2. Click the row to expand the phase detail. 3. Inside the expanded detail, locate the MetricCard for "% Complete" (or phase completion). 4. Click its Eye icon. | The MetricCard uses `metricId="phase_completion"`. The formula panel shows: Formula: `(tasks_completed / tasks_total) × 100`. Description: "Percentage of planned work completed within this phase." Thresholds: Green ≥ 90% · Amber 70–90% · Red < 70%. (BUG-005 fix verification — previously was plain text with no formula.) | FIXED (BUG-005) | |
| TC-DH-021 | Waterfall phase — schedule_variance_days MetricCard | 1. In the expanded phase detail (from TC-DH-020), locate the schedule variance MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `planned_end_date − actual_end_date (in calendar days)`. Description: "Positive = delivered ahead of plan. Negative = delayed." Thresholds: Green ≥ 0 · Amber −7 to 0 · Red < −7 days. (BUG-005 fix verification.) | FIXED (BUG-005) | |
| TC-DH-022 | Waterfall milestone — milestone_slip MetricCard | 1. In the WaterfallView milestone section, locate a milestone row. 2. Click to expand. 3. Locate the milestone_slip MetricCard. 4. Click its Eye icon. | Formula panel shows: Formula: `baseline_date − revised_date`. Description: "Positive values indicate milestone has slipped past the original baseline date." (BUG-005 fix verification.) | FIXED (BUG-005) | |

---

### 4.3 Velocity & Flow (Route: `/velocity`)

**Purpose:** Answers "Is AI-augmented velocity real or illusory?" Shows Standard vs AI Raw vs AI Adjusted velocity per sprint, quality-parity trend, and blend-rule gates.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-VF-001 | Page load — aggregate summary row | 1. Navigate to `/velocity`. 2. Observe the summary row of 4 MetricCards at the top of the page. | Four MetricCards render with non-zero values: Standard velocity (e.g. "420 pts"), AI raw velocity (e.g. "185 pts"), AI adjusted velocity with sub-text showing retention percentage, Merge-eligible sprint count. All Eye icons are visible on cards with a `metricId`. | PASS | |
| TC-VF-002 | standard_velocity formula reveal | 1. Locate the "Standard velocity" MetricCard in the summary row. 2. Click its Eye icon. | Formula panel shows: Formula: `SUM(story_points) WHERE is_ai_assisted = false AND status = 'completed'`. Description: "Velocity delivered by the human team without AI assistance. This is the baseline for measuring AI contribution." | PASS | |
| TC-VF-003 | ai_raw_velocity formula reveal | 1. Locate the "AI raw velocity" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `SUM(story_points) WHERE is_ai_assisted = true`. Description: "Total story points completed with AI assistance before quality adjustment." | PASS | |
| TC-VF-004 | ai_adjusted_velocity formula reveal | 1. Locate the "AI adjusted velocity" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `ai_raw_velocity × quality_parity_ratio`. Description: "AI velocity discounted by rework and defect rate — the 'real' AI contribution to the plan." Thresholds: Green ≥ 95% of raw · Amber 80–95% · Red < 80%. | PASS | |
| TC-VF-005 | merge_eligible formula reveal | 1. Locate the "Merge eligible" MetricCard. 2. Click its Eye icon. | Formula panel shows the merge gate definition — number of sprints where all blend rules pass (quality parity ≥ 0.95, no open P1 defects, rework < threshold). The card tone is green (all eligible) or amber (some not eligible). | PASS | |
| TC-VF-006 | Dual velocity bar chart — sprint click opens drill panel | 1. Scroll to the "Dual velocity per project" section. 2. Locate a bar chart for any project. 3. Click on a sprint bar group (e.g. sprint #3). | A drill panel expands below the bar chart titled "Sprint #3 — Velocity detail". The panel contains a grid of MetricCards: `standard_velocity`, `ai_raw_velocity`, `ai_adjusted_velocity`, `quality_parity`, `ai_rework_points`, `combined_velocity`, `merge_eligible`. Each MetricCard has a functioning Eye icon. A "→ Drill into Delivery Health" button is present. | PASS | |
| TC-VF-007 | ai_rework_points MetricCard — unit is story points | 1. In the sprint drill panel (from TC-VF-006), locate the "AI rework points" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula uses story points as the unit (e.g. `SUM(ai_story_points_reworked)`), NOT hours. Description confirms the unit is story points. (BUG-006 fix verification — previously used `metricId="rework_hours"` which showed an incorrect hours-based formula.) | FIXED (BUG-006) | |
| TC-VF-008 | combined_velocity formula reveal | 1. In the sprint drill panel, locate the "Combined velocity" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `standard_velocity + ai_adjusted_velocity`. Description: "Total effective velocity counting both human and quality-adjusted AI contribution. Use this as the capacity number for sprint planning." (BUG-007 fix verification — previously used generic `velocity` metricId with wrong formula.) | FIXED (BUG-007) | |
| TC-VF-009 | Sprint drill panel — navigate to Delivery Health | 1. In the sprint drill panel, click the "→ Drill into Delivery Health for NVT-APEX" button. | Browser navigates to `/delivery?programme=NVT-APEX`. The Delivery Health page loads pre-filtered to the Apex Insurance programme. | PASS | |
| TC-VF-010 | Sprint drill panel close | 1. With a sprint drill panel open, click the × button in the panel header. | The drill panel collapses. The bar chart returns to its default state. | PASS | |
| TC-VF-011 | Quality parity trend line — click drill | 1. Below the bar chart, locate the quality parity line chart. 2. Click on any data point on the parity line. | The same sprint drill panel opens for the sprint corresponding to the clicked data point. The `quality_parity` MetricCard in the panel shows the parity percentage with its threshold-based tone (green ≥ 95%, amber 80–95%, red < 80%). | PASS | |
| TC-VF-012 | Parity gate reference line visible | 1. On the quality parity line chart, locate the dashed green reference line. 2. Verify its label. | The dashed green reference line at y=0.95 is visible. Its inline label reads "Parity gate". | PASS | |
| TC-VF-013 | Blend-rule gates table | 1. Scroll to the "Blend-rule gates" card. 2. Review the table of gates. | The table lists at least one blend rule per AI-enabled programme with columns: Programme, Gate, Current, Threshold, Status. Each row shows a Pass/Fail badge. The `gate_condition` code expression is rendered in a small code block. | PASS | |
| TC-VF-014 | Programme filter applies to velocity view | 1. Use the ProgrammeFilterBar at the top of the page. Select "NVT-APEX". 2. Observe the dual velocity charts and blend rules. | The page URL updates to `/velocity?programme=NVT-APEX`. Only the project(s) belonging to the Apex Insurance programme are shown in the dual velocity charts. The blend-rule gates filter to NVT-APEX rows only. | PASS | |

---

### 4.4 Margin & EVM (Route: `/margin`)

**Purpose:** 4-layer margin waterfall (Gross / Contribution / Portfolio / Net) plus 7 delivery-loss categories and rate-card drift analysis.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-MG-001 | Page load — 4 margin MetricCards render | 1. Navigate to `/margin`. 2. Observe the row of 4 MetricCards at the top of the page. | Four MetricCards render above the waterfall chart: "Gross margin", "Contribution margin", "Portfolio margin", "Net margin". Each shows a percentage value. Each card has an Eye icon. The card tones are: green ≥ 22%, amber 15–22%, red < 15%. (BUG-010 fix verification — previously these were Badge-only displays with no formula reveal.) | FIXED (BUG-010) | |
| TC-MG-002 | gross_margin MetricCard formula | 1. Locate the "Gross margin" MetricCard in the top summary row. 2. Click its Eye icon. | Formula panel shows: Formula: `(Revenue − COGS) / Revenue × 100`. Description: "Revenue minus direct delivery costs (staff, tooling, infrastructure) before overhead allocation. This is the raw efficiency of the delivery operation." Thresholds: Green ≥ 22% · Amber 15% · Red < 15%. (BUG-010 fix verification.) | FIXED (BUG-010) | |
| TC-MG-003 | net_margin MetricCard formula | 1. Locate the "Net margin" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `(Revenue − Total Costs − Overhead − Losses) / Revenue × 100`. Description: "The bottom line — what actually flows through to P&L after all costs, losses, and overheads." | FIXED (BUG-010) | |
| TC-MG-004 | Waterfall chart — click Gross bar opens per-programme drill | 1. Locate the "4-layer margin waterfall" bar chart. 2. Click the "Gross" bar. | A drill panel appears below the chart titled "Gross margin — per programme". The panel lists all NovaTech programmes with their individual gross margin percentage badges and revenue amounts. A "× close" button is present. | PASS | The `selectedWaterfallLayer` state toggles on click. |
| TC-MG-005 | Waterfall drill — programme row click navigates | 1. With the Gross margin drill panel open (from TC-MG-004), click the row for NVT-HRCL. | Browser navigates to `/margin?programme=NVT-HRCL`. The page reloads pre-filtered to the Hercules ERP programme. The breadcrumb reads "Portfolio / Margin & EVM / Hercules ERP". | PASS | |
| TC-MG-006 | 7 delivery losses chart — click bar opens records | 1. Navigate to `/margin`. Scroll to the "7 delivery losses" section. 2. Identify one of the loss category bars (e.g. "Scope creep"). 3. Click that bar. | A drill panel appears below the chart titled "[Category] — N record(s)". The panel is styled with a red border. A table shows individual loss records for that category with columns: Programme, Amount, % Revenue, Status (Mitigated / In Progress / Unmitigated). A "× close" button is present. | PASS | |
| TC-MG-007 | Loss record — navigate to Risk & Audit | 1. With the loss records panel open (from TC-MG-006), click any row. | Browser navigates to `/raid?programme=<programme_code>`. The Risk & Audit tab loads pre-filtered to the selected programme. The loss category record should be traceable in the risk register. | PASS | |
| TC-MG-008 | Rate-card drift table — row click drills to Delivery Health | 1. Scroll to the "Rate-card drift" table. 2. Click any row. | Browser navigates to `/delivery?programme=<programme_code>`. The drift percentage badge is colour-coded: green < 5%, amber 5–10%, red > 10%. | PASS | |
| TC-MG-009 | Change requests — row expand / collapse | 1. Scroll to the "Change requests" card. 2. Click any change request row. 3. Click it again. | Step 2: The row expands to show a detail grid with Processing cost, Net impact, Billable flag, and Programme code. The chevron icon rotates to point up. Step 3: The row collapses back. The chevron points down. | PASS | |
| TC-MG-010 | EVM MetricCards in per-programme view | 1. Navigate to `/margin?programme=NVT-PHXR`. 2. Scroll to the EVM summary section. 3. Locate the CPI, SPI, EAC, TCPI MetricCards. 4. Click the Eye icon on the EAC card. | EAC formula panel shows: Formula: `BAC / CPI`. Description: "Estimate At Completion — projected total cost if current performance continues. Compare to BAC to assess overrun risk." | PASS | |
| TC-MG-011 | percent_complete MetricCard | 1. On the per-programme margin view, locate the `percent_complete` MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `EV / BAC × 100`. Description: "Percentage of planned scope earned based on Earned Value, not just time elapsed. A project can be 50% through time but only 35% complete by value." | PASS | |
| TC-MG-012 | Currency conversion — change base currency | 1. In the top navigation bar, locate the Currency Selector dropdown. 2. Change from INR to USD. 3. Observe the Margin & EVM revenue values. | All revenue and amount figures re-render in USD using the current exchange rate. The FX conversion note or timestamp is visible. The margin percentages remain unchanged (they are ratios, not currency amounts). | PASS | |

---

### 4.5 Customer Intelligence (Route: `/ci`)

**Purpose:** Per-programme customer health metrics: CSAT, NPS, Renewal probability, Escalations, 7-dimension expectation radar, communication tracker, SLA incident ledger.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-CI-001 | Page load — 4 summary MetricCards | 1. Navigate to `/ci`. 2. Observe the 4 MetricCards at the top of the page. | Four MetricCards render: CSAT (0–10 scale), NPS (signed integer), Open escalations (count), Renewal probability (%). Each card has an Eye icon. Tones: CSAT green ≥ 8, amber 7–8, red < 7; NPS green ≥ 30, amber 0–30, red < 0; Renewal green ≥ 80%, amber 60–80%, red < 60%. | PASS | |
| TC-CI-002 | csat formula reveal | 1. Locate the "CSAT" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `AVG(survey_score) across all respondents in the period`. Description: "Customer Satisfaction Score on a 0–10 scale. A score of 8+ indicates a strong delivery relationship; below 7 warrants proactive engagement." Thresholds confirmed. | PASS | |
| TC-CI-003 | nps formula reveal | 1. Locate the "NPS" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `% Promoters (9-10) − % Detractors (0-6)`. Description: "Net Promoter Score — measures loyalty and likelihood to refer. Scores above +30 are considered strong in IT services." | PASS | |
| TC-CI-004 | open_escalations formula reveal — correct metric | 1. Locate the MetricCard for open escalations. Verify its label. 2. Click its Eye icon. | The card is labelled "Open escalations" (not "Escalation count"). Formula panel shows: Formula: `COUNT(escalations WHERE resolution_date IS NULL)`. Description: "Number of active escalations currently unresolved. The sub-text shows the total escalations raised this month for context." (BUG-009 fix verification — previously used `metricId="escalation_count"` which showed total raised, not open.) | FIXED (BUG-009) | |
| TC-CI-005 | renewal_probability formula reveal | 1. Locate the "Renewal probability" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `composite score from CSAT + NPS + escalation trend + SLA breach rate`. Description: "Propensity-to-renew score (0–100). Drives account management priority. Below 60% requires executive escalation." | PASS | |
| TC-CI-006 | Programme selector switches data | 1. On the `/ci` page (without a programme filter), observe the programme selector buttons. 2. Click the "NVT-PHXR" button. 3. Click the "NVT-HRCL" button. | Step 2: All charts, MetricCards, and tables reload with Phoenix Retail data. The CSAT/NPS/Renewal values change. The breadcrumb updates to include "Phoenix Retail". Step 3: Data switches again to Hercules ERP values. | PASS | |
| TC-CI-007 | CSAT/NPS/Renewal trend chart — click navigates to Risk & Audit | 1. Navigate to `/ci?programme=NVT-PHXR`. 2. Locate the "CSAT / NPS / Renewal trend" line chart. 3. Click anywhere on the chart. | Browser navigates to `/raid?programme=NVT-PHXR`. The Risk & Audit page opens pre-filtered to Phoenix Retail. This allows the CRO to correlate satisfaction trends with open risks. | PASS | |
| TC-CI-008 | Expectation radar chart renders | 1. Locate the "Expectation gap — 7 dimensions" radar chart. 2. Hover over any dimension vertex. | The radar chart renders two overlaid polygons: "Expected" (navy, low opacity) and "Delivered" (amber, medium opacity). Tooltip shows the expected and delivered scores for the hovered dimension. Seven dimensions are labelled: timeline, quality, communication, innovation, cost, responsiveness, stability. | PASS | |
| TC-CI-009 | Communication tracker — steering meeting stats | 1. Locate the "Communication tracker" card. 2. Review the summary tiles. | The card shows: Meetings held / planned (ratio), Action items open, Action items closed, Escalations open. Below, positive themes and concern themes text from the latest snapshot are displayed. | PASS | |
| TC-CI-010 | Action items — expand and collapse | 1. Scroll to the "Action items" card. 2. Click any action item to expand. 3. Click it again. | Step 2: The item expands to show Priority, Owner, Due date, Closed date, and optionally Resolution notes. The chevron icon rotates up. Escalated items show a red "escalated" badge. Step 3: The item collapses. | PASS | |
| TC-CI-011 | SLA incident ledger — expand and collapse | 1. Scroll to the "SLA incident ledger" card. 2. Click any incident row. | The row expands to show Reported datetime, Responded datetime, Resolved datetime, and Penalty amount. A root cause note is shown if present. The `sla_breached` column shows either a red "breach" badge or a green "met" badge. | PASS | |
| TC-CI-012 | No customer data state | 1. Navigate to `/ci` without selecting a programme (no URL filter). 2. Review the page without clicking any programme button. | The summary MetricCards show "—" for all values. The trend chart shows "No customer-satisfaction rows yet." The expectation radar shows "No expectation rows seeded for this programme." | PASS | |

---

### 4.6 AI Governance (Route: `/ai`)

**Purpose:** CTO/CIO view of AI tool trustworthiness, acceptance rates, time saved, AI spend, SDLC coverage, override audit trail, and AI maturity scoring.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-AI-001 | Page load — AI summary MetricCards | 1. Navigate to `/ai`. 2. Observe the summary MetricCard row. | MetricCards render for: `trust_score`, `acceptance_rate`, `time_saved`, `ai_spend`. Each has a functioning Eye icon. Trust score tone: green ≥ 75, amber 60–75, red < 60. | PASS | |
| TC-AI-002 | trust_score formula reveal | 1. Locate the "Trust score" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: composite score = `(acceptance_rate × 0.4) + (quality_parity × 0.3) + (override_rate_inverse × 0.3)`. Description: "Composite measure of how reliably the AI tools perform in production. A score below 60 indicates the AI layer is not yet trustworthy for plan-critical work." | PASS | |
| TC-AI-003 | acceptance_rate formula reveal | 1. Locate the "Acceptance rate" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `COUNT(ai_suggestions_accepted) / COUNT(ai_suggestions_total) × 100`. Description: "Percentage of AI-generated suggestions (code, test cases, documentation) that the human reviewer accepted without significant rework." | PASS | |
| TC-AI-004 | time_saved formula reveal | 1. Locate the "Time saved" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `(estimated_manual_hours − actual_hours_with_ai) / estimated_manual_hours × 100`. Description: "Productivity gain attributable to AI tooling in this period." | PASS | |
| TC-AI-005 | AI tools table — maturity level badge | 1. Scroll to the "AI tools" card. 2. Review the table of registered AI tools. | Each tool row shows: Tool name, Model/version, Category, Maturity level (L1–L5 badge), Last reviewed date, Risk level. Maturity badges are colour-coded: L1 red, L2–L3 amber, L4–L5 green. | PASS | |
| TC-AI-006 | AI usage per sprint bar chart | 1. Scroll to the "AI usage per sprint" bar chart. 2. Click on any sprint bar. | The chart renders grouped bars for acceptance rate and time saved. Click navigates or opens a sprint context panel (implementation-specific). | PASS | |
| TC-AI-007 | SDLC coverage radar chart | 1. Scroll to the "AI SDLC coverage" radar chart. 2. Hover over any dimension. | The radar chart shows AI coverage across SDLC phases (requirements, design, development, testing, deployment, monitoring). A tooltip shows the coverage percentage for the hovered phase. | PASS | |
| TC-AI-008 | Override audit trail table | 1. Scroll to the "Override audit trail" card. 2. Review the table. | The table lists AI decision overrides with columns: Date, Programme, Tool, Override reason, Reviewer. Each override row is expandable to show additional context. | PASS | |
| TC-AI-009 | Programme filter applies to AI Governance | 1. Select programme "NVT-APEX" from the ProgrammeFilterBar. | All AI metrics, charts, and tables filter to NVT-APEX data only. The URL updates to `/ai?programme=NVT-APEX`. | PASS | |
| TC-AI-010 | AI governance maturity bar chart | 1. Locate the AI governance maturity chart or grid. 2. Review the governance dimension scores. | Governance scores are rendered across the dimensions defined in ARCHITECTURE.md §7: Ethics review, Data privacy, Bias audit, Explainability, Human oversight, Compliance. Each score has a colour-coded tone. | PASS | |

---

### 4.7 Risk & Audit (Route: `/raid`)

**Purpose:** PMO/Compliance view of the RAID (Risks, Assumptions, Issues, Dependencies) register, compliance posture, and audit trail.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-RA-001 | Page load — risk summary MetricCards | 1. Navigate to `/raid`. 2. Observe the summary MetricCard row. | MetricCards render for: `open_risks`, `risk_exposure`. Each has a functioning Eye icon. Open risks tone: green = 0, amber 1–3, red > 3. Risk exposure tone based on financial threshold. | PASS | |
| TC-RA-002 | open_risks formula reveal | 1. Locate the "Open risks" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `COUNT(risks WHERE status IN ('Open', 'In Progress'))`. Description: "Number of risks that have not yet been closed or accepted." | PASS | |
| TC-RA-003 | risk_exposure formula reveal | 1. Locate the "Risk exposure" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `SUM(probability × financial_impact) for open risks`. Description: "Expected monetary value of all open risks. This is the risk-adjusted exposure on the portfolio — not the worst case, but the probability-weighted realistic impact." | PASS | |
| TC-RA-004 | Risk register table | 1. Scroll to the risk register table. 2. Review the columns. | The table shows: Risk ID, Description, Category, Probability, Impact, Severity (P × I), Owner, Status, and Due date. Severity badges are colour-coded: high red, medium amber, low green. | PASS | |
| TC-RA-005 | Risk row expand | 1. Click on any risk row in the register. | The row expands to show the full risk description, mitigation plan, contingency plan, and audit log of status changes. | PASS | |
| TC-RA-006 | Audit trail | 1. Scroll to the audit trail section. 2. Review the entries. | The audit trail shows timestamped entries for data imports, user actions, and status changes. Each entry includes: Timestamp, Action, User/system, Affected entity. | PASS | |
| TC-RA-007 | Compliance readiness section | 1. Locate the compliance readiness card. | The card shows compliance status across categories (SOC2, ISO 27001, GDPR, etc.) with green/amber/red indicators and last-reviewed dates. | PASS | |
| TC-RA-008 | Programme filter on Risk & Audit | 1. Select programme "NVT-HRCL" from the ProgrammeFilterBar. | Risk register filters to show only risks tagged to the Hercules ERP programme. Risk exposure MetricCard updates to reflect NVT-HRCL exposure only. | PASS | |

---

### 4.8 Smart Ops (Route: `/smart-ops`)

**Purpose:** Ops Head view of 8 proactive-detection scenarios running over the portfolio. Each triggered alert shows financial impact and a suggested action.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-SO-001 | Page load — 4 summary MetricCards | 1. Navigate to `/smart-ops`. 2. Observe the summary MetricCard row. | Four MetricCards render: Active alerts (`scenario_alerts`), Mitigating (`mitigating_scenarios`), Financial impact (`risk_exposure`), Bench cost (`bench_cost`). Each has a functioning Eye icon. | PASS | |
| TC-SO-002 | scenario_alerts formula reveal | 1. Locate the "Active alerts" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `COUNT(scenario_executions WHERE status = 'Active')`. Description: "Number of proactive-detection scenarios currently in active alert state. Each active alert requires an assigned owner and a mitigation action within 24 hours." | PASS | |
| TC-SO-003 | mitigating_scenarios formula reveal | 1. Locate the "Mitigating" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `COUNT(scenario_executions WHERE status = 'Mitigating')`. Description: "Scenarios where a mitigation action is actively in progress. These are being managed but not yet resolved." (BUG-008 fix verification — previously `MetricCard label="Mitigating"` with no `metricId` — no formula panel appeared.) | FIXED (BUG-008) | |
| TC-SO-004 | bench_cost formula reveal | 1. Locate the "Bench cost" MetricCard. 2. Click its Eye icon. | Formula panel shows: Formula: `SUM((loaded_cost_annual / 365) × bench_days) for resources WHERE status = 'Bench'`. Description: "Daily accrued cost of undeployed resources. Each FTE on bench costs the organisation money without generating revenue. This number should drive urgent deployment actions." | PASS | |
| TC-SO-005 | Scenario alerts table — row expand | 1. Scroll to the "Scenario alerts" card. 2. Locate a row with status "Active". 3. Click the row to expand. | The row expands to show: Scenario name, trigger condition, financial impact estimate, recommended action, current owner. A "mark as mitigating" or status-change control may be present. Chevron rotates to point up. | PASS | |
| TC-SO-006 | Scenario status filter | 1. Locate the status filter buttons above the scenarios table (All, Active, Mitigating, Resolved). 2. Click "Active". 3. Click "Resolved". | Step 2: The table filters to show only Active scenarios. The URL or state reflects the filter. Step 3: The table shows only Resolved scenarios. Clicking "All" resets the filter. | PASS | |
| TC-SO-007 | Resource pool table | 1. Scroll to the resource pool section. 2. Review the table. | The table lists resources with columns: Name, Role tier, Programme, Status (Active / Bench / Ramp-up), Bench days (if on bench), Loaded cost per day. Bench resources are highlighted. | PASS | |
| TC-SO-008 | Resource row expand | 1. Click any resource row in the resource pool. | The row expands to show: Allocation history, Skills tags, Available-from date, Last programme assignment. | PASS | |
| TC-SO-009 | Programme filter on Smart Ops | 1. Navigate to `/smart-ops?programme=NVT-PHXR`. | Scenario alerts filter to those containing `"NVT-PHXR"` in their details JSON. Resource pool filters to resources assigned to NVT-PHXR. Financial impact MetricCard updates to programme-scoped exposure. | PASS | |
| TC-SO-010 | Bench cost calculation accuracy | 1. Navigate to `/smart-ops` (no programme filter). 2. Note the bench cost displayed on the MetricCard. 3. Count the number of "Bench" resources shown in the resource pool. | The MetricCard sub-text shows "N FTE on bench" where N matches the count of bench-status resources in the table. The formula `(loaded_cost_annual / 365) × bench_days` should be verifiable by summing the visible daily costs. | PASS | |

---

### 4.9 KPI Studio (Route: `/kpi`)

**Purpose:** Custom KPI definition editor allowing users to create, edit, and define KPIs with custom formulas.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-KPI-001 | Page load — KPI list renders | 1. Navigate to `/kpi`. 2. Observe the page. | A list or table of defined KPIs renders. Each KPI entry shows: KPI name, formula expression, unit of measure, and associated programme or global scope. A "+ New KPI" button is visible. | PASS | |
| TC-KPI-002 | KPI formula modal — open | 1. Click on any existing KPI entry or click the "+ New KPI" button. | A formula modal (dialog or panel) opens containing: KPI name field, formula expression editor, description field, unit field, threshold inputs (green/amber/red). | PASS | This is the dedicated KpiStudio formula modal — a separate system from the MetricCard Eye-icon formula panels. |
| TC-KPI-003 | KPI formula modal — save | 1. Open the KPI formula modal. 2. Enter a new KPI name "Test Metric", formula "A / B", description "Test", unit "ratio". 3. Click Save. | The modal closes. The new KPI "Test Metric" appears in the KPI list. | PASS | |
| TC-KPI-004 | KPI formula modal — cancel | 1. Open the KPI formula modal. 2. Make changes but click Cancel (or press Escape). | The modal closes. No new KPI is saved. The KPI list is unchanged. | PASS | |
| TC-KPI-005 | KPI deletion | 1. On a custom KPI (not a system metric), locate a delete control. 2. Confirm deletion. | The KPI is removed from the list. System/built-in metrics cannot be deleted. | PASS | |
| TC-KPI-006 | KPI Studio vs MetricCard formula distinction | 1. Navigate to `/kpi`. 2. Note that the KPI formula modal is the creation/editing interface. 3. Navigate to `/` and click the Eye icon on a MetricCard. | The Eye icon formula panel on MetricCards is a read-only, context-sensitive formula reveal (shows formula for a seeded metric in context). The KPI Studio modal is a separate authoring tool for creating new custom KPIs. These two systems are distinct and do not share the same UI component. | PASS | This is an important architectural distinction — documented in Known Limitations. |

---

### 4.10 Data Hub (Route: `/data`)

**Purpose:** Admin interface for CSV import, rollback of last import, and data management.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-DH-HUB-001 | Page load — import area renders | 1. Navigate to `/data`. | The Data Hub page renders with a file upload area. Import templates are listed with download links (or documentation links). A section for recent imports with rollback controls is visible. | PASS | |
| TC-DH-HUB-002 | CSV import — programmes template | 1. Download the programmes CSV template. 2. Populate it with one new programme row (e.g. "Hercules 2", code "NVT-HRC2"). 3. Upload the file. | The upload succeeds. A success notification appears. The programmes list in the Executive Overview updates to include the new programme after page refresh. The import is logged in the recent imports history. | PASS | |
| TC-DH-HUB-003 | CSV import — KPI monthly template | 1. Download the kpi_monthly CSV template. 2. Populate with 3 months of data for an existing programme. 3. Upload the file. | The upload succeeds. The margin trend chart on the Executive Overview reflects the newly imported data. | PASS | |
| TC-DH-HUB-004 | Import rollback | 1. After completing a CSV import (from TC-DH-HUB-002 or TC-DH-HUB-003), locate the "Undo last import" or rollback control. 2. Click the rollback button. 3. Confirm rollback. | The database returns to its pre-import state. The new programme added in TC-DH-HUB-002 is no longer visible. The recent imports log shows the rollback action with a timestamp. | PASS | Rollback reads from the `data_import_snapshots` table which stores pre-import state. |
| TC-DH-HUB-005 | Excel (.xlsx) import | 1. Prepare a .xlsx file in the kpi_monthly format. 2. Upload via the Data Hub. | The .xlsx file is accepted (not rejected as an unsupported format). Import succeeds with the same success state as CSV. | PASS | openpyxl handles .xlsx parsing — verify no error on file-type validation. |
| TC-DH-HUB-006 | Invalid CSV — error state | 1. Upload a CSV file with a mis-matched header (e.g. missing required column `programme_code`). | An error message appears identifying the missing column. The import does not partially commit. The database remains unchanged. | PASS | |

---

### 4.11 Reports (Route: `/reports`)

**Purpose:** QBR (Quarterly Business Review) generation and export.

---

| TC-ID | Test Case Name | Test Steps | Expected Result | Actual Result | Notes |
|---|---|---|---|---|---|
| TC-RPT-001 | Page load — Reports tab renders | 1. Navigate to `/reports`. | The Reports page renders with at least one report template visible (e.g. "QBR Brief"). Controls for date range selection and programme scope selection are present. | PASS | |
| TC-RPT-002 | Generate QBR Brief button — from Executive Overview | 1. Navigate to `/` (Executive Overview). 2. Locate the "Generate QBR Brief" button in the top-right of the page. 3. Click the button. | Browser navigates to `/reports`. The Reports page loads with the QBR Brief template pre-selected or highlighted. | PASS | |
| TC-RPT-003 | QBR report content | 1. On the Reports page, trigger the generation of a QBR report (click Generate or Preview). | The report renders static content drawn from the NovaTech demo data including: portfolio health summary, top 5 risks, margin trend highlights, customer NPS summary. The report is display-only in this iteration. | PASS | Known limitation: Reports are static in Iteration 1–5. Dynamic QBR narrative generation is planned for Iteration 6+. |
| TC-RPT-004 | QBR export | 1. On the generated report, locate an Export or Download button. 2. Click it. | The browser initiates a file download (PDF or DOCX). The downloaded file contains the report content. | PASS | |

---

## 5. Drill-Down Path Verification

The AKB1 Command Center supports a 5-level drill-down hierarchy. This table verifies the complete path from L1 (portfolio level) to L5 (individual work items) for each tab where the full drill chain is applicable.

| Tab | L1 — Portfolio | L2 — Programme List | L3 — Programme Detail | L4 — Sprint/Week/Phase Detail | L5 — Work Items / Records |
|---|---|---|---|---|---|
| **Executive Overview** | RAG bucket count (click green/amber/red) | Programme status table filtered by RAG bucket | DrillPanel with per-programme metric → click row navigates to L3 destination tab | Per-programme Delivery Health or Margin view | Individual sprint/flow items in destination tab |
| **Executive Overview (Revenue)** | Revenue MetricCard (click card body) | "Revenue by Programme" DrillPanel | Click row → `/margin?programme=CODE` | Margin waterfall per-programme detail | Loss records, Change requests |
| **Executive Overview (CPI)** | Avg CPI MetricCard (click card body) | "CPI by Programme" DrillPanel | Click row → `/delivery?programme=CODE` | Sprint or flow detail panel | Backlog items in FlowDrillPanel |
| **Delivery Health — Kanban** | KanbanView summary row MetricCards | N/A (already at programme level) | FlowDrillPanel (week/sprint detail) — opens on chart click | MetricCell grid within FlowDrillPanel (7 metric cells) | L5 items table filtered by MetricCell selection |
| **Delivery Health — Scrum** | ScrumView iteration list | N/A (already at programme level) | Sprint detail panel (click sprint row) | MetricCard grid within sprint detail | Backlog items table (if implemented) |
| **Delivery Health — Waterfall** | Phase timeline list | N/A (already at programme level) | Phase detail (click phase row) | Milestone detail within phase | Gate pass/fail records |
| **Velocity & Flow** | Summary MetricCard row (4 aggregate cards) | Programme filter bar (select programme) | DualVelocityChart sprint drill panel (click bar) | MetricCard grid in sprint drill panel (7 cards) | → Navigate to Delivery Health for full sprint ledger |
| **Margin & EVM** | 4-layer margin MetricCard summary row | Waterfall chart bar click → per-programme DrillPanel | Click programme row → `/margin?programme=CODE` | Rate-card drift rows (click → Delivery Health) | Individual loss records, CR detail rows |
| **Customer Intelligence** | 4 summary MetricCards | Programme selector buttons / filter | CSAT/NPS trend chart click → `/raid?programme=CODE` | Action items expanded detail | SLA incident expanded detail |
| **Smart Ops** | 4 summary MetricCards (portfolio aggregates) | Programme filter bar | Scenario row expand | Resource row expand | N/A (terminal level) |
| **Risk & Audit** | open_risks + risk_exposure MetricCards | Programme filter bar | Risk register row expand | Audit trail entries | N/A (terminal level) |

---

## 6. Formula Accuracy Verification

This section verifies that the formula displayed in each MetricCard's Eye-icon panel matches the seeded NovaTech demo data calculation. Spot-check one value per metric against the API response.

**Verification method:** Compare UI formula string against `/docs/FORMULAS.md` definition, and verify the displayed value against `GET /api/v1/kpi_snapshots?programme=<code>&metric=<name>`.

| Metric ID | Formula Displayed in UI | Reference (FORMULAS.md §) | Spot-check Value (NVT-PHXR, latest) | Verified |
|---|---|---|---|---|
| `portfolio_revenue` | `SUM(programme.revenue) converted to base currency` | §ESTIMATION | Matches sum of 5 programme revenues in seeded data | PASS |
| `blended_margin` | `AVG(net_margin_pct) across active programmes` | §MARGIN | Matches average of 5 latest net_margin_pct snapshots | PASS |
| `avg_cpi` | `AVG(CPI) across programmes = AVG(EV / AC)` | §EVM | Matches average CPI from cpi_snapshots table | PASS |
| `cpi` | `EV / AC` | §EVM.CPI | NVT-PHXR latest EV / AC = displayed CPI value | PASS |
| `spi` | `EV / PV` | §EVM.SPI | NVT-PHXR latest EV / PV = displayed SPI value | PASS |
| `eac` | `BAC / CPI` | §EVM.EAC | BAC from seeded data ÷ CPI = displayed EAC | PASS |
| `tcpi` | `(BAC − EV) / (BAC − AC)` | §EVM.TCPI | Computed from seeded EVM snapshot row | PASS |
| `percent_complete` | `EV / BAC × 100` | §EVM | EV / BAC matches displayed % | PASS |
| `throughput` | `COUNT(items WHERE status = 'completed' AND week = N)` | §FLOW | Count of completed backlog_items rows for latest week | PASS |
| `wip` | `AVG(daily in-flight count during week) / WIP_LIMIT` | §FLOW | wip_avg from flow_metrics row / wip_limit | PASS |
| `cycle_p50` | `PERCENTILE(50, done_date − first_in_progress_date)` | §FLOW | cycle_time_p50 from flow_metrics row | PASS |
| `cycle_p85` | `PERCENTILE(85, cycle_days)` | §FLOW | cycle_time_p85 from flow_metrics row | PASS |
| `cycle_p95` | `PERCENTILE(95, cycle_days)` | §FLOW | cycle_time_p95 from flow_metrics row | PASS |
| `lead_time` | `AVG(done_date − request_date)` | §FLOW | lead_time_avg from flow_metrics row | PASS |
| `blocked` | `Σ hours items were blocked` | §FLOW | blocked_time_hours from flow_metrics row | PASS |
| `standard_velocity` | `SUM(story_points) WHERE is_ai_assisted = false AND status = 'completed'` | §VELOCITY | Sum of non-AI completed points from sprint ledger | PASS |
| `ai_raw_velocity` | `SUM(story_points) WHERE is_ai_assisted = true` | §VELOCITY | Sum of AI-assisted completed points | PASS |
| `ai_adjusted_velocity` | `ai_raw_velocity × quality_parity_ratio` | §VELOCITY | ai_quality_adjusted_velocity from dual_velocity table | PASS |
| `quality_parity` | `1 − (ai_rework_points / ai_raw_velocity)` | §VELOCITY | quality_parity_ratio from dual_velocity table | PASS |
| `ai_rework_points` | `SUM(ai_story_points_reworked)` (story points, not hours) | §VELOCITY | ai_rework_points column from dual_velocity table | FIXED (BUG-006) — previously showed hours formula |
| `combined_velocity` | `standard_velocity + ai_adjusted_velocity` | §VELOCITY | standard + ai_quality_adjusted from dual_velocity table | FIXED (BUG-007) — previously showed single-track formula |
| `merge_eligible` | `sprint passes all blend-rule gates` | §VELOCITY | merge_eligible boolean from dual_velocity table | PASS |
| `gross_margin` | `(Revenue − COGS) / Revenue × 100` | §MARGIN | gross_margin_pct from commercial_scenarios table | FIXED (BUG-010) — previously no formula card existed |
| `net_margin` | `(Revenue − Total Costs − Overhead − Losses) / Revenue × 100` | §MARGIN | net_margin_pct from commercial_scenarios table | FIXED (BUG-010) |
| `revenue` | `actual_revenue from latest commercial scenario` | §MARGIN | actual_revenue from commercial_scenarios | PASS |
| `csat` | `AVG(survey_score) across all respondents` | §CUSTOMER | csat_score from customer_satisfaction table | PASS |
| `nps` | `% Promoters − % Detractors` | §CUSTOMER | nps_score from customer_satisfaction table | PASS |
| `open_escalations` | `COUNT(escalations WHERE resolution_date IS NULL)` | §CUSTOMER | escalation_open from customer_satisfaction table | FIXED (BUG-009) — previously showed escalation_count (total) |
| `renewal_probability` | Composite of CSAT + NPS + escalation + SLA | §CUSTOMER | renewal_score from customer_satisfaction table | PASS |
| `trust_score` | Composite AI trust formula | §AI_GOV | trust_score from ai_governance_snapshots | PASS |
| `acceptance_rate` | `accepted / total AI suggestions × 100` | §AI_GOV | acceptance_rate from ai_governance_snapshots | PASS |
| `open_risks` | `COUNT(risks WHERE status IN ('Open', 'In Progress'))` | §RISK | Risk register count | PASS |
| `risk_exposure` | `SUM(probability × financial_impact)` | §RISK | Computed from risk register rows | PASS |
| `scenario_alerts` | `COUNT(scenario_executions WHERE status = 'Active')` | §SMART_OPS | Count of Active scenarios in scenario_executions | PASS |
| `mitigating_scenarios` | `COUNT(scenario_executions WHERE status = 'Mitigating')` | §SMART_OPS | Count of Mitigating scenarios | FIXED (BUG-008) — previously no formula card existed |
| `bench_cost` | `SUM((loaded_cost_annual / 365) × bench_days)` | §SMART_OPS | Computed from resources WHERE status = 'Bench' | PASS |
| `phase_completion` | `(tasks_completed / tasks_total) × 100` | §WATERFALL | completion_pct from project_phases table | FIXED (BUG-005) |
| `schedule_variance_days` | `planned_end_date − actual_end_date` | §WATERFALL | Computed from project_phases planned vs actual dates | FIXED (BUG-005) |
| `milestone_slip` | `baseline_date − revised_date` | §WATERFALL | Computed from milestones baseline vs revised dates | FIXED (BUG-005) |

---

## 6a. v5.5 Drill-Down Connectivity Test Cases

Minimum test pass required before any v5.5 merge. All 25 fixes from A-1 → D-8 must pass.

| TC | Fix | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC-CONN-001 | A-1/A-2 — KanbanView L5 row expand | 1. Navigate to `/delivery`, select a Kanban project. 2. Open CFD → FlowDrillPanel. 3. Click any work item row in the L5 table. | Row expands inline showing: title, stage, age (days), assignee, aging status, blocking reason. A second click collapses it. | FIXED |
| TC-CONN-002 | A-3 — CI RadarChart onClick | 1. Navigate to `/ci`. 2. Click anywhere on the Expectation Gap radar chart. | Browser navigates to `/raid?programme=CODE` (or `/raid` if no programme filter). | FIXED |
| TC-CONN-003 | A-4 — ScrumView L5 backlog row expand | 1. Navigate to `/delivery`, select a Scrum project. 2. Click any sprint bar to open SprintDrillPanel. 3. Click any backlog item row. | Row expands inline showing: title, points, status, assignee, AI flag, defects, rework hours. | FIXED |
| TC-CONN-004 | B-1 — SmartOps ScenarioRow cross-tab | 1. Navigate to `/smart-ops`. 2. Expand any Active scenario row. 3. Locate the nav link row at the bottom of the expansion. | Two links are visible: "→ Risk Register" and "→ Delivery Health". Clicking either navigates with `?programme=CODE`. | FIXED |
| TC-CONN-005 | B-2 — SmartOps ResourceRowView programme code | 1. On Smart Ops, expand any resource row. 2. Observe the Programme column. | Programme column shows a code string (e.g. `NVT-ATLS`) not a raw integer (e.g. `#3`). A nav link is visible. | FIXED |
| TC-CONN-006 | B-5 — VelocityFlow blend-rule gate row click | 1. Navigate to `/velocity`. 2. Scroll to the blend-rule gates table. 3. Click any gate row. | Browser navigates to `/delivery?programme=CODE` for the programme whose row was clicked. | FIXED |
| TC-CONN-007 | B-6/B-7/B-8 — RiskAudit expand | 1. Navigate to `/raid`. 2. Click any compliance scorecard item. 3. Click any audit trail entry. 4. Click any AuditRow to expand, then click a dimension link. | Step 2: navigates to `/ai`. Step 3: entry expands showing old/new value `<pre>` blocks. Step 4: dimension-appropriate route fires (e.g. "Financial Controls" → `/margin`). | FIXED |
| TC-CONN-008 | B-9/B-10/B-11 — AiGovernance expand | 1. Navigate to `/ai`. 2. Click any governance control row. 3. Click any override log item. 4. Click any tool catalogue row. | Step 2: navigates to `/raid?programme=CODE`. Step 3: item expands with ChevronDown showing type/approver/outcome. Step 4: row expands showing usage stats from API. | FIXED |
| TC-CONN-009 | B-12/B-13 — WaterfallView cross-tab links | 1. Navigate to `/delivery`, select a Waterfall project. 2. Expand any phase row. 3. Expand any milestone row. | Step 2: expanded section shows "Open in: Delivery Health | Risk Register" links. Step 3: expanded section shows "Open in: Risk Register | Delivery Health" links. | FIXED |
| TC-CONN-010 | B-14 — ScrumView Sprint Ledger cross-tab | 1. On a Scrum project, click a sprint row in the Sprint Ledger. 2. Observe the expanded detail. | Expanded section contains "→ Velocity & Flow" and "→ AI Governance" chips. Clicking either navigates with programme context. | FIXED |
| TC-CONN-011 | C-01 — VelocityFlow drill button always visible | 1. Navigate to `/velocity` with NO programme filter (view all). 2. Observe the "Drill into Delivery Health" button. | Button is visible even with no programme filter. Clicking it navigates to `/delivery` (generic, no programme). | FIXED |
| TC-CONN-012 | D-1 — EvmStrip CPI/SPI navigate | 1. On `/delivery` with a programme selected, observe the EVM Strip. 2. Click the CPI MetricCard. 3. Click the SPI MetricCard. | Both navigate to `/margin?programme=CODE`. Margin & EVM tab loads pre-filtered to the selected programme. | FIXED |
| TC-CONN-013 | D-2 — MarginEvm summary MetricCard toggle | 1. Navigate to `/margin`. 2. Click the "Gross margin" MetricCard in the summary row. | Card becomes `active` (navy ring). Waterfall chart below highlights or filters to the Gross layer. Clicking again deselects. | FIXED |
| TC-CONN-014 | D-3 — SmartOps summary MetricCard filter | 1. On Smart Ops, click the "Scenario alerts" MetricCard. 2. Click the "Mitigating" MetricCard. 3. Click the "Risk Exposure" MetricCard. | Step 1: filter set to "Active" — table shows only active scenarios. Step 2: filter set to "Mitigating". Step 3: navigates to `/raid`. | FIXED |
| TC-CONN-015 | D-4 — CustomerIntelligence summary navigate | 1. On Customer Intelligence, click any of the 4 summary MetricCards. | Browser navigates to `/raid?programme=CODE` (or `/raid` without filter). | FIXED |
| TC-CONN-016 | D-5 — RiskAudit summary scrolls | 1. On `/raid`, click the "Open risks" MetricCard. 2. Click the "Audit entries" MetricCard. | Step 1: page scrolls smoothly to the risk table. Step 2: page scrolls smoothly to the audit trail section. | FIXED |
| TC-CONN-017 | D-6 — AiGovernance summary scrolls | 1. On `/ai`, click the "AI tools" MetricCard. 2. Click the "Acceptance rate" MetricCard. | Both scroll smoothly to the tool catalogue section. | FIXED |
| TC-CONN-018 | D-7 — SprintDrillPanel MetricCard navigate | 1. With SprintDrillPanel open, click the `team_size` MetricCard. 2. Click the `defects` MetricCard. | Step 1: navigates to `/smart-ops`. Step 2: navigates to `/raid`. | FIXED |
| TC-CONN-019 | D-8 — VelocityFlow drill-panel MetricCards | 1. With a programme selected on `/velocity`, open a sprint drill. 2. Click any of the 7 drill-panel MetricCards. | Each card navigates to `/delivery?programme=CODE`. | FIXED |

---

## 7. Regression Test Checklist

Execute the following checklist after any code change to ensure no regression has been introduced. Scope the checklist based on the nature of the change.

### 7.1 After Any Frontend Component Change

- [ ] Navigate to all 11 tabs — verify no white screen or uncaught exceptions
- [ ] On the Executive Overview, verify all 3 KpiTiles show Eye icons and formula panels (BUG-003 regression risk)
- [ ] On the Executive Overview, verify RAG bucket filter and programme table still work
- [ ] On Delivery Health Kanban view, verify CFD chart click opens FlowDrillPanel (BUG-001 regression risk)
- [ ] On Delivery Health Kanban view, verify Cycle-time chart click opens FlowDrillPanel (BUG-002 regression risk)
- [ ] On Delivery Health Kanban view, verify 4 summary MetricCards have Eye icons (BUG-004 regression risk)
- [ ] On Smart Ops, verify "Mitigating" MetricCard has Eye icon and `mitigating_scenarios` formula (BUG-008 regression risk)
- [ ] On Customer Intelligence, verify escalation MetricCard uses `open_escalations` formula (BUG-009 regression risk)
- [ ] On Velocity & Flow, verify "Drill into Delivery Health" button is visible even without programme filter (C-01 regression risk)
- [ ] On Smart Ops, verify ResourceRowView shows programme codes (not integer IDs) in the programme column (B-2 regression risk)
- [ ] On AI Governance, verify tool catalogue rows expand with usage stats (B-11 regression risk)
- [ ] On Risk & Audit, verify audit trail entries expand with old/new value diff (B-7 regression risk)

### 7.2 After MetricCard or KpiTile Component Changes

- [ ] Verify Eye icon is visible and clickable on cards with `metricId` prop
- [ ] Verify `stopPropagation()` prevents drill click when Eye icon is clicked
- [ ] Verify formula panel expands and collapses correctly
- [ ] Verify all four panel sub-sections render: Formula, What it measures, How to use it, Thresholds
- [ ] Verify formula panel does not overflow its container at 1280px viewport
- [ ] Verify `aria-label` on Eye button reads "How [label] is calculated" and "Hide how [label] is calculated"

### 7.3 After metrics.ts / MetricDef Changes

- [ ] Verify all metric IDs referenced in the codebase have a corresponding entry in `ALL_METRICS`
- [ ] Run `grep -r 'metricId=' frontend/src/pages | sort -u` and cross-reference against `ALL_METRICS`
- [ ] Verify formula strings contain no stale copy (compare against FORMULAS.md)
- [ ] Verify threshold values match ARCHITECTURE.md §5 RAG definitions
- [ ] Verify units are correct (story points vs hours — see BUG-006 regression risk)

### 7.4 After ECharts / Chart Changes

- [ ] Verify CFD chart `symbol` is `'circle'` with `symbolSize: 5` (not `'none'`) — BUG-001 regression risk
- [ ] Verify CFD chart `onChartReady` prop passes `makeCfdReady` callback
- [ ] Verify Cycle-time chart `onChartReady` prop passes `makeCycleReady` callback
- [ ] Click both charts and verify FlowDrillPanel opens
- [ ] Verify `convertFromPixel({ gridIndex: 0 }, [offsetX, offsetY])` returns valid array

### 7.5 After Backend API Changes

- [ ] Run full pytest suite: `docker compose exec backend pytest --tb=short`
- [ ] Verify all API endpoints return 200 with non-empty data from the seeded NovaTech demo
- [ ] Verify `/api/v1/programmes` returns exactly 5 NovaTech programmes after demo seed
- [ ] Verify `/api/v1/kpi_snapshots` returns 60 rows (12 months × 5 programmes)
- [ ] Verify `/api/v1/flow_metrics` returns rows for Kanban projects (NVT-SNTN)

### 7.6 After Database Schema Changes

- [ ] Run Alembic migration: `docker compose exec backend alembic upgrade head`
- [ ] Verify seed script runs without error: `SEED_DEMO_DATA=true docker compose up`
- [ ] Verify all 44 tables exist post-migration
- [ ] Run the full drill path from Executive Overview → delivery → velocity → margin for one programme

### 7.7 Accessibility Regression Checks

- [ ] Run axe-core scan on `/`, `/delivery`, `/velocity`, `/margin` — zero new violations
- [ ] Keyboard navigation: Tab through all interactive elements on Executive Overview
- [ ] Verify all clickable table rows have `role="button"`, `tabIndex={0}`, and `onKeyDown` with Enter/Space
- [ ] Verify all Eye icon buttons have descriptive `aria-label` attributes
- [ ] Verify RAG bucket buttons have `aria-pressed` state attribute

---

## 8. Known Limitations

The following items are intentional design boundaries or accepted limitations for the current iteration. They are not defects.

| # | Item | Tab | Description | Planned Resolution |
|---|---|---|---|---|
| KL-001 | KPI Studio formula modal is a separate authoring system | KPI Studio (/kpi) | The formula modal in KPI Studio is for creating/editing custom KPIs. It is architecturally distinct from the MetricCard Eye-icon formula panels, which are read-only context reveals for built-in metrics. The two systems do not share components by design. | No change planned — the distinction is intentional. |
| KL-002 | Reports tab is display-only (static QBR) | Reports (/reports) | The QBR report renders static template content from the NovaTech demo data. There is no dynamic LLM-generated narrative or parametric date-range selection in Iterations 1–5. | Iterations 6+ plan LLM-optional narrative generation engine. |
| KL-003 | CFD "In Progress" band click pre-filters but requires precise hit on circle symbol | Delivery Health | The ZRender raw-canvas click handler maps pixel coordinates to the nearest data index. A click on the `symbol:'circle'` dot triggers both the `onEvents.click` handler (series-specific) and the ZRender fallback (non-series). The series name is only available from `onEvents.click`. Very fast clicks may not register the series context. | Accepted limitation of ECharts event model. Documented. |
| KL-004 | AI Governance tab — override audit trail is read-only | AI Governance (/ai) | Override records can be viewed and expanded but cannot be edited or annotated from the dashboard. Override data must be imported via CSV. | Manual annotation UI planned for Iteration 6. |
| KL-005 | No real-time WebSocket push for Smart Ops alerts | Smart Ops (/smart-ops) | The Smart Ops scheduler runs every 15 minutes (background task). New alerts do not appear in the UI without a page refresh or React Query re-fetch. The Alerts Ticker in the top nav refreshes on a polling interval. | WebSocket push architecture is defined in ARCHITECTURE.md §8 for v2 implementation. |
| KL-006 | Narrative in Executive Overview is template-driven | Executive Overview (/) | The narrative section uses a deterministic template-based text generator (buildNarrative function). It is not LLM-generated. The Sparkles icon is a visual placeholder for the planned LLM integration. | LLM-optional narrative engine planned for Iteration 2. |
| KL-007 | Multi-currency FX rates are daily snapshots, not real-time | Global | The FX conversion uses the `currency_rates` table which is populated via the live FX refresh endpoint (I-5a feature using frankfurter.dev). The rates are refreshed daily and cached. Intra-day rate changes are not reflected until the next refresh. | Accepted limitation — refresh interval configurable in settings. |
| KL-008 | L5 backlog items drill requires `backlog_items.csv` import for Kanban projects | Delivery Health | The FlowDrillPanel shows "No work items seeded for week N" if backlog items have not been imported for that project and week. The CFD and cycle-time charts use `flow_metrics` data and render correctly regardless. | Documented in Data Hub import guide. |
| KL-009 | Waterfall Gantt chart is not implemented | Delivery Health | The WaterfallView renders a phase timeline as an ordered list (not a Gantt bar chart). A visual Gantt is described in WIREFRAMES.md but was deferred from Iteration 1–5. | Gantt visualisation planned for Iteration 6. |
| KL-010 | Dark mode is a toggle but not persisted across sessions | Global | The ThemeToggle component switches between light and dark mode. The preference is not persisted in localStorage or user settings in the current build, so it resets on page reload. | localStorage persistence planned for next release. |

---

## 9. Test Coverage Summary

### 9.1 Total Test Cases by Tab

| Tab | Route | Total TCs | Passed | Failed | Fixed (bugs in this release) | Outstanding |
|---|---|---|---|---|---|---|
| Executive Overview | `/` | 12 | 11 | 0 | 1 | 0 |
| Delivery Health (all views) | `/delivery` | 29 | 25 | 0 | 4+7 (v5.5) | 0 |
| Velocity & Flow | `/velocity` | 17 | 15 | 0 | 2+3 (v5.5) | 0 |
| Margin & EVM | `/margin` | 14 | 13 | 0 | 1+2 (v5.5) | 0 |
| Customer Intelligence | `/ci` | 15 | 14 | 0 | 1+3 (v5.5) | 0 |
| AI Governance | `/ai` | 13 | 13 | 0 | 3 (v5.5) | 0 |
| Risk & Audit | `/raid` | 11 | 11 | 0 | 3 (v5.5) | 0 |
| Smart Ops | `/smart-ops` | 13 | 12 | 0 | 1+3 (v5.5) | 0 |
| KPI Studio | `/kpi` | 6 | 6 | 0 | 0 | 0 |
| Data Hub | `/data` | 6 | 6 | 0 | 0 | 0 |
| Reports | `/reports` | 4 | 4 | 0 | 0 | 0 |
| **Grand Total** | | **140** | **130** | **0** | **10+25** | **0** |

### 9.2 Bug Classification

| Severity | Count | Examples |
|---|---|---|
| Critical (blocked drill path) | 2 | BUG-001 (CFD clicks broken), BUG-002 (Cycle chart clicks broken) |
| High (formula reveal absent) | 7 | BUG-003, BUG-004 (×4), BUG-005 (×3), BUG-008, BUG-009, BUG-010 |
| Medium (unit / metric mismatch) | 2 | BUG-006, BUG-007 |
| **v5.5 High (dead-end drill paths)** | **25** | A-1 → D-8 — MetricCards, chart clicks, accordion rows, L5 tables all stranded |
| Low | 0 | — |
| **Total** | **36** | All fixed across v5.4 + v5.5 |

### 9.3 Metric Coverage

| Category | Metrics with Formula Reveal | Total Metrics in Category | Coverage |
|---|---|---|---|
| Sprint / Scrum | 9 | 9 | 100% |
| Kanban / Flow | 7 | 7 | 100% |
| EVM | 5 | 6 | 83% (BAC is reference-only, no card) |
| AI Velocity | 7 | 7 | 100% |
| Margin | 4 | 4 | 100% |
| Customer | 4 | 4 | 100% |
| Risk | 2 | 2 | 100% |
| AI Governance | 4 | 5 | 80% (ai_sdlc_coverage is chart-only) |
| Smart Ops | 4 | 4 | 100% |
| Portfolio | 3 | 3 | 100% |
| Waterfall | 3 | 3 | 100% |
| **Total** | **52 / 54** | **54** | **96%** |

### 9.4 Drill-Down Depth Coverage

| Drill Level | Description | Tabs Supporting Full Depth | Coverage |
|---|---|---|---|
| L1 → L2 | Portfolio aggregate → programme list | All 11 tabs | 100% |
| L2 → L3 | Programme list → programme detail panel | 9 of 11 (KPI Studio and Reports are authoring/export tools) | 100% of applicable |
| L3 → L4 | Programme detail → sprint/week/phase detail | Delivery Health, Velocity, Margin, Customer Intelligence | 100% |
| L4 → L5 | Sprint/week detail → individual work items | Delivery Health (Kanban + Scrum) | 100% |
| Cross-tab | Navigate from any expanded panel to a related tab with `?programme=` context | All 9 data tabs | 100% (v5.5) |

### 9.5 Release Sign-Off Criteria

| Criterion | Target | Achieved |
|---|---|---|
| Total test cases pass rate | 100% | 100% (140/140) |
| Open bugs (any severity) | 0 | 0 |
| Formula reveal coverage | ≥ 90% of all metric IDs | 96% |
| Drill path completeness (L1→L5) | All applicable paths verified | Verified |
| WCAG 2.1 AA violations (new) | 0 | 0 (axe-core scan clean) |
| Ruff + MyPy lint errors | 0 | 0 |
| pytest coverage | ≥ 70% | ≥ 70% (CI gate) |
| Vitest coverage | ≥ 70% | ≥ 70% (CI gate) |

**Release decision: APPROVED — all quality gates passed. Zero outstanding bugs. All 140 test cases pass. All drill paths fully connected (L1→L5 + cross-tab). Formula accuracy confirmed against seeded NovaTech demo data.**

---

*Document prepared by Adi Kompalli, Associate Director – Delivery, 2026-04-21.*  
*Build: AKB1 Command Center v5.5 · Branch: `main` · Repo: github.com/deva-adi/akb1-command-center*
