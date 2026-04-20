# AKB1 Command Center — PRODUCTION-GRADE SDLC ADOPTION
**Version:** 5.2 | **Author:** Adi Kompalli | **Audience:** Engineering leaders evaluating how AKB1 will be built and maintained
**Purpose:** Explain — in production-grade terms — how software applications are actually developed, what phases they traverse, how those phases relate to each other, what is learned from bug fixes, and exactly how AKB1 will adopt that same discipline before going public on GitHub.

---

## 1. EXECUTIVE SUMMARY

Production-grade software is not written — it is **assembled** across seven loosely-coupled phases (Requirements → Design → Implementation → Verification → Release → Operate → Learn) joined by six feedback loops that exist specifically to catch mistakes early and learn from the ones that escape. The phases share three non-negotiable properties: every artefact is versioned, every change is reversible, and every failure becomes a documented lesson.

AKB1 v5.2 will adopt this lifecycle in a lightweight form appropriate to a single-maintainer, community-contributable open-source project. The design phase is already complete (13 docs under `docs/`). The build phase will run in four two-week iterations with explicit gates. A **public postmortem for every Sev-1 defect** will be the cultural keystone — the same discipline AKB1 itself is built to enforce for IT-services delivery is the discipline its own codebase will live by.

---

## 2. THE SEVEN PHASES — WHAT EACH PHASE ACTUALLY DOES

### 2.1 Phase 1 — Requirements (What problem, for whom, success criteria)

**Purpose:** Convert a business problem into a precise, testable specification.

**Outputs:**
- Problem statement (1 page).
- Target user personas with success criteria.
- Functional requirements (numbered, testable, traceable).
- Non-functional requirements (performance, security, accessibility, compliance).
- Explicit non-goals (what we will NOT do).
- Success metrics (how we know we succeeded).

**Relationship to other phases:** Requirements are the anchor. Every test case, every design decision, and every release gate traces back to a requirement ID. Drift from requirements without formal change control is the #1 source of delivery failure industry-wide (Standish CHAOS reports, 1994–present).

**AKB1 evidence:** `docs/ARCHITECTURE.md` §1 (Vision), `docs/CTO_QUESTIONS.md` (58 testable questions that act as acceptance criteria), `docs/MASTER_CHECKLIST.md` (verification baseline).

---

### 2.2 Phase 2 — Design (How we will build it, trade-offs explicit)

**Purpose:** Turn requirements into an architecture that humans can reason about before committing code.

**Outputs:**
- System architecture diagram.
- Data model and schema.
- API contracts.
- Interaction/sequence diagrams for non-obvious flows.
- Architecture Decision Records (ADRs) — one per meaningful decision.
- Failure-mode analysis (what breaks, how do we detect, how do we recover).
- Security threat model (STRIDE per component).

**Relationship to other phases:** Design is where you pay the cheapest price for a change. A schema rethink on paper is hours; the same rethink after 50 features are built is weeks or a rewrite.

**AKB1 evidence:** `docs/ARCHITECTURE.md` (20 sections, 44 tables, 45 formulas), `docs/WIREFRAMES.md` (11 tabs with metric dictionaries), `docs/TECH_STACK_BENCHMARK.md` (stack trade-offs with explicit retain/add/consider/reject), `docs/FORMULAS.md`.

---

### 2.3 Phase 3 — Implementation (Code, with process around it)

**Purpose:** Write the minimum code that satisfies the design, reviewed by a second pair of eyes, under source control, with tests.

**Outputs:**
- Source code, in small, reviewable pull requests.
- Unit tests (hermetic, fast, cover logic branches).
- Integration tests (hit real dependencies: DB, file system).
- Contract tests (API input/output matches spec).
- Migration scripts (forward + rollback).
- Developer-facing docs (READMEs, docstrings, ADR updates).

**Engineering practices that differentiate production from hobby:**
- Trunk-based development with short-lived feature branches.
- Every merge is a green CI build.
- Type checking + linting gates at CI.
- Code owners enforced on critical paths.
- Conventional Commits for human + machine-readable history.
- Pre-commit hooks to catch obvious mistakes before review.

