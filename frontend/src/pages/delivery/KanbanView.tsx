import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import ReactECharts from "echarts-for-react";
import { X } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { fetchFlow, type ProjectListItem } from "@/lib/api";

export function KanbanView({ project }: { project: ProjectListItem }) {
  const [selectedWeekIdx, setSelectedWeekIdx] = useState<number | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ["flow", project.id],
    queryFn: () => fetchFlow(project.id),
  });

  const sorted = useMemo(() => {
    if (!data) return [];
    return data
      .slice()
      .sort((a, b) =>
        (a.period_start ?? "").localeCompare(b.period_start ?? ""),
      );
  }, [data]);

  const cfdOption = useMemo(() => buildCfdOption(sorted), [sorted]);
  const cycleOption = useMemo(() => buildCyclePercentileOption(sorted), [sorted]);

  const chartEvents = useMemo(
    () => ({
      click: (params: { dataIndex?: number }) => {
        const idx = params.dataIndex ?? null;
        if (idx === null) return;
        setSelectedWeekIdx((prev) => (prev === idx ? null : idx));
      },
    }),
    [],
  );

  const selectedWeek = selectedWeekIdx !== null ? sorted[selectedWeekIdx] ?? null : null;

  if (isLoading) return <p className="text-sm text-navy/70">Loading flow metrics…</p>;
  if (error)
    return (
      <p className="text-sm text-danger-600">{(error as Error).message}</p>
    );
  if (sorted.length === 0) {
    return (
      <p className="text-sm text-navy/70">
        No flow metrics seeded for this project.
      </p>
    );
  }

  const latest = sorted[sorted.length - 1];
  const avgThroughput =
    sorted.reduce((sum, r) => sum + (r.throughput_items ?? 0), 0) / sorted.length;
  const wipBreach =
    latest.wip_avg !== null &&
    latest.wip_limit !== null &&
    latest.wip_avg > latest.wip_limit;

  return (
    <div className="flex flex-col gap-4">
      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <FlowStat
          label="Throughput (this wk)"
          value={`${latest.throughput_items ?? 0}`}
          sub={`avg ${avgThroughput.toFixed(1)}`}
        />
        <FlowStat
          label="WIP avg"
          value={`${(latest.wip_avg ?? 0).toFixed(1)}`}
          sub={`limit ${latest.wip_limit ?? "—"}`}
          tone={wipBreach ? "red" : "green"}
        />
        <FlowStat
          label="Cycle time p50"
          value={`${(latest.cycle_time_p50 ?? 0).toFixed(1)}d`}
          sub={`p95 ${(latest.cycle_time_p95 ?? 0).toFixed(1)}d`}
        />
        <FlowStat
          label="Blocked"
          value={`${(latest.blocked_time_hours ?? 0).toFixed(1)}h`}
        />
      </section>

      <Card>
        <CardHeader
          title="Cumulative flow diagram"
          subtitle="Click any point to drill into that week's flow metrics"
        />
        <div className="h-80">
          <ReactECharts
            option={cfdOption}
            style={{ height: "100%", width: "100%" }}
            notMerge
            onEvents={chartEvents}
          />
        </div>
        {selectedWeek && (
          <FlowDrillPanel row={selectedWeek} onClose={() => setSelectedWeekIdx(null)} />
        )}
        <p className="mt-2 text-xs text-navy/70">
          CFD = stacked backlog + in-progress + done. Widening bands →
          growing WIP or slowing throughput; look at the In Progress
          layer's thickness vs. Done's slope.
        </p>
      </Card>

      <Card>
        <CardHeader
          title="Cycle-time percentiles"
          subtitle="p50 / p85 / p95 per week (days) — click any point to drill into that week"
        />
        <div className="h-72">
          <ReactECharts
            option={cycleOption}
            style={{ height: "100%", width: "100%" }}
            notMerge
            onEvents={chartEvents}
          />
        </div>
        {selectedWeek && (
          <FlowDrillPanel row={selectedWeek} onClose={() => setSelectedWeekIdx(null)} />
        )}
      </Card>
    </div>
  );
}

// ---------- Flow drill panel ----------

type FlowRow = {
  period_start: string | null;
  throughput_items: number | null;
  wip_avg: number | null;
  wip_limit: number | null;
  cycle_time_p50: number | null;
  cycle_time_p85: number | null;
  cycle_time_p95: number | null;
  lead_time_avg: number | null;
  blocked_time_hours: number | null;
};

