# AKB1 Command Center — TECH STACK BENCHMARK
**Version:** 5.2 | **Author:** Adi Kompalli | **Audience:** CTO / Engineering Director / Evaluators
**Purpose:** Rigorous comparison of AKB1's chosen stack (FastAPI + React 18 + SQLite + Docker) against the most stable open-source delivery/portfolio/observability applications on the internet. Covers scalability, usability, reusability, installability, maintainability. Ends with explicit retain/replace/augment recommendations.

---

## 1. EXECUTIVE SUMMARY

The AKB1 stack is deliberately chosen for **single-container installability** — a solo delivery leader or small PMO should `git clone && docker compose up` and be running in under 5 minutes. That choice constrains the design envelope (single-node, ≤ 50k rows, ≤ 20 concurrent users) and mirrors the pattern used by the most successful self-hosted, single-purpose dashboards on GitHub today — Plausible, Umami, Linkwarden, Dashy, n8n community edition, and Homepage.

AKB1 differs from heavyweight PPM/PMO platforms (Jira Portfolio, Planview, Clarity, Broadcom Rally) by intent: those are multi-tenant SaaS stacks that require Kubernetes, Postgres clusters, and a vendor team. AKB1 sits in the emerging category of **"personal intelligence dashboards"** — single-user or small-team — where the target is not horizontal scale but zero-friction adoption and executive-grade insight density.

**Headline recommendation:** retain the core stack for v5.2 public release. Three surgical upgrades are proposed for v5.3 (Postgres-compatible DAL, OpenTelemetry tracing, Plausible-style analytics). Two tools are added now (Alembic for migrations, Pydantic Settings for config). No replatforming.

---

## 2. BENCHMARK UNIVERSE — WHAT WE COMPARED AGAINST

Selected 18 highly-starred open-source applications in adjacent categories. All are self-hostable, Docker-friendly, and have > 5k GitHub stars or well-known enterprise pedigree.

| # | Application | Category | Stars* | Backend | Frontend | DB | Install Complexity |
|---|-------------|----------|--------|---------|----------|----|--------------------|
| 1 | Plausible Analytics | Self-hosted analytics | 20k+ | Elixir/Phoenix | Vue | Postgres + ClickHouse | Medium |
| 2 | Umami | Analytics | 22k+ | Node.js/Next.js | React | Postgres/MySQL | Low |
| 3 | Grafana | Observability dashboards | 60k+ | Go | React | SQLite/Postgres/MySQL | Low |
| 4 | Metabase | BI / dashboards | 38k+ | Clojure/Java | React | H2/Postgres/MySQL | Low |
| 5 | Apache Superset | BI platform | 60k+ | Python/Flask | React | Postgres/MySQL | High |
| 6 | n8n | Workflow automation | 45k+ | Node.js | Vue | SQLite/Postgres | Low |
| 7 | NocoDB | Airtable-style | 47k+ | Node.js/NestJS | Vue | SQLite/Postgres/MySQL | Low |
| 8 | Appsmith | Internal tools | 33k+ | Java/Spring | React | Postgres | Medium |
| 9 | ToolJet | Internal tools | 30k+ | Node.js/NestJS | React | Postgres | Medium |
| 10 | Retool OSS / Tooljet alt | Internal tools | — | — | — | — | — |
| 11 | Focalboard | Kanban / PM | 8k+ | Go | React | SQLite | Low |
| 12 | Leantime | OSS project mgmt | 6k+ | PHP | Twig/JS | MySQL | Low |
| 13 | Kanboard | Kanban PM | 9k+ | PHP | Vanilla | SQLite/MySQL/Postgres | Low |
| 14 | OpenProject | Enterprise PM | 10k+ | Ruby on Rails | Angular | Postgres | High |
| 15 | Taiga | Agile PM | 8k+ | Python/Django | Angular | Postgres | High |
| 16 | Homepage | Self-hosted dashboard | 25k+ | Node.js/Next.js | React | File/YAML | Very Low |
| 17 | Dashy | Self-hosted dashboard | 20k+ | Node.js | Vue | File/YAML | Very Low |
| 18 | Wekan | Kanban | 20k+ | Meteor/JS | Blaze | MongoDB | Medium |

*Star counts rounded, as of public benchmark window 2026. Exact figures vary by sampling date; we treat anything > 8k as "stable & widely adopted" and anything > 20k as "category leader".

