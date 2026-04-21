/**
 * Central formula + business-context library.
 * Every metric shown anywhere in the UI has an entry here.
 * MetricCard renders this inline when the user toggles the Eye icon.
 */

export type DrillFilter =
  | "completed"
  | "in_progress"
  | "ai_assisted"
  | "rework"
  | "defects"
  | "planned"
  | "blocked"
  | null;

export type Threshold = { green: string; amber: string; red: string };

export type MetricDef = {
  id: string;
  label: string;
  formula: string;
  description: string;
  interpretation: string;
  unit: string;
  drillFilter?: DrillFilter;
  thresholds?: Threshold;
};

// ─── Sprint / Scrum ────────────────────────────────────────────────────────

export const SPRINT_METRICS: Record<string, MetricDef> = {
  planned_points: {
    id: "planned_points",
    label: "Planned points",
    formula: "SUM(story_points WHERE status != 'added')",
    description:
      "Total story-point commitment the team accepted into this sprint at planning time. Items added after the sprint started are excluded so the baseline stays honest.",
    interpretation:
      "Compare sprint-over-sprint to spot scope creep. A sudden jump usually means the team is over-committing under external pressure — a leading indicator of carry-over and morale decay.",
    unit: "story points",
    drillFilter: "planned",
    thresholds: { green: "Stable ±10% of team average", amber: ">20% above average", red: ">35% above average" },
  },
  completed_points: {
    id: "completed_points",
    label: "Completed points",
    formula: "SUM(story_points WHERE status IN ('completed', 'added'))",
    description:
      "Story points accepted as 'done' by end of sprint, including scope-added items that were completed. This is the delivery output, not the commitment.",
    interpretation:
      "Against Planned Points this gives burndown%. A CTO watching this wants it ≥90% of planned to call the sprint healthy. Persistent gaps below 80% signal team capacity mis-estimation or dependency drag.",
    unit: "story points",
    drillFilter: "completed",
    thresholds: { green: "≥90% of planned", amber: "70–89% of planned", red: "<70% of planned" },
  },
  burndown_pct: {
    id: "burndown_pct",
    label: "Burndown",
    formula: "completed_points / planned_points × 100",
    description:
      "Percentage of the sprint commitment delivered. Reaches 100% only when every planned item is done (not carried-over, not in-progress).",
    interpretation:
      "The single most-watched sprint KPI for delivery assurance. Below 80% two sprints in a row triggers a retrospective on capacity accuracy. Below 70% triggers an escalation to the programme level.",
    unit: "%",
    thresholds: { green: "≥90%", amber: "70–89%", red: "<70%" },
  },
  shortfall: {
    id: "shortfall",
    label: "Shortfall",
    formula: "MAX(0, planned_points − completed_points)",
    description:
      "Points committed but not delivered. These items are typically carried over to the next sprint, diluting its capacity and compounding the gap.",
    interpretation:
      "Even one point of shortfall means something was promised and not delivered. Acceptable occasionally; chronic shortfall above 10% of team capacity is an escalation trigger for the Delivery Manager.",
    unit: "story points",
    thresholds: { green: "0 pts", amber: "1–5 pts", red: ">5 pts" },
  },
  velocity: {
    id: "velocity",
    label: "Velocity",
    formula: "completed_points (normalised) / sprint_duration_weeks",
    description:
      "Story points completed per sprint, normalised for team size and sprint length. This is the team's sustained delivery rate, used for release forecasting.",
    interpretation:
      "Plot 3-sprint rolling average for a stable forecast. A decline in velocity alongside rising rework hours or defects means quality debt is consuming delivery capacity — act before it becomes chronic.",
    unit: "pts/sprint",
    drillFilter: "completed",
    thresholds: { green: "Within 10% of 3-sprint avg", amber: "10–25% below avg", red: ">25% below avg" },
  },
  team_size: {
    id: "team_size",
    label: "Team size",
    formula: "COUNT(DISTINCT assignee WHERE sprint = N)",
    description:
      "Number of distinct contributors active in this sprint. Fluctuates with contractor rotation, leave, and on-boarding.",
    interpretation:
      "Normalise velocity by team size to get per-person throughput. A team with high per-person velocity and high rework is over-loaded. A team with low velocity and low rework is under-loaded or blocked.",
    unit: "people",
  },
  rework_hours: {
    id: "rework_hours",
    label: "Rework hours",
    formula: "SUM(rework_hours) across all items in sprint",
    description:
      "Total hours spent correcting work already marked complete in a previous sprint or earlier in the same sprint. Defect fixes and requirement misunderstandings both count.",
    interpretation:
      "Target is <10% of total sprint capacity. Above 20% means quality issues are cannibalising delivery. Use the L5 drill to pinpoint which stories generate rework — common offenders: unclear acceptance criteria, missing test coverage, or rushed AI-generated code.",
    unit: "hours",
    drillFilter: "rework",
    thresholds: { green: "<10% of capacity", amber: "10–20%", red: ">20%" },
  },
  defects: {
    id: "defects",
    label: "Defects found / fixed",
    formula: "COUNT(defects_raised) / COUNT(defects_fixed) in sprint",
    description:
      "Defects raised measures new quality issues discovered. Defects fixed measures issues resolved. The ratio indicates whether the team is net-reducing or net-accumulating technical debt.",
    interpretation:
      "Fixed/Found ratio below 0.8 over two sprints means debt is growing faster than it is being paid off. Escalate to the Tech Lead to enforce a defect-zero sprint rule or a dedicated bug-bash before the next sprint.",
    unit: "count",
    drillFilter: "defects",
    thresholds: { green: "Fixed ≥ Found", amber: "Fixed 80–99% of Found", red: "Fixed <80% of Found" },
  },
  ai_assisted_points: {
    id: "ai_assisted_points",
    label: "AI-assisted points",
    formula: "SUM(story_points WHERE is_ai_assisted = true AND status IN ('completed','added'))",
    description:
      "Story points completed where the primary code or test was generated or substantially accelerated by an AI tool (Copilot, Claude, etc.). Declared by the assignee at check-in.",
    interpretation:
      "Track alongside quality_parity_ratio in Tab 7. If AI-assisted stories have higher rework_hours or defect rates than non-AI stories, the team's review process for AI output is insufficient. Target: AI points should improve velocity without degrading quality.",
    unit: "story points",
    drillFilter: "ai_assisted",
    thresholds: { green: "AI rework ≤ non-AI rework", amber: "AI rework 10–30% above", red: "AI rework >30% above" },
  },
};

