# AKB1 Command Center v5.2 — Build Roadmap

**Author:** Adi Kompalli, AKB1 Framework  
**Date:** 2026-04-16  
**Version:** 1.1 (Updated for v5.2)  
**Classification:** Internal — Product Development

---

## Executive Summary

This roadmap defines four two-week iterations for AKB1 Command Center v5.2, from Foundation (I-1) through Polish & Ship (I-4). Each iteration incrementally expands tab coverage, backend capabilities, and governance workflows. By I-4, the system answers all 58 CTO/CIO/CEO strategic delivery questions, supports 5 SDLC frameworks (Scrum/Kanban/Waterfall/SAFe/Hybrid), multi-currency portfolios, and ships as a production-grade Docker application. For the detailed 7-phase production SDLC, see [`PRODUCTION_SDLC.md`](PRODUCTION_SDLC.md).

---

## Build Iterations Overview

| Iteration | Duration | Scope | Tabs | CTO Qs | Strategic Benefit |
|-----------|----------|-------|------|--------|------------------|
| **I-1 Foundation** | Weeks 1-2 | Docker, DB (44 tables), seed, API scaffolding, security hardening, Tab 1 + Tab 11 | 1, 11 | 10 | Infrastructure + security + onboarding |
| **I-2 Core Dashboard** | Weeks 3-4 | Tabs 2-5: Programme Portfolio, Delivery Health (3A/3B/3C), Velocity & Flow, Margin & EVM | 2, 3, 4, 5 | 35 | Core delivery intelligence |
| **I-3 Advanced** | Weeks 5-6 | Tabs 6-9: Customer Intelligence, AI Governance, Smart Ops, Risk & Audit | 6, 7, 8, 9 | 52 | Full governance + proactive detection |
| **I-4 Polish & Ship** | Weeks 7-8 | Tab 10 Reports, predictive engine, E2E tests, WCAG AA pass, SBOM, README, release | 10 | 58 | Production-grade release |
| **v5.3+ Horizon** | Q4 2026 | PostgreSQL DAL, OpenTelemetry, Helm chart, DuckDB-WASM, connectors | — | — | Enterprise scale |
| **v5.4 Auth** | Q1 2027 | Built-in OIDC (Tier 3), native login page, fine-grained RBAC, per-user audit trail | — | — | Enterprise auth |

**Total Build Effort:** ~8 weeks (~2 FTE at 80% allocation)

### Quality Gates Per PR (All Iterations)
- Ruff + MyPy pass (zero errors)
- pytest + Vitest pass (coverage ≥ 70%)
- Conventional Commit message format
- No new accessibility regressions (axe-core)

### Release Gates (I-4 Only)
- Trivy container scan (zero critical/high CVEs)
- SBOM generated (CycloneDX)
- CHANGELOG.md updated
- Alembic migration test (fresh DB + upgrade from I-1 schema)
- Cold-start reproduction test (clone → `docker compose up` → dashboard in <3 min)
- All 5 SDLC methodology smoke tests pass
- Security hardening verified (localhost bind, rate limiting, non-root, read-only fs)
- Bandit Python security lint pass (zero high findings)
- OWASP Top 10 checklist reviewed (SECURITY_GUIDE.md §17)

---

## Phase 1: v5.0-alpha (55 hours) — MVP Release Candidate

**Release Target:** 2026-04-30  
**Scope:** 5 of 11 tabs | 30 of 58 CTO questions answered | Foundation complete

### Deliverables by Tab

#### Tab 1: Executive Overview (8 hrs)
**Components:**
- Real-time KPI cards: Revenue, Margin %, On-Time %, Cost Overrun
- Portfolio risk heat map (5×5 programme/risk matrix)
- Monthly burn chart (cost trend last 6 months)
- Governance alerts panel (critical, high, medium priority)
- Health scorecard summary (delivery, margin, quality, people)

**Data Sources:**
- All 5 programmes + YTD actuals
- EVM monthly snapshots (planned value, earned value, actual cost)
- Change request log (uncontrolled scope tracking)
- SLA/CSAT snapshots from Titan programme

**Technical Build:**
- React dashboard layout (Recharts for KPI cards, burn chart)
- Real-time alert engine (filters by severity and programme)
- Mobile-responsive card layout

