import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AxiosError } from "axios";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardHeader } from "@/components/ui/Card";
import { PnlSectionInfo } from "@/components/PnlSectionInfo";
import {
  fetchPnlLosses,
  type LossesOut,
  type LossRow,
  type PnlErrorEnvelope,
  type PnlFilters,
} from "@/api/pnlApi";
import { formatCurrency } from "@/lib/format";
import { cn } from "@/lib/cn";

/**
 * Section 5 of Tab 12: Losses with Attribution.
 *
 * Wires /api/v1/pnl/losses/{programme_code}. Renders a seven-column
 * table of per-category loss rows plus a horizontal bar chart that
 * breaks total losses down by loss_category. A total-row RAG chip
 * fires off (total amount / programme_revenue): red above 2%, amber
 * 1-2%, green under 1%.
 *
 * Column set chosen 2026-04-22 (Option B): Date, Category, Mitigation,
 * Amount, Revenue Foregone, Margin Lost (bps), Cumulative. Revenue
 * Foregone and Margin Lost are the signal that ties this section
 * back to the Waterfall and Bridge — a Scope Creep event translates
 * into basis-point pressure on the programme's margin.
 */

const BREAKDOWN_COLOURS = [
  "#1B2A4A", // navy
  "#2563eb", // blue-600
  "#8b5cf6", // violet-500
  "#f59e0b", // amber-500
  "#ef4444", // red-500
  "#10b981", // emerald-500
  "#0ea5e9", // sky-500
];

function errorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const envelope = err.response?.data as PnlErrorEnvelope | undefined;
    if (envelope?.error?.message) return envelope.error.message;
    return err.message;
  }
  if (err instanceof Error) return err.message;
  return "Unknown error";
}

function totalRagPalette(ratio: number | null): "green" | "amber" | "red" | "neutral" {
  if (ratio === null) return "neutral";
  const pct = ratio * 100;
  if (pct < 1) return "green";
  if (pct <= 2) return "amber";
  return "red";
}

