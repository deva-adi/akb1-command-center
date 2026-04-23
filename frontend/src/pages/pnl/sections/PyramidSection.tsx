import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AxiosError } from "axios";
import {
  LineChart,
  Line,
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardHeader } from "@/components/ui/Card";
import {
  fetchPnlDso,
  fetchPnlEvm,
  fetchPnlPfa,
  fetchPnlPyramid,
  type DsoOut,
  type EvmOut,
  type PfaOut,
  type PnlErrorEnvelope,
  type PnlFilters,
  type PyramidOut,
} from "@/api/pnlApi";
import { formatCurrency } from "@/lib/format";
import { cn } from "@/lib/cn";
import { PyramidChart, type PyramidChartInput } from "@/pages/pnl/sections/PyramidChart";

/**
 * Section 6 of Tab 12: Resource Pyramid with EVM and DSO sub-cards.
 *
 * Three endpoints feed this section, each queried independently so a
 * slow endpoint does not block the others:
 *   - /pyramid for the tier distribution bar chart
 *   - /evm for current CPI / SPI / etc. + two /pfa calls for sparkline trends
 *   - /dso for current DSO days + AR + Unbilled WIP (no trend — v5.8 per TECH_DEBT.md)
 *
 * Scope decisions from 2026-04-22 M7.6 review (all Gap Option A variants
 * unless noted):
 *   - Gap 1: three tiers only (Senior / Mid / Junior). Offshore dropped.
 *   - Gap 2: render headcount + weight + rate + utilisation. No per-tier
 *     margin — the data model does not support it cleanly. Bar width =
 *     actual_weight × programme_revenue as an approx revenue anchor.
 *   - Gap 3: /evm + /pfa(cpi) + /pfa(spi) for the sub-card.
 *   - Gap 4: no DSO trend sparkline — too heavy for a small ornament.
 *     Tracked for v5.8 in docs/TECH_DEBT.md.
 *   - Gap 5: "Unbilled WIP" as the third DSO metric (no Accrued Margin).
 *   - Per-sub-card snapshot dates in subtitles since the three endpoints
 *     reference different months.
 */

type Palette = "neutral" | "green" | "amber" | "red";

function errorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const envelope = err.response?.data as PnlErrorEnvelope | undefined;
    if (envelope?.error?.message) return envelope.error.message;
    return err.message;
  }
  if (err instanceof Error) return err.message;
  return "Unknown error";
}

function paletteClass(p: Palette): string {
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

function cpiSpiPalette(value: number | null): Palette {
  if (value === null) return "neutral";
  if (value >= 1.0) return "green";
  if (value >= 0.9) return "amber";
  return "red";
}

function dsoPalette(days: number | null): Palette {
  if (days === null) return "neutral";
  if (days < 45) return "green";
  if (days <= 60) return "amber";
  return "red";
}

function formatRatio(value: number | null, digits = 2): string {
  if (value === null) return "n/a";
  return value.toFixed(digits);
}

function formatDays(value: number | null): string {
  if (value === null) return "n/a";
  return `${value.toFixed(1)} d`;
}

function tierOrder(role: string): number {
  if (role === "Senior") return 0;
  if (role === "Mid") return 1;
  if (role === "Junior") return 2;
  return 99;
}

// --- Top-level section ------------------------------------------------

export function PyramidSection() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see the resource pyramid"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader
        title="Resource pyramid"
        subtitle="Tier distribution, earned value, and receivables. Each sub-card shows its own snapshot date since the three endpoints reference different months."
      />
      <PyramidBlock programme={programme} searchParams={searchParams} />
      <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
        <EvmSubCard programme={programme} searchParams={searchParams} />
        <DsoSubCard programme={programme} searchParams={searchParams} />
      </div>
    </Card>
  );
}

// --- Pyramid chart block ---------------------------------------------