**Success Criteria:**
- Executive can see portfolio health in <2 minutes
- All 5 programmes visible; drill-down to programme detail available
- Alerts surface top 3 governance issues

#### Tab 2: KPI Studio (12 hrs)
**Components:**
- KPI library sidebar (40+ metrics pre-configured)
- Trend charts: CPI, SPI, Margin %, Utilization %, Defect Density
- Data export: Excel, CSV
- Custom metric creation (formula builder)
- Comparison view: side-by-side programme metrics

**Data Sources:**
- Monthly EVM data (3 months)
- Staffing & utilization data
- Quality metrics (defect density, test coverage)
- Commercial data (margin %, revenue realization %)
- AI augmentation metrics (Sentinel-specific: AI Trust Score, velocity uplift)

**Technical Build:**
- Metric definition table in SQLite (name, formula, unit, target, alert threshold)
- Trend line charts (3 months of history)
- Export pipeline (Pandas + openpyxl for Excel generation)

**Success Criteria:**
- 40+ KPIs pre-configured and callable
- Trend visualization for any KPI over 3 months
- Custom KPI formula builder allows +/- /× operations

#### Tab 4: Portfolio — Programme & Project View (10 hrs)
**Components:**
- Programme-level summary cards (revenue, team size, CPI, margin)
- Project-level drill-down (BAC, EV, AC, schedule variance, risks)
- Uncontrolled scope tracker (change requests by programme)
- Resource allocation heatmap (FTE distribution across programmes)
- Simplified Gantt view (status colour-coded)

**Data Sources:**
- Programme master data (5 programmes, 15 projects)
- EVM monthly actuals (project-level earned value)
- Resource allocation by project
- Change request log (scope impact tracking)
- Risk log (risk ID, status, impact, owner)

**Technical Build:**
- Hierarchical data tree (programme → projects)
- Project cards with 6 key metrics (BAC, EV, AC, SPI, CPI, % Complete)
- Collapsible Gantt timeline (Month-view, colour-coded by status)
- Heatmap rendering (resource allocation % by skill)

**Success Criteria:**
- 15 projects visible; drill-down to project detail
- CPI and schedule variance calculated for each project
- Resource heatmap identifies >100% allocations

#### Tab 8: Commercials (15 hrs)
**Components:**
- Portfolio P&L summary (Revenue, CoD, Gross Margin, Net Margin)
- Programme-level commercial dashboard (by-programme P&L)
- Cost breakdown: labour %, infrastructure %, vendor %
- Bench cost allocation and impact analysis
- Change request financial impact tracker
- Revenue forecast (QoQ for FY)
- Scenario modelling: margin impact of CR approval/deferral

**Data Sources:**
- Programme revenue and cost data (all 5 programmes)
- Labour cost breakdown (by seniority, role)
- Bench cost allocation (Orion: 8 FTE, ₹1.4M annually)
- Change request log with financial impact
- Monthly revenue and cost actuals

**Technical Build:**
- P&L calculation engine (Revenue - CoD - Overhead = Net Margin)
- Scenario modelling (adjust CR approval status, bench FTE, see margin impact)
- Waterfall chart for cost breakdown
- Forecast table (QoQ revenue, margin % trend)

**Success Criteria:**
- Portfolio P&L accurate to ±₹50k
- Bench cost impact clearly visible (3.4% of margin for Orion)
- Scenario: 30% bench reduction in Orion shows +₹420k to net margin

#### Tab 9: Settings (10 hrs)
**Components:**
- Demo mode toggle (Live Data ↔ Demo Data)
- Data seeding: Load NovaTech profile, load sample scenarios, reset to baseline
- KPI configuration UI (define custom metrics, targets, alert thresholds)
- User roles stub (Admin-only for v5.0; RBAC in v5.2)
- Export & reporting: PDF executive summary, Excel KPI trends, audit trail
- System logs & audit trail (data change timestamps, user actions)

**Data Sources:**
- Demo seed data (5 programmes, 15 projects, 3 months EVM, NovaTech narrative)
- KPI definition table
- Audit log table

**Technical Build:**
- Toggle switch for data source (live vs demo)
- Seed script (populates all 5 programmes + EVM data + NovaTech narrative)
- KPI form UI (metric name, formula, unit, target, alert)
- Audit trail view (timestamp, user, action, data affected)

