# FORMULAS REFERENCE — AKB1 Command Center v5.2

## Overview

This document defines all 45 formulas in the AKB1 Command Center v5.2, organized by category. Each formula includes:
- **Definition:** Plain-English explanation
- **Formula Expression:** Executable equation
- **Worked Example 1:** Real numbers, step-by-step calculation, interpretation
- **Worked Example 2:** Different scenario
- **Target (Green) & Alert (Red) Thresholds:** Decision thresholds for dashboard alerts
- **Dashboard Location:** Which tab and section shows this metric

---

## ESTIMATION (6 Formulas)

### 1. Budget At Completion (BAC)

**Definition:** Total approved budget for the programme in USD.

**Formula Expression:**
```
BAC = Master Budget Agreement Amount
```

**Worked Example 1 — Healthcare Programme:**
- Master budget approved: USD 5,000,000
- BAC = 5,000,000
- Interpretation: Programme has USD 5M to execute. All cost performance metrics (CPI, EAC, VAC) are calculated against this baseline.

**Worked Example 2 — Fintech Programme:**
- Master budget approved: USD 3,200,000
- BAC = 3,200,000
- Interpretation: Smaller budget scope; tighter margin for contingency.

**Target (Green):** BAC locked in Signed SOW
**Alert (Red):** BAC not approved or missing from master contract
**Dashboard Location:** Financial Tab → Programme Overview → BAC column

---

### 2. Blended Cost Per Hour

**Definition:** Weighted average cost per billable hour across all resources on the programme.

**Formula Expression:**
```
Blended Cost/Hour = (Sum of (Resource Headcount × Billable Rate × 1.35)) / Total Billable Hours in Period
```
*Note: 1.35 multiplier = base rate + 35% benefits/overhead loading*

**Worked Example 1 — Healthcare Programme (April 2024):**
- Resource costs:
  - 10 Developers @ USD 85/hr = USD 850/hr base
  - 5 QA @ USD 65/hr = USD 325/hr base
  - 3 Architects @ USD 120/hr = USD 360/hr base
  - 2 DevOps @ USD 95/hr = USD 190/hr base
  - Total base = USD 1,725/hr
- Add 35% overhead: 1,725 × 1.35 = USD 2,328.75/hr total loaded cost
- Total billable hours in April = 1,200 hours
- Blended Cost/Hour = 2,328.75 / 1,200 = **USD 1.94/hour effective cost per billable hour**
- Interpretation: On average, each billable hour costs USD 1.94 to deliver (all-in), well below expected USD 2.50–3.00 market rate, indicating good cost efficiency.

**Worked Example 2 — Fintech Programme (April 2024):**
- Resource costs:
  - 5 Senior Developers @ USD 110/hr = USD 550/hr base
  - 2 Principal Architects @ USD 150/hr = USD 300/hr base
  - 1 Tech Lead @ USD 130/hr = USD 130/hr base
  - Total base = USD 980/hr
- Add 35% overhead: 980 × 1.35 = USD 1,323/hr total loaded cost
- Total billable hours in April = 650 hours
- Blended Cost/Hour = 1,323 / 650 = **USD 2.04/hour**
- Interpretation: Senior-heavy team, higher cost per hour; acceptable for high-complexity fintech delivery.

**Target (Green):** 1.8–2.3 USD/hour (market-competitive after overhead)
**Alert (Red):** > 2.8 USD/hour (cost overrun risk) or < 1.2 USD/hour (bench carry or underutilization)
**Dashboard Location:** Financial Tab → Cost Structure → Blended Cost/Hour KPI card

---

### 3. Loaded Cost Per Resource

**Definition:** Total cost to employ one resource for one month, including salary, benefits, and overhead.

**Formula Expression:**
```
Loaded Cost = Base Billable Rate × 1.35 × Hours/Month (160 for standard, adjusted for actual allocation)
```

**Worked Example 1 — Mid-Level Developer (Healthcare):**
- Base billable rate: USD 85/hour
- Allocation: 85% (part-time allocation on programme)
- Hours/Month: 160 × 0.85 = 136 actual hours
- Loaded Cost = 85 × 1.35 × 136 = **USD 15,606/month**
- Interpretation: This developer costs USD 15,606 loaded per month when 85% allocated. Used for resource burn calculations and margin analysis.

**Worked Example 2 — Principal Architect (Fintech):**
- Base billable rate: USD 150/hour
- Allocation: 100% (full-time)
- Hours/Month: 160 × 1.0 = 160 actual hours
- Loaded Cost = 150 × 1.35 × 160 = **USD 32,400/month**
- Interpretation: High-cost specialist; 100% allocated. Contributes significantly to programme burn rate.

**Target (Green):** Loaded cost ≤ billable revenue per resource per month
**Alert (Red):** Loaded cost > billable revenue (resource not covering own cost)
**Dashboard Location:** People Tab → Resource Cost Detail → Loaded Cost column

---

### 4. Billable Hours Per Year

**Definition:** Total productive hours available for billing per resource per year (accounting for standard leave, holidays, non-billable time).

**Formula Expression:**
```
Billable Hours/Year = (365 days - Weekends - Public Holidays - Annual Leave - Admin Time) × 8 hours/day
```

**Worked Example 1 — Standard India-Based Resource:**
- Total calendar days: 365
- Weekends: 104 days
- Public holidays (India): 15 days
- Annual leave (standard): 15 days
- Admin/training time (non-billable): 10 days
- Net billable days: 365 - 104 - 15 - 15 - 10 = **221 days**
- Billable Hours/Year = 221 × 8 = **1,768 hours/year**
- Interpretation: Each India-based resource can bill ~1,768 hours/year on average; planning baseline.

**Worked Example 2 — US-Based Resource:**
- Total calendar days: 365
- Weekends: 104 days
- Public holidays (US): 10 days (fewer than India)
- Annual leave (US): 15 days
- Admin/training time: 10 days
- Net billable days: 365 - 104 - 10 - 15 - 10 = **226 days**
- Billable Hours/Year = 226 × 8 = **1,808 hours/year**
- Interpretation: US resources have slightly higher billable hours baseline due to fewer public holidays.

**Target (Green):** 1,700–1,850 hours/year (realistic capacity)
**Alert (Red):** > 2,000 hours/year (unrealistic planning; burnout risk) or < 1,400 hours/year (capacity constraint)
**Dashboard Location:** Estimation Tab → Resource Planning → Billable Hours/Year KPI

---

### 5. Overhead Allocation Percentage

**Definition:** Percentage of direct labour cost allocated to programme-level overheads (facilities, tools, management, PMO, etc.).

**Formula Expression:**
```
Overhead Allocation % = (Programme-Level Overhead Costs / Direct Labour Costs) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Direct labour cost (payroll): USD 225,000
- Programme-level overhead:
  - PMO/QA team (8 FTE): USD 60,000
  - Tools/infrastructure (Jira, Azure, licenses): USD 12,000
  - Facilities (desk, equipment): USD 8,000
  - Travel/client engagement: USD 5,000
  - Total overhead: USD 85,000
- Overhead Allocation % = (85,000 / 225,000) × 100 = **37.8%**
- Interpretation: For every USD 1 of direct delivery cost, USD 0.378 goes to support/overhead; acceptable for complex programmes.

**Worked Example 2 — Simple Fixed-Price Programme (April 2024):**
- Direct labour cost: USD 120,000
- Programme-level overhead: USD 30,000 (smaller team, shared services)
- Overhead Allocation % = (30,000 / 120,000) × 100 = **25%**
- Interpretation: Lower overhead ratio; streamlined, mature programme.

**Target (Green):** 25–40% (context-dependent by programme complexity)
**Alert (Red):** > 50% (overhead bloat) or < 15% (unrealistic; hidden costs elsewhere)
**Dashboard Location:** Financial Tab → Cost Breakdown → Overhead Allocation % card

---

### 6. Contingency Buffer

**Definition:** Approved contingency reserve as a percentage of BAC, reserved for unknown-unknowns.

**Formula Expression:**
```
Contingency % = (Contingency Reserve / BAC) × 100
```

**Worked Example 1 — Healthcare Programme:**
- BAC: USD 5,000,000
- Approved contingency reserve: USD 500,000
- Contingency % = (500,000 / 5,000,000) × 100 = **10%**
- Interpretation: 10% contingency (typical for fixed-price, mature client, low-risk). Reserve protected; only released via change control.

**Worked Example 2 — Fintech High-Risk Programme:**
- BAC: USD 3,200,000
- Approved contingency reserve: USD 576,000
- Contingency % = (576,000 / 3,200,000) × 100 = **18%**
- Interpretation: 18% contingency (higher risk due to regulatory, emerging tech, tight deadline). Justified by risk profile.

**Target (Green):** 10–15% (standard reserve for mature programmes)
**Alert (Red):** < 5% (insufficient buffer) or > 25% (over-conservative, ties up budget)
**Dashboard Location:** Financial Tab → Budget Reserve → Contingency % card

---

## COST PERFORMANCE (7 Formulas)

### 7. Cost Performance Index (CPI)

**Definition:** Efficiency of cost spending; how much value is being delivered per dollar spent. Ratio of Earned Value to Actual Cost.

**Formula Expression:**
```
CPI = Earned Value / Actual Cost
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Earned Value (value of work completed): USD 450,000
- Actual Cost (cash spent): USD 425,000
- CPI = 450,000 / 425,000 = **1.059**
- Interpretation: For every USD 1 spent, USD 1.059 of value delivered. 5.9% cost underrun. Green signal: programme is cost-efficient.

