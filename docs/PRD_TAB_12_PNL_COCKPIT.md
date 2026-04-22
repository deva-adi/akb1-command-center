# PRD, Tab 12 P&L Cockpit, AKB1 Command Center v5.3

**Document ID:** PRD-T12-PNL-COCKPIT
**Version:** 1.0
**Status:** Locked for Claude Code execution
**Author:** Adi Kompalli
**Date:** 2026-04-22
**Target release:** v5.3 (Iteration 2 delta on top of v5.2)
**Repo:** github.com/deva-adi/akb1-command-center
**Decision record:** Balanced scope, option two, as selected on 2026-04-22. Strategic scope (option three) is a separate ROADMAP entry for v6.

---

## 1. Purpose

Close the commercial blind spot in v5.2. The dashboard today shows margin mechanisms (waterfall, seven losses, rate card drift) but does not answer the five commercial questions a CFO or AD asks in the first five minutes of a steering conversation: where is revenue, where is it billed, where is cash, why did margin move month over month, and what are the top levers to recover it. Tab 12 adds that cockpit as a single screen, powered by the existing seeded data plus a small set of deterministic derivations so the demo is internally consistent.

This PRD is the single source of truth Claude Code executes against. Claude Code must implement from this PRD, not redesign. If any conflict emerges between this PRD and ARCHITECTURE.md, FORMULAS.md, or WIREFRAMES.md, stop and raise the conflict before coding.

---

## 2. Context

| Item | State before Tab 12 |
|---|---|
| Live tabs | Eight of eleven tabs live (Executive, KPI Studio, Delivery, Velocity and Flow, Margin and EVM, Customer Intelligence, Smart Ops, Reports, Data Hub) |
| Stubbed tabs | AI Governance (07), Risk and Audit (09) |
| Existing margin depth | Four layer margin waterfall, seven delivery losses, rate card drift, template narrative on Executive tab |
| Existing revenue depth | Revenue Realised card only, no decomposition, no bridge, no cash |
| Existing data sources | Fifteen CSV templates, `financials.csv` has planned_revenue, actual_revenue, planned_cost, actual_cost, four margin percentages, scenario names (Monthly Actuals, Forecast at Completion) |
| Demo dataset | NovaTech Solutions, six programmes (PHOENIX, ATLAS, SENTINEL, ORION, TITAN, HERCULES), twelve months, April 2025 to March 2026 |
| Base currency | USD, FY 2025 to 26 (April to March), Industry preset IT Services |
| FX engine | frankfurter.app refresh, four currencies stored (EUR, GBP, INR, USD) |
| Documentation locked | 2061 lines in ARCHITECTURE.md, 1490 lines in FORMULAS.md, 588 lines in ROADMAP.md |

---

## 3. Scope, balanced option two, explicit

In scope for this PRD.

Seven sections on the new tab as specified in section six. KPI Board, Margin Bridge, Plan Forecast Actual triangle, Seven Losses with revenue attribution, Pyramid Economics with Realisation Rate, Commercial Levers panel, LLM narrative block. Drill-down and drill-up paths as specified in section eight. Backend API endpoints as specified in section ten. Frontend route at `/pnl` as specified in section eleven. Data seeds for six programmes across twelve months as specified in section nine. FORMULAS.md additions as definitions fifty through fifty-five per section seven.

Out of scope for this PRD, deferred to v6 Iteration 3.

A dedicated invoices table. A dedicated collections ledger. An accounts receivable subledger with aging buckets. A change request register with priced versus absorbed analytics. A contractual SLA credit schedule with penalty cap exposure. A revenue recognition engine (percentage of completion, milestone, subscription, T and M split). A full FX sensitivity view. These features are acknowledged in ROADMAP.md and must not be built in this iteration.

---

## 4. Non-goals

One, do not redesign the existing Margin and EVM tab. Tab 12 reuses its numbers and adds commercial framing, it does not replace the waterfall or the seven-loss bar chart.

Two, do not merge Risk and Audit into Smart Ops in this iteration. That is a v6 decision and is out of scope.

Three, do not promise CFO-grade financial accuracy in v5.3. Simulated fields (billed_revenue, collected_revenue, unbilled_wip, ar_balance) must carry a visible "Simulated from actuals for demo" disclaimer when Data Hub `Demo mode = true`.

Four, do not change the seed dataset numbers already published (planned_revenue, actual_revenue, planned_cost, actual_cost). Seed deltas in section nine are additive only. Existing views must continue to render identical numbers.

Five, do not change base currency handling. The tab respects the existing base-currency selector and FX rate source (`frankfurter`).

---

## 5. Navigation decision

Append as tab 12. Do not renumber existing tabs.

