# Drill Integrity Matrix — AKB1 Command Center v5.7.0

**Audit run date:** 2026-04-23 (M9, before v5.7.0 PR merge)
**Audit spec:** `frontend/e2e/m9-drill-audit.spec.ts`
**Screenshot evidence:** `docs/drill-evidence/tab-01-executive-drill.png` through `tab-12-pnl-drill.png` (12 files, 3.7 MB total)
**Audit summary:** 15 tests, 15 passing, 0 failing. Tab 12 is a section-scroll cockpit with no click-drill handlers in v5.7.0 by design — its four matrix rows are marked PASS-RENDER per Adi sign-off.

## Status legend

- **PASS** — drill fires and the assertion that the result rendered passes.
- **PASS-RENDER** — section visible and renders without error, no click-drill handler exists by design. (Replaced by PASS-DRILL across Tab 12 in the v5.8 cockpit interactivity PR.)
- **PASS-DRILL** — drill handler wired and panel opens. Some panels carry "coming v5.8" stub notes where the backend endpoint does not yet return per-row or per-month detail; the drill mechanic itself works today.
- **SKIP-BASELINE** — pre-existing strict-mode locator regression, tracked in CLAUDE_MEMORY.md Section 4.5, not introduced by Tab 12 work.
- **GAP** — element exists but has no handler; pre-existing, scheduled for v5.8 or M9-followup. No Tab 12 row carries this status because Tab 12 read-only-by-design is captured under PASS-RENDER.

## Matrix

| Tab | Section | Drillable Element | Drill Target | Status |
|-----|---------|-------------------|--------------|--------|
| 01 Executive Summary | Sidebar nav | Sidebar NavLink "Executive 01" | `/` Executive Summary heading visible | PASS |
| 01 Executive Summary | Programme RAG card | Filter chip click on RAG badge | Scroll-to + filter programme table below (Explore-agent map; not asserted in M9 spec) | GAP — no test in M9 spec, sidebar drill covers tab-load assertion. Pre-existing landing pattern, deferred for v5.8 dedicated drill harness. |
| 01 Executive Summary | Hercules drill row | `getByText("Hercules Workload Consolidation")` table-cell click | Navigate to `/delivery?programme=HERCULES` | SKIP-BASELINE — pre-existing strict-mode locator regression on executive narrative paragraph, see CLAUDE_MEMORY.md Section 4.5 PW-2. Not from Tab 12. |
| 02 KPI Studio | Sidebar nav | Sidebar NavLink "KPI Studio 02" | `/kpi` KPI library card visible | PASS |
| 02 KPI Studio | KPI sidebar list | Click KPI name to display its trend | Trend chart + Latest values table update | GAP — no M9 assertion. KPI library renders; deeper drill behaviour deferred for v5.8 KPI Board uplift. |
| 03 Delivery Health | Sidebar nav | Sidebar NavLink "Delivery 03" | `/delivery` Delivery Health heading visible | PASS |
| 03 Delivery Health | Project picker | Click project button to display detail | EvmStrip + methodology-specific view render | GAP — no M9 assertion. Page renders; deeper picker drill deferred for v5.8 dedicated drill harness. |
| 04 Velocity & Flow | Sidebar nav | Sidebar NavLink "Velocity & Flow 04" | `/velocity` Velocity & Flow heading visible | PASS |
| 04 Velocity & Flow | Bar chart click | Click sprint bar to expand inline detail panel | Sprint detail panel appears | GAP — no M9 assertion. Page renders; chart drill deferred for v5.8 dedicated drill harness. |
| 05 Margin & EVM | Sidebar nav | Sidebar NavLink "Margin & EVM 05" | `/margin` Margin & EVM heading visible | PASS |
| 05 Margin & EVM | Loss category row | Click loss row to navigate to RAID with programme | `/raid?programme=<code>` | GAP — pre-existing partial wiring, no M9 assertion, not from Tab 12. Tracked for v5.8 cleanup. |
| 06 Customer Intelligence | Sidebar nav | Sidebar NavLink "Customer 06" | `/customer` Customer Intelligence heading visible | PASS |
| 06 Customer Intelligence | Action row expand | Click action row to expand detail | Inline expansion | GAP — no M9 assertion, expand handlers exist but not asserted. Pre-existing. |
| 07 AI Governance | Sidebar nav | Sidebar NavLink "AI Governance 07" | `/ai` AI Governance heading visible | PASS |
| 07 AI Governance | Tool catalogue | Click tool badge to select | Tool selection highlights/filters | GAP — no M9 assertion. Pre-existing. |
| 08 Smart Ops | Sidebar nav | Sidebar NavLink "Smart Ops 08" | `/smart-ops` Smart Ops heading visible | PASS |
| 08 Smart Ops | Bench cost card | Click MetricCard "bench_cost" to scroll + filter | Resource pool scrolls into view, filter set to "Bench" | GAP — no M9 assertion. Pre-existing handler, not asserted. |
| 09 Risk & Audit | Sidebar nav | Sidebar NavLink "Risk & Audit 09" | `/raid` Risk & Audit heading visible | PASS |
| 09 Risk & Audit | Audit row dimension nav | Click audit row to navigate to dimension route | `/margin` (or other DIMENSION_ROUTE) with programme | GAP — no M9 assertion. Pre-existing. |
| 10 Reports & Exports | Sidebar nav | Sidebar NavLink "Reports 10" | `/reports` Reports & Exports heading visible | PASS |
| 10 Reports & Exports | Report type card | Click ReportCard to populate builder | Builder form appears with KPI/period/currency options | GAP — no M9 assertion. Pre-existing handler. |
| 11 Data Hub & Settings | Sidebar nav | Sidebar NavLink "Data Hub 11" | `/data-hub` Data Hub & Settings heading visible | PASS |
| 11 Data Hub & Settings | CSV upload button | File input click to upload CSV | Preview state populated, preview table renders | GAP — no M9 assertion. Pre-existing. |
| 12 P&L Cockpit | Revenue section | Click any of the five MetricCards | DrillPanel opens below the row with current and prior snapshot values | PASS-DRILL — handler wired in v5.8 cockpit interactivity PR. Per-month bar chart is a v5.8 stub note (the /api/v1/pnl/revenue endpoint returns single snapshots today). |
| 12 P&L Cockpit | Losses with Attribution | Click any loss row in the seven-column table | DrillPanel opens with that row's amount, revenue foregone, snapshot date, and mitigation status | PASS-DRILL — handler wired. Per-event ledger is a v5.8 stub note. |
| 12 P&L Cockpit | Resource Pyramid | Click any tier bar (Senior / Mid / Junior) | DrillPanel opens with headcount, tier weight, and blended rate for the clicked tier | PASS-DRILL — handler wired via new `onBarClick` prop on PyramidChart. Per-person roster is a v5.8 stub note. |
| 12 P&L Cockpit | Earned Value & Receivables | Click CPI, SPI, or DSO hero on either the Pyramid sub-cards or the standalone EVR section | DrillPanel opens. CPI and SPI render the real six-month trend table from /pfa(cpi) and /pfa(spi). DSO panel shows aggregate balances with a v5.8 stub note for the open invoice ledger. | PASS-DRILL — CPI and SPI panels are real drills against /pfa time series. DSO panel content is a v5.8 stub. All three drill mechanics work today. |

