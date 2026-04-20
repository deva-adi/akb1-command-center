import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL?.trim() || "";

export const api = axios.create({
  baseURL,
  timeout: 15_000,
  headers: {
    "Content-Type": "application/json",
  },
});

export type HealthResponse = {
  status: string;
  version: string;
  tables: number;
};

export type Programme = {
  id: number;
  name: string;
  code: string;
  client: string | null;
  start_date: string;
  end_date: string | null;
  status: string;
  bac: number | null;
  revenue: number | null;
  team_size: number | null;
  offshore_ratio: number | null;
  delivery_model: string | null;
  currency_code: string;
};

export type KpiDefinition = {
  id: number;
  name: string;
  code: string;
  formula: string;
  description: string | null;
  unit: string | null;
  green_threshold: number | null;
  amber_threshold: number | null;
  red_threshold: number | null;
  weight: number;
  category: string | null;
  is_higher_better: boolean;
};

export type KpiSnapshot = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  kpi_id: number | null;
  snapshot_date: string;
  value: number;
  trend: string | null;
  notes: string | null;
};

export type AppSetting = {
  key: string;
  value: string | null;
};

export type Risk = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  title: string;
  description: string | null;
  category: string | null;
  probability: number | null;
  impact: number | null;
  severity: string | null;
  status: string;
  owner: string | null;
  mitigation_plan: string | null;
  escalated_to_programme: boolean;
};

export type DataImportLog = {
  id: number;
  file_name: string | null;
  source: string | null;
  rows_imported: number | null;
  status: string | null;
  notes: string | null;
};

export async function fetchHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>("/health");
  return data;
}

export async function fetchProgrammes(): Promise<Programme[]> {
  const { data } = await api.get<Programme[]>("/api/v1/programmes");
  return data;
}

export async function fetchKpiDefinitions(category?: string): Promise<KpiDefinition[]> {
  const { data } = await api.get<KpiDefinition[]>("/api/v1/kpi/definitions", {
    params: category ? { category } : undefined,
  });
  return data;
}

export async function updateKpiWeight(
  kpiId: number,
  weight: number,
): Promise<KpiDefinition> {
  const { data } = await api.put<KpiDefinition>(
    `/api/v1/kpi/definitions/${kpiId}/weight`,
    { weight },
  );
  return data;
}

export async function fetchKpiSnapshots(params: {
  kpiCode?: string;
  programId?: number;
}): Promise<KpiSnapshot[]> {
  const { data } = await api.get<KpiSnapshot[]>("/api/v1/kpi/snapshots", {
    params: {
      kpi_code: params.kpiCode,
      program_id: params.programId,
    },
  });
  return data;
}

export async function fetchTopRisks(limit = 5): Promise<Risk[]> {
  const { data } = await api.get<Risk[]>("/api/v1/risks", {
    params: { sort_by: "impact", limit },
  });
  return data;
}

export async function fetchSettings(): Promise<AppSetting[]> {
  const { data } = await api.get<AppSetting[]>("/api/v1/settings");
  return data;
}

export async function fetchImportLog(): Promise<DataImportLog[]> {
  const { data } = await api.get<DataImportLog[]>("/api/v1/import/log");
  return data;
}

export type CurrencyRate = {
  code: string;
  symbol: string | null;
  rate_to_base: string;
  source: string;
  last_updated: string;
};

export async function fetchCurrencyRates(): Promise<CurrencyRate[]> {
  const { data } = await api.get<CurrencyRate[]>("/api/v1/currency/rates");
  return data;
}

// ---------- Delivery Health ----------

export type Sprint = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  sprint_number: number | null;
  start_date: string | null;
  end_date: string | null;
  planned_points: number | null;
  completed_points: number | null;
  velocity: number | null;
  defects_found: number | null;
  defects_fixed: number | null;
  rework_hours: number | null;
  team_size: number | null;
  ai_assisted_points: number;
  iteration_type: string;
  estimation_unit: string;
};

export type EvmSnapshot = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  snapshot_date: string;
  planned_value: number;
  earned_value: number;
  actual_cost: number;
  percent_complete: number | null;
  bac: number | null;
  cpi: number | null;
  spi: number | null;
  eac: number | null;
  tcpi: number | null;
  vac: number | null;
  notes: string | null;
};

export type FlowMetric = {
  id: number;
  project_id: number | null;
  period_start: string | null;
  period_end: string | null;
  throughput_items: number | null;
  wip_avg: number | null;
  wip_limit: number | null;
  cycle_time_p50: number | null;
  cycle_time_p85: number | null;
  cycle_time_p95: number | null;
  lead_time_avg: number | null;
  blocked_time_hours: number | null;
};