// ─── Flow / Kanban ─────────────────────────────────────────────────────────

export const FLOW_METRICS: Record<string, MetricDef> = {
  throughput: {
    id: "throughput",
    label: "Throughput",
    formula: "COUNT(items WHERE status = 'completed' AND week = N)",
    description:
      "Items that crossed the 'Done' boundary in this calendar week. Each item counts once regardless of size — this is a count, not a point sum.",
    interpretation:
      "Plot throughput over 8+ weeks to get a stable distribution. Use the P50 of that distribution for forecasting: 'Given current throughput, how many more weeks to clear the backlog?' Sudden drops often point to unplanned absence or dependency drag; spikes to artificial scope reduction.",
    unit: "items/week",
    drillFilter: "completed",
    thresholds: { green: "Within 20% of 8-week avg", amber: "20–40% below avg", red: ">40% below avg" },
  },
  wip: {
    id: "wip",
    label: "WIP avg vs limit",
    formula: "AVG(daily_in_flight_count during week) / WIP_LIMIT_POLICY",
    description:
      "Work-in-progress ratio: average number of items simultaneously active during the week divided by the team's WIP limit. WIP limit is the policy constraint agreed in the team charter.",
    interpretation:
      "Little's Law: Throughput = WIP / Cycle Time. Exceeding the WIP limit inflates cycle time and creates context-switching overhead. A ratio >1.0 means the team is violating its own flow policy. Drill to In Progress items to find the bottleneck stage.",
    unit: "ratio",
    drillFilter: "in_progress",
    thresholds: { green: "≤0.8 of WIP limit", amber: "0.8–1.0", red: ">1.0 (limit exceeded)" },
  },
  cycle_p50: {
    id: "cycle_p50",
    label: "Cycle Time P50",
    formula: "PERCENTILE_50(cycle_days) WHERE status = 'completed' AND week ≤ N",
    description:
      "The median number of days from 'In Progress' to 'Done' for items completed in or before this week. 50% of items were delivered faster than this.",
    interpretation:
      "P50 is your baseline delivery speed. Compare to SLA commitments (e.g. 'features ≤ 5 days'). Drill to completed items to see which stories drove the median — typically the cleanest, smallest-scoped ones.",
    unit: "days",
    drillFilter: "completed",
    thresholds: { green: "≤5 days (standard)", amber: "5–10 days", red: ">10 days" },
  },
  cycle_p85: {
    id: "cycle_p85",
    label: "Cycle Time P85",
    formula: "PERCENTILE_85(cycle_days) WHERE status = 'completed' AND week ≤ N",
    description:
      "85th percentile cycle time — 85% of items were delivered equal to or faster than this. The P85 is the 'reliable SLA': if you promise 'done within X days' to your stakeholders, use P85, not P50.",
    interpretation:
      "If P85 is 2–3× your P50, you have high variability in delivery, often caused by a small number of large or blocked stories inflating the tail. Use as your 'safe commitment': commit P85 to the business, optimise P50 internally.",
    unit: "days",
    drillFilter: "completed",
    thresholds: { green: "≤1.5× P50", amber: "1.5–2.5× P50", red: ">2.5× P50 (high variability)" },
  },
  cycle_p95: {
    id: "cycle_p95",
    label: "Cycle Time P95",
    formula: "PERCENTILE_95(cycle_days) WHERE status = 'completed' AND week ≤ N",
    description:
      "95th percentile cycle time — the upper tail of your delivery distribution. Only 5% of items take longer. This is your 'worst case' signal.",
    interpretation:
      "If P95 is dramatically higher than P85, you have occasional outlier stories (likely large features, blocked items, or scope creep) that distort the distribution. These should be split during refinement. A CTO watching P95 wants it below 3× P50 as a team health benchmark.",
    unit: "days",
    drillFilter: "completed",
    thresholds: { green: "≤3× P50", amber: "3–5× P50", red: ">5× P50" },
  },
  lead_time: {
    id: "lead_time",
    label: "Lead Time",
    formula: "PERCENTILE_85(lead_days) = days from 'Backlog → Done'",
    description:
      "Time from when an item entered the backlog (created / committed) to when it was delivered to Done. Includes queue time before the team picks it up — unlike Cycle Time, which starts at 'In Progress'.",
    interpretation:
      "Lead Time is the customer's experience; Cycle Time is the team's experience. If Lead Time >> Cycle Time, items are sitting in the backlog for weeks before the team touches them — a prioritisation or capacity problem, not a delivery problem.",
    unit: "days",
    thresholds: { green: "≤2× Cycle P85", amber: "2–4× Cycle P85", red: ">4× Cycle P85" },
  },
  blocked: {
    id: "blocked",
    label: "Blocked items",
    formula: "COUNT(items WHERE status = 'blocked' OR flag_blocked = true)",
    description:
      "Items currently unable to progress due to an external dependency, missing information, awaiting review, or infrastructure issue. These consume WIP capacity without producing throughput.",
    interpretation:
      "Any blocked item older than 2 days is an escalation. Blocked items inflate cycle time for the whole team because they occupy WIP slots. Drill to In Progress items to see blocked stories — the title and assignee identify the owner and dependency.",
    unit: "items",
    drillFilter: "in_progress",
    thresholds: { green: "0 items", amber: "1–2 items", red: "≥3 items" },
  },
};

