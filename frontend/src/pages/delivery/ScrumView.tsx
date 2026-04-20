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
import { ChevronDown, ChevronUp } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { fetchSprints, type ProjectListItem } from "@/lib/api";
import { formatDate } from "@/lib/format";

export function ScrumView({ project }: { project: ProjectListItem }) {
  const [expandedSprint, setExpandedSprint] = useState<number | null>(null);
  const { data, isLoading, error } = useQuery({
    queryKey: ["sprints", project.id],
    queryFn: () => fetchSprints(project.id),
  });

  if (isLoading) return <p className="text-sm text-navy/60">Loading sprints…</p>;
  if (error)
    return (
      <p className="text-sm text-danger-600">{(error as Error).message}</p>
    );
  if (!data || data.length === 0) {
    return (
      <p className="text-sm text-navy/60">
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

  return (
    <div className="flex flex-col gap-4">
      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <SprintStat label="Last sprint" value={`#${lastSprint.sprint_number ?? "?"}`} />
        <SprintStat
          label="Velocity"
          value={`${(lastSprint.velocity ?? 0).toFixed(0)} pts`}
          sub={`avg ${avgVelocity.toFixed(0)}`}
        />
        <SprintStat
          label="Defects found"
          value={`${lastSprint.defects_found ?? 0}`}
        />
        <SprintStat
          label="Rework hrs"
          value={`${(lastSprint.rework_hours ?? 0).toFixed(0)}h`}
        />
      </section>

      <Card>
        <CardHeader
          title="Planned vs completed points"
          subtitle="Each bar pair is one sprint"
        />
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
              <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
              <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="planned" name="Planned" fill="#D5E8F0" />
              <Bar dataKey="completed" name="Completed" fill="#1B2A4A" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card>
        <CardHeader
          title="Velocity trend + quality burden"
          subtitle="Line = velocity; bars = rework hours and defects"
        />
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData} margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
              <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
              <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <YAxis yAxisId="left" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
              <YAxis
                yAxisId="right"
                orientation="right"
                stroke="#F59E0B"
                tick={{ fontSize: 12 }}
              />
              <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar
                yAxisId="right"
                dataKey="rework"
                name="Rework hrs"
                fill="#FCD8A3"
              />
              <Bar
                yAxisId="right"
                dataKey="defectsFound"
                name="Defects"
                fill="#FCA5A5"
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="velocity"
                name="Velocity"
                stroke="#1B2A4A"
                strokeWidth={2}
                dot={{ r: 3 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {project.is_ai_augmented ? (
        <Card>
          <CardHeader
            title="Dual velocity"
            subtitle={`AI augmentation level: ${project.ai_augmentation_level ?? "—"}`}
            action={
              <Badge tone="amber">AI augmented</Badge>
            }
          />
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="completed" name="Total points" fill="#1B2A4A" />
                <Bar dataKey="aiAssisted" name="AI-assisted points" fill="#F59E0B" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-2 text-xs text-navy/60">
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
                    setExpandedSprint(
                      isOpen ? null : (s.sprint_number ?? null),
                    )
                  }
                  aria-expanded={isOpen}
                  className="grid w-full grid-cols-[auto_1fr_auto] items-center gap-3 py-3 text-left text-sm transition hover:bg-ice-50"
                >
                  <span className="font-mono text-xs text-navy/60">
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
                    <DetailCell
                      label="Rework"
                      value={`${(s.rework_hours ?? 0).toFixed(1)}h`}
                    />
                    <DetailCell
                      label="Defects found / fixed"
                      value={`${s.defects_found ?? 0} / ${s.defects_fixed ?? 0}`}
                    />
                    <DetailCell
                      label="AI-assisted"
                      value={`${s.ai_assisted_points} pts`}
                    />
                    <DetailCell
                      label="Estimation"
                      value={s.estimation_unit}
                    />
                    <DetailCell
                      label="Iteration type"
                      value={s.iteration_type}
                    />
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

function DetailCell({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="kpi-label">{label}</span>
      <span className="font-mono text-sm text-navy">{value}</span>
    </div>
  );
}

function SprintStat({
  label,
  value,
  sub,
}: {
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <div className="rounded border border-ice-100 bg-white px-3 py-2">
      <span className="kpi-label">{label}</span>
      <p className="font-mono text-xl font-semibold text-navy">{value}</p>
      {sub ? <p className="text-xs text-navy/60">{sub}</p> : null}
    </div>
  );
}
