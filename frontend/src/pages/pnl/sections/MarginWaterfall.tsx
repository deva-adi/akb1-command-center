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
  fetchPnlWaterfall,
  type PnlErrorEnvelope,
  type PnlFilters,
  type WaterfallOut,
} from "@/api/pnlApi";

/**
 * Section 3 of Tab 12: four-layer Margin Waterfall cascade.
 *
 * Wires /api/v1/pnl/waterfall/{programme_code}. Single-snapshot view
 * of how gross margin thins through the four accounting layers:
 * Gross -> Contribution -> Portfolio -> Net. No prior period involved
 * (the Margin Bridge in M7.2 covers the prior-to-current walk).
 *
 * Each bar is labelled with the layer percentage at its top. The drop
 * from one layer to the next is labelled in bps between consecutive
 * bars so the reader sees where the margin leaks: cost of delivery,
 * operating overhead, corporate allocation, tax. Three render states
 * mirror M7.1 and M7.2: no-programme prompt, loading skeleton, error
 * banner with the backend envelope message.
 */

const LAYER_ORDER = ["gross", "contribution", "portfolio", "net"] as const;
type LayerKey = (typeof LAYER_ORDER)[number];

type LayerThresholds = { green: number; red: number };

const THRESHOLDS: Record<LayerKey, LayerThresholds> = {
  gross: { green: 0.30, red: 0.22 },
  contribution: { green: 0.18, red: 0.10 },
  portfolio: { green: 0.22, red: 0.15 },
  net: { green: 0.10, red: 0.05 },
};

const TONES = {
  green: "#10b981",
  amber: "#f59e0b",
  red: "#ef4444",
  neutral: "#94a3b8",
} as const;

function toneFor(layer: LayerKey, pct: number | null): string {
  if (pct === null) return TONES.neutral;
  const t = THRESHOLDS[layer];
  if (pct >= t.green) return TONES.green;
  if (pct < t.red) return TONES.red;
  return TONES.amber;
}

function formatPctLabel(value: number | null): string {
  if (value === null) return "n/a";
  return `${(value * 100).toFixed(1)}%`;
}