// ─── EVM ───────────────────────────────────────────────────────────────────

export const EVM_METRICS: Record<string, MetricDef> = {
  cpi: {
    id: "cpi",
    label: "CPI",
    formula: "Earned Value (EV) / Actual Cost (AC)",
    description:
      "Cost Performance Index measures how much value is being delivered per pound (or dollar) spent. EV = BAC × % complete; AC = actual spend to date.",
    interpretation:
      "CPI < 1.0 means you are overspending relative to the work delivered. A CPI of 0.92 means every £1 you planned to spend is costing you £1.09 in reality. Once CPI falls below 0.9, the EAC forecast becomes significantly worse — escalate to the Programme Sponsor.",
    unit: "ratio",
    thresholds: { green: "≥1.00", amber: "0.90–0.99", red: "<0.90" },
  },
  spi: {
    id: "spi",
    label: "SPI",
    formula: "Earned Value (EV) / Planned Value (PV)",
    description:
      "Schedule Performance Index measures how much of the planned work has actually been completed. PV = BAC × (time elapsed / total duration); EV = BAC × % complete.",
    interpretation:
      "SPI < 1.0 means the project is behind schedule. SPI of 0.88 means the team has completed only 88% of the work that was due by this point in time. SPI typically recovers in the second half of a project (as remaining work catches up); don't panic unless SPI < 0.85 beyond mid-project.",
    unit: "ratio",
    thresholds: { green: "≥1.00", amber: "0.90–0.99", red: "<0.90" },
  },
  eac: {
    id: "eac",
    label: "EAC",
    formula: "BAC / CPI  (or AC + (BAC − EV) / CPI for composite forecast)",
    description:
      "Estimate at Completion — the projected total cost of the project if current cost performance continues unchanged to the end. This is the primary financial risk indicator.",
    interpretation:
      "EAC − BAC = projected budget overrun. If EAC > BAC, you need to either find more budget, reduce scope, or improve CPI. The EAC formula assumes current CPI holds — a pessimistic but prudent assumption for board reporting.",
    unit: "currency",
    thresholds: { green: "EAC ≤ BAC", amber: "EAC 1–10% above BAC", red: "EAC >10% above BAC" },
  },
  tcpi: {
    id: "tcpi",
    label: "TCPI",
    formula: "(BAC − EV) / (BAC − AC)",
    description:
      "To-Complete Performance Index — the cost efficiency the project must achieve on all remaining work in order to finish within the original budget (BAC). Values above 1.0 mean 'must work more efficiently than we have been'.",
    interpretation:
      "TCPI > 1.15 is effectively unachievable — the project cannot recover to BAC without a scope reduction or budget increase. Use TCPI to set a realistic 'recovery target' in programme reviews. If TCPI > 1.05, escalate to stakeholders with a revised EAC scenario.",
    unit: "ratio",
    thresholds: { green: "≤1.05 (achievable)", amber: "1.05–1.15 (challenging)", red: ">1.15 (not achievable without scope change)" },
  },
  percent_complete: {
    id: "percent_complete",
    label: "% Complete",
    formula: "EV / BAC × 100",
    description:
      "Earned Value as a proportion of Budget at Completion — the percentage of the total scope that has been completed and accepted, weighted by cost plan.",
    interpretation:
      "This is cost-weighted completion, not task-count completion. A project reporting 60% complete should also show EV = 0.60 × BAC. Discrepancies (high task count, low % complete) indicate that costly deliverables are being deferred to the end — a delivery risk.",
    unit: "%",
  },
};

