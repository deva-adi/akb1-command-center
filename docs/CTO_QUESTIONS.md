# CTO QUESTIONS — AKB1 Command Center v5.2

## Overview

This document maps 58 executive-level questions a CTO/CIO/CEO might ask to the AKB1 Command Center dashboards, data tables, and metric cards that answer them. Each question is organized by category and includes the dashboard location, key metrics, and a sample answer format.

**v5.2 Update:** Added 8 new questions across Kanban & Flow (3), Waterfall & Milestones (2), and Multi-Currency & Fiscal Year (3) categories — reflecting SDLC framework compatibility and multi-currency support.

---

## FINANCIAL (10 Questions)

### Q1: What is our total programme revenue this quarter and are we on track to annual targets?

**Which Tab:** Financial → Revenue Dashboard  
**Data Tables:** kpi_monthly (realized_revenue), programmes (BAC)  
**Metrics Displayed:**
- Quarterly Realized Revenue (actual billed)
- Committed Revenue (milestones due this period)
- Annual Revenue Target vs. Actual
- Revenue Realisation % (% of committed converted to realized)

**Chart Types:**
- Bar chart: Quarterly revenue by programme
- Line chart: YTD actual vs. plan revenue trend

**Sample Answer:**
"Q2 2024 realized revenue is USD 1.28M against USD 1.5M committed, achieving 85% realisation. This is USD 220k below plan due to Fintech milestone delays (2-week slip). Healthcare and Logistics tracking well; we're on pace for USD 5.2M annual target if Fintech recovers in Q3."

---

### Q2: Which programmes are at cost risk and what is the projected cost overrun?

**Which Tab:** Financial → Cost Forecast  
**Data Tables:** kpi_monthly (actual_cost, earned_value), programmes (BAC)  
**Metrics Displayed:**
- CPI (Cost Performance Index) by programme
- EAC (Estimate At Completion) vs. BAC
- VAC (Variance At Completion) — dollar overrun
- TCPI (To-Complete Performance Index) — feasibility of remaining work

**Chart Types:**
- Gauge: CPI per programme (red <0.95, yellow 0.95–1.0, green >1.0)
- Table: EAC vs. BAC with variance $ and %
- Waterfall: Budget utilization vs. forecast

**Sample Answer:**
"Fintech is at risk with CPI of 0.903 (9.7% cost overrun). EAC is USD 3.54M vs. BAC of USD 3.2M, projecting a USD 344k overrun. TCPI required to finish is 0.980, which is tight given current cost inefficiency. Recommend immediate corrective action: resource re-optimization or scope reduction. Healthcare is healthy (CPI 1.059, USD 280k savings projected)."

---

### Q3: What is our blended gross margin and are we protecting profitability?

**Which Tab:** Financial → Profitability  
**Data Tables:** kpi_monthly (realized_revenue, actual_cost), financials (category breakdown)  
**Metrics Displayed:**
- Gross Margin % (revenue - labour / revenue)
- Contribution Margin % (revenue - labour - variable overhead)
- Net Margin % (revenue - all costs)
- Portfolio Margin % (blended across all programmes)

**Chart Types:**
- Stacked bar: Margin by programme
- Line trend: Gross/Net margin YTD
- Waterfall: Revenue → Labour → Overhead → Net Margin decomposition

**Sample Answer:**
"Q2 portfolio gross margin is 39.7% (target 40–50%); healthy. However, net margin after overhead is 18.2%, down from 21% in Q1 due to higher bench carry (USD 120k/month). If we reallocate 4 bench FTE by month-end, we can recover 1.5% net margin. Primary risk: Fintech at 20% gross margin due to tight pricing; needs pricing reset or cost reduction."

---

### Q4: How much revenue are we losing to scope absorption and unplanned work?

**Which Tab:** Financial → Leakage Analysis  
**Data Tables:** losses (loss_hours, loss_cost_usd), kpi_monthly (billable_hours)  
**Metrics Displayed:**
- Revenue Leakage % (loss hours / total billable hours)
- Scope Absorption Cost ($ loss from unplanned scope)
- Scope Absorption Cost as % of contract value
- Unplanned Work Hours by programme

**Chart Types:**
- Pie: Leakage breakdown (scope absorption, rework, unplanned, bench)
- Line trend: Leakage % by month (moving average)
- Table: Loss detail by category, root cause, mitigation

**Sample Answer:**
"Total revenue leakage is 6.2% of billable hours (USD 18.6k this month). Breakdown: 3.8% scope absorption (no change control), 1.5% rework (quality issues), 0.9% unplanned work. Healthcare has tightest change control (2.1% leakage); Fintech highest (12.8%). Recommend formal change control audit for Fintech—current process is broken."

---

### Q5: What is our cash flow forecast and will we have sufficient funds for Q3 operations?

**Which Tab:** Financial → Cash Flow  
**Data Tables:** kpi_monthly (realized_revenue, actual_cost), financials (transaction_date, amount)  
**Metrics Displayed:**
- Monthly Cash Inflow (realized revenue billed and collected)
- Monthly Cash Outflow (payroll, vendor, overhead)
- Net Cash Position (cumulative)
- Days Cash on Hand (DCO)
- ETC (Estimate To Complete) remaining spend

**Chart Types:**
- Waterfall: Inflow vs. Outflow by month
- Line: Cumulative cash position YTD
- Forecast: Projected cash position Q3

**Sample Answer:**
"Q2 ending cash position is positive USD 340k; sufficient for Q3 operations. Monthly burn rate is USD 1.2M (labour + overhead); we have ~3.5 weeks of runway. Revenue collection is lagging 5 days vs. standard net-30 terms (cash squeeze risk). ETC across all programmes is USD 8.1M through completion; all within available budget. Recommend accelerating revenue collection efforts and managing vendor payment terms."

---

### Q6: What percentage of our budget remains unspent and what is the burn rate trend?

**Which Tab:** Financial → Budget Burn  
**Data Tables:** programmes (BAC), kpi_monthly (actual_cost cumulative)  
**Metrics Displayed:**
- Budget Remaining % (unspent / BAC)
- Monthly Burn Rate (USD/month)
- Cumulative Burn Rate (actual spend YTD / budgeted YTD)
- Days to Budget Exhaustion (remaining budget / daily burn)

**Chart Types:**
- Gauge: Remaining budget % (red <20%, yellow 20–40%, green >40%)
- Line: Cumulative spend vs. plan (S-curve)
- Bar: Monthly burn rate by programme
- Table: Budget detail by cost category (labour, overhead, vendor)

**Sample Answer:**
"Overall budget remaining: 42% (USD 5.2M of USD 12.4M portfolio BAC). Burn rate is USD 1.65M/month (up 8% from Q1 due to Fintech ramp-up). At current burn, portfolio exhaustion in 45 weeks (on target for planned completion dates). Healthcare at 44% remaining; Fintech at 28% (accelerating; cost overrun risk). Contingency reserve (10% = USD 1.24M) still intact."

---

### Q7: Which client contracts are most profitable and which are at risk?

**Which Tab:** Financial → Contract Analysis  
**Data Tables:** programmes, kpi_monthly, financials  
**Metrics Displayed:**
- Net Margin % by contract
- CPI & SPI by contract
- Revenue per FTE
- Contract burn rate vs. committed milestones

**Chart Types:**
- Bar: Net margin by programme (green >20%, red <10%)
- Scatter: CPI (x) vs. SPI (y) by programme
- Table: Contract profitability scorecard (margin, CPI, SPI, DHI)

**Sample Answer:**
"Most profitable: Healthcare (25% net margin, CPI 1.059, strong delivery). At risk: Fintech (negative profitability, CPI 0.903, 20% schedule slip). Logistics is sweet spot (18% margin, CPI 1.025, on schedule). Public Sector (new, fixed-price) has thin 8% margin; pricing aggressive. Recommend: (1) Fintech corrective action plan, (2) Pricing reset for Public Sector, (3) Healthcare as reference model."

---

### Q8: What are our fixed vs. variable costs and what is our breakeven point per programme?

**Which Tab:** Financial → Cost Structure  
**Data Tables:** financials (category breakdown), resources (loaded_cost), programmes (BAC)  
**Metrics Displayed:**
- Fixed Costs (PMO, infrastructure, fixed overhead)
- Variable Costs (labour, vendor, travel)
- Contribution Margin (revenue - variable cost)
- Breakeven Revenue (fixed cost / contribution margin %)
- Breakeven point by programme

**Chart Types:**
- Stacked bar: Fixed vs. variable cost by programme
- Line: Contribution margin % vs. breakeven threshold
- Table: Breakeven analysis detail

**Sample Answer:**
"Healthcare fixed costs are USD 120k/month (PMO, infrastructure); variable 65% (labour, vendor). Contribution margin 38% of revenue; breakeven is USD 315k/month revenue. Currently generating USD 480k; 52% above breakeven—strong cushion. Fintech has higher fixed costs (USD 95k/month for specialized QA); breakeven USD 380k revenue. Currently at USD 315k; below breakeven. Cost reduction required."

