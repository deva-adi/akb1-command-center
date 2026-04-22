import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AxiosError } from "axios";
import {
  Bar,
  CartesianGrid,
  Cell,
  ComposedChart,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardHeader } from "@/components/ui/Card";
import {
  fetchPnlBridge,
  fetchPnlWaterfall,
  type BridgeOut,
  type PnlErrorEnvelope,
  type PnlFilters,
  type WaterfallOut,
} from "@/api/pnlApi";

/**
 * Section 2 of Tab 12: Margin Bridge step-walk chart.
 *
 * Wires /api/v1/pnl/bridge/{metric_key} with the canonical key
 * pnl.gross_margin_pct.programme.month. The chart renders a
 * running-total waterfall: prior gross margin on the left, the four
 * drivers (Price, Volume, Mix, Cost) stepping through the middle,
 * current gross margin on the right. Positive drivers rise from the
 * running total; negative drivers drop from it. Each bar carries a
 * bps label so the bridge reads cleanly on a single glance.
 *
 * /bridge requires explicit from + to. When the URL does not set
 * them, we probe /waterfall to learn the programme's current
 * snapshot_date and derive prior as (current - 1 month).
 */

const DEFAULT_METRIC_KEY = "pnl.gross_margin_pct.programme.month";

type BarKind = "anchor" | "up" | "down";

type BridgeBar = {
  name: string;
  label: string;
  invisible: number;
  visible: number;
  kind: BarKind;
};

const COLOURS: Record<BarKind, string> = {
  anchor: "#1B2A4A", // navy
  up: "#10b981", // green-500
  down: "#ef4444", // red-500
};

function formatBps(value: number): string {
  const sign = value > 0 ? "+" : value < 0 ? "−" : "";
  return `${sign}${Math.abs(value).toFixed(0)} bps`;
}

