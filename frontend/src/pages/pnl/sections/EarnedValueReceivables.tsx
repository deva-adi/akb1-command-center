import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AxiosError } from "axios";
import {
  Line,
  LineChart,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader } from "@/components/ui/Card";
import { PnlSectionInfo } from "@/components/PnlSectionInfo";
import {
  fetchPnlDso,
  fetchPnlEvm,
  fetchPnlPfa,
  type DsoOut,
  type EvmOut,
  type PfaOut,
  type PnlErrorEnvelope,
  type PnlFilters,
} from "@/api/pnlApi";
import { cn } from "@/lib/cn";
import {
  cpiSpiPalette,
  dsoPalette,
  type Palette,
} from "@/pages/pnl/sections/palettes";

/**
 * Section 7 of Tab 12: Earned Value and Receivables.
 *
 * Two sub-cards side by side, equal width. CPI and SPI on the left feed
 * from /evm with a combined six-month sparkline pulled from /pfa for each
 * metric. DSO days plus AR balance and Unbilled WIP on the right feed
 * from /dso with no trend (deferred to v5.8 per TECH_DEBT.md).
 *
 * EVM and DSO already appear as compact sub-cards inside the M7.6
 * Pyramid section. This section is the standalone treatment: one
 * combined CPI/SPI sparkline and a DSO-as-hero layout. Both sections
 * are active simultaneously by design.
 */

const CPI_STROKE = "#1E3A5F";
const SPI_STROKE = "#2E6DA4";

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

function errorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const envelope = err.response?.data as PnlErrorEnvelope | undefined;
    if (envelope?.error?.message) return envelope.error.message;
    return err.message;
  }
  if (err instanceof Error) return err.message;
  return "Unknown error";
}

function formatRatio(value: number | null): string {
  if (value === null) return "n/a";
  return value.toFixed(2);
}

function formatMillions(value: number | null): string {
  if (value === null) return "n/a";
  return `$${(value / 1_000_000).toFixed(2)} M`;
}

function formatDsoDays(value: number | null): string {
  if (value === null) return "n/a";
  return `${value.toFixed(1)} days`;
}

export function EarnedValueReceivables() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see earned value and receivables"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader
        title="Earned Value and Receivables"
        subtitle="Cost and schedule indices on the left with a six-month CPI and SPI trend. DSO days and the receivables stack on the right. Each sub-card carries its own snapshot date."
        titleAdornment={
          <PnlSectionInfo
            title="Earned Value and Receivables"
            whatItShows="Standalone deep-dive on two financial health dimensions: delivery cost efficiency (EVM) and cash flow speed (receivables)."
            formula="CPI = EV divided by AC. SPI = EV divided by PV. DSO = (AR Balance divided by Billed Revenue) times 30."
            howToRead="CPI below 1.0 means you are spending more than the value delivered. DSO above 60 means your client is slow to pay. Both red simultaneously means programme in financial distress on two dimensions."
          />
        }
      />
      <div
        className="grid grid-cols-1 gap-4 md:grid-cols-2"
        data-testid="evr-section"
      >
        <EarnedValueCard programme={programme} searchParams={searchParams} />
        <ReceivablesCard programme={programme} searchParams={searchParams} />
      </div>
    </Card>
  );
}