---

### Q9: What is the impact of change requests on our budget and timeline?

**Which Tab:** Financial → Change Management  
**Data Tables:** change_requests (estimated_effort_hours, estimated_cost_impact_usd), kpi_monthly  
**Metrics Displayed:**
- Change Requests Approved vs. Submitted
- Total Approved Change Value ($ impact)
- CR Processing Cost (admin overhead)
- CR Cycle Time (days from submitted to approved)
- Scope absorbed vs. authorized changes

**Chart Types:**
- Funnel: Submitted → Approved → Implemented by status
- Bar: Approved CR value by programme
- Time series: CR volume and value trend
- Table: CR detail with impact decomposition (schedule, cost, resource)

**Sample Answer:**
"Healthcare has 6 approved CRs totaling USD 285k cost impact and 4 weeks schedule extension—well-managed via formal change control (8-day cycle time). Fintech has 12 submitted CRs, only 3 approved (USD 95k), 9 pending—indicating weak gate control. Processing cost (admin) is USD 7.1k/month (Fintech high due to volume). Scope absorption without CR is USD 2.9k/month (Healthcare) vs. USD 4.75k (Fintech)—formal process gap."

---

### Q10: What is our fee realization rate and are we billing what we've earned?

**Which Tab:** Financial → Revenue Management  
**Data Tables:** kpi_monthly (committed_revenue, realized_revenue), programmes (BAC, delivery_model)  
**Metrics Displayed:**
- Revenue Realisation % (realized / committed)
- Monthly Realization Trend
- Days Sales Outstanding (DSO) — time to collect
- Unbilled Earned Value (work done, not yet billed)

**Chart Types:**
- Bar: Monthly realisation % by programme
- Line: Cumulative realized vs. committed YTD
- Waterfall: Committed → Invoiced → Collected
- Aging: Days unbilled by milestone/phase

**Sample Answer:**
"Portfolio realization rate is 89% (USD 1.28M realized of USD 1.44M committed this quarter)—slightly below 90% target. Healthcare at 96% (well-managed milestone billing); Fintech at 72% (2-week delivery slip causing invoice holds). Unbilled earned value is USD 180k (primarily Fintech rework phase pending UAT sign-off). DSO is 32 days (target 30 days); working capital impact USD 45k. Recommend expedite Fintech UAT to unlock billing."

---

## DELIVERY (5 Questions)

### Q11: What is our schedule performance and are we tracking to committed dates?

**Which Tab:** Delivery → Schedule Performance  
**Data Tables:** kpi_monthly (earned_value, planned_value), sprints (completed_story_points, planned_story_points)  
**Metrics Displayed:**
- SPI (Schedule Performance Index)
- Schedule Variance ($ and %)
- Planned vs. Actual Milestone Dates
- Sprint Velocity trend

**Chart Types:**
- Gauge: SPI by programme (red <0.90, yellow 0.90–0.95, green ≥0.95)
- Line: Schedule trend (EV vs. PV cumulative)
- Gantt: Milestone actual vs. planned dates
- Bar: Sprint velocity by week

**Sample Answer:**
"Portfolio SPI is 0.918 (8.2% behind schedule). Healthcare on track (SPI 0.938, minor 1-week slip on UAT phase). Fintech significantly behind (SPI 0.800, 3-week slip on design and build—architectural rework). Logistics healthy (SPI 0.945, on plan). Schedule recovery plan for Fintech: parallel workstreams in design phase, add architect capacity. Recommend CTO review architectural decisions with Fintech architect this week."

---

### Q12: How much effort are we losing to rework and defects?

**Which Tab:** Delivery → Quality  
**Data Tables:** sprints (rework_percentage, defect_count), losses (loss_category='Rework')  
**Metrics Displayed:**
- Rework % (rework hours / total delivery hours)
- Defect Count & Trend
- Root Cause Breakdown (requirements, design, code, integration)
- Quality Score (0–100)
- First-Pass Yield (% of work requiring no rework)

**Chart Types:**
- Bar: Rework % by programme
- Line: Defect rate trend (moving average)
- Pie: Root cause breakdown (design 40%, code 35%, requirements 25%)
- Heatmap: Defect count by component

**Sample Answer:**
"Portfolio rework rate 9.1% (within 5–10% target). Healthcare best-in-class (8%); Fintech problematic (20% due to architectural mismatch and scope misalignment). Root causes: 45% design phase (inadequate requirements sign-off), 35% code (quality gates weak). Quality score: Healthcare 92, Fintech 72. Recommendation: (1) Fintech design review + re-architecture gate, (2) Code quality gate automation, (3) Requirements discipline training."

---

### Q13: What is our velocity trend and are we maintaining planned delivery pace?

**Which Tab:** Delivery → Sprint Execution  
**Data Tables:** sprints (completed_story_points, velocity)  
**Metrics Displayed:**
- Velocity (story points / sprint)
- Velocity Trend (3-sprint moving average)
- Planned vs. Actual Velocity
- Sprint Leakage %

**Chart Types:**
- Bar: Velocity by sprint with trend line
- Line: Planned velocity vs. actual cumulative
- Box plot: Velocity range (mean ± std dev)
- Forecast: Projected completion date based on velocity trend

**Sample Answer:**
"Healthcare velocity stable at 108 SP/sprint (on plan). Fintech declining: Sprint 8 = 72 SP (down from 95 SP in Sprint 5)—36% velocity loss over 3 sprints. Root cause: rework + scope uncertainty. Logistics steady at 85–90 SP. Portfolio velocity risk: Fintech slope suggests 4-week schedule slip by sprint 15. Recommendation: Spike investigation into Fintech architecture stability; consider design debt paydown sprint."

---

### Q14: Which programmes have the highest risk of timeline miss?

**Which Tab:** Delivery → Risk & Forecast  
**Data Tables:** risks (impact, probability), kpi_monthly (SPI, earned_value)  
**Metrics Displayed:**
- SPI by programme (most predictive of timeline miss)
- Open High/Critical Risks (schedule-related)
- Earned Schedule (weeks ahead/behind)
- Variance At Completion % (cost + schedule combined)

**Chart Types:**
- Gauge: Risk of timeline miss (red >20% slip, yellow 10–20%, green <10%)
- Risk Matrix: Impact (y) vs. Probability (x) highlighting schedule risks
- Timeline: Milestone forecast with confidence bands
- Forecast accuracy: Historical estimate vs. actual

**Sample Answer:**
"Fintech at highest timeline risk: SPI 0.800 projects 4-week slip by completion; confidence 85%. Open Critical Risk: 'Architecture design decision' (probability High, impact High, no mitigation in place)—needs immediate escalation. Healthcare lowest risk (SPI 0.938, minor 1-week slip manageable). Logistics on track. Recommendation: CTO + Fintech delivery lead emergency architecture review; if issue not resolved within 5 days, escalate to steering committee."

---

### Q15: What is our current AI tool adoption and its impact on velocity/quality?

**Which Tab:** AI Impact → Adoption & Metrics  
**Data Tables:** ai_tools (active_users, monthly_cost), ai_metrics (ai_velocity_uplift_pct, ai_quality_uplift_pct, ai_trust_score)  
**Metrics Displayed:**
- AI Tools Count (active)
- Active Users % (penetration)
- AI Quality-Adjusted Velocity (velocity with quality uplift factored)
- AI Trust Score (0–100)
- Cost Avoidance (estimated time/$ saved by AI tools)

**Chart Types:**
- Bar: AI tools adopted by programme
- Gauge: AI Trust Score (green 70+, yellow 50–70, red <50)
- Line: Velocity trend with AI uplift overlay
- Table: AI tool ROI (cost vs. avoidance)

**Sample Answer:**
"AI adoption: Healthcare 60% (Copilot, Claude, Jira AI); Fintech 30% (hesitant); Logistics 50%. Healthcare AI-adjusted velocity 111.4 SP/sprint (net 3.1% uplift); AI Trust Score 78/100 (strong). Fintech AI Trust Score 26/100 (low adoption, 5 AI-generated defects eroding trust). Cost avoidance: Healthcare USD 8k/month; Fintech USD 2k. Recommendation: Fintech team training + defect-driven improvement; Healthcare expand adoption to other teams (model programme)."

---

## RISK (4 Questions)

### Q16: What are our open high-impact risks and their mitigation status?

**Which Tab:** Risk → Risk Register  
**Data Tables:** risks (impact, probability, status, mitigation_plan)  
**Metrics Displayed:**
- Risk Count by Impact (Low/Medium/High/Critical)
- Risk Count by Status (Open, Mitigating, Escalated, Closed)
- Risk Score (probability × impact)
- Overdue Risks (no closure date met)
- Mitigation Adequacy (plan completeness %)

**Chart Types:**
- Risk Matrix: Impact (y) vs. Probability (x) bubble chart
- Bar: Risk count by status
- Table: Open High/Critical risks with mitigation detail
- Timeline: Risk aging (days open)

