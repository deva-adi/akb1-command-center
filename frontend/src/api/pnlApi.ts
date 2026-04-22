import { api } from "@/lib/api";

/**
 * Typed client for the nine v5.7.0 Tab 12 /api/v1/pnl/ endpoints.
 *
 * Response types mirror backend/app/schemas/pnl.py. Keep this file in
 * lock-step with the Pydantic schemas — changes to one must land with
 * changes to the other or the OpenAPI contract drifts.
 *
 * M6 ships the client only. M7 wires it to the Tab 12 section
 * components. The three v5.8 deferrals (/board, /levers, /narrative)
 * are not included here by design; adding them is part of the v5.8
 * pickup tracked in docs/TECH_DEBT.md.
 */

// --- Filters ----------------------------------------------------------

/**
 * Canonical universal filter set. Matches the backend FiltersApplied
 * alias vocabulary exactly: `programme`, `from`, `to`, `tier`,
 * `scenario_name`, `portfolio`, `month`. Every endpoint accepts this
 * shape as query params; individual endpoints are free to ignore
 * fields that do not apply.
 */
export type PnlFilters = {
  programme?: string;
  from?: string;
  to?: string;
  tier?: "Junior" | "Mid" | "Senior";
  scenario_name?: string;
  portfolio?: string;
  month?: string;
};

export type FiltersApplied = {
  programme: string[] | null;
  from: string | null;
  to: string | null;
  tier: "Junior" | "Mid" | "Senior" | null;
  scenario_name: string | null;
  portfolio: string | null;
  month: string | null;
};

// --- Shared lineage block --------------------------------------------

export type LineageEntry = {
  composite_key: string;
  program_code: string | null;
  snapshot_date: string | null;
  scenario_name: string | null;
  table: string | null;
  row_id: number | null;
  columns_used: Record<string, unknown> | null;
  description: string | null;
};

export type LineageBlock = {
  formula: string;
  formula_ref: string | null;
  entries: LineageEntry[];
  entries_total_count: number;
  sampling: "full" | "sampled";
  sampling_rule: string | null;
};

// --- Standard error envelope -----------------------------------------

export type PnlErrorEnvelope = {
  error: {
    code: string;
    message: string;
    details: Record<string, unknown> | null;
  };
  filters_applied: FiltersApplied | null;
};

// --- /waterfall ------------------------------------------------------

export type WaterfallLayer = {
  layer: "gross" | "contribution" | "portfolio" | "net";
  label: string;
  margin_pct: number | null;
  margin_value: number | null;
};