function PyramidBlock({
  programme,
  searchParams,
}: {
  programme: string;
  searchParams: URLSearchParams;
}) {
  const filters: PnlFilters = {
    from: searchParams.get("from") ?? undefined,
    to: searchParams.get("to") ?? undefined,
  };

  const pyramidQuery = useQuery<PyramidOut, AxiosError>({
    queryKey: ["pnl", "pyramid", programme, filters],
    queryFn: () => fetchPnlPyramid(programme, filters),
  });

  // /pyramid does not return programme_revenue; fall back to /waterfall
  // (revenue field) so the bar widths are anchored in a real number.
  // This does not block the chart — we render with a sensible default
  // if the waterfall probe has not landed yet.
  const revenueQuery = useQuery<{ revenue: number }, AxiosError>({
    queryKey: ["pnl", "pyramid-revenue", programme, filters],
    queryFn: async () => {
      const { fetchPnlWaterfall } = await import("@/api/pnlApi");
      const w = await fetchPnlWaterfall(programme, filters);
      return { revenue: w.revenue };
    },
  });

  const data: PyramidChartInput[] = useMemo(() => {
    if (!pyramidQuery.data) return [];
    return [...pyramidQuery.data.tiers]
      .sort((a, b) => tierOrder(a.role_tier) - tierOrder(b.role_tier))
      .map((t) => ({
        tier: t.role_tier,
        actual_weight: t.actual_weight ?? 0,
        actual_headcount: t.actual_headcount ?? 0,
        rate: t.actual_rate ?? 0,
        utilisation: (t.utilisation_pct ?? 0) / 100,
      }));
  }, [pyramidQuery.data]);

  if (pyramidQuery.error) {
    return (
      <div
        role="alert"
        className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
      >
        Pyramid failed to load: {errorMessage(pyramidQuery.error)}
      </div>
    );
  }

  if (pyramidQuery.isLoading || !pyramidQuery.data) {
    return (
      <div
        className="h-40 animate-pulse rounded border border-ice-100 bg-ice-50"
        data-testid="pyramid-loading"
      />
    );
  }

  const p = pyramidQuery.data;
  const programmeRevenue = revenueQuery.data?.revenue ?? 0;

  return (
    <div data-testid="pyramid-block">
      <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2 text-xs text-navy/60">
        <span>
          Snapshot {p.snapshot_date ?? "n/a"} · realisation{" "}
          {p.realisation_rate_pct != null
            ? `${p.realisation_rate_pct.toFixed(1)}%`
            : "n/a"}
        </span>
        <span className="flex items-center gap-2">
          Overall RAG
          <span
            className={cn(
              "inline-flex rounded px-2 py-0.5 text-xs font-semibold ring-1",
              paletteClass(p.rag),
            )}
            data-testid="pyramid-rag"
            data-rag-palette={p.rag}
          >
            {p.rag.charAt(0).toUpperCase() + p.rag.slice(1)}
          </span>
        </span>
      </div>
      <PyramidChart data={data} programmeRevenue={programmeRevenue} />
    </div>
  );
}

// --- EVM sub-card ----------------------------------------------------

function EvmSubCard({
  programme,
  searchParams,
}: {
  programme: string;
  searchParams: URLSearchParams;
}) {
  const filters: PnlFilters = {
    from: searchParams.get("from") ?? undefined,
    to: searchParams.get("to") ?? undefined,
  };

  const evmQuery = useQuery<EvmOut, AxiosError>({
    queryKey: ["pnl", "evm", programme, filters],
    queryFn: () => fetchPnlEvm(programme, filters),
  });

  const cpiSeries = useQuery<PfaOut, AxiosError>({
    queryKey: ["pnl", "pfa", "cpi", programme, filters],
    queryFn: () => fetchPnlPfa(programme, "cpi", filters),
  });

  const spiSeries = useQuery<PfaOut, AxiosError>({
    queryKey: ["pnl", "pfa", "spi", programme, filters],
    queryFn: () => fetchPnlPfa(programme, "spi", filters),
  });

  if (evmQuery.error) {
    return (
      <SubCard title="Earned value (CPI · SPI)">
        <Banner message={`EVM failed: ${errorMessage(evmQuery.error)}`} />
      </SubCard>
    );
  }

  if (evmQuery.isLoading || !evmQuery.data) {
    return (
      <SubCard title="Earned value (CPI · SPI)">
        <div
          className="h-40 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="evm-loading"
        />
      </SubCard>
    );
  }

  const e = evmQuery.data;
  const cpiPalette = cpiSpiPalette(e.cpi);
  const spiPal = cpiSpiPalette(e.spi);

  return (
    <SubCard
      title="Earned value (CPI · SPI)"
      subtitle={
        e.snapshot_date
          ? `Snapshot ${e.snapshot_date}. % complete ${e.percent_complete != null ? `${e.percent_complete.toFixed(1)}%` : "n/a"}.`
          : "No EVM snapshot for this window."
      }
      testId="evm-sub-card"
    >
      <div className="grid grid-cols-2 gap-4">
        <EvmMetric
          label="CPI"
          value={formatRatio(e.cpi)}
          formula="CPI = EV / AC"
          palette={cpiPalette}
          sparkline={
            cpiSeries.data?.series.actual.slice(-6) ?? []
          }
          sparklineLoading={cpiSeries.isLoading}
          sparklineError={!!cpiSeries.error}
          testId="evm-cpi"
        />
        <EvmMetric
          label="SPI"
          value={formatRatio(e.spi)}
          formula="SPI = EV / PV"
          palette={spiPal}
          sparkline={
            spiSeries.data?.series.actual.slice(-6) ?? []
          }
          sparklineLoading={spiSeries.isLoading}
          sparklineError={!!spiSeries.error}
          testId="evm-spi"
        />
      </div>
      <p className="mt-3 text-xs text-navy/60">
        RAG: red below 0.9, amber 0.9–1.0, green at or above 1.0. Sparkline
        shows the last six actuals from /pfa for the matching metric.
      </p>
    </SubCard>
  );
}