Rationale: existing routes, wireframes, tests, report types, audit ZIP names, and the WIREFRAMES.md layout all reference the current numbering. Appending is a zero-breakage change. The existing stubs at 07 (AI Governance) and 09 (Risk and Audit) remain, their placeholder page is unchanged.

Side nav order after this change: `01 Executive`, `02 KPI Studio`, `03 Delivery`, `04 Velocity and Flow`, `05 Margin and EVM`, `06 Customer Intelligence`, `07 AI Governance`, `08 Smart Ops`, `09 Risk and Audit`, `10 Reports and Exports`, `11 Data Hub`, `12 P&L Cockpit`.

Route: `/pnl`. Nav label: `P&L Cockpit`. Nav number: `12`.

---

## 6. Tab 12 specification, seven sections

### Section one, KPI Board

Ten cards in a three by four grid (three columns, four rows with the last row holding two cards). Each card shows the KPI name, current value, trend arrow, click-to-drill affordance, and a threshold indicator badge (green, amber, red).

| Card | Formula | Seeded example, Phoenix 2026-03 | Green | Red |
|---|---|---|---|---|
| Committed revenue | Sum of contracted revenue for period | planned_revenue 850K | reference only | n/a |
| Booked revenue | Signed orders in period | actual_revenue 820K | reference only | n/a |
| Billed revenue | `Billed = actual_revenue * billing_ratio` with `billing_ratio = 0.95` default | 820 times 0.95 equals 779K | at or above 95 percent of booked | below 85 percent |
| Collected revenue | `Collected = billed * collection_ratio` with `collection_ratio = 0.88` default | 779 times 0.88 equals 686K | at or above 90 percent of billed | below 80 percent |
| Unbilled WIP | `Unbilled = max(actual_revenue minus billed, 0)` plus residual estimate | 820 minus 779 equals 41K | under five percent of booked | above ten percent |
| DSO, days sales outstanding | `DSO = (AR balance / Billed revenue) times 30` where `AR balance = billed minus collected` | (93 / 779) times 30 equals 3.6 days (demo tight) | under 45 days | above 75 days |
| Gross margin percent | (Actual revenue minus actual cost) / Actual revenue | (820 minus 590) / 820 equals 28.0 percent | at or above 30 percent | below 22 percent |
| Contribution margin percent | From `financials.csv` | 12.5 percent | at or above 18 percent | below 10 percent |
| Portfolio margin percent | Sum of gross profits / Sum of revenues across programmes | 17.3 percent current | at or above 22 percent | below 15 percent |
| Net margin percent | From `financials.csv` | 4.1 percent | at or above 10 percent | below 5 percent |

Cards must carry an information icon that opens a modal with the formula and the two worked examples from FORMULAS.md. Every card is clickable and routes per section eight.

### Section two, Margin Bridge

Single waterfall chart showing month over month margin change decomposed into four drivers: Price, Volume, Mix, Cost. Three bridge views available via a toggle: current month versus prior month, current month versus plan, YTD actual versus plan.

Decomposition formulas.

`Price delta bps = ((rate_actual minus rate_prior) / rate_prior) times (hours_prior / revenue_prior) times 10000`

`Volume delta bps = ((hours_actual minus hours_prior) / hours_prior) times (rate_prior / revenue_prior) times 10000`

`Mix delta bps = sum over tiers of ((tier_weight_actual minus tier_weight_prior) times (tier_rate minus portfolio_rate_prior) / revenue_prior) times 10000`

`Cost delta bps = ((cost_actual minus cost_prior) / revenue_prior) times 10000 minus (price_delta_bps plus volume_delta_bps plus mix_delta_bps)`

The residual lands in the Cost bucket so the bridge always ties out exactly. Each bar is clickable, drills into the underlying programme and tier.

Worked example one, Phoenix February to March bridge.

Prior month gross margin 31.4 percent, current month 28.0 percent, delta minus 340 basis points.

Price bucket: Mid Engineer rate drift planned 110 to actual 118, roughly 7.3 percent on Mid Engineer component, estimated impact minus 180 basis points on blended margin. Volume bucket: billable hours compressed, estimated minus 90 basis points. Mix bucket: Junior to Mid shift worsens pyramid, minus 40 basis points. Cost bucket: residual, minus 30 basis points (tooling and variable overhead). Total ties to minus 340.

Worked example two, Atlas February to March bridge.

Prior 42.1 percent, current 39.8 percent, delta minus 230 basis points. Price minus 210 basis points (Mid Engineer rate drift fifteen percent), Volume plus 20 basis points, Mix minus 30 basis points, Cost minus 10 basis points. Ties to minus 230.

### Section three, Plan Forecast Actual triangle

