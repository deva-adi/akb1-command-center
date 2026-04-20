# AKB1 Command Center v5.2 — Demo Guide: NovaTech Solutions Portfolio

**Author:** Adi Kompalli, AKB1 Framework  
**Date:** 2026-04-16  
**Version:** 1.1 (Updated for v5.2)  
**Classification:** Internal — Educational Demo

---

## Prerequisites

| Requirement | Detail |
|-------------|--------|
| Docker Desktop | Running and healthy (`docker info` shows no errors) |
| OS | Windows 10/11 (Docker Desktop + WSL2), macOS, or Linux |
| Browser | Chrome, Firefox, Safari, or Edge (latest 2 major versions) |
| Ports | 9000 (frontend) and 9001 (backend) available |

### Launch the Demo

```bash
# macOS / Linux
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center && ./scripts/setup.sh
open http://localhost:9000

# Windows (PowerShell)
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center
docker compose up -d --build
Start-Process "http://localhost:9000"
```

---

## Executive Summary

This guide walks you through the AKB1 Command Center v5.2 using live demo data from **NovaTech Solutions**, a 150-person IT services unit managing a ₹41M annual portfolio across 5 programmes for a global banking client. The walkthrough is structured to reveal portfolio health, identify performance anomalies, and demonstrate the governance workflows that drive actionable insights and accountability. v5.2 adds SDLC framework-specific demo scenarios (Scrum, Kanban, Waterfall) and multi-currency views.

---

## Portfolio Overview: NovaTech Solutions

**Organization:** NovaTech Solutions IT Services Unit  
**Headcount:** 150 FTE  
**Portfolio Revenue:** ₹41M annually (YTD tracking)  
**Number of Programmes:** 5 active  
**Client Base:** 1 primary (global banking client)  
**Key Governance Concern:** Margin compression and delivery reliability across portfolio

### Programme Roster

| Programme | Budget | Revenue | Team Size | Status | Primary Risk |
|-----------|--------|---------|-----------|--------|--------------|
| **Phoenix Platform Modernization** | ₹10M | ₹10M | 25 FTE | At Risk | Margin loss, scope creep |
| **Atlas Cloud Migration** | ₹8M | ₹8M | 18 FTE | Watch | Margin cliff, bench allocation |
| **Sentinel Quality Engineering** | ₹5M | ₹5M | 12 FTE | On Track | Defect density, AI validation |
| **Orion Data Platform** | ₹12M | ₹12M | 30 FTE | At Risk | Bench tax, legacy overhead |
| **Titan Digital Commerce** | ₹6M | ₹6M | 15 FTE | At Risk | SLA breaches, attrition |
| **TOTAL** | **₹41M** | **₹41M** | **100 FTE** | — | Portfolio margin: ~14% |

---

## Tab-by-Tab Walkthrough

### Tab 1: Executive Overview

**Purpose:** Real-time portfolio snapshot — revenue, margin, schedule adherence, and health scorecards.

**What You'll See:**

1. **Portfolio KPI Cards** (top row)
   - **Revenue Realization:** ₹41M YTD (on target) | YoY growth: -2.1% (below target of +5%)
   - **Blended Portfolio Margin:** 13.8% (target: 22%) | Trend: ↓ declining 2.3% QoQ
   - **On-Time Delivery Rate:** 78% (target: 95%) | Programmes on-time: 2 of 5
   - **Planned vs Actual Cost Ratio:** 1.18 (planned ₹34.7M vs actual ₹41M) | ₹6.3M overrun

2. **Risk Heat Map** (centre)
   - Red zone: Phoenix (scope creep + margin loss), Orion (bench tax), Titan (SLA)
   - Yellow zone: Atlas (margin cliff scenario)
   - Green zone: Sentinel (AI augmentation working)

3. **Monthly Burn Chart**
   - Show cost trend over last 6 months
   - Highlight: acceleration in Q2, particularly in Orion bench cost

4. **Governance Alerts** (bottom panel)
   - **CRITICAL:** 3 uncontrolled change requests in Phoenix totalling ₹1.2M scope
   - **HIGH:** Titan SLA: 2 P1 breaches last quarter, CSAT dropped to 6.8
   - **HIGH:** Atlas margin forecast: breakeven in Month 8 if bench allocation continues
   - **MEDIUM:** Sentinel defect density 1.15x baseline (AI augmentation catching issues, not creating them — validate)

