# AKB1 Command Center v5.2 — Early Adopter FAQ & Comprehensive Guide

**Version:** 1.2 | **Date:** 2026-04-16 (v5.2 ultra-think addendum added)
**Author:** Adi Kompalli | AKB1 Framework
**Audience:** Early Adopters, Delivery Directors, Portfolio Heads, CTOs, CIOs, Hiring Managers, Programme Managers
**Purpose:** Everything you need to understand, evaluate, adopt, and derive intelligence from the AKB1 Command Center — including why it exists, what makes it unique, how it compares to the market, and how to get real value from it within 15 minutes.

---

## TABLE OF CONTENTS

1. [What Is the AKB1 Command Center?](#1-what-is-the-akb1-command-center)
2. [Why Does This Exist? The Problem It Solves](#2-why-does-this-exist-the-problem-it-solves)
3. [Market Comparison — How It Differs From Existing Tools](#3-market-comparison--how-it-differs-from-existing-tools)
4. [Unique Advantages — What You Cannot Get Elsewhere](#4-unique-advantages--what-you-cannot-get-elsewhere)
5. [Who Should Use This?](#5-who-should-use-this)
6. [Getting Started — Installation & First Data in 15 Minutes](#6-getting-started--installation--first-data-in-15-minutes)
7. [Data Ingestion — The Most Common Questions](#7-data-ingestion--the-most-common-questions)
8. [Formula Accuracy & Industry Alignment](#8-formula-accuracy--industry-alignment)
9. [Real-World Adoption Scenarios](#9-real-world-adoption-scenarios)
10. [What Intelligence Can You Derive?](#10-what-intelligence-can-you-derive)
11. [Design Rigour — How This Was Made Foolproof](#11-design-rigour--how-this-was-made-foolproof)
12. [Known Limitations & Honest Trade-offs](#12-known-limitations--honest-trade-offs)
13. [Architecture & Build Instructions](#13-architecture--build-instructions)
14. [Complete Question Inventory — 58 CTO/CIO/CEO Questions Answered](#14-complete-question-inventory--58-ctocioceo-questions-answered)
15. [For Hiring Managers — What This Demonstrates About the Builder](#15-for-hiring-managers--what-this-demonstrates-about-the-builder)
16. [v5.2 ADDENDUM — SDLC compatibility, Multi-Currency, Windows, xlsx, Wireframes, Tech Stack, Production SDLC](#16-v52-addendum)

---

## 1. WHAT IS THE AKB1 COMMAND CENTER?

**One-line answer:** A plug-and-play, Docker-containerized delivery intelligence dashboard that gives you complete portfolio visibility — financials, risk, AI governance, customer satisfaction, audit readiness — in a single browser tab.

**The longer version:**

AKB1 Command Center v5.2 is an open-source application designed for IT services delivery leaders who manage multi-programme portfolios. You clone the repository, run `docker-compose up`, and within 15 minutes you have a fully functional delivery intelligence platform showing:

- Portfolio health across all your programmes and projects
- Four-layer margin analysis (Gross → Contribution → Portfolio → Net)
- Seven categories of delivery losses with financial quantification
- AI governance with a 6-factor trust score and maturity model
- Dual velocity tracking (standard teams vs. AI-augmented teams)
- Customer satisfaction, expectation gaps, and renewal probability
- Predictive analytics — what will happen in the next 3 months
- Auto-generated narratives — the "so what?" for every data point
- 58 CTO/CIO/CEO questions answered directly by dashboard data
- Audit-ready governance trail for compliance reviews

**Tech Stack:** FastAPI (Python) + React 18 + SQLite + Docker Compose
**Port:** 9000 (dashboard) / 9001 (API with auto-generated Swagger docs)
**License:** MIT — completely free, fork it, modify it, use it commercially
**Data:** Ships with realistic demo data for 5 programmes × 12 months, or bring your own via CSV upload or guided wizard

---

## 2. WHY DOES THIS EXIST? THE PROBLEM IT SOLVES

### The Reality Every Delivery Director Faces

You manage 4-8 programmes, 80-300 people, ₹20M-₹100M in revenue. Your Monday morning looks like this:

- Your CFO asks: "Why is margin down 2 points this quarter?"
- Your CTO asks: "Are the AI tools actually helping or just adding overhead?"
- Your client asks: "Will you deliver on time? My CSAT score says you're slipping."
- Your auditor asks: "Can you prove that AI-generated code was reviewed before production?"
- Your HR asks: "Why did we lose 3 people this quarter and what did it cost?"

You have data scattered across 6-8 tools: Jira for sprints, ServiceNow for incidents, Excel for financials, Power BI for utilisation, a Confluence wiki for risks, and email threads for customer feedback. No single view answers any of these questions without 4 hours of manual data aggregation.

### What the Market Currently Offers (And Why It Falls Short)

| Problem | Current Market Response | Why It's Insufficient |
|---------|----------------------|----------------------|
| Portfolio visibility | Jira Portfolio, Azure DevOps Plans, Planview | Delivery execution only — no financials, no AI governance, no customer intelligence |
| Financial tracking | SAP, Oracle Financials, QuickBooks | ERP-grade financial systems — no delivery context, no sprint-level margin, no loss categories |
| AI governance | No established tool exists | Most organisations track AI adoption in spreadsheets or not at all |
| Delivery P&L | Custom Excel models | Brittle, not shareable, no automation, person-dependent |
| Customer satisfaction | SurveyMonkey, Qualtrics | Survey tools — not integrated with delivery health or renewal prediction |
| Delivery dashboard | Power BI / Tableau / Looker | BI tools show data. They don't compute formulas, detect losses, generate narratives, or run proactive scenarios |

The AKB1 Command Center exists because **no single tool in the market combines delivery execution + financial intelligence + AI governance + customer intelligence + predictive analytics + audit readiness in one deployable application.**

---

## 3. MARKET COMPARISON — HOW IT DIFFERS FROM EXISTING TOOLS

### 3.1 Feature-by-Feature Comparison

| Capability | Jira Portfolio / Azure DevOps | Planview / Clarity | Power BI / Tableau | ServiceNow ITOM | Custom Excel | **AKB1 Command Center** |
|------------|------------------------------|-------------------|-------------------|-----------------|-------------|------------------------|
| Sprint velocity tracking | Yes | Partial | Via connector | No | Manual | **Yes — with dual AI/standard tracking** |
| Earned Value Management (CPI/SPI/EAC) | Plugin required | Yes | Via model | No | Manual | **Yes — with 3-month forecast** |
| 4-layer margin analysis | No | Partial (2 layers) | Via model | No | Manual | **Yes — Gross/Contribution/Portfolio/Net** |
| 7 delivery loss categories | No | No | No | No | Manual | **Yes — auto-detected with financial impact** |
| AI governance & trust score | No | No | No | No | No | **Yes — 6-factor composite, 5-level maturity** |
| AI vs Traditional team comparison | No | No | No | No | No | **Yes — 12-dimension framework** |
| Customer satisfaction + renewal prediction | No | No | Via model | Partial (CSAT only) | Manual | **Yes — 7-dimension expectation gap + renewal probability** |
| Predictive analytics (3-month forecasts) | No | Partial | Via model | No | No | **Yes — 3 forecast models built-in** |
| Auto-generated narratives | No | No | No | No | No | **Yes — template-based "so what?" for every metric** |
| Audit & compliance trail | No | Partial | No | Yes | No | **Yes — AI audit trail, data lineage, export audit package** |
| Proactive problem detection (Smart Ops) | No | No | Via alerts | Yes (event-driven) | No | **Yes — 8 proactive scenarios, 15-min background scan** |
| Utilisation waterfall (3-system) | No | No | No | No | Rare | **Yes — HRIS/RM/Billing with gap breakdown** |
| Single docker-compose deployment | No (SaaS) | No (Enterprise) | No (SaaS) | No (Enterprise) | N/A | **Yes — clone, up, done** |
| Open source (MIT) | No | No | No | No | N/A | **Yes — fork, modify, contribute** |
| Cost | $10-50/user/month | $50K-500K/year | $10-70/user/month | $100K+/year | Free but manual | **Free — MIT license** |
| Time to first dashboard | Days-weeks | Months | Days-weeks | Months | Hours | **15 minutes** |

### 3.2 Why Existing Tools Don't Solve the Delivery Director's Problem

**Jira / Azure DevOps:**
These are execution tools. They track stories, sprints, and bugs. They do not know what your margin is, what bench is costing you, whether your AI tools are trustworthy, or whether your customer will renew. A delivery director needs execution data AND commercial intelligence AND governance AND customer intelligence in one view. Jira gives you one of these.

**Planview / Clarity / PPM Tools:**
Enterprise PPM tools are powerful but require 3-6 month implementation, dedicated administrators, and $50K-$500K annual licensing. They excel at portfolio planning but lack AI governance, delivery loss detection, and predictive narratives. They are built for PMO offices of 50+ people, not for a single portfolio owner managing 5 programmes.

**Power BI / Tableau / Looker:**
BI tools are visualisation engines. They show data beautifully. But they don't compute CPI from EVM inputs. They don't detect margin leakage across 7 categories. They don't generate a narrative that says "Phoenix is spending ₹1.23 for every ₹1 of value — recovery is improbable without scope reduction." They don't run 8 proactive detection scenarios every 15 minutes. You would need to build all of this logic yourself — which is exactly what the AKB1 Command Center has done.

**ServiceNow ITOM:**
Excellent for incident management and ITSM. But it operates at the infrastructure layer, not the delivery P&L layer. It doesn't know your programme margin, your sprint velocity, or your AI trust score.

**Custom Excel Models:**
This is what 80% of delivery directors actually use. And it works — until you need to share it, automate it, audit it, or hand it to your successor. Excel models are person-dependent, non-auditable, and break when the creator leaves. The AKB1 Command Center codifies the same logic into a deployable, shareable, version-controlled application.

### 3.3 The Positioning

AKB1 Command Center is not competing with Jira or SAP. It sits in a gap that no existing tool covers:

```
Execution Tools (Jira, ADO) ← Sprint data feeds in
                                    ↓
              ┌─────────────────────────────────────┐
              │     AKB1 Command Center             │
              │     The Delivery Intelligence Layer  │
              │                                     │
              │  Financial + Delivery + AI + Customer│
              │  + Risk + Audit + Predictive         │
              └─────────────────────────────────────┘
                                    ↓
Finance Tools (SAP, Oracle) ← Financial context feeds in
HR Tools (HRIS) ← Utilisation data feeds in
Customer Tools (Surveys) ← CSAT/NPS data feeds in
```

It is the **missing middle layer** between your execution tools and your ERP — the layer where a delivery director actually lives.

---

## 4. UNIQUE ADVANTAGES — WHAT YOU CANNOT GET ELSEWHERE

### 4.1 Seven Things Only AKB1 Command Center Does

**1. Seven Delivery Loss Categories with Financial Quantification**

No tool in the market categorises delivery losses into 7 explicit categories (Bench Tax, Scope Creep, AI Productivity Tax, Sprint Leakage, SLA Penalty Exposure, Attrition Knowledge Loss, Pyramid Inversion) and then quantifies each in currency terms. Most organisations discover these losses in post-mortems. The Command Center detects them in real-time.

- **Bench Tax Example:** Your programme has 28 people on the roster but only 25 are billable. The 3 bench resources cost ₹260/day each. Shadow allocation = 3 × ₹260 × 22 days × 65% allocation = ₹11,154/month charged to the programme. Over a quarter, that is ₹33,462 — invisible in most tools but visible in the Command Center's loss waterfall.

- **AI Productivity Tax Example:** Your AI-augmented team generates 22% more code but 15% of it requires rework. The rework costs 12 developer-hours per sprint at ₹2,500/hour = ₹30,000/sprint. Plus governance overhead of 8 hours/sprint = ₹20,000. Total AI Productivity Tax = ₹50,000/sprint. The Command Center computes this automatically from sprint data + AI code metrics.

**2. AI Governance with 6-Factor Trust Score and 5-Level Maturity Model**

There is no commercial tool that provides a structured AI governance framework for delivery teams. The Command Center computes an AI Trust Score from 6 measurable factors (Provenance, Review Status, Test Coverage, Drift Check, Human Override Rate, Production Defect Rate) with explicit weights and thresholds. It also maps your team to a 5-level AI Governance Maturity Model (Unaware → Ad-Hoc → Managed → Governed → Optimized).

This is not theoretical governance. Every factor has a data source, a formula, a threshold, and an alert. When your trust score drops 10 points in 2 sprints, the Smart Ops engine fires a governance drift alert.

**3. AI vs. Traditional Team Comparison (12 Dimensions)**

The question every CTO asks in 2025-2026: "Are the AI tools actually helping?" Most organisations answer this with anecdotes. The Command Center answers with a 12-dimension quantitative comparison: raw velocity, quality-adjusted velocity, defect density, test coverage, code review rejection rate, estimation accuracy, rework percentage, cost per story point, time to market, governance overhead, trust score, and net productivity gain.

The honest answer template built into the dashboard says: "AI-augmented teams on Sentinel are delivering 22% higher raw velocity but 14% higher quality-adjusted velocity after rework deduction. Governance overhead adds 8 hours/sprint (3% of capacity). Net productivity gain is 11%. Cost per story point is 9% lower. However, defect density is 1.15x human baseline — within acceptable range but not yet at parity."

No dashboard in the market produces this level of comparative analysis.

**4. Dual Velocity Tracking with 6-Gate Merge Protocol**

Traditional velocity and AI-augmented velocity are tracked separately. They only merge into a single planning velocity after passing 6 quality gates:

1. Defect density parity (AI ≤ 1.2x human baseline)
2. Test coverage parity (AI ≥ 95% of human baseline)
3. Review rejection rate below 15%
4. 8+ sprints of stable data
5. Human override rate between 10-30% (healthy range)
6. AI Trust Score ≥ 75

Until all 6 gates pass, the dashboard shows both velocities separately and explicitly warns against using AI velocity for planning. This prevents the common mistake of inflating velocity estimates with unvalidated AI output.

**5. Three-System Utilisation Waterfall**

Most organisations report a single utilisation number. But there are actually three utilisation systems, each owned by a different function:

| System | Owner | Typical Value | What It Measures |
|--------|-------|--------------|------------------|
| HRIS Utilisation | HR | ~82% | Capacity (headcount × available hours) |
| RM Utilisation | Delivery | ~78% | Assignment (who is allocated where) |
| Billing Utilisation | Finance | ~71% | Revenue (who is actually billing) |

The 11-point gap between HRIS (82%) and Billing (71%) is where margin erodes. The Command Center breaks this gap into 5 categories: leave/holidays, bench/rotation, rework/quality, meetings/admin, and transition/churn. No commercial tool provides this waterfall.

**6. Predictive Analytics with Confidence Bands**

Every trend chart in the dashboard shows a solid line (historical actuals) and a dashed line (3-month forecast) with a shaded confidence band. The forecast uses 3 models (linear regression, weighted moving average, exponential smoothing) selected automatically based on data characteristics.

When CPI is projected to drop below 0.85 in 2 months, the dashboard doesn't just show the trend — it triggers a CPI Trajectory Alert in the Smart Ops engine and generates a narrative: "At current trajectory, Phoenix CPI will reach 0.79 by Q3-end. TCPI of 1.31 indicates budget recovery is improbable. Recommend scope reduction or sponsor escalation."

**7. Auto-Generated Narratives (The "So What?" Layer)**

Data without interpretation is just noise. The Command Center generates template-based narratives for every major metric: CPI, margin, portfolio summary, customer satisfaction, and QBR briefs. These are not AI-generated hallucinations — they are deterministic templates that produce factually accurate summaries from the data.

Example: "Portfolio of 5 programmes tracking at 18.5% net margin (1.5 points below plan). 1 programme at Red status. Top concern: Phoenix (CPI 0.81, scope creep absorbing ₹450K). Recommend steering committee review for Phoenix."

A delivery director can copy-paste this into a steering committee slide deck.

### 4.2 Advantages for Different Stakeholders

| Stakeholder | What They Get | Time Saved |
|-------------|---------------|------------|
| **Delivery Director** | Single-screen portfolio health, proactive alerts, auto-narratives, QBR prep in 5 minutes instead of 4 hours | 4-6 hours/week |
| **Portfolio Head** | Cross-programme comparison, margin waterfall, loss detection, resource rebalancing recommendations | 3-5 hours/week |
| **CTO/CIO** | AI governance visibility, AI vs. traditional comparison, technology risk posture, forecast accuracy | 2-3 hours/week on data gathering |
| **CFO** | 4-layer margin, bench cost allocation, revenue leakage, rate card drift, financial forecasts | 3-4 hours/month on QBR prep |
| **Programme Manager** | EVM dashboard, sprint health, milestone tracking, customer satisfaction, change request economics | 2-3 hours/week |
| **Auditor** | Governance control dashboard, AI audit trail, data lineage, exportable audit package | Hours → minutes for evidence gathering |
| **HR / Resource Manager** | Utilisation waterfall, bench tracking, attrition cost analysis | 1-2 hours/week |

### 4.3 Why It's Free (And Why That's a Feature, Not a Bug)

This is not a product company. This is a delivery intelligence framework built by a practitioner with ~20 years of enterprise delivery experience. It is open-source (MIT) because:

1. **Portfolio intelligence should not be locked behind $50K licensing.** A delivery manager at a 200-person unit in Hyderabad should have the same visibility as a VP at Accenture.
2. **The framework codifies real operating models, not theoretical consulting frameworks.** Every formula, every threshold, every loss category comes from actual portfolio governance experience.
3. **Open-source means you can fork, customise, and extend it.** Add your company's specific KPIs, modify thresholds for your industry, integrate with your existing tools via the REST API.

---

## 5. WHO SHOULD USE THIS?

### 5.1 Primary Users

| Role | Use Case | Minimum Data Needed |
|------|----------|-------------------|
| Delivery Director managing 3-8 programmes | Full portfolio intelligence | programmes + KPI monthly |
| Programme Manager managing 1-3 programmes | Programme-level health + EVM + customer | programmes + sprints + KPI monthly |
| Portfolio Head / Account Lead | Cross-programme comparison + financials | programmes + financials + KPI monthly |
| CTO/CIO evaluating delivery health | Executive overview + AI governance + forecasts | programmes + KPI monthly + AI metrics |

### 5.2 Organisation Profiles That Get Maximum Value

| Organisation Type | Team Size | Why AKB1 Fits |
|-------------------|-----------|---------------|
| Indian IT Services (TCS, Infosys, Wipro, HCL, Tech Mahindra, smaller firms) | 50-500 people per delivery unit | Built for this context — INR, offshore ratios, pyramid economics, bench management |
| US/European Consulting firms | 20-200 people per practice | Multi-currency support, adjustable thresholds, industry presets |
| Enterprise IT departments with outsourced delivery | Managing 3-10 vendor programmes | Portfolio-level aggregation, vendor comparison, SLA tracking |
| Startups with delivery teams scaling past 50 people | 50-150 people | Prevents the "spreadsheet chaos" phase, codifies governance early |

### 5.3 Who Should NOT Use This (Honest Assessment)

- **Single-project teams (< 15 people):** Overkill. Use Jira + a spreadsheet.
- **Product companies (building their own product):** This is for IT services delivery, not product development. Product teams need different metrics (activation, retention, churn) — not EVM and bench tracking.
- **Non-technical managers who cannot run Docker:** The application requires Docker Desktop and basic terminal familiarity. If `docker-compose up` is unfamiliar, you'll need a technical colleague to set it up.
- **Organisations that need multi-user access control:** v5.0 is single-user (no authentication). Multi-user support is on the roadmap but not built yet.

---

## 6. GETTING STARTED — INSTALLATION & FIRST DATA IN 15 MINUTES

### 6.1 Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Docker Desktop | v20.10+ | Latest |
| Docker Compose | v2.0+ | Latest (bundled with Docker Desktop) |
| RAM | 2 GB free | 4 GB free |
| Disk | 500 MB | 1 GB |
| OS | macOS 12+, Windows 10+, Ubuntu 20.04+ | macOS or Linux |
| Browser | Chrome, Safari, or Firefox (latest 2 versions) | Chrome |

### 6.2 Installation (3 Commands)

```bash
# Step 1: Clone the repository
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center

# Step 2: Run setup (creates .env, builds images, starts services)
./scripts/setup.sh

# Step 3: Open your browser
open http://localhost:9000
```

That's it. The setup script checks Docker, creates your environment file, builds both containers (backend + frontend), starts the services, and waits for the health check. Demo data is pre-loaded automatically.

### 6.3 First 15 Minutes — What to Do

| Minute | Action | What You See |
|--------|--------|-------------|
| 0-2 | Run setup.sh | Docker images build (first time takes 2-3 minutes) |
| 2-3 | Open http://localhost:9000 | Executive Overview with demo data (5 programmes, 12 months) |
| 3-5 | Explore Tab 1 (Executive Overview) | Portfolio health, DHI scores, top risks, auto-narrative |
| 5-7 | Click Tab 8 (Commercials) | Margin waterfall, loss categories, utilisation waterfall |
| 7-10 | Click Tab 6 (AI Governance) | Trust scores, AI vs Traditional comparison, maturity model |
| 10-12 | Go to Tab 9 (Settings) | Start the guided wizard — set your currency, industry, org name |
| 12-15 | Upload your first CSV | programmes.csv with your real programme names, BAC, revenue, team size |

After 15 minutes, you have either explored the demo or started seeing your own data.

### 6.4 Minimum Viable Data — What You Need to See a Real Dashboard

The application renders meaningful dashboards with just **2 CSV files:**

1. **programmes.csv** — columns: name, code, start_date, bac, revenue, team_size
2. **kpi_monthly.csv** — columns: program_code, snapshot_date, cpi, utilization, margin_pct

Everything else gracefully degrades. If you haven't uploaded risk data, the Risk tab shows "No data yet — upload risks.csv to see this section." No errors, no broken charts — just clear prompts telling you what to add next.

### 6.5 Stopping and Restarting

```bash
# Stop the application (data is preserved)
docker-compose down

# Restart (data is still there — SQLite persists in Docker volume)
docker-compose up -d

# Reset to demo data (WARNING: deletes your data)
./scripts/seed.sh

# Export your data
./scripts/export-db.sh
```

### 6.6 Troubleshooting — First-Time Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Port 9000 already in use | Another app on port 9000 | Edit `.env`: change `FRONTEND_PORT=9000` to `FRONTEND_PORT=9002` |
| Docker build fails | Docker not running | Start Docker Desktop first |
| Backend health check fails | Port 9001 conflict | Edit `.env`: change `BACKEND_PORT=9001` to `BACKEND_PORT=9003` |
| CSV upload fails | Wrong column names | Check required columns against the CSV template files in `docs/csv-templates/` |
| No data showing after CSV upload | Snapshot dates don't match | Ensure your `snapshot_date` values are in YYYY-MM-DD format |
| Charts show "No data" after upload | Programme codes don't match | Ensure `program_code` in your KPI CSV matches the `code` in your programmes CSV exactly |

---

## 7. DATA INGESTION — THE MOST COMMON QUESTIONS

This is the #1 area where early adopters have questions. Data ingestion covers: where your data comes from, how to get it into the Command Center, what format it needs, and how to handle the fact that your data lives in 6-8 different tools.

### 7.1 FAQ: Data Sources

**Q: My data is in Jira. How do I get it into the Command Center?**

Export from Jira → CSV → upload to Command Center. Specifically:
1. In Jira, go to your board → Reports → Sprint Report → Export to CSV
2. Map columns: `Sprint Name` → sprint_number, `Story Points Committed` → planned_points, `Story Points Completed` → completed_points, `Bugs Created` → defects_found
3. Save the column mapping — it will auto-apply for future uploads

For automated ingestion: use the Jira REST API to pull sprint data via a scheduled script (cron job) and POST to `/api/v1/import/csv`. Example scripts are in `docs/DATA_INGESTION.md`.

**Q: My data is in Azure DevOps. How do I get it into the Command Center?**

Azure DevOps has built-in Analytics views. Export sprint data to CSV:
1. Go to Analytics → Boards → Sprint Burndown → Export
2. Map columns using the CSV auto-mapper in Tab 9

Alternatively, use the Azure DevOps REST API: `GET https://dev.azure.com/{org}/{project}/_apis/work/teamsettings/iterations` to pull sprint data programmatically.

**Q: My financial data is in SAP/Oracle/Tally.**

The Command Center needs 4 financial data points per programme per month: planned_revenue, actual_revenue, planned_cost, actual_cost. Export these from your ERP as a CSV and upload to the `financials.csv` template. You do not need to connect SAP directly — the Command Center consumes summarised financial data, not transactional ERP data.

**Q: My utilisation data comes from 3 different systems (HRIS, RM tool, Timesheet).**

This is exactly what the utilisation waterfall is designed for. Upload `utilization_detail.csv` with columns: program_code, snapshot_date, hris_utilization, rm_utilization, billing_utilization. The gap breakdown (leave, bench, rework, meetings, transition) can be added optionally — if not provided, the system calculates the total gap and labels it "unclassified."

**Q: My customer satisfaction data is in SurveyMonkey/Qualtrics.**

Export survey results as CSV. Map the overall satisfaction score to `csat_score` (1-10 scale). Map NPS question to `nps_score` (-100 to +100). Upload via the `customer_satisfaction` template. Open-text themes can be entered manually in Tab 10 as "positive_themes" and "concern_themes."

**Q: I use ServiceNow for incident management.**

Export incident data filtered by your programme/project. Map fields: `Number` → incident_id, `Priority` → priority (P1/P2/P3/P4), `Opened` → reported_at, `Response Time` → responded_at, `Resolved` → resolved_at. Upload via the `sla_incidents` template. The dashboard will compute response times, resolution times, and SLA breach flags automatically.

**Q: My AI tool usage data doesn't exist in any tool.**

This is common. Most organisations in 2025-2026 don't have structured AI usage tracking. Start with manual entry:
1. Go to Tab 6 → AI Tool Registry → Add Tool (name, vendor, category, cost per seat)
2. Each sprint, enter: prompts count, suggestions accepted/rejected, time saved estimate
3. Over 3-4 sprints, you'll have enough data for the trust score and comparison panel

The Command Center is designed to bootstrap from zero AI data and build the tracking infrastructure organically.

**Q: I want to connect my tools directly (API integration) instead of CSV uploads.**

The Command Center exposes a full REST API at `http://localhost:9001/docs` (Swagger). You can POST data directly:

```bash
# Example: Create a programme
curl -X POST http://localhost:9001/api/v1/programs \
  -H "Content-Type: application/json" \
  -d '{"name": "Phoenix", "code": "PHX", "bac": 6800000, "revenue": 10000000, "team_size": 25}'

# Example: Post a KPI snapshot
curl -X POST http://localhost:9001/api/v1/kpis/snapshots \
  -H "Content-Type: application/json" \
  -d '{"program_id": 1, "kpi_id": 7, "snapshot_date": "2026-03-01", "value": 0.81}'
```

Any tool that can make HTTP requests can integrate: Python scripts, Power Automate flows, Zapier, n8n, cron jobs, CI/CD pipelines.

### 7.2 FAQ: CSV Templates

**Q: What CSV templates are provided?**

13 templates, each with headers and 2-3 sample rows:

| # | Template | Required Columns | Maps To |
|---|----------|-----------------|---------|
| 1 | programmes.csv | name, code, start_date, bac, revenue, team_size | programs table |
| 2 | projects.csv | program_code, name, code, start_date, bac, team_size, is_ai_augmented | projects table |
| 3 | kpi_monthly.csv | program_code, snapshot_date, kpi_code, value | kpi_snapshots table |
| 4 | evm_monthly.csv | program_code, snapshot_date, planned_value, earned_value, actual_cost | evm_snapshots table |
| 5 | risks.csv | program_code, title, probability, impact, severity, status, owner | risks table |
| 6 | sprints.csv | program_code, sprint_number, planned_points, completed_points, defects_found, ai_assisted_points | sprint_data table |
| 7 | financials.csv | program_code, snapshot_date, planned_revenue, actual_revenue, planned_cost, actual_cost | commercial_scenarios table |
| 8 | ai_tools.csv | name, vendor, category, cost_per_seat | ai_tools table |
| 9 | ai_metrics.csv | program_code, sprint_number, ai_lines_generated, ai_defect_count, ai_test_coverage_pct | ai_code_metrics table |
| 10 | resources.csv | name, role, role_tier, current_program_code, utilization_pct, bench_days | resource_pool table |
| 11 | bench.csv | program_code, snapshot_date, planned_headcount, actual_headcount, bench_headcount | bench_tracking table |
| 12 | change_requests.csv | program_code, cr_date, cr_description, effort_hours, cr_value, is_billable | scope_creep_log table |
| 13 | losses.csv | program_code, snapshot_date, loss_category, amount | loss_exposure table |

**Q: My CSV columns don't match the template names.**

The CSV Auto-Mapper handles this. When you upload a CSV:
1. The app reads your column headers
2. It suggests matches with confidence scores (e.g., "Budget" → `bac` at 82% confidence)
3. You confirm or adjust the mapping
4. The mapping is saved as a template for future uploads of the same format

**Q: What if I only have partial data?**

Start with what you have. The minimum viable dataset is:
- **programmes.csv** (name, code, BAC, revenue, team size)
- **kpi_monthly.csv** (CPI, utilisation, margin for each programme)

Every other section gracefully degrades with a clear message: "No data yet — upload [template name] to see this section."

### 7.3 FAQ: Data Refresh & Freshness

**Q: How often should I update the data?**

| Data Type | Recommended Cadence | Why |
|-----------|-------------------|-----|
| Sprint data | End of each sprint (bi-weekly) | Velocity, defects, rework are sprint-scoped |
| KPI snapshots | Monthly | Most KPIs are month-end measurements |
| EVM snapshots | Monthly | Aligns with financial reporting cycles |
| Financial data | Monthly | Revenue and cost are monthly |
| Risk register | Weekly | Risks change frequently |
| Customer satisfaction | Monthly or after each survey | CSAT and NPS are periodic |
| AI metrics | Per sprint | Aligns with sprint cadence |
| Resource/bench data | Monthly | Aligns with HR/RM reporting |

**Q: Does the dashboard auto-refresh?**

The dashboard polls the backend API every 60 seconds for new data. If you upload a CSV or POST via the API, the charts update within 60 seconds without manual refresh.

**Q: What happens if I upload the same data twice?**

The import system checks for duplicates based on (program_id + snapshot_date + kpi_id) for KPI snapshots and (program_id + snapshot_date) for EVM/financial data. Duplicates are rejected with a clear error message. If you need to update existing data, use the PUT API endpoints.

### 7.4 FAQ: Data Migration from Existing Systems

**Q: I have 2 years of historical data in Excel. Can I load it all at once?**

Yes. Prepare your Excel data as CSV (one file per template), ensure dates are in YYYY-MM-DD format, and upload via Tab 9. The system handles bulk imports — tested with 5 programmes × 24 months × 13 KPIs = 1,560 data points in a single upload. Performance: < 5 seconds.

**Q: Can I import data from multiple sources into the same programme?**

Yes. The system uses `program_code` as the join key. You can upload sprint data from Jira (sprint.csv), financial data from SAP (financials.csv), and risk data from a Confluence export (risks.csv) — as long as the `program_code` matches, data aggregates correctly.

**Q: What if my programme codes are different across systems?**

Use the programme code you define in the Command Center as the canonical identifier. When preparing CSVs from different source systems, map their identifiers to your Command Center programme codes. The auto-mapper does not resolve this — you need to standardise codes before upload.

---

## 8. FORMULA ACCURACY & INDUSTRY ALIGNMENT

### 8.1 Formula Design Principles

Every formula in the Command Center follows 4 rules:

1. **Traceable:** Every input variable maps to a specific database column. Click any metric → see its calculation chain (Tab 11 data lineage).
2. **Industry-standard where applicable:** CPI, SPI, EAC, TCPI, VAC use standard Earned Value Management formulas (per PMI PMBOK 7th Edition). Utilisation formulas follow PMI/Gartner benchmarks.
3. **Worked examples for every formula:** Not just the formula — but 2 complete worked examples with real numbers, step-by-step calculation, and interpretation. See FORMULAS.md for the full reference.
4. **Editable thresholds:** Every threshold (Green/Amber/Red) is a default loaded from the industry preset. You can adjust to match your organisation's standards in Tab 9.

### 8.2 Complete Formula Inventory (40 Formulas)

Organised by category with industry alignment:

**ESTIMATION (6 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 1 | Budget At Completion (BAC) | Master budget agreement amount | PMI PMBOK EVM | Direct from programmes.bac |
| 2 | Blended Cost Per Hour | Σ(HC × Rate × 1.35) / Total Billable Hours | Industry standard with 35% overhead loading | commercial_scenarios + resource_pool |
| 3 | Loaded Cost Per Resource | Base Rate × 1.35 × Hours/Month | Standard for T&M engagements | resource_pool.loaded_cost_annual / 12 |
| 4 | PERT Estimate | (Optimistic + 4×Most Likely + Pessimistic) / 6 | PMI PMBOK — PERT weighted average | Sprint estimation calculator in Tab 3 |
| 5 | Contingency Reserve | BAC × Risk Factor (typically 5-15%) | PMI recommended 10% for medium-risk | Configurable per programme |
| 6 | Estimate At Completion (EAC) | BAC / CPI | PMI PMBOK EVM | evm_snapshots.eac (auto-computed) |

**EARNED VALUE MANAGEMENT (6 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 7 | Cost Performance Index (CPI) | EV / AC | PMI PMBOK — ratio of value earned to cost spent | evm_snapshots.cpi |
| 8 | Schedule Performance Index (SPI) | EV / PV | PMI PMBOK — ratio of value earned to value planned | evm_snapshots.spi |
| 9 | Estimate To Complete (ETC) | EAC - AC | PMI PMBOK | Computed in Tab 3 EVM panel |
| 10 | To-Complete Performance Index (TCPI) | (BAC - EV) / (BAC - AC) | PMI PMBOK — efficiency needed to finish on budget | evm_snapshots.tcpi |
| 11 | Variance At Completion (VAC) | BAC - EAC | PMI PMBOK — projected budget overrun/underrun | evm_snapshots.vac |
| 12 | Percent Complete | EV / BAC × 100 | PMI PMBOK | evm_snapshots.percent_complete |

**FINANCIAL (8 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 13 | Gross Margin % | (Revenue - Effort Cost) / Revenue × 100 | Standard P&L | commercial_scenarios.gross_margin_pct |
| 14 | Contribution Margin % | (Gross Margin - Direct Overhead) / Revenue × 100 | Management accounting standard | commercial_scenarios.contribution_margin_pct |
| 15 | Portfolio Margin % | (Contribution Margin - Shared Overhead) / Revenue × 100 | IT Services specific — Infosys, TCS, Wipro use this layered approach | commercial_scenarios.portfolio_margin_pct |
| 16 | Net Programme Margin % | (Portfolio Margin - Bench Allocation) / Revenue × 100 | AKB1 proprietary — includes shadow bench cost | commercial_scenarios.net_margin_pct |
| 17 | Shadow Bench Allocation | (Actual HC - Planned HC) × Loaded Cost × Alloc% | AKB1 proprietary | bench_tracking.shadow_allocation_cost |
| 18 | CR Processing Cost | Σ(CR Effort × Loaded Cost) where CR is non-billable | Change management economics | scope_creep_log.processing_cost |
| 19 | Revenue Realisation % | Invoiced Revenue / Planned Revenue × 100 | Standard for T&M and FP contracts | kpi_snapshots where kpi_code = 'REV_REAL' |
| 20 | Rate Card Drift % | (Actual Blended Rate - Planned Blended Rate) / Planned × 100 | Pyramid economics in IT Services (TCS, Infosys standard) | rate_cards (planned_rate vs actual_rate) |

**DELIVERY HEALTH (5 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 21 | Schedule Adherence | (On-Time Milestones / Total Milestones) × 100 | PMI standard | milestones table aggregation |
| 22 | Scope Stability Index | 1 - (Approved Changes / Original Requirements) | Change management metric (Gartner) | scope_creep_log aggregation |
| 23 | Resource Utilisation (True Billable) | Billable Hours / Total Available Hours × 100 | Industry standard — Gartner benchmarks 65-78% | kpi_snapshots or utilization_detail.billing_utilization |
| 24 | Quality Index | Weighted(Defect Density, Test Coverage, Rework%) | AKB1 composite — inspired by CMMi quality frameworks | Computed from sprint_data |
| 25 | Delivery Health Index (DHI) | Weighted composite of 13 core KPIs | AKB1 proprietary composite | Computed from kpi_definitions weights × kpi_snapshots values |

**SPRINT & VELOCITY (5 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 26 | Sprint Velocity | Completed Story Points / Sprint | Agile standard (SAFe, Scrum) | sprint_data.velocity |
| 27 | Sprint Leakage % | (Planned Points - Completed Points) / Planned × 100 | Agile metric — target < 20% | Computed from sprint_data |
| 28 | Defect Density | Defects Found / Story Points Completed | Quality metric per sprint | sprint_data.defects_found / sprint_data.completed_points |
| 29 | Rework % | Rework Hours / Total Sprint Hours × 100 | Quality metric (target < 15%) | sprint_data.rework_hours / (sprint_data.team_size × 80) |
| 30 | AI Quality-Adjusted Velocity | AI Velocity - (AI Rework Points × Rework Factor) | AKB1 proprietary — prevents velocity inflation | sprint_velocity_dual.ai_quality_adjusted_velocity |

**AI GOVERNANCE (4 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 31 | AI Trust Score | Weighted(Provenance 0.20, Review 0.25, Tests 0.20, Drift 0.15, Override 0.10, Defects 0.10) | AKB1 proprietary — no market standard exists | ai_trust_scores.composite_score |
| 32 | AI Governance Maturity | 5-level model (0-100 scoring) | Inspired by CMMi maturity levels, adapted for AI context | ai_trust_scores.maturity_level |
| 33 | AI Override Rate | (Overrides / Total AI Suggestions) × 100 | AKB1 proprietary — healthy range 10-30% | ai_override_log aggregation |
| 34 | Net AI Productivity Gain | (AI Velocity - Governance Overhead) / Baseline Velocity × 100 | AKB1 proprietary | sprint_velocity_dual + ai_sdlc_metrics |

**LOSS DETECTION (3 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 35 | Attrition Knowledge Loss Cost | Hiring Cost + Ramp-Up Cost + Productivity Gap Cost | HR industry standard (SHRM benchmarks ₹300K+ per departure) | loss_exposure + resource_pool |
| 36 | SLA Penalty Exposure | Breach Count × Penalty Rate × Monthly Bill | Contractual penalty clause standard | sla_incidents + commercial_scenarios |
| 37 | Scope Creep Absorption | Σ(Unbilled CR Effort × Blended Cost) | Change management economics | scope_creep_log where is_billable = false |

**NEW IN v5.1 (3 Formulas)**

| # | Formula | Calculation | Industry Standard | AKB1 Implementation |
|---|---------|------------|-------------------|---------------------|
| 38 | Renewal Probability | Weighted(CSAT 0.30, DHI 0.25, Escalation 0.20, Communication 0.15, Innovation 0.10) | AKB1 proprietary — inspired by account health scoring used at TCS, Infosys | customer_satisfaction.renewal_score |
| 39 | AI Cost-Benefit Ratio | (Time Saved × Blended Rate) / (AI Tool Cost + Rework Cost) | AKB1 proprietary — no market standard | Computed from ai_usage_metrics + ai_code_metrics + commercial_scenarios |
| 40 | Forecast Confidence | R² of linear regression on last 6-12 data points | Statistical standard (R-squared goodness of fit) | kpi_forecasts.confidence_pct |

### 8.3 Formula Validation — How We Ensured Accuracy

Every formula was validated through 3 checks:

1. **PMI/PMBOK alignment:** All EVM formulas (CPI, SPI, EAC, ETC, TCPI, VAC) match PMBOK 7th Edition definitions exactly. These are not approximations.

2. **Worked example verification:** Each formula has 2 worked examples in FORMULAS.md with real numbers. Example for CPI:
   - Example 1 — Phoenix Programme: BAC ₹6.8M, PV ₹4.08M, AC ₹4.2M, EV ₹3.4M → CPI = 3.4/4.2 = 0.81 → Over budget by 19%
   - Example 2 — Orion Programme: BAC ₹12M, PV ₹7.2M, AC ₹6.5M, EV ₹6.84M → CPI = 6.84/6.5 = 1.05 → On budget, 5% efficient

3. **Industry benchmark alignment:** All threshold defaults are sourced from published benchmarks:
   - Utilisation targets: Gartner IT Services Benchmarking (2024)
   - Margin ranges: NASSCOM IT Services Industry Report (2024)
   - Attrition costs: SHRM Human Capital Benchmarking Report (2024)
   - SLA frameworks: ITIL v4 best practices

### 8.4 Proprietary Formulas — What's New and Why

7 of the 45 formulas are AKB1 proprietary — they don't exist in standard frameworks because the problems they solve are not addressed by standard tools:

| Formula | Why It's New | Why It Matters |
|---------|-------------|---------------|
| Net Programme Margin (including bench shadow allocation) | Standard margin calculations ignore bench costs | A programme showing 22% gross margin might be at 6% net after bench — this is the real margin |
| AI Trust Score (6-factor composite) | No governance framework for AI-augmented delivery exists in the market | Without this, organisations adopt AI tools with no way to measure whether they're trustworthy |
| AI Quality-Adjusted Velocity | Raw AI velocity is misleading — it doesn't account for rework | Using raw AI velocity for planning leads to consistent under-delivery |
| Delivery Health Index (13-KPI composite) | Single health score for a programme doesn't exist in standard frameworks | A portfolio head needs one number per programme to triage — DHI provides this |
| 3-System Utilisation Waterfall | No tool breaks utilisation into HRIS/RM/Billing with gap analysis | The 11-point gap between HR and billing utilisation is where margin dies |
| Renewal Probability | Account health scoring is done ad-hoc in most organisations | A Delivery Director's biggest risk is contract non-renewal — this makes it measurable |
| AI Cost-Benefit Ratio | No standard way to measure whether AI investment pays off | AI tool licenses cost money. Are they saving more than they cost, including rework? |

---

## 9. REAL-WORLD ADOPTION SCENARIOS

### Scenario A: Indian IT Services Delivery Director (Infosys/TCS/Wipro-size unit)

**Profile:** You manage a 120-person delivery unit serving a global banking client. 4 programmes, ₹32M annual revenue. Your data lives in: Jira (sprints), Confluence (risks), Excel (financials), HRIS (utilisation), and email (customer feedback).

**Week 1 — Setup:**
1. Install Command Center (15 minutes)
2. Upload programmes.csv with your 4 programmes
3. Upload kpi_monthly.csv from your existing Excel tracker (last 6 months)
4. Upload financials.csv from your P&L Excel

**Week 2 — Enrich:**
1. Export Jira sprint data → upload sprints.csv
2. Export HRIS utilisation → upload utilization_detail.csv
3. Enter risk register manually from Confluence (10-15 risks, 20 minutes)

**Week 3 — AI Governance:**
1. Register your AI tools in Tab 6 (Copilot, ChatGPT, Tabnine — 5 minutes)
2. Start tracking AI metrics per sprint (first data entry — 10 minutes)
3. First AI Trust Score appears

**Week 4 — Operational:**
1. Smart Ops starts firing alerts based on 4 weeks of data
2. First auto-generated narrative appears on Tab 1
3. First QBR prepared using "Generate QBR Brief" button — 5 minutes instead of 4 hours

**Outcome after 1 month:** You have a single dashboard answering 35+ CTO questions, automatic narrative summaries, proactive alerts for margin leaks and bench burns, and the foundation for AI governance. Your QBR prep time dropped from 4 hours to 5 minutes.

### Scenario B: US Consulting Practice Lead (Accenture/Deloitte-size practice)

**Profile:** You lead a 60-person consulting practice with 3 active engagements. USD $8M annual revenue. Your data is in Azure DevOps (delivery), Oracle Financials (costs), and Salesforce (customer).

**Setup:**
1. Install Command Center, select "US Consulting" industry preset (auto-sets USD, margin targets 40-55%, utilisation targets 65-72%)
2. Export Azure DevOps sprint data → map via auto-mapper → upload
3. Export monthly P&L summary from Oracle → upload financials.csv
4. Enter CSAT from last client survey manually

**Value realised in Week 1:** The margin waterfall reveals that bench allocation is absorbing 4.2% of gross margin — invisible in Oracle because bench costs are allocated to overhead, not programmes. The Command Center makes this visible for the first time.

### Scenario C: CTO Evaluating AI Adoption Across Portfolio

**Profile:** You're the CTO. You approved $120K for AI coding tools 6 months ago. The board asks: "What's the ROI?"

**What you need:**
1. AI cost per team per month (tool licenses)
2. AI productivity impact (velocity change, rework change)
3. AI quality impact (defect density comparison)
4. AI governance posture (are we using these tools safely?)

**What the Command Center shows:**
- Tab 6: AI Cost-Benefit Ratio = (1,240 hours saved × $95/hr) / ($120K tools + $28K rework) = $117,800 / $148,000 = 0.80 → AI investment is not yet ROI-positive
- Tab 6: AI vs Traditional Comparison → velocity +14%, but rework +3%, governance overhead +8 hrs/sprint
- Tab 6: AI Trust Score = 72 (Managed level, not yet Governed)
- Smart Ops: Governance drift alert fired for Project 2B (trust score dropped from 78 to 65 in 2 sprints)

**CTO's honest answer to the board:** "AI tools are showing 14% raw velocity improvement but are not yet ROI-positive when we factor in rework and governance overhead. We're 6 months into adoption. Projection shows breakeven at month 9 as rework stabilises. Governance maturity is at Level 2 (Managed) — we need to reach Level 3 (Governed) before expanding to more teams."

### Scenario D: Portfolio Head Preparing for QBR

**Profile:** You have a QBR with the client CEO in 3 hours. You need the "5 numbers that matter."

**Without AKB1 Command Center:** 4 hours of Excel wrangling, pulling data from 5 systems, formatting slides, hoping the numbers add up.

**With AKB1 Command Center:**
1. Open Tab 1 → Executive Overview → "Generate QBR Brief" button
2. Copy the auto-generated summary:
   "Portfolio of 5 programmes tracking at 18.5% net margin (1.5 points below plan). 1 programme at Red. Top concern: Phoenix (CPI 0.81, scope creep ₹450K). 4 programmes Green/Amber. Revenue realisation at 96.2%. Utilisation trending up 0.8 points month-over-month. Forecast: margin recovery to 20.1% by Q4 if Phoenix scope is controlled."
3. 5 minutes. Done.

---

## 10. WHAT INTELLIGENCE CAN YOU DERIVE?

### 10.1 The 50 Questions This Dashboard Answers

The Command Center is designed to answer every question a CTO, CIO, or CEO would ask about programme delivery. These are not hypothetical — they are the actual questions that come up in steering committees, QBRs, board reviews, and audit sessions.

**Financial Performance (12 questions):**
1. Are we making enough margin?
2. Where are we losing money?
3. What is true utilisation vs. reported?
4. How much does bench cost us?
5. Are change requests margin-positive or negative?
6. What is our revenue leakage?
7. Will we hit profit target this quarter?
8. What does rate card drift look like?
9. What is CPI telling us?
10. What is closeout variance?
11. What is AI costing us vs. saving us?
12. Cost per story point: AI vs. traditional?

**Delivery Health (6 questions):**
13. Which programmes need attention?
14. Are we on schedule?
15. Sprint velocity trend?
16. How accurate are forecasts?
17. Overall portfolio health?
18. Which projects within a programme are dragging?

**Risk & Governance (5 questions):**
19. Top 3 risks by financial impact?
20. Are we governing effectively?
21. SLA compliance rate?
22. How reliable is risk forecasting?
23. Predicted SLA breach risk?

**AI Governance (7 questions):**
24. Are AI tools actually helping?
25. Can we trust AI-generated code?
26. AI governance maturity?
27. How often do humans override AI?
28. What is AI productivity tax?
29. AI teams vs. traditional — give me the comparison
30. Is the AI velocity reliable enough to plan with?

**Customer & Relationship (6 questions):**
31. Is the customer happy?
32. What are they complaining about?
33. Will they renew?
34. Are we meeting their expectations?
35. How responsive are we to their problems?
36. Are we communicating enough?

**Strategic & Operational (6 questions):**
37. What should I fix right now?
38. Where can I reallocate resources?
39. Bench runway?
40. QBR story in 5 numbers?
41. What does the forecast say about next quarter?
42. Is pyramid inversion happening?

**Estimation & Planning (4 questions):**
43. How accurate were estimates?
44. Efficiency needed to finish on budget?
45. Estimation bias across portfolio?
46. What will this programme actually cost?

**People & Capacity (4 questions):**
47. Attrition cost?
48. Right skill pyramid?
49. Weekly utilisation recovery?
50. Team stability?

### 10.2 Intelligence Layers

The Command Center provides intelligence at 4 layers:

| Layer | What It Does | Example |
|-------|-------------|---------|
| **Descriptive** | What happened? | "CPI dropped from 0.92 to 0.81 over 3 months" |
| **Diagnostic** | Why did it happen? | "Primary driver: 3 uncontrolled change requests absorbing ₹450K" |
| **Predictive** | What will happen? | "At current trajectory, CPI will reach 0.79 by Q3-end" |
| **Prescriptive** | What should we do? | "TCPI of 1.31 indicates budget recovery is improbable. Recommend scope reduction." |

Most dashboards stop at descriptive. Power BI and Tableau can do diagnostic with manual modeling. The AKB1 Command Center delivers all 4 layers automatically.

---

## 11. DESIGN RIGOUR — HOW THIS WAS MADE FOOLPROOF

### 11.1 The Design Review Process

The v5.0 design went through a structured review cycle before any code was written:

**Round 1 — Initial Design (v5.0):**
- 9-tab architecture, 30 database tables, 37 formulas, 35 CTO questions
- Complete API spec, Docker configuration, demo data narrative

**Round 2 — Ruthless Self-Review (10 Critical Findings):**

A systematic review from the perspective of "what would break if a real delivery director tried to use this?" identified 10 critical gaps:

| # | Finding | Severity | Fix |
|---|---------|----------|-----|
| 1 | **Cold Start Problem** — No guidance for first-time users. They clone the repo and see demo data but have no path to their own data. | Critical | Added guided onboarding wizard (15 min to first real data), CSV auto-mapping, minimum viable data mode |
| 2 | **Currency/Localisation Hardcoded** — All examples in INR. A US consulting firm or European MSP cannot use it as-is. | High | Added multi-currency support (INR/USD/EUR/GBP), industry presets with adjustable thresholds |
| 3 | **No Predictive Analytics** — Dashboard only shows historical data. A CTO asks "what will happen next quarter?" and gets nothing. | Critical | Added forecast engine (3 models: linear regression, weighted moving average, exponential smoothing) |
| 4 | **Schema Gaps** — Missing Planned Value (PV) and Earned Value (EV) as stored data. CPI and SPI cannot be computed without inputs. No rate cards, milestones, or SLA incidents tables. | Critical | Added 7 new tables: evm_snapshots, milestones, sla_incidents, rate_cards, utilization_detail, customer_satisfaction, kpi_forecasts |
| 5 | **Frontend Scope Too Large** — 9 tabs in one build session is unrealistic (150+ hours). | High | Created phased build plan: alpha (55h, 5 tabs) → beta (3 tabs) → release (3 tabs) |
| 6 | **No Narrative Layer** — Data without interpretation is noise. Dashboard shows CPI = 0.81 but doesn't say "recovery is improbable." | High | Added template-based narrative generation engine — deterministic, no LLM dependency |
| 7 | **Utilisation Waterfall Data Gap** — Designed the waterfall visualisation but didn't create a table to store the 3-system data. | High | Added utilization_detail table with HRIS/RM/Billing + 5 gap categories |
| 8 | **No Export/Reporting** — No way to generate a QBR brief, audit package, or printable report. | Medium | Added PDF export, QBR brief generator, audit package ZIP export |
| 9 | **Smart Ops Not Actually Autonomous** — Called them "autonomous" but they're just threshold alerts. | Medium | Renamed to "proactive detection," added background scheduler (15-min scan), alert badges on Tab 1 |
| 10 | **Demo Data Lacks Narrative** — 5 programmes with random numbers. No story, no reason to care. | Medium | Created NovaTech Solutions story — each programme has a distinct problem that teaches the user how to interpret the dashboard |

**Round 3 — Ground-Level Reality Check:**

After fixing the 10 findings, a second review asked: "What does a portfolio owner actually do on a Monday morning? Does the dashboard support every action?"

This review added:
- Portfolio → Programme → Project three-level hierarchy (fixing the flat programme structure)
- Customer Intelligence tab (Tab 10) — because contract renewal is the biggest risk, not margin
- Audit & Compliance tab (Tab 11) — because enterprise IT services operate under compliance frameworks
- AI vs. Traditional team comparison framework (12 dimensions) — because "are AI teams faster?" is the CTO's #1 question
- 3 new Smart Ops scenarios (CPI trajectory, customer satisfaction drift, pyramid inversion)
- 15 new CTO questions (expanded from 35 → 50)
- 3 new formulas (Renewal Probability, AI Cost-Benefit Ratio, Forecast Confidence)

**Round 4 — Input Integration:**

All cross-verification, self-evaluation findings, and user inputs were documented as part of this FAQ to demonstrate the depth of design thinking.

### 11.2 What "Foolproof" Means in This Context

1. **Every formula is traceable** — click any number → see the formula, the input values, the data source
2. **Every threshold is editable** — disagree with the 74% utilisation target? Change it in Settings
3. **Every scenario has been walked through** — from first-time setup to QBR preparation to audit response
4. **Every gap has been identified and addressed** — 10 critical findings found and fixed before code was written
5. **The demo data tells a story** — not random numbers, but a realistic portfolio with 5 distinct problems
6. **Graceful degradation** — missing data doesn't break the dashboard, it shows clear prompts
7. **Multiple entry points** — guided wizard for beginners, CSV for bulk data, API for automation, manual forms for ad-hoc

---

## 12. KNOWN LIMITATIONS & HONEST TRADE-OFFS

No tool is perfect. Here are the honest limitations:

### 12.1 Current Limitations

| Limitation | Impact | Workaround | Roadmap |
|-----------|--------|-----------|---------|
| **Single-user (no auth)** | Cannot share with team members who need different views | Run on a shared machine or deploy to a team server | Multi-user with role-based access planned for v6 |
| **No direct integrations** | Cannot pull from Jira/ADO/ServiceNow natively | CSV export → upload, or script the REST API | Jira and ADO connectors planned for v6 |
| **SQLite** | Not suitable for > 50 programmes or > 500 concurrent users | Sufficient for single-portfolio use (5-15 programmes) | PostgreSQL migration planned for v6 |
| **Template-based narratives** | Narratives are formulaic, not natural language | Effective for structured reporting; won't replace human commentary | LLM-based narratives planned for v7 (optional) |
| **No Gantt chart** | Milestone timeline instead of full Gantt | Milestones with dependencies cover 80% of the need | Gantt planned for v6 |
| **No mobile app** | Tablet-friendly, not phone-optimized | Use Chrome on tablet | PWA planned for v7 |
| **AI metrics require manual input** | Most orgs don't have automated AI tracking | Start manual; build habit over 3-4 sprints | Auto-integration with Copilot/GitHub planned for v7 |

### 12.2 What This Tool Is NOT

- **Not an execution tool.** It doesn't replace Jira, Azure DevOps, or ServiceNow. Those are where your team does the work. This is where you measure and govern the work.
- **Not a financial system.** It doesn't replace SAP, Oracle, or QuickBooks. It consumes summarised financial data and provides delivery-specific financial intelligence.
- **Not a project management tool.** It doesn't manage tasks, assign work, or track time. It aggregates data from those tools into portfolio intelligence.
- **Not an AI platform.** It doesn't generate code or run AI models. It governs and measures AI tool usage across your delivery teams.

### 12.3 When You Should NOT Choose This Tool

| Scenario | Better Alternative |
|----------|-------------------|
| You manage a single project with < 15 people | Jira + a spreadsheet |
| You need enterprise-grade multi-user access with SSO | Planview, Clarity, or ServiceNow SPM |
| You need real-time Jira integration without CSV exports | Jira Portfolio or BigPicture plugin |
| You're a product company tracking user metrics | Mixpanel, Amplitude, or a product analytics tool |
| You need financial audit-grade accounting | SAP, Oracle Financials, NetSuite |

---

## 13. ARCHITECTURE & BUILD INSTRUCTIONS

### 13.1 Technical Architecture

```
Frontend (React 18 + Vite + Tailwind)
  ↕ REST API (JSON)
Backend (FastAPI + Python 3.12)
  ↕ SQL
Database (SQLite — /data/akb1.db in Docker volume)
```

**Why this stack:**
- **FastAPI:** Auto-generated Swagger docs, async by default, Python ecosystem for data processing
- **React 18:** Component model, rich chart libraries (Recharts, Chart.js), fast development
- **SQLite:** Zero-config, single-file backup, portable — perfect for single-user deployment
- **Docker Compose:** Single command deployment, reproducible across any OS

### 13.2 Database Schema Summary

44 tables across 10 groups:

| Group | Tables | Purpose |
|-------|--------|---------|
| Core (10) | programs, projects, kpi_definitions, kpi_snapshots, risks, risk_history, initiatives, sprint_data, commercial_scenarios, evm_snapshots | Main delivery data |
| New (7) | milestones, sla_incidents, rate_cards, utilization_detail, customer_satisfaction, kpi_forecasts, narrative_cache | v5.1 additions |
| AI Governance (8) | ai_tools, ai_tool_assignments, ai_usage_metrics, ai_code_metrics, ai_sdlc_metrics, ai_trust_scores, ai_governance_config, ai_override_log | AI tracking |
| Smart Ops (2) | resource_pool, scenario_executions | Proactive detection |
| Financial (3) | bench_tracking, scope_creep_log, loss_exposure | Loss tracking |
| Dual Velocity (2) | sprint_velocity_dual, sprint_velocity_blend_rules | AI velocity |
| System (3) | data_imports, app_settings, audit_log | Configuration |
| Customer Intelligence (2) | customer_expectations, customer_actions | Tab 10 expectation gap + action tracker |
| v5.2 Additions (5) | flow_metrics, project_phases, currency_rates, data_import_snapshots, schema_version | Kanban / Waterfall / multi-currency / rollback / Alembic |
| Security Stubs (2) | users, user_roles | Tier 3 RBAC scaffolding (populated when auth is enabled) |

Full SQL schemas with all columns, types, and relationships are in ARCHITECTURE.md Section 5.

### 13.3 API Documentation

The backend auto-generates Swagger documentation at `http://localhost:9001/docs`. All endpoints:

- 8 programme/project endpoints (CRUD)
- 5 KPI endpoints (definitions, snapshots, forecasts)
- 3 EVM endpoints
- 4 risk endpoints
- 2 sprint endpoints
- 2 financial endpoints
- 5 AI governance endpoints
- 3 Smart Ops endpoints
- 3 customer intelligence endpoints
- 3 narrative endpoints
- 2 report endpoints (QBR PDF, audit package)
- 5 data management endpoints (CSV import, auto-map, export, seed)
- 3 settings endpoints

### 13.4 Building From Source (For Contributors)

```bash
# Clone
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center

# Backend (Python 3.12)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 9001

# Frontend (Node 20)
cd ../frontend
npm install
npm run dev   # Starts Vite dev server on port 5173

# Docker (production)
docker-compose up --build
```

See CONTRIBUTING.md for code style, PR process, and testing requirements.

### 13.5 Phased Build Plan

| Phase | What | Tabs | Hours | CTO Questions Answered |
|-------|------|------|-------|----------------------|
| **Alpha** | Minimum Viable Command Center | 1, 2, 4, 8, 9 | 55 | 30 of 50 |
| **Beta** | Delivery + Risk + Customer | 3, 5, 10 | ~35 | 42 of 50 |
| **Release** | AI Governance + Smart Ops + Audit | 6, 7, 11 | ~40 | 50 of 50 |

---

## 14. COMPLETE QUESTION INVENTORY — 58 CTO/CIO/CEO QUESTIONS ANSWERED

For each question, the Command Center provides: the answer source (which tab, which chart), the formula used, and the data tables involved. The full mapping is in CTO_QUESTIONS.md.

| # | Question | Tab | Visual | Formula/Source |
|---|----------|-----|--------|---------------|
| 1 | Are we making enough margin? | 8 | Margin waterfall | 4-layer margin (Gross → Net) |
| 2 | Where are we losing money? | 8 | Loss category bar chart | 7 delivery loss formulas |
| 3 | True utilisation vs. reported? | 8 | 3-system waterfall | HRIS/RM/Billing comparison |
| 4 | Bench cost? | 8 | Bench allocation breakdown | Shadow allocation formula |
| 5 | CRs margin-positive? | 8 | CR economics table | CR value vs. processing cost |
| 6 | Revenue leakage? | 8 | 5-category tracker | Revenue realisation % |
| 7 | Hit profit target? | 8 | Forecast chart | EAC + predictive projection |
| 8 | Rate card drift? | 8 | Rate card comparison | Planned vs actual by tier |
| 9 | CPI telling us? | 3/8 | CPI trend + forecast | EV/AC with 3-month forecast |
| 10 | Closeout variance? | 8 | Decomposition chart | 5-component variance |
| 11 | AI cost vs saving? | 6 | Cost-benefit chart | AI Cost-Benefit Ratio |
| 12 | Cost/point: AI vs traditional? | 6/8 | Comparison panel | Sprint cost / points |
| 13 | Which programmes need attention? | 1/4 | CPI heatmap + DHI cards | DHI composite |
| 14 | On schedule? | 3 | SPI + milestones | EV/PV |
| 15 | Sprint velocity trend? | 3 | Burndown + velocity chart | Sprint velocity |
| 16 | Forecast accuracy? | 3 | Forecast vs actual | Prediction accuracy % |
| 17 | Portfolio health? | 1 | DHI + radar chart | 13-KPI composite |
| 18 | Projects dragging? | 4 | Project-level drill | Project CPI within programme |
| 19 | Top 3 risks? | 5 | Risk register sorted | Probability × Impact |
| 20 | Governing effectively? | 5 | Maturity scorecard | Governance maturity |
| 21 | SLA compliance? | 5 | SLA dashboard | SLA incidents analysis |
| 22 | Risk forecast reliability? | 5 | Prediction accuracy | Risk prediction vs actual |
| 23 | Predicted SLA breach? | 7 | Trend forecast | Linear regression on SLA data |
| 24 | AI tools helping? | 6 | SDLC impact metrics | Velocity/quality delta |
| 25 | Trust AI code? | 6 | Trust Score dashboard | 6-factor composite |
| 26 | AI governance maturity? | 6 | Maturity model | 5-level assessment |
| 27 | Override frequency? | 6 | Override log analysis | Override rate % |
| 28 | AI productivity tax? | 6 | Rework cost chart | Rework + governance hours |
| 29 | AI vs traditional comparison? | 6/4 | 12-dimension panel | Full comparison framework |
| 30 | AI velocity reliable for planning? | 3/6 | Merge protocol status | 6-gate assessment |
| 31 | Customer happy? | 10 | CSAT + NPS trends | Survey scores |
| 32 | Complaints? | 10 | Concern themes | Voice of Customer |
| 33 | Will they renew? | 10 | Renewal gauge | Renewal probability formula |
| 34 | Meeting expectations? | 10 | Expectation gap radar | 7-dimension analysis |
| 35 | Responsiveness? | 10 | Resolution time trend | SLA incident response |
| 36 | Communicating enough? | 10 | Meeting tracker | Meetings held vs planned |
| 37 | What to fix now? | 7 | Active alerts | Smart Ops 8 scenarios |
| 38 | Resource reallocation? | 7 | Rebalancing proposal | Utilisation delta |
| 39 | Bench runway? | 7 | Bench burn chart | Days × daily cost |
| 40 | QBR in 5 numbers? | 1 | Executive summary | Margin, util, forecast, rev real, CPI |
| 41 | Next quarter forecast? | 1/3 | Forecast charts | 3-model prediction |
| 42 | Pyramid inversion? | 7/8 | Rate card drift alert | Blended rate trend |
| 43 | Estimate accuracy? | 3 | BAC vs EAC vs Actual | Estimation variance |
| 44 | Efficiency to finish on budget? | 3 | TCPI calculation | (BAC-EV)/(BAC-AC) |
| 45 | Estimation bias? | 3 | Variance trend | Cross-programme comparison |
| 46 | Actual programme cost? | 3 | EAC + confidence band | Forecast with confidence % |
| 47 | Attrition cost? | 7 | Replacement cost | Hiring + ramp + productivity gap |
| 48 | Right skill pyramid? | 7 | Role distribution | Planned vs actual by tier |
| 49 | Utilisation recovery? | 7 | Weekly tracking | Weekly vs monthly delta |
| 50 | Team stability? | 7 | Attrition + tenure | Rate by programme |

---

## 15. FOR HIRING MANAGERS — WHAT THIS DEMONSTRATES ABOUT THE BUILDER

### 15.1 Why This Application Exists (The Career Context)

This application was designed and built by Adi Kompalli — a Senior Delivery & Program Manager with ~20 years of enterprise software delivery experience based in Hyderabad, India. It exists for two reasons:

1. **Solve a real problem:** Portfolio owners lack a single integrated view of delivery health + financials + AI governance + customer intelligence. This tool fills that gap.

2. **Demonstrate capability through execution, not just a resume:** Anyone can claim "portfolio management experience" or "AI governance expertise" on a resume. This application proves it — every formula, every framework, every scenario comes from real operational experience.

### 15.2 What This Application Demonstrates

| Competency | Evidence in This Application |
|-----------|------------------------------|
| **Delivery P&L Mastery** | 4-layer margin analysis, 7 delivery loss categories with financial quantification, shadow bench allocation, CR economics, rate card drift detection — none of these exist in standard tools because they come from real portfolio governance experience |
| **AI Governance (practical, not theoretical)** | 6-factor trust score, 5-level maturity model, 5-control framework, dual velocity tracking with 6-gate merge protocol, AI vs Traditional 12-dimension comparison — this is not from a consulting deck, it's from managing AI-augmented delivery teams |
| **System Architecture** | FastAPI + React + SQLite + Docker — a full-stack architecture designed for one-command deployment, with 44-table schema, REST API with Swagger, phased build plan, and clear separation of concerns |
| **Data-Driven Decision Making** | 45 formulas, each with 2 worked examples. 58 CTO questions, each mapped to a specific data source and visualisation. Predictive analytics with 3 forecast models. Template-based narrative generation |
| **Operating Model Design** | The entire application IS an operating model — it codifies how to govern a delivery portfolio: what to measure, what thresholds to set, what alerts to fire, what actions to take, what to report to whom |
| **Customer & Stakeholder Intelligence** | Renewal probability scoring, 7-dimension expectation gap analysis, escalation tracking, NPS/CSAT integration — because a portfolio owner's biggest risk is contract non-renewal |
| **Audit & Compliance Readiness** | AI audit trail, governance control dashboard, data lineage, exportable audit package — because enterprise IT services operate under compliance frameworks that most delivery tools ignore |
| **Open-Source Community Building** | MIT license, comprehensive documentation, contributor guide, CSV templates, demo data with narrative — designed for adoption, not just personal use |

### 15.3 The Gap This Person Fills

**The traditional delivery manager** manages timelines, resources, and risks. They use Jira and Excel. They prepare QBRs manually. They track AI adoption informally. They answer the CFO's margin questions by pulling 6 reports.

**What Adi Kompalli brings** is the layer above execution: a codified, data-driven delivery intelligence system that transforms scattered operational data into executive-ready portfolio intelligence. The AKB1 Command Center is proof of concept — not of a tool, but of an operating model.

This is what a Director-level Delivery Leader looks like: someone who doesn't just manage programmes but builds the systems, frameworks, and governance structures that make delivery predictable, measurable, and defensible.

### 15.4 Relevant Target Roles

| Role | Why This Person Fits |
|------|---------------------|
| Director — Delivery / Program Management | Proven portfolio-level governance, P&L accountability, operating model design |
| Associate Director — Delivery Excellence | Built the delivery excellence framework (the Command Center IS the delivery excellence tool) |
| Head of PMO / Transformation Office | Designed the Command Center + transformation playbooks + AI governance framework |
| Senior Delivery Manager (large accounts) | Multi-programme management with financial intelligence and AI governance |
| VP — Delivery Operations | Strategic delivery intelligence + AI transformation + commercial governance |

### 15.5 How to Evaluate This Work

If you're a hiring manager evaluating this candidate:

1. **Clone the repo and run it.** `docker-compose up` — 3 minutes. See the demo data. Click through the 11 tabs. Ask yourself: "Did this person understand my delivery challenges?"

2. **Read ARCHITECTURE.md.** Locked design. 42 database tables. 45 formulas. 58 CTO questions mapped. Ask yourself: "Is this design thoughtful or superficial?"

3. **Check the design review trail.** This FAQ documents 10 critical findings found and fixed during self-review — before code was written. Ask yourself: "Does this person catch problems proactively?"

4. **Look at the AI governance framework.** 6-factor trust score, 5-level maturity model, dual velocity tracking with 6-gate merge. Ask yourself: "Has this person actually governed AI-augmented delivery teams?"

5. **Look at the financial intelligence.** 4-layer margin, 7 loss categories, 3-system utilisation waterfall, bench allocation. Ask yourself: "Does this person understand delivery P&L at the level I need?"

---

## APPENDIX A: GLOSSARY

| Term | Definition |
|------|-----------|
| BAC | Budget At Completion — total approved budget |
| CPI | Cost Performance Index — value delivered per rupee/dollar spent |
| SPI | Schedule Performance Index — value delivered vs. planned |
| EAC | Estimate At Completion — projected total cost |
| TCPI | To-Complete Performance Index — efficiency needed to finish on budget |
| DHI | Delivery Health Index — AKB1 composite health score |
| RAG | Red-Amber-Green status |
| QBR | Quarterly Business Review |
| CSAT | Customer Satisfaction Score |
| NPS | Net Promoter Score |
| P&L | Profit and Loss |
| T&M | Time and Materials (contract type) |
| FP | Fixed Price (contract type) |
| CR | Change Request |
| SLA | Service Level Agreement |
| EVM | Earned Value Management |
| HRIS | Human Resources Information System |
| RM | Resource Management |

## APPENDIX B: DEMO DATA — NOVATECH SOLUTIONS PORTFOLIO

The demo ships with a complete narrative portfolio:

**Organisation:** NovaTech Solutions — 150-person IT services unit
**Client:** Global banking client
**Revenue:** ₹41M annually
**Programmes:** 5

| Programme | Revenue | Team | Key Challenge | What It Teaches |
|-----------|---------|------|--------------|-----------------|
| **Phoenix** — Core Banking Migration | ₹10M | 25 | CPI at 0.81, scope creep, margin compressed | How to detect and respond to cost overruns |
| **Atlas** — Cloud Migration | ₹8M | 18 | Razor-thin margin (8%), attrition risk | How bench allocation erodes margin invisibly |
| **Sentinel** — AI Test Automation | ₹5M | 12 | AI pilot: velocity +14%, defects +15% | How to govern AI tools and interpret dual velocity |
| **Orion** — Data Platform | ₹12M | 30 | Cash cow but bench tax absorbing ₹1.4M | How hidden losses eat into profitable programmes |
| **Titan** — Digital Commerce | ₹6M | 15 | SLA breaches, 25% attrition, CSAT dropping | How customer intelligence prevents contract loss |

Each programme has 12 months of synthetic but realistic data. The data tells a story — it's not random numbers.

---

## 16. v5.2 ADDENDUM

Added 2026-04-16 after ultra-think review (28 gaps closed). Everything below supplements, not replaces, the sections above. Where a section 1–15 claim conflicts with this addendum, the addendum wins.

### 16.1 SDLC Framework Compatibility — "Does this work for Waterfall / Kanban / SAFe / Hybrid, or only Scrum?"

**Answer:** v5.2 supports Scrum, Kanban, Waterfall, SAFe, and Hybrid side-by-side in the same portfolio. Each project has a `delivery_methodology` field; Tab 3 Delivery Health adapts its UI per project.

| Methodology | What you upload | What you see on Tab 3 | Metrics used |
|-------------|-----------------|------------------------|--------------|
| Scrum | `sprints.csv` | Sprint burndown, velocity | Velocity, SPI/CPI, predictability |
| Kanban | `flow_metrics.csv` | Cumulative flow diagram, WIP aging | Throughput, cycle time p85, lead time, WIP breach |
| Waterfall | `project_phases.csv` + `evm_monthly.csv` | Milestone timeline, phase gates | Phase variance, gate approval rate, milestone slip |
| SAFe | `sprints.csv` (PI mapped to Programme, Feature to Project, Iteration to Sprint) | PI burnup + Scrum view | Velocity + Feature completion + PI predictability |
| Hybrid | Mix of above per project | Project-level adaptive view | Auto-selected per project |

### 16.2 Multi-Currency — "We run projects in USD, GBP, EUR — not just INR. Will this work?"

**Answer:** Yes. v5.2 has a first-class currency engine.

- Pick your base currency on first-run (INR, USD, EUR, GBP, or any ISO 4217 code).
- Each programme stores its native currency in the programmes table.
- `currency_rates` table holds editable exchange rates with a "last updated" timestamp.
- Portfolio totals always display in base currency; tooltips show native value and rate.
- Rate refresh is manual in v5.2 (Tab 11 Settings); v5.3 adds an optional daily API refresh.

**Example:** Base = USD. You have programmes in GBP 1.2M, EUR 3.4M, INR 28 Cr. The portfolio dashboard rolls up to USD using your rates; each programme card shows its native value, and hovering reveals the conversion.

### 16.3 Fiscal Year, Number Format, Date Format

- **FY:** Apr–Mar (India, UK, Saudi), Jan–Dec (US, most of Europe), Oct–Sep (Japan, US Fed), or any custom start month.
- **Numbers:** Indian lakh/crore, US thousand/million/billion, European (1.000.000,00).
- **Dates:** DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD.

Settings are applied system-wide and can be changed at any time.

### 16.4 Windows Users — "Does this run on Windows or only Mac/Linux?"

**Answer:** Yes, it runs on Windows 10/11 natively via Docker Desktop + WSL2.

**Install on Windows:**
1. Install Docker Desktop for Windows (includes WSL2 setup): https://www.docker.com/products/docker-desktop
2. Enable WSL2 backend (Settings → General → "Use the WSL 2 based engine").
3. Open PowerShell:
   ```powershell
   git clone https://github.com/deva-adi/akb1-command-center.git
   cd akb1-command-center
   docker compose up -d
   start http://localhost:9000
   ```
4. Health check:
   ```powershell
   Invoke-WebRequest http://localhost:9001/health
   ```

**Windows-specific gotchas handled in v5.2:**
- Path separators: we never hardcode `/` or `\`.
- Line endings: `.gitattributes` enforces LF in checked-in scripts.
- File uploads: drag-drop works identically on Windows; large .xlsx files stream so 8GB laptops work.

### 16.5 Excel / XLSX Import — "I only have .xlsx files from Jira, ADO, SAP exports"

**Answer:** Native .xlsx is supported in v5.2 via openpyxl. No pre-conversion needed. CSV is still supported — you can mix formats in the same upload session.

**Source-tool walkthroughs** in `docs/DATA_INGESTION.md`:
- Jira (CSV or XLSX export) → `sprints.xlsx` or `flow_metrics.xlsx`
- Azure DevOps → `sprints.xlsx`
- ServiceNow (PPM) → `risks.xlsx`
- SAP (financials) → `financials.xlsx`

### 16.6 Wireframes — "Can I see every screen before I install?"

**Answer:** Yes. `docs/WIREFRAMES.md` contains ASCII mockups for all 11 tabs with a metric dictionary per tab explaining what every number means, who asks for it, and why it matters. Scroll through WIREFRAMES.md before cloning — it is designed as your pre-install evaluation tool.

### 16.7 Tech Stack — "Is your stack stable? Have you benchmarked it?"

**Answer:** Yes. `docs/TECH_STACK_BENCHMARK.md` compares AKB1 (FastAPI + React + SQLite + Docker) against 18 stable open-source dashboards (Plausible, Grafana, Metabase, Focalboard, Homepage, n8n, NocoDB, etc.). Conclusion: the stack is correct-by-design for single-maintainer + single-container installability. Surgical additions in v5.2: shadcn/ui (accessible components), Alembic (migrations), Pydantic Settings, React Query, Zustand, Playwright, Ruff/MyPy, openpyxl. No replatforming. Postgres DAL and OpenTelemetry are v5.3 roadmap.

### 16.8 Production Grade — "How do I know this won't fall over?"

**Answer:** `docs/PRODUCTION_SDLC.md` documents the seven-phase SDLC AKB1 follows: Requirements → Design → Implementation → Verification → Release → Operate → Learn. Every Sev-1 bug gets a public postmortem in `docs/postmortems/`. Every PR must pass lint + type check + tests. Every release must pass Trivy scan, migration test against prior-version snapshot, and cold-start reproduction on a fresh VM.

### 16.9 Data Safety — "What happens if I upload a bad CSV?"

**Answer:**
- Pre-flight validation gives clear, line-numbered error messages before any write.
- If the import succeeds, a snapshot of pre-import state is saved in `data_import_snapshots`.
- One-click rollback from Tab 11 Data Hub restores the prior state instantly.
- Automated daily SQLite backup runs inside the container with 30-day rolling retention.

### 16.10 Accessibility — "Is this accessible for users with disabilities?"

**Answer:** v5.2 targets WCAG 2.1 AA. Contrast ratios validated against Navy/Ice Blue/Amber palette. Keyboard navigation supported throughout. ARIA labels on all interactive elements. Charts supplement colour with icons and labels. Screen-reader spot-check is a release gate.

### 16.11 Alerting — "Can Smart Ops alert me in Slack or Teams?"

**Answer:** Yes. v5.2 Smart Ops engine supports configurable webhooks — email, Slack incoming webhook, Microsoft Teams connector. Configure in Tab 11 Settings → Alerts. Severity SLAs: Sev-1 30 min, Sev-2 4 hours, Sev-3 24 hours.

### 16.12 Browser Support

Chrome, Firefox, Safari, **Edge** — latest two versions of each.

### 16.13 Upgrading from v5.0 or v5.1

Run `docker compose pull && docker compose up -d`. Alembic migrations apply automatically on container start. Pre-upgrade snapshot is taken and can be rolled back via the `scripts/rollback.sh` helper.

### 16.14 Security — "What about authentication and security? This is my delivery data."

**Answer:** AKB1 provides a **4-tier progressive security model** — you choose the level that matches your deployment:

| Tier | What It Does | Setup |
|------|-------------|-------|
| **0 — Localhost** (default) | Dashboard only accessible from your machine (`127.0.0.1`). Rate limiting, input validation, non-root container, read-only filesystem. | Zero config |
| **1 — Basic Auth + HTTPS** | Caddy reverse proxy with password protection and automatic TLS certificate. | `docker compose -f docker-compose.yml -f docker-compose.proxy.yml up -d` |
| **2 — SSO (OAuth2 Proxy)** | Plug in Google Workspace, Azure AD, Okta, Keycloak, or GitHub as your identity provider. No code changes. | Set 3 env vars, run with SSO overlay |
| **3 — Built-in OIDC** (v5.4) | Native login page with per-user RBAC (Admin / Portfolio Lead / Viewer). Fine-grained access control at API level. | Planned for v5.4 |

**What ships by default (Tier 0):**
- Ports bound to `127.0.0.1` — not accessible over the network
- Rate limiting (60 reads/min, 10 writes/min per IP)
- All inputs validated via Pydantic v2 — no injection risk
- Container runs as non-root with read-only filesystem
- OWASP Top 10 (2021) fully mapped with mitigations documented

**API access:** Bearer token API key generated on first run, rotatable via Tab 11. Used for CI/CD pipelines, cron jobs, Power Automate.

**Full guide:** `docs/SECURITY_GUIDE.md` (20 sections, OWASP + CIS Docker Benchmark aligned). Vulnerability disclosure: `SECURITY.md`.

### 16.15 Complete v5.2 Change Summary

- Tables 37 → 44 (+ flow_metrics, project_phases, currency_rates, data_import_snapshots, schema_version, users, user_roles).
- Formulas 40 → 45 (+ currency conversion, Kanban throughput, cycle time, lead time, WIP aging).
- CTO/CIO/CEO questions 50 → 58 (+ 8 for Kanban/Waterfall/currency/FY).
- CSV templates 13 → 15 (+ flow_metrics.csv, project_phases.csv).
- Tabs 9 → 11 (+ Reports/Exports tab, + Data Hub/Settings tab).
- New docs: SECURITY.md, SECURITY_GUIDE.md, MASTER_CHECKLIST.md, WIREFRAMES.md, TECH_STACK_BENCHMARK.md, PRODUCTION_SDLC.md.
- New configs: docker-compose.proxy.yml, Caddyfile.
- Security hardening: localhost bind, rate limiting, container hardening, OWASP mapped, 4-tier auth strategy.

---

**Document maintained by Adi Kompalli | AKB1 Framework | v1.3 | 2026-04-16**
**License:** MIT — this documentation is part of the open-source AKB1 Command Center repository.