Three-line trend chart per metric. Metrics selectable from a dropdown: Revenue, Gross margin percent, Net margin percent, CPI, SPI.

Lines: Plan (from planned_revenue and planned_cost), Forecast (from `scenario_name = Forecast at Completion` rows in `financials.csv`, extended month by month), Actual (from `scenario_name = Monthly Actuals`).

Worked example, Orion Data Platform. Plan revenue 5.1M at margin 18.0 percent. Forecast at completion revenue 5.05M at margin 13.8 percent. YTD actual revenue 415K at March at margin 24.1 percent. Triangle shows YTD actual looking healthy but forecast diverging downward, which is the margin cliff already flagged in Smart Ops. Clicking the forecast line routes to Smart Ops with the Margin Cliff Projected alert preselected.

### Section four, Seven Losses with revenue attribution

Extends the existing seven-loss bar on the Margin tab. Each loss category now also shows revenue foregone and margin-points lost, not only dollar loss.

Formulas.

`Revenue foregone = loss_amount / (1 minus target_margin_pct)` with target 30 percent gross.

`Margin points lost = loss_amount / portfolio_revenue times 10000`

Worked example, Phoenix Bench Tax 765K at target 30 percent. Revenue foregone equals 765 divided by 0.70 equals 1093K. That is the revenue the commercial team would have needed to book at target margin to absorb the bench cost. Margin points lost on Phoenix revenue of 820K is 765 divided by 820 times 10000 equals 9329 basis points of programme-level margin compression (a programme-level view). At portfolio level on revenue 540K YTD, 765 divided by 2954K (estimated FY revenue run rate) equals 259 basis points.

Each category row is clickable, drills to the underlying programme and to Smart Ops for any matching active alert.

### Section five, Pyramid Economics and Realisation Rate

Three sub-cards.

Sub-card one, Pyramid Ratio. Shows Jr count to Mid count to Sr count, with target ratio from settings. Heat highlights deviation.

`Pyramid Ratio = Jr_count : Mid_count : Sr_count` with target in settings, default 30:50:20.

Worked example. Phoenix seeded team composition from resources pool filtered to `current_program_code = PHOENIX`: three Junior (assumed), two Mid, one Senior, ratio 50:33:17. Senior-heavy against target, explains the 22.3 percent gross margin compression. Amber.

Sub-card two, Realisation Rate.

`Realisation = hours_billed / hours_worked`

Worked example. Phoenix team worked 1200 hours in March and billed 1150, realisation 95.8 percent. Leakage 4.2 percent equates to 50 hours times blended rate 85 USD equals 4250 USD foregone in March on Phoenix.

Sub-card three, Utilisation by tier.

`Utilisation_tier = sum(billable_hours_tier) / sum(available_hours_tier)`

Worked example. Seeded resources: Senior tier (Priya, Rajesh, Deepak, Suresh, Nisha) average 88 percent utilisation. Mid tier (Kavya, Rohit, Mehul) average 85 percent. Junior tier (Vikram Rao, Ananya Desai) both on bench, zero percent. Red flag surfaced here: Juniors on bench while Seniors over-utilised, classic pyramid inversion that kills margin even when rates hold.

### Section six, Commercial Levers panel

Ranked list of the top five margin recovery levers across the portfolio, computed every render. Each row shows: lever name, programme, mechanism, estimated impact in basis points, owner from seed data, action window.

Scoring algorithm.

`Lever score = estimated_bps_impact times feasibility_weight` with feasibility default 1.0 for mechanisms inside delivery control, 0.7 for mechanisms requiring customer, 0.5 for mechanisms requiring legal or contractual change.

Sample top five for NovaTech at 2026-03 close.

| Lever | Programme | Mechanism | Estimated impact | Owner | Window |
|---|---|---|---|---|---|
| Reprice three open CRs | PHOENIX | Close scope absorption by repricing | plus 120 bps on PHOENIX margin | Priya Sharma | Two weeks |
| Rebalance pyramid | SENTINEL | Swap two Sr for two Mid, keep Jr steady | plus 180 bps on SENTINEL margin | Raj Kumar | One quarter |
| Redeploy bench | PORTFOLIO | Move Vikram Rao and Ananya Desai onto billable | 28K annualised saving | Suresh Menon | Two weeks |
| Invoke rate indexation | ORION | Trigger WPI-indexed rate escalation per contract | plus 90 bps | Commercial lead | Sixty days |
| Close rate drift | ATLAS | Enforce Mid Engineer rate at 100, not 115 | plus 150 bps on ATLAS margin | Gaurav Mehta | Thirty days |

Each row opens a modal with the full math, the affected records, and the recommended communication template.

### Section seven, LLM narrative block