export type WaterfallOut = {
  programme_code: string;
  snapshot_date: string;
  scenario_name: string;
  revenue: number;
  layers: WaterfallLayer[];
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlWaterfall(
  programmeCode: string,
  filters: PnlFilters = {},
): Promise<WaterfallOut> {
  const { data } = await api.get<WaterfallOut>(
    `/api/v1/pnl/waterfall/${programmeCode}`,
    { params: filters },
  );
  return data;
}

// --- /bridge ---------------------------------------------------------

export type BridgeDrivers = {
  price_bps: number;
  volume_bps: number;
  mix_bps: number;
  cost_bps_residual: number;
};

export type BridgeOut = {
  metric_key: string;
  programme_code: string;
  prior_snapshot_date: string;
  current_snapshot_date: string;
  prior_value: number;
  current_value: number;
  total_delta_bps: number;
  drivers: BridgeDrivers;
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlBridge(
  metricKey: string,
  filters: PnlFilters = {},
): Promise<BridgeOut> {
  const { data } = await api.get<BridgeOut>(
    `/api/v1/pnl/bridge/${encodeURIComponent(metricKey)}`,
    { params: filters },
  );
  return data;
}

// --- /pfa ------------------------------------------------------------

export type PfaMetric = "revenue" | "gross_pct" | "net_pct" | "cpi" | "spi";

export type PfaPoint = {
  snapshot_date: string;
  value: number | null;
};

export type PfaSeries = {
  plan: PfaPoint[];
  forecast: PfaPoint[];
  actual: PfaPoint[];
};

export type PfaOut = {
  programme_code: string;
  metric: PfaMetric;
  series: PfaSeries;
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlPfa(
  programmeCode: string,
  metric: PfaMetric = "gross_pct",
  filters: PnlFilters = {},
): Promise<PfaOut> {
  const { data } = await api.get<PfaOut>(
    `/api/v1/pnl/pfa/${programmeCode}`,
    { params: { ...filters, metric } },
  );
  return data;
}

// --- /pyramid --------------------------------------------------------

export type PyramidTier = {
  role_tier: "Junior" | "Mid" | "Senior";
  planned_headcount: number | null;
  actual_headcount: number | null;
  planned_weight: number | null;
  actual_weight: number | null;
  planned_rate: number | null;
  actual_rate: number | null;
  utilisation_pct: number | null;
};

export type PyramidOut = {
  programme_code: string;
  snapshot_date: string | null;
  tiers: PyramidTier[];
  realisation_rate_pct: number | null;
  rag: "green" | "amber" | "red";
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlPyramid(
  programmeCode: string,
  filters: PnlFilters = {},
): Promise<PyramidOut> {
  const { data } = await api.get<PyramidOut>(
    `/api/v1/pnl/pyramid/${programmeCode}`,
    { params: filters },
  );
  return data;
}

// --- /losses ---------------------------------------------------------

export type LossRow = {
  loss_category: string;
  amount: number;
  revenue_foregone: number;
  margin_points_lost_programme_bps: number;
  margin_points_lost_portfolio_bps: number;
  snapshot_date: string | null;
  mitigation_status: string | null;
};

export type LossesOut = {
  programme_code: string;
  target_gross_margin_pct: number;
  programme_revenue: number;
  portfolio_revenue: number;
  rows: LossRow[];
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlLosses(
  programmeCode: string,
  filters: PnlFilters = {},
): Promise<LossesOut> {
  const { data } = await api.get<LossesOut>(
    `/api/v1/pnl/losses/${programmeCode}`,
    { params: filters },
  );
  return data;
}

// --- /evm ------------------------------------------------------------

export type EvmOut = {
  programme_code: string;
  snapshot_date: string | null;
  planned_value: number | null;
  earned_value: number | null;
  actual_cost: number | null;
  percent_complete: number | null;
  bac: number | null;
  cpi: number | null;
  spi: number | null;
  eac: number | null;
  tcpi: number | null;
  vac: number | null;
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlEvm(
  programmeCode: string,
  filters: PnlFilters = {},
): Promise<EvmOut> {
  const { data } = await api.get<EvmOut>(
    `/api/v1/pnl/evm/${programmeCode}`,
    { params: filters },
  );
  return data;
}

// --- /dso ------------------------------------------------------------

export type DsoOut = {
  programme_code: string;
  snapshot_date: string | null;
  scenario_name: string | null;
  billed_revenue: number | null;
  collected_revenue: number | null;
  ar_balance: number | null;
  unbilled_wip: number | null;
  dso_days: number | null;
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlDso(
  programmeCode: string,
  filters: PnlFilters = {},
): Promise<DsoOut> {
  const { data } = await api.get<DsoOut>(
    `/api/v1/pnl/dso/${programmeCode}`,
    { params: filters },
  );
  return data;
}

// --- /revenue --------------------------------------------------------

export type RevenueCardKey =
  | "committed_revenue"
  | "booked_revenue"
  | "billed_revenue"
  | "collected_revenue"
  | "unbilled_wip";

export type RevenueCard = {
  card_key: RevenueCardKey;
  label: string;
  value: number | null;
  source_column: string;
};

export type RevenueOut = {
  programme_code: string;
  snapshot_date: string | null;
  scenario_name: string | null;
  cards: RevenueCard[];
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlRevenue(
  programmeCode: string,
  filters: PnlFilters = {},
): Promise<RevenueOut> {
  const { data } = await api.get<RevenueOut>(
    `/api/v1/pnl/revenue/${programmeCode}`,
    { params: filters },
  );
  return data;
}

// --- /lineage --------------------------------------------------------

export type LineageAtomicRow = {
  composite_key: string;
  table: string;
  row_id: number | null;
  program_code: string | null;
  snapshot_date: string | null;
  scenario_name: string | null;
  columns_used: Record<string, unknown> | null;
};

export type LineageResolverOut = {
  metric_key: string;
  parsed: { tab: string; metric: string; slice: string; aggregation: string };
  supported: boolean;
  formula: string;
  formula_ref: string | null;
  value: number | null;
  unit: string;
  atomic_rows: LineageAtomicRow[];
  filters_applied: FiltersApplied;
  lineage: LineageBlock;
};

export async function fetchPnlLineage(
  metricKey: string,
  filters: PnlFilters = {},
): Promise<LineageResolverOut> {
  const { data } = await api.get<LineageResolverOut>(
    `/api/v1/pnl/lineage/${encodeURIComponent(metricKey)}`,
    { params: filters },
  );
  return data;
}