// ─── AI / Velocity ─────────────────────────────────────────────────────────

export const AI_VELOCITY_METRICS: Record<string, MetricDef> = {
  standard_velocity: {
    id: "standard_velocity",
    label: "Standard velocity",
    formula: "SUM(story_points WHERE NOT is_ai_assisted AND status = 'completed')",
    description:
      "Points delivered by the team using conventional (non-AI-assisted) development. This is the baseline human throughput of the team.",
    interpretation:
      "Stable standard velocity is a healthy team signal. If standard velocity is falling as AI-assisted velocity rises, the team may be over-relying on AI for tasks outside its competency zone — monitor quality parity ratio.",
    unit: "pts",
    thresholds: { green: "Stable or rising", amber: "5–15% declining vs 3-sprint avg", red: ">15% declining" },
  },
  ai_raw_velocity: {
    id: "ai_raw_velocity",
    label: "AI raw velocity",
    formula: "SUM(story_points WHERE is_ai_assisted = true AND status = 'completed')",
    description:
      "Total points on AI-assisted stories, measured at face value (story point estimate), regardless of quality outcome.",
    interpretation:
      "Raw AI velocity can be inflated by poor estimates or by accepting AI-generated code with minimal review. Always compare against AI quality-adjusted velocity and rework hours to check if the speed gain is genuine.",
    unit: "pts",
  },
  ai_adjusted_velocity: {
    id: "ai_adjusted_velocity",
    label: "AI quality-adjusted",
    formula: "ai_raw_velocity × quality_parity_ratio",
    description:
      "AI velocity adjusted for quality parity — discounts AI-assisted points by the ratio of AI rework to non-AI rework, so inflated velocity due to poor quality is penalised.",
    interpretation:
      "The trust-adjusted view of AI contribution. If AI-adjusted velocity ≈ AI raw velocity, quality parity is good. If adjusted is materially lower, the AI-generated code is producing more rework and the acceleration is illusory.",
    unit: "pts",
    thresholds: { green: "≥90% of raw AI velocity", amber: "75–89% of raw", red: "<75% (quality penalty dominant)" },
  },
  quality_parity: {
    id: "quality_parity",
    label: "Quality parity",
    formula: "1 − (AI_rework_rate / non_AI_rework_rate)",
    description:
      "Ratio comparing defect/rework rates of AI-assisted stories to non-AI stories. A ratio of 1.0 means AI output has the same quality as human output. Below 1.0 means AI introduces more rework.",
    interpretation:
      "Target is ≥0.90. Below 0.80 means AI assistance is generating significant extra rework. Common causes: insufficient code review for AI output, prompts not including acceptance criteria, AI used on unfamiliar codebases. Review the merge policy in the AI Governance tab.",
    unit: "ratio",
    thresholds: { green: "≥0.90", amber: "0.75–0.89", red: "<0.75" },
  },
  ai_rework_points: {
    id: "ai_rework_points",
    label: "AI rework points",
    formula: "SUM(story_points WHERE is_ai_assisted = true AND rework_hours > 0)",
    description:
      "Story points on AI-assisted stories that generated rework in the same or following sprint. Indicates AI output that was accepted but later found to need correction.",
    interpretation:
      "AI rework points should stay below 10% of total AI velocity. High AI rework means either the review process for AI suggestions is too permissive, or the AI is being applied to areas where it lacks sufficient context. Compare to non-AI rework rate to isolate the AI-specific penalty.",
    unit: "story points",
    thresholds: { green: "<10% of AI velocity", amber: "10–20% of AI velocity", red: ">20% of AI velocity" },
  },
  combined_velocity: {
    id: "combined_velocity",
    label: "Combined velocity",
    formula: "standard_velocity + ai_quality_adjusted_velocity",
    description:
      "Total velocity for the sprint including both standard (non-AI) and quality-adjusted AI-assisted points. This is the number that feeds into release forecasting.",
    interpretation:
      "Use combined velocity for sprint forecasting, but always show it next to its breakdown (standard + AI adjusted). If combined velocity is growing but the AI-adjusted component is shrinking as a fraction, the AI contribution is decelerating — investigate whether AI tooling or adoption is regressing.",
    unit: "story points",
    thresholds: { green: "Growing vs 3-sprint avg", amber: "Flat", red: "Declining" },
  },
  merge_eligible: {
    id: "merge_eligible",
    label: "Merge eligible",
    formula: "COUNT(sprints WHERE quality_parity ≥ 0.90 AND ai_adoption_rate ≥ target)",
    description:
      "Number of sprint/project combinations where AI adoption meets the programme's blend rules and quality parity is at threshold — making them eligible for the AI-blended velocity merge into portfolio reporting.",
    interpretation:
      "A sprint becomes merge-eligible when it demonstrates that AI acceleration is real, not a quality mirage. The blended portfolio velocity (used in executive reporting) only includes merge-eligible sprints, preventing inflated numbers from reaching the board pack.",
    unit: "count",
    thresholds: { green: "All AI projects eligible", amber: "50–99% eligible", red: "<50% eligible" },
  },
};

