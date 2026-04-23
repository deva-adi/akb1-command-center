// PyramidChart.tsx
// Provided verbatim by Adi on 2026-04-22 during M7.6 scoping. Do not
// edit the visual logic here — changes belong in the wrapper. Call
// sites adapt /pyramid rows into the expected input shape:
//
//   { tier, actual_weight, actual_headcount, rate, utilisation }
//
// where `utilisation` is a 0..1 fraction (not a percentage).
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ResponsiveContainer,
  LabelList,
} from "recharts";

const TIER_COLOURS: Record<string, string> = {
  Senior: "#1E3A5F",
  Mid: "#2E6DA4",
  Junior: "#6BAED6",
};

const safeWeight = (w: number) => Math.max(0, Math.min(w, 2));

/* eslint-disable @typescript-eslint/no-explicit-any */
const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #E2E8F0",
        padding: "8px 12px",
        borderRadius: 6,
        fontSize: 13,
      }}
    >
      <p style={{ fontWeight: 600, marginBottom: 4 }}>{d.tier}</p>
      <p>
        Headcount: <strong>{d.headcount}</strong>
      </p>
      <p>
        Blended rate: <strong>${d.rate}/hr</strong>
      </p>
      <p>
        Utilisation: <strong>{d.utilPct}%</strong>
      </p>
      <p>
        Approx revenue weight: <strong>${d.approxRevenue}K</strong>
      </p>
    </div>
  );
};
/* eslint-enable @typescript-eslint/no-explicit-any */

export type PyramidChartInput = {
  tier: string;
  actual_weight: number;
  actual_headcount: number;
  rate: number;
  utilisation: number;
};

export function PyramidChart({
  data,
  programmeRevenue,
  onBarClick,
}: {
  data: PyramidChartInput[];
  programmeRevenue: number;
  onBarClick?: (tier: string) => void;
}) {
  const chartData = data.map((t) => ({
    tier: t.tier,
    approxRevenue: Math.round((safeWeight(t.actual_weight) * programmeRevenue) / 1000),
    headcount: t.actual_headcount,
    rate: t.rate,
    utilPct: Math.round(t.utilisation * 100),
  }));

  return (
    <div data-testid="pyramid-chart">
      <ResponsiveContainer width="100%" height={160}>
        <BarChart
          layout="vertical"
          data={chartData}
          margin={{ top: 8, right: 80, bottom: 8, left: 64 }}
          onClick={(state: { activePayload?: Array<{ payload: { tier: string } }> }) => {
            const tier = state?.activePayload?.[0]?.payload?.tier;
            if (tier && onBarClick) onBarClick(tier);
          }}
        >
          <XAxis
            type="number"
            tickFormatter={(v) => `$${v}K`}
            tick={{ fontSize: 11, fill: "#64748B" }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="tier"
            tick={{ fontSize: 12, fill: "#1E3A5F", fontWeight: 600 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="approxRevenue" radius={[0, 4, 4, 0]} maxBarSize={36}>
            {chartData.map((entry) => (
              <Cell
                key={entry.tier}
                fill={TIER_COLOURS[entry.tier] ?? "#94A3B8"}
              />
            ))}
            <LabelList
              dataKey="headcount"
              position="right"
              formatter={(v: number) => `${v} HC`}
              style={{ fontSize: 11, fill: "#64748B" }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p
        style={{
          fontSize: 11,
          color: "#94A3B8",
          marginTop: 4,
          fontStyle: "italic",
        }}
        data-testid="pyramid-chart-footnote"
      >
        Bar width = actual tier weight × programme revenue. Per-tier gross
        margin requires v5.8 per-tier cost data.
        {data.some((t) => t.actual_weight < 0 || t.actual_weight > 1.2) &&
          " Tier weight anomaly detected — see TECH_DEBT.md."}
      </p>
    </div>
  );
}
