# Tomorrow morning — pick-up plan (2026-04-21 IST)

We stopped on **2026-04-20 ~22:50 IST**. You said "let's stop for today and resume tomorrow morning IST". This file is the plan I committed to execute when you log back in and run `claude` from this directory.

## What to do when you sit down

1. **Log into the Mac.** Docker Desktop starts, the LaunchAgent runs `scripts/autostart.sh`, the dashboard opens in your default browser at http://localhost:9000.
2. **Open Terminal and get into the repo**:
   ```bash
   cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center
   git checkout feat/iteration-5-integration
   git pull
   claude
   ```
3. **Tell Claude Code**: "Resume from docs/TOMORROW.md." It will read this file plus its memory note (`project_status.md`) and run the plan below.

## Today's branch state

Branch: **`feat/iteration-5-integration`** (pushed, no PR yet).

Commits on top of main:
- `3e1fbb9` — reboot workflow guide + browser auto-open on login
- `f2f6fb8` — **I-5a**: live FX refresh via frankfurter.dev (✅ end-to-end verified)
- `234b2b2` — **I-5b**: CSV import commit + rollback backend (programmes + kpi_monthly entity types). **Frontend wiring NOT done yet — the new commit/rollback buttons still need to be added to Tab 11.**

Remaining from original I-5 scope:
- I-5c — SSE Smart Ops alerts ticker on Tab 1
- I-5d — Dark mode

## Plan to execute tomorrow (in order)

### Step 1 — full test matrix from a cold boot

Before we touch new code. Confirms every slice we've already shipped still works.

```bash
# From the repo root
cd ~/Documents/Claude/Claude_Code/Projects/akb1-command-center

# Backend
cd backend
.venv/bin/ruff check app tests
.venv/bin/pytest --cov=app --cov-report=term --cov-fail-under=70

# Frontend (unit + lint + build)
cd ../frontend
npm run lint
npm test
npm run build

# Full stack cold-start
cd ..
./scripts/cold-start-test.sh   # expects <180s; verified 26s last time

# Playwright E2E (stack must be up)
cd frontend
npm run test:e2e
```

Report the matrix back before moving on. Expected: pytest 37/37, vitest 17/17, ruff/ESLint clean, build green, Playwright 3/3, cold-start under 3 min.

### Step 2 — wire Tab 11 to the new commit + rollback endpoints

The backend already ships `POST /import/csv/commit` and `POST /import/{id}/rollback` with rollback-capable snapshots. The UI still shows only the I-1 preview-only flow. Wiring work:

- In `frontend/src/lib/api.ts`: add `fetchImportSchemas()`, `commitCsv(file, entityType)`, `rollbackImport(importId)`.
- In `frontend/src/pages/DataHub.tsx`:
  - Below the preview table, render an entity-type dropdown populated from `fetchImportSchemas()` (`programmes` + `kpi_monthly` today) with a **Commit** button.
  - On success: reset preview state, invalidate `["imports"]` so the ledger refreshes, toast a success message.
  - In the existing "Recent imports" list, make the **Rollback** button call the new mutation. On error (e.g. already rolled back) surface the backend message.
- Add a Vitest or Playwright check: preview → commit → rollback round-trip so the guarantee is codified.

### Step 3 — add the **Hercules** programme via the new CSV import flow

This is the validation exercise you specifically asked for.

1. Create `docs/csv-templates/hercules-programme.csv` (or whatever path makes sense for you — this file's content is the thing that matters). Suggested content (tell me if you want different numbers):

   ```csv
   name,code,client,start_date,end_date,status,bac,revenue,team_size,offshore_ratio,delivery_model,currency_code
   Hercules Workload Consolidation,HERCULES,GlobalBank Corp,2026-05-01,2027-06-30,At Risk,9500000,9500000,22,0.60,Managed Services,INR
   ```
2. Launch the dashboard (should already be running). Tab 11 → drag-drop the CSV → pick `programmes` entity → **Commit**.
3. Expect: programme count on Tab 1 goes from 5 to 6. Hercules visible in the status table. RAG counts reflect `At Risk`.

If you also want Hercules to show up on Tabs 3 / 4 / 5 / 6 / 7 / 8 / 9, we need to extend the `SCHEMA_REGISTRY` in `backend/app/services/csv_import.py` to accept more entity types (projects, sprints, evm_monthly, kpi_monthly, risks, customer_satisfaction, etc.). Say the word and I'll add them before generating the seed CSVs.

### Step 4 — full drill-navigation regression on Hercules

Once Hercules is in, exercise every drill pattern so we know the new programme behaves like the seeded ones:

- **Drill-down**: Executive row → `/delivery?programme=HERCULES`; Top Risks (if any) → same; RAG bucket filter.
- **Drill-up**: breadcrumb, clear-filter chip, collapse expanded rows.
- **Drill-across**: prev/next programme arrows in ProgrammeFilterBar cycle past Hercules.
- **Drill-through**: "Open in: KPI / Velocity / Margin / Customer / AI / Smart Ops / Risk & Audit" chips from any Hercules context.
- **Leaf expand**: sprint, phase, milestone, CR, action item, SLA incident, risk row expansions all render cleanly even when the underlying tables are empty for Hercules (expect "no data" placeholders, not crashes).

Report any rendering regressions so we fix them before closing I-5.

### Step 5 — open the PR (only when you've signed off on steps 1-4)

```bash
gh pr create --title "feat: Iteration 5 — live FX + CSV commit/rollback + Hercules validation" \
  --body-file /tmp/i5-pr-body.md
```

I'll draft the body from the commit list + what we validated.

## File pointers

- Auto-start guide: `docs/AFTER_REBOOT.md`
- Daily workflow: `docs/RUN_BOOK.md`
- Changelog: `CHANGELOG.md`
- Session memory (Claude Code loads this automatically):
  `~/.claude/projects/-Users-adikompalli-Documents-Claude-Claude-Code-Projects-akb1-command-center/memory/project_status.md`