**What to Look For:**

- Compare Portfolio Margin 13.8% to Industry Benchmark (typically 20–24% for IT services). NovaTech is 6–10 points below target.
- Note the divergence: Sentinel margin is healthy (22%), but Phoenix and Orion drag portfolio down.
- Observe that "on-time" is programme-level metric. Dig into Tab 4 (Portfolio) to see project-level granularity.

**Action Questions to Ask:**

1. Why is blended margin declining despite on-target revenue? (Answer: Bench tax in Orion + scope creep in Phoenix)
2. Which programmes are tier-1 accounts vs. margin-optimization targets? (Answer: Phoenix and Orion are strategically critical; Titan is margin-positive but SLA-risky)
3. What is the forecast for Q3 margin recovery? (Answer: Requires bench rationalization in Orion + scope freeze in Phoenix)

---

### Tab 2: KPI Studio

**Purpose:** Deep-dive performance analytics. Define, track, and trend key metrics across programmes.

**What You'll See:**

1. **KPI Library** (left sidebar)
   - **Delivery KPIs:** Schedule Performance Index (SPI), Cost Performance Index (CPI), On-Time Delivery %
   - **Quality KPIs:** Defect Density, Critical Defect Rate, Test Coverage %
   - **People KPIs:** Utilization %, Attrition %, Bench %
   - **Commercial KPIs:** Revenue Realization %, Margin %, Forecast Accuracy %, Contract Variance
   - **AI KPIs:** AI Trust Score (Sentinel-specific), AI Velocity Uplift %, Augmentation Cost-Benefit Ratio

2. **Phoenix Programme — Detailed KPI Trend** (example)
   - **CPI Trend:** Month 1: 0.95 → Month 2: 0.88 → Month 3: 0.81 (declining, scope creep)
   - **Margin Trend:** Month 1: 22% → Month 3: 14% (erosion due to scope + rework)
   - **Schedule Performance:** SPI 0.82 (behind schedule, pulling resources from other programmes)
   - **Forecast to Complete (ETC):** ₹11.8M (original ₹10M BAC + ₹1.8M for uncontrolled CRs)

3. **Sentinel Programme — AI Augmentation KPIs** (example)
   - **AI Trust Score:** 86/100 (model performing well; defect catch rate higher than human baseline)
   - **Velocity Uplift:** +14% over baseline (18 story points/week vs. 15.8 baseline)
   - **Defect Density:** 1.15x baseline (expected — AI is finding more defects early, reducing production issues)
   - **Cost per QA Hour:** -18% (AI augmentation improving productivity)

4. **Orion Programme — Bench & Overhead KPIs** (example)
   - **Utilization Rate:** 62% (target: 85%) | Bench Allocation: ₹1.4M annually
   - **Revenue per FTE:** ₹400k (target: ₹510k) | Variance: -21%
   - **Bench Cost as % of Programme Margin:** 28% (unsustainable)
   - **Forecast Margin Impact if bench reduced by 30%:** +₹420k (margin would improve to 18%)

5. **Titan Programme — SLA & Customer Health** (example)
   - **SLA Compliance:** 98.1% (target: 99.9%) | Last quarter: 2 P1 breaches (30min + 45min downtime)
   - **CSAT Score:** 6.8/10 (down from 8.2 last year) | Root cause: SLA breaches + team attrition
   - **Attrition Rate:** 25% (target: 8%) | 2 of 8 senior engineers left in last 2 quarters
   - **Rework Cost:** ₹280k (8% of programme revenue, tied to attrition-driven quality decline)

6. **Custom KPI Comparison** (tool)
   - Filter by programme, date range, KPI set
   - Compare programmes side-by-side (e.g., Margin % across all 5 programmes)
   - Export trends to PowerPoint or PDF

**What to Look For:**