**Sample Answer:**
"Portfolio open risks: 12 (3 Critical, 5 High, 4 Medium). Critical risks: (1) Fintech architecture design (probability High, impact Critical, open 15 days, mitigation 40% complete—escalate), (2) Fintech vendor availability (probability Medium, impact Critical, mitigating), (3) Healthcare client approval delays (probability Medium, impact High, closed track record—lower risk). Overdue: 2 risks (Fintech architecture, Healthcare scope approval). Recommendation: CTO architecture review for Fintech (this week); Healthcare sponsor steering meeting (next week)."

---

### Q17: What is our portfolio risk exposure score?

**Which Tab:** Risk → Portfolio Risk  
**Data Tables:** risks (all), programmes (BAC)  
**Metrics Displayed:**
- Portfolio Risk Score (weighted by programme BAC)
- Expected Monetary Value (EMV) of top 10 risks
- Risk Heat Index (probability-weighted impact)
- Schedule Risk Exposure (risk-adjusted timeline)
- Cost Risk Exposure (risk-adjusted budget)

**Chart Types:**
- Gauge: Portfolio Risk Score (red >40, yellow 25–40, green <25)
- Bar: EMV by risk
- Timeline: Risk-adjusted milestone dates vs. plan
- Waterfall: Schedule/cost reserve impact of risks

**Sample Answer:**
"Portfolio Risk Score: 34/100 (yellow—elevated). Top 3 risk exposures: (1) Fintech architecture (EMV USD 200k, 2-week delay), (2) Resource attrition (EMV USD 120k), (3) Regulatory change (Healthcare, EMV USD 85k). Risk-adjusted schedule: 3-week slip vs. plan (primarily Fintech). Cost contingency: 10% (USD 1.24M) is adequate for current risk profile if mitigations hold. Recommendation: Approve contingency request for Fintech architecture remediation; activate resource retention bonuses."

---

### Q18: Which programmes have the highest probability of cost or schedule overrun?

**Which Tab:** Risk & Forecast → Overrun Probability  
**Data Tables:** kpi_monthly (CPI, SPI), risks (cost/schedule impact)  
**Metrics Displayed:**
- Probability of Cost Overrun % (forecast EAC > BAC)
- Probability of Schedule Overrun %
- Confidence intervals (80%, 95%) on budget and timeline
- Risk-adjusted EAC and schedule

**Chart Types:**
- Gauge: Overrun probability by programme
- Distribution: Cost/schedule forecast with confidence bands
- Table: Overrun scenario analysis (best case, most likely, worst case)

**Sample Answer:**
"Cost overrun probability: Fintech 85% (confidence 90%), Healthcare 15%, Logistics 10%. Schedule overrun: Fintech 80%, Healthcare 35%, Logistics 5%. Risk-adjusted EAC (Fintech): USD 3.65M (mean), 95% CI USD 3.45M–3.95M vs. BAC USD 3.2M. Risk-adjusted schedule (Fintech): +4 weeks, 95% CI +2 to +6 weeks. Scenarios: Worst case (architecture rework + resource loss) → USD 3.95M + 6 weeks. Best case (architecture holds) → USD 3.54M + 3 weeks. Recommendation: Steer toward best-case mitigation; approve contingency allocation."

---

### Q19: What are our top operational risks (people, process, vendor, external)?

**Which Tab:** Risk → Risk Register (filtered by category)  
**Data Tables:** risks (category, description, root_cause)  
**Metrics Displayed:**
- Risk Count by Category (Technical, Schedule, Resource, Financial, Stakeholder, External)
- Open Risks by Category
- Escalated Risks

**Chart Types:**
- Pie: Risk distribution by category
- Bar: Open risks by category
- Table: Top 10 risks with category, status, owner

**Sample Answer:**
"Category breakdown: Technical 4 (Fintech architecture), Schedule 3 (Fintech rework), Resource 2 (attrition risk), Financial 2 (vendor pricing), Stakeholder 1 (Healthcare scope approval), External 0. Escalated (requiring CTO/executive action): Fintech architecture (technical), Resource attrition (people). Process risks: Change control (Fintech weak), Code quality gates (enterprise-wide). Vendor risks: Single-vendor dependency (Azure infrastructure). Recommendation: (1) Architecture deep-dive, (2) Retention bonus activation, (3) Code quality gate automation, (4) Vendor diversification study."

---

## AI (5 Questions)

### Q20: What is our AI maturity level and are we capturing AI value?

**Which Tab:** AI Impact → Maturity & Value  
**Data Tables:** ai_tools (status, adoption_date), ai_metrics (ai_velocity_uplift_pct, ai_quality_uplift_pct, ai_cost_avoidance)  
**Metrics Displayed:**
- AI Maturity Level (1–5: Awareness → Evaluation → Pilot → Active → Scaling)
- AI adoption rate (active users %)
- AI velocity uplift % (net impact on sprint velocity)
- AI quality uplift %
- AI ROI (cost avoidance / tool cost)
- AI Trust Score (0–100)

**Chart Types:**
- Gauge: AI Maturity Level by programme
- Bar: AI adoption rate, velocity uplift, quality uplift by programme
- Table: AI tools with maturity, active users, cost, ROI
- Waterfall: AI value realization (cost → avoidance → net ROI)

**Sample Answer:**
"Portfolio AI Maturity: Healthcare at Level 3.5 (Active, expanding), Fintech Level 2 (Evaluation, hesitant), Logistics Level 3 (Pilot → Active transition). Adoption rate: Healthcare 60%, Fintech 30%, Logistics 50%. Net value: Healthcare USD 8k/month cost avoidance on USD 2.5k tool cost (3.2× ROI); Fintech USD 2k avoidance on USD 1.8k cost (1.1× ROI, marginal). AI Trust Score: Healthcare 78/100, Fintech 26/100. Recommendation: (1) Fintech defect remediation + team training to build trust, (2) Healthcare expand adoption to infrastructure/ops team, (3) Establish AI center of excellence (Healthcare as hub)."

---

### Q21: What AI-generated defects are we seeing and what is the remediation plan?

**Which Tab:** AI Impact → Defect Analysis  
**Data Tables:** sprints (defect_count), losses (loss_category='Rework'), risks (description containing 'AI')  
**Metrics Displayed:**
- AI-generated defects (count, category)
- Defect rate trend (AI vs. non-AI)
- Root cause (e.g., code generation, test coverage, prompt quality)
- Remediation status

**Chart Types:**
- Bar: AI-generated defects by type (code gen, test, design)
- Line: Defect rate trend (AI vs. non-AI over time)
- Table: High-impact AI defects with remediation plan

**Sample Answer:**
"Fintech AI-generated defects: 5 this month (vs. 3 prior month—trend negative). Breakdown: 3 code generation (logic errors), 2 test automation (edge case misses). Cost impact: 65 rework hours (USD 6,175) + 10 CR hours. Root cause: Developers not validating Copilot output; insufficient test coverage on generated code. Remediation: (1) Code review gate (peer review 100% of AI-generated code), (2) Test coverage enforcement (min 85% for generated), (3) Team training on Copilot limitations. Healthcare has 2 AI defects (minor; trend positive with training). Recommendation: Fintech mandatory AI coding standards + weekly training. Pause further AI tool adoption until defect rate <1/month."

---

### Q22: What is our AI tool cost vs. benefit and what is the payback period?

**Which Tab:** AI Impact → ROI Analysis  
**Data Tables:** ai_tools (monthly_cost, estimated_cost_savings_monthly), ai_metrics (ai_cost_avoidance)  
**Metrics Displayed:**
- AI tool cost per user per month
- Cost avoidance (estimated time saved × hourly rate)
- Payback period (months)
- ROI (cost avoidance / tool cost %)
- Net benefit (annualized)

**Chart Types:**
- Bar: Cost vs. avoidance by tool
- Waterfall: AI tool cost → avoidance → net benefit
- Table: Tool-level ROI with payback period

**Sample Answer:**
"AI Tool ROI summary:
- GitHub Copilot: USD 138.89/user/month, USD 8k/month avoidance (18 users), 1.4× ROI, 4.2-month payback
- Jira AI: USD 40/month, USD 2.5k/month avoidance (search/automation), 62.5× ROI, <1-month payback
- Claude (external API): USD 3k/month, USD 5k/month avoidance (doc gen, design), 1.67× ROI, 1.8-month payback

Portfolio total: USD 5.8k/month cost, USD 15.5k/month avoidance, 2.67× ROI, 2.8-month payback. Fintech defect remediation will reduce avoidance 15% short-term (Q3) but improve long-term (Q4+). Recommendation: Expand Claude adoption to architecture/design teams (highest ROI); pause Copilot expansion until Fintech defect rate normalizes."

---

### Q23: Which teams are driving AI adoption and which need support?

**Which Tab:** AI Impact → Team Adoption  
**Data Tables:** ai_tools (active_users by programme/team), ai_metrics (ai_trust_score by team)  
**Metrics Displayed:**
- AI adoption rate by team (%)
- AI Trust Score by team
- Time to adoption (days from tool launch)
- Training completion %