**Relationship:** Implementation is the phase where design assumptions are tested against reality. The tests written here are the ones that catch regressions forever.

**AKB1 plan:** Ruff + Black + MyPy + pytest + Vitest + Playwright + Conventional Commits + pre-commit + squash-merge + code owners (Adi initially; expand on contributor onboarding).

---

### 2.4 Phase 4 — Verification (Does it actually work, under real load, for real users)

**Purpose:** Prove the built system meets the requirements, non-functionally and functionally.

**Outputs:**
- Test plan mapping test cases to requirement IDs.
- Automated test suite results (unit + integration + E2E + contract).
- Performance test results against explicit budgets.
- Accessibility audit (axe-core + keyboard walkthrough + screen reader spot check).
- Security scan results (SAST, dependency vulnerability scan, container scan).
- User-acceptance test sign-off (for enterprise) or **early-adopter feedback** (for OSS).

**Relationship:** This is where the feedback loop to Phase 2 fires hardest. A design flaw found in verification is painful but recoverable; the same flaw found in production is expensive and visible.

**AKB1 plan:**
- Unit coverage ≥ 70% on the formula/math module.
- Integration coverage on data-ingestion (CSV + XLSX) end-to-end.
- Playwright smoke: cold-start → demo-seed → every tab renders.
- axe-core on every page in CI.
- Trivy scan on container image in CI.
- Performance budget: Time-To-Interactive < 3s on 4-core/8GB host.

---

### 2.5 Phase 5 — Release (Ship it safely, be ready to pull it back)

**Purpose:** Get the verified artefact into users' hands with a clear rollback path.

**Outputs:**
- Signed release artefact (container image, tag).
- Release notes (user-visible changes in plain language).
- CHANGELOG entry (Keep a Changelog format).
- Migration runbook (for breaking changes).
- Pre-release checklist signed.
- Rollback procedure documented and rehearsed.

**Release patterns worth using in AKB1:**
- Semantic versioning (major.minor.patch).
- Image tags: `5.2.0`, `5.2`, `5`, `latest`.
- Pre-release channel for early adopters: `5.3.0-rc.1`.
- Signed images via cosign (v5.3+).

**Relationship:** Release closes the forward loop from Requirements. Operate opens the backward loop to Learn.

---

### 2.6 Phase 6 — Operate (Run it, watch it, respond to incidents)

**Purpose:** Keep the system healthy and responsive after release.

**Outputs:**
- Monitoring dashboards (SLOs, error rates, latency).
- Alerting on symptoms, not causes.
- On-call runbooks per alert.
- Incident log.
- Change log for every config update in production.

**For self-hosted OSS like AKB1:**
- The "on-call" is the user running the container.
- Our job is to make failures **observable and self-recoverable**.
- Structured logs, `/health` endpoint, clear error messages, rollback scripts.
- `docker compose logs` should be sufficient for 90% of diagnosis.

**Relationship:** Every operational surprise is a Phase-5 release-notes miss or a Phase-2 design-blind-spot. Capture it.

---

### 2.7 Phase 7 — Learn (Postmortems, root cause, permanent fixes)

**Purpose:** Convert every failure into a permanent improvement.

**Outputs:**
- Blameless postmortem per Sev-1/Sev-2 incident.
- Root-cause analysis using "5 whys" or causal-chain method.
- Action items with owners and due dates.
- Test case that would have caught this bug (added to the suite permanently).
- Documentation update.
- Public CHANGELOG entry if user-visible.

**AKB1 plan:** Every Sev-1 bug report becomes a public postmortem in `/docs/postmortems/YYYY-MM-DD-<slug>.md`. Non-negotiable. This is the single most important cultural practice we can adopt, because it signals to every evaluator that we treat bugs like the AI industry treats outages — with structured learning, not embarrassment.

---

## 3. HOW BUG FIXES ACTUALLY WORK (PRODUCTION-GRADE)

