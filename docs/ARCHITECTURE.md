# AKB1 Command Center v5.2 — Architecture & Design Document

**Version:** 5.2 (Revised) | **Status:** LOCKED | **Date:** 2026-04-15
**Author:** Adi Kompalli | AKB1 Framework
**Repo:** github.com/deva-adi/akb1-command-center
**Review Cycle:** v5.0 initial → v5.1 after ruthless self-review (10 critical findings) → v5.2 after ultra-think review (28 gap findings — SDLC framework compatibility, multi-currency, cross-platform, data safety)

---

## 1. EXECUTIVE SUMMARY

AKB1 Command Center v5.2 is a Docker-containerized, open-source delivery intelligence platform that answers every question a CTO, CIO, or CEO would ask about programme delivery health, financial performance, AI governance, and operational risk — driven entirely by dashboard data.

**Tech Stack:** FastAPI (Python) + React 18 + SQLite + Docker Compose
**Port:** 9000 (isolated from existing apps: 8080 static, 8502 Hub, 8503 Nexus)
**Data Modes:** Pre-loaded demo (5 programmes × 12 months) | CSV upload with auto-mapping | Manual form entry | Guided onboarding wizard
**Target Users:** Delivery Directors, Portfolio Heads, CIOs/CTOs, Programme Managers
**License:** MIT (open-source, fork-and-use)
**Localisation:** Multi-currency, industry presets (Indian IT Services, US Consulting, European MSP, Custom)

### What Changed in v5.1
- Added Programme → Project hierarchy (real portfolio structure)
- Added 7 missing database tables (EVM, rate cards, milestones, SLA incidents, utilization detail, customer satisfaction, forecasts)
- Added customer satisfaction & expectation management framework
- Added audit & compliance readiness architecture
- Added AI-augmented vs. traditional team comparison framework
- Added narrative generation engine ("So What?" layer)
- Added predictive analytics / forecast engine
- Added guided onboarding wizard + CSV auto-mapping
- Added multi-currency / localisation support
- Added phased build plan (alpha → beta → release)
- Added export / reporting capability
- Consolidated redundant tables, fixed schema gaps
- Expanded CTO questions from 35 → 50
- Expanded Smart Ops from 5 → 8 scenarios
- Renamed "autonomous" to "proactive detection"

### What Changed in v5.2 (Ultra-Think Review — 28 Gaps Fixed)
- **SDLC Framework Compatibility:** Added `delivery_methodology` on projects table, `flow_metrics` table (Kanban), `project_phases` table (Waterfall). Dashboard adapts per methodology.
- **Multi-Currency Conversion Engine:** Added `currency_rates` table, base currency config, real-time aggregation in base currency, configurable exchange rates.
- **Excel (.xlsx) Native Import:** System now accepts both .csv and .xlsx files. Added openpyxl dependency. Excel pitfall guidance documented.
- **Cross-Platform Support:** Windows (Docker Desktop + WSL2), macOS (Docker Desktop), Linux (Docker Engine) — OS-specific commands throughout all docs.
- **Fiscal Year Configuration:** `fiscal_year_start_month` in app_settings. Financial summaries, YTD, QBR boundaries respect fiscal year.
- **Import Undo / Rollback:** `data_import_snapshots` table stores pre-import state. One-click rollback of last import.
- **Database Backup Strategy:** Automated daily backup via SQLite `.backup` command. WAL mode for corruption prevention.
- **Version Migration Path:** Schema migration scripts for each version upgrade. `schema_version` tracking in app_settings.
- **Accessibility (WCAG 2.1 AA):** Text labels alongside colour RAG indicators. Keyboard navigation. High contrast mode. Screen reader friendly charts.
- **Webhook Alert Architecture:** Smart Ops can push alerts to email/Slack/Teams via configurable webhooks (v2 implementation, architecture defined now).
- **Edge Browser Support:** Added to browser compatibility list.
- **Number Format Localisation:** Indian lakh (₹1,00,000), US standard ($1,000.00), European (€1.000,00).
- **Sprint data extended:** `iteration_type` field for non-Scrum entries. `estimation_unit` field (story_points, hours, function_points).
- **Expanded from 37 → 42 → 45 tables, 40 → 45 formulas, 50 → 58 CTO questions, 13 → 16 CSV templates**

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Container Topology

```
┌─────────────────────────────────────────────────────────┐
│                 Docker Compose Network                   │
│                                                         │
│  ┌──────────────┐    ┌───────────────────────────┐     │
│  │   Frontend    │    │        Backend             │     │
│  │  React + Vite │◄──►│  FastAPI + SQLite          │     │
│  │  Port: 9000   │    │  Port: 9001 (internal)     │     │
│  │  (nginx proxy)│    │                            │     │
│  └──────────────┘    │  ┌────────────────────┐    │     │
│                       │  │  Forecast Engine    │    │     │
│                       │  │  (linear regression,│    │     │
│                       │  │   moving average)   │    │     │
│                       │  └────────────────────┘    │     │
│                       │  ┌────────────────────┐    │     │
│                       │  │  Narrative Generator│    │     │
│                       │  │  (template-based)   │    │     │
│                       │  └────────────────────┘    │     │
│                       │  ┌────────────────────┐    │     │
│                       │  │  Smart Ops Scheduler│    │     │
│                       │  │  (background, 15min)│    │     │
│                       │  └────────────────────┘    │     │
│                       └───────────────────────────┘     │
│                              │                           │
│                     ┌────────▼────────┐                 │
│                     │    SQLite DB     │                 │
│                     │  /data/akb1.db   │                 │
│                     │  (volume mount)  │                 │
│                     └─────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Technology Choices

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | FastAPI (Python 3.12) | Auto-generated Swagger docs, async, type safety |
| Frontend | React 18 + Vite | Component model, fast builds, rich chart ecosystem |
| Charts | Recharts + Chart.js | Recharts for React, Chart.js for waterfalls/bridges |
| Styling | Tailwind CSS | Utility-first, AKB1 brand tokens built-in |
| Database | SQLite | Zero-config, portable, single-file backup |
| Container | Docker Compose | Single `docker-compose up` deployment |
| Forecast | NumPy + scipy (built-in) | Linear regression, moving averages — no ML overhead |
| API Docs | Swagger/OpenAPI | Auto-generated from FastAPI |

### 2.3 AKB1 Brand Tokens

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | #1B2A4A | Primary backgrounds, headers, text |
| Ice Blue | #D5E8F0 | Secondary backgrounds, card surfaces, chart fills |
| Amber | #F59E0B | Alerts, warnings, accent highlights, CTAs |
| Success Green | #10B981 | On-target KPIs, healthy status |
| Danger Red | #EF4444 | Critical alerts, SLA breaches, loss indicators |
| White | #FFFFFF | Card backgrounds, text on dark surfaces |

---

## 3. DATA HIERARCHY: PORTFOLIO → PROGRAMME → PROJECT

### 3.1 The Real-World Structure

**Previous design flaw:** Treated programmes as flat entities. In reality, a portfolio owner manages:

```
Portfolio (1 account, 150 people, ₹41M revenue)
├── Programme 1: Phoenix Platform Modernization (₹10M, 25 people)
│   ├── Project 1A: Core Banking Module (₹4M, 10 people, 12 months)
│   ├── Project 1B: Payment Gateway Integration (₹3.5M, 8 people, 8 months)
│   └── Project 1C: Regulatory Compliance Module (₹2.5M, 7 people, 6 months)
├── Programme 2: Atlas Cloud Migration (₹8M, 18 people)
│   ├── Project 2A: Infrastructure Migration (₹5M, 12 people, 18 months)
│   └── Project 2B: Application Modernization (₹3M, 6 people, 10 months)
├── Programme 3: Sentinel Quality Engineering (₹5M, 12 people)
│   └── Project 3A: Test Automation Platform (₹5M, 12 people, 24 months)
├── Programme 4: Orion Data Platform (₹12M, 30 people)
│   ├── Project 4A: Data Lake Build (₹7M, 18 people, 14 months)
│   └── Project 4B: Analytics Dashboard (₹5M, 12 people, 10 months)
└── Programme 5: Titan Digital Commerce (₹6M, 15 people)
    ├── Project 5A: E-commerce Platform (₹4M, 10 people, 12 months)
    └── Project 5B: Mobile App (₹2M, 5 people, 8 months)