function FlowDrillPanel({ row, onClose }: { row: FlowRow; onClose: () => void }) {
  const wipBreach =
    row.wip_avg !== null && row.wip_limit !== null && row.wip_avg > row.wip_limit;

  return (
    <div className="mt-3 rounded-lg border border-navy/20 bg-navy/[0.03] p-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-navy">
            Week of {row.period_start?.slice(0, 10) ?? "—"} — Level 4 detail
          </p>
          <p className="text-xs text-navy/60">Flow metrics for this period</p>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1 hover:bg-ice-100"
          aria-label="Close flow detail"
        >
          <X className="size-3.5 text-navy/60" />
        </button>
      </div>

      <dl className="mt-3 grid grid-cols-2 gap-3 md:grid-cols-4">
        <FlowCell
          label="Throughput"
          value={`${row.throughput_items ?? 0} items`}
          tone="neutral"
        />
        <FlowCell
          label="WIP avg vs limit"
          value={`${(row.wip_avg ?? 0).toFixed(1)} / ${row.wip_limit ?? "—"}`}
          tone={wipBreach ? "red" : "green"}
        />
        <FlowCell
          label="Cycle time p50"
          value={`${(row.cycle_time_p50 ?? 0).toFixed(1)}d`}
          tone="neutral"
        />
        <FlowCell
          label="Cycle time p85"
          value={`${(row.cycle_time_p85 ?? 0).toFixed(1)}d`}
          tone={(row.cycle_time_p85 ?? 0) > (row.cycle_time_p50 ?? 0) * 2 ? "amber" : "neutral"}
        />
        <FlowCell
          label="Cycle time p95"
          value={`${(row.cycle_time_p95 ?? 0).toFixed(1)}d`}
          tone={(row.cycle_time_p95 ?? 0) > (row.cycle_time_p50 ?? 0) * 3 ? "red" : "neutral"}
        />
        <FlowCell
          label="Lead time avg"
          value={`${(row.lead_time_avg ?? 0).toFixed(1)}d`}
          tone="neutral"
        />
        <FlowCell
          label="Blocked time"
          value={`${(row.blocked_time_hours ?? 0).toFixed(1)}h`}
          tone={(row.blocked_time_hours ?? 0) > 8 ? "red" : (row.blocked_time_hours ?? 0) > 4 ? "amber" : "green"}
        />
      </dl>

      <p className="mt-3 text-xs text-navy/50">
        Level 4 of 4 · Lowest granularity · Raw flow metrics for this week
      </p>
    </div>
  );
}

function FlowCell({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: "green" | "amber" | "red" | "neutral";
}) {
  return (
    <div className="flex flex-col gap-1">
      <span className="kpi-label">{label}</span>
      <Badge tone={tone}>{value}</Badge>
    </div>
  );
}

function FlowStat({
  label,
  value,
  sub,
  tone = "neutral",
}: {
  label: string;
  value: string;
  sub?: string;
  tone?: "green" | "amber" | "red" | "neutral";
}) {
  return (
    <div className="rounded border border-ice-100 bg-white px-3 py-2">
      <span className="kpi-label">{label}</span>
      <div className="flex items-center gap-2">
        <p className="font-mono text-xl font-semibold text-navy">{value}</p>
        {tone !== "neutral" ? <Badge tone={tone}>·</Badge> : null}
      </div>
      {sub ? <p className="text-xs text-navy/70">{sub}</p> : null}
    </div>
  );
}

function buildCfdOption(
  rows: { period_start: string | null; throughput_items: number | null; wip_avg: number | null }[],
) {
  const weeks = rows.map((r) => weekLabel(r.period_start));
  const doneRunning: number[] = [];
  let running = 0;
  for (const r of rows) {
    running += r.throughput_items ?? 0;
    doneRunning.push(running);
  }
  const inProgress = rows.map((r) => r.wip_avg ?? 0);
  // Synthesise backlog so the topmost band expands with WIP pressure.
  const backlog = rows.map((_, i) =>
    Math.max(5, inProgress[i] * 1.3 + (i * 0.8)),
  );

  return {
    tooltip: { trigger: "axis" },
    legend: { data: ["Done (cumulative)", "In Progress", "Backlog"], bottom: 0 },
    grid: { top: 20, right: 20, bottom: 40, left: 50 },
    xAxis: { type: "category", data: weeks, boundaryGap: false },
    yAxis: { type: "value", name: "Items" },
    series: [
      {
        name: "Done (cumulative)",
        type: "line",
        stack: "cfd",
        areaStyle: { color: "#10B981", opacity: 0.8 },
        lineStyle: { width: 0 },
        symbol: "none",
        data: doneRunning,
      },
      {
        name: "In Progress",
        type: "line",
        stack: "cfd",
        areaStyle: { color: "#F59E0B", opacity: 0.7 },
        lineStyle: { width: 0 },
        symbol: "none",
        data: inProgress,
      },
      {
        name: "Backlog",
        type: "line",
        stack: "cfd",
        areaStyle: { color: "#1B2A4A", opacity: 0.15 },
        lineStyle: { width: 0 },
        symbol: "none",
        data: backlog,
      },
    ],
  };
}

function buildCyclePercentileOption(
  rows: {
    period_start: string | null;
    cycle_time_p50: number | null;
    cycle_time_p85: number | null;
    cycle_time_p95: number | null;
  }[],
) {
  const weeks = rows.map((r) => weekLabel(r.period_start));
  return {
    tooltip: { trigger: "axis" },
    legend: { data: ["p50", "p85", "p95"], bottom: 0 },
    grid: { top: 20, right: 20, bottom: 40, left: 50 },
    xAxis: { type: "category", data: weeks },
    yAxis: { type: "value", name: "Days" },
    series: [
      {
        name: "p50",
        type: "line",
        smooth: true,
        lineStyle: { color: "#10B981", width: 2 },
        itemStyle: { color: "#10B981" },
        data: rows.map((r) => r.cycle_time_p50 ?? 0),
      },
      {
        name: "p85",
        type: "line",
        smooth: true,
        lineStyle: { color: "#F59E0B", width: 2 },
        itemStyle: { color: "#F59E0B" },
        data: rows.map((r) => r.cycle_time_p85 ?? 0),
      },
      {
        name: "p95",
        type: "line",
        smooth: true,
        lineStyle: { color: "#EF4444", width: 2 },
        itemStyle: { color: "#EF4444" },
        data: rows.map((r) => r.cycle_time_p95 ?? 0),
      },
    ],
  };
}

function weekLabel(iso: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short" });
}