The common misconception is that fixing a bug equals "changing the code until the symptom goes away." That is the worst possible outcome because the bug is suppressed, not eliminated, and the underlying fault returns somewhere else.

### 3.1 The 9-step production bug-fix process

1. **Reproduce** — in isolation, with a failing test (or a documented manual recipe if automation impossible).
2. **Bisect** — identify the commit or change that introduced the defect.
3. **Root cause** — why did this happen, not where. 5-whys until the answer names a design or process gap.
4. **Blast radius** — what else is affected by the same root cause? Often the visible bug is one of many.
5. **Test first** — write the failing test that encodes the defect. This test stays in the suite forever.
6. **Fix minimally** — change the smallest amount of code that makes the test pass without breaking others.
7. **Verify** — rerun the full suite; confirm no regressions.
8. **Ship with narrative** — commit message + CHANGELOG entry explains what users experienced, what we changed, and what the lesson is.
9. **Postmortem if user-visible** — convert the fix into a blameless document. Update runbooks, threat model, ADRs, test plan as needed.

### 3.2 What each fix teaches us (taxonomy of lessons)

| Lesson type | Recurring pattern | Permanent fix added to practice |
|-------------|-------------------|---------------------------------|
| Input the system did not expect | Fuzz/invalid input, encoding, boundary | Add validation; fuzz test; document input contract |
| State the system did not expect | Concurrency, partial failure, retry | Add idempotency; circuit-breaker; retry budget |
| Dependency changed underneath us | Library upgrade, API change | Pin versions; contract test; Dependabot review gate |
| Performance cliff | N+1 query, unbounded loop, memory leak | Load test; perf budget; paginated query; profiler-in-CI |
| Miscommunication in the spec | Requirement was ambiguous | Rewrite requirement with explicit example + counter-example |
| Process failure | No one reviewed; CI skipped | Enforce branch protection; required checks |
| Human error | Ran migration in wrong env | Runbook + dry-run + approval gate |
| Architectural limit hit | Scale exceeded design envelope | ADR documenting the limit and the migration path |

The point is not to memorise the taxonomy. The point is that the process of writing it down per bug is what converts one team's pain into every future user's silent benefit.

### 3.3 What good looks like (examples we emulate)

- **Google SRE** — error budgets, blameless postmortems, toil tracking.
- **PostgreSQL** — every bug fix ships with a regression test that stays forever.
- **Rails** — incremental `deprecate → remove` migration discipline per feature.
- **Grafana Labs** — public postmortems after every major incident.
- **Kubernetes** — SIG-ownership model for every bug; no orphaned defects.

---

## 4. THE FEEDBACK LOOPS (WHY THE PHASES ARE NOT LINEAR)

| Loop | From → To | Trigger | Frequency |
|------|-----------|---------|-----------|
| 1. Design review fail | Implementation → Design | Developer finds design can't be built | Weekly |
| 2. Test red → spec red | Verification → Requirements | Test reveals an ambiguous requirement | Every iteration |
| 3. Release blocker | Verification → Implementation | Critical bug found pre-release | Per release |
| 4. Incident retro | Operate → Design | Sev-1 reveals architectural blind spot | Per incident |
| 5. User feedback | Operate → Requirements | Users reveal unmet needs | Continuous |
| 6. Upstream dependency change | Operate → Implementation | Security patch, API break | Ad-hoc |

Production-grade teams treat these loops as first-class citizens, not exceptions. They plan capacity for them.

---

## 5. HOW AKB1 WILL ADOPT THIS APPROACH

### 5.1 Build phase plan (post v5.2 doc lock)

Four two-week iterations with explicit entry/exit gates.