- **CPI < 1.0 signals scope creep or productivity loss.** Phoenix's 0.81 is critical.
- **Defect density trending is often a leading indicator of attrition or technical debt.** Titan's increase correlates with team turnover.
- **Bench allocation >20% of programme margin is a value destruction signal.** Orion at 28% is unsustainable.
- **AI Trust Score + Velocity Uplift without defect density increase = successful AI integration.** Sentinel is the model case.

**Action Questions to Ask:**

1. Why is Phoenix's CPI declining while schedule is also slipping? (Answer: Scope creep + rework cycle, not resource shortage)
2. Is Sentinel's higher defect density a quality problem or a detection improvement? (Answer: Detection improvement — defects are caught in test, not production)
3. What would happen to Orion's margin if we reduce bench from 30 FTE to 24 FTE? (Answer: Margin improves ₹420k, but risk to future project capacity increases)

---

### Tab 3: Delivery Planning (v5.1-beta, not available in v5.0-alpha)

*This tab will be added in v5.1-beta. Reserved for future roadmap.*

---

### Tab 4: Portfolio — Programme & Project View

**Purpose:** Hierarchical programme-to-project breakdown. Scope, schedule, and resource allocation visibility.

**What You'll See:**

1. **Programme Summary Cards** (top)
   - Phoenix: 4 active projects | 25 FTE allocated | CPI 0.81 | Margin 14%
   - Atlas: 3 active projects | 18 FTE | CPI 0.94 | Margin 8%
   - Sentinel: 2 active projects | 12 FTE | CPI 1.04 | Margin 22%
   - Orion: 5 active projects | 30 FTE | CPI 0.97 | Margin 16% (before bench tax)
   - Titan: 3 active projects | 15 FTE | CPI 0.89 | Margin 18%

2. **Phoenix Programme Detail** (example drill-down)
   - **Project 1: Core Banking Module**
     - Start: Jan 2025 | End: Jun 2025 | BAC: ₹4.2M | Revenue: ₹4.2M
     - Current Status: 68% complete | CPI: 0.76 | Schedule Variance: -₹180k
     - Uncontrolled CRs: 2 (totalling ₹580k scope impact)
     - Risk: Rework cycle on core modules due to evolving regulatory requirements
   
   - **Project 2: Payment Gateway Integration**
     - Start: Feb 2025 | End: Jul 2025 | BAC: ₹3.1M | Revenue: ₹3.1M
     - Current Status: 52% complete | CPI: 0.82 | Schedule Variance: -₹95k
     - Uncontrolled CRs: 1 (₹220k scope impact)
     - Risk: Third-party API integration delays (vendor-side)
   
   - **Project 3: Regulatory Compliance Module**
     - Start: Mar 2025 | End: Aug 2025 | BAC: ₹2.7M | Revenue: ₹2.7M
     - Current Status: 35% complete | CPI: 0.87 | Schedule Variance: -₹120k
     - Uncontrolled CRs: 0 (but 1 pending change request under review)
     - Risk: Compliance requirements changing monthly; scope definition incomplete

   - **Programme-level Aggregates**
     - Total BAC: ₹10M | Total Revenue: ₹10M | Total Spent to Date: ₹7.8M (78%)
     - Portfolio CPI: 0.81 | Schedule Health: -₹395k behind plan
     - Earned Value: ₹6.3M | Planned Value: ₹7.8M | Variance: -₹1.5M

3. **Cross-Programme Resource Heat Map**
   - Show allocation % for each resource pool: architects, senior engineers, QA, DevOps
   - Identify bottlenecks: e.g., 5 shared architects across 5 programmes, causing context-switch overhead
   - Highlight: 2 senior architects allocated 120% (shared across Phoenix and Orion)

4. **Gantt View** (simplified, full version in v5.2)
   - Visual timeline showing programmes and projects
   - Colour-coded by status: Green (on-track), Yellow (at-risk), Red (off-track)
   - Show critical path and dependencies

**What to Look For:**

- **CPI < 0.9 combined with uncontrolled CRs = scope creep, not productivity loss.** Phoenix's 0.81 + 3 CRs confirms this.
- **Schedule variance on all three Phoenix projects indicates systemic issue,** not isolated project problems.
- **Shared resource pools (architects) allocated >100% across programmes = context-switch cost and quality risk.**