Single paragraph, auto-generated from the sections above. Uses the existing template-driven narrative generator from the Executive tab, upgraded to pull from the P&L data shape. Must be deterministic in v5.3 (no LLM call yet), template-driven with variable substitution, to keep demo output stable.

Template.

`Portfolio gross margin sits at {portfolio_gross} percent, {gap_bps} basis points {above|below} the {target_floor} percent floor. {worst_programme} is the largest drag (gross {worst_margin} percent, down {worst_delta_bps} bps month over month, {worst_driver} driven on {worst_driver_detail}). {forecast_risk_programme} is the forward-looking risk (YTD {ytd_margin} percent, forecast at completion {fac_margin} percent, margin cliff in month {cliff_month}). {top_levers_count} levers with combined {combined_bps} bps impact are available this quarter: {lever_list}.`

Sample output at 2026-03 close.

`Portfolio gross margin sits at 17.3 percent, 470 basis points below the 22 percent floor. Phoenix is the largest drag (gross 22 percent, down 340 bps month over month, price driven on mid engineer rate). Orion is the forward-looking risk (YTD 24.1 percent, forecast at completion 13.8 percent, margin cliff in month eight). Three levers with combined 390 bps impact are available this quarter: reprice Phoenix CRs, rebalance Sentinel pyramid, close Atlas rate drift.`

---

## 7. FORMULAS.md additions, definitions fifty through fifty-five

Append to FORMULAS.md in the same format as existing definitions. Each definition must carry two worked examples and a dashboard location.

Definition fifty, Margin Bridge Price Delta.
Definition fifty-one, Margin Bridge Volume Delta.
Definition fifty-two, Margin Bridge Mix Delta.
Definition fifty-three, Margin Bridge Cost Delta (residual).
Definition fifty-four, DSO and AR balance.
Definition fifty-five, Pyramid Ratio deviation from target.

Realisation Rate and Revenue Leakage already exist in FORMULAS.md, reuse them, do not duplicate.

---

## 8. Drill logic

Drill-down paths.

| From | To | Trigger |
|---|---|---|
| KPI Board card (portfolio) | Programme breakdown table inside the same tab | Click card |
| KPI Board card (programme level) | Monthly time series inline | Click card |
| Margin Bridge bar | Programme and tier detail modal with underlying rows | Click bar |
| PFA line (forecast) | Smart Ops, Margin Cliff Projected alert for that programme | Click line point |
| Seven Losses row | Programme detail on Margin and EVM | Click row |
| Pyramid card | Smart Ops resource pool filtered to programme | Click card |
| Realisation card | Delivery Health tab for programme | Click card |
| Commercial Lever row | Modal with full math, affected records, communication template | Click row |

Drill-up paths, new across the app. Add a right-rail context panel that follows the user when a programme is in focus. Panel shows three buttons.

`To Executive narrative for this programme` (highlights the matching sentence on Executive tab), `To Margin and EVM waterfall for this programme` (preselected), `To Customer Intelligence for this programme` (preselected). The right rail renders only when a programme is selected, and it is implemented once for all tabs, not only the P&L cockpit, so the drill-up works everywhere.

Cross-tab Director chain. One click each: Executive narrative, P&L Cockpit, Margin and EVM, Delivery Health, Velocity blend gates. Five clicks end to end, CPI to cash.

---

## 9. Seed data, NovaTech deltas

Two update paths, choose both.

### 9.1 Extend `financials.csv`

Add five new columns. Do not remove existing columns.

`billed_revenue, collected_revenue, unbilled_wip, ar_balance, billing_ratio`

Deterministic derivations for the demo. For every existing row apply.

`billing_ratio = 0.95 default, 0.88 for PHOENIX and ORION (lagging programmes), 0.97 for ATLAS and SENTINEL (healthy programmes)`

`billed_revenue = round(actual_revenue * billing_ratio, 0)`

`collected_revenue = round(billed_revenue * 0.88, 0)` default, `0.92 for ATLAS and SENTINEL`, `0.80 for PHOENIX and ORION`

`unbilled_wip = max(actual_revenue minus billed_revenue, 0)`

`ar_balance = billed_revenue minus collected_revenue`

Claude Code must regenerate all twelve months for all six programmes using these rules, output exactly the same row count as the existing file, and produce a diff that shows additions only. Commit message: `feat(seed): extend financials with billing and cash columns for P&L tab 12`.

### 9.2 New CSV, `programme_rates.csv`

For the pyramid and rate-drift math to compute cleanly, add a per-programme, per-tier rate card snapshot (two snapshots: planned and actual, per programme, per month).

Columns.

`program_code, snapshot_date, role_tier, planned_rate, actual_rate, planned_headcount, actual_headcount, tier_weight_planned, tier_weight_actual`

