# AKB1 Command Center — Technical debt register

This file tracks scope items intentionally deferred from the release they were originally scoped into. Each entry records: what was deferred, why it was deferred, the release it was deferred from, the release it is picked up in, and the trigger that reopens it.

Deferrals are not bugs. Bugs live in the GitHub issue tracker. This file exists so the next builder does not re-derive the reasoning behind a missing endpoint or section.

---

## v5.7.0 Tab 12 P&L Cockpit — M3b deferrals

Three endpoints and their matching frontend sections were deferred from v5.7.0 (Tab 12 P&L Cockpit) to v5.8. The PRD at `docs/PRD_TAB_12_PNL_COCKPIT.md` retains the design content for each — sections six (Commercial Levers) and seven (LLM Narrative) carry an explicit "Status: deferred to v5.8" banner at the top; section one (KPI Board) carries the same banner.

| Deferred item | Scope | Deferred from | Picked up in | Trigger to reopen |
|---|---|---|---|---|
| `GET /api/v1/pnl/board/{scope}` and `KpiBoard.jsx` | Unified ten-card KPI grid covering committed, booked, billed, collected, unbilled WIP, DSO, gross, contribution, portfolio, net | v5.7.0 | v5.8 | Already unblocked. v5.7.0 split the ten cards across `/pnl/revenue` (five), `/pnl/waterfall` (four), `/pnl/dso` (one). v5.8 re-unifies them into a single grid endpoint on top of the existing data paths. |
| `GET /api/v1/pnl/levers` and `LeversPanel.jsx` | Ranked top-five margin recovery levers with feasibility-weighted impact scoring | v5.7.0 | v5.8 | Lever-framework design must land first. Without it, the endpoint surfaces numbers a PM cannot act on (feasibility weights are un-defensible, estimated impact is un-auditable). v5.8 opens with the framework design, then this endpoint follows. |
| `GET /api/v1/pnl/narrative` and `NarrativeBlock.jsx` | Deterministic template-substituted executive paragraph covering portfolio margin, worst programme, forecast risk, top levers | v5.7.0 | v5.8 | Tab AI PRD must land first. Shipping a template-only version in v5.7.0 creates a second narrative pattern for the Executive tab team to reconcile later. Better to land once, correctly, once the LLM orchestration layer is designed. |

### Why these three, not others

The nine endpoints shipped in v5.7.0 (waterfall, bridge, pfa, pyramid, losses, evm, dso, revenue, lineage) compute from data that exists in the M2 seed using formulas locked in `docs/FORMULAS.md`. The three deferred endpoints each depend on one or more design artefacts that are not locked yet:

- `/board` depends on the unified card-layout decision that v5.8 will ratify alongside the planned Executive-tab refresh.
- `/levers` depends on the margin-lever action framework (feasibility weights, mechanism taxonomy, ownership routing) — all open questions.
- `/narrative` depends on the Tab AI PRD, which specifies whether the narrative is LLM-generated, template-substituted, or hybrid, and which endpoint fans out.

Shipping any of these on placeholders in v5.7.0 would have created three rewrites in v5.8. Deferring once is cheaper.

---

## v5.7.0 Tab 12 P&L Cockpit — M7.6 data gaps

Two gaps surfaced while wiring the Pyramid section at M7.6. Both are tracked here for v5.8 pickup.

| Deferred item | Scope | Deferred from | Picked up in | Trigger to reopen |
|---|---|---|---|---|
| Tier weight seed anomalies in `programme_rates` | Some PHOENIX rows carry `tier_weight_actual` values outside the `[0, 1.2]` expected range (e.g. Junior 1.4, Mid −0.435 on the 2026-12-01 snapshot). Normalisation across tiers breaks. The frontend renders what the endpoint returns and surfaces a data-quality footnote on the Pyramid chart when any weight is out-of-range. | v5.7.0 M7.6 | v5.8 | Fix the seed generator in `backend/app/seed/pnl_seed.py` so `sum(tier_weight_actual)` per (programme, snapshot) equals 1.0 ± 0.02 and no individual tier sits outside `[0, 1.0]`. Add a reconciliation test under `backend/tests/test_pnl_reconciliation.py` that asserts the invariant across all seeded programme_rates rows. |
| DSO trend sparkline | The Pyramid section's DSO sub-card currently shows a single-snapshot number plus AR balance and Unbilled WIP. A six-month DSO trend line was dropped at M7.6 because it would have required six parallel `/dso` calls with rolling windows — too heavy for a small ornament. | v5.7.0 M7.6 | v5.8 | Add `metric="dso_days"` to the `/api/v1/pnl/pfa/{programme_code}` endpoint vocabulary so a single call returns the full time series, matching the existing pattern used for CPI / SPI sparklines in the EVM sub-card. Then wire the line chart into `DsoSubCard` inside `PyramidSection.tsx`. |

### Why these two, not a broader backlog

Both items surfaced as direct blockers to rendering the Pyramid section cleanly. The tier weight anomaly is a seed bug, not a contract bug — the endpoint behaves correctly given the data it holds. The DSO trend is a contract gap: the `/pfa` metric vocabulary should include `dso_days` but does not. Neither justified breaking the M3b endpoint scope-seal at M7.6.

---

### Acceptance for reopen

When v5.8 picks these up, acceptance criteria must include:

1. Lever-framework doc merged and referenced by `/levers`.
2. Tab AI PRD merged and referenced by `/narrative`.
3. Ten-card grid visually validated against the Executive-tab refresh.
4. All three endpoints return the shared `FiltersApplied` + `LineageBlock` shape (no deviation from the v5.7.0 envelope).
5. The three deferred-to-v5.8 banners in `docs/PRD_TAB_12_PNL_COCKPIT.md` sections 6.1, 6.6, 6.7 are removed and replaced with live worked examples.
