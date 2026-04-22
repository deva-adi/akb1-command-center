# CLAUDE_MEMORY.md — AKB1 Command Center project recovery file

This file is the recovery document. It is updated at the end of every milestone commit, before the git push. In any future Claude Code session starting cold after data loss or a machine reset, the first instruction is: read this file and resume from the state it describes.

Last updated: 2026-04-22 (end of M6)

---

## Section 1 — Project identity

- **Local repo path:** `/Users/adikompalli/Documents/Claude/Claude_Code/Projects/akb1-command-center` (iCloud-synced)
- **GitHub remote:** https://github.com/deva-adi/akb1-command-center
- **Current feature branch:** `feat/tab-12-pnl-cockpit-v5.7`
- **Main branch:** `main`
- **Target tag:** `v5.7.0` (cut only after M9 drill-audit sign-off)
- **Docker ports:** 9000 (frontend / nginx), 9001 (backend / uvicorn), both bound to 127.0.0.1
- **Tech stack:**
  - Backend: FastAPI + Python 3.12, SQLAlchemy 2.0 async, Pydantic v2, Alembic, structlog
  - Database: SQLite WAL mode, volume-mounted at `/data/akb1.db` inside the backend container
  - Frontend: React 18, Vite, Tailwind, shadcn/ui, Recharts, ECharts, Zustand, React Query
  - Tests: pytest on host venv (`backend/.venv`), Vitest + axe-core on the frontend
  - Lint and type: Ruff + MyPy backend, ESLint frontend
  - Orchestration: Docker Compose (services `backend`, `frontend`)
- **Host venv for pytest:** `source backend/.venv/bin/activate` then `python -m pytest tests/`

---

## Section 2 — Milestone log

| Milestone | Commit | Date | One-line description |
|---|---|---|---|
| M0 (PRD lock) | `d80a42e` | 2026-04-22 | docs: add PRD_TAB_12_PNL_COCKPIT.md — locked spec for the Tab 12 build |
| M1 (DB) | `9fb974d` | 2026-04-22 | feat(db): Alembic bootstrap + migration 0003 + ProgrammeRate model for v5.7.0 |
| M2 (seed) | `a1a7414` | 2026-04-22 | feat(seed): programme_rates, Feb-Mar Monthly Actuals, billing backfill (252-row programme_rates, 7 programmes incl. BHARAT) |
| M3a (infra) | `0175b5f` | 2026-04-22 | chore: version SSOT + P&L shared infra (filters, error envelope, lineage keys, schemas) |
| M3b (endpoints) | `9561102` | 2026-04-22 | feat(api): nine P&L endpoints + PRD v5.7 scope rewrite + docs/TECH_DEBT.md |
| M3b recovery doc | `31ddd99` | 2026-04-22 | docs: add CLAUDE_MEMORY.md project recovery file (standing rule established) |
| M4 (formulas + harness) | `8cc823e` | 2026-04-22 | feat(test): FORMULAS 50-55 for the 6 new Tab 12 definitions + cross-endpoint reconciliation harness (+55 tests, 205 total green) |
| M5 (ContextRail) | `d0885dd` | 2026-04-22 | feat(ui): global ContextRail breadcrumb + drill-up/across + URL-encoded filter state; delete per-page Breadcrumb; migrate Customer to URL programme state (+8 Vitest, +2 Playwright) |
| M6 (/pnl stub + API client) | `d41eb3a` | 2026-04-22 | feat(ui): /pnl route + PnlCockpit.tsx stub + typed pnlApi.ts client for nine endpoints + nav entry + Vitest + Playwright (+3 Vitest, +3 Playwright) |

Earlier v5.x milestones (pre-Tab 12, already on main): v5.6 drill-fidelity audit (`792aa0d`), v5.5.4 margin bug fixes (`22c93b1`), v5.5.3 a11y trust-badge fix (`0854876`), v5.5.2 dead-metric-card fix (`7e03e1c`). These are retained on `main`; the Tab 12 branch builds forward from there.

---

## Section 3 — Current state

