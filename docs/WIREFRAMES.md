# AKB1 Command Center — WIREFRAMES
**Version:** 5.2 | **Status:** Design Locked | **Author:** Adi Kompalli
**Purpose:** ASCII wireframes + metric narratives for every screen, so evaluators can decide whether to install AKB1 *before* running it. Each tab shows: layout → what it displays → what the numbers mean → who asks for it → why it matters.

---

## GLOBAL LAYOUT

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  [AKB1 ⬛] AKB1 Command Center               [Base ₹ INR ▼] [FY Apr–Mar ▼] [⚙] │
├──────┬────────────────────────────────────────────────────────────────────────┤
│      │                                                                        │
│ Nav  │                     ACTIVE TAB CONTENT                                 │
│ 01   │                                                                        │
│ 02   │                                                                        │
│ ...  │                                                                        │
│ 11   │                                                                        │
│      │                                                                        │
├──────┴────────────────────────────────────────────────────────────────────────┤
│  Last sync: 16 Apr 2026, 09:12 IST    v5.2    github.com/deva-adi/akb1...    │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Brand tokens:** Navy `#1B2A4A` top bar & nav, Ice Blue `#D5E8F0` card surfaces, Amber `#F59E0B` CTAs & alerts.
**Typography:** Inter for UI, JetBrains Mono for numerics.
**Grid:** 12-column, 24px gutter, 1280px minimum width.

---

## NAVIGATION (11 TABS)

| # | Tab | Primary Persona | Core Question Answered |
|---|-----|-----------------|------------------------|
| 1 | Executive Summary | CEO / COO | "How is the portfolio doing this month?" |
| 2 | Programme Portfolio | Delivery Head | "Which programmes are green/amber/red and why?" |
| 3 | Delivery Health | Programme Manager | "Is each project on track across any SDLC framework?" |
| 4 | Velocity & Flow | Agile Coach / RTE | "Is AI-augmented velocity real or illusory?" |
| 5 | Margin & EVM | CFO / Account Director | "Where is margin leaking and by how much?" |
| 6 | Customer Intelligence | CRO / Account VP | "Which clients will renew? Where is expectation gap?" |
| 7 | AI Governance | CTO / CIO | "Are AI tools trustworthy, compliant, productive?" |
| 8 | Smart Ops | Ops Head | "Which early-warning scenarios are firing?" |
| 9 | Risk & Audit | PMO / Compliance | "What is the RAID posture and audit readiness?" |
| 10 | Reports & Exports | All | "Export what I see for my next steering committee." |
| 11 | Data Hub & Settings | Admin | "Configure, import, back up, migrate." |

---

## TAB 1 — EXECUTIVE SUMMARY