export type ProjectPhase = {
  id: number;
  project_id: number | null;
  phase_name: string;
  phase_sequence: number | null;
  planned_start: string | null;
  planned_end: string | null;
  actual_start: string | null;
  actual_end: string | null;
  percent_complete: number | null;
  gate_status: string | null;
  gate_approver: string | null;
  gate_date: string | null;
  notes: string | null;
};

export type Milestone = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  name: string;
  planned_date: string;
  actual_date: string | null;
  status: string;
  owner: string | null;
  notes: string | null;
};

export type ProjectListItem = {
  id: number;
  program_id: number | null;
  name: string;
  code: string;
  delivery_methodology: string;
  is_ai_augmented: boolean;
  ai_augmentation_level: string | null;
  start_date: string | null;
  end_date: string | null;
  status: string;
};

export async function fetchProjectsForProgramme(
  programId: number,
): Promise<ProjectListItem[]> {
  const { data } = await api.get<ProjectListItem[]>(
    `/api/v1/programmes/${programId}/projects`,
  );
  return data;
}

export async function fetchSprints(projectId: number): Promise<Sprint[]> {
  const { data } = await api.get<Sprint[]>("/api/v1/sprints", {
    params: { project_id: projectId },
  });
  return data;
}

export async function fetchEvm(projectId: number): Promise<EvmSnapshot[]> {
  const { data } = await api.get<EvmSnapshot[]>("/api/v1/evm", {
    params: { project_id: projectId },
  });
  return data;
}

export async function fetchFlow(projectId: number): Promise<FlowMetric[]> {
  const { data } = await api.get<FlowMetric[]>("/api/v1/flow", {
    params: { project_id: projectId },
  });
  return data;
}

export async function fetchPhases(projectId: number): Promise<ProjectPhase[]> {
  const { data } = await api.get<ProjectPhase[]>("/api/v1/phases", {
    params: { project_id: projectId },
  });
  return data;
}

export async function fetchMilestones(projectId: number): Promise<Milestone[]> {
  const { data } = await api.get<Milestone[]>("/api/v1/milestones", {
    params: { project_id: projectId },
  });
  return data;
}

// ---------- Velocity & Flow / Margin & EVM ----------

export type DualVelocity = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  sprint_number: number | null;
  standard_velocity: number | null;
  ai_raw_velocity: number | null;
  ai_rework_points: number | null;
  ai_quality_adjusted_velocity: number | null;
  combined_velocity: number | null;
  merge_eligible: boolean;
  quality_parity_ratio: number | null;
  snapshot_date: string | null;
};

export type BlendRule = {
  id: number;
  program_id: number | null;
  gate_name: string;
  gate_condition: string | null;
  current_value: number | null;
  threshold: number | null;
  passed: boolean;
  last_evaluated: string | null;
};

export type CommercialScenario = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  scenario_name: string | null;
  planned_revenue: number | null;
  actual_revenue: number | null;
  planned_cost: number | null;
  actual_cost: number | null;
  gross_margin_pct: number | null;
  contribution_margin_pct: number | null;
  portfolio_margin_pct: number | null;
  net_margin_pct: number | null;
  snapshot_date: string | null;
  notes: string | null;
};

export type LossExposure = {
  id: number;
  program_id: number | null;
  snapshot_date: string | null;
  loss_category: string;
  amount: number | null;
  percentage_of_revenue: number | null;
  detection_method: string | null;
  mitigation_status: string | null;
  notes: string | null;
};

export type RateCardRow = {
  id: number;
  program_id: number | null;
  role_tier: string;
  planned_rate: number;
  actual_rate: number | null;
  planned_headcount: number | null;
  actual_headcount: number | null;
  snapshot_date: string | null;
  notes: string | null;
};

export type ChangeRequest = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  cr_date: string | null;
  cr_description: string | null;
  effort_hours: number | null;
  cr_value: number | null;
  processing_cost: number | null;
  status: string | null;
  margin_impact: number | null;
  is_billable: boolean | null;
};