Seed rows, six programmes times three tiers (Junior, Mid, Senior) times twelve months equals 216 rows. Values must be consistent with the existing `Rate-card drift` table visible on the Margin and EVM page (planned vs actual rates already shown there) and with `resources.csv`.

Representative baseline row set for PHOENIX.

```
PHOENIX,2026-03-01,Junior,70,72,3,3,0.30,0.50
PHOENIX,2026-03-01,Mid,110,118,2,2,0.50,0.33
PHOENIX,2026-03-01,Senior,180,175,1,1,0.20,0.17
```

Repeat pattern for ATLAS, SENTINEL, ORION, TITAN, HERCULES with programme-specific drift as per the Rate-card drift table already rendered at `http://localhost:9000/margin`. Claude Code must regenerate the 216 rows using the same drift semantics.

### 9.3 Existing files, no changes

`losses.csv`, `resources.csv`, `bench.csv`, `change_requests.csv`, `ai_tools.csv`, `ai_metrics.csv`, `flow_metrics.csv`, `evm_monthly.csv`, `kpi_monthly.csv`, `programmes.csv`, `projects.csv`, `sprints.csv`, `risks.csv`, `project_phases.csv` remain unchanged.

---

## 10. Backend, API additions

All new endpoints live under `/api/v1/pnl/`. Versioned. JSON responses. Follow existing FastAPI conventions in `backend/app/api/`.

| Method | Path | Returns |
|---|---|---|
| GET | `/api/v1/pnl/board/{scope}` | KPI Board data, scope in {portfolio, programme}. Programme takes `?programme=PHOENIX` |
| GET | `/api/v1/pnl/bridge/{programme}/{period}` | Margin Bridge with four drivers, period in {mom, vs_plan, ytd_vs_plan} |
| GET | `/api/v1/pnl/pfa/{programme}` | PFA triangle series per metric, query param `metric` in {revenue, gross_pct, net_pct, cpi, spi} |
| GET | `/api/v1/pnl/losses_with_attribution` | Seven-loss list extended with revenue foregone and margin points lost |
| GET | `/api/v1/pnl/pyramid/{programme}` | Pyramid ratio, realisation, utilisation per tier |
| GET | `/api/v1/pnl/levers` | Top five levers with mechanism, impact, owner, window |
| GET | `/api/v1/pnl/narrative` | Template-substituted paragraph, deterministic |
| GET | `/api/v1/pnl/narrative?llm=true` | Reserved for v6 Iteration 3. In v5.3 must return HTTP 501 with message `LLM narrative scheduled for v6 Iteration 3` |

Contract tests live under `backend/tests/api/test_pnl_*.py`. Minimum seven contract tests, one per endpoint. Response schemas documented in OpenAPI, auto-generated.

---

## 11. Frontend, component plan

New route `/pnl` mounted in `frontend/src/routes/` per existing convention. New files.

```
frontend/src/routes/pnl/index.jsx                    # Tab entry
frontend/src/routes/pnl/sections/KpiBoard.jsx
frontend/src/routes/pnl/sections/MarginBridge.jsx
frontend/src/routes/pnl/sections/PfaTriangle.jsx
frontend/src/routes/pnl/sections/LossesAttribution.jsx
frontend/src/routes/pnl/sections/Pyramid.jsx
frontend/src/routes/pnl/sections/LeversPanel.jsx
frontend/src/routes/pnl/sections/NarrativeBlock.jsx
frontend/src/components/common/ContextRail.jsx       # New right-rail drill-up component, shared across tabs
frontend/src/lib/pnlApi.js                           # Data fetchers
```

Reuse existing primitives: `KpiCard`, `WaterfallChart` from `frontend/src/components/charts/`, `DataTable` from `frontend/src/components/common/`, `InfoModal` from `frontend/src/components/common/`. Recharts for KPI trends, ECharts where the Margin and EVM tab uses it for consistency.

Side nav entry appended to the existing nav config at `frontend/src/config/nav.js` (or equivalent file Claude Code finds during discovery). Must match numbering convention and route.

Dark mode support required, same Tailwind theme tokens as Executive tab.

---

## 12. ContextRail, the drill-up component

Shared right-rail component added in this iteration. Mounted globally. Renders only when a programme selection is active in the route state.

Props.

```
<ContextRail
  programme={selected}
  links={[
    { label: "To Executive narrative", to: `/?programme=${selected}#narrative` },
    { label: "To Margin and EVM",      to: `/margin?programme=${selected}` },
    { label: "To Customer Intelligence", to: `/customer?programme=${selected}` }
  ]}