**Action Questions to Ask:**

1. Why are uncontrolled CRs accumulating in Phoenix but not in Sentinel? (Answer: Phoenix had incomplete requirements; Sentinel benefited from Agile refinement approach)
2. If we freeze scope in Phoenix, what is the revised margin and schedule? (Answer: Margin improves to 19%, schedule slips 6 weeks)
3. What is the impact of shared architect pool on delivery? (Answer: Context switching costs ~15% velocity loss; dedicated pool would improve both delivery and quality)

---

### Tab 5: Risk & Governance (v5.1-beta, not available in v5.0-alpha)

*This tab will be added in v5.1-beta. Reserved for future roadmap.*

---

### Tab 6: AI Governance (v5.2-release, not available in v5.0-alpha)

*This tab will be added in v5.2-release. Reserved for future roadmap.*

---

### Tab 7: Smart Ops (v5.2-release, not available in v5.0-alpha)

*This tab will be added in v5.2-release. Reserved for future roadmap. Background scheduler for autonomous governance.*

---

### Tab 8: Commercials

**Purpose:** Revenue, margin, cost tracking, and commercial P&L accountability.

**What You'll See:**

1. **Portfolio P&L Summary**
   - **Revenue:** ₹41M (on target)
   - **Cost of Delivery (CoD):** ₹35.2M (85.9% of revenue)
     - Labour: ₹29.4M (71.5%)
     - Infrastructure & Tools: ₹3.2M (7.8%)
     - Subcontracting & Vendor: ₹2.6M (6.3%)
   - **Gross Margin:** ₹5.8M (14.1%)
   - **Overhead & G&A Allocation:** ₹2.1M (5.1% of revenue)
   - **Net Margin:** ₹3.7M (9.0%)
   - **Portfolio Status:** Below target margin of 22%

2. **Programme-Level Commercial Dashboard**
   
   | Programme | Revenue | CoD | Gross Margin | Margin % | Trend | Status |
   |-----------|---------|-----|--------------|----------|-------|--------|
   | Phoenix | ₹10M | ₹8.6M | ₹1.4M | 14% | ↓ | At Risk |
   | Atlas | ₹8M | ₹7.4M | ₹0.6M | 8% | ↓ | Watch |
   | Sentinel | ₹5M | ₹3.9M | ₹1.1M | 22% | → | On Track |
   | Orion | ₹12M | ₹10.1M | ₹1.9M | 16%* | → | At Risk (bench) |
   | Titan | ₹6M | ₹4.9M | ₹1.1M | 18% | ↓ | At Risk |
   | **Total** | **₹41M** | **₹35.2M** | **₹5.8M** | **14.1%** | **↓** | — |
   
   *Orion margin is 16% before bench tax allocation; actual margin post-overhead is ~13%

3. **Cost Breakdown by Programme**
   - Phoenix: Labour ₹7.8M (90%), Infrastructure ₹0.6M, Vendor ₹0.2M
   - Orion: Labour ₹9.1M (90%), Infrastructure ₹0.7M, Vendor ₹0.3M
   - (Pattern: ~90% labour cost across all programmes; AI augmentation in Sentinel optimizing this to 78%)

4. **Bench Cost Allocation & Impact**
   - Total bench FTE: 12 (across portfolio)
   - Bench cost: ₹1.4M annually (₹116k per FTE)
   - Primary driver: Orion (8 FTE bench), because programme backlog is cyclical
   - Impact on portfolio margin: -3.4 percentage points
   - Scenario: If bench reduced by 30% (reduces capacity by 20%), portfolio margin improves to +16.8%

5. **Revenue Forecast & Variance**
   - Q1 Revenue: ₹9.5M (achieved)
   - Q2 Revenue: ₹10.2M (forecast)
   - Q3-Q4 Revenue: ₹10.7M + ₹10.6M (forecast, at risk if Phoenix schedule slips further)
   - YTD vs Plan: On target; FY forecast variance: -1% (conservative due to Phoenix risk)