// ─── Margin / Financial ─────────────────────────────────────────────────────

export const MARGIN_METRICS: Record<string, MetricDef> = {
  gross_margin: {
    id: "gross_margin",
    label: "Gross margin",
    formula: "(Revenue − Direct Costs) / Revenue × 100",
    description:
      "Revenue less direct project costs (labour, tools, subcontractors), expressed as a percentage of revenue. Does not include overheads or G&A.",
    interpretation:
      "Primary commercial health indicator. Below 20% on a professional services programme means insufficient margin to absorb overruns. Watch for month-over-month decline as a leading indicator of cost escalation before it reaches project accounts.",
    unit: "%",
    thresholds: { green: "≥22%", amber: "15–21%", red: "<15%" },
  },
  net_margin: {
    id: "net_margin",
    label: "Net margin",
    formula: "(Revenue − Total Costs including overheads) / Revenue × 100",
    description:
      "Revenue less all costs including allocated overheads and G&A. The 'true' profitability of the programme after full cost attribution.",
    interpretation:
      "Net margin below 10% means the programme is marginally profitable at best. A programme in the red corridor should trigger a revenue uplift negotiation, scope reduction, or resource efficiency review.",
    unit: "%",
    thresholds: { green: "≥18%", amber: "10–17%", red: "<10%" },
  },
  revenue: {
    id: "revenue",
    label: "Revenue",
    formula: "SUM(invoiced_value WHERE invoice_date BETWEEN period_start AND period_end)",
    description:
      "Recognised revenue in the reporting period — typically monthly, aligned to invoice milestones or time-and-materials actuals. In fixed-price contracts, recognition follows the delivery completion curve.",
    interpretation:
      "Compare against the revenue plan baseline to spot slippage. Late milestones in delivery directly delay revenue recognition and create cash-flow pressure on the account team.",
    unit: "currency",
  },
};

// ─── Customer Intelligence ─────────────────────────────────────────────────