/>
```

Store programme selection in a URL query param so the drill-up is deep-linkable. This is an explicit dependency for Tab 12 acceptance, since drill-up is listed as a documented gap in v5.2.

---

## 13. Documentation updates required

Every doc touched here must be updated as part of the same PR, not a later PR. Keeping docs in sync is a hard gate.

| File | Change |
|---|---|
| `docs/ARCHITECTURE.md` | Add section 6.14 P&L Cockpit. Reference Tab 12 route, seven sections, simulated-field disclaimer |
| `docs/WIREFRAMES.md` | Add Tab 12 wireframe mirroring the seven-section layout |
| `docs/FORMULAS.md` | Append definitions 50 through 55 with two worked examples each |
| `docs/ROADMAP.md` | Iteration 2 closes with Tab 12, Iteration 3 opens with commercial backbone (invoices table, collections ledger, AR subledger, CR register, SLA credit, revenue recognition, FX sensitivity). Do not delete existing entries, add only |
| `docs/DEMO_GUIDE.md` | Add Tab 12 walkthrough to NovaTech demo script |
| `docs/MASTER_CHECKLIST.md` | Add Tab 12 build gate rows to section G (UI) and section H (API) |
| `docs/CTO_QUESTIONS.md` | Add five new CTO questions covered by Tab 12 (below) |
| `README.md` | Update tab count from 11 to 12, update version to v5.3 |

Five new CTO questions to add to CTO_QUESTIONS.md.

1. Where is revenue leaking, and how much would we have to book to recover it at target margin?
2. What drove the month over month margin move, price, volume, mix, or cost?
3. Is the pyramid inverted on any programme, and what is the margin impact?
4. What are the top five margin levers across the portfolio, ranked by feasibility-weighted impact?
5. For any programme, what is the single next step a Director should take this week to recover margin?

---

## 14. Acceptance criteria, per section

Every acceptance criterion must pass before the PR is mergeable. Run by Claude Code against the NovaTech seed after the build.

Section one, KPI Board.

Cards render all ten KPIs. Threshold colour matches the green and red rules in section six table one. Every card clickable. Info icon opens modal with formula and two worked examples. In Demo mode, cards for billed, collected, unbilled_wip, DSO carry a small "Simulated" pill.

Section two, Margin Bridge.

For Phoenix Feb to Mar the bridge ties to minus 340 basis points (plus or minus five basis points rounding). For Atlas Feb to Mar the bridge ties to minus 230 basis points. Cost bucket is the residual, all four bars always sum to the total delta exactly.

Section three, PFA triangle.

Dropdown renders five metrics. Orion forecast line diverges below YTD actual. Clicking a forecast point routes to Smart Ops with the Margin Cliff Projected alert preselected.

Section four, Seven Losses attribution.

Phoenix Bench Tax row shows loss 765K, revenue foregone 1093K, margin points lost both at programme level and portfolio level. Sort toggles work for dollars and for basis points.

Section five, Pyramid and Realisation.

Phoenix card renders ratio 50:33:17 with amber colour. Seniors show utilisation 88 percent, Juniors show zero. Realisation card shows 95.8 percent for Phoenix March.

Section six, Commercial Levers.

Top five levers rendered with owner names drawn from `resources.csv`. Each modal opens with formula breakdown and a plaintext communication template.

Section seven, Narrative.

Paragraph renders with all seven variables substituted. Deterministic, no LLM call, same input produces same output.

ContextRail.

Appears on Executive, Margin and EVM, Customer, Delivery Health, and P&L Cockpit when a programme is selected. Links are URL-driven and deep-linkable.

---

## 15. Verification protocol

Claude Code must execute this sequence after implementation and before opening the PR.

Step one, run backend unit and contract tests: `pytest backend/tests/ -v`. All pass.

Step two, run frontend linter and tests: `npm --prefix frontend run lint && npm --prefix frontend test`. All pass.

Step three, bring the app up via docker-compose and hit each of the seven new endpoints with `curl` or equivalent. Response shapes match the OpenAPI spec.

Step four, open the app at `http://localhost:9000/pnl`, verify all seven sections render, every acceptance criterion in section fourteen passes.

Step five, run each drill-down and drill-up route manually. Every link must land on the correct tab with the correct programme preselected.

Step six, take four screenshots: full Tab 12 top, Margin Bridge zoomed, Pyramid section zoomed, Commercial Levers modal open. Save under `docs/screenshots/tab-12-pnl-cockpit/` and reference them in `DEMO_GUIDE.md`.

Step seven, generate a verification note at `docs/VERIFICATION_REPORT_TAB_12.md` listing every acceptance criterion with pass or fail and the command that proved it.

---

## 16. Commit convention and PR plan

Branch: `feat/tab-12-pnl-cockpit`.