---

## 3. STACK LAYER-BY-LAYER COMPARISON

### 3.1 Backend Framework

| Criterion | FastAPI (AKB1) | Flask | Django | Express/Node | NestJS | Spring Boot | Rails | Phoenix |
|-----------|----------------|-------|--------|--------------|--------|-------------|-------|---------|
| Type-safe by default | ✅ (Pydantic) | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Async native | ✅ | ⚠️ (add-on) | ⚠️ (3.1+) | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Auto OpenAPI docs | ✅ (built-in) | ❌ | ⚠️ (DRF) | ❌ | ✅ | ✅ (SpringDoc) | ❌ | ❌ |
| Cold-start time | 200–400 ms | 150 ms | 500 ms | 100 ms | 400 ms | 2–5 s | 1–3 s | 200 ms |
| Container image size | 80 MB (slim) | 75 MB | 120 MB | 110 MB | 160 MB | 250 MB | 220 MB | 100 MB |
| Learning curve for reviewers | Low | Low | Medium | Low | Medium | High | Medium | High |
| Community size | Very Large | Very Large | Very Large | Very Large | Large | Very Large | Large | Medium |

**Verdict:** FastAPI is the correct choice. It is the single best Python framework for "dashboard-grade" applications because Pydantic eliminates an entire class of data bugs and the auto-generated OpenAPI spec doubles as our API documentation. Flask would save 5% on cold start but cost us type safety. Django would give us an admin panel but triple the bundle size and force us into its ORM. Node/NestJS is a legitimate alternative, but Python's pandas ecosystem is materially better for the KPI math this application is built around.

### 3.2 Frontend Framework

| Criterion | React 18 (AKB1) | Vue 3 | Svelte/SvelteKit | Solid | Angular | HTMX + Alpine |
|-----------|-----------------|-------|------------------|-------|---------|---------------|
| Bundle size (hello-world) | 44 KB gz | 34 KB gz | 4 KB gz | 7 KB gz | 160 KB gz | 14 KB + 8 KB |
| Hiring pool | Largest | Large | Small | Very Small | Large | Small |
| TypeScript maturity | ✅ | ✅ | ✅ | ✅ | ✅ native | N/A |
| Charting library coverage | Excellent (Recharts, Nivo, Visx, ECharts, Chart.js) | Good | Fair | Fair | Excellent | Limited |
| State management | React Query + Zustand | Pinia | Svelte stores | Solid stores | NgRx | Alpine |
| Server-side rendering | Next.js/Remix | Nuxt | SvelteKit | SolidStart | Angular Universal | N/A |

**Verdict:** React 18 is correct for AKB1's use case (dense data tables, 8+ chart types, heavy interactivity). Svelte would win on bundle size, but the charting ecosystem is thinner and contributors will be scarcer. HTMX is attractive for simplicity but will struggle with the Tab 3 methodology-adaptive views. **Retain React 18 with Vite.** Add React Query for server-state caching (currently implicit), Zustand for UI state.

### 3.3 Database

| Criterion | SQLite (AKB1) | Postgres | MySQL | DuckDB | MongoDB |
|-----------|---------------|----------|-------|--------|---------|
| Zero-config install | ✅ | ❌ | ❌ | ✅ | ❌ |
| Concurrent writers | Limited (WAL helps) | Excellent | Excellent | Limited | Excellent |
| Max practical size | 100 GB | TBs | TBs | TBs | TBs |
| Analytical query speed | Good | Good | Fair | Excellent | Fair |
| Schema-less flexibility | ❌ | ⚠️ (JSONB) | ⚠️ | ⚠️ | ✅ |
| Built-in full-text search | ✅ (FTS5) | ✅ (tsvector) | ✅ | ⚠️ | ✅ |
| Backup = single file | ✅ | ❌ (pg_dump) | ❌ | ✅ | ❌ |
| Used by | Focalboard, Grafana, Plausible (edge), Kanboard | OpenProject, Taiga, Plausible | Leantime, Kanboard | Emerging | Wekan |

**Verdict:** SQLite with WAL is the ideal fit for v5.2 because (a) the entire DB is a single portable file — one-click backup/rollback, (b) install complexity is literally zero, and (c) the workload (< 50k rows, < 20 concurrent users, analytical reads dominant) is inside SQLite's comfort envelope by a factor of 20. **Recommendation:** keep SQLite as default for v5.2; add a Postgres-compatible DAL layer in v5.3 so the same codebase can scale up for the rare deployment that needs it. Alembic for migrations instead of hand-rolled SQL from v5.2 onward.