**Worked Example 2 — Fintech Programme (April 2024):**
- Earned Value: USD 280,000
- Actual Cost: USD 310,000
- CPI = 280,000 / 310,000 = **0.903**
- Interpretation: For every USD 1 spent, only USD 0.903 of value delivered. 9.7% cost overrun. Red signal: programme is cost-inefficient; likely due to rework, scope creep, or resource inefficiency.

**Target (Green):** ≥ 1.0 (at or above planned cost efficiency)
**Alert (Red):** < 0.95 (persistent cost overrun; forecasting concern)
**Dashboard Location:** Financial Tab → Cost Performance → CPI card + Cost Performance Chart (historical trend)

---

### 8. Earned Value (EV)

**Definition:** Monetary value of work completed to date, independent of cost.

**Formula Expression:**
```
EV = (Work Completed % / 100) × BAC
```

**Worked Example 1 — Healthcare Programme (Month 4 of 12):**
- BAC: USD 5,000,000
- Work completed: 45% (4 modules out of 9 complete, 1 module in progress)
- EV = (45 / 100) × 5,000,000 = **USD 2,250,000**
- Interpretation: USD 2.25M of planned work has been completed; used to judge progress independent of actual spending.

**Worked Example 2 — Fintech Programme (Month 3 of 8):**
- BAC: USD 3,200,000
- Work completed: 32% (design + build phase 1 complete)
- EV = (32 / 100) × 3,200,000 = **USD 1,024,000**
- Interpretation: USD 1.024M of value delivered against USD 3.2M total scope.

**Target (Green):** EV ≥ Planned Value (on schedule)
**Alert (Red):** EV significantly < Planned Value (falling behind schedule; schedule risk)
**Dashboard Location:** Financial Tab → Cost Performance → Earned Value KPI + Cost Performance Chart

---

### 9. Estimate At Completion (EAC)

**Definition:** Forecast of total programme cost based on current spend trajectory and CPI.

**Formula Expression:**
```
EAC = (BAC / CPI)
```

**Worked Example 1 — Healthcare Programme (April 2024, assuming CPI continues):**
- BAC: USD 5,000,000
- Current CPI: 1.059 (from earlier example)
- EAC = 5,000,000 / 1.059 = **USD 4,720,585**
- Interpretation: If cost performance holds, programme will complete at USD 4.72M (USD 279,415 under budget). Positive forecast.

**Worked Example 2 — Fintech Programme (April 2024, assuming CPI continues):**
- BAC: USD 3,200,000
- Current CPI: 0.903 (from earlier example)
- EAC = 3,200,000 / 0.903 = **USD 3,544,074**
- Interpretation: If cost overrun continues, programme will cost USD 3.54M (USD 344,074 over budget). Red flag; needs corrective action.

**Target (Green):** EAC ≤ BAC (on budget or better)
**Alert (Red):** EAC > BAC (projected cost overrun)
**Dashboard Location:** Financial Tab → Cost Forecast → EAC card + Financial Forecast Chart

---

### 10. Estimate To Complete (ETC)

**Definition:** How much more money is needed to finish the programme.

**Formula Expression:**
```
ETC = EAC - Actual Cost to Date
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- EAC (from previous example): USD 4,720,585
- Actual Cost to date: USD 425,000 (April only, but assume cumulative YTD is USD 1,700,000)
- ETC = 4,720,585 - 1,700,000 = **USD 3,020,585**
- Interpretation: USD 3.02M more needed to completion; good cash flow visibility for budget holder.

**Worked Example 2 — Fintech Programme (April 2024):**
- EAC: USD 3,544,074
- Actual Cost to date (YTD): USD 980,000
- ETC = 3,544,074 - 980,000 = **USD 2,564,074**
- Interpretation: USD 2.56M remaining; monitor closely given cost overrun trend.

**Target (Green):** ETC ≤ Remaining Budget (on track for completion)
**Alert (Red):** ETC > Remaining Budget (insufficient funds to complete)
**Dashboard Location:** Financial Tab → Cash Flow → ETC card

---

### 11. To-Complete Performance Index (TCPI)

**Definition:** Cost efficiency needed going forward to complete within remaining budget.

**Formula Expression:**
```
TCPI = (BAC - EV) / (BAC - Actual Cost)
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- BAC: USD 5,000,000
- EV: USD 2,250,000 (from earlier example)
- Actual Cost YTD: USD 1,700,000
- Remaining work value: 5,000,000 - 2,250,000 = USD 2,750,000
- Remaining budget: 5,000,000 - 1,700,000 = USD 3,300,000
- TCPI = 2,750,000 / 3,300,000 = **0.833**
- Interpretation: To finish within budget, need to deliver remaining work at 83.3% of current cost (more efficient). Achievable given current 1.059 CPI.

**Worked Example 2 — Fintech Programme (April 2024):**
- BAC: USD 3,200,000
- EV: USD 1,024,000
- Actual Cost YTD: USD 980,000
- Remaining work value: 3,200,000 - 1,024,000 = USD 2,176,000
- Remaining budget: 3,200,000 - 980,000 = USD 2,220,000
- TCPI = 2,176,000 / 2,220,000 = **0.980**
- Interpretation: Need to deliver remaining work at 98% of current cost (nearly breakeven on remaining budget). Tight; current CPI of 0.903 makes this difficult; corrective action needed.

**Target (Green):** TCPI 0.90–1.10 (achievable efficiency for remainder)
**Alert (Red):** TCPI < 0.85 or > 1.15 (unrealistic; either too lenient or too tight)
**Dashboard Location:** Financial Tab → Forecast → TCPI card

---

### 12. Variance At Completion (VAC)

**Definition:** Dollar difference between budget and forecasted cost.

**Formula Expression:**
```
VAC = BAC - EAC
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- BAC: USD 5,000,000
- EAC: USD 4,720,585 (from earlier example)
- VAC = 5,000,000 - 4,720,585 = **USD 279,415** (positive = savings)
- Interpretation: Based on current spend, programme will deliver USD 279k under budget. Green signal.

**Worked Example 2 — Fintech Programme (April 2024):**
- BAC: USD 3,200,000
- EAC: USD 3,544,074 (from earlier example)
- VAC = 3,200,000 - 3,544,074 = **USD -344,074** (negative = overrun)
- Interpretation: Projected USD 344k cost overrun. Red signal; needs corrective action plan.

**Target (Green):** VAC ≥ 0 (on budget or savings)
**Alert (Red):** VAC < -(5% of BAC) (significant projected overrun)
**Dashboard Location:** Financial Tab → Budget Performance → VAC card + Variance Trend Chart

---

### 13. Schedule Performance Index (SPI)

**Definition:** Efficiency of schedule execution; how much progress made relative to plan.

**Formula Expression:**
```
SPI = Earned Value / Planned Value
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- EV (work completed value): USD 2,250,000
- Planned Value (what should be done): USD 2,400,000 (45% of BAC planned for this point)
- SPI = 2,250,000 / 2,400,000 = **0.938**
- Interpretation: Delivering 93.8% of planned progress; slightly behind schedule (6.2% slip). Not critical; watch trend.

**Worked Example 2 — Fintech Programme (April 2024, month 3 of 8):**
- EV: USD 1,024,000
- Planned Value: USD 1,280,000 (37.5% planned for month 3)
- SPI = 1,024,000 / 1,280,000 = **0.800**
- Interpretation: Delivering only 80% of planned progress; 20% behind schedule. Red signal; schedule risk escalation warranted.

**Target (Green):** ≥ 0.95 (at or ahead of schedule)
**Alert (Red):** < 0.90 (schedule slip; risk of timeline miss)
**Dashboard Location:** Delivery Tab → Schedule Performance → SPI card + Schedule Trend Chart

---

## MARGIN (4 Formulas)

### 14. Gross Margin Percentage

**Definition:** Profit as a percentage of realized revenue before overhead allocation.