**Chart Types:**
- Bar: Adoption rate by team
- Heat map: AI Trust Score by team
- Table: Team adoption profile (rate, maturity, support needs)

**Sample Answer:**
"Adoption leaders: Healthcare Development (80% adoption, 6/10 devs using Copilot), Healthcare QA (70%, AI test automation). Mid-adopters: Logistics (50% adoption, steady growth), Healthcare Architecture (55%, high trust). Laggards: Fintech Development (30%, low trust due to defects), Fintech QA (25%, resistant to change). Support needs: Fintech teams require defect remediation + training (invest 40 hours); Healthcare ready for expansion (minimal support). Recommendation: (1) Healthcare lead 'AI adoption champion' role for Fintech, (2) Fintech team mandatory training (2 days), (3) Code review process audit, (4) AI center of excellence charter with Healthcare + Logistics leads."

---

### Q24: What is our AI governance and are we managing risks?

**Which Tab:** AI Impact → Governance  
**Data Tables:** risks (containing 'AI'), policies (if tracked)  
**Metrics Displayed:**
- AI governance maturity (policies, oversight, compliance)
- AI risk count (bias, security, IP, vendor lock-in)
- Audit trail completeness (AI decision logging)
- Vendor compliance (SOC 2, data residency)

**Chart Types:**
- Gauge: Governance maturity level
- Checklist: Governance controls in place
- Risk matrix: AI-specific risks

**Sample Answer:**
"AI Governance Status: GAPS IDENTIFIED. Current state: Reactive (ad-hoc tool adoption, no policy). Critical gaps: (1) No AI tool selection framework (approval process undefined), (2) No audit trail (can't track which decisions use AI), (3) Limited vendor compliance review (Copilot, Claude API—need SOC 2 verification), (4) No bias testing (generated code may embed patterns from biased training data), (5) IP risk (code generated by Copilot may infringe third-party IP). Risks: Regulatory (GDPR, DPA compliance for code gen), vendor lock-in (Copilot switching cost high). Recommendation: (1) Establish AI governance committee (CTO, legal, delivery), (2) Create AI tool selection & approval policy (30 days), (3) Implement audit logging (Copilot code → decision log), (4) Vendor SOC 2 review + DPA amendments, (5) Bias testing framework (code review gates)."

---

## STRATEGIC (5 Questions)

### Q25: What is our programme portfolio health and what are our top strategic risks?

**Which Tab:** Executive → Portfolio Health  
**Data Tables:** All programmes, aggregated metrics  
**Metrics Displayed:**
- Portfolio Health Index (DHI weighted by programme BAC)
- Weighted Portfolio CPI
- Portfolio Margin %
- Top 5 programme risks
- Strategic gaps/opportunities

**Chart Types:**
- Gauge: Portfolio Health Index (PHI)
- Heatmap: DHI by programme (cost, schedule, quality, utilization)
- Table: Scorecard (all 37 KPIs by programme)
- Risk bubble chart: Impact vs. probability

**Sample Answer:**
"Portfolio Health: 87.9/100 (yellow; caution). Weighted CPI 0.961 (3.9% cost overrun), Portfolio Margin 36.3% (down from 39.7% Q1 due to bench and Fintech). Programme breakdown: Healthcare strong (DHI 96.4, CPI 1.059, NM 25%), Logistics good (DHI 89.4, CPI 1.025, NM 18%), Fintech weak (DHI 84.8, CPI 0.903, NM -8.6%), Public Sector risk (DHI 78.6, CPI 0.920, NM 8%). Top strategic risks: Fintech unprofitable, cost overrun likely; resource attrition (losing architects); AI maturity gaps. Recommendation: (1) Fintech immediate intervention (steering), (2) Talent retention plan (bonus/growth), (3) AI governance framework (30 days)."

---

### Q26: Are we growing revenue faster than cost and what is our unit economics?

**Which Tab:** Executive → Growth & Economics  
**Data Tables:** All programmes (BAC, revenue), all cost data  
**Metrics Displayed:**
- YoY Revenue Growth %
- YoY Cost Growth %
- Revenue per FTE (blended)
- Cost per FTE (blended)
- Gross Profit per FTE

**Chart Types:**
- Line: Revenue vs. cost trend (divergence = margin expansion)
- Bar: Revenue per FTE by programme
- Table: Unit economics by client/contract type

**Sample Answer:**
"YoY metrics: Q2 2024 vs. Q2 2023: Revenue +22% (USD 1.28M → USD 1.56M, annualized USD 6.24M), Cost +18% (labour USD 870k → USD 1.02M; overhead +25% due to bench). Revenue per FTE: USD 310k (blended); Healthcare USD 330k, Fintech USD 245k (weak—pricing or utilization issue). Cost per FTE: USD 205k (blended). Gross Profit per FTE: USD 105k (Healthcare USD 125k, Fintech USD 48k—unprofitable on unit basis). Margin expansion: 22% vs. 18% growth differential = strong. Strategic gap: Fintech unit economics broken; requires pricing/cost intervention. Recommendation: (1) Fintech pricing reset, (2) Cost per FTE benchmarking vs. market, (3) Revenue per FTE target (USD 350k by Q1 2025)."

---

### Q27: What are our top 3 opportunities for margin improvement?

**Which Tab:** Financial → Margin Improvement  
**Data Tables:** All cost, revenue, leakage, bench data  
**Metrics Displayed:**
- Margin gap to target
- Leakage as % of revenue (scope absorption, rework, bench)
- Bench runway and carry cost
- Overhead allocation %

**Chart Types:**
- Waterfall: Current margin → opportunities → target margin
- Table: Opportunity ranking (impact, effort, priority)

**Sample Answer:**
"Top 3 margin improvement opportunities:
1. **Reduce Fintech bench carry** (USD 120k/month → USD 60k/month via reallocation): Impact +2.0% net margin (~USD 64k/quarter savings), Effort: Medium (resource moves), Timeline: 4 weeks. Priority: HIGH.
2. **Eliminate scope absorption via formal change control** (reduce from 3.8% to <1%): Impact +1.5% net margin (~USD 48k/quarter), Effort: Medium (process + training), Timeline: 6 weeks. Priority: HIGH.
3. **Reduce rework via code quality gates** (Fintech 20% → 10%): Impact +0.9% net margin (~USD 29k/quarter), Effort: High (tool + discipline), Timeline: 12 weeks. Priority: MEDIUM.

Combined impact: +4.4% net margin (USD 141k/quarter), achievable in 12 weeks with focused effort. Recommendation: Approve 3-month focused improvement programme; CTO + delivery lead ownership."

---

### Q28: What is our organizational capacity and capability for next year's growth targets?

**Which Tab:** People → Capacity & Skills  
**Data Tables:** resources, bench, skills_inventory  
**Metrics Displayed:**
- Available FTE capacity (allocated + bench)
- Skills gap (demand vs. supply by role/skill)
- Billable hours capacity vs. commitment
- Attrition risk and retention plan

**Chart Types:**
- Bar: Capacity by skill (demand vs. supply)
- Forecast: FTE capacity vs. revenue growth target
- Table: Risk roles (high turnover, hard to fill)

**Sample Answer:**
"Capacity Analysis: Current FTE: 45 active + 8 bench = 53 total. FY2025 demand (based on pipeline): 65 FTE needed (22% growth). Gap: 12 FTE (23% shortfall). Skill gaps: Java architects (need 3, have 1), DevOps (need 4, have 2), AI/ML engineers (need 5, have 0—NEW). Billable hours capacity: 1,768 hrs/FTE/year × 45 = 79,560 hours; FY2025 demand 95,000 hours (19.5% gap). Attrition risk: 4 architects flagged (no retention in place), 2 QA leads. Retention cost: USD 200k bonuses vs. USD 600k replacement cost (hire + ramp-up). Recommendation: (1) Immediate retention plan (architects, QA), (2) FY2025 hiring plan (12 FTE, +6 bench), (3) Skill development program (AI/ML bootcamp for 3 current team members), (4) Assess build-vs-buy for AI/ML capability."

---

### Q29: What is our delivery operating model maturity and are we set up for scaling?

**Which Tab:** Governance → Operating Model  
**Data Tables:** Implicit in process metrics: CPI, SPI, DHI, governance maturity  
**Metrics Displayed:**
- Delivery governance maturity (1–5: Ad-hoc → Defined → Managed → Optimized → AI-driven)
- Process compliance (on-time reporting, risk escalation, change control)
- Dashboard adoption & cadence

**Chart Types:**
- Gauge: Maturity level by function (delivery, finance, risk, people)
- Checklist: Governance controls

**Sample Answer:**
"Operating Model Maturity: LEVEL 2.5 (Defined, partial). Strengths: Healthcare (Level 3 – Managed), defined governance, weekly steering, strong KPI discipline. Gaps: Fintech (Level 1.5 – Ad-hoc), weak change control, inconsistent reporting, risk escalation failures. Enterprise-wide gaps: (1) No AI-driven forecasting (still manual), (2) Bench management ad-hoc (no runway planning), (3) Cross-programme dependency tracking weak, (4) PMO lite (no consistent process across programmes). Scaling readiness: MODERATE (can handle 65 FTE with current model, but 80+ FTE requires process tightening). Recommendation: (1) Level up Fintech governance (30 days), (2) Establish enterprise PMO practices (60 days), (3) Implement AI-driven forecasting & bench planning (90 days), (4) Cross-programme dependency management tool (60 days). Investment: 2 PMO resources + tools (USD 250k/year). ROI: 15% margin improvement via efficiency."