**Success Criteria:**
- Demo data loads in <1 second
- Reset to baseline clears all data and resets to v5.0-alpha state
- Audit log shows all data modifications with timestamp

### Backend Build (Phase 1 — v5.0-alpha)

**Database Schema: 30 tables**

**Core Entities (6 tables):**
- `organizations` (org_id, name, revenue, headcount, created_at)
- `programmes` (programme_id, org_id, code, name, start_date, end_date, bac, revenue, team_size, status, created_at)
- `projects` (project_id, programme_id, code, name, start_date, end_date, bac, revenue, team_size, tech_stack, is_ai_augmented, ai_augmentation_level, created_at)
- `resources` (resource_id, project_id, role, seniority, allocation_pct, cost_monthly, created_at)
- `staffing_pool` (pool_id, programme_id, role, total_fte, available_fte, cost_per_fte, created_at)

**EVM & Delivery (6 tables):**
- `evm_monthly` (snapshot_id, programme_id, project_id, snapshot_date, planned_value, earned_value, actual_cost, bac, percent_complete, created_at)
- `schedule_variance` (variance_id, project_id, snapshot_date, planned_finish, actual_finish, variance_days, created_at)
- `sla_metrics` (sla_id, programme_id, project_id, metric_name, target, actual, period_start, period_end, created_at)
- `defect_metrics` (defect_id, programme_id, project_id, period_start, period_end, total_defects, critical_defects, defect_density, created_at)
- `quality_metrics` (quality_id, programme_id, project_id, metric_name, value, period_start, period_end, created_at)

**Commercial & Financials (6 tables):**
- `programme_commercial` (commercial_id, programme_id, snapshot_date, revenue, labour_cost, infra_cost, vendor_cost, gross_margin, margin_pct, bench_cost, bench_fte, created_at)
- `cost_breakdown` (cost_id, programme_id, cost_category, cost_amount, cost_type, period_start, period_end, created_at)
- `bench_allocation` (bench_id, programme_id, bench_fte, bench_cost_monthly, utilization_pct, reason, created_at)
- `change_requests` (cr_id, programme_id, project_id, cr_name, description, scope_cost, schedule_impact_days, status, requested_by, created_at, approved_at)
- `revenue_forecast` (forecast_id, programme_id, period, revenue_forecast, margin_forecast, confidence_pct, created_at)

**KPI & Governance (6 tables):**
- `kpi_definitions` (kpi_id, kpi_name, formula, unit, target, alert_threshold, owner, created_at)
- `kpi_values` (value_id, kpi_id, programme_id, project_id, snapshot_date, value, status, created_at)
- `alerts` (alert_id, alert_type, severity, message, programme_id, created_at, acknowledged_at)
- `risk_log` (risk_id, programme_id, project_id, risk_description, impact, likelihood, status, owner, created_at, resolved_at)
- `governance_events` (event_id, event_type, affected_object, action, timestamp, user_id, created_at)

**AI & Augmentation (4 tables):**
- `ai_augmentation` (aug_id, programme_id, project_id, augmentation_type, model_name, trust_score, velocity_uplift_pct, defect_density_change_pct, cost_benefit_ratio, created_at)
- `ai_model_performance` (perf_id, augmentation_id, metric_name, baseline_value, augmented_value, period_start, period_end, created_at)

**Configuration & Audit (2 tables):**
- `kpi_config` (config_id, kpi_id, target, alert_low, alert_high, owner, programme_id, created_at)
- `audit_trail` (audit_id, table_name, record_id, action, old_value, new_value, user_id, timestamp, created_at)

**API Endpoints (Core v5.0):**

| Endpoint | Method | Purpose | Returns |
|----------|--------|---------|---------|
| `/api/org/{org_id}/dashboard` | GET | Executive overview data | KPI cards, alerts, heat map |
| `/api/org/{org_id}/programmes` | GET | List programmes | [programme objects] |
| `/api/programme/{programme_id}/detail` | GET | Programme detail + projects | Programme + [projects] |
| `/api/programme/{programme_id}/evm` | GET | EVM history (3 months) | [evm_monthly rows] |
| `/api/kpi/{kpi_id}/trends` | GET | KPI trend over 3 months | [kpi_values] |
| `/api/org/{org_id}/commercials` | GET | P&L summary | Portfolio P&L object |
| `/api/programme/{programme_id}/commercials` | GET | Programme P&L | Programme P&L object |
| `/api/programme/{programme_id}/change-requests` | GET | CRs for programme | [change_requests] |
| `/api/scenario/margin-impact` | POST | Model margin impact of CR | { margin_delta, margin_pct_new } |
| `/api/data/seed-demo` | POST | Load NovaTech demo data | Confirmation message |
| `/api/audit-trail` | GET | List audit events | [governance_events] |