export const CUSTOMER_METRICS: Record<string, MetricDef> = {
  open_escalations: {
    id: "open_escalations",
    label: "Open escalations",
    formula: "COUNT(escalation_events WHERE status = 'open' AND period = N)",
    description:
      "Number of client escalations currently open and unresolved — issues that bypassed normal delivery channels and were raised directly with senior management.",
    interpretation:
      "Even one open escalation is a relationship signal. Zero is the target at all times. Open escalations older than 2 weeks without a closure plan are a retention risk. Drill to the escalation log to see owner, severity, and resolution date.",
    unit: "count",
    thresholds: { green: "0 open", amber: "1 open", red: "≥2 open or >2 weeks unresolved" },
  },
  csat: {
    id: "csat",
    label: "CSAT score",
    formula: "AVG(survey_score) WHERE survey_type = 'CSAT' AND period = N",
    description:
      "Customer Satisfaction score from periodic pulse surveys (typically monthly). Scored 1–10 by the sponsor, key users, and steering group.",
    interpretation:
      "CSAT <7.0 is a commercial risk — contract renewal probability drops sharply below this threshold. Drill to the survey comments for root causes. CSAT is a lagging indicator; use escalation count as the leading indicator.",
    unit: "score /10",
    thresholds: { green: "≥8.0", amber: "6.5–7.9", red: "<6.5" },
  },
  nps: {
    id: "nps",
    label: "NPS",
    formula: "% Promoters (9–10) − % Detractors (0–6)",
    description:
      "Net Promoter Score derived from the question 'How likely are you to recommend this programme/team?' Ranges from −100 to +100.",
    interpretation:
      "NPS above 0 means more promoters than detractors. In enterprise IT delivery, NPS above 30 is excellent. NPS below −10 is a retention/renewal risk and should trigger a client satisfaction review.",
    unit: "score",
    thresholds: { green: "≥30", amber: "0–29", red: "<0" },
  },
  renewal_probability: {
    id: "renewal_probability",
    label: "Renewal probability",
    formula: "Logistic model: P(renewal) = f(CSAT, NPS, delivery_rag, escalation_count)",
    description:
      "Predicted probability of contract renewal at end of current term, derived from a weighted model using satisfaction scores, delivery health, and engagement signals.",
    interpretation:
      "Use this to prioritise account management effort. Programmes with renewal_probability <60% need a quarterly business review with the client executive within 30 days. Feed this into revenue forecasting for the next financial year.",
    unit: "%",
    thresholds: { green: "≥80%", amber: "60–79%", red: "<60%" },
  },
  escalation_count: {
    id: "escalation_count",
    label: "Escalations",
    formula: "COUNT(escalation_events WHERE period = N AND severity IN ('high','critical'))",
    description:
      "Number of formal client escalations in the reporting period. An escalation is any issue raised by the client directly with senior management, bypassing normal delivery channels.",
    interpretation:
      "Even one high-severity escalation in a month is a warning signal. Two or more signals a relationship in crisis. Escalations correlate strongly with CSAT decline 1–2 months later — use as a leading indicator of satisfaction deterioration.",
    unit: "count",
    thresholds: { green: "0", amber: "1", red: "≥2" },
  },
};

// ─── Risk ─────────────────────────────────────────────────────────────────

export const RISK_METRICS: Record<string, MetricDef> = {
  risk_exposure: {
    id: "risk_exposure",
    label: "Risk exposure",
    formula: "SUM(probability × impact × residual_factor) across open risks",
    description:
      "Weighted risk exposure = sum of (likelihood × consequence × mitigation_effectiveness) for all open risks. Expressed in currency or weighted score.",
    interpretation:
      "Use as the headline portfolio risk number in the board pack. Month-over-month growth in exposure means new risks are being added faster than old ones are being mitigated. Target is declining exposure trend by mid-project.",
    unit: "weighted score",
    thresholds: { green: "Declining or stable", amber: "Growing <10% m/m", red: "Growing >10% m/m" },
  },
  open_risks: {
    id: "open_risks",
    label: "Open risks",
    formula: "COUNT(risks WHERE status = 'open' AND review_date <= TODAY + 14d)",
    description:
      "Count of risks with open status that are due for review within the next 14 days. Overdue reviews mean the risk register is not being actively maintained.",
    interpretation:
      "Every open risk should have an owner, a mitigation action, and a review date. If any risk is overdue for review by more than one sprint, escalate to the Programme Manager to enforce the RAID governance process.",
    unit: "count",
    thresholds: { green: "All reviewed on time", amber: "1–3 overdue", red: ">3 overdue" },
  },
};

// ─── AI Governance ─────────────────────────────────────────────────────────