function paletteClass(p: "green" | "amber" | "red" | "neutral"): string {
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

function formatPct(ratio: number | null, digits = 1): string {
  if (ratio === null) return "n/a";
  return `${(ratio * 100).toFixed(digits)}%`;
}

function formatBps(value: number | null): string {
  if (value === null) return "n/a";
  return `${Math.round(value).toLocaleString("en-US")} bps`;
}

function formatDate(iso: string | null): string {
  if (!iso) return "n/a";
  return iso;
}

type RunningRow = LossRow & { cumulative: number };

export function LossesAttribution() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");

  const filters: PnlFilters = {
    from: searchParams.get("from") ?? undefined,
    to: searchParams.get("to") ?? undefined,
    scenario_name: searchParams.get("scenario_name") ?? undefined,
  };

  const lossesQuery = useQuery<LossesOut, AxiosError>({
    queryKey: ["pnl", "losses", programme, filters],
    queryFn: () => fetchPnlLosses(programme!, filters),
    enabled: !!programme,
  });

  const withCumulative: RunningRow[] = useMemo(() => {
    if (!lossesQuery.data) return [];
    let running = 0;
    return lossesQuery.data.rows.map((r) => {
      running += r.amount;
      return { ...r, cumulative: running };
    });
  }, [lossesQuery.data]);

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see losses with attribution"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  if (lossesQuery.error) {
    return (
      <Card>
        <CardHeader
          title="Losses section failed to load"
          subtitle="Try refreshing or check /api/v1/pnl/losses."
        />
        <div
          role="alert"
          className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {errorMessage(lossesQuery.error)}
        </div>
      </Card>
    );
  }

  if (lossesQuery.isLoading || !lossesQuery.data) {
    return (
      <Card>
        <CardHeader
          title="Losses with attribution"
          subtitle="Loading loss events from the backend."
        />
        <div
          className="h-40 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="losses-loading"
        />
      </Card>
    );
  }

  const data = lossesQuery.data;
  const totalAmount = withCumulative.reduce((s, r) => s + r.amount, 0);
  const ratio =
    data.programme_revenue > 0 ? totalAmount / data.programme_revenue : null;
  const palette = totalRagPalette(ratio);

  if (withCumulative.length === 0) {
    return (
      <Card>
        <CardHeader
          title="Losses with attribution"
          subtitle="Loss events recorded against programme for selected period."
        />
        <div
          className="flex items-center justify-center gap-3 rounded border border-dashed border-ice-100 px-4 py-10 text-sm text-navy/60"
          data-testid="losses-empty"
        >
          <span
            aria-hidden="true"
            className="inline-flex size-8 items-center justify-center rounded-full bg-ice-50 text-navy/40"
          >
            ∅
          </span>
          <span>No loss events recorded for this programme in the selected period.</span>
        </div>
      </Card>
    );
  }

  const breakdownData = withCumulative.map((r) => ({
    category: r.loss_category,
    amount: r.amount,
    pct: totalAmount > 0 ? r.amount / totalAmount : 0,
    label: `${formatCurrency(r.amount)} (${formatPct(totalAmount > 0 ? r.amount / totalAmount : 0)})`,
  }));

  return (
    <Card>
      <CardHeader
        title="Losses with attribution"
        subtitle="Loss events recorded against programme for selected period."
        titleAdornment={
          <PnlSectionInfo
            title="Losses with attribution"
            whatItShows="Every identified delivery loss event (money spent on non-billable work) categorised by root cause and converted to revenue equivalent impact."
            formula="Revenue Foregone = Loss Amount divided by (1 minus Target Gross Margin pct). Margin Lost bps = Amount divided by Programme Revenue times 10000."
            howToRead="Total losses as percent of revenue is the headline. Above 5 percent is a red flag. PHOENIX at 237.8 percent is critically distressed. Sort by Amount to find where to intervene first."
            thresholds="Green under 1 percent of revenue. Amber 1 to 5 percent. Red above 5 percent."
          />
        }
      />

      <div className="overflow-x-auto" data-testid="losses-table">
        <table className="w-full text-sm">
          <thead className="border-b border-ice-100 text-left text-xs uppercase tracking-wide text-navy/60">
            <tr>
              <th className="py-2 pr-4 font-semibold">Date</th>
              <th className="py-2 pr-4 font-semibold">Category</th>
              <th className="py-2 pr-4 font-semibold">Mitigation</th>
              <th className="py-2 pr-4 text-right font-semibold">Amount</th>
              <th className="py-2 pr-4 text-right font-semibold">
                Revenue foregone
                <PnlSectionInfo
                  title="Revenue foregone"
                  whatItShows="Converts a cost loss into revenue equivalent: how much you would need to bill to recover it at target margin."
                  formula="Revenue foregone = Amount divided by (1 minus target margin)"
                  howToRead="Use this to size the commercial recovery needed to absorb the loss without dropping below target margin."
                />
              </th>
              <th className="py-2 pr-4 text-right font-semibold">
                Margin lost
                <PnlSectionInfo
                  title="Margin lost"
                  whatItShows="Loss expressed as basis points of programme revenue."
                  formula="Margin lost (bps) = Amount divided by Programme Revenue times 10000"
                  howToRead="One bps equals 0.01 percent of programme revenue."
                />
              </th>
              <th className="py-2 pr-4 text-right font-semibold">
                Cumulative
                <PnlSectionInfo
                  title="Cumulative loss"
                  whatItShows="Running total of all losses to this row, sorted by date."
                  howToRead="Read top-down to see how losses compound over the period."
                />
              </th>
            </tr>
          </thead>
          <tbody>
            {withCumulative.map((row) => (
              <tr
                key={`${row.loss_category}-${row.snapshot_date ?? "nd"}`}
                className="border-b border-ice-100 last:border-b-0"
                data-testid={`losses-row-${row.loss_category
                  .toLowerCase()
                  .replace(/\W+/g, "-")
                  .replace(/^-+|-+$/g, "")}`}
              >
                <td className="py-2 pr-4 font-mono tabular-nums text-navy/80">
                  {formatDate(row.snapshot_date)}
                </td>
                <td className="py-2 pr-4 font-semibold text-navy">
                  {row.loss_category}
                </td>
                <td className="py-2 pr-4 text-navy/70">
                  {row.mitigation_status ?? "n/a"}
                </td>
                <td className="py-2 pr-4 text-right font-mono tabular-nums text-navy">
                  {formatCurrency(row.amount)}
                </td>
                <td className="py-2 pr-4 text-right font-mono tabular-nums text-navy/80">
                  {formatCurrency(row.revenue_foregone)}
                </td>
                <td className="py-2 pr-4 text-right font-mono tabular-nums text-navy/80">
                  {formatBps(row.margin_points_lost_programme_bps)}
                </td>
                <td className="py-2 pr-4 text-right font-mono tabular-nums text-navy/80">
                  {formatCurrency(row.cumulative)}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr
              className="border-t-2 border-navy/20"
              data-testid="losses-total-row"
            >
              <td className="py-2 pr-4 font-semibold text-navy" colSpan={3}>
                Total losses
              </td>
              <td className="py-2 pr-4 text-right font-mono tabular-nums font-bold text-navy">
                {formatCurrency(totalAmount)}
              </td>
              <td className="py-2 pr-4 text-right font-mono tabular-nums text-navy/60" colSpan={2}>
                {ratio === null
                  ? ""
                  : `${formatPct(ratio)} of programme revenue ${formatCurrency(data.programme_revenue)}`}
              </td>
              <td className="py-2 pr-4 text-right">
                <span
                  className={cn(
                    "inline-flex rounded px-2 py-0.5 text-xs font-semibold ring-1",
                    paletteClass(palette),
                  )}
                  data-rag-palette={palette}
                  data-testid="losses-total-rag"
                >
                  {palette === "red"
                    ? "Red"
                    : palette === "amber"
                      ? "Amber"
                      : palette === "green"
                        ? "Green"
                        : "n/a"}
                </span>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      <div className="mt-6">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-navy/60">
          Breakdown by category
        </p>
        <div
          className="h-48 w-full"
          data-testid="losses-breakdown-chart"
          aria-label={`Loss breakdown for ${data.programme_code}: ${breakdownData
            .map((b) => `${b.category} ${formatCurrency(b.amount)} (${formatPct(b.pct)})`)
            .join(", ")}.`}
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={breakdownData}
              layout="vertical"
              margin={{ top: 8, right: 96, bottom: 8, left: 8 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#d5e8f0"
                horizontal={false}
              />
              <XAxis
                type="number"
                tick={{ fontSize: 11, fill: "#1B2A4A" }}
                tickFormatter={(v: number) => formatCurrency(v)}
                axisLine={{ stroke: "#d5e8f0" }}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="category"
                tick={{ fontSize: 12, fill: "#1B2A4A" }}
                axisLine={{ stroke: "#d5e8f0" }}
                tickLine={false}
                width={160}
              />
              <Tooltip
                formatter={(_v: unknown, _name: unknown, entry: { payload?: { amount: number; pct: number } }) => {
                  const p = entry?.payload;
                  return p
                    ? [`${formatCurrency(p.amount)} (${formatPct(p.pct)})`, "Amount"]
                    : [null, null];
                }}
              />
              <Bar dataKey="amount">
                {breakdownData.map((_, i) => (
                  <Cell
                    key={i}
                    fill={BREAKDOWN_COLOURS[i % BREAKDOWN_COLOURS.length]}
                  />
                ))}
                <LabelList
                  dataKey="label"
                  position="right"
                  style={{
                    fontSize: 11,
                    fill: "#1B2A4A",
                    fontWeight: 600,
                  }}
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <p className="mt-3 text-xs text-navy/60">
        Revenue foregone uses target gross margin {formatPct(data.target_gross_margin_pct, 0)}:
        revenue_foregone = amount / (1 − target_gross_margin_pct). Margin lost in bps is
        amount / programme_revenue × 10,000. Total RAG: red above 2% of programme revenue,
        amber 1–2%, green under 1%.
      </p>
    </Card>
  );
}
