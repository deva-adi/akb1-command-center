import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ChevronDown, ChevronUp, X } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
import {
  fetchSprints,
  fetchBacklogItems,
  type Sprint,
  type BacklogItem,
  type ProjectListItem,
} from "@/lib/api";
import { formatDate } from "@/lib/format";

export function ScrumView({ project }: { project: ProjectListItem }) {
  const [expandedSprint, setExpandedSprint] = useState<number | null>(null);
  const [drillSprint, setDrillSprint] = useState<string | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ["sprints", project.id],
    queryFn: () => fetchSprints(project.id),
  });

  if (isLoading) return <p className="text-sm text-navy/70">Loading sprints…</p>;
  if (error)
    return (
      <p className="text-sm text-danger-600">{(error as Error).message}</p>
    );
  if (!data || data.length === 0) {
    return (
      <p className="text-sm text-navy/70">
        No sprint data seeded for this project.
      </p>
    );
  }

  const sprints = data.slice().sort(
    (a, b) => (a.sprint_number ?? 0) - (b.sprint_number ?? 0),
  );
  const chartData = sprints.map((s) => ({
    sprint: `#${s.sprint_number ?? "?"}`,
    planned: s.planned_points ?? 0,
    completed: s.completed_points ?? 0,
    velocity: s.velocity ?? 0,
    rework: s.rework_hours ?? 0,
    defectsFound: s.defects_found ?? 0,
    aiAssisted: s.ai_assisted_points,
  }));

  const lastSprint = sprints[sprints.length - 1];
  const avgVelocity =
    sprints.reduce((sum, s) => sum + (s.velocity ?? 0), 0) / sprints.length;

  function handleChartClick(payload: { activeLabel?: string } | null) {
    const label = payload?.activeLabel ?? null;
    if (!label) return;
    setDrillSprint((prev) => (prev === label ? null : label));
  }

  const drillSprintData = drillSprint
    ? sprints.find((s) => `#${s.sprint_number}` === drillSprint) ?? null
    : null;

  return (
    <div className="flex flex-col gap-4">
      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <MetricCard label="Last sprint" value={`#${lastSprint.sprint_number ?? "?"}`} />
        <MetricCard
          metricId="velocity"
          value={`${(lastSprint.velocity ?? 0).toFixed(0)} pts`}
          sub={`avg ${avgVelocity.toFixed(0)}`}
        />
        <MetricCard
          metricId="defects"
          value={`${lastSprint.defects_found ?? 0}`}
        />
        <MetricCard
          metricId="rework_hours"
          value={`${(lastSprint.rework_hours ?? 0).toFixed(0)}h`}
        />
      </section>

      <Card>
        <CardHeader
          title="Planned vs completed points"
          subtitle="Click any bar to drill into that sprint's full detail"
        />
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 8, right: 20, left: 0, bottom: 8 }}
              onClick={handleChartClick}
              style={{ cursor: "pointer" }}
            >
              <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
              <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <Tooltip
                contentStyle={{ border: "1px solid #D5E8F0" }}
                labelFormatter={(l) => `${l} — click bar to see detail`}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="planned" name="Planned" fill="#D5E8F0" />
              <Bar dataKey="completed" name="Completed" fill="#1B2A4A" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        {drillSprintData && (
          <SprintDrillPanel
            sprint={drillSprintData}
            onClose={() => setDrillSprint(null)}
          />
        )}
      </Card>

      <Card>
        <CardHeader
          title="Velocity trend + quality burden"
          subtitle="Click any bar or point to drill into that sprint's quality data"
        />
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart
              data={chartData}
              margin={{ top: 8, right: 20, left: 0, bottom: 8 }}
              onClick={handleChartClick}
              style={{ cursor: "pointer" }}
            >
              <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
              <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <YAxis yAxisId="left" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <YAxis
                yAxisId="right"
                orientation="right"
                stroke="#F59E0B"
                tick={{ fontSize: 12 }}
              />
              <Tooltip
                contentStyle={{ border: "1px solid #D5E8F0" }}
                labelFormatter={(l) => `${l} — click to drill down`}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar yAxisId="right" dataKey="rework" name="Rework hrs" fill="#FCD8A3" />
              <Bar yAxisId="right" dataKey="defectsFound" name="Defects" fill="#FCA5A5" />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="velocity"
                name="Velocity"
                stroke="#1B2A4A"
                strokeWidth={2}
                dot={{ r: 4, style: { cursor: "pointer" } }}
                activeDot={{ r: 6 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
        {drillSprintData && (
          <SprintDrillPanel
            sprint={drillSprintData}
            onClose={() => setDrillSprint(null)}
          />
        )}
      </Card>

      {project.is_ai_augmented ? (
        <Card>
          <CardHeader
            title="Dual velocity"
            subtitle={`AI augmentation level: ${project.ai_augmentation_level ?? "—"} — click any bar to drill into sprint`}
            action={<Badge tone="amber">AI augmented</Badge>}
          />
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{ top: 8, right: 20, left: 0, bottom: 8 }}
                onClick={handleChartClick}
                style={{ cursor: "pointer" }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{ border: "1px solid #D5E8F0" }}
                  labelFormatter={(l) => `${l} — click to drill down`}
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="completed" name="Total points" fill="#1B2A4A" />
                <Bar dataKey="aiAssisted" name="AI-assisted points" fill="#F59E0B" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          {drillSprintData && (
            <SprintDrillPanel
              sprint={drillSprintData}
              onClose={() => setDrillSprint(null)}
            />
          )}
          <p className="mt-2 text-xs text-navy/70">
            Track AI-assisted points alongside standard velocity so trust-score
            and quality-parity dashboards in Tab 7 stay honest.
          </p>
        </Card>
      ) : null}

      <Card>
        <CardHeader
          title="Sprint ledger"
          subtitle="Click a sprint to expand full detail"
        />
        <ul className="flex flex-col divide-y divide-ice-100">
          {sprints.map((s) => {
            const isOpen = expandedSprint === s.sprint_number;
            const burndownPct =
              s.planned_points && s.planned_points > 0
                ? Math.round(((s.completed_points ?? 0) / s.planned_points) * 100)
                : 0;
            return (
              <li key={s.id}>
                <button
                  type="button"
                  onClick={() =>
                    setExpandedSprint(isOpen ? null : (s.sprint_number ?? null))
                  }
                  aria-expanded={isOpen}
                  className="grid w-full grid-cols-[auto_1fr_auto] items-center gap-3 py-3 text-left text-sm transition hover:bg-ice-50"
                >
                  <span className="font-mono text-xs text-navy/70">
                    Sprint #{s.sprint_number ?? "?"}
                  </span>
                  <span>
                    {s.completed_points ?? 0} / {s.planned_points ?? 0} pts ·{" "}
                    {s.defects_found ?? 0} defects · {burndownPct}% of plan
                  </span>
                  {isOpen ? (
                    <ChevronUp className="size-4 text-navy/40" aria-hidden="true" />
                  ) : (
                    <ChevronDown className="size-4 text-navy/40" aria-hidden="true" />
                  )}
                </button>
                {isOpen ? (
                  <dl className="grid grid-cols-2 gap-3 pb-3 pl-4 text-sm md:grid-cols-4">
                    <DetailCell
                      label="Dates"
                      value={`${formatDate(s.start_date)} → ${formatDate(s.end_date)}`}
                    />
                    <DetailCell label="Team size" value={`${s.team_size ?? "—"}`} />
                    <DetailCell label="Velocity" value={`${(s.velocity ?? 0).toFixed(0)} pts`} />
                    <DetailCell label="Rework" value={`${(s.rework_hours ?? 0).toFixed(1)}h`} />
                    <DetailCell
                      label="Defects found / fixed"
                      value={`${s.defects_found ?? 0} / ${s.defects_fixed ?? 0}`}
                    />
                    <DetailCell label="AI-assisted" value={`${s.ai_assisted_points} pts`} />
                    <DetailCell label="Estimation" value={s.estimation_unit} />
                    <DetailCell label="Iteration type" value={s.iteration_type} />
                  </dl>
                ) : null}
              </li>
            );
          })}
        </ul>
      </Card>
    </div>
  );
}

