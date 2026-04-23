import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { Card, CardHeader } from "@/components/ui/Card";
import {
  fetchPnlPfa,
  type PfaOut,
  type PfaPoint,
  type PnlErrorEnvelope,
  type PnlFilters,
} from "@/api/pnlApi";
import { formatCurrency } from "@/lib/format";
import { cn } from "@/lib/cn";

/**
 * Section 4 of Tab 12: Plan / Forecast / Actual comparison table.
 *
 * Wires /api/v1/pnl/pfa with two calls: metric=revenue and
 * metric=gross_pct. Cost is derived client-side per session decision
 * 2026-04-22 (Gap 1 Option A): cost = revenue * (1 - gross_margin_pct).
 * Cost is not a /pfa metric; this keeps the backend contract stable
 * and the cost column reconciles with the planned_revenue /
 * actual_cost pair already exposed via M7.1.
 *
 * Collapse rule for the time-series response (Gap 2 Option B):
 *   - If URL sets ?from= or ?to= those bound the candidate window.
 *   - Within that window, the latest snapshot from each series wins.
 *   - No filters -> latest across the whole seeded range.
 *
 * The Iron Triangle diagram called out in earlier drafts of the brief
 * was dropped by decision (Gap 3 Option A). PFA stays PFA-only; an
 * Iron Triangle section earns its own milestone with /evm + scope
 * health plumbing.
 *
 * Variance rules for the gross-margin row (Adi's brief):
 *   - Red if actual is below plan by more than 200 bps.
 *   - Amber if between 0 and 200 bps below plan.
 *   - Green if at or above plan.
 *
 * Revenue and Cost variance cells stay neutrally toned; only the
 * gross-margin row carries the RAG colouring.
 */

const FORECAST_FOOTNOTE =
  "Forecast at Completion not seeded — planned for v5.8.";

type VariancePalette = "neutral" | "red" | "amber" | "green";

type RowDisplay = {
  label: string;
  planned: string;
  forecast: string;
  actual: string;
  variance: string;
  palette: VariancePalette;
};

function errorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const envelope = err.response?.data as PnlErrorEnvelope | undefined;
    if (envelope?.error?.message) return envelope.error.message;
    return err.message;
  }
  if (err instanceof Error) return err.message;
  return "Unknown error";
}

function latestInWindow(
  points: PfaPoint[],
  from: string | null,
  to: string | null,
): PfaPoint | null {
  const filtered = points.filter((p) => {
    if (from && p.snapshot_date < from) return false;
    if (to && p.snapshot_date > to) return false;
    return p.value !== null;
  });
  if (filtered.length === 0) return null;
  // Series are returned in ascending snapshot_date, but sort defensively.
  return [...filtered].sort((a, b) =>
    a.snapshot_date.localeCompare(b.snapshot_date),
  )[filtered.length - 1];
}

function pickSnapshots(
  series: PfaOut["series"],
  from: string | null,
  to: string | null,
): { plan: PfaPoint | null; forecast: PfaPoint | null; actual: PfaPoint | null } {
  return {
    plan: latestInWindow(series.plan, from, to),
    forecast: latestInWindow(series.forecast, from, to),
    actual: latestInWindow(series.actual, from, to),
  };
}

function marginRagPalette(
  planPct: number | null,
  actualPct: number | null,
): VariancePalette {
  if (planPct === null || actualPct === null) return "neutral";
  const deltaBps = (actualPct - planPct) * 10000;
  if (deltaBps >= 0) return "green";
  if (deltaBps >= -200) return "amber";
  return "red";
}

function formatSignedCurrency(delta: number | null): string {
  if (delta === null) return "n/a";
  const sign = delta > 0 ? "+" : delta < 0 ? "−" : "";
  return `${sign}${formatCurrency(Math.abs(delta))}`;
}