```

### 3.2 Three-Level Metric Aggregation

Every KPI computes at 3 levels:

| Level | Scope | Key Metrics | Who Watches |
|-------|-------|-------------|-------------|
| Project | Single workstream, 3-15 people | CPI, Sprint Velocity, Defect Density, Rework % | Tech Lead, Project Manager |
| Programme | Multi-project engagement, 8-50 people | Programme CPI (weighted), Margin %, EAC, Change Impact, AI Trust | Programme Manager, Delivery Manager |
| Portfolio | All programmes, 30-300 people | Portfolio Margin, Weighted CPI, Bench Cost, Revenue Realisation, DHI | Delivery Director, Portfolio Head, CTO |

**Aggregation Rules:**
- Project CPI → Programme CPI = Σ(Project CPI × Project Revenue Weight)
- Project Margin → Programme Margin = Σ(Project Revenue - Project Cost) / Σ(Project Revenue)
- Programme DHI → Portfolio DHI = Σ(Programme DHI × Programme Revenue Weight)
- Utilization aggregates bottom-up: individual → project → programme → portfolio
- Risks roll up: project risks bubble to programme if impact > threshold

### 3.3 Ground-Level Reality Check

What a portfolio owner actually does on a Monday morning:

| Time | Action | Data Needed | Dashboard Section |
|------|--------|-------------|-------------------|
| 8:00 AM | Check overnight alerts | Smart Ops triggers, SLA incidents | Tab 1: Alert ticker |
| 8:15 AM | Review programme health | DHI scores, RAG status per programme | Tab 1: Programme cards |
| 8:30 AM | Deep-dive troubled programme | CPI trend, root cause, team allocation | Tab 3: EVM + Tab 4: Portfolio drill |
| 9:00 AM | Prepare for steering committee | 5-number QBR summary + narrative | Tab 1: Generate Brief button |
| 10:00 AM | Review AI tool performance | Trust scores, override rates, productivity delta | Tab 6: AI Governance |
| 11:00 AM | Customer satisfaction check | CSAT trend, escalation log, expectation gaps | Tab 6: Customer Intelligence |
| 2:00 PM | Financial review with CFO | 4-layer margin, loss categories, forecast | Tab 5: Margin & EVM |
| 4:00 PM | Resource planning for next sprint | Utilization waterfall, bench, skill gaps | Tab 8: Smart Ops + resource view |
| 5:00 PM | Audit readiness check | Governance controls, compliance %, override log | Tab 9: Risk & Audit |

---

## 4. ELEVEN-TAB ARCHITECTURE (expanded from 9)

### Tab 1: Executive Overview
**Purpose:** Single-screen portfolio health for C-level consumption (the "17-minute QBR" view)
**Answers:** "How is my portfolio performing right now?"

**Components:**
- Portfolio health score (DHI composite, weighted)
- Programme cards with RAG status + project count per programme
- Revenue vs. Cost trend (12-month sparkline)
- Top 3 risks by financial impact
- 5-number executive summary: Margin Trend (3Q), Utilization Trend (3Q), Forecast Accuracy %, Revenue Realisation %, Portfolio CPI
- **Active alerts ticker (Smart Ops proactive detections)**
- **Auto-generated narrative summary** ("Portfolio is tracking at 18.5% net margin, 1.5 points below plan. Primary driver: Phoenix scope creep absorbing ₹450K in Q3. Recovery path: offshore rebalancing on Atlas recovers 1.2 points by Q4.")
- **"Generate QBR Brief" button** — exports 5-number summary + narrative + top risks as copy-paste text or printable PDF

**Data Tables:** programs, projects, kpi_snapshots, risks, commercial_scenarios, kpi_forecasts, narrative_cache

---

### Tab 2: KPI Studio
**Purpose:** 13+ KPI definitions with formulas, thresholds, weights, and drill-down
**Answers:** "What are we measuring and why?"

**Components:**
- KPI card grid (each card: name, formula, current value, trend, RAG, weight)
- Editable scoring weights (slider + save)
- KPI trend charts (line charts, 12-month rolling + **dashed forecast line with confidence band**)
- Initiative scoring matrix
- Formula reference modal (click any KPI → formula + 2 worked examples + interpretation)
- **Industry benchmark overlay** (show industry average as dotted line on each KPI chart)

**13 Core KPIs:**

| # | KPI | Formula | Target (Green) | Alert (Red) |
|---|-----|---------|----------------|-------------|
| 1 | Schedule Adherence | (On-Time Milestones / Total Milestones) × 100 | ≥ 90% | < 75% |
| 2 | Scope Stability Index | 1 - (Approved Changes / Original Requirements) | ≥ 0.85 | < 0.70 |
| 3 | Resource Utilization (True Billable) | Billable Hours / Total Available Hours × 100 | ≥ 74% | < 65% |
| 4 | Quality Index | Weighted(Defects, Test Coverage, Rework%) | ≥ 85 | < 70 |
| 5 | Stakeholder Satisfaction | Survey Score (1-10 scale) | ≥ 8.0 | < 6.0 |
| 6 | Risk Exposure Score | Σ(Risk Probability × Financial Impact) | < $500K | > $2M |
| 7 | Budget Variance (CPI) | Earned Value / Actual Cost | ≥ 0.95 | < 0.85 |
| 8 | Delivery Health Index (DHI) | Weighted composite of all KPIs | ≥ 80 | < 60 |
| 9 | SLA Compliance | (SLAs Met / Total SLAs) × 100 | ≥ 98% | < 90% |
| 10 | Forecast Accuracy | 1 - |Forecast - Actual| / Actual × 100 | ≥ 90% | < 80% |
| 11 | Gross Margin % | (Revenue - Effort Cost) / Revenue × 100 | ≥ 35% | < 25% |
| 12 | Revenue Realisation % | Invoiced Revenue / Planned Revenue × 100 | ≥ 95% | < 85% |
| 13 | AI Trust Score | Composite (see Tab 6) | ≥ 75 | < 50 |

**Note:** All thresholds are defaults loaded from the locale/industry preset. Fully editable per deployment.

**Data Tables:** kpi_definitions, kpi_snapshots, scoring_weights (merged into kpi_definitions.weight), initiatives

---

### Tab 3: Delivery Planning
**Purpose:** Sprint-level and programme-level planning with EVM integration
**Answers:** "Are we on track? Will we finish on budget?"

**Components:**
- **Milestone timeline** with dependencies (milestones table, not Gantt — simpler to build, equally useful)
- Sprint burndown chart (current sprint)
- EVM dashboard (CPI, SPI, EAC, TCPI, VAC — **all with forecast projection as dashed line**)
- PERT-based estimation calculator
- Dual velocity tracker (Standard vs. AI-Augmented — see Section 10)
- Forecast confidence meter
- **Project-level drill-down** (click programme → see projects within it)

**EVM Formulas:**

| Formula | Calculation | Interpretation |
|---------|------------|----------------|
| CPI | EV / AC | < 1.0 = over budget |
| SPI | EV / PV | < 1.0 = behind schedule |
| EAC | BAC / CPI | Projected final cost |
| ETC | EAC - AC | Cost to complete |
| TCPI | (BAC - EV) / (BAC - AC) | Efficiency needed to finish on budget |
| VAC | BAC - EAC | Budget variance at completion |

**Worked Example (displayed in UI tooltip):**
- Programme: Phoenix Platform Modernization
- BAC: ₹6.8M | PV at Month 6: ₹4.08M (60% planned) | AC: ₹4.2M | EV: ₹3.4M (50% complete)
- CPI = 3.4M / 4.2M = 0.81 → Over budget by 19%
- SPI = 3.4M / 4.08M = 0.83 → Behind schedule by 17%
- EAC = 6.8M / 0.81 = ₹8.4M → Overrun of ₹1.6M (23.5%)
- TCPI = (6.8M - 3.4M) / (6.8M - 4.2M) = 1.31 → Need 31% improvement (improbable)
- **Narrative:** "Phoenix is spending ₹1.23 for every ₹1 of value delivered. At current burn rate, final cost will be ₹8.4M (23.5% over budget). To finish on budget, remaining work must be 31% more efficient than work completed — statistically improbable without scope reduction or team restructuring."

**Data Tables:** sprint_data, programs, projects, evm_snapshots, milestones, kpi_forecasts

---

### Tab 4: Portfolio
**Purpose:** Multi-programme portfolio view with aggregated financials
**Answers:** "Which programmes need attention? Where is the portfolio margin?"

**Components:**
- Programme comparison matrix (5 programmes, key metrics side-by-side, **expandable to show projects**)
- Portfolio CPI heatmap (monthly, by programme)
- Revenue waterfall chart (planned → adjustments → actual)
- Margin bridge chart (planned margin → erosion drivers → actual margin)
- Programme health radar chart (6 axes: Schedule, Quality, Scope, Risk, Margin, Satisfaction)
- Three-level drill: **Project → Programme → Portfolio**
- **AI vs. Traditional team performance comparison panel** (side-by-side for the same programme)

**Portfolio Margin Layers:**

| Layer | Formula | Typical Range | What It Measures |
|-------|---------|--------------|------------------|
| Gross Margin | (Revenue - Effort Cost) / Revenue | 35-45% | Delivery efficiency |
| Contribution Margin | (Gross Margin - Direct Overhead) / Revenue | 10-15% | After PM, admin, compliance costs |
| Portfolio Margin | (Contribution Margin - Shared Overhead) / Revenue | 8-12% | After shared org costs |
| Net Programme Margin | (Portfolio Margin - Bench Allocation) / Revenue | 6-10% | True economic margin |

**Worked Example — Margin Compression Waterfall:**
- Revenue: ₹10M
- Effort Cost: ₹7.6M → Gross Margin: 24% (₹2.4M)
- Direct Overhead (PM, admin, compliance): ₹1.4M → Contribution Margin: 10% (₹1.0M)
- Shared Overhead: ₹0.2M → Portfolio Margin: 8% (₹0.8M)
- Bench Allocation: ₹0.765M → Net Margin: 0.35% (₹0.035M)

**Data Tables:** programs, projects, kpi_snapshots, commercial_scenarios, bench_tracking

---

### Tab 5: Risk & Governance
**Purpose:** RAID management, SLA tracking, governance health
**Answers:** "What can go wrong? Are we governing effectively?"

**Components:**
- Risk register table (sortable, filterable by programme/project/severity/status)
- Risk heatmap (5×5 probability × impact matrix)
- RAID trend chart (open/mitigated/closed over time)
- **SLA incident tracker** (individual P1-P4 incidents with timestamps, response/resolution times)
- SLA compliance dashboard (P1-P4 tiers)
- Governance maturity scorecard
- Forecast accuracy tracker (last 4 QBR predictions vs. actual)
- **Risk roll-up view** (project risks that exceed threshold auto-bubble to programme level)

**SLA Framework (4-Tier):**

| Priority | Response Time | Resolution Time | Penalty | Escalation |
|----------|--------------|-----------------|---------|------------|
| P1 — Critical | 15 min | 4 hours | 2% monthly bill | Immediate to DM + Client |
| P2 — High | 1 hour | 8 hours | 1% monthly bill | Within 4 hours to DM |
| P3 — Medium | 4 hours | 24 hours | Warning | Weekly report |
| P4 — Low | 8 hours | 72 hours | None | Sprint retro |

**Data Tables:** risks, risk_history, programs, projects, sla_incidents

---

### Tab 6: AI Governance & Productivity
**Purpose:** Govern AI tool usage, measure AI productivity impact, ensure trust
**Answers:** "Are AI tools helping or hurting? Can we trust AI-generated output?"

**Components:**
- AI tool registry (which tools, which programmes/projects, usage metrics)
- AI Trust Score dashboard (composite score with 6-factor breakdown)
- **AI vs. Traditional Team Comparison Panel** (see Section 11 — the core comparison framework)
- AI code quality metrics (AI vs. human: defect density, test coverage, review rejection rate)
- AI SDLC metrics (estimation accuracy, planning velocity, code review speed)
- AI governance maturity model (5 levels with current assessment)
- AI override log (when humans override, why, outcome)
- AI policy compliance tracker
- **AI cost-benefit analysis** (total AI tool cost vs. measured productivity gain vs. quality impact)
- **AI audit trail** (every AI-generated artifact logged with provenance, review status, production outcome)

**AI Trust Score Formula:**

```
AI Trust Score = (Provenance × 0.20) + (Review_Status × 0.25) + (Test_Coverage × 0.20)
               + (Drift_Check × 0.15) + (Human_Override_Rate × 0.10) + (Prod_Defect_Rate × 0.10)