**Forecast Engine (v5.0-alpha: Basic):**
- Linear regression on EVM trend (planned value, earned value, actual cost)
- Estimate-to-Complete (ETC) = BAC - EV + (AC / EV)
- Forecast at Completion (FAC) = AC + ETC
- Schedule forecast: project finish date based on SPI trend

**Demo Seeder:**
- NovaTech Solutions profile: 5 programmes, 15 projects, 100 FTE
- 3 months of monthly EVM data (January–March 2025)
- Commercial data: revenue, labour cost, bench allocation
- Change request log: 3 CRs for Phoenix (tracking uncontrolled scope)
- SLA/CSAT/attrition data for Titan
- AI augmentation metrics for Sentinel (AI Trust Score 86, +14% velocity)

### Questions Answered by v5.0-alpha

**Delivery & Schedule (10 questions):**
1. What is the current schedule performance across the portfolio? (Tab 1, 4: SPI trend)
2. Which projects are at risk of missing their end date? (Tab 4: schedule variance)
3. What is the forecast completion date and cost for each project? (Tab 2, 4: ETC/FAC)
4. How much schedule buffer remains? (Tab 4: variance % of plan)
5. What is the critical path across all programmes? (Tab 4: Gantt view)
6. What is the impact on schedule if we approve pending change requests? (Tab 8: scenario model)
7. Are we trending better or worse than last month? (Tab 2: KPI trends)
8. Which programmes are on-time and which are not? (Tab 1, 4: status summary)
9. How many projects have schedule variance >10%? (Tab 2: KPI filter)
10. What is the team's actual productivity vs. plan? (Tab 2: velocity KPI)

**Margin & Commercial (10 questions):**
11. What is the portfolio margin and how does it compare to target? (Tab 1, 8: margin %)
12. Which programmes are above/below margin target? (Tab 8: by-programme P&L)
13. What is the cost breakdown by programme? (Tab 8: labour, infra, vendor %)
14. How much is bench costing us? (Tab 8: bench cost allocation)
15. What would margin be if we rationalize bench by 30%? (Tab 8: scenario model)
16. How much uncontrolled scope is in the pipeline? (Tab 4, 8: CR financial impact)
17. What is the impact of pending CRs on margin? (Tab 8: scenario model)
18. What is the revenue forecast for the rest of the year? (Tab 8: forecast table)
19. Are we on-track for annual revenue targets? (Tab 8: YTD vs plan)
20. What is the cost-to-serve by programme? (Tab 8: CoD breakdown)

**Quality & Risk (10 questions):**
21. What is the defect density by programme? (Tab 2: quality KPI)
22. Are defect trends improving or worsening? (Tab 2: defect density trend)
23. What is the critical defect rate? (Tab 2: critical defect KPI)
24. Which programmes have quality risk? (Tab 1: risk heat map)
25. What is the test coverage by programme? (Tab 2: test coverage KPI)
26. How many open risks are there and by severity? (Tab 1: alerts panel)
27. What is the SLA compliance by programme? (Tab 2: SLA compliance KPI)
28. How many P1 incidents occurred in the last quarter? (Tab 2: SLA metric)
29. What is CSAT by programme? (Tab 2: CSAT KPI)
30. How is our quality trending vs. last month? (Tab 2: quality KPI trends)

**Total Questions Answered by v5.0-alpha: 30 of 50**

---

## Phase 2: v5.1-beta (60 hours) — Delivery Planning + Risk Governance + Customer Intelligence

**Release Target:** 2026-05-31  
**Scope:** Add 3 new tabs | 52 of 58 CTO questions answered | Risk governance workflows operationalized

### Deliverables by Tab

#### Tab 3: Delivery Planning (20 hrs)
**Purpose:** Roadmap visibility, capacity planning, resource forecasting