Commit convention, conventional commits, one commit per logical unit. Use these scopes.

```
feat(seed): extend financials with billing and cash columns
feat(seed): add programme_rates.csv with planned vs actual per tier per month
feat(backend): add /api/v1/pnl/board endpoint
feat(backend): add /api/v1/pnl/bridge endpoint
feat(backend): add /api/v1/pnl/pfa endpoint
feat(backend): add /api/v1/pnl/losses_with_attribution endpoint
feat(backend): add /api/v1/pnl/pyramid endpoint
feat(backend): add /api/v1/pnl/levers endpoint
feat(backend): add /api/v1/pnl/narrative endpoint
feat(frontend): scaffold /pnl route and Tab 12 entry
feat(frontend): add KpiBoard section for P&L Cockpit
feat(frontend): add MarginBridge section
feat(frontend): add PfaTriangle section
feat(frontend): add LossesAttribution section
feat(frontend): add Pyramid section
feat(frontend): add LeversPanel section
feat(frontend): add NarrativeBlock section
feat(frontend): add ContextRail global drill-up component
docs: add PRD_TAB_12_PNL_COCKPIT.md
docs: update ARCHITECTURE.md section 6.14 for P&L Cockpit
docs: update WIREFRAMES.md with Tab 12 wireframe
docs: append definitions 50-55 to FORMULAS.md
docs: add Tab 12 entries to MASTER_CHECKLIST.md
docs: append Tab 12 walkthrough to DEMO_GUIDE.md
docs: add 5 new CTO questions to CTO_QUESTIONS.md
docs: update ROADMAP.md Iteration 2 close, Iteration 3 open
docs: bump README.md tab count and version
test(backend): contract tests for 7 P&L endpoints
test(frontend): component tests for 7 P&L sections
chore: bump frontend package.json version to 5.3.0
chore: bump backend pyproject.toml version to 5.3.0
```

PR title: `feat: Tab 12 P&L Cockpit (v5.3, Iteration 2 close)`.

PR description must reference this PRD, list acceptance criteria results, and link the four screenshots.

Tag after merge: `v5.3.0`.

---

## 17. Risk register for the build

| Risk | Severity | Mitigation |
|---|---|---|
| Simulated fields leak into a non-demo deployment and mislead a real user | High | Render a visible "Simulated from actuals for demo" pill on every simulated card whenever `Demo mode = true`. Block render of simulated fields when `Demo mode = false` unless real data is present |
| Navigation changes break deep links or QBR PDF routes | Medium | Append only, no renumbering. Run existing E2E tests before merge |
| Schema change on `financials.csv` breaks existing importers | Medium | Additive columns only, importers default missing columns to null and derive using the same ratios |
| ContextRail introduces regressions on other tabs | Medium | Feature flag the rail, default on, off behaviour verified in E2E |
| FX rendering drift between tabs | Low | All currency conversion goes through the existing `currency_rates` service, no per-tab conversion |
| Narrative template becomes stale as KPIs shift | Low | Variables live in one place, unit tested against the NovaTech fixture |

---

## 18. Failure modes to watch

One, the Margin Bridge math does not tie out to the headline delta. Fix: always compute Cost as the residual so the four drivers sum to the total by construction. Covered by unit test.

Two, the PFA triangle shows Forecast equal to Actual. Fix: load the `Forecast at Completion` scenario rows specifically, fall back to weighted MA only if that scenario is absent.

Three, the Commercial Levers panel shows zero rows. Fix: if fewer than five real levers are computable, pad with the highest-impact loss categories reframed as levers so the panel always renders five rows.

Four, the Pyramid card looks fine while Juniors are on bench. Fix: utilisation filter must include zero-util resources in the tier denominator, do not silently drop them.

Five, the narrative paragraph reads robotic. Fix acceptable in v5.3, the point is determinism. v6 Iteration 3 upgrades to LLM when allowed.

---

## 19. Out of scope reminders

Do not touch existing tabs, except for the ContextRail mount-point (which is additive).

Do not change the base currency behaviour.

Do not add a Risk and Audit merge into Smart Ops in this iteration.

Do not call out to any external LLM. Narrative is deterministic in v5.3.

Do not add authentication or permissions changes. Security posture remains Tier 1 per SECURITY_GUIDE.md.

---

## 20. Paste-ready Claude Code session prompt

Use the block below as the first message in a new Claude Code session opened at `~/Documents/Claude/Claude_Code/Projects/akb1-command-center`. It primes Claude Code with everything needed to execute this PRD end to end.

---