```

| Factor | Weight | Scoring (0-100) | Source |
|--------|--------|-----------------|--------|
| Provenance | 20% | Tool verified + version locked = 100; Unknown = 0 | ai_tools |
| Review Status | 25% | 100% human-reviewed = 100; 0% = 0 | ai_code_metrics |
| Test Coverage | 20% | ≥80% = 100; 50-79% proportional; <50% = 0 | ai_code_metrics |
| Drift Check | 15% | Stable model + consistent output = 100 | ai_trust_scores |
| Human Override Rate | 10% | 10-30% = 100 (healthy); <10% = 50 (rubber-stamping); >30% = 40 (unreliable) | ai_override_log |
| Prod Defect Rate | 10% | 0 defects = 100; >5/sprint = 0 | ai_code_metrics |

**AI Governance Maturity Model:**

| Level | Score | Description |
|-------|-------|-------------|
| 0 — Unaware | 0-20 | No governance, no tracking |
| 1 — Ad-Hoc | 21-40 | Individual team rules, inconsistent |
| 2 — Managed | 41-60 | Documented policies, partial enforcement |
| 3 — Governed | 61-80 | Systematic enforcement, dashboards, audits |
| 4 — Optimized | 81-100 | Predictive controls, continuous improvement |

**5-Control Framework:**

| # | Control | Enforcement |
|---|---------|-------------|
| 1 | Mandatory Human Review | PR gate: AI-authored flag triggers review |
| 2 | Separate Quality Metrics | Defect density, coverage, rejection split by origin |
| 3 | Static Analysis Gates | CI/CD gate: lint, security, complexity |
| 4 | Override Protocol | Logged with timestamp, reason, outcome, approver |
| 5 | Sprint-Level Quality Retros | Retro agenda: trust score trend, incidents |

**Data Tables:** ai_tools, ai_tool_assignments, ai_usage_metrics, ai_code_metrics, ai_sdlc_metrics, ai_trust_scores, ai_override_log, ai_governance_config

---

### Tab 7: Smart Ops (Proactive Detection Engine)
**Purpose:** Proactive problem detection with one-click proposed actions
**Answers:** "What should I fix right now? Show me the problem AND the solution."

**Background Scheduler:** Evaluates all enabled triggers every 15 minutes. Fires alerts visible on Tab 1 ticker and Tab 7 alert badge.

**8 Proactive Detection Scenarios:**

| # | Scenario | Trigger | Proposed Action | Financial Impact |
|---|----------|---------|----------------|-----------------|
| 1 | Resource Rebalancing | Programme A util < 65% AND Programme B > 90% | Transfer named resource with impact calc | 1% util improvement ≈ ₹850K/year recovery |
| 2 | Bench Burn Prevention | Resource on bench > 15 days, no pipeline | Redeploy, cross-train, or managed exit | ₹260/day/person burn |
| 3 | Margin Leak Detection | Any of 7 loss categories exceeds threshold | Flag loss type, quantify, suggest recovery | 3-8% programme revenue |
| 4 | AI Governance Drift | Trust Score drops > 10 pts in 2 sprints | Flag tool, recommend intervention | 15-30% higher defect rate |
| 5 | SLA Breach Prediction | **Trend-based:** linear regression on last 8 weeks predicts breach within 14 days | Predict breach probability + suggest staffing | P1 penalty = 2% monthly bill |
| 6 | **CPI Trajectory Alert** | CPI declining 3 consecutive months AND TCPI > 1.2 | Flag programme as recovery-improbable, suggest scope reduction or sponsor escalation | EAC-based overrun projection |
| 7 | **Customer Satisfaction Drift** | CSAT drops > 0.5 points in 2 consecutive surveys OR escalation count doubles | Flag relationship risk, surface complaint themes | Contract renewal risk |
| 8 | **Pyramid Inversion Alert** | Actual blended rate drifts > 3% from planned for 2+ months | Flag rate card drift, show margin impact, propose rebalancing | 1% drift = ₹1.2M/year on 300-person unit |

**Data Tables:** resource_pool, scenario_executions, kpi_forecasts

---

### Tab 8: Commercials (Delivery P&L Intelligence)
**Purpose:** Full P&L visibility — the financial brain of the Command Center
**Answers:** "Are we making money? Where are we losing it? How do we recover?"

**Components:**
- P&L waterfall chart (Revenue → 4 margin layers → Net margin)
- 7 delivery loss categories with financial quantification
- Rate card economics dashboard (planned vs. actual blended rate, **by role tier**)
- **Utilization waterfall** (3-system comparison with gap breakdown: HRIS → RM → Billing)
- Bench cost allocation breakdown (shadow allocation formula)
- Change request economics (CR processing cost vs. CR value)
- Revenue leakage tracker (5 leak categories)
- QBR prep dashboard (5 numbers that matter)
- Programme closeout variance decomposition
- Estimation accuracy tracker (BAC vs. EAC vs. Actual)
- **Auto-generated financial narrative** for each programme
- **"Export as QBR PDF" button**

**(See Sections 7 and 8 for complete loss categories and formula reference)**

**Data Tables:** programs, projects, kpi_snapshots, commercial_scenarios, bench_tracking, scope_creep_log, loss_exposure, rate_cards, utilization_detail

---

### Tab 9: Settings & Administration
**Purpose:** System configuration, data management, user preferences
**Answers:** "How do I set this up? How do I get my data in?"

**Components:**
- **Guided onboarding wizard** (Step 1: locale/currency, Step 2: add programmes, Step 3: add first KPIs, Step 4: see dashboard — target: 15 minutes to first real data)
- **CSV upload with auto-column-mapping** (user uploads messy CSV, app shows headers, user maps to required fields, mapping saved for future uploads)
- Manual entry forms for each entity type
- Demo data reset button
- Programme + Project configuration
- KPI weight editor + threshold editor (pre-loaded from industry preset)
- Export workspace (JSON/CSV)
- Import workspace (restore from export)
- **Locale/currency selector** (INR, USD, EUR, GBP + custom)
- **Industry preset selector** (Indian IT Services, US Consulting, European MSP, Custom)
- Database status (row counts, last update, data freshness)
- API documentation link (Swagger)
- About / Version info

---

### Tab 10: Customer Intelligence (NEW)
**Purpose:** Customer satisfaction, expectation management, relationship health
**Answers:** "Is the customer happy? What are they expecting? Where are we falling short?"

**Why this tab exists:** A portfolio owner's biggest risk is not margin compression — it's contract non-renewal. Every commercial metric is meaningless if the customer walks. This tab tracks the relationship dimension that no EVM formula captures.

**Components:**
- **Customer Satisfaction (CSAT) trend** (monthly survey scores per programme, 12-month trend)
- **Net Promoter Score (NPS)** tracking (per programme and portfolio aggregate)
- **Expectation Gap Analysis** (what customer expected vs. what was delivered, by dimension: timeline, quality, communication, innovation, cost)
- **Escalation log** (every escalation with severity, resolution time, root cause, owner)
- **Customer communication tracker** (steering committees held vs. planned, action items open/closed)
- **Renewal probability estimator** (weighted composite of CSAT, delivery health, escalation frequency, executive relationship score)
- **Voice of Customer summary** (top 3 positive themes, top 3 concerns — manual entry or from survey data)

**Customer Expectation Framework:**

| Dimension | Customer Question | Metric | Source |
|-----------|------------------|--------|--------|
| Timeline | "Will you deliver on time?" | SPI + milestone adherence | evm_snapshots + milestones |
| Quality | "Is the output production-ready?" | Defect density + test coverage + rework % | kpi_snapshots + sprint_data |
| Communication | "Am I being kept informed?" | Steering meetings held % + action item closure rate | customer_satisfaction |
| Innovation | "Are you bringing new ideas?" | AI tool adoption + process improvement proposals | ai_usage_metrics |
| Cost | "Am I getting value for money?" | CPI + revenue realisation + margin (from customer's perspective: are they paying fair price?) | commercial_scenarios |
| Responsiveness | "How fast do you fix problems?" | SLA compliance + average P1/P2 resolution time | sla_incidents |
| Stability | "Is the team stable? Do I keep explaining things?" | Attrition rate + knowledge transfer incidents | resource_pool + loss_exposure |

**Renewal Probability Formula:**
```
Renewal Score = (CSAT × 0.30) + (Delivery Health × 0.25) + (Escalation Score × 0.20)
              + (Communication Score × 0.15) + (Innovation Score × 0.10)

Where:
- CSAT: Latest survey score normalised to 0-100
- Delivery Health: DHI from Tab 1
- Escalation Score: 100 - (Open Escalations × 15), min 0
- Communication Score: (Meetings Held / Meetings Planned) × 100
- Innovation Score: (Process Improvements Proposed + AI Initiatives Active) × 10, max 100

Interpretation:
≥ 80: Renewal highly likely (Green)
60-79: Renewal probable with attention (Amber)
< 60: Renewal at risk (Red) — trigger proactive account governance
```

**Data Tables:** customer_satisfaction, sla_incidents, programs

---

### Tab 11: Audit & Compliance (NEW)
**Purpose:** Audit readiness, governance control verification, compliance trail
**Answers:** "If an auditor walks in today, can we demonstrate governance? Is every AI-generated artifact traceable?"

**Why this tab exists:** Enterprise IT services operate under compliance frameworks (SOX, ISO 27001, CMMI, client-specific audit requirements). AI tool adoption adds a new dimension: can you prove that AI-generated code was reviewed, tested, and approved? This tab provides the evidence trail.

**Components:**
- **Governance Control Dashboard** (list of all active controls with compliance % per programme)
- **AI Audit Trail** (every AI-generated artifact: code, estimate, document — with provenance, reviewer, test result, production outcome)
- **Override Audit Report** (all human overrides of AI suggestions with rationale and outcome classification)
- **Process Compliance Scorecard** (planned reviews vs. actual, planned retros vs. actual, planned steering committees vs. actual)
- **Data Lineage Tracker** (for every dashboard number: which table, which formula, which input data — click any metric to see its calculation chain)
- **Export Audit Package** (generates a dated ZIP with: all governance controls + compliance %, AI audit trail, override log, process compliance evidence, data lineage snapshots)
- **Change Audit Trail** (every data change in the system logged in audit_log table)

**Audit Readiness Scorecard:**

| Dimension | What Auditor Asks | Evidence Source | Target |
|-----------|-------------------|-----------------|--------|
| Financial Controls | "Are costs tracked against budget?" | evm_snapshots + commercial_scenarios | CPI/SPI available monthly |
| AI Governance | "Is AI output reviewed before production?" | ai_override_log + ai_code_metrics | 100% review rate |
| Risk Management | "Are risks identified, assessed, mitigated?" | risks + risk_history | All risks have owner + plan |
| Change Management | "Are changes tracked and approved?" | scope_creep_log + audit_log | All CRs logged with approval |
| Quality Assurance | "Is quality measured and improving?" | sprint_data (defects, rework) | Rework % declining trend |
| Process Adherence | "Are governance meetings happening?" | customer_satisfaction (meeting tracker) | ≥ 90% meetings held |
| Data Integrity | "Can you trace every number?" | Data lineage + audit_log | Full traceability |

**Data Tables:** ai_override_log, ai_code_metrics, ai_governance_config, audit_log, risks, scope_creep_log, customer_satisfaction

---

## 5. DATABASE SCHEMA (44 TABLES — updated in v5.2)

### 5.1 Core Tables (10) — was 9, added projects

```sql
CREATE TABLE programs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    client TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    status TEXT DEFAULT 'Active',
    bac REAL,
    revenue REAL,
    team_size INTEGER,
    offshore_ratio REAL,
    delivery_model TEXT,
    currency_code TEXT DEFAULT 'INR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NEW: Projects sit under programmes
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'Active',
    bac REAL,
    revenue REAL,
    team_size INTEGER,
    tech_stack TEXT,
    is_ai_augmented BOOLEAN DEFAULT 0,
    ai_augmentation_level TEXT,          -- None, Light (docs/testing), Medium (code assist), Heavy (code gen + planning)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kpi_definitions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    formula TEXT NOT NULL,
    description TEXT,
    unit TEXT,
    green_threshold REAL,
    amber_threshold REAL,
    red_threshold REAL,
    weight REAL DEFAULT 1.0,
    category TEXT,
    is_higher_better BOOLEAN DEFAULT 1
);

CREATE TABLE kpi_snapshots (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),    -- NULL = programme-level
    kpi_id INTEGER REFERENCES kpi_definitions(id),
    snapshot_date DATE NOT NULL,
    value REAL NOT NULL,
    trend TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE risks (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),    -- NULL = programme-level risk
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    probability REAL,
    impact REAL,
    severity TEXT,
    status TEXT DEFAULT 'Open',
    owner TEXT,
    mitigation_plan TEXT,
    escalated_to_programme BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE risk_history (
    id INTEGER PRIMARY KEY,
    risk_id INTEGER REFERENCES risks(id),
    snapshot_date DATE NOT NULL,
    probability REAL,
    impact REAL,
    status TEXT,
    notes TEXT
);

CREATE TABLE initiatives (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    name TEXT NOT NULL,
    description TEXT,
    priority TEXT,
    score REAL,
    status TEXT DEFAULT 'Proposed',
    owner TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sprint_data (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),    -- NULL = programme-level
    sprint_number INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    planned_points INTEGER,
    completed_points INTEGER,
    velocity REAL,
    defects_found INTEGER,
    defects_fixed INTEGER,
    rework_hours REAL,
    team_size INTEGER,
    ai_assisted_points INTEGER DEFAULT 0,         -- Points where AI tools were used
    notes TEXT
);

CREATE TABLE backlog_items (
    -- Level 5 granularity: individual story / task / bug / spike inside a sprint.
    -- Invariant: sum(story_points WHERE status IN ('completed','added')) = sprint_data.completed_points
    --            sum(story_points WHERE status != 'added')               = sprint_data.planned_points
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    sprint_number INTEGER,
    item_type TEXT DEFAULT 'story',       -- story | bug | task | spike
    title TEXT NOT NULL,
    story_points INTEGER,
    status TEXT DEFAULT 'planned',        -- completed | carried_over | added
    assignee TEXT,
    is_ai_assisted BOOLEAN DEFAULT 0,
    defects_raised INTEGER DEFAULT 0,
    rework_hours REAL DEFAULT 0.0,
    priority TEXT                         -- critical | high | medium | low
);

CREATE TABLE commercial_scenarios (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    scenario_name TEXT,
    planned_revenue REAL,
    actual_revenue REAL,
    planned_cost REAL,
    actual_cost REAL,
    gross_margin_pct REAL,
    contribution_margin_pct REAL,
    portfolio_margin_pct REAL,
    net_margin_pct REAL,
    snapshot_date DATE,
    notes TEXT
);

-- NEW: EVM snapshots (fixes Critical Finding 4 — missing PV/EV)
CREATE TABLE evm_snapshots (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    snapshot_date DATE NOT NULL,
    planned_value REAL NOT NULL,
    earned_value REAL NOT NULL,
    actual_cost REAL NOT NULL,
    percent_complete REAL,
    bac REAL,
    cpi REAL,                            -- Computed: EV/AC
    spi REAL,                            -- Computed: EV/PV
    eac REAL,                            -- Computed: BAC/CPI
    tcpi REAL,                           -- Computed: (BAC-EV)/(BAC-AC)
    vac REAL,                            -- Computed: BAC-EAC
    notes TEXT
);
```

### 5.2 NEW Tables (7 — all addressing v5.0 gaps)

```sql
-- NEW: Milestones and dependencies (for Tab 3 timeline)
CREATE TABLE milestones (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    name TEXT NOT NULL,
    planned_date DATE NOT NULL,
    actual_date DATE,
    status TEXT DEFAULT 'Pending',       -- Pending, In Progress, Completed, Delayed, At Risk
    dependencies TEXT,                   -- JSON: [milestone_id, milestone_id]
    owner TEXT,
    notes TEXT
);