function EvmMetric({
  label,
  value,
  formula,
  palette,
  sparkline,
  sparklineLoading,
  sparklineError,
  testId,
}: {
  label: string;
  value: string;
  formula: string;
  palette: Palette;
  sparkline: Array<{ snapshot_date: string; value: number | null }>;
  sparklineLoading: boolean;
  sparklineError: boolean;
  testId: string;
}) {
  return (
    <div data-testid={testId}>
      <div className="flex items-baseline justify-between">
        <span className="text-xs uppercase tracking-wide text-navy/60">
          {label}
        </span>
        <span
          className={cn(
            "inline-flex rounded px-2 py-0.5 text-[10px] font-semibold uppercase ring-1",
            paletteClass(palette),
          )}
          data-rag-palette={palette}
        >
          {palette}
        </span>
      </div>
      <div className="mt-1 font-mono text-3xl font-bold tabular-nums text-navy">
        {value}
      </div>
      <div className="text-[11px] font-mono text-navy/60">{formula}</div>
      <div className="mt-2 h-10 w-full" data-testid={`${testId}-sparkline`}>
        {sparklineLoading ? (
          <div className="h-full animate-pulse rounded bg-ice-50" />
        ) : sparklineError ? (
          <div className="text-[11px] text-red-600">sparkline unavailable</div>
        ) : sparkline.length === 0 ? (
          <div className="text-[11px] text-navy/40">no trend data</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sparkline}>
              <XAxis dataKey="snapshot_date" hide />
              <YAxis hide domain={["dataMin", "dataMax"]} />
              <RechartsTooltip
                formatter={(v: number | string) => [v, label]}
                labelFormatter={(l) => l}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#1E3A5F"
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

// --- DSO sub-card ----------------------------------------------------

function DsoSubCard({
  programme,
  searchParams,
}: {
  programme: string;
  searchParams: URLSearchParams;
}) {
  const filters: PnlFilters = {
    from: searchParams.get("from") ?? undefined,
    to: searchParams.get("to") ?? undefined,
  };

  const dsoQuery = useQuery<DsoOut, AxiosError>({
    queryKey: ["pnl", "pyramid-dso", programme, filters],
    queryFn: () => fetchPnlDso(programme, filters),
  });

  if (dsoQuery.error) {
    return (
      <SubCard title="Days sales outstanding">
        <Banner message={`DSO failed: ${errorMessage(dsoQuery.error)}`} />
      </SubCard>
    );
  }

  if (dsoQuery.isLoading || !dsoQuery.data) {
    return (
      <SubCard title="Days sales outstanding">
        <div
          className="h-40 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="dso-loading"
        />
      </SubCard>
    );
  }

  const d = dsoQuery.data;
  const palette = dsoPalette(d.dso_days);

  return (
    <SubCard
      title="Days sales outstanding"
      subtitle={
        d.snapshot_date
          ? `Snapshot ${d.snapshot_date}${d.scenario_name ? ` · scenario ${d.scenario_name}` : ""}.`
          : "No DSO snapshot for this window."
      }
      testId="dso-sub-card"
    >
      <div>
        <div className="flex items-baseline justify-between">
          <span className="text-xs uppercase tracking-wide text-navy/60">
            DSO days
          </span>
          <span
            className={cn(
              "inline-flex rounded px-2 py-0.5 text-[10px] font-semibold uppercase ring-1",
              paletteClass(palette),
            )}
            data-rag-palette={palette}
            data-testid="dso-rag"
          >
            {palette}
          </span>
        </div>
        <div
          className="mt-1 font-mono text-3xl font-bold tabular-nums text-navy"
          data-testid="dso-value"
        >
          {formatDays(d.dso_days)}
        </div>
        <div className="text-[11px] font-mono text-navy/60">
          DSO = (AR balance / billed revenue) × 30
        </div>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3">
        <div data-testid="dso-ar">
          <div className="text-[11px] uppercase tracking-wide text-navy/60">
            AR balance
          </div>
          <div className="font-mono text-lg font-semibold tabular-nums text-navy">
            {formatCurrency(d.ar_balance)}
          </div>
        </div>
        <div data-testid="dso-unbilled">
          <div className="text-[11px] uppercase tracking-wide text-navy/60">
            Unbilled WIP
          </div>
          <div className="font-mono text-lg font-semibold tabular-nums text-navy">
            {formatCurrency(d.unbilled_wip)}
          </div>
        </div>
      </div>
      <p className="mt-3 text-xs text-navy/60">
        RAG: green under 45 d, amber 45–60 d, red above 60 d. DSO trend
        sparkline is deferred to v5.8 (see TECH_DEBT.md).
      </p>
    </SubCard>
  );
}

// --- Shared sub-card primitive ---------------------------------------

function SubCard({
  title,
  subtitle,
  children,
  testId,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  testId?: string;
}) {
  return (
    <div
      className="rounded border border-ice-100 bg-white p-4 dark:border-navy-500 dark:bg-navy-700"
      data-testid={testId}
    >
      <div className="mb-3">
        <div className="text-sm font-semibold text-navy dark:text-navy-50">
          {title}
        </div>
        {subtitle && (
          <div className="text-xs text-navy/60 dark:text-navy-100/60">
            {subtitle}
          </div>
        )}
      </div>
      {children}
    </div>
  );
}

function Banner({ message }: { message: string }) {
  return (
    <div
      role="alert"
      className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
    >
      {message}
    </div>
  );
}