function formatSignedPct(delta: number | null): string {
  if (delta === null) return "";
  const sign = delta > 0 ? "+" : delta < 0 ? "−" : "";
  return `${sign}${Math.abs(delta * 100).toFixed(1)}%`;
}

function formatSignedBps(delta: number | null): string {
  if (delta === null) return "n/a";
  const sign = delta > 0 ? "+" : delta < 0 ? "−" : "";
  return `${sign}${Math.abs(Math.round(delta))} bps`;
}

function formatPctValue(value: number | null): string {
  if (value === null) return "n/a";
  return `${(value * 100).toFixed(1)}%`;
}

function formatCurrencyValue(value: number | null): string {
  if (value === null) return "n/a";
  return formatCurrency(value);
}

function currencyVarianceText(
  plan: number | null,
  actual: number | null,
): string {
  if (plan === null || actual === null) return "n/a";
  const abs = actual - plan;
  const pct = plan !== 0 ? (actual - plan) / Math.abs(plan) : null;
  const pctText = pct === null ? "" : ` (${formatSignedPct(pct)})`;
  return `${formatSignedCurrency(abs)}${pctText}`;
}

function deriveCost(
  revenueSnap: PfaPoint | null,
  marginSnap: PfaPoint | null,
): number | null {
  if (revenueSnap?.value == null || marginSnap?.value == null) return null;
  return revenueSnap.value * (1 - marginSnap.value);
}

function paletteClass(p: VariancePalette): string {
  switch (p) {
    case "red":
      return "bg-red-50 text-red-700 ring-red-200";
    case "amber":
      return "bg-amber-50 text-amber-700 ring-amber-200";
    case "green":
      return "bg-emerald-50 text-emerald-700 ring-emerald-200";
    default:
      return "bg-ice-50 text-navy/80 ring-ice-100";
  }
}

function buildRows(revenue: PfaOut, margin: PfaOut, from: string | null, to: string | null): RowDisplay[] {
  const rev = pickSnapshots(revenue.series, from, to);
  const mar = pickSnapshots(margin.series, from, to);

  // Revenue row.
  const revRow: RowDisplay = {
    label: "Revenue",
    planned: formatCurrencyValue(rev.plan?.value ?? null),
    forecast: formatCurrencyValue(rev.forecast?.value ?? null),
    actual: formatCurrencyValue(rev.actual?.value ?? null),
    variance: currencyVarianceText(
      rev.plan?.value ?? null,
      rev.actual?.value ?? null,
    ),
    palette: "neutral",
  };

  // Cost row, derived.
  const planCost = deriveCost(rev.plan, mar.plan);
  const forecastCost = deriveCost(rev.forecast, mar.forecast);
  const actualCost = deriveCost(rev.actual, mar.actual);
  const costRow: RowDisplay = {
    label: "Cost (derived)",
    planned: formatCurrencyValue(planCost),
    forecast: formatCurrencyValue(forecastCost),
    actual: formatCurrencyValue(actualCost),
    variance: currencyVarianceText(planCost, actualCost),
    palette: "neutral",
  };

  // Gross margin row with RAG.
  const marginPalette = marginRagPalette(
    mar.plan?.value ?? null,
    mar.actual?.value ?? null,
  );
  const marginDeltaBps =
    mar.plan?.value != null && mar.actual?.value != null
      ? (mar.actual.value - mar.plan.value) * 10000
      : null;
  const marginRow: RowDisplay = {
    label: "Gross margin",
    planned: formatPctValue(mar.plan?.value ?? null),
    forecast: formatPctValue(mar.forecast?.value ?? null),
    actual: formatPctValue(mar.actual?.value ?? null),
    variance: formatSignedBps(marginDeltaBps),
    palette: marginPalette,
  };

  return [revRow, costRow, marginRow];
}