**Formula Expression:**
```
Gross Margin % = ((Realized Revenue - Direct Labour Cost) / Realized Revenue) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Realized Revenue (actual billed): USD 480,000
- Direct Labour Cost (payroll): USD 225,000
- Gross Margin % = ((480,000 - 225,000) / 480,000) × 100 = **46.9%**
- Interpretation: 46.9% gross margin; 53.1% cost of delivery. Strong; typical is 40–50% for services.

**Worked Example 2 — Fintech Programme (April 2024):**
- Realized Revenue: USD 350,000
- Direct Labour Cost: USD 280,000
- Gross Margin % = ((350,000 - 280,000) / 350,000) × 100 = **20%**
- Interpretation: 20% gross margin; thin. Either high-skill resource cost or pricing issue. Requires review.

**Target (Green):** 40–55% (healthy for IT services delivery)
**Alert (Red):** < 30% (margin erosion; business case broken)
**Dashboard Location:** Financial Tab → Profitability → Gross Margin % card + Margin Waterfall

---

### 15. Contribution Margin Percentage

**Definition:** Profit after direct labour costs and variable overhead (e.g., tools, travel, vendor costs).

**Formula Expression:**
```
Contribution Margin % = ((Realized Revenue - Direct Labour - Variable Overhead) / Realized Revenue) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Realized Revenue: USD 480,000
- Direct Labour Cost: USD 225,000
- Variable Overhead (tools, vendor, travel): USD 45,000
- Contribution Margin % = ((480,000 - 225,000 - 45,000) / 480,000) × 100 = **31.25%**
- Interpretation: After labour and variable costs, 31.25% margin remains to cover fixed overhead and profit. Good.

**Worked Example 2 — Fintech Programme (April 2024):**
- Realized Revenue: USD 350,000
- Direct Labour: USD 280,000
- Variable Overhead: USD 35,000
- Contribution Margin % = ((350,000 - 280,000 - 35,000) / 350,000) × 100 = **7.1%**
- Interpretation: Thin margin after variable costs. Insufficient to cover fixed overhead; programme not profitable at current pricing.

**Target (Green):** 25–40% (sufficient to cover overhead + profit)
**Alert (Red):** < 15% (unsustainable; pricing or cost issue)
**Dashboard Location:** Financial Tab → Profitability → Contribution Margin % card

---

### 16. Portfolio Margin Percentage

**Definition:** Blended gross margin across all active programmes.

**Formula Expression:**
```
Portfolio Margin % = (Sum of All Programmes' Gross Profit / Sum of All Programmes' Realized Revenue) × 100
```

**Worked Example 1 — Q1 2024 Portfolio (3 active programmes):**
- Healthcare: Revenue USD 480,000, Gross Profit USD 226,000
- Fintech: Revenue USD 350,000, Gross Profit USD 70,000
- Logistics: Revenue USD 420,000, Gross Profit USD 200,000
- Total Revenue: USD 1,250,000
- Total Gross Profit: USD 496,000
- Portfolio Margin % = (496,000 / 1,250,000) × 100 = **39.68%**
- Interpretation: Portfolio health good; balanced mix of high-margin (Healthcare, Logistics) and lower-margin (Fintech) programmes.

**Worked Example 2 — Q2 2024 Portfolio (4 active programmes, 1 new low-margin):**
- Healthcare: Revenue USD 500,000, Gross Profit USD 235,000
- Fintech: Revenue USD 380,000, Gross Profit USD 76,000
- Logistics: Revenue USD 450,000, Gross Profit USD 225,000
- New Public Sector (fixed-price): Revenue USD 250,000, Gross Profit USD 37,500
- Total Revenue: USD 1,580,000
- Total Gross Profit: USD 573,500
- Portfolio Margin % = (573,500 / 1,580,000) × 100 = **36.3%**
- Interpretation: Margin dilution due to new fixed-price public sector programme. Watch; requires offset with high-margin work.

**Target (Green):** 38–48% (healthy portfolio)
**Alert (Red):** < 32% (portfolio margin erosion; address mix and pricing)
**Dashboard Location:** Executive Tab → Portfolio Health → Portfolio Margin % KPI

---

### 17. Net Programme Margin Percentage

**Definition:** Profit after all programme costs (labour, overhead, tools, vendor, etc.) as percentage of revenue.

**Formula Expression:**
```
Net Margin % = ((Realized Revenue - Total Programme Costs) / Realized Revenue) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Realized Revenue: USD 480,000
- Direct Labour: USD 225,000
- Programme Overhead (PMO, QA, facilities, etc.): USD 85,000
- Vendor/Subcontractor: USD 30,000
- Tools & Infrastructure: USD 12,000
- Travel & Client Engagement: USD 8,000
- Total Costs: USD 360,000
- Net Margin % = ((480,000 - 360,000) / 480,000) × 100 = **25%**
- Interpretation: After all costs, 25% net profit. Healthy; strong programme.

**Worked Example 2 — Fintech Programme (April 2024):**
- Realized Revenue: USD 350,000
- Direct Labour: USD 280,000
- Programme Overhead: USD 60,000
- Vendor/Subcontractor: USD 25,000
- Tools & Infrastructure: USD 10,000
- Travel: USD 5,000
- Total Costs: USD 380,000
- Net Margin % = ((350,000 - 380,000) / 350,000) × 100 = **-8.6%**
- Interpretation: Programme is unprofitable; losing USD 30k/month. Immediate corrective action required.

**Target (Green):** 15–25% (profitable after all costs)
**Alert (Red):** < 10% or negative (programme unprofitable; escalate)
**Dashboard Location:** Financial Tab → Profitability → Net Margin % card + Margin Analysis Table

---

## UTILIZATION (4 Formulas)

### 18. HRIS Utilization Percentage

**Definition:** Percentage of allocated resource time actually billable (vs. non-billable admin, training, bench).

**Formula Expression:**
```
HRIS Utilization % = (Billable Hours Logged / (Allocation % × Billable Hours Available)) × 100
```

**Worked Example 1 — Senior Developer (April 2024):**
- Billable hours logged: 136 hours
- Allocation percentage: 85% of full-time
- Billable hours available in April: 160 × 0.85 = 136 hours
- HRIS Utilization % = (136 / 136) × 100 = **100%**
- Interpretation: Resource fully utilized against allocation. No slack; healthy.

**Worked Example 2 — Mid-Level Developer (April 2024):**
- Billable hours logged: 115 hours
- Allocation percentage: 85% (136 hours available)
- HRIS Utilization % = (115 / 136) × 100 = **84.6%**
- Interpretation: 15.4% idle time against allocation (21 hours non-billable: training, admin). Slight slack; acceptable.

**Target (Green):** 85–100% of allocated hours billable
**Alert (Red):** < 75% (too much bench/non-billable time) or >105% (overallocation; burnout risk)
**Dashboard Location:** People Tab → Utilization → HRIS Utilization % by resource

---

### 19. RM (Resource Manager) Utilization Percentage

**Definition:** Percentage of total programme headcount actively allocated (not on bench).

**Formula Expression:**
```
RM Utilization % = (Total Allocated FTE / Total Available FTE in Pool) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Total allocated FTE: 22 (developers, QA, architects, DevOps combined)
- Total available FTE in resource pool: 25 (includes 3 bench resources)
- RM Utilization % = (22 / 25) × 100 = **88%**
- Interpretation: 88% of headcount pool in use; 12% on bench. Healthy ratio; some slack for attrition/absences.

**Worked Example 2 — Fintech Programme (April 2024, ramp-down phase):**
- Total allocated FTE: 16
- Total available FTE: 20 (4 on bench, awaiting new assignment)
- RM Utilization % = (16 / 20) × 100 = **80%**
- Interpretation: 80% utilization; 4 FTE bench carry. Expected in ramp-down; monitor for bench runway.

**Target (Green):** 85–95% (balanced utilization)
**Alert (Red):** < 75% (high bench cost) or >98% (no buffer for attrition)
**Dashboard Location:** People Tab → Resource Utilization → RM Utilization % card

---

### 20. Billing Utilization Percentage

**Definition:** Percentage of billable hours actually billed to client (vs. absorbed, unbillable).

**Formula Expression:**
```
Billing Utilization % = (Hours Billed / Total Billable Hours Worked) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Billable hours worked: 1,200
- Hours actually billed to client: 1,176
- Absorption (rework, unplanned work): 24 hours
- Billing Utilization % = (1,176 / 1,200) × 100 = **98%**
- Interpretation: 98% of billable time billed; only 2% absorbed (rework, etc.). Excellent; low leakage.

**Worked Example 2 — Fintech Programme (April 2024, high-rework phase):**
- Billable hours worked: 650
- Hours billed to client: 585
- Absorption (rework, defect remediation, extra design): 65 hours
- Billing Utilization % = (585 / 650) × 100 = **90%**
- Interpretation: 10% of hours absorbed (not billed). Significant leakage due to quality issues. Red flag; investigate root cause.

**Target (Green):** 95–100% (high billing efficiency)
**Alert (Red):** < 90% (significant leakage; cost impact)
**Dashboard Location:** Delivery Tab → Leakage → Billing Utilization % card

---

### 21. Utilization Waterfall Loss

**Definition:** Cumulative loss from available hours to billable hours due to bench, non-billable time, and absorption.

**Formula Expression:**
```
Loss = Available Hours - (HRIS Utilization % × Allocated Hours) - (Absorption Hours)
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Available hours: 4,000 (25 FTE × 160 hours/month)
- HRIS Utilization: 85% of allocated = 3,400 billable hours logged
- Absorption hours (unplanned work, rework): 48 hours
- Loss = 4,000 - 3,400 - (1,200 billable - 48 absorbed)
  - Simplify: Bench loss = 600 hours, absorption loss = 48 hours
  - Total loss = 648 hours
- Interpretation: 648 hours lost in month; 16.2% of total available. Breakdown: 15% bench, 1.2% absorption.

