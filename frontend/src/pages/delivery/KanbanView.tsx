import { useQuery } from "@tanstack/react-query";
import { useMemo } from "react";
import ReactECharts from "echarts-for-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { fetchFlow, type ProjectListItem } from "@/lib/api";

export function KanbanView({ project }: { project: ProjectListItem }) {
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
          subtitle="Approximate CFD built from per-week WIP and throughput"
        />
        <div className="h-80">
          <ReactECharts
            option={cfdOption}
            style={{ height: "100%", width: "100%" }}
            notMerge
          />
        </div>
        <p className="mt-2 text-xs text-navy/70">
          CFD = stacked backlog + in-progress + done. Widening bands →
          growing WIP or slowing throughput; look at the In Progress
          layer's thickness vs. Done's slope.
        </p>
      </Card>

      <Card>
        <CardHeader
          title="Cycle-time percentiles"
          subtitle="p50 / p85 / p95 per week (days)"
        />
        <div className="h-72">
          <ReactECharts
            option={cycleOption}
            style={{ height: "100%", width: "100%" }}
            notMerge
          />
        </div>
      </Card>
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