-- NEW: SLA incidents (for Tab 5 SLA tracking)
CREATE TABLE sla_incidents (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    incident_id TEXT,                    -- External ticket ID
    priority TEXT NOT NULL,              -- P1, P2, P3, P4
    summary TEXT,
    reported_at TIMESTAMP NOT NULL,
    responded_at TIMESTAMP,
    resolved_at TIMESTAMP,
    response_time_minutes REAL,          -- Computed
    resolution_time_minutes REAL,        -- Computed
    sla_breached BOOLEAN DEFAULT 0,
    penalty_amount REAL DEFAULT 0,
    root_cause TEXT,
    notes TEXT
);

-- NEW: Rate cards (for Tab 8 rate card drift tracking)
CREATE TABLE rate_cards (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    role_tier TEXT NOT NULL,             -- 'Senior Architect', 'Mid Engineer', 'Junior Developer', etc.
    planned_rate REAL NOT NULL,
    actual_rate REAL,
    planned_headcount INTEGER,
    actual_headcount INTEGER,
    snapshot_date DATE,
    notes TEXT
);

-- NEW: Utilization detail (for Tab 8 utilization waterfall)
CREATE TABLE utilization_detail (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE NOT NULL,
    hris_utilization REAL,               -- HR system (capacity)
    rm_utilization REAL,                 -- RM system (assignment)
    billing_utilization REAL,            -- Timesheet (billable)
    gap_leave_holidays REAL,             -- % lost to leave
    gap_bench_rotation REAL,             -- % lost to bench
    gap_rework_quality REAL,             -- % lost to rework
    gap_meetings_admin REAL,             -- % lost to overhead
    gap_transition_churn REAL,           -- % lost to attrition ramp
    gap_other REAL,
    notes TEXT
);

-- NEW: Customer satisfaction (for Tab 10)
CREATE TABLE customer_satisfaction (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE NOT NULL,
    csat_score REAL,                     -- 1-10 scale
    nps_score REAL,                      -- -100 to +100
    escalation_count INTEGER DEFAULT 0,
    escalation_open INTEGER DEFAULT 0,
    steering_meetings_planned INTEGER,
    steering_meetings_held INTEGER,
    action_items_open INTEGER,
    action_items_closed INTEGER,
    positive_themes TEXT,                -- JSON array
    concern_themes TEXT,                 -- JSON array
    renewal_score REAL,                  -- Computed composite
    notes TEXT
);