**Components:**
- Rolling wave planning: Next 2 quarters visible
- Sprint/iteration board (if Agile; else, Waterfall milestone view)
- Capacity planning: FTE available vs. committed
- Resource levelling: Identify over/under-allocated resources
- Dependency visualization: Cross-programme impacts
- Risk register with mitigation actions
- Burndown/Burnup charts (by programme)

**Data Sources:**
- Project roadmap (milestones, deliverables, dates)
- Sprint/story backlog
- Resource calendar (availability, planned leave)
- Dependency map (internal and external)

#### Tab 5: Risk & Governance (20 hrs)
**Purpose:** Operational risk dashboard, governance workflow tracking, RAID management

**Components:**
- Risk heat map (5×5: impact vs likelihood)
- Risk register with drill-down
- Action items (RAID: Risks, Actions, Issues, Decisions)
- Change control workflow (CR submission → review → approval)
- Steering committee scorecard (readiness for governance meeting)
- Risk response tracking (mitigations, owners, due dates)
- Governance metrics: Forecast accuracy %, RAID quality score

**Data Sources:**
- Risk log (risk_id, description, impact, likelihood, status, owner)
- Action item log (action_id, owner, due_date, status)
- Issue log (issue_id, programme_id, impact, owner, resolution_target)
- Decision log (decision_id, decision, rationale, owner, approval_date)
- Change request workflow states (submitted, under-review, approved, rejected, in-progress, closed)

#### Tab 10: Customer Intelligence (20 hrs)
**Purpose:** Client relationship health, CSAT/NPS trends, upsell/cross-sell opportunities

**Components:**
- Client health scorecard (by programme)
- CSAT/NPS trends (quarterly)
- Account risk analysis (churn risk, satisfaction trend)
- Upsell/cross-sell pipeline
- Service level agreements (SLA compliance by metric)
- Escalations and resolutions (P1/P2/P3 incidents)
- Executive sponsor alignment (stakeholder sentiment)

**Data Sources:**
- CSAT survey data (quarterly by programme)
- NPS survey data
- SLA compliance metrics
- Incident/service request log
- Account health assessments
- Renewal dates and pipeline

### Questions Answered by v5.1-beta

**Delivery Planning & Capacity (7 questions):**
31. What capacity do we have available for new work in the next 2 quarters? (Tab 3: capacity plan)
32. Which resources are over-allocated and by how much? (Tab 3: resource levelling)
33. What are the critical path dependencies across programmes? (Tab 3: dependency viz)
34. What is the forecast headcount need for next quarter? (Tab 3: resource forecast)
35. How many story points can we commit to in the next sprint? (Tab 3: capacity + backlog)
36. What are the inter-programme dependencies and risks? (Tab 3: dependency map)
37. What is the team's velocity trend over the last 4 sprints? (Tab 3: burndown chart)

**Risk & Governance (8 questions):**
38. What are the top 5 risks by impact? (Tab 5: risk heat map)
39. Which risks are trending better or worse? (Tab 5: risk status trend)
40. What actions are overdue and by whom? (Tab 5: RAID board)
41. What is the forecast accuracy for our estimates? (Tab 5: governance metric)
42. How many unresolved issues are there and by severity? (Tab 5: issue log)
43. What is the change request approval rate? (Tab 5: CR workflow metrics)
44. Are we ready for the steering committee meeting? (Tab 5: readiness scorecard)
45. What is the RAID quality score (governance health)? (Tab 5: RAID metrics)

**Customer Intelligence (7 questions):**
46. What is the CSAT/NPS for each programme? (Tab 10: health scorecard)
47. Which accounts are at churn risk? (Tab 10: account risk analysis)
48. What is the SLA compliance for each service? (Tab 10: SLA trends)
49. What upsell/cross-sell opportunities are on the horizon? (Tab 10: pipeline)
50. How are executive sponsors tracking vs. expectations? (Tab 10: stakeholder alignment)

**Note:** Tabs 1, 2, 4, 8 are enhanced with new KPIs and deeper drill-downs.

**Total Questions Answered by v5.1-beta: 42 of 50**

---

## Phase 3: v5.2-release (75 hours) — Full Production Release

**Release Target:** 2026-06-30  
**Scope:** Add 3 final tabs | All 58 CTO questions answered | Predictive engine, PDF export, audit package

### Deliverables by Tab

#### Tab 6: AI Governance (20 hrs)
**Purpose:** AI augmentation oversight, model performance tracking, trust and compliance monitoring