---

## ESTIMATION (3 Questions)

### Q30: What is our overall programme estimation accuracy and what is the forecast confidence?

**Which Tab:** Estimation → Accuracy Analysis  
**Data Tables:** programmes (BAC, delivered EAC/VAC), historical estimates  
**Metrics Displayed:**
- Estimate accuracy (actual vs. planned for completed programmes)
- Forecast accuracy % (% of forecasts within 10% of actual)
- Estimation bias (systematic over/under estimate)
- MAPE (Mean Absolute Percentage Error)

**Chart Types:**
- Scatter: Planned BAC (x) vs. Actual Cost (y) for completed programmes
- Bar: Estimation accuracy by programme
- Histogram: Forecast error distribution

**Sample Answer:**
"Estimation Accuracy: MAPE 12.3% (acceptable; target <10%). Completed programmes (last 5 years): 68% of forecasts within ±10% of actual; 85% within ±15%. Estimation bias: +4.2% systematic overestimate (conservative bias; better than underestimate). Variance: Range +2% to +18% across programme sizes. Smaller programmes (<USD 1M) more accurate (±7%); larger programmes (>USD 3M) wider variance (±15%). Confidence in current forecasts: Healthcare EAC confident (85%), Fintech low (65% due to rework uncertainty). Recommendation: (1) Improve Fintech architecture confidence (spike technical design), (2) Calibrate estimation model for large programmes (>USD 3M), (3) Add risk-adjusted confidence bands to EAC."

---

### Q31: What is our contingency reserve adequacy and are we using it effectively?

**Which Tab:** Financial → Contingency Reserve  
**Data Tables:** programmes (contingency % of BAC), risks (EMV)  
**Metrics Displayed:**
- Contingency Reserve Balance ($ and % of BAC)
- Contingency Usage (drawn vs. approved)
- Risk-Adjusted Reserve Adequacy (contingency vs. risk EMV)

**Chart Types:**
- Gauge: Reserve adequacy (red <10%, yellow 10–15%, green >15%)
- Waterfall: Contingency released and used by risk
- Table: Contingency draw approvals and justification

**Sample Answer:**
"Contingency Reserve Status: Total portfolio contingency 10% of BAC (USD 1.24M). Risk-adjusted adequacy: Top 10 risks have combined EMV USD 485k (39% of contingency). Usage YTD: USD 95k (7.6% of reserve) for Fintech architecture rework and Healthcare scope changes. Remaining: USD 1.145M. Adequacy assessment: ADEQUATE if current risk mitigations hold; at risk if Fintech architecture requires full redesign (worst-case USD 300k impact). Recommendation: (1) Approve contingency allocation for Fintech mitigation (USD 150k), (2) Monitor reserve against risk trends quarterly, (3) No further contingency draws without steering approval."

---

### Q32: What are our cost estimation model inputs and assumptions?

**Which Tab:** Estimation → Model & Assumptions  
**Data Tables:** Implicit in BAC, blended rates, overhead allocations  
**Metrics Displayed:**
- Estimation model structure (cost drivers, rates, overhead)
- Key assumptions (FTE costs, productivity, overhead %)
- Sensitivity (impact of ±10% changes in key drivers)

**Chart Types:**
- Waterfall: Cost build-up from base estimate to BAC
- Sensitivity table: Cost impact of key assumption changes

**Sample Answer:**
"Cost Estimation Model Inputs:
- Base FTE cost: USD 15k–20k/month (blended; India offshore USD 12k–15k, US onshore USD 20k–30k)
- Loaded cost multiplier: 1.35 (salary + 35% benefits/overhead)
- Productivity: 1,768 billable hours/year/FTE (80% utilization target after non-billable time)
- Overhead allocation: 30–40% of labour cost (programme-level PMO, QA, tools, facilities)
- Contingency: 10% of BAC

Sensitivity (±10% change impact on USD 5M BAC programme):
- FTE cost ±10% → BAC ±USD 450k (HIGH sensitivity; critical to model)
- Overhead ±10% → BAC ±USD 225k
- Utilization ±10% → BAC ±USD 100k
- Productivity ±10% → BAC ±USD 75k

Assumption validation: QUARTERLY. Key risks: India wage inflation (historical +5–8%/year), offshore resource scarcity, overhead creep (tools/headcount). Recommendation: (1) Quarterly assumption review (wage, overhead), (2) Build probabilistic model for large deals (>USD 5M), (3) Vendor rate benchmarking annual."

---

## PEOPLE (3 Questions)

### Q33: What is our resource utilization and bench situation?

**Which Tab:** People → Utilization & Bench  
**Data Tables:** resources, bench, kpi_monthly (headcount, billable_hours)  
**Metrics Displayed:**
- HRIS Utilization % (allocated billable hours / available)
- RM Utilization % (allocated FTE / total pool)
- Billing Utilization % (billed / billable hours)
- Bench Runway (days of budget remaining)
- Daily Bench Burn (cost/day)

**Chart Types:**
- Gauge: Utilization % by programme
- Line: Bench runway trend
- Table: Resource detail (allocation, utilization, billable rate)

**Sample Answer:**
"Utilization Summary: Portfolio HRIS utilization 88% (target 85–100%; healthy). Breakdown: Healthcare 92%, Fintech 85%, Logistics 88%. RM Utilization 88% (allocated 42 FTE of 48 available; 6 FTE bench). Billing Utilization 94% (only 6% loss from billing; low leakage). Bench Status: 6 FTE on bench, daily burn USD 4,000/day, runway 30 days at current burn. Bench composition: 3 developers (awaiting Healthcare ramp-down), 2 QA (can allocate to new programmes), 1 architect (high-value; redeployment planned). Bench action: Allocate 2 QA to Public Sector (starts next month), repatriate 1 developer (end-of-month Healthcare release). Projected bench: 3 FTE by May 1. Recommendation: (1) Finalize Public Sector resource plan (ensure QA allocation), (2) Healthcare closeout staffing plan (May ramp-down), (3) Approve bench carry for May–June (growth buffer)."

---

### Q34: What is our talent pipeline and succession plan for key roles?

**Which Tab:** People → Talent & Succession  
**Data Tables:** resources (role, tenure, performance), bench, skills_inventory  
**Metrics Displayed:**
- Headcount by role (demand vs. supply)
- Bench depth by skill
- Attrition risk (tenure, satisfaction proxy)
- Succession readiness (key role coverage %)

**Chart Types:**
- Bar: Headcount by role vs. demand
- Heat map: Succession depth (red = single point of failure)
- Risk: High-risk roles (poor succession coverage)

**Sample Answer:**
"Talent Pipeline: GAPS in key roles. Current vs. needed: Java Architects (have 1, need 3), DevOps (have 2, need 4), AI/ML (have 0, need 5—NEW). Bench depth: WEAK. Only 1 bench architect (single point of failure if deployed). Succession: 3 roles with single coverage (Principal Architect, Delivery Lead, PMO Lead). Attrition risk: 4 architects flagged (>5 years tenure, market demand high); no active retention plan in place. Cost of loss: 1 architect × 6-month ramp-up = USD 120k productivity loss + USD 60k replacement. Recommendation: (1) IMMEDIATE: Retention bonuses for 4 architects (USD 200k investment, save USD 600k loss), (2) Succession depth: 2 architects in development plan (fast-track skill growth), (3) FY2025 hiring: 6 architects (net +3 FTE), 2 DevOps (net +1), 5 AI/ML (new), (4) Build bench: aim for 2–3 architect capacity (5–8 weeks runway), (5) HRBP partnership on retention strategy."

---

### Q35: What is our team satisfaction and morale and are we at burnout risk?

**Which Tab:** People → Engagement & Health  
**Data Tables:** Resources (implicit: utilization >100%, allocation on multiple programmes)  
**Metrics Displayed:**
- Resource allocation % (1.0 = full-time, >1.0 = overallocated)
- Overallocation rate (% of team >100%)
- Utilization >100% flag (burnout risk)
- Vacation/time-off patterns (deferred time-off = stress signal)
- Team satisfaction (if surveyed)

**Chart Types:**
- Gauge: Burnout risk score
- Bar: Overallocation by programme/team
- Table: High-risk resources (overallocated, deferred time-off)