### 3.4 Orchestration

| Criterion | Docker Compose (AKB1) | Kubernetes | Nomad | Bare metal |
|-----------|-----------------------|------------|-------|------------|
| Install effort for user | 2 commands | Weeks | Days | Days |
| Scales to multi-node | ❌ | ✅ | ✅ | Manual |
| Fits our audience | ✅ | ❌ overkill | ❌ | ❌ |

**Verdict:** Correct for v5.2. For v5.3+, publish a Helm chart for the rare enterprise deployment, but do not replace Compose as the default.

### 3.5 Styling

| Criterion | Tailwind (AKB1) | CSS Modules | styled-components | Chakra UI | Mantine | shadcn/ui |
|-----------|-----------------|-------------|-------------------|-----------|---------|-----------|
| Bundle size | Minimal (purge) | Minimal | Larger | Medium | Medium | Minimal |
| Design tokens | Tailwind config | Manual | Theme object | Theme object | Theme object | Tailwind + primitives |
| Accessibility primitives | ❌ (BYO) | ❌ | ❌ | ✅ | ✅ | ✅ (Radix) |
| Velocity | High | Medium | Medium | High | High | Very High |

**Verdict:** Tailwind + shadcn/ui primitives is the optimal pairing. shadcn provides Radix-powered accessible components (dialogs, tooltips, tabs, command palette) while Tailwind handles design tokens. This matches how modern OSS dashboards (Plausible's latest UI, Homepage, Dashy, Umami v2) are built. **Adopt shadcn/ui as the component primitive layer in v5.2.**

### 3.6 Charting

| Library | Bundle | Chart breadth | Interactivity | Accessibility | Fit |
|---------|--------|---------------|---------------|---------------|-----|
| Recharts | Medium | Good | Good | Good | ✅ Primary |
| Chart.js | Small | Wide | Good | Fair | Backup |
| ECharts | Large | Very Wide | Excellent | Good | Specialty (cumulative flow diagrams) |
| Visx (Airbnb) | Small | Custom | Excellent | Requires work | Advanced |
| Nivo | Medium | Wide | Good | Good | Alt. to Recharts |

**Verdict:** Recharts as primary (covers burndown, waterfall, bar, line, pie), ECharts specifically for the Kanban Cumulative Flow Diagram in Tab 3B (where Recharts struggles). This is the pattern Grafana and Superset use internally — one default + one specialty.

---

## 4. SCALABILITY / USABILITY / REUSABILITY SCORECARD

Scored 0–5 (5 = best-in-class).

| Dimension | AKB1 v5.2 | Plausible | Metabase | Focalboard | Grafana |
|-----------|-----------|-----------|----------|------------|---------|
| Install simplicity (time-to-first-screen) | 5 (<5 min) | 4 | 3 | 5 | 4 |
| Single-binary/container feasibility | 5 | 3 | 3 | 5 | 4 |
| Horizontal scalability | 2 | 5 | 5 | 2 | 5 |
| Vertical scalability (≤ 50k rows) | 5 | 5 | 5 | 5 | 5 |
| UX density for exec use | 5 | 4 | 4 | 3 | 4 |
| Accessibility (WCAG 2.1 AA) | 4 target | 3 | 3 | 3 | 4 |
| Methodology-aware views (Scrum/Kanban/Waterfall) | 5 | 0 | 2 | 3 | 2 |
| Multi-currency portfolio | 5 | 0 | 3 | 0 | 2 |
| Extensibility (plugins/API) | 3 | 4 | 5 | 3 | 5 |
| Community size | 0 (new) | 4 | 5 | 3 | 5 |

**Where AKB1 already wins:** methodology-aware views, multi-currency portfolio aggregation, executive information density, install simplicity.
**Where AKB1 is weaker:** horizontal scalability (by design), extensibility (no plugin framework yet), community (new project).

---

## 5. STACK RECOMMENDATIONS (RETAIN / ADD / CONSIDER / REJECT)

### RETAIN (v5.2 public release)
- **FastAPI** — correct. The OpenAPI auto-generation is worth 20 hours of documentation effort per release.
- **React 18 + Vite** — correct. Charting ecosystem alone justifies it.
- **SQLite + WAL** — correct for v5.2 audience.
- **Docker Compose** — correct.
- **Tailwind** — correct.
- **Pydantic v2** — correct.
- **Recharts** — correct default.
- **Uvicorn** — correct.

### ADD (v5.2 — part of this release)
1. **shadcn/ui** — accessible component primitives via Radix, no runtime dependency.
2. **Alembic** — schema migrations instead of hand-rolled SQL. Standard across the Python world.
3. **Pydantic Settings** — replace ad-hoc env parsing; single source of config truth.
4. **React Query (TanStack Query)** — server-state cache. Industry default.
5. **Zustand** — 1.1 KB state library for UI state. Used by Excalidraw, Poimandres-sphere.
6. **ECharts** — exclusively for cumulative flow diagrams in Tab 3B.
7. **openpyxl** — native .xlsx import/export (v5.2 requirement).
8. **Ruff + Black + MyPy** — linting baseline.
9. **Playwright** — single E2E smoke test for `cold-start → demo data → first chart renders`.
10. **Vitest + React Testing Library** — frontend unit tests.
11. **pytest + pytest-asyncio** — backend tests.

### CONSIDER (v5.3 roadmap)
1. **SQLAlchemy 2 async + Postgres-compatible DAL** — one-line toggle from SQLite to Postgres for enterprise deployments.
2. **OpenTelemetry** — tracing for the rare perf bug; trivial to add once, pays for itself long-term.
3. **Plausible self-hosted** — opt-in anonymous usage analytics for AKB1 itself (know what tabs are actually used).
4. **Helm chart** — for the 1-in-100 deployment that wants K8s.
5. **MotherDuck / DuckDB-WASM** — in-browser analytical engine for ≤ 500k-row deployments. Experimental.
6. **tRPC-style typed RPC** — if we grow beyond ~50 endpoints, consider.
7. **Keyv or Redis** — only if caching becomes a bottleneck. Measure before adding.

### REJECT (with reasoning)
- **Kubernetes** — overkill for target audience; adds weeks of install time.
- **MongoDB** — schema flexibility is not a requirement; relational integrity IS.
- **GraphQL** — wrong tool; our endpoints are dashboard-shaped, not graph-shaped.
- **Next.js / SSR** — dashboards don't need SEO; SPA is simpler.
- **JWT with refresh tokens** — v5.2 is single-user self-hosted; basic auth with container-level isolation is sufficient. Add OIDC in v5.4 for enterprise.
- **Electron** — we are not a desktop app.
- **React Native / Flutter** — mobile is out of scope (executives browse on laptops/iPads).
- **Microservices** — every microservice charter ever written was "we need independent scaling" — which we don't.

---

## 6. INDUSTRY BEST PRACTICES WE WILL FOLLOW

Validated against the practices shared by the top-10 applications above (Plausible, Grafana, Metabase, Umami, Homepage, Focalboard, n8n, NocoDB, Appsmith, ToolJet).

| # | Practice | Implementation in AKB1 |
|---|----------|------------------------|
| 1 | 12-Factor App compliance | Env-driven config via Pydantic Settings; stateless app; logs to stdout |
| 2 | Multi-stage Dockerfile | Already in v5.2 backend + frontend Dockerfiles |
| 3 | Health endpoint at `/health` | Present; wired to Docker healthcheck |
| 4 | Semantic versioning | Release tags v5.2.0, v5.2.1, … |
| 5 | Automated CI (lint + test + build) | GitHub Actions workflow in `.github/workflows/ci.yml` |
| 6 | Renovate / Dependabot | Add `.github/dependabot.yml` in v5.2 |
| 7 | CHANGELOG.md (Keep a Changelog format) | Add in v5.2 |
| 8 | Reproducible builds via lock files | `requirements.txt` pinned; `package-lock.json` committed |
| 9 | Structured logs (JSON) | Configure uvicorn + structlog |
| 10 | Metrics endpoint (Prometheus format) | Optional in v5.3 |
| 11 | SBOM generation | CycloneDX step in CI, v5.2 |
| 12 | Container image scanning | Trivy step in CI, v5.2 |
| 13 | Pre-commit hooks (Ruff, Prettier) | `.pre-commit-config.yaml`, v5.2 |
| 14 | Docker image published to GHCR | `ghcr.io/deva-adi/akb1-command-center:5.2.0` |
| 15 | Docs in repo (not wiki) | Already the convention |
| 16 | `docs/` as GitHub Pages source | v5.2 |
| 17 | Issue + PR templates | v5.2 pre-release (K-06/K-07 in MASTER_CHECKLIST) |
| 18 | CODE_OF_CONDUCT | v5.2 pre-release |
| 19 | SECURITY.md with responsible disclosure | v5.2 pre-release |
| 20 | `make dev`, `make test`, `make build` | v5.2 Makefile |

---

## 7. RISK REGISTER FOR STACK CHOICES

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SQLite write contention at scale | Low (audience mismatch) | Medium | Postgres DAL in v5.3; WAL mode; single writer pattern |
| Python GIL performance | Low | Low | Async I/O dominates; CPU work offloaded to pandas/numpy (C) |
| React 18 bundle bloat | Low | Low | Route-level code splitting + Vite tree-shaking |
| Docker-on-Windows idiosyncrasies | Medium | Medium | Tested WSL2 path; documented gotchas in CONTRIBUTING.md |
| openpyxl memory on huge xlsx | Medium | Medium | 50 MB upload cap; streaming read mode for files > 10 MB |
| Breaking changes in FastAPI/Pydantic v2 | Medium | Medium | Pin minor versions; Dependabot alerts |
| No SSO in v5.2 | High | Low (audience is self-hosted single-user) | Document; OIDC in v5.4 |
| Single-container backup = single file = single point of failure | Medium | High | Automated daily backup to volume + external-path hook |

---

## 8. DECISION SUPPORT — 3 OPTIONS

| Option | Type | Description | Risk | Outcome |
|--------|------|-------------|------|---------|
| 1 | Conservative | Ship v5.2 exactly as designed: FastAPI + React + SQLite + Docker Compose. No stack changes. | Low | Stable, predictable, known performance envelope |
| 2 | Balanced (RECOMMENDED) | Ship v5.2 with the surgical ADD list (shadcn, Alembic, Pydantic Settings, React Query, Zustand, Ruff/MyPy, Playwright, openpyxl). | Low–Medium | Higher code quality and contributor velocity; marginal extra complexity |
| 3 | Strategic | Also ship the v5.3 CONSIDER list (Postgres DAL, OpenTelemetry, Helm chart) to be enterprise-ready at launch. | Medium | Eliminates scale ceiling; delays v5.2 by ~4 weeks |

**Recommended: Option 2** — the Balanced path ships a production-grade open-source release now without over-engineering for scale we do not yet need. The Strategic items become v5.3 roadmap with user feedback informing priority.

---

## 9. BENCHMARK SUMMARY TABLE

| Dimension | Best-in-class | AKB1 v5.2 target | Gap closed by | Status |
|-----------|---------------|------------------|---------------|--------|
| Install in ≤ 5 min | Focalboard, Homepage | ✅ | Already met | ✅ |
| Auto-generated API docs | FastAPI | ✅ | Built-in | ✅ |
| Accessibility AA | Grafana | 🟡 | shadcn/ui + axe-core CI check | In plan |
| Migrations automated | Django, Rails | 🟡 | Alembic | In plan |
| Config 12-factor | Plausible | ✅ | Pydantic Settings | In plan |
| Structured logs | Grafana | ✅ | structlog | In plan |
| SBOM + scan | Enterprise best practice | ✅ | Trivy + CycloneDX in CI | In plan |
| Multi-currency aggregation | SAP BPC | ✅ | v5.2 native | ✅ |
| Methodology-adaptive UI | None (unique to AKB1) | ✅ | v5.2 native | ✅ |
| Governed AI velocity | None (unique) | ✅ | v5.2 native | ✅ |

---

## 10. CLOSING POSITION

AKB1's stack is **correct-by-design** for the target audience: a delivery leader who needs to evaluate in 5 minutes, install in 5 minutes, and trust the numbers for 5 years. It borrows the winning patterns from the most adopted open-source dashboards (Plausible, Grafana, Focalboard, Homepage) and adds three capabilities **none of them have**: methodology-adaptive views, governed AI velocity, and multi-currency portfolio aggregation.

No replatforming recommended. Ship v5.2 on the Balanced path (Option 2). Revisit the stack only when a measured constraint — not a hypothetical — forces the next change.