6. **Change Request Financial Impact** (Phoenix focus)
   - **CR 001:** Core banking security hardening | ₹420k scope impact | Status: Approved (not yet started)
   - **CR 002:** Payment gateway load testing | ₹320k scope impact | Status: Approved (in progress, scope creeping)
   - **CR 003:** Regulatory compliance data extraction | ₹460k scope impact | Status: Pending approval (high risk)
   - **Total Uncontrolled Scope:** ₹1.2M (12% of Phoenix budget) | **Action Required:** Scope freeze or re-baseline required

**What to Look For:**

- **Labour is 71.5% of CoD across portfolio; any 1% productivity gain = ₹291k cost savings.**
- **Bench cost at 3.4% of margin is controllable and the fastest way to improve portfolio margin by 2–3 percentage points.**
- **Three uncontrolled CRs in Phoenix = margin loss path; CRs should be tracked as change control to revenue.**
- **Orion appears healthy at 16% margin, but post-overhead allocation and bench tax, real margin is ~12–13%.**

**Action Questions to Ask:**

1. What is the break-even point for Atlas programme if bench allocation continues? (Answer: Month 8; requires immediate margin recovery plan)
2. If we reduce Orion bench by 50%, what is new portfolio margin? (Answer: Portfolio margin improves to 16.1%, but Orion capacity planning becomes constrained)
3. What is the cost of each uncontrolled CR in Phoenix if approval takes 2 more months? (Answer: ₹280k in extended labour; each month of delay costs ₹140k)

---

### Tab 9: Settings

**Purpose:** Configuration, demo data management, and system administration.

**What You'll See:**

1. **Demo Mode Toggle**
   - Switch between "Live Data" and "Demo Data" modes
   - Demo data is reset-able for training and presentation purposes

2. **Data Seeding Options**
   - **Load NovaTech Solutions Profile:** Populates all 5 programmes, 15 projects, 3 months of EVM data
   - **Load Sample Governance Scenarios:** Pre-configured risk, change control, and governance workflows
   - **Reset to Baseline:** Clears all data and resets to v5.0-alpha initial state

3. **KPI Configuration**
   - Define custom KPIs for your organization
   - Set targets, thresholds, and alert levels
   - Map KPI to programmes or projects

4. **User Roles & Permissions** (stub for v5.2)
   - Admin, PMO Lead, Programme Manager, Project Manager, Finance Lead, Stakeholder
   - Currently, demo mode has admin-only access; v5.2 adds RBAC

5. **Export & Reporting**
   - Generate PDF executive summary
   - Export KPI trends to Excel
   - Generate audit trail reports (for compliance)

6. **System Logs & Audit Trail**
   - Timestamp of data changes
   - User actions (currently: demo mode only)
   - Forecast recalculations

---

## Learning Pathways

### Pathway 1: The Portfolio Margin Crisis (30 minutes)
**Goal:** Understand why portfolio margin is at 14% instead of 22% and identify recovery levers.

1. Start at **Tab 1 (Executive Overview):** Identify that blended margin is 13.8%, ↓ declining.
2. Go to **Tab 8 (Commercials):** Drill into cost structure.
   - Observation: Bench cost in Orion is ₹1.4M (3.4% of margin).
   - Observation: Phoenix CRs are ₹1.2M uncontrolled scope.
3. Go to **Tab 2 (KPI Studio):** Trend CPI for each programme.
   - Observation: Phoenix CPI declining (scope creep).
   - Observation: Orion has healthy CPI but bench utilization at 62%.
4. Decision Point: Which lever is fastest to move margin? (Answer: Bench rationalization in Orion saves ₹420k immediately; CR freeze in Phoenix saves ₹1.2M but requires scope conversation with client.)

### Pathway 2: The AI Augmentation Bet (20 minutes)
**Goal:** Validate that AI integration in Sentinel is improving both delivery and margin without increasing defect risk.

1. Start at **Tab 2 (KPI Studio),** filter to Sentinel programme.
   - Observation: AI Trust Score 86/100, Velocity Uplift +14%.
2. Cross-check **Defect Density:** 1.15x baseline (not a sign of degradation).
   - Interpretation: AI is catching MORE defects in test phase, reducing production risk.
3. Check **Margin Impact:** Sentinel at 22%, while portfolio average is 14%.
   - Observation: AI augmentation is improving unit economics.