export async function fetchDualVelocity(programId?: number): Promise<DualVelocity[]> {
  const { data } = await api.get<DualVelocity[]>("/api/v1/dual-velocity", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchBlendRules(programId?: number): Promise<BlendRule[]> {
  const { data } = await api.get<BlendRule[]>("/api/v1/blend-rules", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchCommercial(programId?: number): Promise<CommercialScenario[]> {
  const { data } = await api.get<CommercialScenario[]>("/api/v1/commercial", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchLosses(programId?: number): Promise<LossExposure[]> {
  const { data } = await api.get<LossExposure[]>("/api/v1/losses", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchRateCards(programId?: number): Promise<RateCardRow[]> {
  const { data } = await api.get<RateCardRow[]>("/api/v1/rate-cards", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchChangeRequests(programId?: number): Promise<ChangeRequest[]> {
  const { data } = await api.get<ChangeRequest[]>("/api/v1/change-requests", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

// ---------- Customer Intelligence ----------

export type CustomerSatisfaction = {
  id: number;
  program_id: number | null;
  snapshot_date: string;
  csat_score: number | null;
  nps_score: number | null;
  escalation_count: number;
  escalation_open: number;
  steering_meetings_planned: number | null;
  steering_meetings_held: number | null;
  action_items_open: number | null;
  action_items_closed: number | null;
  positive_themes: string | null;
  concern_themes: string | null;
  renewal_score: number | null;
};

export type SlaIncident = {
  id: number;
  program_id: number | null;
  incident_id: string | null;
  priority: string;
  summary: string | null;
  reported_at: string;
  responded_at: string | null;
  resolved_at: string | null;
  response_time_minutes: number | null;
  resolution_time_minutes: number | null;
  sla_breached: boolean;
  penalty_amount: number;
  root_cause: string | null;
};

export type CustomerExpectation = {
  id: number;
  program_id: number | null;
  snapshot_date: string;
  dimension: string;
  expected_score: number | null;
  delivered_score: number | null;
  gap: number | null;
  weight: number;
  evidence_source: string | null;
  owner: string | null;
  notes: string | null;
};

export type CustomerAction = {
  id: number;
  program_id: number | null;
  meeting_date: string | null;
  description: string;
  owner: string | null;
  due_date: string | null;
  status: string;
  priority: string | null;
  escalated: boolean;
  resolution_notes: string | null;
  closed_date: string | null;
};

export async function fetchCustomerSatisfaction(
  programId?: number,
): Promise<CustomerSatisfaction[]> {
  const { data } = await api.get<CustomerSatisfaction[]>(
    "/api/v1/customer/satisfaction",
    { params: programId ? { program_id: programId } : undefined },
  );
  return data;
}

export async function fetchSlaIncidents(
  programId?: number,
  breachedOnly = false,
): Promise<SlaIncident[]> {
  const { data } = await api.get<SlaIncident[]>(
    "/api/v1/customer/sla-incidents",
    {
      params: {
        program_id: programId,
        breached_only: breachedOnly || undefined,
      },
    },
  );
  return data;
}

export async function fetchCustomerExpectations(
  programId: number,
): Promise<CustomerExpectation[]> {
  const { data } = await api.get<CustomerExpectation[]>(
    `/api/v1/customer/${programId}/expectations`,
  );
  return data;
}

export async function fetchCustomerActions(
  programId: number,
): Promise<CustomerAction[]> {
  const { data } = await api.get<CustomerAction[]>(
    `/api/v1/customer/${programId}/actions`,
  );
  return data;
}

// ---------- AI Governance ----------

export type AiTool = {
  id: number;
  name: string;
  vendor: string | null;
  version: string | null;
  category: string | null;
  license_type: string | null;
  cost_per_seat: number | null;
  status: string;
};

export type AiUsage = {
  id: number;
  ai_tool_id: number | null;
  program_id: number | null;
  snapshot_date: string | null;
  prompts_count: number | null;
  suggestions_accepted: number | null;
  suggestions_rejected: number | null;
  time_saved_hours: number | null;
  cost: number | null;
};

export type AiCodeMetric = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  sprint_number: number | null;
  ai_lines_generated: number | null;
  ai_lines_accepted: number | null;
  ai_defect_count: number | null;
  ai_test_coverage_pct: number | null;
  ai_review_rejection_pct: number | null;
  human_defect_count: number | null;
  human_test_coverage_pct: number | null;
  human_review_rejection_pct: number | null;
  snapshot_date: string | null;
};

export type AiSdlcMetric = {
  id: number;
  program_id: number | null;
  sprint_number: number | null;
  estimation_accuracy_with_ai: number | null;
  estimation_accuracy_without_ai: number | null;
  code_review_hours_with_ai: number | null;
  code_review_hours_without_ai: number | null;
  planning_velocity_with_ai: number | null;
  planning_velocity_without_ai: number | null;
  documentation_hours_with_ai: number | null;
  documentation_hours_without_ai: number | null;
  snapshot_date: string | null;
};

export type AiTrustScore = {
  id: number;
  ai_tool_id: number | null;
  program_id: number | null;
  snapshot_date: string | null;
  provenance_score: number | null;
  review_status_score: number | null;
  test_coverage_score: number | null;
  drift_check_score: number | null;
  override_rate_score: number | null;
  defect_rate_score: number | null;
  composite_score: number | null;
  maturity_level: string | null;
};

export type AiGovernanceConfig = {
  id: number;
  config_type: string;
  name: string;
  description: string | null;
  scope: string | null;
  enforcement_method: string | null;
  program_id: number | null;
  status: string;
  compliance_pct: number | null;
  last_audit_date: string | null;
  review_date: string | null;
  owner: string | null;
};

export type AiOverride = {
  id: number;
  ai_tool_id: number | null;
  program_id: number | null;
  project_id: number | null;
  override_date: string | null;
  override_type: string | null;
  reason: string | null;
  outcome: string | null;
  approver: string | null;
};

export async function fetchAiTools(): Promise<AiTool[]> {
  const { data } = await api.get<AiTool[]>("/api/v1/ai/tools");
  return data;
}

export async function fetchAiUsage(programId?: number): Promise<AiUsage[]> {
  const { data } = await api.get<AiUsage[]>("/api/v1/ai/usage", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchAiCodeMetrics(programId?: number): Promise<AiCodeMetric[]> {
  const { data } = await api.get<AiCodeMetric[]>("/api/v1/ai/code-metrics", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchAiSdlcMetrics(programId?: number): Promise<AiSdlcMetric[]> {
  const { data } = await api.get<AiSdlcMetric[]>("/api/v1/ai/sdlc-metrics", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchAiTrustScores(programId?: number): Promise<AiTrustScore[]> {
  const { data } = await api.get<AiTrustScore[]>("/api/v1/ai/trust-scores", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchAiGovernance(programId?: number): Promise<AiGovernanceConfig[]> {
  const { data } = await api.get<AiGovernanceConfig[]>("/api/v1/ai/governance-config", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

export async function fetchAiOverrides(programId?: number): Promise<AiOverride[]> {
  const { data } = await api.get<AiOverride[]>("/api/v1/ai/override-log", {
    params: programId ? { program_id: programId } : undefined,
  });
  return data;
}

// ---------- Smart Ops + Risk & Audit ----------

export type ScenarioExecution = {
  id: number;
  scenario_name: string;
  execution_date: string | null;
  triggered_by: string | null;
  status: string | null;
  details: string | null;
  financial_impact: number | null;
  outcome_notes: string | null;
};

export type ResourceRow = {
  id: number;
  name: string;
  role: string | null;
  role_tier: string | null;
  skill_set: string | null;
  current_program_id: number | null;
  current_project_id: number | null;
  utilization_pct: number | null;
  bench_days: number;
  loaded_cost_annual: number | null;
  status: string;
};

export type AuditEntry = {
  id: number;
  action: string | null;
  table_name: string | null;
  record_id: number | null;
  old_value: string | null;
  new_value: string | null;
  user_action: string | null;
  timestamp: string;
};

export async function fetchScenarios(status?: string): Promise<ScenarioExecution[]> {
  const { data } = await api.get<ScenarioExecution[]>(
    "/api/v1/smart-ops/scenarios",
    { params: status ? { status } : undefined },
  );
  return data;
}

export async function fetchResources(benchOnly = false): Promise<ResourceRow[]> {
  const { data } = await api.get<ResourceRow[]>("/api/v1/smart-ops/resources", {
    params: benchOnly ? { bench_only: true } : undefined,
  });
  return data;
}

export async function fetchAuditLog(
  tableName?: string,
  limit = 50,
): Promise<AuditEntry[]> {
  const { data } = await api.get<AuditEntry[]>("/api/v1/audit", {
    params: { table_name: tableName, limit },
  });
  return data;
}

// ---------- Reports & Forecasts ----------

export type Forecast = {
  kpi_code: string;
  programme_code: string | null;
  historical_dates: string[];
  historical_values: number[];
  horizon_months: number;
  horizon_labels: string[];
  series: { label: string; values: number[] }[];
};

export async function fetchForecast(
  kpiCode: string,
  programmeCode?: string,
  horizon = 3,
): Promise<Forecast> {
  const { data } = await api.get<Forecast>("/api/v1/forecasts", {
    params: {
      kpi_code: kpiCode,
      programme_code: programmeCode,
      horizon,
    },
  });
  return data;
}

export function qbrPdfUrl(programId: number): string {
  return `/api/v1/reports/qbr/${programId}.pdf`;
}

export function auditPackageUrl(programId?: number): string {
  return programId !== undefined
    ? `/api/v1/reports/audit-package.zip?program_id=${programId}`
    : `/api/v1/reports/audit-package.zip`;
}

export async function previewCsv(file: File): Promise<{
  filename: string;
  columns: string[];
  row_count: number;
  sample: Record<string, string>[];
}> {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/api/v1/import/csv/preview", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}