**Components:**
- AI augmentation registry (by programme, model, trust score)
- Model performance dashboard (baseline vs. augmented metrics)
- AI trust score trending
- Defect detection vs. prevention analysis
- AI cost-benefit analysis
- Augmentation expansion recommendations
- Compliance & audit trail for AI decisions

**Data Sources:**
- AI augmentation table (aug_id, programme_id, model, trust_score, velocity_uplift, defect_density_change)
- AI model performance (baseline vs. augmented comparisons)
- Trust score calculation methodology

#### Tab 7: Smart Ops (20 hrs)
**Purpose:** Autonomous governance, background scheduler, predictive alerts, anomaly detection

**Components:**
- Autonomous governance workflows (background scheduler)
- Predictive alerts: forecasts when metrics will breach threshold
- Anomaly detection: identifies unusual patterns
- Recommendation engine: suggests remediation actions
- Automated reports (daily digest, weekly highlights)
- Workflow automation: auto-escalate overdue actions, auto-approve low-risk CRs
- Smart notifications (to Slack, email, Teams)

**Technical Implementation:**
- APScheduler for background job scheduling
- Anomaly detection: isolation forest or 3-sigma rule for metric outliers
- Predictive model: ARIMA or Prophet for time-series forecasting
- Workflow engine: Airflow or custom state machine for automation

#### Tab 11: Audit & Compliance (15 hrs)
**Purpose:** Full audit trail, compliance reporting, SOX 404 controls, data lineage

**Components:**
- Audit trail (all data modifications, who, when, what changed)
- Compliance report (regulatory findings, control testing)
- Data lineage (source → transformation → dashboard)
- Forecast accuracy tracking (vs actual outcomes)
- Decision audit (all governance decisions, rationale, approvers)
- QBR brief generation (auto-generated from dashboard data)
- Audit package export (all supporting data for external audit)

**Data Sources:**
- Audit trail table (audit_id, table, record_id, action, old_value, new_value, user_id, timestamp)
- Compliance control matrix

### Backend Enhancements (Phase 3)

**Predictive Engine:**
- Forecast programme completion date (Earned Value-based + risk adjustment)
- Forecast margin at completion (ETC-based, accounting for bench cost and CR pipeline)
- Identify programmes at risk of margin cliff (probability and timeline)
- Predict defect escapes (based on defect density trend + coverage %)
- Predict attrition risk (based on team turnover indicators)

**Data Connectors (Phase 3+):**
- Jira/ADO connector: Sync story points, sprint velocity, defect tracking
- Slack integration: Smart notifications, workflow alerts
- Teams integration: Embed dashboard widgets, send digest
- Salesforce connector: Sync customer health, renewals, upsell pipeline

### Questions Answered by v5.2-release

**AI Governance (3 questions):**
51. What is the AI trust score by augmentation? (Tab 6)
52. What is the cost-benefit ratio of each AI augmentation? (Tab 6)
53. Which programmes are ready for AI augmentation expansion? (Tab 6 recommendation engine)

**Smart Ops & Automation (3 questions):**
54. What anomalies were detected in portfolio metrics this week? (Tab 7)
55. What actions should we take based on predictive forecasts? (Tab 7 recommendation engine)
56. Are there any overdue RAID items that need escalation? (Tab 7 auto-escalation)

**Audit & Compliance (3 questions):**
57. What is our forecast accuracy vs actual for the past 6 months? (Tab 11)
58. Generate an audit-ready QBR brief for stakeholders. (Tab 11 auto-generate)
59. What is the data lineage for margin % calculation? (Tab 11 lineage)

**Enhanced Questions from Prior Phases (consolidation):**
All 42 questions from v5.1-beta are enhanced with:
- Predictive dimensions (not just current state)
- Auto-generated recommendations (not just data)
- Audit trail visibility (not just metrics)

**Total Questions Answered by v5.2-release: 50 of 50**

---

## Phase 4+: v6.0+ — Enterprise SaaS Platform

**Timeline:** 2026-Q4 onwards (future roadmap)

**Scope:**
- Multi-tenant architecture
- PostgreSQL migration (from SQLite)
- User authentication & RBAC (Auth0 or Okta)
- Jira/ADO connectors
- Slack/Teams integrations
- Gantt chart (full timeline visualization)
- PWA (Progressive Web App) for mobile
- API versioning & SDK
- Data marketplace (export to BI tools: Tableau, Power BI)