4. Decision Point: Should NovaTech expand AI augmentation to other programmes? (Answer: Yes, but sequence matters — Orion next, given bench constraints.)

### Pathway 3: The SLA & Attrition Spiral (25 minutes)
**Goal:** Understand how Titan's SLA failures are linked to attrition and how to break the cycle.

1. Start at **Tab 1 (Executive Overview):** Note Titan's critical alert about 2 P1 breaches.
2. Go to **Tab 2 (KPI Studio),** filter to Titan.
   - SLA Compliance: 98.1% (target: 99.9%) | CSAT: 6.8 (down from 8.2)
   - Attrition: 25% (target: 8%)
3. Drill into **Root Cause:**
   - Q1 2025: 2 senior engineers resigned.
   - Result: Remaining team absorbed extra load, causing fatigue and quality lapses.
   - Result: 2 P1 breaches in last quarter (each tied to missing a known workaround due to team fatigue).
4. Go to **Tab 8 (Commercials):** Check rework cost.
   - Rework: ₹280k (8% of programme revenue).
5. Decision Point: What is the cost of retaining 1 senior engineer vs. cost of SLA breach? (Answer: Retention bonus ₹80k << ₹280k rework cost + CSAT impact.)

### Pathway 4: The Scope Creep in Phoenix (35 minutes)
**Goal:** Quantify the scope creep in Phoenix and understand the alternatives (re-baseline, scope freeze, or extend timeline).

1. Start at **Tab 4 (Portfolio),** drill into Phoenix.
   - Observation: 3 uncontrolled CRs totalling ₹1.2M scope.
   - Observation: CPI declining from 0.95 to 0.81 over 3 months.
2. Go to **Tab 8 (Commercials):** Analyze impact on Phoenix margin.
   - Current margin: 14% (target: 22%)
   - If all 3 CRs are approved as-is, margin drops to 10%.
3. Model Scenarios:
   - **Scenario A (Scope Freeze):** Reject all pending CRs. Margin: 19%, Schedule: On-time. Client impact: High (unmet requirements).
   - **Scenario B (Approved & Re-baseline):** Approve CRs, extend timeline 12 weeks, add 2 FTE. Margin: 15%, Schedule: Extended. Client impact: Managed (transparent re-plan).
   - **Scenario C (Partial Approval):** Approve CRs 001 & 002 (₹740k), defer CR 003. Margin: 16%, Schedule: 6-week slip. Client impact: Medium.
4. Decision Point: Which scenario minimizes client relationship risk while protecting margin? (Answer: Scenario B is preferable if client can accept 12-week slip; otherwise, Scenario C is compromise.)

---

## Governance Workflows Demonstrated

### 1. Change Control Review (Phoenix CR governance)
- **Trigger:** CR submitted (e.g., CR 003 at ₹460k)
- **Governance Step 1:** Financial Impact Assessment (Tab 8 shows ₹460k scope cost)
- **Governance Step 2:** Schedule Impact (Tab 4 shows 4-week slip if approved)
- **Governance Step 3:** Margin Impact (margin drops from 14% to 12% if approved)
- **Governance Step 4:** Client Conversation (if approved, requires re-baseline and timeline extension)
- **Outcome:** Recommendation to defer until Phase 2 or negotiate extended timeline

### 2. Bench Rationalization (Orion cost control)
- **Trigger:** Monthly governance review shows 62% utilization on Orion (benchmark: 85%)
- **Analysis:** ₹1.4M bench cost annually (28% of programme margin)
- **Scenario Modelling:** 30% bench reduction saves ₹420k with acceptable capacity risk
- **Recommendation:** Transition 2 FTE to billable projects; 6 FTE retained for backlog absorption
- **Outcome:** Portfolio margin improves from 14% to 16%

### 3. Attrition Response (Titan SLA recovery)
- **Trigger:** CSAT drops to 6.8; 2 senior engineers resign; SLA breaches occur
- **Root Cause Analysis:** Fatigue + workload imbalance after team reduction
- **Intervention:** Retention bonus for critical roles + onboarding plan for 2 new hires
- **Timeline:** New hires ramped by Month 6 (estimated)
- **Expected Outcome:** CSAT recovery to 7.8+ by end of Q3