export const AI_GOVERNANCE_METRICS: Record<string, MetricDef> = {
  trust_score: {
    id: "trust_score",
    label: "AI trust score",
    formula: "WEIGHTED_AVG(quality_parity × 0.4, acceptance_rate × 0.3, security_pass_rate × 0.3)",
    description:
      "Composite score summarising the trustworthiness of AI output across three dimensions: quality parity with human code, acceptance rate (ratio of AI suggestions accepted to generated), and security scan pass rate.",
    interpretation:
      "Used as the gate for increasing AI adoption limits in the blend policy. Trust score ≥0.80 enables higher WIP for AI-assisted stories. Trust score <0.65 should trigger a freeze on new AI tooling introduction until root cause is identified.",
    unit: "score 0–1",
    thresholds: { green: "≥0.80", amber: "0.65–0.79", red: "<0.65" },
  },
  acceptance_rate: {
    id: "acceptance_rate",
    label: "AI acceptance rate",
    formula: "COUNT(ai_suggestions_accepted) / COUNT(ai_suggestions_generated)",
    description:
      "Fraction of AI-generated suggestions that were accepted and incorporated by engineers, measured at the IDE or code-review level. Low acceptance means engineers are rejecting AI output.",
    interpretation:
      "Target: 35–60% for a well-tuned AI workflow. Below 30% means the AI is not aligned to team conventions (fix with project-specific prompt templates). Above 70% suggests insufficient review — engineers are accepting too quickly without critical assessment.",
    unit: "%",
    thresholds: { green: "35–60%", amber: "20–34% or 61–75%", red: "<20% or >75%" },
  },
  time_saved: {
    id: "time_saved",
    label: "Time saved",
    formula: "SUM(estimated_manual_hours − actual_hours) WHERE is_ai_assisted = true",
    description:
      "Estimated hours saved by AI assistance, calculated as the difference between estimated manual effort and actual time logged on AI-assisted stories.",
    interpretation:
      "Divide by total sprint capacity to get AI efficiency lift percentage. Report this to the CTO as the ROI signal for AI tooling cost. But always cross-check against rework_hours — net time saved must account for rework generated by low-quality AI output.",
    unit: "hours",
    thresholds: { green: "Net positive (saved > rework)", amber: "Break-even ±5%", red: "Net negative (rework > saved)" },
  },
  ai_spend: {
    id: "ai_spend",
    label: "AI tooling spend",
    formula: "SUM(ai_tool_cost) WHERE period = N",
    description:
      "Monthly cost of AI tooling licences, API consumption, and infrastructure allocated to AI features. Tracked per programme to attribute cost accurately.",
    interpretation:
      "Compare against time_saved × blended_day_rate to compute ROI. AI spend is justified when time saved (at cost) exceeds the tooling cost. Flag to Finance if AI spend > 5% of programme monthly cost without a corresponding velocity uplift.",
    unit: "currency",
    thresholds: { green: "ROI ≥ 3×", amber: "ROI 1–2.9×", red: "ROI <1× (breaking even or negative)" },
  },
};

// ─── Smart Ops ─────────────────────────────────────────────────────────────

export const SMARTOPS_METRICS: Record<string, MetricDef> = {
  mitigating_scenarios: {
    id: "mitigating_scenarios",
    label: "Mitigating",
    formula: "COUNT(scenarios WHERE status = 'Mitigating')",
    description:
      "Number of active scenario alerts currently in a mitigation state — an owner has acknowledged the risk and a corrective action is in progress.",
    interpretation:
      "Mitigating scenarios are positive: they show the team is actively managing risk rather than ignoring it. Watch whether they resolve within the agreed SLA (typically 2 sprints). If mitigating count grows without resolution, escalate the action owners.",
    unit: "count",
    thresholds: { green: "Resolving within SLA", amber: "SLA at risk (>2 sprints)", red: "Stale — no progress" },
  },
  scenario_alerts: {
    id: "scenario_alerts",
    label: "Scenario alerts",
    formula: "COUNT(scenario_simulations WHERE outcome = 'breach' AND threshold_crossed = true)",
    description:
      "Number of active scenario simulations that have crossed a threshold — e.g. 'if CPI falls another 0.05, EAC will breach BAC+10%'. These are forward-looking risk triggers, not current breaches.",
    interpretation:
      "Scenario alerts give you 2–4 week lead time on delivery or financial threshold breaches. One active alert is informational; two or more active alerts on the same programme should trigger a Steering Committee review.",
    unit: "count",
    thresholds: { green: "0 alerts", amber: "1 alert", red: "≥2 alerts on same programme" },
  },
  bench_cost: {
    id: "bench_cost",
    label: "Bench cost",
    formula: "SUM(daily_rate × bench_days) WHERE status = 'benched' AND period = N",
    description:
      "Total cost of resources on the bench — allocated but not billable in the current period. Includes contractor day rates and opportunity cost of permanent staff not deployed to chargeable work.",
    interpretation:
      "Bench cost above 5% of total programme cost signals a resource allocation problem. Common causes: delayed onboarding, awaiting environment access, dependencies not cleared, or poor sprint planning. Escalate to Resource Manager for reallocation within 2 weeks.",
    unit: "currency",
    thresholds: { green: "<2% of programme cost", amber: "2–5%", red: ">5%" },
  },
};

// ─── Portfolio / Executive ──────────────────────────────────────────────────