- **Milestone just completed:** M6 (/pnl route stub + typed pnlApi client + nav entry)
- **Tests:** backend 205 passed (unchanged — M6 is frontend-only), frontend 28 Vitest passed (up from 25 at M5 — 3 new PnlCockpit tests), plus 5 Playwright specs total (2 from M5 + 3 new pnl-stub specs)
- **/health output:** `{"status":"healthy","version":"5.7.0-dev","tables":47}`
- **Docker state:** `akb1-backend` healthy on 127.0.0.1:9001, `akb1-frontend` rebuilt at M6 close and healthy on 127.0.0.1:9000
- **Nine active endpoints registered** under `/api/v1/pnl/`: waterfall, bridge, pfa, pyramid, losses, evm, dso, revenue, lineage
- **Bridge identity locked:** Phoenix Feb→Mar `gross_margin_pct` reconciles to −340.00 bps exact (price +147.17, volume +61.71, mix −505.65, cost_residual −43.23)
- **Cross-endpoint identities pinned (M4):** 55 reconciliation tests across two programmes (Phoenix, Atlas)
- **ContextRail (M5):** global component at `frontend/src/components/ContextRail.tsx`, mounted once in `Layout.tsx`, URL-driven
- **PnlCockpit stub (M6):** `/pnl` route live at `frontend/src/pages/PnlCockpit.tsx` showing the M7 placeholder card. Nav entry "P&L Cockpit — 12" appears in the sidebar via the shared TABS registry. Typed API client at `frontend/src/api/pnlApi.ts` exports `fetchPnlWaterfall`, `fetchPnlBridge`, `fetchPnlPfa`, `fetchPnlPyramid`, `fetchPnlLosses`, `fetchPnlEvm`, `fetchPnlDso`, `fetchPnlRevenue`, `fetchPnlLineage` plus the shared `PnlFilters`, `FiltersApplied`, `LineageBlock`, and per-endpoint response types mirroring `backend/app/schemas/pnl.py`. No endpoints wired to UI yet — that's M7.
- **Branch state:** `feat/tab-12-pnl-cockpit-v5.7` is now eight commits ahead of main (M3a, M3b, M3b-memory, M4, M4-memory-fix, M5, M5-memory-fix, M6); no merge to main yet
- **In flight:** nothing mid-change on disk; working tree clean except unrelated Finder duplicate files
- **Next milestone:** M7 — wire the five Tab 12 section components (RevenueCards, MarginWaterfall, MarginBridge, PfaTriangle, LossesAttribution, Pyramid with EVM and DSO sub-cards) to the pnlApi client via React Query hooks. UI rendering against live Phoenix data.

---

## Section 4 — Deferred items

| Item | Deferred from | Picked up in | Tracked in |
|---|---|---|---|
| `GET /api/v1/pnl/board/{scope}` unified ten-card KPI grid and `KpiBoard.jsx` | v5.7.0 | v5.8 | `docs/TECH_DEBT.md` §"v5.7.0 Tab 12 P&L Cockpit — M3b deferrals" |
| `GET /api/v1/pnl/levers` and `LeversPanel.jsx` (ranked margin recovery levers) | v5.7.0 | v5.8 | same |
| `GET /api/v1/pnl/narrative` and `NarrativeBlock.jsx` (deterministic narrative paragraph) | v5.7.0 | v5.8 | same |

Reasons summarised (full reasoning in `docs/TECH_DEBT.md`):
- /board → card-layout decision pending alongside Executive-tab refresh.
- /levers → lever-framework design (feasibility weights, mechanism taxonomy, ownership routing) must land first.
- /narrative → Tab AI PRD must land first so the narrative pattern is chosen once.

PRD §6.1, §6.6, §6.7 carry "Status: deferred to v5.8" banners at the top with the full design content preserved underneath for v5.8 implementers.

---

## Section 4.5 — Known issues (must be fixed before M8 verification)

These are pre-existing issues carried forward from before the Tab 12 build began. They are not blockers for intermediate milestones but must be resolved before the M8 verification protocol runs, per Adi's note at the close of M5.