```
┌──── EXECUTIVE SUMMARY — Portfolio Snapshot ──────────────────────────────────┐
│                                                                              │
│  ┌──── PORTFOLIO HEALTH ────┐  ┌──── FINANCIALS ─────┐  ┌──── DELIVERY ───┐ │
│  │  🟢 12 Green             │  │  Revenue: ₹48.6 Cr   │  │  On-time:  87%  │ │
│  │  🟡  4 Amber             │  │  Margin:  26.4%      │  │  Budget:   91%  │ │
│  │  🔴  1 Red               │  │  Leakage: ₹1.8 Cr    │  │  Quality:  94%  │ │
│  │   Total 17 programmes    │  │  Forecast ±3.1%      │  │  NPS:      +42  │ │
│  └──────────────────────────┘  └──────────────────────┘  └─────────────────┘ │
│                                                                              │
│  ┌──── 12-MONTH REVENUE & MARGIN TREND ─────────────────────────────────┐   │
│  │  ₹ Cr  ┤                                                             │   │
│  │   60   ┤       ╱╲                                   ╱                │   │
│  │   50   ┤    ╱─╯  ╲─╮    ╱──╮   ╭──╮    ╭────────╯ ← Amber line     │   │
│  │   40   ┤──╯       ╰───╯    ╰──╯  ╰────╯                             │   │
│  │        └────────────────────────────────────────────                │   │
│  │          May Jun Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──── TOP 5 RISKS ──────────────────┐  ┌──── THIS WEEK'S DECISIONS ───┐   │
│  │ 1. FinCo CR overrun  — Sev 1 🔴   │  │ • Approve TCS rate card      │   │
│  │ 2. Retail go-live slip — Sev 2 🟡 │  │ • Close Q4 bench (3 FTE)     │   │
│  │ 3. AI trust drop BBVA  — Sev 2 🟡 │  │ • Release v2 to HealthCo     │   │
│  │ 4. Bench crossing 12%  — Sev 3 🟡 │  │ • Escalate ERP defect SLA    │   │
│  │ 5. Vendor SOC-2 lapse  — Sev 3 🟡 │  │                               │   │
│  └───────────────────────────────────┘  └──────────────────────────────┘   │
│                                                                              │
│  [ Narrative: AI-generated weekly commentary, 2–3 paragraphs ]              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Metric dictionary**

| Metric | What it shows | Why it matters | Formula |
|--------|---------------|----------------|---------|
| RAG bucket count | Programmes by traffic-light status | One-glance portfolio posture | Rules in Section 7 FORMULAS.md |
| Revenue | Sum of invoiced + WIP revenue YTD in base currency | Top-line accountability | Σ(programme_revenue × FX_rate) |
| Margin % | Gross margin after direct cost | Commercial health | (Revenue − Cost) / Revenue × 100 |
| Leakage | Quantified value lost to the 7 loss categories | The number CFOs actually care about | Σ loss_events — Section 7 FORMULAS |
| Forecast ±% | MAPE of last 3 month forecasts vs actuals | Governance maturity signal | Mean absolute % error |
| On-time | % projects delivered within schedule tolerance | Delivery reliability | On-time / Total × 100 |
| Budget adherence | % projects within ±5% of plan cost | Commercial discipline | In-budget / Total × 100 |
| Quality | Composite of defect leakage + CSAT + SLA | Client-visible output | Weighted composite (FORMULAS) |
| NPS | Client Net Promoter Score, rolling 90 days | Renewal signal | % Promoters − % Detractors |

**Who asks for it:** CEO/COO pre-board. **Export:** PDF + PowerPoint one-click.

---

## TAB 2 — PROGRAMME PORTFOLIO

```
┌──── PROGRAMME PORTFOLIO ─────────────────────────────────────────────────────┐
│  [Search ▢] [Status: All ▼] [Client: All ▼] [Methodology: All ▼] [+ New]    │
│                                                                              │
│  ┌─ GridView ─┬─ KanbanView ─┬─ TimelineView ─┐                             │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 🟢 GlobalBank AI Transformation        SAFe   PI 14  ₹12.4 Cr  (USD)│   │
│  │    Margin 29.1%   SPI 1.02   CPI 0.98   NPS +55   Trust 87         │   │
│  │    [Drill]                                                          │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │ 🟡 RetailCo POS Rollout                Waterfall  Ph 4/6  £3.8 M   │   │
│  │    Margin 22.4%   Gate slip 11 days  Phase Variance +8%            │   │
│  │    [Drill]                                                          │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │ 🔴 FinCo Core Upgrade                  Scrum    Spr 23  ₹8.1 Cr    │   │
│  │    Margin 14.2%   CR overrun 18%   Velocity drop 22% WoW           │   │
│  │    [Drill]                                                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Showing 3 of 17 programmes  [◀ Prev 1 2 3 4 5 6 Next ▶]                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Metric dictionary**

| Metric | What it shows | Per methodology |
|--------|---------------|-----------------|
| RAG badge | Current status | Rules adapt: Scrum uses SPI/CPI thresholds; Kanban uses cycle-time SLA; Waterfall uses phase variance |
| Methodology | Scrum / Kanban / Waterfall / SAFe / Hybrid | Drives downstream UI per Tab 3 |
| PI/Sprint/Phase | Current iteration unit | Auto-labelled per methodology |
| Contract value | Programme value in native currency | Tooltip shows converted to base |
| Margin % | Realised margin to date | Common to all |
| SPI / CPI | Earned Value indices | Scrum/Waterfall/SAFe |
| Gate slip | Days behind the last gate review | Waterfall-specific |
| Phase variance | (Actual effort − Planned effort) / Planned | Waterfall-specific |
| Velocity drop | Week-over-week velocity % change | Scrum/SAFe |
| Trust score | AI Governance trust composite | If AI-assisted programme |

**Who asks for it:** Delivery Head pre-portfolio review. **Exports:** Excel filterable table + PDF deck.

---

## TAB 3 — DELIVERY HEALTH (ADAPTS TO METHODOLOGY)

### 3A. Scrum / SAFe View