### 4. AI Augmentation Expansion (Sentinel success to Orion)
- **Trigger:** Sentinel demonstrates +14% velocity uplift without quality degradation
- **Evaluation:** Sentinel AI Trust Score 86/100; Defect Density 1.15x (improvement signal, not degradation)
- **Candidate:** Orion Data Platform (large QA footprint, high test automation potential)
- **Proposal:** Pilot AI augmentation for Orion data pipeline testing (Months 5–6)
- **Expected Benefit:** If successful, +8% velocity + margin improvement of ₹300k annually

---

## Key Takeaways & Discussion Questions

1. **Portfolio Visibility:** The Command Center consolidates 5 programmes, 15 projects, and 100 FTE into a unified governance view. What decisions would you make differently with this visibility vs. relying on programme-level reports alone?

2. **Margin Recovery Levers:** Three primary levers are visible: bench rationalization, scope control, and AI augmentation. Which would you prioritize first, and why?

3. **Risk Trade-offs:** Rejecting Phoenix CRs improves margin but damages client relationship. Accepting them protects relationship but erodes margin. How do you navigate this trade-off in your governance model?

4. **AI Governance:** Sentinel demonstrates successful AI augmentation. What metrics would you require before expanding AI to other programmes?

5. **Attrition Linkage:** Titan's attrition directly caused SLA failures and rework cost. How should attrition risk be modelled into programme delivery confidence?

---

## v5.2 Demo Scenarios: SDLC Framework Compatibility

### Scenario 5: Kanban Flow Analysis (DATAOPS-001)

**Setup:** DATAOPS-001 project uses Kanban methodology. Demo data includes 5 weeks of flow metrics.

1. Navigate to **Tab 3B (Delivery Health → Kanban sub-view)**.
2. Observe the **Cumulative Flow Diagram** — look for widening bands (indicates bottleneck).
3. Check **WIP Aging Heatmap** — items in red have exceeded p85 cycle time.
4. **Throughput trend:** Week of Mar 22 = 9 items (best week). Week of Mar 15 = 6 items (worst — 6.5 hrs blocked).
5. **Discussion Point:** "When blocked time spikes, throughput drops. What is the external dependency causing the blocked hours, and can we decouple?"

### Scenario 6: Waterfall Gate Review (RETAILCO-POS)

**Setup:** RETAILCO-POS project uses Waterfall methodology. Demo data includes 6 phases.

1. Navigate to **Tab 3C (Delivery Health → Waterfall sub-view)**.
2. Observe the **Milestone Timeline** — Requirements, Design, Development gates all passed.
3. **Testing phase** at 62% with +11 day slip. UAT blocked — not started.
4. **Gate Status Badges:** 3 passed ✅, 1 pending ⏳, 2 not started.
5. **Discussion Point:** "The Testing slip cascades to UAT. If Testing doesn't recover, the August 15 deployment target slips by at least 11 days. What is the recovery plan?"

### Scenario 7: Multi-Currency Portfolio View

1. Navigate to **Tab 1 (Executive Summary)** — observe portfolio total in base currency (INR ₹).
2. Navigate to **Tab 5 (Margin & EVM)** — observe the multi-currency aggregation panel.
3. **Discussion Point:** "If GBP strengthens by 5%, how does that impact our UK programme costs and blended portfolio margin?"

---

## Next Steps in the Demo

- **Live Scenario Modelling:** Use Tab 5 to model a Phoenix scope freeze vs. re-baseline decision.
- **Kanban Flow Deep Dive:** Drill into Tab 3B to investigate blocked time patterns on DATAOPS-001.
- **Waterfall Gate Review:** Walk through Tab 3C to assess RETAILCO-POS recovery options.
- **KPI Export:** Export Sentinel KPI trends to PowerPoint for stakeholder presentation.
- **Audit Trail:** Review Tab 9 logs to see all change requests and governance decisions made on this portfolio.
- **Custom Report:** Generate a PDF executive summary suitable for CIO or CFO review.

---

**End of Demo Guide — v5.2**

For questions or walkthrough requests, contact Adi Kompalli (AKB1 Framework).