// ---------- Sprint drill panel (Level 4) + Story table (Level 5) ----------

type StoryFilter = "planned" | "completed" | "velocity" | "ai" | "rework" | null;

function SprintDrillPanel({
  sprint,
  onClose,
}: {
  sprint: Sprint;
  onClose: () => void;
}) {
  const [storyFilter, setStoryFilter] = useState<StoryFilter>(null);

  const burndownPct =
    sprint.planned_points && sprint.planned_points > 0
      ? Math.round(((sprint.completed_points ?? 0) / sprint.planned_points) * 100)
      : 0;
  const shortfall = (sprint.planned_points ?? 0) - (sprint.completed_points ?? 0);
  const aiPct =
    sprint.completed_points && sprint.completed_points > 0
      ? ((sprint.ai_assisted_points / sprint.completed_points) * 100).toFixed(0)
      : "0";

  const { data: backlogItems, isLoading: backlogLoading } = useQuery({
    queryKey: ["backlog", sprint.project_id, sprint.sprint_number],
    queryFn: () =>
      sprint.project_id != null
        ? fetchBacklogItems(sprint.project_id, sprint.sprint_number ?? undefined)
        : Promise.resolve([]),
    enabled: storyFilter !== null && sprint.project_id != null,
  });

  function toggleFilter(f: StoryFilter) {
    setStoryFilter((prev) => (prev === f ? null : f));
  }

  const filteredItems = (backlogItems ?? []).filter((item) => {
    if (storyFilter === "planned") return item.status !== "added";
    if (storyFilter === "completed") return item.status === "completed" || item.status === "added";
    if (storyFilter === "velocity") return item.status === "completed" || item.status === "added";
    if (storyFilter === "ai") return item.is_ai_assisted;
    if (storyFilter === "rework") return item.rework_hours > 0;
    return true;
  });

  return (
    <div className="mt-3 rounded-lg border border-navy/20 bg-navy/[0.03] p-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-navy">
            Sprint #{sprint.sprint_number} — Level 4 detail
          </p>
          <p className="text-xs text-navy/60">
            {formatDate(sprint.start_date)} → {formatDate(sprint.end_date)} ·{" "}
            {sprint.iteration_type} · {sprint.estimation_unit}
          </p>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1 hover:bg-ice-100"
          aria-label="Close sprint detail"
        >
          <X className="size-3.5 text-navy/60" />
        </button>
      </div>

      <dl className="mt-3 grid grid-cols-2 gap-3 md:grid-cols-4">
        <MetricCard
          metricId="planned_points"
          value={`${sprint.planned_points ?? 0}`}
          tone="neutral"
          active={storyFilter === "planned"}
          onClick={() => toggleFilter("planned")}
          drillFilter="planned"
        />
        <MetricCard
          metricId="completed_points"
          value={`${sprint.completed_points ?? 0}`}
          tone={burndownPct >= 90 ? "green" : burndownPct >= 70 ? "amber" : "red"}
          active={storyFilter === "completed"}
          onClick={() => toggleFilter("completed")}
          drillFilter="completed"
        />
        <MetricCard
          metricId="burndown_pct"
          value={`${burndownPct}%`}
          tone={burndownPct >= 90 ? "green" : burndownPct >= 70 ? "amber" : "red"}
        />
        <MetricCard
          metricId="shortfall"
          value={shortfall > 0 ? `${shortfall} pts behind` : "On target"}
          tone={shortfall > 0 ? "red" : "green"}
        />
        <MetricCard
          metricId="velocity"
          value={`${(sprint.velocity ?? 0).toFixed(0)} pts`}
          tone="neutral"
          active={storyFilter === "velocity"}
          onClick={() => toggleFilter("velocity")}
          drillFilter="completed"
        />
        <MetricCard
          metricId="team_size"
          value={`${sprint.team_size ?? "—"} people`}
          tone="neutral"
        />
        <MetricCard
          metricId="rework_hours"
          value={`${(sprint.rework_hours ?? 0).toFixed(1)}h`}
          tone={(sprint.rework_hours ?? 0) > 20 ? "red" : (sprint.rework_hours ?? 0) > 10 ? "amber" : "green"}
          active={storyFilter === "rework"}
          onClick={() => toggleFilter("rework")}
          drillFilter="rework"
        />
        <MetricCard
          metricId="defects"
          value={`${sprint.defects_found ?? 0} found · ${sprint.defects_fixed ?? 0} fixed`}
          tone={(sprint.defects_found ?? 0) > (sprint.defects_fixed ?? 0) ? "amber" : "green"}
        />
        <MetricCard
          metricId="ai_assisted_points"
          value={`${sprint.ai_assisted_points} pts (${aiPct}% of completed)`}
          tone="neutral"
          active={storyFilter === "ai"}
          onClick={() => toggleFilter("ai")}
          drillFilter="ai_assisted"
        />
      </dl>

      {storyFilter !== null && (
        <div className="mt-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-navy/60">
            Level 5 · Story / Task breakdown — {filteredItems.length} items
            {backlogLoading && " (loading…)"}
          </p>
          <BacklogItemsTable items={filteredItems} />
        </div>
      )}

      <p className="mt-3 text-xs text-navy/50">
        Level 4 of 5 · Click any metric above to drill into individual stories/tasks
      </p>
    </div>
  );
}