```
┌──── DELIVERY HEALTH · GlobalBank AI Transformation · SAFe PI 14 ────────────┐
│  Sprint 6/10       Velocity: 82 SP  (3-sprint avg 76)    Predictability 89% │
│                                                                              │
│  ┌── SPRINT BURNDOWN ────────┐   ┌── CUMULATIVE FLOW ──────────────┐        │
│  │  SP                       │   │       ┌──╮                       │        │
│  │ 100 ╲   ideal             │   │ Work  │  ╲    WIP               │        │
│  │  80  ╲╲   actual          │   │       │   ╰──╮                   │        │
│  │  60    ╲──╮               │   │       │      ╰── Done            │        │
│  │  40      ╲╰─╮             │   │       └───────────────           │        │
│  │          D1 D5 D10        │   │        Day 1 … Day 14            │        │
│  └───────────────────────────┘   └──────────────────────────────────┘        │
│                                                                              │
│  SPI 1.02   CPI 0.98   Defect leakage 1.4%  SLA breaches 0   Sev-1 defects 0│
│  Dependencies: 3 cross-team  |  Blockers: 1 (vendor API spec)               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3B. Kanban View

```
┌──── DELIVERY HEALTH · DataOps Platform · Kanban ────────────────────────────┐
│  WIP 14 / limit 18    Throughput 7.2/wk    Cycle time p85: 6.4d   Lead 9.1d │
│                                                                              │
│  ┌── CUMULATIVE FLOW DIAGRAM (8-week) ─────────────────────────────┐        │
│  │  Items                                                          │        │
│  │   60 ┤                                   ═══════ Backlog         │        │
│  │   45 ┤               ───────────         ─────── In Progress    │        │
│  │   30 ┤       ────────                    ───────  Review        │        │
│  │   15 ┤   ────                            ───────  Done           │        │
│  │      └─────────────────────────────                             │        │
│  │        W1 W2 W3 W4 W5 W6 W7 W8                                   │        │
│  └──────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│  WIP Aging   | < 3d  | 3–7d | 7–14d | >14d (🔴)                              │
│  Items       |   6   |   5  |   2   |   1                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3C. Waterfall View

```
┌──── DELIVERY HEALTH · RetailCo POS Rollout · Waterfall Phase 4/6 ──────────┐
│  Plan 18 mo  |  Elapsed 11 mo  |  Remaining 7 mo  |  Gate 4 slipped +11d   │
│                                                                             │
│  Requirements ──┤████████│ 100%  on-time    (2 mo, gate green)              │
│  Design ────────┤████████│ 100%  +4d        (3 mo, gate green)              │
│  Development ───┤████████│ 100%  on-time    (4 mo, gate green)              │
│  Testing (cur)──┤█████───│  62%  +11d       (3 mo plan, now 3.4 mo)         │
│  UAT ───────────┤────────│   0%             (2 mo plan)                     │
│  Deploy ────────┤────────│   0%             (0.5 mo plan)                   │
│                                                                             │
│  Phase variance +8%  |  Gate approval rate 75% (3/4)  |  Milestone slip +11d│
└─────────────────────────────────────────────────────────────────────────────┘
```

**Metric dictionary (all views)**

| Metric | Shows | Target (green) | Alert (red) |
|--------|-------|----------------|-------------|
| Velocity (Scrum) | Story points per sprint | Within ±10% of 3-sprint avg | Drop > 20% WoW |
| Predictability | Delivered SP / Committed SP | ≥ 85% | < 70% |
| SPI | EV / PV | ≥ 0.95 | < 0.85 |
| CPI | EV / AC | ≥ 0.95 | < 0.85 |
| Throughput (Kanban) | Items completed / week | Stable trend | Falling 3 wks |
| Cycle time p85 | 85th percentile time in progress | ≤ SLA | > SLA |
| Lead time | End-to-end customer wait | ≤ SLA | > SLA |
| WIP limit breach | WIP > limit | 0 | Any |
| Phase variance | (Actual − Plan) / Plan | ≤ +5% | > +15% |
| Gate approval rate | Gates passed / gates held | = 100% | < 80% |
| Milestone slip | Days late vs plan | ≤ 3d | > 10d |

---

## TAB 4 — VELOCITY & FLOW (DUAL VELOCITY)