function formatDropBps(delta: number): string {
  // Drops are positive numbers (the amount lost between layers). Show
  // with a leading minus to read as "margin fell by N bps".
  return `−${Math.abs(Math.round(delta))} bps`;
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

type BarDatum = {
  key: LayerKey;
  label: string;
  value: number | null;
  displayPct: string;
  fill: string;
};

function buildBars(waterfall: WaterfallOut): BarDatum[] {
  const byLayer = new Map(waterfall.layers.map((l) => [l.layer, l]));
  return LAYER_ORDER.map((key) => {
    const l = byLayer.get(key);
    const pct = l?.margin_pct ?? null;
    return {
      key,
      label: l?.label ?? key,
      value: pct,
      displayPct: formatPctLabel(pct),
      fill: toneFor(key, pct),
    };
  });
}

function buildDrops(
  bars: BarDatum[],
): Array<{ from: LayerKey; to: LayerKey; bps: number } | null> {
  const drops: Array<{ from: LayerKey; to: LayerKey; bps: number } | null> = [];
  for (let i = 0; i < bars.length - 1; i++) {
    const a = bars[i].value;
    const b = bars[i + 1].value;
    if (a === null || b === null) {
      drops.push(null);
    } else {
      drops.push({
        from: bars[i].key,
        to: bars[i + 1].key,
        bps: (a - b) * 10000,
      });
    }
  }
  return drops;
}

export function MarginWaterfall() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");

  const filters: PnlFilters = {
    from: searchParams.get("from") ?? undefined,
    to: searchParams.get("to") ?? undefined,
    scenario_name: searchParams.get("scenario_name") ?? undefined,
  };

  const waterfallQuery = useQuery<WaterfallOut, AxiosError>({
    queryKey: ["pnl", "waterfall", programme, filters],
    queryFn: () => fetchPnlWaterfall(programme!, filters),
    enabled: !!programme,
  });

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see the margin waterfall"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  if (waterfallQuery.error) {
    return (
      <Card>
        <CardHeader
          title="Margin waterfall failed to load"
          subtitle="Try refreshing or check /api/v1/pnl/waterfall."
        />
        <div
          role="alert"
          className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {errorMessage(waterfallQuery.error)}
        </div>
      </Card>
    );
  }

  if (waterfallQuery.isLoading || !waterfallQuery.data) {
    return (
      <Card>
        <CardHeader
          title="Margin waterfall"
          subtitle="Loading latest snapshot."
        />
        <div
          className="h-64 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="margin-waterfall-loading"
        />
      </Card>
    );
  }

  const data = waterfallQuery.data;
  const bars = buildBars(data);
  const drops = buildDrops(bars);
  const yMax = Math.max(0.01, ...bars.map((b) => b.value ?? 0)) * 1.2;

  const ariaLabel = `Margin waterfall for ${data.programme_code} at ${data.snapshot_date}: ${bars
    .map((b) => `${b.label} ${b.displayPct}`)
    .join(", ")}. Drops: ${drops
    .map((d) =>
      d
        ? `${d.from} to ${d.to} ${formatDropBps(d.bps)}`
        : "drop unavailable",
    )
    .join(", ")}.`;

  return (
    <Card>
      <CardHeader
        title="Margin waterfall"
        subtitle={`Snapshot ${data.snapshot_date} · scenario ${data.scenario_name} · revenue base ${data.revenue.toLocaleString("en-US")}`}
        titleAdornment={
          <PnlSectionInfo
            title="Margin waterfall"
            whatItShows="How gross margin erodes through four layers of cost allocation, from raw delivery margin to the net return after all overheads."
            formula="Gross = Revenue minus Direct Cost. Contribution = Gross minus Shared Overhead. Portfolio = Contribution minus Programme Overhead. Net = Portfolio minus Corporate Overhead."
            howToRead="Each drop shows what a cost layer consumes. Net Margin near zero means the programme is structurally unprofitable even if gross looks acceptable."
            thresholds="Gross target 30 percent. Net target 10 percent. PHOENIX current: Gross 28 percent (RED), Net 4.1 percent (RED)."
          />
        }
      />
      <div
        className="relative h-64 w-full"
        data-testid="margin-waterfall-chart"
        aria-label={ariaLabel}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={bars}
            margin={{ top: 28, right: 16, bottom: 8, left: 8 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#d5e8f0"
              vertical={false}
            />
            <XAxis
              dataKey="label"
              tick={{ fontSize: 12, fill: "#1B2A4A" }}
              axisLine={{ stroke: "#d5e8f0" }}
              tickLine={false}
            />
            <YAxis
              domain={[0, yMax]}
              tick={{ fontSize: 11, fill: "#1B2A4A" }}
              tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
              axisLine={{ stroke: "#d5e8f0" }}
              tickLine={false}
              label={{
                value: "Margin %",
                angle: -90,
                position: "insideLeft",
                style: { fontSize: 11, fill: "#1B2A4A" },
              }}
            />
            <Tooltip
              formatter={(_v: unknown, _name: unknown, entry: { payload?: BarDatum }) => {
                const bar = entry?.payload;
                return bar ? [bar.displayPct, bar.label] : [null, null];
              }}
            />
            <Bar dataKey="value">
              {bars.map((b) => (
                <Cell key={b.key} fill={b.fill} />
              ))}
              <LabelList
                dataKey="displayPct"
                position="top"
                style={{ fontSize: 12, fill: "#1B2A4A", fontWeight: 600 }}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        {/*
          Drop annotations sit in a three-cell row positioned at the
          midpoints between the four bars. Using pointer-events-none
          keeps Recharts interactions unblocked; the z-index lifts the
          pills above the chart SVG.
        */}
        <div
          className="pointer-events-none absolute inset-x-8 top-1/2 z-10 -translate-y-1/2 grid grid-cols-3"
          data-testid="margin-waterfall-drops"
        >
          {drops.map((d, idx) => (
            <div
              key={idx}
              className="flex justify-center"
              data-rail-drop-index={idx}
            >
              {d ? (
                <span className="rounded-full bg-white/95 px-2 py-0.5 text-[11px] font-semibold text-navy shadow-sm ring-1 ring-navy/10 dark:bg-navy-700 dark:text-navy-50 dark:ring-navy-400/40">
                  {formatDropBps(d.bps)}
                </span>
              ) : (
                <span className="text-[11px] text-navy/40">n/a</span>
              )}
            </div>
          ))}
        </div>
      </div>
      <p className="mt-3 text-xs text-navy/60">
        Bars cascade left to right through the four margin layers. The
        pill between consecutive bars shows the drop in basis points.
        Phoenix demo thresholds: gross green ≥ 30%, net green ≥ 10%.
      </p>
    </Card>
  );
}