```
You are building AKB1 Command Center v5.3, Iteration 2 close, Tab 12 P&L Cockpit. The entire spec is locked at docs/PRD_TAB_12_PNL_COCKPIT.md. Your job is to implement from that PRD and the existing ARCHITECTURE.md, FORMULAS.md, WIREFRAMES.md, MASTER_CHECKLIST.md, SECURITY_GUIDE.md. Do not redesign. If any conflict appears between this PRD and the existing locked docs, stop, surface the conflict, and wait for my instruction.

WHO I AM
Adi Kompalli, Senior Delivery and Program Manager, Hyderabad India. Repo github.com/deva-adi/akb1-command-center. User deva-adi. Email deva.adi@gmail.com.

CONTEXT
v5.2 is live at localhost:9000 with eight tabs live and two stubs. v5.3 adds one tab (Tab 12 P&L Cockpit) and a shared ContextRail drill-up component. Seeds extend financials.csv and add programme_rates.csv, deterministic derivation documented in the PRD section 9. No existing seed row numbers change.

TECH STACK
FastAPI Python 3.12, React 18, Vite, Tailwind, shadcn/ui, Recharts and ECharts, SQLite WAL, Docker Compose, Alembic, pandas. Ports 9000 front and 9001 back.

STEP ZERO, confirm workspace
1. Print the current directory and confirm it is ~/Documents/Claude/Claude_Code/Projects/akb1-command-center.
2. Print `git status` and confirm a clean working tree.
3. Print the first twenty lines of docs/PRD_TAB_12_PNL_COCKPIT.md and confirm it exists. If missing, copy it from ~/Documents/Claude/Cowork/Projects/"AKB1 Base — Chief of Staff"/16_AKB1_Command_Center_v5/docs/PRD_TAB_12_PNL_COCKPIT.md.

STEP ONE, create the feature branch
git checkout -b feat/tab-12-pnl-cockpit

STEP TWO, read the PRD end to end
Open docs/PRD_TAB_12_PNL_COCKPIT.md and summarise to me in ten bullet points what you will build, in implementation order. Wait for my approval before writing any code.

STEP THREE, seed deltas
Implement section 9 exactly. Regenerate financials.csv with five new columns using the deterministic billing_ratio and collection_ratio rules. Regenerate programme_rates.csv for six programmes times three tiers times twelve months. Show me the diff before committing.

STEP FOUR, backend endpoints
Implement the seven endpoints in section 10, one commit per endpoint. Each endpoint gets a contract test. All pytest tests pass before moving on.

STEP FIVE, frontend sections
Scaffold /pnl route, then implement the seven sections in the order listed in section 11. One commit per section. Lint and component tests must pass before moving on.

STEP SIX, ContextRail
Implement the shared drill-up rail per section 12. Mount on Executive, Margin and EVM, Customer, Delivery, and P&L Cockpit. URL-driven programme selection.

STEP SEVEN, doc updates
Update ARCHITECTURE.md (new section 6.14), WIREFRAMES.md (Tab 12), FORMULAS.md (definitions 50 through 55 with two worked examples each), DEMO_GUIDE.md (walkthrough), MASTER_CHECKLIST.md (build gates), CTO_QUESTIONS.md (five new questions), ROADMAP.md (Iteration 2 close, Iteration 3 open with commercial backbone entries), README.md (tab count and version bump).

STEP EIGHT, verification
Run the full section 15 protocol. Generate docs/VERIFICATION_REPORT_TAB_12.md with pass or fail per criterion. Take four screenshots under docs/screenshots/tab-12-pnl-cockpit/ and reference them in DEMO_GUIDE.md.

STEP NINE, PR
Open the PR with title `feat: Tab 12 P&L Cockpit (v5.3, Iteration 2 close)`. Description links this PRD and lists acceptance criteria status. Do not merge. Tag the release v5.3.0 after I approve the PR.

HARD RULES
1. Never change existing seed row numbers (planned_revenue, actual_revenue, planned_cost, actual_cost must be byte-identical before and after).
2. Never renumber existing tabs. Tab 12 is appended.
3. Every simulated field carries a visible disclaimer when Demo mode is true.
4. Narrative is deterministic, no external LLM call in v5.3.
5. All file creations or edits must be committed on the feature branch. No direct commits to main.
6. When in doubt, stop and ask me. Do not guess.

Begin with STEP ZERO now. Show me the output and wait for approval before STEP ONE.
```

---

## 21. Approval log

| Decision | Choice | Date | Source |
|---|---|---|---|
| Scope | Balanced, option two | 2026-04-22 | Cowork session with Claude, Chief of Staff review |
| Format | Self-contained PRD with paste-ready session prompt | 2026-04-22 | Same |
| Navigation | Append as tab 12, no renumbering | 2026-04-22 | Same |
| Seeds | Seed deltas included in PRD | 2026-04-22 | Same |

End of PRD.