**Worked Example 2 — Fintech Programme (April 2024):**
- Available hours: 3,200 (20 FTE × 160 hours)
- HRIS Utilization: 90% = 2,880 hours
- Absorption: 65 hours
- Loss = 3,200 - 2,880 - 65 = **255 hours** (7.9% loss)
- Interpretation: Lower loss; better utilization. Still, 65-hour absorption indicates quality issues to address.

**Target (Green):** < 10% total loss (bench + absorption combined)
**Alert (Red):** > 15% loss (significant inefficiency; investigate)
**Dashboard Location:** Delivery Tab → Utilization Waterfall Chart (visualization of all loss components)

---

## BENCH & OVERHEAD (3 Formulas)

### 22. Shadow Allocation Cost

**Definition:** Cost of resources on bench allocated to internal initiatives or transitional work.

**Formula Expression:**
```
Shadow Allocation Cost = Bench Resource Count × Loaded Cost/Month × Shadow Allocation %
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Bench resources: 3 FTE
- Loaded cost per resource: USD 15,000/month (average)
- Shadow allocation (allocated to training, internal process improvement): 40%
- Shadow Allocation Cost = 3 × 15,000 × 0.40 = **USD 18,000/month**
- Interpretation: USD 18k of bench cost absorbed by internal initiatives; offsets pure bench cost.

**Worked Example 2 — Fintech Programme (April 2024):**
- Bench resources: 4 FTE
- Loaded cost: USD 20,000/month (senior resources)
- Shadow allocation: 25%
- Shadow Allocation Cost = 4 × 20,000 × 0.25 = **USD 20,000/month**
- Interpretation: USD 20k partially offset; still carries significant pure bench cost.

**Target (Green):** Shadow allocation > 30% (meaningful offset to bench cost)
**Alert (Red):** Shadow allocation < 15% (bench mostly idle)
**Dashboard Location:** Financial Tab → Bench Management → Shadow Allocation Cost card

---

### 23. Bench Runway

**Definition:** Number of days a bench pool can be sustained given current burn rate and available budget.

**Formula Expression:**
```
Bench Runway (days) = (Available Budget for Bench / Daily Bench Burn Rate)
```

**Worked Example 1 — Q2 2024 Bench Pool:**
- Bench headcount: 8 FTE
- Daily bench burn rate: (8 × 15,000 loaded cost per month) / 20 working days = USD 6,000/day
- Available bench budget (Q2 allocation): USD 120,000
- Bench Runway = 120,000 / 6,000 = **20 days**
- Interpretation: At current burn, bench budget exhausted in 20 days (end of first week of May). Must allocate bench resources or secure additional budget urgently.

**Worked Example 2 — Q3 2024 Bench Pool (lower burn):**
- Bench headcount: 5 FTE
- Daily bench burn rate: (5 × 18,000) / 20 = USD 4,500/day
- Available bench budget: USD 200,000
- Bench Runway = 200,000 / 4,500 = **44.4 days**
- Interpretation: Sustainable for ~6 weeks; good runway for planned ramp-ups.

**Target (Green):** > 30 days bench runway
**Alert (Red):** < 15 days (urgent allocation or budget issue)
**Dashboard Location:** People Tab → Bench Management → Bench Runway card + Bench Forecast Chart

---

### 24. Daily Bench Burn

**Definition:** Daily cost of bench resources (non-billable).

**Formula Expression:**
```
Daily Bench Burn = (Bench FTE × Loaded Cost/Month) / 20 Working Days
```

**Worked Example 1 — Fintech Bench (April 2024):**
- Bench FTE: 4
- Loaded cost per resource: USD 20,000/month
- Total bench cost: 4 × 20,000 = USD 80,000/month
- Daily Bench Burn = 80,000 / 20 = **USD 4,000/day**
- Interpretation: Every day 4 FTE on bench costs USD 4,000. Urgent to allocate or release resources.

**Worked Example 2 — Healthcare Bench (April 2024):**
- Bench FTE: 2
- Loaded cost: USD 15,000/month
- Total bench cost: 2 × 15,000 = USD 30,000/month
- Daily Bench Burn = 30,000 / 20 = **USD 1,500/day**
- Interpretation: Sustainable; small bench pool.

**Target (Green):** < USD 3,000/day (minimal bench cost)
**Alert (Red):** > USD 6,000/day (significant bench carrying cost; escalate)
**Dashboard Location:** People Tab → Bench Management → Daily Bench Burn KPI + Bench Cost Trend

---

## REVENUE & LEAKAGE (4 Formulas)

### 25. Revenue Leakage Percentage

**Definition:** Percentage of billable hours not converted to revenue due to scope absorption, rework, unplanned work, etc.

**Formula Expression:**
```
Revenue Leakage % = (Loss Hours / Total Billable Hours) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Total billable hours worked: 1,200
- Loss hours (rework, scope absorption, unplanned): 48
- Revenue Leakage % = (48 / 1,200) × 100 = **4%**
- Interpretation: 4% of billable effort not converted to revenue. Acceptable; loss of ~USD 4,080 in billable value (48 × USD 85/hour).

**Worked Example 2 — Fintech Programme (April 2024):**
- Total billable hours: 650
- Loss hours: 95 (rework 65 + unplanned 30)
- Revenue Leakage % = (95 / 650) × 100 = **14.6%**
- Interpretation: 14.6% leakage; significant. Loss of ~USD 10,450 billable value. Root cause analysis required.

**Target (Green):** 2–5% (minor, acceptable leakage)
**Alert (Red):** > 10% (material leakage; investigate root cause)
**Dashboard Location:** Financial Tab → Leakage Analysis → Revenue Leakage % card

---

### 26. Scope Absorption Cost

**Definition:** Cost of unplanned scope executed without change request or billing adjustment.

**Formula Expression:**
```
Scope Absorption Cost = Loss Hours × Blended Cost/Hour
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Loss hours (scope absorption): 35 hours (subset of 48 total loss hours)
- Blended cost/hour: USD 85/hour (calculated earlier as USD 1.94/hour, adjusted to USD 85 for visible cost)
- Scope Absorption Cost = 35 × 85 = **USD 2,975**
- Interpretation: USD 2.975k of unplanned scope delivered without recovery. Margin impact.

**Worked Example 2 — Fintech Programme (April 2024):**
- Loss hours (scope absorption): 50 hours (subset of 95 total)
- Blended cost/hour: USD 95/hour
- Scope Absorption Cost = 50 × 95 = **USD 4,750**
- Interpretation: USD 4.75k absorbed; material. Indicates weak change control.

**Target (Green):** < 1% of contract value
**Alert (Red):** > 2% of contract value (scope creep; escalate)
**Dashboard Location:** Financial Tab → Leakage Analysis → Scope Absorption Cost card + Change Control Dashboard

---

### 27. CR (Change Request) Processing Cost

**Definition:** Administrative and review cost incurred to process change requests.

**Formula Expression:**
```
CR Processing Cost = (CR Count × Avg Review Hours per CR × Blended Cost/Hour)
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Change requests received: 8
- Avg review/approval hours per CR: 4 hours (analysis + steering approval + implementation tracking)
- Blended cost/hour: USD 85
- CR Processing Cost = 8 × 4 × 85 = **USD 2,720**
- Interpretation: USD 2.72k administrative cost to process 8 CRs. Reasonable; ~USD 340 per CR.

**Worked Example 2 — Fintech Programme (April 2024, high-change period):**
- Change requests: 15
- Avg hours per CR: 5 (complex reviews, multiple stakeholder gates)
- Blended cost: USD 95
- CR Processing Cost = 15 × 5 × 95 = **USD 7,125**
- Interpretation: USD 7.125k processing cost; significant due to high change volume. Consider process automation.

**Target (Green):** < 0.5% of contract value
**Alert (Red):** > 1.5% of contract value (change process overhead too high)
**Dashboard Location:** Financial Tab → Change Management → CR Processing Cost + CR Trends

---

### 28. Revenue Realisation Percentage

**Definition:** Percentage of committed revenue actually realized (billed and collected).