-- NEW: KPI forecasts (for predictive analytics)
CREATE TABLE kpi_forecasts (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    kpi_id INTEGER REFERENCES kpi_definitions(id),
    forecast_date DATE NOT NULL,         -- The future date being predicted
    forecast_value REAL NOT NULL,
    confidence_pct REAL,                 -- 0-100
    model_type TEXT,                     -- 'linear_regression', 'weighted_moving_avg', 'exponential_smoothing'
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NEW: Narrative cache (for auto-generated summaries)
CREATE TABLE narrative_cache (
    id INTEGER PRIMARY KEY,
    entity_type TEXT NOT NULL,           -- 'programme', 'portfolio', 'qbr', 'tab'
    entity_id INTEGER,
    narrative_text TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP               -- Invalidated on data change
);
```

### 5.3 AI Governance Tables (8 — consolidated from 9)

```sql
CREATE TABLE ai_tools (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    vendor TEXT,
    version TEXT,
    category TEXT,
    license_type TEXT,
    cost_per_seat REAL,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE ai_tool_assignments (
    id INTEGER PRIMARY KEY,
    ai_tool_id INTEGER REFERENCES ai_tools(id),
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    assigned_date DATE,
    users_count INTEGER,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE ai_usage_metrics (
    id INTEGER PRIMARY KEY,
    ai_tool_id INTEGER REFERENCES ai_tools(id),
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE,
    prompts_count INTEGER,
    suggestions_accepted INTEGER,
    suggestions_rejected INTEGER,
    time_saved_hours REAL,
    cost REAL
);

CREATE TABLE ai_code_metrics (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    sprint_number INTEGER,
    ai_lines_generated INTEGER,
    ai_lines_accepted INTEGER,
    ai_defect_count INTEGER,
    ai_test_coverage_pct REAL,
    ai_review_rejection_pct REAL,
    human_defect_count INTEGER,
    human_test_coverage_pct REAL,
    human_review_rejection_pct REAL,
    snapshot_date DATE
);

CREATE TABLE ai_sdlc_metrics (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    sprint_number INTEGER,
    estimation_accuracy_with_ai REAL,
    estimation_accuracy_without_ai REAL,
    code_review_hours_with_ai REAL,
    code_review_hours_without_ai REAL,
    planning_velocity_with_ai REAL,
    planning_velocity_without_ai REAL,
    documentation_hours_with_ai REAL,
    documentation_hours_without_ai REAL,
    snapshot_date DATE
);

CREATE TABLE ai_trust_scores (
    id INTEGER PRIMARY KEY,
    ai_tool_id INTEGER REFERENCES ai_tools(id),
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE,
    provenance_score REAL,
    review_status_score REAL,
    test_coverage_score REAL,
    drift_check_score REAL,
    override_rate_score REAL,
    defect_rate_score REAL,
    composite_score REAL,
    maturity_level TEXT
);

-- CONSOLIDATED: Merged ai_policies + ai_governance_controls into one table
CREATE TABLE ai_governance_config (
    id INTEGER PRIMARY KEY,
    config_type TEXT NOT NULL,            -- 'policy' or 'control'
    name TEXT NOT NULL,
    description TEXT,
    scope TEXT,                           -- Global, Programme, Team
    enforcement_method TEXT,
    program_id INTEGER REFERENCES programs(id),
    status TEXT DEFAULT 'Active',
    compliance_pct REAL,
    last_audit_date DATE,
    review_date DATE,
    owner TEXT
);

CREATE TABLE ai_override_log (
    id INTEGER PRIMARY KEY,
    ai_tool_id INTEGER REFERENCES ai_tools(id),
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    override_date TIMESTAMP,
    override_type TEXT,
    reason TEXT,
    outcome TEXT,
    approver TEXT
);
```

### 5.4 Smart Ops Tables (2 — consolidated from 4)

```sql
-- Scenario triggers and actions are hardcoded in smart_ops_engine.py for v1
-- Only execution log persists in DB

CREATE TABLE resource_pool (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    role_tier TEXT,                       -- Senior, Mid, Junior
    skill_set TEXT,
    current_program_id INTEGER REFERENCES programs(id),
    current_project_id INTEGER REFERENCES projects(id),
    utilization_pct REAL,
    bench_days INTEGER DEFAULT 0,
    loaded_cost_annual REAL,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE scenario_executions (
    id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,          -- Matches hardcoded scenario names
    execution_date TIMESTAMP,
    triggered_by TEXT,
    status TEXT,
    details TEXT,                         -- JSON with trigger data + proposed action
    financial_impact REAL,
    outcome_notes TEXT
);
```

### 5.5 Financial / Loss Tracking Tables (3 — unchanged)

```sql
CREATE TABLE bench_tracking (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE,
    planned_headcount INTEGER,
    actual_headcount INTEGER,
    bench_headcount INTEGER,
    loaded_cost_per_head REAL,
    shadow_allocation_cost REAL,
    allocation_method TEXT,
    notes TEXT
);

CREATE TABLE scope_creep_log (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    cr_date DATE,
    cr_description TEXT,
    effort_hours REAL,
    cr_value REAL,
    processing_cost REAL,
    status TEXT,
    margin_impact REAL,
    is_billable BOOLEAN
);

CREATE TABLE loss_exposure (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE,
    loss_category TEXT NOT NULL,
    amount REAL,
    percentage_of_revenue REAL,
    detection_method TEXT,
    mitigation_status TEXT,
    notes TEXT
);
```

### 5.6 Dual Velocity Tables (2 — unchanged)

```sql
CREATE TABLE sprint_velocity_dual (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    project_id INTEGER REFERENCES projects(id),
    sprint_number INTEGER,
    standard_velocity REAL,
    ai_raw_velocity REAL,
    ai_rework_points REAL,
    ai_quality_adjusted_velocity REAL,
    combined_velocity REAL,
    merge_eligible BOOLEAN DEFAULT 0,
    quality_parity_ratio REAL,
    snapshot_date DATE
);

CREATE TABLE sprint_velocity_blend_rules (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    gate_name TEXT NOT NULL,
    gate_condition TEXT,
    current_value REAL,
    threshold REAL,
    passed BOOLEAN DEFAULT 0,
    last_evaluated DATE
);
```

### 5.7 System Tables (3 — unchanged)

```sql
CREATE TABLE data_imports (
    id INTEGER PRIMARY KEY,
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    file_name TEXT,
    rows_imported INTEGER,
    status TEXT,
    column_mapping TEXT,                 -- JSON: saved mapping for auto-reuse
    notes TEXT
);

CREATE TABLE app_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Pre-loaded keys: currency_code, industry_preset, locale, org_name

CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    action TEXT,
    table_name TEXT,
    record_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    user_action TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.8 Customer Intelligence Tables (2 — v5.2 addition)

These two tables power Tab 10 (Customer Intelligence). `customer_satisfaction`
captures the monthly scorecard snapshot; these two capture the dimensional
gap analysis and the steering-committee action log that sit underneath it.

```sql
-- 36. customer_expectations — per-dimension gap analysis (Tab 10)
CREATE TABLE customer_expectations (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    snapshot_date DATE NOT NULL,
    dimension TEXT NOT NULL,             -- timeline | quality | communication | innovation | cost | responsiveness | stability
    expected_score REAL,                 -- 1–10 customer expectation
    delivered_score REAL,                -- 1–10 actual delivered value
    gap REAL,                            -- Computed: delivered_score - expected_score
    weight REAL DEFAULT 1.0,             -- Dimension weight in renewal composite
    evidence_source TEXT,                -- Survey / Escalation / Steering committee / Manual
    owner TEXT,
    notes TEXT
);

-- 37. customer_actions — steering-committee action-item tracker (Tab 10)
CREATE TABLE customer_actions (
    id INTEGER PRIMARY KEY,
    program_id INTEGER REFERENCES programs(id),
    meeting_date DATE,
    description TEXT NOT NULL,
    owner TEXT,
    due_date DATE,
    status TEXT DEFAULT 'Open',          -- Open | In Progress | Closed | Escalated
    priority TEXT,                       -- P1 | P2 | P3
    escalated BOOLEAN DEFAULT 0,
    resolution_notes TEXT,
    closed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### NEW v5.2 TABLES (5 added)

```sql
-- 38. flow_metrics (Kanban support)
flow_metrics (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    period_start DATE,
    period_end DATE,
    throughput_items INTEGER,
    wip_avg DECIMAL(6,2),
    wip_limit INTEGER,
    cycle_time_p50 DECIMAL(6,2),
    cycle_time_p85 DECIMAL(6,2),
    cycle_time_p95 DECIMAL(6,2),
    lead_time_avg DECIMAL(6,2),
    blocked_time_hours DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 39. project_phases (Waterfall support)
project_phases (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    phase_name TEXT NOT NULL,      -- Requirements | Design | Dev | Test | UAT | Deploy
    phase_sequence INTEGER,
    planned_start DATE,
    planned_end DATE,
    actual_start DATE,
    actual_end DATE,
    percent_complete DECIMAL(5,2),
    gate_status TEXT,              -- pending | passed | failed | conditional
    gate_approver TEXT,
    gate_date DATE,
    notes TEXT
);

-- 40. currency_rates
currency_rates (
    code TEXT PRIMARY KEY,          -- ISO 4217
    symbol TEXT,
    rate_to_base DECIMAL(18,8) NOT NULL,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'manual'
);

-- 41. data_import_snapshots (undo/rollback)
data_import_snapshots (
    id INTEGER PRIMARY KEY,
    import_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_filename TEXT,
    source_format TEXT,             -- csv | xlsx | manual
    row_count INTEGER,
    affected_tables TEXT,           -- JSON array
    pre_import_state BLOB,          -- gzipped SQL dump of affected rows
    status TEXT,                    -- committed | rolled_back
    rollback_timestamp DATETIME
);

-- 42. schema_version (Alembic-compatible)
schema_version (
    version TEXT PRIMARY KEY,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    applied_by TEXT
);

-- 43. users (stub — populated when auth is enabled, see SECURITY_GUIDE.md)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',       -- admin, portfolio_lead, viewer, api_service
    is_active BOOLEAN DEFAULT 1,
    auth_provider TEXT DEFAULT 'local',         -- local, google, azure_ad, okta, keycloak, github
    external_id TEXT,                           -- IdP subject identifier
    password_hash TEXT,                         -- bcrypt hash (local accounts only)
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 44. user_roles (fine-grained RBAC — populated when auth is enabled)
CREATE TABLE user_roles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL,                         -- admin, portfolio_lead, viewer, api_service
    scope_type TEXT,                            -- NULL (global), 'programme', 'project'
    scope_id INTEGER,                           -- programme or project ID (NULL = all)
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, role, scope_type, scope_id)
);

CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_users_email ON users(email);
```

**Total: 45 tables** (11 core + 7 new + 8 AI governance + 2 Smart Ops + 3 financial + 2 dual velocity + 3 system + 2 intelligence + 5 v5.2 + 2 security stub)

### NEW v5.2 PROJECTS.delivery_methodology

Projects table gets a new column:

```sql
ALTER TABLE projects ADD COLUMN delivery_methodology TEXT DEFAULT 'Scrum';
-- Allowed values: Scrum | Kanban | Waterfall | SAFe | Hybrid
```

### NEW v5.2 SPRINTS EXTENSIONS

Sprints table (renamed conceptually to "iterations") gets:

```sql
ALTER TABLE sprints ADD COLUMN iteration_type TEXT DEFAULT 'Sprint';   -- Sprint | Iteration | Cycle | Release
ALTER TABLE sprints ADD COLUMN estimation_unit TEXT DEFAULT 'StoryPoints';  -- StoryPoints | Hours | TShirt | Days
ALTER TABLE sprints ALTER COLUMN sprint_number DROP NOT NULL;  -- Kanban teams have no sprint number
```

---

## 6. SEVEN DELIVERY LOSS CATEGORIES

*(Unchanged from v5.0 — all 7 losses with formulas, worked examples, detection, prevention. See Section 5 of v5.0 document for full detail. The formulas, worked examples, and detection methods are preserved exactly.)*

**Summary:**

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

## 7. MASTER FORMULA REFERENCE (40+ Formulas)

*(37 formulas from v5.0 preserved. Added 3 new formulas.)*

**New formulas added in v5.1:**

| # | Formula | Calculation | Use Case |
|---|---------|------------|----------|
| 38 | Renewal Probability | Weighted(CSAT, DHI, Escalation, Communication, Innovation) | Contract renewal risk |
| 39 | AI Cost-Benefit Ratio | (Time Saved × Blended Rate) / (AI Tool Cost + Rework Cost) | AI investment ROI |
| 40 | Forecast Confidence | Based on R² of linear regression on last 6-12 data points | Prediction reliability |

---

## 8. DUAL VELOCITY TRACKING SYSTEM

*(Unchanged from v5.0 — dual track, quality-adjusted AI velocity, 6-gate merge protocol. See v5.0 for full detail.)*

---

## 9. AI-AUGMENTED vs. TRADITIONAL TEAM COMPARISON FRAMEWORK (NEW)

### 9.1 The Core Question

"My CTO asks: are the AI-augmented teams actually performing better than the traditional teams? Show me the data."

This is not a single metric — it's a multi-dimensional comparison that must account for quality, speed, cost, and governance overhead.

### 9.2 Comparison Dimensions (12)

| # | Dimension | Traditional Team Metric | AI-Augmented Team Metric | Comparison | Where to See |
|---|-----------|------------------------|-------------------------|------------|-------------|
| 1 | Velocity (raw) | Sprint velocity (story points) | Sprint velocity (story points) | Direct compare | Tab 3 |
| 2 | Velocity (quality-adjusted) | Velocity - rework points | AI quality-adjusted velocity | Direct compare | Tab 3 |
| 3 | Defect Density | Defects / 1000 lines | AI defects / 1000 AI lines | Ratio (target ≤ 1.2x) | Tab 6 |
| 4 | Test Coverage | Human test coverage % | AI test coverage % | Direct compare | Tab 6 |
| 5 | Code Review Rejection | Human review rejection % | AI review rejection % | Lower is better | Tab 6 |
| 6 | Estimation Accuracy | Estimated vs. actual hours | AI-estimated vs. actual hours | Closer to 1.0 is better | Tab 6 |
| 7 | Rework % | Rework hours / total hours | AI rework hours / AI total hours | Lower is better | Tab 3 |
| 8 | Cost per Story Point | Sprint cost / completed points | Sprint cost / AI-adjusted points | Lower is better | Tab 8 |
| 9 | Time to Market | Average feature cycle time | Average feature cycle time with AI | Days (lower is better) | Tab 3 |
| 10 | Governance Overhead | Standard review hours | AI review hours + override hours | Higher for AI (expected) | Tab 6 |
| 11 | Trust Score | N/A | AI Trust Score (0-100) | ≥ 75 = trusted | Tab 6 |
| 12 | Net Productivity Gain | Baseline velocity | (AI velocity - governance overhead) / baseline velocity | % improvement | Tab 4 |

### 9.3 The Honest Conversation with the CTO

**Question:** "Are AI teams faster?"
**Honest Answer Template:** "AI-augmented teams on Sentinel are delivering 22% higher raw velocity but 14% higher quality-adjusted velocity after rework deduction. Governance overhead adds 8 hours/sprint (3% of capacity). Net productivity gain is 11%. Cost per story point is 9% lower. However, defect density is 1.15x human baseline — within acceptable range but not yet at parity. We need 3 more sprints to evaluate merge readiness."

### 9.4 What the Dashboard Shows

On Tab 4 (Portfolio), a new comparison panel:

```
┌─────────────────────────────────────────────┐
│  AI-Augmented vs. Traditional Performance    │
│                                              │
│  Project: Sentinel Test Automation           │
│                                              │
│  Velocity:     Traditional 85 pts | AI 103 pts (adj: 97)  [+14%]
│  Defect Rate:  Traditional 4.2/K  | AI 4.8/K              [1.15x]
│  Rework %:     Traditional 8%     | AI 11%                 [+3pp]
│  Cost/Point:   Traditional ₹8.4K  | AI ₹7.6K              [-9%]
│  Trust Score:  N/A                | 86.1                    [Governed]
│  Merge Ready:  N/A                | 4/6 gates passed        [Sprint 19]
│                                              │
│  Net Assessment: AI tools are net-positive   │
│  with 11% productivity gain. Recommend       │
│  continued AI expansion with current         │
│  governance controls.                        │
└─────────────────────────────────────────────┘
```

---

## 10. SDLC FRAMEWORK COMPATIBILITY (NEW in v5.2)

### 10.1 The Problem

Enterprise portfolios are multi-methodology. A 150-person unit (our NovaTech persona) typically runs:
- 2-3 programmes on **Scrum** (application development)
- 1 programme on **Kanban** (support, maintenance, SRE)
- 1 programme on **Waterfall** (infrastructure, regulatory compliance, hardware)
- Some **hybrid** projects within the same programme

A tool that only speaks "Sprint Velocity" and "Story Points" alienates 40-50% of the portfolio. AKB1 Command Center adapts to the delivery methodology at the **project level** — not the portfolio level.

### 10.2 Supported Frameworks

| Framework | How AKB1 Adapts | Primary Metrics | Data Input |
|-----------|----------------|-----------------|------------|
| **Scrum** | Sprint burndown, velocity trend, story points, dual velocity | Velocity, Sprint Completion %, Defect Density | sprints.csv |
| **Kanban** | Cumulative flow diagram, cycle time trend, throughput chart, WIP tracking | Throughput, Cycle Time, Lead Time, WIP | flow_metrics.csv |
| **Waterfall** | Milestone timeline, phase progress bars, phase-gate approvals, EVM native | Milestone Adherence %, Phase Completion %, CPI/SPI | project_phases.csv + evm_monthly.csv |
| **SAFe** | PI timeline, iteration burndown, feature flow, PI predictability | PI Predictability, Feature Throughput, ART velocity | sprints.csv (iterations) + milestones (PI events) |
| **Hybrid** | Combined view — methodology label per project, mixed metrics dashboard | All of the above, filtered by project methodology | All templates accepted |

### 10.3 How It Works

**Configuration:** Each project has a `delivery_methodology` field set during onboarding or CSV import.

**UI Adaptation Logic:**
```
project.delivery_methodology determines which components render on Tabs 2, 3, 4:

Scrum    → Sprint burndown, velocity trend, story point tracking
Kanban   → Cumulative flow diagram, cycle time, throughput, WIP gauge
Waterfall → Milestone timeline, phase bars, phase-gate checklist
SAFe     → PI timeline + iteration burndown (Scrum at iteration level)
Hybrid   → Per-project toggle — each project renders its own methodology view
```

**Portfolio Aggregation:** Regardless of methodology, every project rolls up to the same portfolio-level KPIs:
- **CPI/SPI** — universal (EVM works for all methodologies; for Kanban, CPI is derived from cost/throughput)
- **Quality** — defect density, rework %, test coverage (universal)
- **Financial** — margin, revenue realisation, loss categories (universal)
- **Delivery Health Index (DHI)** — weighted composite adapts weights based on methodology (Kanban weighs throughput; Scrum weighs velocity; Waterfall weighs milestone adherence)

### 10.4 Estimation Unit Flexibility

| Unit | Who Uses It | How AKB1 Handles It |
|------|-------------|-------------------|
| Story Points | Scrum, SAFe teams | Default unit. Sprint velocity = points/sprint. |
| Hours | Waterfall, some Agile teams | Supported via `estimation_unit` field on sprint_data. Velocity = hours completed / hours planned. |
| Function Points | Large enterprise, government contracts | Supported as custom unit. Maps to effort via conversion factor in app_settings. |
| Throughput (items) | Kanban teams | Tracked in flow_metrics table. No "velocity" — uses throughput/week. |

### 10.5 Framework-Specific Implementation Scenarios

**Scenario: "We use Kanban for support. We don't have sprints."**
→ Set project `delivery_methodology = 'Kanban'`. Upload `flow_metrics.csv` instead of `sprints.csv`. Tab 3 shows cumulative flow diagram, not sprint burndown. KPI Studio shows Throughput and Cycle Time, not Velocity.

**Scenario: "Half our portfolio is Waterfall infrastructure."**
→ Set those projects to `delivery_methodology = 'Waterfall'`. Upload `project_phases.csv` + `evm_monthly.csv`. Tab 3 shows milestone timeline and phase-gate progress. Sprint metrics hidden for those projects.

**Scenario: "Project A is Scrum, Project B is Kanban — same programme."**
→ Each project has its own methodology. Programme-level view shows both side-by-side. Portfolio roll-up uses universal KPIs (CPI, Quality, Margin).

**Scenario: "We're transitioning from Waterfall to Agile mid-project."**
→ Change project methodology when transition happens. Historical data preserved under old methodology. New data enters under new methodology. Timeline shows transition point.

**Scenario: "We run SAFe with 8 teams in an ART."**
→ Map ART = Programme, Features = Projects, Iterations = Sprints. PI Planning events = Milestones with type 'PI_boundary'. PI Objectives tracked via initiatives table with PI-level scoring.

**Scenario: "We estimate in hours, not story points."**
→ Set `estimation_unit = 'hours'` on sprint_data entries. UI labels adapt: "Hours Planned" instead of "Points Planned." Velocity becomes "Hours Delivered / Hours Available."

### 10.6 SAFe Mapping Guide

| SAFe Concept | AKB1 Mapping | Notes |
|-------------|-------------|-------|
| Portfolio | All programmes (top level) | Direct map |
| Agile Release Train (ART) | Programme | 1 ART = 1 Programme |
| Team | Project | 1 Team = 1 Project within Programme |
| Program Increment (PI) | Milestone group with type 'PI_boundary' | PI start/end as milestones |
| PI Objective | Initiative with PI-level scoring | Use initiatives table |
| Iteration | Sprint (in sprint_data) | Direct map |
| Feature | Tracked via project-level metrics | Not a separate entity in v1 |
| Innovation & Planning Sprint | Sprint with `iteration_type = 'ip_sprint'` | Excluded from velocity calculations |

---

## 11. PREDICTIVE ANALYTICS ENGINE (NEW)

### 11.1 Purpose

Transform the dashboard from "what happened" to "what will happen."

### 10.2 Forecast Models

| Model | When Used | Algorithm |
|-------|----------|-----------|
| Linear Regression | KPIs with clear directional trend (CPI declining, margin compressing) | `scipy.stats.linregress` on last 6-12 data points |
| Weighted Moving Average | Volatile KPIs (velocity, defects) | 3-period WMA with weights [0.5, 0.3, 0.2] |
| Exponential Smoothing | Seasonal patterns (utilization, revenue) | Simple exponential with alpha=0.3 |

### 10.3 What Gets Forecasted

| KPI | Forecast Horizon | Trigger for Alert |
|-----|-----------------|-------------------|
| CPI | 3 months forward | Forecast CPI < 0.85 |
| SPI | 3 months forward | Forecast SPI < 0.80 |
| Margin | Quarter-end | Forecast margin < plan by > 3 points |
| Utilization | 3 months forward | Forecast billing util < 65% |
| SLA compliance | 4 weeks forward | Trend predicts breach within 14 days |
| CSAT | Next survey | Forecast CSAT drop > 0.5 points |
| AI Trust Score | 2 sprints forward | Forecast trust < 60 |

### 10.4 Display

All trend charts show:
- **Solid line:** Historical actuals
- **Dashed line:** Forecast with confidence band (shaded area)
- **Red zone:** Threshold below which alert triggers

---

## 12. NARRATIVE GENERATION ENGINE (NEW)

### 12.1 Purpose

Auto-generate the "So What?" for every data point. Template-based for v1 (no LLM dependency).

### 12.2 Narrative Templates

**CPI Narrative:**
```python
if cpi < 0.85:
    f"CRITICAL: {program} is spending ₹{1/cpi:.2f} for every ₹1 of value. "
    f"EAC projects final cost at {eac}M ({overrun_pct:.1f}% over budget). "
    f"TCPI of {tcpi:.2f} indicates recovery is {'improbable' if tcpi > 1.2 else 'challenging'}. "
    f"Recommend {'scope reduction' if tcpi > 1.3 else 'efficiency review + sponsor conversation'}."
elif cpi < 0.95:
    f"{program} is running {(1-cpi)*100:.1f}% above budget. "
    f"Primary driver: {top_loss_category}. Recovery target: {recovery_action}."
else:
    f"{program} CPI at {cpi:.2f} — on budget. No action required."
```

**Margin Narrative:**
```python
if margin_trend == 'declining' and months_declining >= 3:
    f"Margin has declined from {m1}% to {m_current}% over {months_declining} months. "
    f"Primary drivers: {', '.join(top_2_losses)}. "
    f"Quarterly impact: ₹{quarterly_impact}. "
    f"Recovery path: {recovery_action} recovers {recovery_pct} points."
```

**Portfolio Summary:**
```python
f"Portfolio of {program_count} programmes tracking at {portfolio_margin}% net margin "
f"({'above' if above_plan else 'below'} plan by {abs(variance):.1f} points). "
f"{red_count} programme(s) at Red status. "
f"Top concern: {worst_programme} ({worst_reason}). "
f"{'No immediate escalation needed.' if red_count == 0 else f'Recommend steering committee review for {worst_programme}.'}"
```

### 11.3 Where Narratives Appear

- Tab 1: Portfolio summary narrative (always visible)
- Tab 3: Per-programme EVM narrative (in tooltip and sidebar)
- Tab 8: Per-programme financial narrative
- Tab 10: Customer relationship narrative
- "Generate QBR Brief" button: Consolidates all narratives into copy-paste format

---

## 13. LOCALISATION & MULTI-CURRENCY (NEW — expanded in v5.2)

### 13.1 First-Run Setup

On first launch, the guided wizard asks:
1. **Base Currency:** INR (₹), USD ($), EUR (€), GBP (£), or ANY ISO-4217 code
2. **Industry Preset:** Indian IT Services | US Consulting | European MSP | Custom
3. **Fiscal Year:** Indian (Apr–Mar) | US (Jan–Dec) | UK/Saudi (Apr–Mar) | Japan/US-Fed (Oct–Sep) | Custom
4. **Number Format:** Indian (lakh/crore) | US (thousand/million/billion) | European (1.000.000,00)
5. **Date Format:** DD/MM/YYYY | MM/DD/YYYY | YYYY-MM-DD
6. **Organisation Name:** (displayed in headers and exports)

### 13.2 Industry Preset Effects

| Setting | Indian IT Services | US Consulting | European MSP |
|---------|-------------------|---------------|-------------|
| Currency | INR (₹) | USD ($) | EUR (€) |
| Gross Margin target | 35–45% | 40–55% | 30–40% |
| Billing Utilization target | 71–76% | 65–72% | 60–68% |
| Loaded Cost range | ₹50K–₹120K | $80K–$200K | €60K–€150K |
| Bench % healthy range | 10–15% | 8–12% | 12–18% |
| Attrition rate benchmark | 15–22% | 12–18% | 8–15% |
| SLA framework | P1–P4 (as designed) | P1–P4 (adjusted response times) | ITIL-aligned |
| Offshore ratio default | 0.65 | 0.40 | 0.30 |
| Default FY | Apr–Mar | Jan–Dec | Jan–Dec |

All benchmarks stored in `app_settings` and fully editable after initial setup.

### 13.3 Multi-Currency Conversion Engine (NEW in v5.2)

**Problem solved:** A programme in GBP, another in USD, another in INR — portfolio totals need to aggregate correctly. Users outside India must see their native base currency without losing per-programme detail.

**Design:**

```
currency_rates (
    code TEXT PRIMARY KEY,          -- ISO 4217, e.g. 'USD'
    symbol TEXT,                    -- '$'
    rate_to_base DECIMAL(18,8),     -- units of base per 1 unit of this currency
    last_updated DATETIME,
    source TEXT                     -- 'manual' | 'api' (v5.3)
)
```

**Aggregation rule:** every numeric value in the database is stored in its programme's native currency. At query time, the aggregation layer multiplies by `rate_to_base` for portfolio-level rollups. Tooltips show both native and base values.

**Conversion formula:**

```
amount_base = amount_native × rate_to_base
```

**Worked example 1:** GlobalBank programme has USD 2,500,000 revenue. Base currency = INR. Rate = 83.25. Displayed in portfolio total as ₹20.81 Cr. Tooltip: "USD 2,500,000 @ 83.25 (updated 2026-04-15)".

**Worked example 2:** RetailCo programme has GBP 1,200,000 revenue. Base currency = USD. Rate = 1.27. Displayed in portfolio total as USD 1,524,000. Tooltip: "GBP 1,200,000 @ 1.27 (updated 2026-04-12)".

**Rate update:** Tab 11 Settings exposes an editable grid with every active currency. Manual edit is the v5.2 mode. v5.3 adds optional daily auto-refresh from a configurable API (ECB, exchangerate.host, user-provided URL).

### 13.4 Fiscal Year Configuration

Stored as `app_settings.fy_start_month` (1–12). All month-over-month, quarter, and YTD calculations use this anchor. Reports adapt labels automatically (e.g., "Q1 FY26" for Indian FY starting April).

### 13.5 Number Format Localisation

| Locale | 10,000,000 displays as | 12,345.67 displays as |
|--------|------------------------|------------------------|
| Indian | 1,00,00,000 (1 Cr) | 12,345.67 |
| US | 10,000,000 (10 M) | 12,345.67 |
| European | 10.000.000 | 12.345,67 |

Implementation: client-side via Intl.NumberFormat with the configured locale code.

### 13.6 Date Format Localisation

Applied consistently across UI and exports. Stored dates are always ISO 8601 in the DB; only the display layer formats.

---

## 14. DATA INGESTION ARCHITECTURE (UPDATED)

### 13.1 Three Modes + Guided Wizard

| Mode | How | Time to First Data | Audience |
|------|-----|-------------------|----------|
| **Guided Wizard** (NEW) | Step-by-step: locale → add programmes → add first KPIs → see dashboard | **15 minutes** | First-time users |
| Demo Data | Pre-loaded via seed on first run | Instant | Evaluators |
| CSV Upload + **Auto-Mapping** | Upload any CSV, map columns visually, save mapping | 30-60 minutes | Portfolio teams |
| Manual Entry | Forms per entity type | Ongoing | Programme managers |

### 13.2 CSV Auto-Mapping (NEW)

```
User uploads: "Q3_2026_Programme_Report.xlsx"
App detects columns: [Programme Name, Budget, Actual Spend, % Complete, Risk Count, ...]
App suggests mapping:
  "Programme Name"  → programs.name        [Auto-matched: 95% confidence]
  "Budget"          → programs.bac         [Auto-matched: 82% confidence]
  "Actual Spend"    → evm_snapshots.actual_cost  [Suggested: verify]
  "% Complete"      → evm_snapshots.percent_complete [Auto-matched: 90%]
  "Risk Count"      → [No match — skip or create custom KPI]

User confirms/adjusts → mapping saved as template for next upload.
```

### 13.3 Minimum Viable Data (NEW)

The app renders meaningful dashboards with just 2 data inputs:
1. **programmes** (name, code, BAC, revenue, team_size)
2. **kpi_monthly** (CPI, utilization, margin)

Everything else gracefully degrades to "No data yet — upload [CSV template name] to see this section."

### 13.4 API Endpoints (UPDATED)

```
# Programmes + Projects
GET    /api/v1/programs
GET    /api/v1/programs/{id}
GET    /api/v1/programs/{id}/projects
POST   /api/v1/programs
POST   /api/v1/projects
PUT    /api/v1/programs/{id}
PUT    /api/v1/projects/{id}

# KPIs
GET    /api/v1/kpis
GET    /api/v1/kpis/{program_id}/snapshots
GET    /api/v1/kpis/{program_id}/forecasts         # NEW
POST   /api/v1/kpis/snapshots

# EVM (NEW)
GET    /api/v1/evm/{program_id}
POST   /api/v1/evm/snapshots

# Risks
GET    /api/v1/risks
GET    /api/v1/risks/{program_id}
POST   /api/v1/risks
PUT    /api/v1/risks/{id}

# Sprints
GET    /api/v1/sprints/{program_id}
POST   /api/v1/sprints

# Financials
GET    /api/v1/financials/{program_id}
POST   /api/v1/financials

# AI Governance
GET    /api/v1/ai/tools
GET    /api/v1/ai/trust-scores/{program_id}
GET    /api/v1/ai/metrics/{program_id}
GET    /api/v1/ai/comparison/{program_id}           # NEW: AI vs Traditional
POST   /api/v1/ai/override-log

# Smart Ops
GET    /api/v1/smartops/alerts                      # NEW: Active alerts
GET    /api/v1/smartops/executions
POST   /api/v1/smartops/acknowledge/{execution_id}  # NEW

# Customer Intelligence (NEW)
GET    /api/v1/customer/{program_id}
POST   /api/v1/customer/satisfaction
GET    /api/v1/customer/{program_id}/renewal-score

# Narratives (NEW)
GET    /api/v1/narratives/portfolio
GET    /api/v1/narratives/{program_id}
GET    /api/v1/narratives/qbr-brief/{program_id}

# Reports (NEW)
GET    /api/v1/reports/qbr/{program_id}             # Printable QBR
GET    /api/v1/reports/audit-package                 # Audit ZIP

# Data Management
POST   /api/v1/import/csv
POST   /api/v1/import/csv/auto-map                  # NEW: column mapping
POST   /api/v1/import/reset-demo
GET    /api/v1/export/workspace
POST   /api/v1/import/workspace

# Settings
GET    /api/v1/settings
PUT    /api/v1/settings
POST   /api/v1/settings/locale                      # NEW
```

---

## 15. CTO/CIO/CEO QUESTION MAP (58 QUESTIONS — expanded from 50)

### Financial Performance (12 questions — Tab 8)

| # | Question | Answer Source |
|---|----------|--------------|
| 1 | Are we making enough margin? | 4-layer margin waterfall |
| 2 | Where are we losing money? | 7 delivery loss categories |
| 3 | What is true utilization vs. reported? | 3-system utilization waterfall |
| 4 | How much does bench cost us? | Shadow allocation formula |
| 5 | Are CRs margin-positive or negative? | CR processing cost vs. CR value |
| 6 | What is our revenue leakage? | 5-category leakage tracker |
| 7 | Will we hit profit target this quarter? | EAC-based margin forecast + **predictive projection** |
| 8 | What does rate card drift look like? | Planned vs. actual blended rate **by role tier** |
| 9 | What is CPI telling us? | CPI trend + EAC + **3-month forecast** |
| 10 | What is closeout variance? | 5-component decomposition |
| 11 | **What is AI costing us vs. saving us?** | AI cost-benefit ratio (Formula #39) |
| 12 | **What is the cost per story point: AI vs. traditional?** | Sprint cost / points comparison |

### Delivery Health (6 questions — Tabs 1, 3, 4)

| # | Question | Answer Source |
|---|----------|--------------|
| 13 | Which programmes need attention? | Portfolio CPI heatmap + DHI |
| 14 | Are we on schedule? | SPI + milestone tracking |
| 15 | What is sprint velocity trend? | Burndown + velocity chart |
| 16 | How accurate are forecasts? | Forecast vs. actual + **prediction accuracy** |
| 17 | What is overall portfolio health? | DHI composite + radar chart |
| 18 | **Which projects within a programme are dragging?** | Project-level CPI drill-down |

### Risk & Governance (5 questions — Tab 5)

| # | Question | Answer Source |
|---|----------|--------------|
| 19 | Top 3 risks by financial impact? | Risk register sorted by impact |
| 20 | Are we governing effectively? | Governance maturity score |
| 21 | SLA compliance rate? | P1-P4 SLA incident tracker |
| 22 | How reliable is risk forecasting? | Risk prediction accuracy |
| 23 | **What is the predicted SLA breach risk?** | Trend-based forecast |

### AI Governance (7 questions — Tab 6)

| # | Question | Answer Source |
|---|----------|--------------|
| 24 | Are AI tools actually helping? | AI SDLC impact metrics |
| 25 | Can we trust AI-generated code? | Trust Score + defect comparison |
| 26 | AI governance maturity? | 5-level maturity assessment |
| 27 | How often do humans override AI? | Override log analysis |
| 28 | What is AI productivity tax? | Rework cost from AI work |
| 29 | **AI teams vs. traditional — give me the comparison** | 12-dimension comparison panel |
| 30 | **Is the AI velocity reliable enough to plan with?** | 6-gate merge protocol status |

### Customer & Relationship (6 questions — Tab 10 NEW)

| # | Question | Answer Source |
|---|----------|--------------|
| 31 | **Is the customer happy?** | CSAT trend + NPS |
| 32 | **What are they complaining about?** | Concern themes from surveys |
| 33 | **Will they renew?** | Renewal probability score |
| 34 | **Are we meeting their expectations?** | Expectation gap analysis (7 dimensions) |
| 35 | **How responsive are we to their problems?** | Average P1/P2 resolution time trend |
| 36 | **Are we communicating enough?** | Steering meetings held % + action item closure |

### Strategic & Operational (6 questions — Tab 7)

| # | Question | Answer Source |
|---|----------|--------------|
| 37 | What should I fix right now? | Smart Ops proactive alerts |
| 38 | Where can I reallocate resources? | Resource rebalancing scenario |
| 39 | Bench runway? | Bench burn calculation |
| 40 | What is the QBR story in 5 numbers? | 5-number summary + narrative |
| 41 | **What does the forecast say about next quarter?** | Predictive engine output |
| 42 | **Is pyramid inversion happening?** | Rate card drift alert |

### Estimation & Planning (4 questions — Tab 3)

| # | Question | Answer Source |
|---|----------|--------------|
| 43 | How accurate were estimates? | BAC vs. EAC vs. Actual |
| 44 | Efficiency needed to finish on budget? | TCPI calculation |
| 45 | Estimation bias across portfolio? | Estimation variance trend |
| 46 | **What will this programme actually cost?** | EAC with forecast confidence band |

### People & Capacity (4 questions — Tab 7)

| # | Question | Answer Source |
|---|----------|--------------|
| 47 | Attrition cost? | Replacement cost formula |
| 48 | Right skill pyramid? | Planned vs. actual role distribution |
| 49 | Weekly utilization recovery? | Weekly vs. monthly tracking delta |
| 50 | **Team stability — are we keeping people?** | Attrition rate by programme + tenure tracking |

### Audit & Compliance (NEW — asked by auditors, not CTO, but CTO needs to answer)

These are handled by Tab 11 and don't need to be in the CTO question map, but the CTO needs to know the answer exists:
- "Can you prove AI output was reviewed?" → Tab 11 AI audit trail
- "Show me your change management evidence" → Tab 11 audit package
- "Is every dashboard number traceable?" → Tab 11 data lineage

---

## 16. PHASED BUILD PLAN (UPDATED)

### v5.0-alpha (Next Session Target — Minimum Viable Command Center)

**Tabs:** 1 (Executive Overview), 2 (KPI Studio), 4 (Portfolio), 8 (Commercials), 9 (Settings — wizard + CSV import)

**Backend:** All 37 tables, core API endpoints, demo data seeder, basic forecast engine, narrative templates for Tabs 1 and 8

**This alpha answers 30 of the 58 CTO questions and ships the financial intelligence core.**

| Step | What | Hours Est. |
|------|------|-----------|
| 1 | FastAPI skeleton + SQLite schema (37 tables) | 4 |
| 2 | Demo data seeder (5 programmes + projects × 12 months) | 4 |
| 3 | Core API: programmes, projects, KPIs, EVM, financials | 6 |
| 4 | Forecast engine (linear regression on CPI/margin/util) | 3 |
| 5 | Narrative generator (template-based, 4 templates) | 2 |
| 6 | React scaffold + Tailwind + layout shell | 3 |
| 7 | Tab 1: Executive Overview + narrative + alerts | 6 |
| 8 | Tab 2: KPI Studio + formula tooltips | 5 |
| 9 | Tab 4: Portfolio + comparison matrix + AI vs. Traditional | 6 |
| 10 | Tab 8: Commercials + margin waterfall + utilization waterfall | 8 |
| 11 | Tab 9: Settings (wizard + CSV upload + locale) | 5 |
| 12 | Docker Compose + Dockerfiles + health check | 3 |
| **Total** | | **55 hours** |

### v5.1-beta (Session +1)

**Add Tabs:** 3 (Delivery Planning), 5 (Risk & Governance), 10 (Customer Intelligence)

### v5.2-release (Session +2)

**Add Tabs:** 6 (AI Governance), 7 (Smart Ops with background scheduler), 11 (Audit & Compliance)
**Add:** Export as PDF, QBR brief generator, audit package export, full predictive engine

---

## 17. DEMO NARRATIVE (UPDATED)

**You are the Delivery Director at NovaTech Solutions**, a 150-person IT services unit managing 5 programmes for a global banking client. Your portfolio revenue is ₹41M annually. Here's your Monday morning reality:

| Programme | Revenue | Team | Story | Key Problem |
|-----------|---------|------|-------|-------------|
| **Phoenix** | ₹10M | 25 | Legacy core banking migration — 18 months in, scope keeps growing | CPI at 0.81, 3 uncontrolled CRs this month, margin compressed from 22% to 14% |
| **Atlas** | ₹8M | 18 | Multi-cloud migration — technically on track but financially razor-thin | Margin at 8% after bench allocation, one attrition away from loss |
| **Sentinel** | ₹5M | 12 | Test automation with heavy AI augmentation — the pilot everyone watches | AI Trust Score 86, velocity +14% over baseline, but defect density 1.15x |
| **Orion** | ₹12M | 30 | Big data platform — your cash cow | Bench tax absorbing ₹1.4M, actual margin 16% vs planned 24% |
| **Titan** | ₹6M | 15 | E-commerce platform with 99.9% SLA requirement | 2 P1 breaches last quarter, attrition at 25%, CSAT dropped to 6.8 |

The demo data tells this story. Every chart, every alert, every narrative is grounded in this portfolio's reality.

---

## 18. CONSTRAINTS & NON-FUNCTIONAL REQUIREMENTS (UPDATED to v5.2)

| Requirement | Specification |
|-------------|--------------|
| Deployment | Single `docker compose up -d` (v2) or `docker-compose up -d` (v1) — no manual steps |
| Port | 9000 (frontend), 9001 (backend API, internal) |
| Isolation | MUST NOT interfere with 8080, 8502, 8503 |
| Data persistence | Docker volume mount — survives restarts |
| **Backup** | **Automated daily SQLite backup, 30-day rolling retention** |
| **Data import safety** | **Snapshot + one-click rollback via data_import_snapshots table** |
| **Schema migration** | **Alembic migrations run on container start** |
| Demo data | Pre-loaded on first run, resettable via UI |
| **First real data** | **15 minutes via guided wizard (minimum viable: 2 CSV/XLSX files)** |
| **xlsx support** | **Native .xlsx import/export via openpyxl** |
| **SDLC framework** | **Scrum, Kanban, Waterfall, SAFe, Hybrid (per-project methodology)** |
| **Multi-currency** | **INR, USD, EUR, GBP + any ISO 4217 — editable rates, portfolio base-currency aggregation** |
| **Fiscal year** | **Configurable: Apr–Mar, Jan–Dec, Oct–Sep, custom** |
| **Number format** | **Indian (lakh/crore), US, European** |
| API documentation | Auto-generated OpenAPI at /docs |
| Browser support | Chrome, Safari, Firefox, **Edge** (latest 2 versions) |
| **Operating system** | **Windows 10/11 (Docker Desktop + WSL2), macOS (Intel + Apple Silicon), Linux (Ubuntu 22.04+)** |
| Mobile responsive | Desktop-first (≥ 1280px); tablet-friendly; not phone-optimised |
| Performance | Dashboard loads < 2 seconds with 5 programmes; TTI < 3s on 4-core/8GB |
| **Forecast latency** | **< 500ms for 12-month dataset per KPI** |
| **Accessibility** | **WCAG 2.1 AA contrast, keyboard navigation, ARIA labels, screen-reader pass (NVDA/VoiceOver)** |
| **Webhook alerts** | **Smart Ops scenarios can notify email / Slack / Teams via configurable webhooks** |
| **Security** | **4-tier auth strategy (None → Basic Auth → OAuth2 Proxy → Built-in OIDC). Localhost bind default (127.0.0.1). CORS hardening. Rate limiting (slowapi). API key auth. Non-root containers. Read-only filesystem. No hardcoded secrets. Trivy scan clean at release. OWASP Top 10 mapped. See SECURITY_GUIDE.md** |
| License | MIT — open-source, fork-friendly |
| **Localisation** | **Multi-currency, industry presets, editable thresholds, date/number format** |
| Brand | Navy #1B2A4A / Ice Blue #D5E8F0 / Amber #F59E0B exclusively |
| **Tables** | **45 (was 37 → 42 → 44 → 45 — added flow_metrics, project_phases, currency_rates, data_import_snapshots, schema_version, users, user_roles)** |
| **Formulas** | **45 (was 40 — added currency conversion + Kanban throughput/cycle/lead/WIP-aging)** |
| **CTO questions** | **58 (was 50 — added 8 for Kanban/Waterfall/currency/FY)** |
| **CSV templates** | **15 (was 13 — added flow_metrics.csv + project_phases.csv)** |
| **Tabs** | **11 (was 9 — added Reports/Exports tab and Data Hub/Settings tab)** |

---

## 19. FILE STRUCTURE (UPDATED)

```
akb1-command-center/
├── README.md
├── LICENSE (MIT)
├── SECURITY.md                          # NEW v5.2: Vulnerability disclosure policy
├── docker-compose.yml
├── docker-compose.proxy.yml             # NEW v5.2: Caddy reverse proxy overlay (HTTPS + Basic Auth)
├── docker-compose.sso.yml              # NEW v5.2: OAuth2 Proxy SSO overlay (documented)
├── Caddyfile                            # NEW v5.2: Caddy config (TLS, headers, auth)
├── .env.example
├── .gitignore
├── .github/workflows/ci.yml
│
├── docs/
│   ├── ARCHITECTURE.md                 # This document (v5.2)
│   ├── SECURITY_GUIDE.md              # NEW v5.2: Comprehensive security guide (4-tier auth, OWASP)
│   ├── MASTER_CHECKLIST.md             # NEW v5.2: consolidated verification baseline
│   ├── WIREFRAMES.md                   # NEW v5.2: all 11 tabs + metric dictionaries
│   ├── TECH_STACK_BENCHMARK.md         # NEW v5.2: stack research + recommendations
│   ├── PRODUCTION_SDLC.md              # NEW v5.2: SDLC adoption plan
│   ├── DATA_INGESTION.md
│   ├── FORMULAS.md                     # 45 formulas with worked examples
│   ├── CTO_QUESTIONS.md                # 58 questions mapped
│   ├── CONTRIBUTING.md
│   ├── EARLY_ADOPTER_FAQ.md
│   ├── DEMO_GUIDE.md                   # Narrative walkthrough
│   ├── ROADMAP.md                      # alpha → beta → release
│   └── csv-templates/                  # 15 CSV templates (added flow_metrics, project_phases)
│       ├── programmes.csv
│       ├── projects.csv                # NEW
│       ├── kpi_monthly.csv
│       ├── evm_monthly.csv             # NEW
│       ├── risks.csv
│       ├── sprints.csv
│       ├── financials.csv
│       ├── ai_tools.csv
│       ├── ai_metrics.csv
│       ├── resources.csv
│       ├── bench.csv
│       ├── change_requests.csv
│       ├── losses.csv
│       ├── flow_metrics.csv              # NEW v5.2 (Kanban)
│       └── project_phases.csv            # NEW v5.2 (Waterfall)
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── api/
│   │   │   ├── programs.py
│   │   │   ├── projects.py             # NEW
│   │   │   ├── kpis.py
│   │   │   ├── evm.py                  # NEW
│   │   │   ├── risks.py
│   │   │   ├── sprints.py
│   │   │   ├── financials.py
│   │   │   ├── ai_governance.py
│   │   │   ├── smart_ops.py
│   │   │   ├── velocity.py
│   │   │   ├── customer.py             # NEW
│   │   │   ├── narratives.py           # NEW
│   │   │   ├── reports.py              # NEW
│   │   │   ├── data_management.py
│   │   │   └── settings.py
│   │   ├── models/ (...)
│   │   ├── services/
│   │   │   ├── kpi_calculator.py
│   │   │   ├── forecast_engine.py      # NEW
│   │   │   ├── narrative_generator.py  # NEW
│   │   │   ├── smart_ops_engine.py
│   │   │   ├── trust_score.py
│   │   │   ├── velocity_merger.py
│   │   │   ├── loss_detector.py
│   │   │   ├── renewal_scorer.py       # NEW
│   │   │   └── csv_importer.py
│   │   └── seed/
│   │       ├── seed_demo_data.py
│   │       └── demo_narrative.json     # NEW: Story-driven demo data
│   └── tests/
│       ├── test_formulas.py
│       ├── test_forecast.py            # NEW
│       ├── test_narratives.py          # NEW
│       ├── test_trust_score.py
│       ├── test_velocity_merge.py
│       ├── test_loss_detection.py
│       └── test_api.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── nginx.conf
│   └── src/
│       ├── pages/
│       │   ├── ExecutiveOverview.jsx
│       │   ├── KPIStudio.jsx
│       │   ├── DeliveryPlanning.jsx
│       │   ├── Portfolio.jsx
│       │   ├── RiskGovernance.jsx
│       │   ├── AIGovernance.jsx
│       │   ├── SmartOps.jsx
│       │   ├── Commercials.jsx
│       │   ├── Settings.jsx
│       │   ├── CustomerIntelligence.jsx # NEW
│       │   └── AuditCompliance.jsx      # NEW
│       ├── components/
│       │   ├── ... (existing)
│       │   ├── NarrativeBlock.jsx       # NEW
│       │   ├── ForecastChart.jsx        # NEW
│       │   ├── AIComparisonPanel.jsx    # NEW
│       │   ├── OnboardingWizard.jsx     # NEW
│       │   ├── CSVAutoMapper.jsx        # NEW
│       │   ├── RenewalGauge.jsx         # NEW
│       │   └── AlertBadge.jsx           # NEW
│       └── ...
│
└── scripts/
    ├── setup.sh
    ├── seed.sh
    └── export-db.sh
```

---

## 20. SECURITY ARCHITECTURE (NEW in v5.2)

### 20.1 Design Philosophy

AKB1 Command Center is a **localhost-first, single-user application**. Security is layered progressively — deployers choose the tier that matches their exposure level. No security overhead for personal laptop use; full enterprise-grade protection available for cloud deployments.

**Industry precedent:** Grafana (anonymous → org viewer → LDAP/OIDC), Metabase (no auth → basic → SSO), Prometheus (no built-in auth → reverse proxy pattern).

### 20.2 4-Tier Authentication Strategy

| Tier | Mechanism | Config Effort | Deployment Scenario |
|------|-----------|--------------|-------------------|
| 0 — None | `127.0.0.1` binding, no auth | Zero | Personal laptop, demo |
| 1 — Basic Auth | Caddy/Nginx `basicauth` + HTTPS | 10 min | Team LAN, small office |
| 2 — OAuth2 Proxy | Sidecar container + IdP (Google/Azure AD/Okta/Keycloak/GitHub) | 30 min | Corporate VPN, cloud VM |
| 3 — Built-in OIDC | python-jose + authlib in FastAPI (v5.4 roadmap) | Code change | SaaS, fine-grained RBAC |

### 20.3 RBAC Conceptual Model

| Role | Read | Write | Admin | API | Scope |
|------|------|-------|-------|-----|-------|
| Admin | All | All | Yes | Full | Global |
| Portfolio Lead | All | Own programmes | No | Scoped | Programme |
| Viewer | All | None | No | Read-only | Global |
| API Service | Scoped | Scoped | No | Scoped | Per key |

Stub tables (`users`, `user_roles`) created in schema v5.2 (Section 5). Populated when Tier 3 auth is enabled in v5.4.

### 20.4 API Key Authentication

- Generated on first run via `secrets.token_hex(32)`
- Format: `akb1_sk_{32-char-hex}`
- Stored hashed (SHA-256) in `app_settings`; plaintext shown once
- Used for: programmatic uploads (CI/CD, cron, Power Automate, Zapier)
- Rotatable via Tab 11 (Data Hub & Settings)

### 20.5 Rate Limiting

| Endpoint | Limit | Algorithm |
|----------|-------|-----------|
| GET (read) | 60/min per IP | Leaky bucket (slowapi) |
| POST/PUT (write) | 10/min per IP | Leaky bucket |
| Upload | 5/min per IP | Leaky bucket |
| Health check | Unlimited | — |

Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Exceeds return `429 Too Many Requests`.

### 20.6 Container Hardening (CIS Docker Benchmark v1.6)

| Control | Implementation |
|---------|---------------|
| Non-root user | `USER 1001` (akb1) in Dockerfile |
| Read-only filesystem | `read_only: true` in docker-compose |
| Drop all capabilities | `cap_drop: ALL`, add only `NET_BIND_SERVICE` |
| No privilege escalation | `security_opt: no-new-privileges:true` |
| Temp filesystem | `tmpfs: /tmp:noexec,nosuid,size=64m` |
| Health check | `/health` endpoint, no sensitive data |
| Multi-stage build | Builder + runtime stages (no dev tools in final image) |
| Image scanning | Trivy + Docker Scout in CI |

### 20.7 HTTPS Configuration

- **Caddy (recommended):** Automatic HTTPS via Let's Encrypt (public) or self-signed (localhost/LAN). See `Caddyfile` + `docker-compose.proxy.yml`.
- **Nginx alternative:** Manual TLS cert configuration documented in `SECURITY_GUIDE.md`.
- **Required for:** Tier 1+ (Basic Auth credentials are base64, not encrypted — HTTPS mandatory).

### 20.8 OWASP Top 10 (2021) Compliance Summary

| # | Threat | Mitigation | Status |
|---|--------|-----------|--------|
| A01 | Broken Access Control | Localhost bind, CORS, RBAC, rate limiting | ✅ |
| A02 | Cryptographic Failures | HTTPS (Caddy/Nginx), bcrypt passwords, SHA-256 API keys | ✅ |
| A03 | Injection | Parameterised SQL (SQLAlchemy), Pydantic validation | ✅ |
| A04 | Insecure Design | Threat model documented, rate limiting, upload limits | ✅ |
| A05 | Security Misconfiguration | Hardened containers, no defaults in prod | ✅ |
| A06 | Vulnerable Components | Trivy, pip-audit, npm audit, SBOM | ✅ CI |
| A07 | Auth Failures | 4-tier strategy, session management, cookie security | ✅ |
| A08 | Data Integrity | Import validation, snapshot rollback, Alembic migrations | ✅ |
| A09 | Logging Failures | structlog JSON, audit trail, no PII in logs | ✅ |
| A10 | SSRF | No user-controlled URL fetching, webhook validation | ✅ |

**Full security guide:** [`docs/SECURITY_GUIDE.md`](SECURITY_GUIDE.md) | **Vulnerability disclosure:** [`SECURITY.md`](../SECURITY.md)

---

## DOCUMENT STATUS (v5.2)

| Item | Status | Change History |
|------|--------|---------------|
| Architecture | LOCKED | v5.1: forecast, narrative, scheduler. v5.2: SDLC, multi-currency, security |
| **11-Tab Design** | LOCKED | v5.0: 9 → v5.1: 11 → v5.2: 11 (sub-views 3A/3B/3C added) |
| **44-Table Schema** | LOCKED | v5.0: 30 → v5.1: 37 → v5.2: 42 → 44 (added users, user_roles stubs) |
| **45 Formulas** | LOCKED | v5.0: 37 → v5.1: 40 → v5.2: 45 (currency, Kanban flow, WIP aging) |
| 7 Loss Categories | LOCKED | Unchanged across all versions |
| **58 CTO Questions** | LOCKED | v5.0: 35 → v5.1: 50 → v5.2: 58 (Kanban, Waterfall, multi-currency) |
| **8 Smart Ops** | LOCKED | v5.0: 5 → v5.1: 8. v5.2: webhook alerts added |
| AI Governance | LOCKED | 8 tables, 6-factor trust, 5-level maturity, 5 controls |
| Dual Velocity | LOCKED | 6-gate confidence merge protocol |
| Demo Data | LOCKED | NovaTech Solutions — 5 programmes × 12 months |
| Data Ingestion | LOCKED | Guided wizard, CSV + xlsx, auto-mapping, snapshot rollback |
| Localisation | LOCKED | Multi-currency + fiscal year + number/date format |
| **SDLC Framework** | LOCKED | **NEW v5.2: Scrum/Kanban/Waterfall/SAFe/Hybrid per project** |
| **Security Architecture** | LOCKED | **NEW v5.2: 4-tier auth, RBAC, API keys, container hardening, OWASP** |
| Predictive Analytics | LOCKED | 3 forecast models with confidence bands |
| Narrative Generation | LOCKED | Template-based auto-narratives |
| File Structure | LOCKED | Updated: SECURITY.md, SECURITY_GUIDE.md, Caddyfile, proxy overlays |

**All design elements are LOCKED. Documentation complete. Code build awaiting Adi's explicit go-ahead.**

---

**Adi Kompalli — Architect & Designer | AKB1 v5.2 | Confidential**