| ID | File | Line(s) | Description | Detected in |
|---|---|---|---|---|
| LINT-1 | `frontend/src/pages/MarginEvm.tsx` | 36 | `WATERFALL_LABELS` is assigned a value but only used as a type. Rule: `@typescript-eslint/no-unused-vars`. | pre-M5 baseline |
| LINT-2 | `frontend/src/pages/delivery/KanbanView.tsx` | 122, 139, 722, 725, 780, 783 | Six uses of `any`. Rule: `@typescript-eslint/no-explicit-any`. Columns-value typing or generic narrowing needed. | pre-M5 baseline |

Fix target: before the M8 verification protocol begins. Rerun `npm --prefix frontend run lint` after fixes and confirm the error count is zero. Record the resolving commit hashes in this table when done.

---

## Section 5 — Hard rules (non-negotiables)

1. **Feature-branch workflow.** All new work lands on a feature branch (currently `feat/tab-12-pnl-cockpit-v5.7`). No direct commits to `main`.
2. **Atomic milestone commits.** One milestone = one atomic commit (plus, when required, a `docs: add/update CLAUDE_MEMORY.md` follow-up commit). No partial milestone commits.
3. **No merge to main without M9 drill-audit sign-off.** The Tab 12 branch merges only after M9 (cross-tab drill integrity audit across all 12 tabs) closes.
4. **No commit without passing tests.** `python -m pytest tests/` must be green on the host venv before any commit. Commit hash and test count are reported at every milestone close.
5. **Human voice in all messages.** No em dashes, no emojis, no AI-speak in commit messages, code comments, or UI copy. Direct imperative, match existing British-English base.
6. **CLAUDE_MEMORY.md updated and pushed at every milestone close.** Update Section 2, Section 3, Section 4 at the end of every milestone commit. Either fold the update into the milestone commit or land it as an immediate follow-up `docs: update CLAUDE_MEMORY.md` commit before the push.
7. **GitHub push after every milestone commit, without exception.** `git push origin feat/tab-12-pnl-cockpit-v5.7` runs as soon as the milestone commit (and the CLAUDE_MEMORY.md commit if separate) lands. The remote branch is the off-machine backup.
8. **No CSV template rewrites.** Existing seed CSVs are ground truth. Only additive columns via a signed-off PRD, or brand-new CSVs, are allowed.
9. **No tab-index shift.** Tab 12 is appended. Existing tabs 01–11 keep their numbering.
10. **Idempotent migrations.** Every Alembic migration survives repeated `docker compose down -v` and fresh container bring-up. See `backend/app/db/migration_bootstrap.py` for the three-state classifier.

---

## Section 6 — Resume instructions (cold start after data loss)

If you are reading this in a new session where the previous conversation is gone, execute these steps in order and do nothing else until they complete.

**Step 1 — read this file.** You are doing that now. Note the "Last updated" date at the top. If it is older than expected, assume the project has moved on and skip to Step 4 to re-derive current state from the repo itself.

**Step 2 — confirm Docker is up.**
```
cd /Users/adikompalli/Documents/Claude/Claude_Code/Projects/akb1-command-center
docker compose ps
```
Both `akb1-backend` (127.0.0.1:9001) and `akb1-frontend` (127.0.0.1:9000) should show `Up`. If not: `docker compose up -d`. Wait for `/api/v1/health` to return 200.

**Step 3 — run pytest to confirm test count.**
```
source backend/.venv/bin/activate
python -m pytest tests/
```
The number must match (or exceed, for later milestones) Section 3's "Tests" line. If it does not, stop and investigate before writing any code.

**Step 4 — read the last milestone log entry and the current-state section.** The last row of Section 2 is the commit to resume from. Section 3 tells you the next milestone. Verify against `git log --oneline -5` that the commit hash in Section 2 matches what is on the branch.

**Step 5 — continue from the next milestone.** The "Next milestone" field in Section 3 is the authoritative pointer. Re-open the PRD (`docs/PRD_TAB_12_PNL_COCKPIT.md`) and `docs/TECH_DEBT.md` for context before touching code. Hold for Adi's sign-off before committing.

If any step produces an unexpected result, stop and surface the gap. Do not guess.