**Formula Expression:**
```
Revenue Realisation % = (Realized Revenue / Committed Revenue) × 100
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Committed revenue (milestone due this month): USD 500,000
- Realized revenue (actually billed): USD 480,000
- Revenue Realisation % = (480,000 / 500,000) × 100 = **96%**
- Interpretation: 96% realized; 4% deferred (milestone not 100% complete, deferred to May). Good; typical in milestone-based billing.

**Worked Example 2 — Fintech Programme (April 2024):**
- Committed revenue: USD 400,000
- Realized revenue: USD 315,000
- Revenue Realisation % = (315,000 / 400,000) × 100 = **78.75%**
- Interpretation: 22.25% deferred; significant. Indicates delivery delays or billing holds. Cash flow impact.

**Target (Green):** ≥ 90% (good realization)
**Alert (Red):** < 80% (material revenue deferral; cash flow concern)
**Dashboard Location:** Financial Tab → Revenue Management → Revenue Realisation % card + Realization Trend

---

## QUALITY & VELOCITY (4 Formulas)

### 29. Sprint Leakage Percentage

**Definition:** Percentage of planned story points not completed in sprint.

**Formula Expression:**
```
Sprint Leakage % = ((Planned Points - Completed Points) / Planned Points) × 100
```

**Worked Example 1 — Healthcare Sprint 5 (April 2024):**
- Planned story points: 120
- Completed story points: 108
- Sprint Leakage % = ((120 - 108) / 120) × 100 = **10%**
- Interpretation: 10% of planned work not completed; slipped to next sprint. Minor; typical variance.

**Worked Example 2 — Fintech Sprint 8 (April 2024):**
- Planned: 100 points
- Completed: 72 points
- Sprint Leakage % = ((100 - 72) / 100) × 100 = **28%**
- Interpretation: 28% leakage; significant. Indicates estimation error, resource unavailability, or blockers. Investigate.

**Target (Green):** 5–15% (normal variance)
**Alert (Red):** > 20% (consistent miss; process issue)
**Dashboard Location:** Delivery Tab → Sprint Execution → Sprint Leakage % card + Leakage Trend Chart

---

### 30. Rework Percentage

**Definition:** Percentage of delivered features requiring rework (defects, requirement misalignment, tech debt).

**Formula Expression:**
```
Rework % = (Rework Hours / Total Delivery Hours) × 100
```

**Worked Example 1 — Healthcare (April 2024):**
- Rework hours: 96 (defects identified in QA, tech debt fixes)
- Total delivery hours: 1,200
- Rework % = (96 / 1,200) × 100 = **8%**
- Interpretation: 8% of effort is rework; acceptable quality level. Indicates mature process.

**Worked Example 2 — Fintech (April 2024):**
- Rework hours: 130 (high defect count, requirement misalignment)
- Total delivery hours: 650
- Rework % = (130 / 650) × 100 = **20%**
- Interpretation: 20% rework; high. Quality issue; impacts velocity and margin.

**Target (Green):** 5–10% (normal rework)
**Alert (Red):** > 15% (quality concern; escalate)
**Dashboard Location:** Delivery Tab → Quality → Rework % card + Defect Trend Chart

---

### 31. AI Quality-Adjusted Velocity

**Definition:** Velocity adjusted for AI tool influence on quality (uplift % applied to base velocity).

**Formula Expression:**
```
AI Quality-Adjusted Velocity = Velocity × (1 + AI Quality Uplift %) × (1 - Rework %)
```

**Worked Example 1 — Healthcare Sprint 5 (AI-enhanced):**
- Base velocity: 108 story points completed
- AI quality uplift: +12% (AI code generation + test automation reducing defects)
- Rework percentage: 8%
- AI Quality-Adjusted Velocity = 108 × (1 + 0.12) × (1 - 0.08) = 108 × 1.12 × 0.92 = **111.4 adjusted points**
- Interpretation: Effective velocity 111.4 after accounting for AI uplift and rework; net gain of 3.4 points (3.1%) vs. base.

**Worked Example 2 — Fintech Sprint 8 (no AI benefit yet):**
- Base velocity: 72 points
- AI quality uplift: 0% (limited AI adoption)
- Rework: 20%
- AI Quality-Adjusted Velocity = 72 × (1 + 0) × (1 - 0.20) = 72 × 0.80 = **57.6 adjusted points**
- Interpretation: After accounting for rework, effective velocity only 57.6; significant quality drag.

**Target (Green):** Adjusted velocity ≥ planned velocity trend
**Alert (Red):** Declining adjusted velocity (quality degradation)
**Dashboard Location:** Delivery Tab → AI Impact → AI Quality-Adjusted Velocity card + Sprint Trend

---

### 32. AI Trust Score

**Definition:** Composite trust score (0–100) based on AI tool adoption, quality/velocity uplift, cost avoidance, and failure rate.

**Formula Expression:**
```
AI Trust Score = (0.30 × Adoption Rate %) + (0.25 × Quality Uplift %) + (0.25 × Velocity Uplift %) + (0.20 × Cost Avoidance / Total Cost %)
- (Failure Penalty = # AI-Generated-Defects × 2 points each, max -15)
```

**Worked Example 1 — Healthcare Programme (April 2024):**
- Adoption Rate: 60% (6 of 10 developers using GitHub Copilot, Claude, etc.)
- Quality Uplift: +12%
- Velocity Uplift: +18%
- Cost Avoidance: USD 8,000 / USD 225,000 labour cost = 3.6%
- AI-Generated Defects: 2 (minor; -4 points)
- AI Trust Score = (0.30 × 60) + (0.25 × 12) + (0.25 × 18) + (0.20 × 3.6) - 4
  - = 18 + 3 + 4.5 + 0.72 - 4 = **22.22** (note: high adoption needed; adjust to 60/100 scale)
- Normalized to 0–100: ~**78/100** (strong AI integration)
- Interpretation: High trust in AI tooling; benefits realized, few failures.

**Worked Example 2 — Fintech Programme (April 2024):**
- Adoption Rate: 30% (limited use; team hesitant)
- Quality Uplift: 0%
- Velocity Uplift: +5% (minimal)
- Cost Avoidance: USD 2,000 / USD 280,000 = 0.7%
- AI-Generated Defects: 5 (code generation issues; -10 points)
- AI Trust Score = (0.30 × 30) + (0.25 × 0) + (0.25 × 5) + (0.20 × 0.7) - 10
  - = 9 + 0 + 1.25 + 0.14 - 10 = **0.39** → **26/100** (low trust)
- Interpretation: Low AI adoption; no quality gains; defects reducing trust. Requires change management / training.

**Target (Green):** 70–100 (strong AI integration and value)
**Alert (Red):** < 50 (low trust; AI not delivering value)
**Dashboard Location:** AI Impact Tab → AI Trust Score card + AI Maturity Gauge

---

## CLOSEOUT (2 Formulas)

### 33. Closeout Variance

**Definition:** Final budget vs. actual cost variance at programme completion.

**Formula Expression:**
```
Closeout Variance = BAC - Final Actual Cost
```

**Worked Example 1 — Healthcare Programme (Completed Q4 2024):**
- BAC: USD 5,000,000
- Final Actual Cost: USD 4,720,585 (as forecasted earlier, achieved)
- Closeout Variance = 5,000,000 - 4,720,585 = **USD 279,415** (positive = savings)
- Interpretation: Programme delivered USD 279k under budget. Strong execution; final CPI maintained at 1.059.

**Worked Example 2 — Fintech Programme (Completed Q3 2024):**
- BAC: USD 3,200,000
- Final Actual Cost: USD 3,488,000 (cost overrun materialized)
- Closeout Variance = 3,200,000 - 3,488,000 = **USD -288,000** (negative = overrun)
- Interpretation: USD 288k cost overrun despite mitigation efforts. Root cause: scope creep (USD 200k), resource inefficiency (USD 88k).

**Target (Green):** Closeout Variance ≥ 0 (at or under budget)
**Alert (Red):** Closeout Variance < -(5% of BAC) (significant overrun)
**Dashboard Location:** Closeout Tab → Financial Closeout → Closeout Variance card + Final Results Summary

---

### 34. Variance Decomposition

**Definition:** Analysis breaking down total variance into Schedule Variance and Cost Variance components.

**Formula Expression:**
```
Schedule Variance (SV) = EV - PV
Cost Variance (CV) = EV - AC
Total Variance = SV + CV (not additive; shown separately)
```

**Worked Example 1 — Healthcare Programme (Month 4):**
- EV (Earned Value): USD 2,250,000
- PV (Planned Value): USD 2,400,000
- AC (Actual Cost): USD 1,700,000
- Schedule Variance = 2,250,000 - 2,400,000 = **USD -150,000** (behind schedule)
- Cost Variance = 2,250,000 - 1,700,000 = **USD 550,000** (under cost)
- Decomposition: 6.25% schedule slip, 24.4% cost efficiency
- Interpretation: Programme is ahead on cost (good CPI) but lagging schedule (SPI 0.938). Cost efficiency masking schedule risk.

**Worked Example 2 — Fintech Programme (Month 3):**
- EV: USD 1,024,000
- PV: USD 1,280,000
- AC: USD 980,000
- Schedule Variance = 1,024,000 - 1,280,000 = **USD -256,000** (behind schedule)
- Cost Variance = 1,024,000 - 980,000 = **USD 44,000** (under cost so far)
- Decomposition: 20% schedule slip, 4.3% cost efficiency (weak)
- Interpretation: Both schedule and cost risk; schedule lag primary concern (20% slip). Cost variance small; could reverse as scope overruns continue.

**Target (Green):** SV ≥ 0 and CV ≥ 0 (on schedule and on cost)
**Alert (Red):** Both SV < 0 and CV < 0 (dual risk; escalate)
**Dashboard Location:** Closeout Tab → Variance Analysis → Variance Decomposition table + Variance Trend Chart

---

## PORTFOLIO (3 Formulas)

### 35. Portfolio Health Index (PHI)

**Definition:** Weighted composite score (0–100) of portfolio health across all programmes, weighted by BAC.

**Formula Expression:**
```
PHI = Σ(Programme DHI × Programme BAC / Total Portfolio BAC)
DHI = (0.35 × CPI) + (0.35 × SPI) + (0.15 × Quality Score/100) + (0.15 × Utilization %)
```

**Worked Example 1 — Q2 2024 Portfolio (3 programmes):**
- Healthcare: BAC USD 5M, CPI 1.059, SPI 0.938, Quality 92%, Utilization 85%
  - DHI = (0.35 × 1.059) + (0.35 × 0.938) + (0.15 × 0.92) + (0.15 × 0.85) = 0.3706 + 0.3283 + 0.138 + 0.1275 = 0.9644 → 96.44/100
- Fintech: BAC USD 3.2M, CPI 0.903, SPI 0.800, Quality 78%, Utilization 90%
  - DHI = (0.35 × 0.903) + (0.35 × 0.800) + (0.15 × 0.78) + (0.15 × 0.90) = 0.3161 + 0.2800 + 0.117 + 0.135 = 0.8481 → 84.81/100
- Logistics: BAC USD 4.2M, CPI 1.025, SPI 0.945, Quality 88%, Utilization 88%
  - DHI = (0.35 × 1.025) + (0.35 × 0.945) + (0.15 × 0.88) + (0.15 × 0.88) = 0.3588 + 0.3308 + 0.132 + 0.132 = 0.9536 → 95.36/100
- Total BAC: USD 12.4M
- PHI = (96.44 × 5.0 + 84.81 × 3.2 + 95.36 × 4.2) / 12.4
  - = (482.2 + 271.4 + 400.5) / 12.4 = 1154.1 / 12.4 = **93.07/100** (Green)
- Interpretation: Portfolio health strong; Fintech dragging down overall score but offset by strong Healthcare and Logistics.

**Worked Example 2 — Q3 2024 Portfolio (4 programmes, stress scenario):**
- Healthcare: BAC USD 5M, CPI 1.040, SPI 0.920, Quality 90%, Utilization 82%
  - DHI = (0.35 × 1.040) + (0.35 × 0.920) + (0.15 × 0.90) + (0.15 × 0.82) = 0.364 + 0.322 + 0.135 + 0.123 = 0.944 → 94.4/100
- Fintech: BAC USD 3.2M, CPI 0.885, SPI 0.780, Quality 72%, Utilization 92%
  - DHI = (0.35 × 0.885) + (0.35 × 0.780) + (0.15 × 0.72) + (0.15 × 0.92) = 0.310 + 0.273 + 0.108 + 0.138 = 0.829 → 82.9/100
- Logistics: BAC USD 4.2M, CPI 0.950, SPI 0.880, Quality 84%, Utilization 85%
  - DHI = (0.35 × 0.950) + (0.35 × 0.880) + (0.15 × 0.84) + (0.15 × 0.85) = 0.3325 + 0.308 + 0.126 + 0.1275 = 0.894 → 89.4/100
- Public Sector (new): BAC USD 2.5M, CPI 0.920, SPI 0.700, Quality 68%, Utilization 78%
  - DHI = (0.35 × 0.920) + (0.35 × 0.700) + (0.15 × 0.68) + (0.15 × 0.78) = 0.322 + 0.245 + 0.102 + 0.117 = 0.786 → 78.6/100
- Total BAC: USD 14.9M
- PHI = (94.4 × 5.0 + 82.9 × 3.2 + 89.4 × 4.2 + 78.6 × 2.5) / 14.9
  - = (472 + 265.3 + 375.5 + 196.5) / 14.9 = 1309.3 / 14.9 = **87.87/100** (Yellow/Caution)
- Interpretation: Portfolio health declining; Fintech and Public Sector dragging down average. Steering intervention required.

**Target (Green):** > 90 (healthy portfolio)
**Alert (Red):** < 75 (portfolio health at risk; escalate)
**Dashboard Location:** Executive Tab → Portfolio Health → Portfolio Health Index gauge + Programme Contribution breakdown

---

### 36. Weighted Portfolio CPI

**Definition:** Blended Cost Performance Index across all programmes, weighted by BAC.

**Formula Expression:**
```
Weighted Portfolio CPI = Σ(Programme CPI × Programme BAC) / Total Portfolio BAC
```

**Worked Example 1 — Q2 2024 Portfolio:**
- Healthcare: CPI 1.059, BAC USD 5M
- Fintech: CPI 0.903, BAC USD 3.2M
- Logistics: CPI 1.025, BAC USD 4.2M
- Total BAC: USD 12.4M
- Weighted Portfolio CPI = ((1.059 × 5.0) + (0.903 × 3.2) + (1.025 × 4.2)) / 12.4
  - = (5.295 + 2.890 + 4.305) / 12.4 = 12.49 / 12.4 = **1.007**
- Interpretation: Portfolio cost performance at breakeven (CPI 1.007); modest cost efficiency. Healthcare and Logistics offset by Fintech overrun.

**Worked Example 2 — Q3 2024 Portfolio (stress scenario):**
- Healthcare: CPI 1.040, BAC USD 5M
- Fintech: CPI 0.885, BAC USD 3.2M
- Logistics: CPI 0.950, BAC USD 4.2M
- Public Sector: CPI 0.920, BAC USD 2.5M
- Total BAC: USD 14.9M
- Weighted Portfolio CPI = ((1.040 × 5.0) + (0.885 × 3.2) + (0.950 × 4.2) + (0.920 × 2.5)) / 14.9
  - = (5.20 + 2.832 + 3.99 + 2.30) / 14.9 = 14.322 / 14.9 = **0.961**
- Interpretation: Portfolio CPI deteriorating to 0.961 (3.9% cost overrun). Trend negative; needs corrective action.

**Target (Green):** ≥ 1.0 (portfolio on budget or better)
**Alert (Red):** < 0.95 (portfolio cost overrun; escalate)
**Dashboard Location:** Executive Tab → Portfolio Health → Weighted Portfolio CPI card + Portfolio Cost Trend

---

### 37. Delivery Health Index (DHI)

**Definition:** Composite health score (0–100) for a single programme, integrating cost, schedule, quality, and utilization.

**Formula Expression:**
```
DHI = (0.35 × CPI) + (0.35 × SPI) + (0.15 × Quality Score/100) + (0.15 × Utilization %)
```
*Note: See formula 35 for component definitions; DHI is the building block for PHI.*

**Worked Example 1 — Healthcare Programme (April 2024):**
- CPI: 1.059
- SPI: 0.938
- Quality Score: 92%
- Utilization: 85%
- DHI = (0.35 × 1.059) + (0.35 × 0.938) + (0.15 × 0.92) + (0.15 × 0.85)
  - = 0.3706 + 0.3283 + 0.138 + 0.1275 = 0.9644
- Normalized to 0–100: **96.44/100** (Green; excellent)
- Interpretation: Programme is healthy across all dimensions. Cost efficient, nearly on schedule, high quality, good utilization.

**Worked Example 2 — Fintech Programme (April 2024):**
- CPI: 0.903
- SPI: 0.800
- Quality Score: 78%
- Utilization: 90%
- DHI = (0.35 × 0.903) + (0.35 × 0.800) + (0.15 × 0.78) + (0.15 × 0.90)
  - = 0.3161 + 0.2800 + 0.117 + 0.135 = 0.8481
- Normalized to 0–100: **84.81/100** (Yellow; caution)
- Interpretation: Programme struggling on cost (CPI 0.903) and schedule (SPI 0.800); quality and utilization not compensating. Escalation recommended.

**Target (Green):** > 85 (healthy programme)
**Alert (Red):** < 70 (programme at risk; intervention needed)
**Dashboard Location:** Delivery Tab → Programme Health → DHI card + DHI Trend Chart per programme

---

## Summary Table — All 37 Formulas

| # | Formula | Category | Target (Green) | Alert (Red) | Dashboard Tab |
|---|---------|----------|--|--|--|
| 1 | BAC | Estimation | Locked in SOW | Not approved | Financial |
| 2 | Blended Cost/Hour | Estimation | 1.8–2.3 USD | >2.8 or <1.2 | Financial |
| 3 | Loaded Cost | Estimation | ≤ Revenue/Resource | > Revenue | People |
| 4 | Billable Hours/Year | Estimation | 1,700–1,850 hrs | >2,000 or <1,400 | Estimation |
| 5 | Overhead Allocation % | Estimation | 25–40% | >50% or <15% | Financial |
| 6 | Contingency % | Estimation | 10–15% | <5% or >25% | Financial |
| 7 | CPI | Cost Performance | ≥ 1.0 | < 0.95 | Financial |
| 8 | Earned Value (EV) | Cost Performance | EV ≥ PV | EV << PV | Financial |
| 9 | EAC | Cost Performance | ≤ BAC | > BAC | Financial |
| 10 | ETC | Cost Performance | ≤ Remaining Budget | > Remaining Budget | Financial |
| 11 | TCPI | Cost Performance | 0.90–1.10 | <0.85 or >1.15 | Financial |
| 12 | VAC | Cost Performance | ≥ 0 | < -(5% BAC) | Financial |
| 13 | SPI | Cost Performance | ≥ 0.95 | < 0.90 | Delivery |
| 14 | Gross Margin % | Margin | 40–55% | < 30% | Financial |
| 15 | Contribution Margin % | Margin | 25–40% | < 15% | Financial |
| 16 | Portfolio Margin % | Margin | 38–48% | < 32% | Executive |
| 17 | Net Margin % | Margin | 15–25% | <10% or negative | Financial |
| 18 | HRIS Utilization % | Utilization | 85–100% | <75% or >105% | People |
| 19 | RM Utilization % | Utilization | 85–95% | <75% or >98% | People |
| 20 | Billing Utilization % | Utilization | 95–100% | < 90% | Delivery |
| 21 | Utilization Waterfall Loss | Utilization | < 10% | > 15% | Delivery |
| 22 | Shadow Allocation Cost | Bench | > 30% offset | < 15% offset | Financial |
| 23 | Bench Runway | Bench | > 30 days | < 15 days | People |
| 24 | Daily Bench Burn | Bench | < USD 3,000/day | > USD 6,000/day | People |
| 25 | Revenue Leakage % | Leakage | 2–5% | > 10% | Financial |
| 26 | Scope Absorption Cost | Leakage | < 1% contract value | > 2% contract value | Financial |
| 27 | CR Processing Cost | Leakage | < 0.5% contract value | > 1.5% contract value | Financial |
| 28 | Revenue Realisation % | Leakage | ≥ 90% | < 80% | Financial |
| 29 | Sprint Leakage % | Quality | 5–15% | > 20% | Delivery |
| 30 | Rework % | Quality | 5–10% | > 15% | Delivery |
| 31 | AI Quality-Adjusted Velocity | Quality | ≥ Planned trend | Declining | Delivery/AI |
| 32 | AI Trust Score | Quality | 70–100 | < 50 | AI Impact |
| 33 | Closeout Variance | Closeout | ≥ 0 | < -(5% BAC) | Closeout |
| 34 | Variance Decomposition | Closeout | SV ≥0, CV ≥0 | Both <0 | Closeout |
| 35 | Portfolio Health Index | Portfolio | > 90 | < 75 | Executive |
| 36 | Weighted Portfolio CPI | Portfolio | ≥ 1.0 | < 0.95 | Executive |
| 37 | Delivery Health Index (DHI) | Portfolio | > 85 | < 70 | Delivery |

---

## Formula Validation Rules

**All formulas enforce:**
- Denominator never zero (handled with NULL result or default 0 if numerator 0)
- Results capped to sensible ranges (e.g., percentages 0–100; indices 0–100)
- Recalculation triggered on any underlying data change
- Nightly batch recalculation of all 45 formulas across all programmes

---

## NEW IN v5.1 (3 Formulas)

### 38. Renewal Probability

**Definition:** Weighted composite score predicting the likelihood of contract renewal based on delivery health, customer satisfaction, and relationship quality.

**Formula Expression:**
```
Renewal Score = (CSAT × 0.30) + (Delivery Health × 0.25) + (Escalation Score × 0.20)
              + (Communication Score × 0.15) + (Innovation Score × 0.10)

Where:
- CSAT: Latest survey score normalised to 0-100 (e.g., 8.2/10 = 82)
- Delivery Health: DHI composite score from Tab 1
- Escalation Score: 100 - (Open Escalations × 15), minimum 0
- Communication Score: (Steering Meetings Held / Steering Meetings Planned) × 100
- Innovation Score: (Process Improvements Proposed + AI Initiatives Active) × 10, maximum 100
```

**Worked Example 1 — Orion Data Platform (Healthy Account):**
- CSAT: 8.5/10 = 85
- DHI: 78
- Open Escalations: 1 → Escalation Score = 100 - (1 × 15) = 85
- Meetings: 11 held / 12 planned = 91.7
- Innovations: 3 proposals + 2 AI initiatives = 5 → Innovation Score = 50
- Renewal Score = (85 × 0.30) + (78 × 0.25) + (85 × 0.20) + (91.7 × 0.15) + (50 × 0.10)
- = 25.5 + 19.5 + 17.0 + 13.8 + 5.0 = **80.8 (Green — renewal highly likely)**
- Interpretation: Solid delivery health and high satisfaction. Slight gap on innovation score — consider proposing more AI-driven efficiency improvements.

**Worked Example 2 — Titan Digital Commerce (At Risk):**
- CSAT: 6.8/10 = 68
- DHI: 55
- Open Escalations: 4 → Escalation Score = 100 - (4 × 15) = 40
- Meetings: 7 held / 12 planned = 58.3
- Innovations: 1 proposal + 0 AI = 1 → Innovation Score = 10
- Renewal Score = (68 × 0.30) + (55 × 0.25) + (40 × 0.20) + (58.3 × 0.15) + (10 × 0.10)
- = 20.4 + 13.75 + 8.0 + 8.75 + 1.0 = **51.9 (Red — renewal at risk)**
- Interpretation: Multiple signals of account distress. 4 open escalations, missed governance meetings, and no innovation proposals. Requires immediate proactive account governance: executive sponsor meeting, escalation resolution plan, and communication cadence reset.

**Target (Green):** ≥ 80 (renewal highly likely)
**Amber:** 60-79 (renewal probable with attention)
**Alert (Red):** < 60 (renewal at risk — trigger proactive account governance)
**Dashboard Location:** Tab 10 (Customer Intelligence) → Renewal Gauge

---

### 39. AI Cost-Benefit Ratio

**Definition:** Measures whether AI tool investment is generating positive ROI by comparing the financial value of time saved against the total cost of AI (tool licenses + rework from AI-generated output).

**Formula Expression:**
```
AI Cost-Benefit Ratio = (Time Saved × Blended Rate) / (AI Tool Cost + AI Rework Cost)

Where:
- Time Saved: Hours saved per period from AI usage (from ai_usage_metrics.time_saved_hours)
- Blended Rate: Weighted average billable rate for the team
- AI Tool Cost: Total AI tool licensing cost for the period
- AI Rework Cost: Hours spent fixing AI-generated output × Blended Rate
```

**Worked Example 1 — Sentinel (AI-Heavy, 6 Months In):**
- Time Saved: 1,240 hours over 6 months (from usage tracking)
- Blended Rate: ₹2,500/hour
- Value of Time Saved: 1,240 × ₹2,500 = ₹31,00,000
- AI Tool Cost: ₹3,60,000 (GitHub Copilot + Tabnine for 12 developers, 6 months)
- AI Rework Cost: 185 hours × ₹2,500 = ₹4,62,500
- Total AI Cost: ₹3,60,000 + ₹4,62,500 = ₹8,22,500
- AI Cost-Benefit Ratio = ₹31,00,000 / ₹8,22,500 = **3.77**
- Interpretation: For every ₹1 spent on AI tools (including rework), the team recovered ₹3.77 in productivity. Strong ROI — recommend expansion.

**Worked Example 2 — Phoenix (AI-Light, Early Adoption):**
- Time Saved: 180 hours over 3 months
- Blended Rate: ₹2,200/hour
- Value of Time Saved: 180 × ₹2,200 = ₹3,96,000
- AI Tool Cost: ₹1,80,000 (Copilot for 8 developers, 3 months)
- AI Rework Cost: 95 hours × ₹2,200 = ₹2,09,000
- Total AI Cost: ₹1,80,000 + ₹2,09,000 = ₹3,89,000
- AI Cost-Benefit Ratio = ₹3,96,000 / ₹3,89,000 = **1.02**
- Interpretation: Barely breaking even. Rework cost (₹2.09L) nearly equals tool cost (₹1.80L), indicating AI output quality is not yet stable. Recommend: continue for 2 more sprints, tighten review gates, evaluate tool-team fit before expanding.

**Target (Green):** ≥ 2.0 (clear ROI)
**Amber:** 1.0-1.99 (marginal — monitor)
**Alert (Red):** < 1.0 (negative ROI — review AI tool selection and usage patterns)
**Dashboard Location:** Tab 6 (AI Governance) → AI Cost-Benefit Analysis panel

---

### 40. Forecast Confidence

**Definition:** Statistical measure of how reliable the predictive forecast is, based on the goodness-of-fit (R²) of the linear regression model applied to the last 6-12 historical data points.

**Formula Expression:**
```
Forecast Confidence = R² × 100

Where:
- R² (coefficient of determination) is computed from scipy.stats.linregress
  on the last 6-12 monthly data points for a given KPI
- R² ranges from 0 to 1
  - 1.0 = perfect fit (all variance explained by the trend)
  - 0.0 = no linear relationship (forecast is unreliable)
```

**Worked Example 1 — Phoenix CPI Forecast (Strong Trend):**
- Historical CPI (6 months): 0.95, 0.93, 0.90, 0.87, 0.84, 0.81
- Linear regression: slope = -0.028/month, intercept = 0.978
- R² = 0.997
- Forecast Confidence = 0.997 × 100 = **99.7%**
- Interpretation: CPI is declining in a highly predictable pattern. The forecast that CPI will reach 0.78 next month is very reliable. This is a clear trend — not noise.

**Worked Example 2 — Orion Utilisation Forecast (Volatile):**
- Historical Utilisation (8 months): 74%, 71%, 78%, 72%, 76%, 73%, 77%, 74%
- Linear regression: slope = +0.11/month, intercept = 73.5
- R² = 0.032
- Forecast Confidence = 0.032 × 100 = **3.2%**
- Interpretation: Utilisation fluctuates without a clear trend. The linear forecast is unreliable — the system should use weighted moving average instead for this KPI. Confidence below 50% means the dashed forecast line will show a wider confidence band and reduced visual prominence.

**Target (Green):** ≥ 70% (forecast is reliable)
**Amber:** 40-69% (forecast is indicative, not predictive)
**Alert (Red):** < 40% (forecast is unreliable — use with caution, wider confidence bands displayed)
**Dashboard Location:** Tab 2 (KPI Studio) → Forecast chart tooltip shows confidence %; Tab 3 (Delivery Planning) → EVM forecast confidence meter

---

## NEW IN v5.2: MULTI-CURRENCY & FLOW METRICS (5 Formulas)

### 41. Currency Conversion (Base Aggregation)

**Definition:** Converts a local-currency amount to the portfolio's base currency using the effective exchange rate for the given date. All portfolio-level aggregations (Tab 1, Tab 5) display base currency totals.

**Formula Expression:**
```
Base Amount = Local Amount × Exchange Rate (local → base, effective date)

Where:
- Exchange Rate is looked up from currency_rates table
- Effective date = closest rate on or before the transaction date
- If no rate found, the system flags the amount as "unconverted" and excludes from aggregation
```

**Worked Example 1 — GBP Project in USD Portfolio:**
- Project revenue: GBP £1,200,000
- Base currency: USD
- GBP→USD rate (effective 2026-03-01): 1.2650
- Base Amount = £1,200,000 × 1.2650 = **USD $1,518,000**
- Interpretation: This GBP project contributes $1.518M to the USD-denominated portfolio total on Tab 1.

**Worked Example 2 — INR Project in USD Portfolio:**
- Project cost: INR ₹28,00,00,000 (₹28 Crore)
- Base currency: USD
- INR→USD rate (effective 2026-03-01): 0.01190 (i.e., 1 INR = $0.0119, or ₹84 = $1)
- Base Amount = ₹28,00,00,000 × 0.01190 = **USD $3,332,000**
- Interpretation: The INR delivery centre's cost contributes $3.33M to the USD portfolio total.

**Target (Green):** All projects have valid exchange rates within 30 days
**Alert (Red):** Any project has no exchange rate, or rate is >90 days stale
**Dashboard Location:** Tab 5 (Margin & EVM) → multi-currency aggregation panel; Tab 11 (Data Hub) → Currency Rates management

---

### 42. Kanban Throughput

**Definition:** Number of work items completed in a measurement period (typically weekly). The fundamental output metric for Kanban teams — analogous to sprint velocity for Scrum.

**Formula Expression:**
```
Throughput = Count of items moved to "Done" in [period_start, period_end]
```

**Worked Example 1 — DATAOPS-001 Week of 2026-03-22:**
- Items completed: 9
- Throughput = **9 items/week**
- Interpretation: Best week in the 5-week dataset. Team exceeded their 4-week average of 7.4 items/week, suggesting process improvement or reduced blockers.

**Worked Example 2 — DATAOPS-001 Week of 2026-03-15:**
- Items completed: 6
- Throughput = **6 items/week**
- Interpretation: Below average. Correlates with highest blocked_time_hours (6.5 hrs) in the dataset. Root cause: dependency on external API team.

**Target (Green):** Throughput stable or trending up (within 1 std dev of 4-week average)
**Alert (Red):** Throughput drops >25% below 4-week average for 2 consecutive weeks
**Dashboard Location:** Tab 3B (Kanban sub-view) → Throughput trend chart

---

### 43. Cycle Time (p50 / p85 / p95)

**Definition:** Time elapsed from "In Progress" to "Done" for a work item, measured at the 50th, 85th, and 95th percentiles. p50 represents the typical item; p85 is used for SLA commitments ("85% of items complete within X days"); p95 flags outliers.

**Formula Expression:**
```
Cycle Time pN = Nth percentile of (Done Date - In Progress Date) across all items in period

Where:
- p50 = median cycle time
- p85 = 85th percentile (commonly used for delivery commitments)
- p95 = 95th percentile (outlier detection)
```

**Worked Example 1 — DATAOPS-001 Week of 2026-03-22:**
- p50 = 2.8 days, p85 = 5.4 days, p95 = 8.1 days
- Interpretation: Typical item completes in under 3 days. 85% of items finish within 5.4 days. Only 5% take longer than 8.1 days. Healthy distribution with narrow spread.

**Worked Example 2 — DATAOPS-001 Week of 2026-03-15:**
- p50 = 3.9 days, p85 = 7.2 days, p95 = 10.4 days
- Interpretation: Cycle times inflated across all percentiles. p85 at 7.2 days means SLA commitments are at risk. Correlates with high blocked time (6.5 hrs). Root cause investigation warranted.

**Target (Green):** p85 ≤ team's SLA commitment (e.g., 7 days)
**Amber:** p85 exceeds SLA by up to 20%
**Alert (Red):** p85 exceeds SLA by >20% for 2+ consecutive weeks
**Dashboard Location:** Tab 3B (Kanban sub-view) → Cycle Time scatter plot with percentile lines

---

### 44. Lead Time

**Definition:** Time elapsed from item creation (request received) to item completion (delivered). Includes queue time + cycle time. Measures the customer's experience of delivery speed — how long from asking to receiving.

**Formula Expression:**
```
Lead Time = Done Date - Created Date

Lead Time Avg = Mean of Lead Time across all items completed in period
```

**Worked Example 1 — DATAOPS-001 Week of 2026-03-22:**
- Lead Time Avg = 8.5 days
- Cycle Time p50 = 2.8 days
- Queue Time (implied) = 8.5 - 2.8 = 5.7 days
- Interpretation: Items wait 5.7 days in the backlog before work starts. Once started, they finish in 2.8 days. Queue time dominates — backlog prioritisation or WIP limits may help.

**Worked Example 2 — DATAOPS-001 Week of 2026-03-15:**
- Lead Time Avg = 10.1 days
- Cycle Time p50 = 3.9 days
- Queue Time (implied) = 10.1 - 3.9 = 6.2 days
- Interpretation: Both queue and cycle time increased. Total lead time above 10 days means stakeholders wait nearly 2 weeks from request to delivery. Investigate both backlog grooming cadence and blocked time.

**Target (Green):** Lead Time Avg ≤ 2× Cycle Time p50 (indicates reasonable queue time)
**Amber:** Lead Time Avg = 2-3× Cycle Time p50
**Alert (Red):** Lead Time Avg > 3× Cycle Time p50 (excessive queue time)
**Dashboard Location:** Tab 3B (Kanban sub-view) → Lead Time trend; Tab 4 (Velocity & Flow) → Lead Time vs Cycle Time comparison

---

### 45. WIP Aging

**Definition:** Age (in days) of each work item currently in progress, compared to the team's cycle time percentiles. Items older than the p85 cycle time are "aging" — they're taking longer than 85% of historical items and are at risk of becoming blockers.

**Formula Expression:**
```
Item Age = Today - In Progress Date

WIP Aging Category:
- Green: Age < Cycle Time p50 (on track)
- Amber: Cycle Time p50 ≤ Age < Cycle Time p85 (watch)
- Red: Age ≥ Cycle Time p85 (aging — intervention needed)
```

**Worked Example 1 — DATAOPS-001 Current WIP:**
- Item A: In Progress since 2026-04-14 = 2 days old → p50 = 3.3 → **Green** (on track)
- Item B: In Progress since 2026-04-10 = 6 days old → p85 = 6.2 → **Red** (aging)
- Item C: In Progress since 2026-04-12 = 4 days old → p50 = 3.3, p85 = 6.2 → **Amber** (watch)
- Interpretation: 1 of 3 WIP items is aging beyond p85. Standup should focus on unblocking Item B.

**Worked Example 2 — Team with WIP Limit 18, Current WIP 15:**
- 10 items Green, 3 items Amber, 2 items Red
- WIP utilisation = 15/18 = 83%
- Interpretation: WIP is within limits, but 2 red items need immediate attention. The heatmap should highlight these in the daily standup view.

**Target (Green):** ≤10% of WIP items in Red
**Amber:** 10-25% of WIP items in Red
**Alert (Red):** >25% of WIP items in Red (systemic flow problem)
**Dashboard Location:** Tab 3B (Kanban sub-view) → WIP Aging heatmap (items coloured by age category)

---

## Support & Questions

For formula interpretation or calculation verification:
- **Tab 3 (Delivery Health)** includes a "?" icon for each metric with live formula reference and worked examples
- **Data Lineage (Tab 11)** click any number to see the full calculation chain
- **API:** `GET /api/v1/kpis` returns formula definitions with thresholds

---

**Last Updated:** 2026-04-16
**Version:** 5.2
**Maintainer:** Adi Kompalli — AKB1 Framework