**Sample Answer:**
"Team Health: MODERATE BURNOUT RISK. Overallocation: 15% of team >100% (6 of 45 active resources). High-risk: 2 architects at 120%, 3 developers at 115%. Root cause: Fintech rework absorbing capacity. Deferred time-off: 5 resources (aggregate 3 weeks), suggesting stress/disengagement. Utilization trend: UP 5% since Q1 (due to bench pressures). Vacation planning: Low uptake (only 40% of Q2 leave booked). Satisfaction proxy: Bench time (indicates morale? no survey data). Retention risk: Correlated with overallocation (architects at risk). Recommendation: (1) Reduce overallocation (move 2 devs from Fintech to bench by month-end), (2) Encourage vacation planning (leadership modeling), (3) HRBP survey on satisfaction/burnout (monthly pulse), (4) Mental health support messaging, (5) Consider bonus/time-off trade for overallocated staff (recognition)."

---

## Summary Reference

| Question # | Category | Question Title | Dashboard Tab | Key Metric(s) |
|---|---|---|---|---|
| 1 | Financial | Revenue tracking vs. annual target | Financial → Revenue | Realized Revenue, Revenue Realisation % |
| 2 | Financial | Cost risk and overrun forecast | Financial → Cost Forecast | CPI, EAC, VAC, TCPI |
| 3 | Financial | Gross margin and profitability | Financial → Profitability | Gross Margin %, Contribution Margin %, Net Margin % |
| 4 | Financial | Revenue leakage from scope absorption | Financial → Leakage | Revenue Leakage %, Scope Absorption Cost |
| 5 | Financial | Cash flow and Q3 runway | Financial → Cash Flow | Monthly Cash, Days Cash on Hand, ETC |
| 6 | Financial | Budget burn and remaining spend | Financial → Budget Burn | Remaining %, Monthly Burn, Days to Exhaustion |
| 7 | Financial | Profitable contracts & at-risk ones | Financial → Contract Analysis | Net Margin %, CPI, SPI by contract |
| 8 | Financial | Fixed vs. variable costs & breakeven | Financial → Cost Structure | Fixed/Variable Cost breakdown, Breakeven Revenue |
| 9 | Financial | Impact of change requests | Financial → Change Management | CR Count, Approved CR Value, Processing Cost, Scope Absorbed |
| 10 | Financial | Fee realization & billing alignment | Financial → Revenue Management | Revenue Realisation %, DSO, Unbilled Earned Value |
| 11 | Delivery | Schedule performance vs. plan | Delivery → Schedule | SPI, Planned vs. Actual Milestones, Sprint Velocity |
| 12 | Delivery | Effort loss to rework & defects | Delivery → Quality | Rework %, Defect Count & Trend, Quality Score |
| 13 | Delivery | Velocity trend & delivery pace | Delivery → Sprint Execution | Velocity by Sprint, Trend, Forecast |
| 14 | Delivery | Timeline miss risk by programme | Delivery → Risk & Forecast | SPI, Risk Matrix (schedule), Forecast Confidence |
| 15 | Delivery | AI adoption & impact on delivery | AI Impact → Adoption | AI Tools Count, Active Users %, AI Trust Score, Uplift % |
| 16 | Risk | Open high-impact risks & mitigation | Risk → Risk Register | Risk Count by Impact, Status, Score, Mitigation % |
| 17 | Risk | Portfolio risk exposure score | Risk → Portfolio Risk | Risk Score, EMV, Risk Heat Index |
| 18 | Risk | Cost/schedule overrun probability | Risk & Forecast → Overrun | Overrun Probability %, Risk-Adjusted EAC/Schedule |
| 19 | Risk | Operational risks (people, process, vendor, external) | Risk → Risk Register | Risk Count by Category, Escalated Risks |
| 20 | AI | AI maturity & value capture | AI Impact → Maturity | Maturity Level, Adoption %, Uplift %, AI Trust Score, ROI |
| 21 | AI | AI-generated defects & remediation | AI Impact → Defect Analysis | AI Defect Count, Type, Trend, Remediation Plan |
| 22 | AI | AI tool cost vs. benefit & payback | AI Impact → ROI | Tool Cost, Cost Avoidance, Payback Period, ROI |
| 23 | AI | Team adoption drivers & support needs | AI Impact → Team Adoption | Adoption Rate by Team, AI Trust, Maturity |
| 24 | AI | AI governance & risk management | AI Impact → Governance | Governance Maturity, Policy Coverage, Audit Trail, Compliance |
| 25 | Strategic | Portfolio health & top risks | Executive → Portfolio Health | Portfolio Health Index, DHI, CPI, Margin % |
| 26 | Strategic | Revenue growth vs. cost growth & economics | Executive → Growth & Economics | Revenue Growth %, Cost Growth %, Revenue per FTE, Margin |
| 27 | Strategic | Top 3 margin improvement opportunities | Financial → Margin Improvement | Margin Gap, Leakage %, Bench Cost, Overhead % |
| 28 | Strategic | Organizational capacity for FY2025 growth | People → Capacity | FTE Capacity, Skills Gap, Billable Hours Capacity, Attrition Risk |
| 29 | Strategic | Delivery operating model maturity & scale readiness | Governance → Operating Model | Maturity Level, Compliance %, Process Strength |
| 30 | Estimation | Estimation accuracy & forecast confidence | Estimation → Accuracy | MAPE %, Forecast Accuracy %, Bias, Confidence |
| 31 | Estimation | Contingency reserve adequacy | Financial → Contingency Reserve | Reserve Balance %, Usage, Risk EMV, Adequacy |
| 32 | Estimation | Cost estimation model & assumptions | Estimation → Model | Cost Drivers, FTE Rates, Overhead %, Sensitivity |
| 33 | People | Resource utilization & bench situation | People → Utilization & Bench | HRIS %, RM %, Billing %, Bench Runway, Daily Burn |
| 34 | People | Talent pipeline & succession plan | People → Talent & Succession | Headcount vs. Demand, Bench Depth, Succession Coverage, Attrition Risk |
| 35 | People | Team satisfaction & burnout risk | People → Engagement & Health | Overallocation %, Burnout Risk Score, Deferred Time-off, Satisfaction |

---

## NEW IN v5.1 — 15 Additional Questions (Q36–Q50)

### CUSTOMER & RELATIONSHIP (6 Questions — Tab 10: Customer Intelligence)

### Q36: Is the customer happy?

**Which Tab:** Tab 10 → Customer Intelligence → CSAT & NPS Trends
**Data Tables:** customer_satisfaction (csat_score, nps_score)
**Metrics Displayed:**
- CSAT score trend (12-month, per programme)
- NPS score (per programme and portfolio aggregate)
- Month-over-month change with trend arrow

**Sample Answer:**
"Overall portfolio CSAT is 7.8/10, stable over 3 months. Titan is the outlier at 6.8 (down from 7.5 in Q1). NPS across portfolio is +32, but Titan is at -5."

---

### Q37: What are they complaining about?

**Which Tab:** Tab 10 → Customer Intelligence → Voice of Customer
**Data Tables:** customer_satisfaction (concern_themes, positive_themes)
**Metrics Displayed:**
- Top 3 concern themes (extracted from surveys)
- Top 3 positive themes
- Concern frequency and trend

**Sample Answer:**
"Top 3 concerns across portfolio: (1) Response time on P1 incidents — Titan, (2) Team turnover — Titan and Atlas, (3) Scope change communication — Phoenix. Positive themes: technical quality on Orion, innovation on Sentinel."

---

### Q38: Will they renew?

**Which Tab:** Tab 10 → Customer Intelligence → Renewal Gauge
**Data Tables:** customer_satisfaction (renewal_score), programs, kpi_snapshots
**Metrics Displayed:**
- Renewal Probability score (0-100, weighted composite)
- Factor breakdown (CSAT, DHI, Escalation, Communication, Innovation)
- RAG status per programme

**Sample Answer:**
"4 of 5 programmes are Green for renewal (score > 80). Titan is Red at 51.9 — driven by 4 open escalations, 58% meeting adherence, and CSAT drop. Recommend executive intervention."

---

### Q39: Are we meeting their expectations?

**Which Tab:** Tab 10 → Customer Intelligence → Expectation Gap Analysis
**Data Tables:** customer_satisfaction, evm_snapshots, sla_incidents, milestones
**Metrics Displayed:**
- 7-dimension radar chart (Timeline, Quality, Communication, Innovation, Cost, Responsiveness, Stability)
- Gap score per dimension (expected vs. delivered)

**Sample Answer:**
"Across portfolio: strongest on Quality (gap +0.8) and Innovation (gap +0.5). Weakest on Responsiveness (gap -1.2, driven by Titan SLA issues) and Stability (gap -0.9, driven by Titan/Atlas attrition)."

---

### Q40: How responsive are we to their problems?

**Which Tab:** Tab 10 → Customer Intelligence (also Tab 5 → SLA Dashboard)
**Data Tables:** sla_incidents (response_time_minutes, resolution_time_minutes)
**Metrics Displayed:**
- Average P1/P2 response time (trend)
- Average P1/P2 resolution time (trend)
- SLA breach count per programme

**Sample Answer:**
"Average P1 response: 12 min (within 15-min SLA). Average P1 resolution: 5.2 hours (within 4-hour SLA? NO — breached by 1.2 hours). Titan has 2 P1 breaches this quarter. Phoenix: zero breaches."