function formatPctLabel(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

function priorFromSnapshot(snapshot: string | null): {
  from: string;
  to: string;
} | null {
  if (!snapshot) return null;
  const current = new Date(`${snapshot}T00:00:00Z`);
  if (Number.isNaN(current.getTime())) return null;
  const priorMonth = new Date(
    Date.UTC(
      current.getUTCFullYear(),
      current.getUTCMonth() - 1,
      1,
    ),
  );
  const toIso = (d: Date) => d.toISOString().slice(0, 10);
  return { from: toIso(priorMonth), to: toIso(current) };
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

function buildBars(bridge: BridgeOut): BridgeBar[] {
  const priorBps = bridge.prior_value * 10000;
  const currentBps = bridge.current_value * 10000;
  const d = bridge.drivers;

  // Walk the running total so each driver bar floats between its
  // previous running total and its new running total. This keeps
  // positive drivers rising and negative drivers falling, so a viewer
  // reads the visual drop from prior to current as the sum of the
  // four steps.
  const afterPrice = priorBps + d.price_bps;
  const afterVolume = afterPrice + d.volume_bps;
  const afterMix = afterVolume + d.mix_bps;
  const afterCost = afterMix + d.cost_bps_residual;

  const step = (
    name: string,
    delta: number,
    runningBefore: number,
    runningAfter: number,
  ): BridgeBar => {
    const up = delta >= 0;
    return {
      name,
      label: formatBps(delta),
      invisible: Math.min(runningBefore, runningAfter),
      visible: Math.abs(delta),
      kind: up ? "up" : "down",
    };
  };

  return [
    {
      name: "Prior",
      label: formatPctLabel(bridge.prior_value),
      invisible: 0,
      visible: priorBps,
      kind: "anchor",
    },
    step("Price", d.price_bps, priorBps, afterPrice),
    step("Volume", d.volume_bps, afterPrice, afterVolume),
    step("Mix", d.mix_bps, afterVolume, afterMix),
    step("Cost", d.cost_bps_residual, afterMix, afterCost),
    {
      name: "Current",
      label: formatPctLabel(bridge.current_value),
      invisible: 0,
      visible: currentBps,
      kind: "anchor",
    },
  ];
}

export function MarginBridge() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");
  const urlFrom = searchParams.get("from");
  const urlTo = searchParams.get("to");

  const baseFilters: PnlFilters = {
    scenario_name: searchParams.get("scenario_name") ?? undefined,
  };

  // When the URL does not carry from/to we probe /waterfall for the
  // programme's current snapshot_date so we can derive a default
  // one-month-prior window for the bridge.
  const waterfallQuery = useQuery<WaterfallOut, AxiosError>({
    queryKey: ["pnl", "bridge", "waterfall-probe", programme, baseFilters],
    queryFn: () => fetchPnlWaterfall(programme!, baseFilters),
    enabled: !!programme && (!urlFrom || !urlTo),
  });

  const derivedWindow =
    urlFrom && urlTo
      ? { from: urlFrom, to: urlTo }
      : priorFromSnapshot(waterfallQuery.data?.snapshot_date ?? null);

  const bridgeQuery = useQuery<BridgeOut, AxiosError>({
    queryKey: [
      "pnl",
      "bridge",
      programme,
      DEFAULT_METRIC_KEY,
      derivedWindow,
    ],
    queryFn: () =>
      fetchPnlBridge(DEFAULT_METRIC_KEY, {
        programme: programme!,
        from: derivedWindow!.from,
        to: derivedWindow!.to,
      }),
    enabled: !!programme && !!derivedWindow,
  });

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see the margin bridge"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  const loading =
    waterfallQuery.isLoading ||
    bridgeQuery.isLoading ||
    bridgeQuery.isFetching && !bridgeQuery.data;
  const firstError = waterfallQuery.error ?? bridgeQuery.error;

  if (firstError) {
    return (
      <Card>
        <CardHeader
          title="Margin bridge failed to load"
          subtitle="Try refreshing or check /api/v1/pnl/bridge."
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

  if (loading || !bridgeQuery.data) {
    return (
      <Card>
        <CardHeader
          title="Margin bridge"
          subtitle="Loading prior and current snapshots."
        />
        <div
          className="h-64 animate-pulse rounded border border-ice-100 bg-ice-50"
          data-testid="margin-bridge-loading"
        />
      </Card>
    );
  }

  const bridge = bridgeQuery.data;
  const bars = buildBars(bridge);

  const minY = Math.min(...bars.map((b) => b.invisible));
  const maxY = Math.max(...bars.map((b) => b.invisible + b.visible));
  const pad = Math.max((maxY - minY) * 0.1, 50);
  const yDomain: [number, number] = [
    Math.max(0, Math.floor(minY - pad)),
    Math.ceil(maxY + pad),
  ];

  // formatBps uses the Unicode minus; reuse it for the total so the
  // subtitle and aria-label stay consistent with the driver bars.
  const totalLabel = formatBps(bridge.total_delta_bps).replace(/ bps$/, "");

  return (
    <Card>
      <CardHeader
        title="Margin bridge"
        subtitle={`Gross margin ${formatPctLabel(bridge.prior_value)} on ${bridge.prior_snapshot_date} → ${formatPctLabel(bridge.current_value)} on ${bridge.current_snapshot_date} · total delta ${totalLabel} bps`}
      />
      <div
        className="h-64 w-full"
        data-testid="margin-bridge-chart"
        aria-label={`Margin bridge for ${bridge.programme_code}: prior ${formatPctLabel(bridge.prior_value)}, price ${formatBps(bridge.drivers.price_bps)}, volume ${formatBps(bridge.drivers.volume_bps)}, mix ${formatBps(bridge.drivers.mix_bps)}, cost ${formatBps(bridge.drivers.cost_bps_residual)}, current ${formatPctLabel(bridge.current_value)}, total ${totalLabel} bps`}
      >
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={bars}
            margin={{ top: 24, right: 16, bottom: 8, left: 8 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#d5e8f0"
              vertical={false}
            />
            <XAxis
              dataKey="name"
              tick={{ fontSize: 12, fill: "#1B2A4A" }}
              axisLine={{ stroke: "#d5e8f0" }}
              tickLine={false}
            />
            <YAxis
              domain={yDomain}
              tick={{ fontSize: 11, fill: "#1B2A4A" }}
              axisLine={{ stroke: "#d5e8f0" }}
              tickLine={false}
              label={{
                value: "bps",
                angle: -90,
                position: "insideLeft",
                style: { fontSize: 11, fill: "#1B2A4A" },
              }}
            />
            <Tooltip
              formatter={(_: unknown, __: unknown, entry: { payload?: BridgeBar }) => {
                const bar = entry?.payload;
                return bar ? [bar.label, bar.name] : [null, null];
              }}
            />
            <Bar dataKey="invisible" stackId="walk" fill="transparent" />
            <Bar dataKey="visible" stackId="walk">
              {bars.map((b) => (
                <Cell key={b.name} fill={COLOURS[b.kind]} />
              ))}
              <LabelList
                dataKey="label"
                position="top"
                style={{
                  fontSize: 11,
                  fill: "#1B2A4A",
                  fontWeight: 600,
                }}
              />
            </Bar>
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-3 text-xs text-navy/60">
        Prior and current bars anchor from zero. Green steps raise the
        running margin; red steps drop it. The four drivers sum to
        the total delta by construction (see formulas 50 through 53 in
        docs/FORMULAS.md).
      </p>
    </Card>
  );
}
