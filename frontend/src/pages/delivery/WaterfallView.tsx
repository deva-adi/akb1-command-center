import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
import { fetchPhases, fetchMilestones, type ProjectListItem } from "@/lib/api";
import { formatDate, type RagBucket } from "@/lib/format";

const GATE_TONE: Record<string, RagBucket | "neutral"> = {
  passed: "green",
  failed: "red",
  conditional: "amber",
  pending: "neutral",
};

const STATUS_TONE: Record<string, RagBucket | "neutral"> = {
  Completed: "green",
  "In Progress": "amber",
  Pending: "neutral",
  Delayed: "red",
  "At Risk": "red",
};

export function WaterfallView({ project }: { project: ProjectListItem }) {
  const [expandedPhase, setExpandedPhase] = useState<number | null>(null);
  const [expandedMilestone, setExpandedMilestone] = useState<number | null>(null);

  const phases = useQuery({
    queryKey: ["phases", project.id],
    queryFn: () => fetchPhases(project.id),
  });
  const milestones = useQuery({
    queryKey: ["milestones", project.id],
    queryFn: () => fetchMilestones(project.id),
  });

  const isLoading = phases.isLoading || milestones.isLoading;
  const error = phases.error ?? milestones.error;

  if (isLoading)
    return <p className="text-sm text-navy/70">Loading phases + milestones…</p>;
  if (error)
    return (
      <p className="text-sm text-danger-600">{(error as Error).message}</p>
    );

  return (
    <div className="flex flex-col gap-4">
      <Card>
        <CardHeader
          title="Phase timeline"
          subtitle="Planned vs actual per phase with gate status"
        />
        <ol className="flex flex-col divide-y divide-ice-100">
          {(phases.data ?? []).map((phase) => {
            const plannedDurationMs =
              phase.planned_start && phase.planned_end
                ? new Date(phase.planned_end).getTime() -
                  new Date(phase.planned_start).getTime()
                : 0;
            const actualDurationMs =
              phase.actual_start
                ? (phase.actual_end
                    ? new Date(phase.actual_end).getTime()
                    : Date.now()) - new Date(phase.actual_start).getTime()
                : 0;
            const varianceDays =
              actualDurationMs && plannedDurationMs
                ? Math.round(
                    (actualDurationMs - plannedDurationMs) / (1000 * 60 * 60 * 24),
                  )
                : null;
            const isOpen = expandedPhase === phase.id;
            return (
              <li key={phase.id}>
                <button
                  type="button"
                  onClick={() => setExpandedPhase(isOpen ? null : phase.id)}
                  aria-expanded={isOpen}
                  className="grid w-full gap-2 py-3 text-left md:grid-cols-[1fr_auto_auto] hover:bg-ice-50"
                >
                  <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs text-navy/70">
                        {phase.phase_sequence ?? "?"}.
                      </span>
                      <span className="font-semibold">{phase.phase_name}</span>
                      <Badge
                        tone={GATE_TONE[phase.gate_status ?? "pending"] ?? "neutral"}
                      >
                        {phase.gate_status ?? "pending"}
                      </Badge>
                    </div>
                    <div className="text-xs text-navy/70">
                      Planned {formatDate(phase.planned_start)} →{" "}
                      {formatDate(phase.planned_end)}
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-2 min-w-[140px]">
                    <MetricCard
                      metricId="phase_completion"
                      value={`${(phase.percent_complete ?? 0).toFixed(0)}%`}
                      tone={
                        (phase.percent_complete ?? 0) >= 80
                          ? "green"
                          : (phase.percent_complete ?? 0) >= 60
                            ? "amber"
                            : "red"
                      }
                      className="w-full"
                    />
                    {varianceDays !== null ? (
                      <MetricCard
                        metricId="schedule_variance_days"
                        value={varianceDays > 0 ? `+${varianceDays}d slip` : `${Math.abs(varianceDays)}d ahead`}
                        tone={varianceDays > 7 ? "red" : varianceDays > 0 ? "amber" : "green"}
                        className="w-full"
                      />
                    ) : null}
                  </div>
                  <span className="self-center pr-1 text-navy/40">
                    {isOpen ? (
                      <ChevronUp className="size-4" aria-hidden="true" />
                    ) : (
                      <ChevronDown className="size-4" aria-hidden="true" />
                    )}
                  </span>
                </button>
                {isOpen ? (
                  <dl className="grid grid-cols-2 gap-3 pb-3 pl-4 text-sm md:grid-cols-3">
                    <DetailCell
                      label="Actual"
                      value={
                        phase.actual_start
                          ? `${formatDate(phase.actual_start)} → ${formatDate(phase.actual_end)}`
                          : "pending"
                      }
                    />
                    <DetailCell
                      label="Gate approver"
                      value={phase.gate_approver ?? "—"}
                    />
                    <DetailCell
                      label="Gate date"
                      value={formatDate(phase.gate_date)}
                    />
                    {phase.notes ? (
                      <div className="md:col-span-3">
                        <span className="kpi-label">Notes</span>
                        <p className="text-sm italic text-navy/80">{phase.notes}</p>
                      </div>
                    ) : null}
                  </dl>
                ) : null}
              </li>
            );
          })}
        </ol>
      </Card>

      <Card>
        <CardHeader
          title="Milestones"
          subtitle={`${milestones.data?.length ?? 0} tracked`}
        />
        <ol className="flex flex-col gap-2">
          {(milestones.data ?? []).map((m) => {
            const slipDays =
              m.actual_date && m.planned_date
                ? Math.round(
                    (new Date(m.actual_date).getTime() -
                      new Date(m.planned_date).getTime()) /
                      (1000 * 60 * 60 * 24),
                  )
                : null;
            const isOpen = expandedMilestone === m.id;
            return (
              <li
                key={m.id}
                className="rounded border border-ice-100 bg-white"
              >
                <button
                  type="button"
                  onClick={() => setExpandedMilestone(isOpen ? null : m.id)}
                  aria-expanded={isOpen}
                  className="flex w-full items-center justify-between gap-3 px-3 py-2 text-left transition hover:bg-ice-50"
                >
                  <div>
                    <p className="font-medium">{m.name}</p>
                    <p className="text-xs text-navy/70">
                      Planned {formatDate(m.planned_date)}
                      {m.actual_date
                        ? ` · Actual ${formatDate(m.actual_date)}`
                        : ""}
                      {m.owner ? ` · ${m.owner}` : ""}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge tone={STATUS_TONE[m.status] ?? "neutral"}>{m.status}</Badge>
                    {slipDays !== null && slipDays !== 0 ? (
                      <MetricCard
                        metricId="milestone_slip"
                        value={slipDays > 0 ? `+${slipDays}d` : `${slipDays}d`}
                        tone={slipDays > 5 ? "red" : slipDays > 0 ? "amber" : "green"}
                        className="px-2 py-1"
                      />
                    ) : null}
                    {isOpen ? (
                      <ChevronUp className="size-4 text-navy/40" aria-hidden="true" />
                    ) : (
                      <ChevronDown className="size-4 text-navy/40" aria-hidden="true" />
                    )}
                  </div>
                </button>
                {isOpen ? (
                  <dl className="grid grid-cols-2 gap-3 px-3 pb-3 text-sm md:grid-cols-3">
                    <DetailCell label="Status" value={m.status} />
                    <DetailCell label="Owner" value={m.owner ?? "—"} />
                    <DetailCell
                      label="Slip"
                      value={
                        slipDays === null
                          ? "—"
                          : slipDays > 0
                            ? `+${slipDays}d`
                            : `${slipDays}d`
                      }
                    />
                    {m.notes ? (
                      <div className="md:col-span-3">
                        <span className="kpi-label">Notes</span>
                        <p className="text-sm italic text-navy/80">{m.notes}</p>
                      </div>
                    ) : null}
                  </dl>
                ) : null}
              </li>
            );
          })}
        </ol>
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