---

### Q41: Are we communicating enough?

**Which Tab:** Tab 10 → Customer Intelligence → Communication Tracker
**Data Tables:** customer_satisfaction (steering_meetings_planned, steering_meetings_held, action_items_open, action_items_closed)
**Metrics Displayed:**
- Steering meetings held vs. planned (per programme)
- Action item closure rate
- Open action items count

**Sample Answer:**
"Portfolio average: 87% meetings held. Titan at 58% (7/12 meetings) — communication breakdown. Orion at 100%. Open action items: 14 total, 6 overdue (4 on Titan)."

---

### AI COMPARISON (2 Questions — Tab 6: AI Governance)

### Q42: AI teams vs. traditional — give me the comparison

**Which Tab:** Tab 6 → AI Governance → AI vs. Traditional Comparison Panel (also Tab 4 → Portfolio)
**Data Tables:** sprint_velocity_dual, ai_code_metrics, ai_sdlc_metrics, ai_usage_metrics, sprint_data
**Metrics Displayed:**
- 12-dimension comparison table (raw velocity, quality-adjusted velocity, defect density, test coverage, review rejection, estimation accuracy, rework %, cost per point, time to market, governance overhead, trust score, net productivity)

**Sample Answer:**
"AI-augmented teams on Sentinel are delivering 22% higher raw velocity but 14% higher quality-adjusted velocity after rework deduction. Governance overhead adds 8 hours/sprint (3% of capacity). Net productivity gain is 11%. Cost per story point is 9% lower. However, defect density is 1.15x human baseline — within acceptable range but not yet at parity. We need 3 more sprints to evaluate merge readiness."

---

### Q43: Is the AI velocity reliable enough to plan with?

**Which Tab:** Tab 3 → Delivery Planning → Dual Velocity + Tab 6 → Merge Protocol Status
**Data Tables:** sprint_velocity_dual, sprint_velocity_blend_rules
**Metrics Displayed:**
- 6-gate merge protocol status (passed/failed per gate)
- Gate details: minimum sprints, variance, defect parity, rework trend, override rate, sign-off

**Sample Answer:**
"Sentinel has passed 4 of 6 gates. Remaining: Gate 3 (defect density 1.15x, needs ≤ 1.2x — borderline) and Gate 6 (Delivery Director sign-off pending). Estimated merge readiness: Sprint 19 (2 sprints out). Until then, plan with standard velocity only."

---

### FORECAST & PREDICTIVE (3 Questions — Tabs 1, 2, 3)

### Q44: What does the forecast say about next quarter?

**Which Tab:** Tab 1 → Executive Overview (forecast summaries) + Tab 2 → KPI Studio (forecast charts)
**Data Tables:** kpi_forecasts, kpi_snapshots
**Metrics Displayed:**
- 3-month forecast for key KPIs (CPI, margin, utilisation, CSAT)
- Confidence percentage per forecast
- Trend direction and velocity

**Sample Answer:**
"CPI forecast: Phoenix drops to 0.78 (99.7% confidence — strong trend). Orion stable at 1.05. Portfolio margin forecast: 17.8% by Q3-end (vs. 20% plan). Utilisation forecast: steady at 73%. Biggest risk: Phoenix CPI trajectory indicates budget overrun is near-certain without scope intervention."

---

### Q45: What will this programme actually cost?

**Which Tab:** Tab 3 → Delivery Planning → EVM Dashboard
**Data Tables:** evm_snapshots (eac, cpi, bac), kpi_forecasts
**Metrics Displayed:**
- EAC (Estimate At Completion) = BAC / CPI
- EAC with confidence band (from forecast engine)
- TCPI (efficiency needed to finish on budget)

**Sample Answer:**
"Phoenix: BAC ₹6.8M, current EAC ₹8.4M (23.5% overrun, CPI-based). Forecast EAC with 3-month projection: ₹8.7M. TCPI = 1.31 (need 31% efficiency improvement — improbable). Recommend: scope reduction of ₹1.2M or sponsor escalation for budget increase."

---

### Q46: How reliable is our forecasting?

**Which Tab:** Tab 2 → KPI Studio → Forecast Confidence + Tab 3 → Delivery Planning
**Data Tables:** kpi_forecasts (confidence_pct), kpi_snapshots
**Metrics Displayed:**
- Forecast Confidence (R²) per KPI per programme
- Historical forecast accuracy (last 4 predictions vs. actual)

**Sample Answer:**
"CPI forecasts: 99.7% confidence for Phoenix (strong declining trend), 3.2% for Orion utilisation (volatile, no trend). Overall forecast accuracy across portfolio: 87% for financial KPIs, 65% for operational KPIs. Financial forecasts are reliable; operational forecasts need more data points."

---

### AUDIT & COMPLIANCE (4 Questions — Tab 11: Audit & Compliance)

### Q47: If an auditor walks in today, can we demonstrate governance?

**Which Tab:** Tab 11 → Audit & Compliance → Governance Control Dashboard
**Data Tables:** ai_governance_config, ai_override_log, audit_log, risks
**Metrics Displayed:**
- Governance controls list with compliance % per programme
- Process compliance scorecard (reviews, retros, steering committees)
- Overall governance readiness score

**Sample Answer:**
"Governance readiness: 78% across portfolio. All programmes have risk registers with owners. AI governance controls: 4/5 enforced (static analysis gates still being implemented for Titan). Process compliance: 87% meetings held, 91% retros conducted. Gap: Titan at 62% — needs improvement before audit."

---

### Q48: Can you prove AI output was reviewed before production?

**Which Tab:** Tab 11 → Audit & Compliance → AI Audit Trail
**Data Tables:** ai_override_log, ai_code_metrics (ai_review_rejection_pct)
**Metrics Displayed:**
- AI artifact audit trail (code, estimates, documents with provenance, reviewer, test result, production outcome)
- Review completion rate (target: 100%)
- Override log with rationale and outcome

**Sample Answer:**
"AI review rate: 98.2% across portfolio (target 100%). Sentinel: 100% — all AI-generated code reviewed before merge. Phoenix: 96% — 4 AI artifacts deployed without explicit review (flagged, corrective action taken). Override count: 23 this quarter, 78% positive outcome after override."

---

### Q49: Show me the change management evidence

**Which Tab:** Tab 11 → Audit & Compliance → Change Audit Trail + Export Audit Package
**Data Tables:** scope_creep_log, audit_log
**Metrics Displayed:**
- Change request log with approval chain
- Every data change in the system logged with timestamp
- Exportable audit package (dated ZIP)

**Sample Answer:**
"47 change requests logged this quarter. 38 approved, 5 rejected, 4 under review. All approved CRs have documented impact assessment and approval signature. 3 CRs on Phoenix were scope absorption (not billed) — total impact ₹450K. Audit package export available with one click."

---

### Q50: Is every dashboard number traceable?

**Which Tab:** Tab 11 → Audit & Compliance → Data Lineage
**Data Tables:** All tables (via data lineage tracker)
**Metrics Displayed:**
- Click any metric → see full calculation chain (formula, input values, data source table, last update timestamp)
- Data freshness indicators per table

**Sample Answer:**
"Yes. Every number on the dashboard is traceable to source data. Example: Phoenix CPI 0.81 → computed from EV ₹3.4M / AC ₹4.2M → sourced from evm_snapshots table → last updated 2026-04-01. Click any metric on any tab to see its lineage. Audit package includes lineage snapshots for all KPIs."

---

## COMPLETE QUESTION MAP (50 Questions)