---

## Build Effort Breakdown

| Phase | Tab Work | Backend | Testing | Docs | Total |
|-------|----------|---------|---------|------|-------|
| v5.0-alpha | 45 hrs | 30 hrs | 8 hrs | 5 hrs | 55 hrs |
| v5.1-beta | 35 hrs | 35 hrs | 10 hrs | 5 hrs | 60 hrs |
| v5.2-release | 40 hrs | 40 hrs | 15 hrs | 10 hrs | 75 hrs |
| **Total to Release** | **120 hrs** | **105 hrs** | **33 hrs** | **20 hrs** | **190 hrs** |

**Assuming 3 engineers at 60% allocation (2 full-time equivalent):**
- v5.0-alpha: 4 weeks (end of April 2026)
- v5.1-beta: 4 weeks (end of May 2026)
- v5.2-release: 5 weeks (end of June 2026)
- **Total to production-ready: 13 weeks (~3 months)**

---

## Risk Mitigation & Success Criteria

### v5.0-alpha Release Criteria
- [ ] All 5 tabs render without errors
- [ ] 30 of 58 CTO questions answered (validated)
- [ ] NovaTech demo data loads in <2 seconds
- [ ] Executive can discover top 3 portfolio issues in <5 minutes
- [ ] All EVM calculations accurate to ±₹50k
- [ ] API response times <500ms for dashboard load

### v5.1-beta Release Criteria
- [ ] Tabs 3, 5, 10 fully functional
- [ ] 52 of 58 CTO questions answered
- [ ] Risk governance workflows operationalized (CR submission to approval)
- [ ] Forecast accuracy model validated against historical data
- [ ] Change request scenario modelling produces consistent results

### v5.2-release (Production) Criteria
- [ ] All 58 CTO questions answered
- [ ] All 45 formulas implemented with 2 worked examples each
- [ ] 42 database tables operational
- [ ] 15 CSV/Excel templates importable
- [ ] 11 tabs rendering correctly across Chrome, Firefox, Safari, Edge
- [ ] Scrum, Kanban, Waterfall, SAFe, Hybrid methodology smoke tests pass
- [ ] Multi-currency aggregation tested with 3+ currencies
- [ ] Fiscal year config tested (Apr–Mar, Jan–Dec, Oct–Sep)
- [ ] WCAG 2.1 AA audit pass (axe-core zero critical violations)
- [ ] Predictive engine forecasts with 85%+ accuracy
- [ ] QBR brief auto-generation produces executive-ready output
- [ ] Audit trail captures all governance decisions
- [ ] Cold-start repro: fresh clone → dashboard in <3 minutes
- [ ] Cross-platform tested: Windows (Docker Desktop + WSL2), macOS, Linux

---

## Known Dependencies & Constraints

1. **Demo Data Accuracy:** NovaTech Solutions profile must reflect realistic IT services delivery patterns. Validation against real case studies recommended.
2. **Forecast Engine Validation:** ARIMA/Prophet models require >6 months of historical data for production use. v5.2-release will use 3-month baseline from demo.
3. **Integration Readiness:** Jira/ADO connectors deferred to v6.0+. v5.2-release is manual data entry / CSV import only.
4. **Scalability Limits:** SQLite is suitable for <10k records (demo scale). PostgreSQL migration required for >100 programmes or >1 year history.

---

## Success Metrics & Adoption

**Post-Release Metrics:**

1. **Adoption:** Number of IT services organizations deploying v5.0–v5.2 (target: 3–5 reference customers)
2. **Portfolio Visibility:** Average time to identify top 3 portfolio risks (target: <5 minutes)
3. **Governance Velocity:** Time from CR submission to approval decision (target: <2 days)
4. **Margin Impact:** Customers reporting margin improvement from insights (target: avg +2–3 percentage points)
5. **Forecast Accuracy:** Variance between forecasted and actual outcomes (target: <10%)

---

**End of Roadmap — v5.2**

For the full 7-phase production SDLC with bug-fix discipline: see [`PRODUCTION_SDLC.md`](PRODUCTION_SDLC.md).
For the pre-release verification register: see [`MASTER_CHECKLIST.md`](MASTER_CHECKLIST.md).

For questions, contact Adi Kompalli (AKB1 Framework).