function BacklogItemsTable({ items }: { items: BacklogItem[] }) {
  if (items.length === 0) {
    return <p className="text-xs text-navy/50 italic">No items match this filter.</p>;
  }

  const totalPts = items.reduce((s, i) => s + (i.story_points ?? 0), 0);
  const totalRework = items.reduce((s, i) => s + i.rework_hours, 0);

  const typeBadge = (t: string) => {
    if (t === "bug") return "red";
    if (t === "spike") return "amber";
    if (t === "task") return "neutral";
    return "neutral";
  };

  const statusBadge = (s: string): "green" | "amber" | "red" | "neutral" => {
    if (s === "completed") return "green";
    if (s === "added") return "green";
    if (s === "carried_over") return "amber";
    return "neutral";
  };

  return (
    <div className="overflow-x-auto rounded border border-navy/10">
      <table className="w-full text-xs">
        <thead>
          <tr className="bg-navy/5 text-left text-navy/60">
            <th className="px-2 py-1.5 font-medium">Type</th>
            <th className="px-2 py-1.5 font-medium">Title</th>
            <th className="px-2 py-1.5 font-medium">Pts</th>
            <th className="px-2 py-1.5 font-medium">Assignee</th>
            <th className="px-2 py-1.5 font-medium">Status</th>
            <th className="px-2 py-1.5 font-medium">AI</th>
            <th className="px-2 py-1.5 font-medium">Defects</th>
            <th className="px-2 py-1.5 font-medium">Rework h</th>
            <th className="px-2 py-1.5 font-medium">Priority</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-navy/5">
          {items.map((item) => (
            <tr key={item.id} className="bg-white hover:bg-ice-50">
              <td className="px-2 py-1.5">
                <Badge tone={typeBadge(item.item_type) as "green" | "amber" | "red" | "neutral"}>
                  {item.item_type}
                </Badge>
              </td>
              <td className="px-2 py-1.5 font-medium text-navy">{item.title}</td>
              <td className="px-2 py-1.5 font-mono text-navy">{item.story_points ?? "—"}</td>
              <td className="px-2 py-1.5 text-navy/80">{item.assignee ?? "—"}</td>
              <td className="px-2 py-1.5">
                <Badge tone={statusBadge(item.status)}>{item.status}</Badge>
              </td>
              <td className="px-2 py-1.5">
                {item.is_ai_assisted ? <Badge tone="amber">AI</Badge> : <span className="text-navy/30">—</span>}
              </td>
              <td className="px-2 py-1.5 font-mono text-navy">{item.defects_raised}</td>
              <td className="px-2 py-1.5 font-mono text-navy">{item.rework_hours.toFixed(1)}</td>
              <td className="px-2 py-1.5">
                <Badge
                  tone={
                    item.priority === "critical"
                      ? "red"
                      : item.priority === "high"
                        ? "amber"
                        : "neutral"
                  }
                >
                  {item.priority ?? "—"}
                </Badge>
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="bg-navy/5 font-semibold text-navy">
            <td className="px-2 py-1.5" colSpan={2}>
              Totals ({items.length} items)
            </td>
            <td className="px-2 py-1.5 font-mono">{totalPts}</td>
            <td colSpan={4} />
            <td className="px-2 py-1.5 font-mono">{totalRework.toFixed(1)}</td>
            <td />
          </tr>
        </tfoot>
      </table>
    </div>
  );
}

// ---------- helpers ----------

function DetailCell({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="kpi-label">{label}</span>
      <span className="font-mono text-sm text-navy">{value}</span>
    </div>
  );
}