| Iteration | Scope | Entry Gate | Exit Gate |
|-----------|-------|------------|-----------|
| I-1 — Foundation | Backend scaffold, SQLite schema v5.2, demo seed, `/health`, Docker compose works | Docs locked, checklist green | Backend boots; tests pass; health green |
| I-2 — Core dashboard | Tabs 1, 2, 3 (methodology-adaptive), 5 (margin/EVM) | I-1 exit | Tabs 1/2/3/5 render demo data; axe-core clean |
| I-3 — Advanced | Tabs 4 (velocity), 6 (customer), 7 (AI governance), 8 (smart ops), 9 (RAID) | I-2 exit | All 11 tabs render; smoke test green; perf budget met |
| I-4 — Polish & Ship | Tab 10 reports, Tab 11 data hub, backup/restore, migration scripts, release notes, screenshots | I-3 exit | v5.2.0 tag, GHCR image, GitHub Pages site live |

### 5.2 Quality gates applied to every PR

1. Ruff (lint) green.
2. MyPy (type check) green.
3. pytest green on affected module.
4. Vitest green on affected component.
5. Coverage ≥ 70% on changed files.
6. Conventional Commit message.
7. Self-review checklist ticked in PR description.
8. Single reviewer approval (Adi initially).

### 5.3 Release gates applied to every tag

Derived from `MASTER_CHECKLIST.md` section M:
- Full suite (unit + integration + E2E) green on Mac, Windows-WSL2, Linux.
- Trivy scan: no CRITICAL or HIGH CVEs on the image.
- SBOM generated and attached to release.
- CHANGELOG updated.
- Migration script tested against prior-version snapshot.
- Cold-start install reproduced on a fresh VM.
- At least one human smoke of the UI for each methodology view.

### 5.4 Bug-fix discipline from day one

- One GitHub issue per defect with reproduction steps.
- Labels: `bug`, `severity/sev-1..4`, `area/backend|frontend|docs|data`.
- PR linked to issue via `Fixes #NNN`.
- Regression test added in the same PR as the fix.
- Sev-1 fixes get a postmortem in `docs/postmortems/`.
- Monthly bug-triage review; stale issues either actioned or explicitly deferred with rationale.

### 5.5 Observability for self-hosted users

- Structured JSON logs (one-line-per-event) from the backend.
- `/health` returns DB connectivity + disk space + last-backup timestamp.
- `/debug/snapshot` (admin-only) produces a sanitised diagnostic bundle users can attach to issues — saves hours per support thread.

---

## 6. RISK OF SKIPPING ANY PHASE (WHY NONE IS OPTIONAL)

| Skipped phase | What tends to happen |
|---------------|----------------------|
| Requirements | Built the wrong thing; nobody uses it |
| Design | Built a thing that cannot evolve; rewrite in 18 months |
| Implementation discipline (tests, lint, review) | Shipped defects; velocity collapses after 6 months |
| Verification | Discover production defects at the worst possible time |
| Release discipline | Cannot roll back; outages become permanent |
| Operate/observability | Silent failures; trust erodes |
| Learn | Same bug ships three times |

Every one of those failures is visible in the audit trail of projects we have seen fail. Adopting the full lifecycle is cheaper, every time, than skipping steps and paying at the end.

---

## 7. DECISION SUPPORT — 3 OPTIONS FOR AKB1

| Option | Type | Description | Risk | Outcome |
|--------|------|-------------|------|---------|
| 1 | Conservative | Hobby-grade: write code, ship it when it runs, fix bugs as reported. | High | Users lose trust; contributions dry up |
| 2 | Balanced (RECOMMENDED) | The seven-phase lifecycle applied lightweight as described above. | Low | Slower first release, but every release afterward is cheap |
| 3 | Strategic | Full enterprise rigour — SLSA supply chain, SOC-2 controls, threat modelling per feature. | Medium | Overkill for an OSS project with a single maintainer today |

**Recommended: Option 2** — Balanced. It is the minimum viable production discipline, the level at which Grafana, Plausible, and Focalboard operate, and the only level that matches the credibility AKB1 must project to be adopted by delivery leaders.

---

## 8. CLOSING POSITION

We will not ship AKB1 as code that happens to compile. We will ship it as a system that has been specified, designed, implemented, verified, released, operated, and learned from — publicly and in writing, every step traceable. The discipline AKB1 enforces on the programmes it monitors is the same discipline it will live by itself. That is the argument for credibility, and it is the only argument that matters.