export const PORTFOLIO_METRICS: Record<string, MetricDef> = {
  portfolio_revenue: {
    id: "portfolio_revenue",
    label: "Revenue realised",
    formula: "SUM(revenue_recognised) across all active programmes, converted to display currency",
    description:
      "Total revenue recognised across all programmes in the portfolio year-to-date, converted to the selected display currency using live FX rates.",
    interpretation:
      "Compare against the annual contract value plan. Revenue shortfall at portfolio level usually means milestone slippage on multiple programmes simultaneously — a structural delivery problem. Track programme-by-programme in the drill panel.",
    unit: "currency",
    thresholds: { green: "≥100% of plan YTD", amber: "90–99% of plan", red: "<90% of plan" },
  },
  blended_margin: {
    id: "blended_margin",
    label: "Blended margin",
    formula: "WEIGHTED_AVG(gross_margin, weight = revenue) across all programmes",
    description:
      "Revenue-weighted average gross margin across the portfolio. Individual programmes with higher revenue have more influence on this number.",
    interpretation:
      "Portfolio blended margin below 20% means the book of business is structurally under-margined. Identify programmes pulling the average down (use the drill) and assess whether price increases, scope adjustments, or resource swaps are feasible.",
    unit: "%",
    thresholds: { green: "≥22%", amber: "15–21%", red: "<15%" },
  },
  avg_cpi: {
    id: "avg_cpi",
    label: "Avg CPI",
    formula: "MEAN(latest_cpi) across all active programmes with EVM data",
    description:
      "Simple average of the most recent CPI snapshot for each programme in the portfolio. Gives a headline cost performance signal without revenue weighting.",
    interpretation:
      "Avg CPI below 0.95 means the portfolio is collectively overspending. Drill into the per-programme CPI breakdown to find the biggest drag — typically one or two programmes with structural cost problems pulling the average below 1.0.",
    unit: "ratio",
    thresholds: { green: "≥1.00", amber: "0.90–0.99", red: "<0.90" },
  },
};

// ─── Waterfall / Phase ─────────────────────────────────────────────────────

export const WATERFALL_METRICS: Record<string, MetricDef> = {
  phase_completion: {
    id: "phase_completion",
    label: "Phase complete",
    formula: "EV / BAC × 100 within this phase (or deliverable count ratio)",
    description:
      "Percentage of the current phase's scope that has been delivered and accepted through the phase gate. Measured as earned value within phase budget, or as completed deliverable count / total planned deliverables.",
    interpretation:
      "In waterfall delivery, phase completion below 80% at the planned gate date is a red flag. The phase gate cannot be signed off until completion reaches 100% — so any shortfall directly delays the downstream phases. Escalate to the Programme Director if completion falls more than 10% behind at the 60% time mark of the phase.",
    unit: "%",
    thresholds: { green: "On track (completion ≥ time elapsed %)", amber: "5–10% behind time-curve", red: ">10% behind or gate risk" },
  },
  schedule_variance_days: {
    id: "schedule_variance_days",
    label: "Schedule variance",
    formula: "actual_duration_days − planned_duration_days",
    description:
      "Difference in calendar days between the actual time spent on a phase and the planned duration. Positive = running late (slip); negative = ahead of schedule.",
    interpretation:
      "Each day of phase slip adds directly to the project end date unless recovery is built into subsequent phases. A slip of more than 10% of phase duration without a recovery plan should be escalated and reflected in the EAC forecast immediately.",
    unit: "days",
    thresholds: { green: "0 to −∞ (on time or ahead)", amber: "+1 to +7 days slip", red: ">7 days slip or gate missed" },
  },
  milestone_slip: {
    id: "milestone_slip",
    label: "Milestone slip",
    formula: "actual_date − planned_date  (days, positive = late)",
    description:
      "Days by which a milestone delivery was delayed from the planned date. Milestones represent key contractual or programme commitments — slip has direct commercial consequences.",
    interpretation:
      "Any milestone slip triggers a change notification to the client under most fixed-price contracts. Slip of more than 5 days requires the Programme Manager to issue a revised delivery baseline. Slip above 14 days usually triggers a commercial impact assessment.",
    unit: "days",
    thresholds: { green: "0 (on time)", amber: "1–5 days", red: ">5 days or contractual breach risk" },
  },
};

// ─── Master lookup ──────────────────────────────────────────────────────────

export const ALL_METRICS: Record<string, MetricDef> = {
  ...SPRINT_METRICS,
  ...FLOW_METRICS,
  ...EVM_METRICS,
  ...AI_VELOCITY_METRICS,
  ...MARGIN_METRICS,
  ...CUSTOMER_METRICS,
  ...RISK_METRICS,
  ...AI_GOVERNANCE_METRICS,
  ...SMARTOPS_METRICS,
  ...PORTFOLIO_METRICS,
  ...WATERFALL_METRICS,
};

export function getMetric(id: string): MetricDef | undefined {
  return ALL_METRICS[id];
}