function EarnedValueCard({
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
    queryKey: ["pnl", "evr-evm", programme, filters],
    queryFn: () => fetchPnlEvm(programme, filters),
  });

  const cpiSeries = useQuery<PfaOut, AxiosError>({
    queryKey: ["pnl", "evr-pfa", "cpi", programme, filters],
    queryFn: () => fetchPnlPfa(programme, "cpi", filters),
  });

  const spiSeries = useQuery<PfaOut, AxiosError>({
    queryKey: ["pnl", "evr-pfa", "spi", programme, filters],
    queryFn: () => fetchPnlPfa(programme, "spi", filters),
  });

  const sparkData = useMemo(() => {
    const cpiPoints = (cpiSeries.data?.series.actual ?? []).slice(-6);
    const spiPoints = (spiSeries.data?.series.actual ?? []).slice(-6);
    const dates = new Set<string>();
    cpiPoints.forEach((p) => dates.add(p.snapshot_date));
    spiPoints.forEach((p) => dates.add(p.snapshot_date));
    const cpiByDate = new Map(cpiPoints.map((p) => [p.snapshot_date, p.value]));
    const spiByDate = new Map(spiPoints.map((p) => [p.snapshot_date, p.value]));
    return Array.from(dates)
      .sort()
      .map((d) => ({
        snapshot_date: d,
        cpi: cpiByDate.get(d) ?? null,
        spi: spiByDate.get(d) ?? null,
      }));
  }, [cpiSeries.data, spiSeries.data]);

  if (evmQuery.error) {
    return (
      <SubCard title="Earned Value">
        <Banner message={`Earned value failed: ${errorMessage(evmQuery.error)}`} />
      </SubCard>
    );
  }

  if (evmQuery.isLoading || !evmQuery.data) {
    return (
      <SubCard title="Earned Value">
        <div
          className="h-40 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="evr-evm-loading"
        />
      </SubCard>
    );
  }

  const e = evmQuery.data;
  const cpiPal = cpiSpiPalette(e.cpi);
  const spiPal = cpiSpiPalette(e.spi);
  const sparklineLoading = cpiSeries.isLoading || spiSeries.isLoading;
  const sparklineError = !!cpiSeries.error || !!spiSeries.error;

  return (
    <SubCard
      title="Earned Value"
      subtitle={
        e.snapshot_date
          ? `Snapshot ${e.snapshot_date}`
          : "No earned value snapshot for this window."
      }
      testId="evr-evm-card"
    >
      <div className="grid grid-cols-2 gap-4">
        <RatioBlock
          label="CPI"
          labelAdornment={
            <PnlSectionInfo
              title="CPI (Cost Performance Index)"
              whatItShows="Cost Performance Index. Above 1.0 means under budget. Below 0.9 means cost overrun."
              formula="CPI = EV / AC"
              howToRead="PHOENIX 0.87 means spending 1.15 dollars per 1 dollar of value delivered."
              thresholds="Green at or above 1.0, Amber 0.9 to 1.0, Red below 0.9."
            />
          }
          value={formatRatio(e.cpi)}
          palette={cpiPal}
          testId="evr-cpi"
        />
        <RatioBlock
          label="SPI"
          labelAdornment={
            <PnlSectionInfo
              title="SPI (Schedule Performance Index)"
              whatItShows="Schedule Performance Index. Above 1.0 means ahead of schedule. Below 0.9 means behind schedule."
              formula="SPI = EV / PV"
              howToRead="PHOENIX 0.84 means 84 percent of planned work completed on time."
              thresholds="Green at or above 1.0, Amber 0.9 to 1.0, Red below 0.9."
            />
          }
          value={formatRatio(e.spi)}
          palette={spiPal}
          testId="evr-spi"
        />
      </div>
      <div
        className="mt-2 text-[11px] font-mono text-navy/60"
        data-testid="evr-formula"
      >
        CPI = EV / AC   |   SPI = EV / PV
      </div>
      <div className="mt-3" data-testid="evr-sparkline">
        <div style={{ width: 200, height: 52 }}>
          {sparklineLoading ? (
            <div className="h-full w-full animate-pulse rounded bg-ice-50" />
          ) : sparklineError ? (
            <div className="text-[11px] text-red-600">sparkline unavailable</div>
          ) : sparkData.length === 0 ? (
            <div className="text-[11px] text-navy/40">no trend data</div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={sparkData}
                margin={{ top: 4, right: 4, bottom: 4, left: 4 }}
              >
                <Line
                  type="monotone"
                  dataKey="cpi"
                  stroke={CPI_STROKE}
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                  connectNulls
                />
                <Line
                  type="monotone"
                  dataKey="spi"
                  stroke={SPI_STROKE}
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                  connectNulls
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
        <div className="mt-1 flex gap-3 text-[11px] text-navy/60">
          <span className="flex items-center gap-1">
            <span
              className="inline-block h-2 w-2 rounded-full"
              style={{ background: CPI_STROKE }}
            />
            CPI
          </span>
          <span className="flex items-center gap-1">
            <span
              className="inline-block h-2 w-2 rounded-full"
              style={{ background: SPI_STROKE }}
            />
            SPI
          </span>
        </div>
      </div>
    </SubCard>
  );
}

function ReceivablesCard({
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
    queryKey: ["pnl", "evr-dso", programme, filters],
    queryFn: () => fetchPnlDso(programme, filters),
  });

  if (dsoQuery.error) {
    return (
      <SubCard title="Receivables">
        <Banner message={`Receivables failed: ${errorMessage(dsoQuery.error)}`} />
      </SubCard>
    );
  }

  if (dsoQuery.isLoading || !dsoQuery.data) {
    return (
      <SubCard title="Receivables">
        <div
          className="h-40 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="evr-dso-loading"
        />
      </SubCard>
    );
  }

  const d = dsoQuery.data;
  const palette = dsoPalette(d.dso_days);

  return (
    <SubCard
      title="Receivables"
      subtitle={
        d.snapshot_date
          ? `Snapshot ${d.snapshot_date}`
          : "No DSO snapshot for this window."
      }
      testId="evr-receivables-card"
    >
      <div className="flex items-baseline gap-3">
        <div
          className="font-mono text-3xl font-bold tabular-nums text-navy"
          data-testid="evr-dso-days"
        >
          {formatDsoDays(d.dso_days)}
          <PnlSectionInfo
            title="DSO (Days Sales Outstanding)"
            whatItShows="Days Sales Outstanding. The average number of days between invoicing and payment receipt."
            formula="DSO = (AR Balance / Billed Revenue) × 30"
            howToRead="PHOENIX 6.0 days is GREEN. Client pays within one week of invoice. Industry average 45 to 60 days."
            thresholds="Green under 45 days, Amber 45 to 60, Red above 60."
          />
        </div>
        <span
          className={cn(
            "inline-flex rounded px-2 py-0.5 text-[10px] font-semibold uppercase ring-1",
            paletteClass(palette),
          )}
          data-rag-palette={palette}
          data-testid="evr-dso-rag"
        >
          {palette}
        </span>
      </div>
      <div className="mt-1 text-[11px] font-mono text-navy/60">
        DSO = (AR balance / billed revenue) × 30
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3">
        <div data-testid="evr-dso-ar">
          <div className="text-[11px] uppercase tracking-wide text-navy/60">
            AR balance
          </div>
          <div className="font-mono text-lg font-semibold tabular-nums text-navy">
            {formatMillions(d.ar_balance)}
          </div>
        </div>
        <div data-testid="evr-dso-unbilled">
          <div className="text-[11px] uppercase tracking-wide text-navy/60">
            Unbilled WIP
          </div>
          <div className="font-mono text-lg font-semibold tabular-nums text-navy">
            {formatMillions(d.unbilled_wip)}
          </div>
        </div>
      </div>
      <p className="mt-3 text-xs text-navy/60">
        RAG: green under 45 days, amber 45 to 60, red above 60. DSO trend
        sparkline is deferred to v5.8.
      </p>
    </SubCard>
  );
}

function RatioBlock({
  label,
  labelAdornment,
  value,
  palette,
  testId,
}: {
  label: string;
  labelAdornment?: React.ReactNode;
  value: string;
  palette: Palette;
  testId: string;
}) {
  return (
    <div data-testid={testId}>
      <div className="flex items-baseline justify-between">
        <span className="text-xs uppercase tracking-wide text-navy/60">
          {label}
          {labelAdornment}
        </span>
        <span
          className={cn(
            "inline-flex rounded px-2 py-0.5 text-[10px] font-semibold uppercase ring-1",
            paletteClass(palette),
          )}
          data-rag-palette={palette}
          data-testid={`${testId}-rag`}
        >
          {palette}
        </span>
      </div>
      <div className="mt-1 font-mono text-3xl font-bold tabular-nums text-navy">
        {value}
      </div>
    </div>
  );
}

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