```
┌──── VELOCITY & FLOW · AI-Augmented vs Traditional ──────────────────────────┐
│                                                                              │
│  ┌── DUAL VELOCITY (last 8 sprints) ──────────────────────────────────┐    │
│  │  SP                                                                 │    │
│  │  120 ┤           ╱╲  AI-augmented                                   │    │
│  │   90 ┤        ╱─╯  ╲╮                                               │    │
│  │   60 ┤  ─────╯      ╰──── Traditional                               │    │
│  │      └────────────────────────                                      │    │
│  │         S1  S2  S3  S4  S5  S6  S7  S8                              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌── 6-GATE CONFIDENCE MERGE ──────────────┐                                │
│  │  Gate 1 Code gen     ✅ 94% accepted     │                                │
│  │  Gate 2 Review       ✅ no regressions   │                                │
│  │  Gate 3 Test pass    ✅ 96% pass          │                                │
│  │  Gate 4 Defect leak  🟡 1.6% (target 1%) │                                │
│  │  Gate 5 Cycle time   ✅ −28% vs baseline │                                │
│  │  Gate 6 Productivity ✅ +34% validated    │                                │
│  │  Merged confidence: 82 / 100 (Amber)     │                                │
│  └──────────────────────────────────────────┘                                │
│                                                                              │
│  Productivity uplift  +34%   Code-gen acceptance 64%   AI trust drift −3 WoW│
└──────────────────────────────────────────────────────────────────────────────┘
```

**Metric dictionary**

| Metric | Plain English |
|--------|---------------|
| AI-augmented velocity | SP delivered by teams using Copilot/Cursor/Claude Code |
| Traditional velocity | SP delivered by teams without AI assistance |
| Uplift % | (AI − Trad) / Trad × 100 |
| 6-gate confidence | Composite score 0–100 validating uplift is real, not inflated |
| Code-gen acceptance | % of AI-suggested lines kept after review |
| Defect leakage | Defects escaping to QA as % of total |

**Why it matters:** prevents false productivity claims that blow up in customer audits — a real risk as AI enters delivery. Ties every AI investment to a governed number.

---

## TAB 5 — MARGIN & EVM

```
┌──── MARGIN & EVM · Portfolio Rolled Up (Base ₹ INR) ────────────────────────┐
│                                                                              │
│  ┌── MARGIN WATERFALL ────────────────────────────────────────────────┐    │
│  │  Contracted ──────────────────────────── 31.0%                      │    │
│  │   − Scope creep         ▼ 1.2%                                      │    │
│  │   − Rate concessions    ▼ 0.8%                                      │    │
│  │   − Bench drag          ▼ 0.7%                                      │    │
│  │   − Defect rework       ▼ 0.6%                                      │    │
│  │   − FX slippage         ▼ 0.4%                                      │    │
│  │   − Unbilled CRs        ▼ 0.5%                                      │    │
│  │   − Tool/infra overrun  ▼ 0.4%                                      │    │
│  │  Realised  ─────────────────────────── 26.4%                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌── EVM ─────────────────────┐  ┌── 7 LOSS CATEGORIES ────────────────┐  │
│  │  PV  ₹ 42.1 Cr             │  │ 1. Scope creep         ₹ 58 L 🔴    │  │
│  │  EV  ₹ 39.7 Cr             │  │ 2. Unbilled change     ₹ 24 L 🟡    │  │
│  │  AC  ₹ 40.8 Cr             │  │ 3. Bench drag          ₹ 34 L 🟡    │  │
│  │  SPI 0.94   CPI 0.97       │  │ 4. Rework              ₹ 29 L 🟡    │  │
│  │  EAC ₹ 60.2 Cr             │  │ 5. Rate concession     ₹ 39 L 🟡    │  │
│  │  VAC ₹ −1.8 Cr             │  │ 6. FX slippage         ₹ 20 L 🟢    │  │
│  │  TCPI 1.03                 │  │ 7. Infra/tool overrun  ₹ 19 L 🟢    │  │
│  └────────────────────────────┘  └──────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Metric dictionary**

| Metric | Formula |
|--------|---------|
| Margin | (Revenue − Direct Cost) / Revenue |
| SPI | EV / PV |
| CPI | EV / AC |
| EAC | BAC / CPI |
| VAC | BAC − EAC |
| TCPI | (BAC − EV) / (BAC − AC) |
| Leakage by category | Sum of quantified loss events in the category |

**Why it matters:** Margin leakage is the #1 hidden value destroyer in IT services — CFO board packs live on this tab.

---

## TAB 6 — CUSTOMER INTELLIGENCE

```
┌──── CUSTOMER INTELLIGENCE ──────────────────────────────────────────────────┐
│                                                                              │
│  ┌── CLIENT HEALTH ─────────────────────┐  ┌── RENEWAL PIPELINE ─────┐    │
│  │ Client         CSAT NPS Renewal Prob │  │  <90d   4 contracts     │    │
│  │ GlobalBank       92  +55   94% 🟢    │  │  90–180 3 contracts     │    │
│  │ RetailCo         78  +12   61% 🟡    │  │  180–365 6 contracts    │    │
│  │ FinCo            64  -8    38% 🔴    │  │  >365    4 contracts    │    │
│  │ HealthCo         88  +48   89% 🟢    │  │                          │    │
│  └──────────────────────────────────────┘  └──────────────────────────┘    │
│                                                                              │
│  ┌── 7-DIMENSION EXPECTATION GAP (RetailCo) ────────────────────────────┐  │
│  │                Client expects │ We deliver │ Gap                     │  │
│  │ Speed          Fast launch    │ 18-mo plan │ -2.0 🔴                 │  │
│  │ Cost           ±5% budget     │ +8%        │ -0.5 🟡                 │  │
│  │ Quality        Zero Sev-1     │ 0 Sev-1    │  0   🟢                 │  │
│  │ Scope          Weekly change  │ Monthly CR │ -1.0 🟡                 │  │
│  │ Communication  Bi-weekly exec │ Monthly    │ -0.5 🟡                 │  │
│  │ Innovation     AI embedded    │ Traditional│ -1.5 🔴                 │  │
│  │ Governance     Real-time dash │ PPT pack   │ -1.0 🟡                 │  │
│  │ Gap Index     -6.5 / -14      │                                       │  │
│  └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Metric dictionary**