export function PfaTable() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");
  const fromParam = searchParams.get("from");
  const toParam = searchParams.get("to");

  const filters: PnlFilters = {
    from: fromParam ?? undefined,
    to: toParam ?? undefined,
    scenario_name: searchParams.get("scenario_name") ?? undefined,
  };

  const revenueQuery = useQuery<PfaOut, AxiosError>({
    queryKey: ["pnl", "pfa", "revenue", programme, filters],
    queryFn: () => fetchPnlPfa(programme!, "revenue", filters),
    enabled: !!programme,
  });

  const marginQuery = useQuery<PfaOut, AxiosError>({
    queryKey: ["pnl", "pfa", "gross_pct", programme, filters],
    queryFn: () => fetchPnlPfa(programme!, "gross_pct", filters),
    enabled: !!programme,
  });

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see plan vs forecast vs actual"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  const firstError = revenueQuery.error ?? marginQuery.error;

  if (firstError) {
    return (
      <Card>
        <CardHeader
          title="PFA table failed to load"
          subtitle="Try refreshing or check /api/v1/pnl/pfa."
        />
        <div
          role="alert"
          className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {errorMessage(firstError)}
        </div>
      </Card>
    );
  }

  if (
    revenueQuery.isLoading ||
    marginQuery.isLoading ||
    !revenueQuery.data ||
    !marginQuery.data
  ) {
    return (
      <Card>
        <CardHeader
          title="Plan vs forecast vs actual"
          subtitle="Loading revenue and gross-margin series."
        />
        <div
          className="h-32 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="pfa-loading"
        />
      </Card>
    );
  }

  const rows = buildRows(
    revenueQuery.data,
    marginQuery.data,
    fromParam,
    toParam,
  );

  const windowLabel =
    fromParam || toParam
      ? `${fromParam ?? "…"} → ${toParam ?? "…"}`
      : "latest seeded snapshot in each series";

  return (
    <Card>
      <CardHeader
        title="Plan vs forecast vs actual"
        subtitle={`Comparison window: ${windowLabel}. Cost row derived as revenue × (1 − gross margin %).`}
      />
      <div className="overflow-x-auto" data-testid="pfa-table">
        <table className="w-full text-sm">
          <thead className="border-b border-ice-100 text-left text-xs uppercase tracking-wide text-navy/60">
            <tr>
              <th className="py-2 pr-4 font-semibold">Row</th>
              <th className="py-2 pr-4 font-semibold">Planned</th>
              <th className="py-2 pr-4 font-semibold">Forecast</th>
              <th className="py-2 pr-4 font-semibold">Actual</th>
              <th className="py-2 pr-4 font-semibold">Variance (actual − planned)</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.label}
                className="border-b border-ice-100 last:border-b-0"
                data-testid={`pfa-row-${row.label
                  .toLowerCase()
                  .replace(/\W+/g, "-")
                  .replace(/^-+|-+$/g, "")}`}
              >
                <td className="py-2 pr-4 font-semibold text-navy">
                  {row.label}
                </td>
                <td className="py-2 pr-4 font-mono tabular-nums text-navy">
                  {row.planned}
                </td>
                <td className="py-2 pr-4 font-mono tabular-nums text-navy/50">
                  {row.forecast}
                </td>
                <td className="py-2 pr-4 font-mono tabular-nums text-navy">
                  {row.actual}
                </td>
                <td className="py-2 pr-4">
                  <span
                    className={cn(
                      "inline-flex rounded px-2 py-0.5 font-mono text-xs font-semibold tabular-nums ring-1",
                      paletteClass(row.palette),
                    )}
                    data-variance-palette={row.palette}
                  >
                    {row.variance}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-navy/60" data-testid="pfa-forecast-footnote">
        {FORECAST_FOOTNOTE}
      </p>
      <p className="mt-1 text-xs text-navy/60">
        Gross margin variance uses RAG: red if actual is more than 200
        bps below plan, amber between 0 and 200 bps below, green at or
        above plan. Revenue and Cost variance cells stay neutral.
      </p>
    </Card>
  );
}