| # | Category | Question | Tab | Key Metric |
|---|----------|----------|-----|-----------|
| 1 | Financial | Revenue vs. annual targets | 8 | Revenue Realisation % |
| 2 | Financial | CPI & budget variance | 3, 8 | CPI, EAC, VAC |
| 3 | Financial | Margin across portfolio | 8 | 4-layer margin waterfall |
| 4 | Financial | Bench cost allocation | 8 | Shadow allocation formula |
| 5 | Financial | Revenue leakage & recovery | 8 | 5-category leakage tracker |
| 6 | Financial | Rate card drift | 8 | Planned vs actual by tier |
| 7 | Financial | CR economics (value vs. cost) | 8 | CR value vs processing cost |
| 8 | Financial | True utilisation vs. reported | 8 | 3-system waterfall |
| 9 | Financial | Where are we losing money? | 8 | 7 delivery loss categories |
| 10 | Financial | Will we hit profit target? | 8 | Margin forecast + prediction |
| 11 | Financial | AI cost vs. saving | 6 | AI Cost-Benefit Ratio |
| 12 | Financial | Cost/point: AI vs traditional | 6, 8 | Sprint cost / points |
| 13 | Delivery | Which programmes need attention | 1, 4 | CPI heatmap + DHI |
| 14 | Delivery | Schedule adherence | 3 | SPI + milestones |
| 15 | Delivery | Sprint velocity trend | 3 | Velocity chart |
| 16 | Delivery | Forecast accuracy | 3 | Forecast vs actual |
| 17 | Delivery | Portfolio health | 1 | DHI composite + radar |
| 18 | Delivery | Projects dragging within programme | 4 | Project-level CPI drill |
| 19 | Risk | Top 3 risks by financial impact | 5 | Risk register sorted |
| 20 | Risk | Governance effectiveness | 5 | Maturity score |
| 21 | Risk | SLA compliance rate | 5 | SLA incident tracker |
| 22 | Risk | Risk forecast reliability | 5 | Prediction accuracy |
| 23 | Risk | Predicted SLA breach risk | 7 | Trend-based forecast |
| 24 | AI | Are AI tools helping? | 6 | SDLC impact metrics |
| 25 | AI | Trust AI code? | 6 | 6-factor trust score |
| 26 | AI | AI governance maturity | 6 | 5-level model |
| 27 | AI | Override frequency | 6 | Override log analysis |
| 28 | AI | AI productivity tax | 6 | Rework + governance |
| 29 | AI | AI vs traditional comparison | 6, 4 | 12-dimension panel |
| 30 | AI | AI velocity reliable for planning? | 3, 6 | 6-gate protocol |
| 31 | Strategic | What to fix right now | 7 | Smart Ops alerts |
| 32 | Strategic | Resource reallocation | 7 | Rebalancing proposal |
| 33 | Strategic | Bench runway | 7 | Bench burn calc |
| 34 | Strategic | QBR in 5 numbers | 1 | Executive summary |
| 35 | Strategic | Next quarter forecast | 1, 3 | Predictive engine |
| 36 | Strategic | Pyramid inversion? | 7, 8 | Rate card drift |
| 37 | Customer | Is customer happy? | 10 | CSAT + NPS trends |
| 38 | Customer | Complaints? | 10 | Concern themes |
| 39 | Customer | Will they renew? | 10 | Renewal probability |
| 40 | Customer | Meeting expectations? | 10 | 7-dimension gap analysis |
| 41 | Customer | Responsiveness? | 10 | Resolution time trend |
| 42 | Customer | Communicating enough? | 10 | Meeting tracker |
| 43 | AI Comparison | AI vs Traditional — full comparison | 6, 4 | 12-dimension framework |
| 44 | AI Comparison | AI velocity merge readiness | 3, 6 | 6-gate status |
| 45 | Forecast | Next quarter forecast | 1, 2 | 3-model prediction |
| 46 | Forecast | Programme actual cost projection | 3 | EAC + confidence band |
| 47 | Forecast | Forecasting reliability | 2, 3 | R² confidence % |
| 48 | Audit | Governance evidence | 9 | Control dashboard |
| 49 | Audit | AI review proof | 9 | AI audit trail |
| 50 | Audit | Number traceability | 9 | Data lineage |
| 51 | Kanban & Flow | Throughput trend | 3B | Weekly throughput chart |
| 52 | Kanban & Flow | Cycle time SLA risk | 3B | p85 vs SLA target |
| 53 | Kanban & Flow | Flow bottlenecks | 3B | CFD + WIP aging heatmap |
| 54 | Waterfall | Phase gate status | 3C | Gate approval badges |
| 55 | Waterfall | Milestone slippage | 3C | Planned vs actual timeline |
| 56 | Multi-Currency | Portfolio in base currency | 5, 1 | Currency aggregation panel |
| 57 | Multi-Currency | FX impact on margin | 5 | Rate variance analysis |
| 58 | Multi-Currency | Stale exchange rates | 11 | Currency rates management |

---

## NEW IN v5.2: KANBAN & FLOW (3 Questions)

### Q51: What is our Kanban team's throughput trend and are we improving?

**Which Tab:** Tab 3B (Delivery Health → Kanban sub-view)
**Data Tables:** flow_metrics (throughput_items, period_start, period_end)
**Metrics Displayed:**
- Weekly throughput (items completed)
- 4-week moving average
- Throughput variance (current week vs. average)

**Sample Answer:**
"DATAOPS-001 averaged 7.4 items/week over the last 5 weeks. Last week hit 9 items — a 22% improvement. Blocked time dropped from 6.5 to 1.5 hours, which correlates with the throughput increase. The 4-week trend is positive."

---

### Q52: Are we meeting our cycle time SLA commitments?

**Which Tab:** Tab 3B (Delivery Health → Kanban sub-view)
**Data Tables:** flow_metrics (cycle_time_p50, cycle_time_p85, cycle_time_p95)
**Metrics Displayed:**
- Cycle time p50 (typical), p85 (SLA), p95 (outliers)
- SLA target line overlay
- Trend over last 8 weeks

**Sample Answer:**
"Our SLA commitment is 7-day cycle time at p85. Current p85 is 5.4 days — within target. However, the week of March 15 spiked to 7.2 days (correlating with 6.5 blocked hours from external dependency). We're now back on track."

---

### Q53: Where are the bottlenecks in our Kanban flow?

**Which Tab:** Tab 3B (Delivery Health → Kanban sub-view)
**Data Tables:** flow_metrics (wip_avg, wip_limit, blocked_time_hours)
**Metrics Displayed:**
- Cumulative Flow Diagram (stacked area by workflow stage)
- WIP aging heatmap (green/amber/red by item age)
- Blocked time trend

**Sample Answer:**
"WIP averages 14.0 against a limit of 18 — 78% utilisation. However, 2 of 14 items are aging beyond p85 cycle time. Blocked time averaged 3.5 hours/week, primarily from external API team dependency. The CFD shows widening 'In Review' band — suggests code review capacity constraint."

---

## NEW IN v5.2: WATERFALL & MILESTONES (2 Questions)

### Q54: What is the gate approval status across our Waterfall phases?

**Which Tab:** Tab 3C (Delivery Health → Waterfall sub-view)
**Data Tables:** project_phases (gate_status, gate_approver, gate_date)
**Metrics Displayed:**
- Gate status badges per phase (passed ✅ / failed ❌ / conditional ⚠️ / pending ⏳)
- Gate approver and date
- Phase completion % bar

**Sample Answer:**
"RETAILCO-POS: 3 of 6 gates passed (Requirements, Design, Development). Testing is at 62% with a pending gate. UAT and Deployment not started. The Development gate passed on time; Testing has an 11-day slip due to UAT environment blocking."

---

### Q55: Which milestones have slipped and what is the cascade impact?

**Which Tab:** Tab 3C (Delivery Health → Waterfall sub-view)
**Data Tables:** project_phases (planned_start, planned_end, actual_start, actual_end)
**Metrics Displayed:**
- Planned vs. actual phase timeline (Gantt-style bar chart)
- Phase variance in days (positive = ahead, negative = behind)
- Critical path indicator (phases where slip cascades to project end date)

**Sample Answer:**
"RETAILCO-POS Design phase slipped +4 days (actual end Nov 4 vs. planned Oct 31). Testing is currently +11 days behind, which directly cascades to UAT start. If Testing doesn't recover, the August 15 deployment target is at risk by at least 11 days."

---

## NEW IN v5.2: MULTI-CURRENCY & FISCAL YEAR (3 Questions)

### Q56: What is our total portfolio value in base currency across all regions?

**Which Tab:** Tab 1 (Executive Summary) + Tab 5 (Margin & EVM)
**Data Tables:** programs, commercial_scenarios, currency_rates
**Metrics Displayed:**
- Portfolio total in base currency (e.g., USD)
- Breakdown by local currency with conversion rate applied
- Currency mix pie chart

**Sample Answer:**
"Total portfolio: USD $12.85M. Breakdown: US programmes $6.0M (47%), India programmes ₹28 Cr = $3.33M (26%), UK programmes £1.2M = $1.52M (12%), EU programmes €1.8M = $2.0M (15%). All rates as of April 1, 2026."

---

### Q57: What is the FX impact on our margins this quarter?

**Which Tab:** Tab 5 (Margin & EVM)
**Data Tables:** currency_rates, commercial_scenarios
**Metrics Displayed:**
- Margin at current rates vs. margin at budgeted rates
- FX variance (positive = favourable, negative = adverse)
- Rate movement trend over last 4 quarters

**Sample Answer:**
"FX slippage cost us $180K this quarter. INR weakened from ₹83 to ₹84.5/USD, improving our India delivery margin by 1.8%. However, GBP strengthened from $1.25 to $1.27, increasing UK programme costs by $24K. Net FX impact: -0.4% on portfolio margin."

---

### Q58: Are our exchange rates up to date for accurate reporting?

**Which Tab:** Tab 11 (Data Hub & Settings) → Currency Rates
**Data Tables:** currency_rates (effective_date, source)
**Metrics Displayed:**
- Last update date per currency pair
- Staleness indicator (green <30d, amber 30-60d, red >60d)
- Rate source (manual / API)

**Sample Answer:**
"INR/USD updated April 1 (15 days ago — green). GBP/USD updated March 15 (32 days ago — amber, refresh recommended). EUR/USD updated April 1 (green). No red flags, but GBP rate should be refreshed before month-end close."

---

**Last Updated:** 2026-04-16
**Version:** 5.2
**Maintainer:** Adi Kompalli — AKB1 Framework