| Metric | What it shows |
|--------|---------------|
| CSAT | Rolling 30-day survey score |
| NPS | Promoters − Detractors, rolling 90d |
| Renewal probability | Composite model: CSAT + NPS + health + exec engagement |
| 7-Dim gap | Client-stated expectation vs measured delivery per dimension |
| Gap Index | Sum of signed gaps across 7 dimensions (−14 worst, +14 best) |

**Why it matters:** Sales forecasts are worthless without renewal probability; 7-dim gap is an early-warning system for the renewal conversation.

---

## TAB 7 — AI GOVERNANCE

```
┌──── AI GOVERNANCE ──────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌── AI TRUST SCORE (Portfolio) ──┐   ┌── MATURITY LEVELS ─────────┐       │
│  │                                │   │ L1 Ad-hoc        3 prgs    │       │
│  │        ●  82 / 100             │   │ L2 Controlled    6 prgs    │       │
│  │                                │   │ L3 Governed      5 prgs    │       │
│  │ Accuracy    88                 │   │ L4 Optimised     2 prgs    │       │
│  │ Reliability 84                 │   │ L5 Generative    1 prg     │       │
│  │ Explain.    79                 │   └────────────────────────────┘       │
│  │ Bias        81                 │                                         │
│  │ Compliance  90                 │   ┌── 5-CONTROL FRAMEWORK ─────┐       │
│  │ Security    77 🟡              │   │ 1. Data provenance   ✅    │       │
│  └────────────────────────────────┘   │ 2. Model registry    ✅    │       │
│                                       │ 3. Approval workflow ✅    │       │
│                                       │ 4. Monitoring drift  🟡    │       │
│                                       │ 5. Kill-switch       ✅    │       │
│                                       └────────────────────────────┘       │
│                                                                              │
│  [AI Tool Register — Copilot, Cursor, Claude Code, etc.: usage + ROI + risk]│
└──────────────────────────────────────────────────────────────────────────────┘
```

**Why it matters:** board-level AI exposure is top-3 CIO concern. This tab is the audit artefact.

---

## TAB 8 — SMART OPS (EARLY-WARNING SCENARIOS)