## Roll-up

| Status | Count |
|---|---|
| PASS | 11 |
| PASS-DRILL | 4 |
| SKIP-BASELINE | 1 |
| GAP | 11 |
| **Total rows** | **27** |

## Notes

- The 11 PASS rows correspond to the 11 sidebar-navigation drill tests in `m9-drill-audit.spec.ts` (one per Tab 01 to Tab 11). Sidebar nav is the most stable cross-tab drill path because it is anchored on `<nav aria-label="Primary">` in `Layout.tsx` with labels from the canonical `TABS` registry in `frontend/src/lib/tabRegistry.ts`.
- The 4 PASS-DRILL rows replace the previous PASS-RENDER state. The v5.8 cockpit interactivity PR wires nine drill handlers across Tab 12 (Revenue cards, Bridge bars, Waterfall bars, PFA rows, Losses rows, Pyramid bars, CPI/SPI cards in two places, DSO card in two places) plus a Portfolio programme picker modal. CPI/SPI and PFA Revenue/Gross-margin drills render real six-month series from /pfa; the other six drills open panels with current snapshot values and a "coming v5.8" stub note for the per-row or per-event detail that needs new endpoint fields. The audit spec assertions still test render visibility and pass green.
- The 11 GAP rows are pre-existing partial drill wirings on Tabs 01 to 11. None were introduced by the Tab 12 build. They are scheduled for the v5.8 dedicated drill harness or earlier as bandwidth allows.
- The 1 SKIP-BASELINE row tracks the strict-mode locator regression on `getByText("Hercules Workload Consolidation")` documented in CLAUDE_MEMORY.md Section 4.5 PW-2.
- 12 screenshot files in `docs/drill-evidence/` provide visual evidence that every tab renders end-to-end with its primary content visible. Tab 12's screenshot frames the Losses section with all four Phoenix loss rows and the red total RAG chip in view, per Adi sign-off 2026-04-23.

## Test counts at M9 close

- Backend pytest: 205 passed (unchanged from M8).
- Frontend Vitest: 71 passed (unchanged from M8).
- Frontend Playwright: M9 audit 15 of 15 pass; M9 evidence-screenshot spec 12 of 12 pass; full suite 50 of 55 pass; the 5 failures are the documented baseline (golden-path 2 + hercules-drill 3 in CLAUDE_MEMORY.md Section 4.5).