```
┌──── SMART OPS · 5 scenarios monitoring 17 programmes ───────────────────────┐
│                                                                              │
│  🔴 Scenario 1: Margin erosion        FIRING on FinCo (−4.8% WoW)            │
│  🟡 Scenario 2: Velocity collapse     AMBER on RetailCo (−11%)                │
│  🟡 Scenario 3: Bench drift           AMBER at 11.8% (threshold 12%)          │
│  🟢 Scenario 4: Customer dissatisfaction  All green                           │
│  🟢 Scenario 5: AI trust drop         All green                               │
│                                                                              │
│  [ Alert routing: email to delivery_head@, Slack #portfolio-alerts ]        │
│  [ Escalation SLA: Sev1 30min, Sev2 4h, Sev3 24h ]                         │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## TAB 9 — RISK & AUDIT (RAID)

```
┌──── RAID REGISTER ──────────────────────────────────────────────────────────┐
│  [Risks 42] [Assumptions 18] [Issues 11] [Decisions 27]                     │
│                                                                              │
│  ID   Title                        Prob  Impact  Exposure  Owner   Status   │
│  R-042 Vendor SOC-2 lapse           M     H       ₹1.2 Cr   NK      Open 🟡  │
│  R-041 Regulator sandbox deadline   H     H       ₹3.0 Cr   AR      Open 🔴  │
│  R-040 FX volatility on USD deals   M     M       ₹40 L     SF      Mit 🟢   │
│                                                                              │
│  [Audit readiness: 92% — 3 controls need evidence re-upload ]               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## TAB 10 — REPORTS & EXPORTS

```
┌──── REPORTS ────────────────────────────────────────────────────────────────┐
│  [ Executive PDF ]   [ Board PowerPoint ]   [ Excel workbook ]              │
│  [ CSV bundle ]      [ JSON snapshot ]      [ Custom builder ]              │
│                                                                              │
│  Saved reports:                                                              │
│   • Weekly_Exec_Summary_2026-04-14.pdf                                       │
│   • Portfolio_Board_2026-Q1.pptx                                             │
│   • EVM_Export_2026-04.xlsx                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## TAB 11 — DATA HUB & SETTINGS

```
┌──── DATA HUB ───────────────────────────────────────────────────────────────┐
│  Ingest:   [Demo mode]  [Upload CSV/XLSX]  [Manual entry]  [API sync]       │
│                                                                              │
│  ┌── DRAG & DROP ─────────────────┐   ┌── TEMPLATES ───────────────┐       │
│  │                                │   │ [programmes.csv]            │       │
│  │    Drop CSV or XLSX here       │   │ [projects.csv]              │       │
│  │    or click to browse          │   │ [sprints.csv]               │       │
│  │    (max 50 MB)                 │   │ [flow_metrics.csv] NEW       │       │
│  │                                │   │ [project_phases.csv] NEW     │       │
│  └────────────────────────────────┘   │ [… 10 more]                  │       │
│                                       └──────────────────────────────┘       │
│                                                                              │
│  Last imports:                                                               │
│   • 2026-04-14 14:22 — programmes.csv — 17 rows — ✅ committed               │
│   • 2026-04-13 09:11 — sprints.xlsx — 340 rows — 🔄 [Rollback]              │
│                                                                              │
│  ┌── SETTINGS ─────────────────────────────────────────────────────────┐   │
│  │  Base currency     [ INR ₹ ▼ ]    Edit exchange rates ▸              │   │
│  │  Fiscal year       [ Apr – Mar ▼ ]                                    │   │
│  │  Number format     [ Indian (lakh/crore) ▼ ]                          │   │
│  │  Date format       [ DD/MM/YYYY ▼ ]                                   │   │
│  │  Backup            [ Daily 02:00 ▼ ]   Last backup 16 Apr 02:01 ✅    │   │
│  │  Schema version    5.2                                                │   │
│  └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## INTERACTION PATTERNS

| Pattern | Where | Behaviour |
|---------|-------|-----------|
| Drill-down | Any card with `[Drill]` | Opens programme-level detail pane |
| Inline edit | Settings, manual entry | Optimistic update + rollback on validation fail |
| Hover tooltip | Every numeric value | Native currency + base currency + formula |
| Export | Tab 10 + every chart | PDF / PPTX / XLSX / CSV / PNG |
| Rollback | Tab 11 import list | Restores snapshot from data_import_snapshots |
| Filter chips | Tabs 2, 5, 9 | Multi-select, persisted per user session |

---

## USE AS PRE-INSTALL EVALUATION TOOL

These wireframes are embedded in the README hero, the EARLY_ADOPTER_FAQ, and the GitHub Pages site so prospective users can:
1. See every screen before cloning.
2. Read the plain-English metric dictionary for each tab.
3. Match the tab contents to questions their CTO/CIO/CEO actually asks.
4. Evaluate fit for their delivery methodology (Scrum/Kanban/Waterfall/SAFe/Hybrid).
5. Confirm currency, fiscal-year, and platform support before any install.

**Recommended copy path for the README:**

> "Before you install AKB1, scroll through WIREFRAMES.md — every screen, every metric, explained in plain English, mapped to the persona who asks for it. If the answers match the questions your leadership asks, AKB1 is for you."
