import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
import {
  fetchPhases,
  fetchMilestones,
  fetchPhaseDeliverables,
  type PhaseDeliverable,
  type ProjectListItem,
} from "@/lib/api";
import { formatDate, type RagBucket } from "@/lib/format";

const DELIVERABLE_STATUS_TONE: Record<string, RagBucket | "neutral"> = {
  Completed: "green",
  "In Progress": "amber",
  Pending: "neutral",
  Blocked: "red",
};

const DELIVERABLE_TYPE_TONE: Record<string, RagBucket | "neutral"> = {
  doc: "neutral",
  artefact: "neutral",
  "sign-off": "amber",
  build: "neutral",
  review: "amber",
};

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

export function WaterfallView({ project, programmeCode }: { project: ProjectListItem; programmeCode?: string }) {
  const navigate = useNavigate();
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
  const deliverables = useQuery({
    queryKey: ["phase-deliverables", project.id],
    queryFn: () => fetchPhaseDeliverables(project.id),
  });

  const deliverablesByPhase = useMemo(() => {
    const map = new Map<number, PhaseDeliverable[]>();
    for (const d of deliverables.data ?? []) {
      const list = map.get(d.phase_id) ?? [];
      list.push(d);
      map.set(d.phase_id, list);
    }
    return map;
  }, [deliverables.data]);

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
                <div
                  role="button"
                  tabIndex={0}
                  onClick={() => setExpandedPhase(isOpen ? null : phase.id)}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setExpandedPhase(isOpen ? null : phase.id); } }}
                  aria-expanded={isOpen}
                  className="grid w-full gap-2 py-3 text-left md:grid-cols-[1fr_auto_auto] hover:bg-ice-50 cursor-pointer"
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
                  <div className="flex flex-col items-end gap-2 min-w-[140px]" onClick={(e) => e.stopPropagation()}>
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
                      onClick={() => navigate(programmeCode ? `/delivery?programme=${programmeCode}` : '/delivery')}
                    />
                    {varianceDays !== null ? (
                      <MetricCard
                        metricId="schedule_variance_days"
                        value={varianceDays > 0 ? `+${varianceDays}d slip` : `${Math.abs(varianceDays)}d ahead`}
                        tone={varianceDays > 7 ? "red" : varianceDays > 0 ? "amber" : "green"}
                        className="w-full"
                        onClick={() => navigate(programmeCode ? `/delivery?programme=${programmeCode}` : '/delivery')}
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
                </div>
                {isOpen ? (
                  <div className="pb-3 pl-4">
                    <dl className="grid grid-cols-2 gap-3 text-sm md:grid-cols-3">
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
                    <PhaseDeliverablesBlock
                      deliverables={deliverablesByPhase.get(phase.id) ?? []}
                      phaseName={phase.phase_name}
                      phaseCompletionPct={phase.percent_complete ?? 0}
                      loading={deliverables.isLoading}
                    />
                    {programmeCode && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        <span className="text-xs text-navy/50 self-center">Open in:</span>
                        <Link to={`/delivery?programme=${programmeCode}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">Delivery Health</Link>
                        <Link to={`/raid?programme=${programmeCode}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">Risk Register</Link>
                      </div>
                    )}
                  </div>
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
                <div
                  role="button"
                  tabIndex={0}
                  onClick={() => setExpandedMilestone(isOpen ? null : m.id)}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setExpandedMilestone(isOpen ? null : m.id); } }}
                  aria-expanded={isOpen}
                  className="flex w-full items-center justify-between gap-3 px-3 py-2 text-left transition hover:bg-ice-50 cursor-pointer"
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
                      <div onClick={(e) => e.stopPropagation()}>
                        <MetricCard
                          metricId="milestone_slip"
                          value={slipDays > 0 ? `+${slipDays}d` : `${slipDays}d`}
                          tone={slipDays > 5 ? "red" : slipDays > 0 ? "amber" : "green"}
                          className="px-2 py-1"
                          onClick={() => navigate(programmeCode ? `/raid?programme=${programmeCode}` : '/raid')}
                        />
                      </div>
                    ) : null}
                    {isOpen ? (
                      <ChevronUp className="size-4 text-navy/40" aria-hidden="true" />
                    ) : (
                      <ChevronDown className="size-4 text-navy/40" aria-hidden="true" />
                    )}
                  </div>
                </div>
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
                    {programmeCode && (
                      <div className="md:col-span-3 flex flex-wrap gap-2 mt-2">
                        <span className="text-xs text-navy/50 self-center">Open in:</span>
                        <Link to={`/raid?programme=${programmeCode}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">Risk Register</Link>
                        <Link to={`/delivery?programme=${programmeCode}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">Delivery Health</Link>
                      </div>
                    )}
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

type DeliverableFilter = "all" | "Completed" | "In Progress" | "Pending" | "Blocked";

function PhaseDeliverablesBlock({
  deliverables,
  phaseName,
  phaseCompletionPct,
  loading,
}: {
  deliverables: PhaseDeliverable[];
  phaseName: string;
  phaseCompletionPct: number;
  loading: boolean;
}) {
  const [filter, setFilter] = useState<DeliverableFilter>("all");

  const totals = useMemo(() => {
    const completed = deliverables.filter((d) => d.status === "Completed").length;
    const inProgress = deliverables.filter((d) => d.status === "In Progress").length;
    const pending = deliverables.filter((d) => d.status === "Pending").length;
    const blocked = deliverables.filter((d) => d.status === "Blocked").length;
    const countPct = deliverables.length > 0
      ? Math.round((completed / deliverables.length) * 100)
      : 0;
    const totalPlannedEffort = deliverables.reduce((s, d) => s + (d.effort_days_planned ?? 0), 0);
    const completedEffort = deliverables
      .filter((d) => d.status === "Completed")
      .reduce((s, d) => s + (d.effort_days_planned ?? 0), 0);
    const effortPct = totalPlannedEffort > 0
      ? Math.round((completedEffort / totalPlannedEffort) * 100)
      : 0;
    return { completed, inProgress, pending, blocked, countPct, effortPct };
  }, [deliverables]);

  const filtered = useMemo(
    () => filter === "all" ? deliverables : deliverables.filter((d) => d.status === filter),
    [filter, deliverables],
  );

  const plannedSum = filtered.reduce((s, d) => s + (d.effort_days_planned ?? 0), 0);
  const actualSum = filtered.reduce((s, d) => s + (d.effort_days_actual ?? 0), 0);

  if (loading) {
    return <p className="mt-3 text-xs text-navy/50">Loading deliverables…</p>;
  }

  if (deliverables.length === 0) {
    return (
      <p className="mt-3 text-xs italic text-navy/50">
        No deliverables seeded for this phase yet. L5 work-item traceability
        lands when phase_deliverables are loaded via CSV import or seeding.
      </p>
    );
  }

  // Compare phase header % against BOTH count-based and effort-weighted
  // completion. Effort-weighted is usually the closer match because a phase's
  // percent_complete is typically weighted by effort, not by item count.
  const header = Math.round(phaseCompletionPct);
  const countDelta = Math.abs(totals.countPct - header);
  const effortDelta = Math.abs(totals.effortPct - header);
  const mismatch = countDelta > 10 && effortDelta > 10;
  const reconcileNote = mismatch
    ? ` · ⚠ header ${header}% but items=${totals.countPct}% · effort=${totals.effortPct}%`
    : ` · reconciles to ${totals.countPct}% of items · ${totals.effortPct}% of effort`;

  return (
    <div className="mt-3 rounded-lg border border-navy/15 bg-navy/[0.02] p-3">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs font-semibold text-navy">
          {phaseName} — deliverables ({deliverables.length})
          <span className="ml-1 font-normal text-navy/60">{reconcileNote}</span>
        </p>
        <div className="flex flex-wrap gap-1">
          {(["all", "Completed", "In Progress", "Pending", "Blocked"] as DeliverableFilter[]).map((f) => {
            const count = f === "all" ? deliverables.length
              : f === "Completed" ? totals.completed
              : f === "In Progress" ? totals.inProgress
              : f === "Pending" ? totals.pending
              : totals.blocked;
            const isActive = filter === f;
            const tone =
              f === "Completed" ? "bg-success-50 text-success-700"
              : f === "In Progress" ? "bg-amber-50 text-amber-800"
              : f === "Blocked" ? "bg-danger-50 text-danger-700"
              : "bg-ice-50 text-navy";
            return (
              <button
                key={f}
                type="button"
                onClick={() => setFilter(f)}
                className={`rounded-full px-2 py-0.5 text-[10px] transition ${
                  isActive ? "bg-navy text-white" : `${tone} hover:opacity-80`
                }`}
              >
                {f} ({count})
              </button>
            );
          })}
        </div>
      </div>
      <div className="overflow-x-auto rounded border border-navy/10">
        <table className="w-full text-xs">
          <thead>
            <tr className="bg-navy/5 text-left text-navy/60">
              <th className="px-2 py-1.5 font-medium">Type</th>
              <th className="px-2 py-1.5 font-medium">Title</th>
              <th className="px-2 py-1.5 font-medium">Owner</th>
              <th className="px-2 py-1.5 font-medium">Planned</th>
              <th className="px-2 py-1.5 font-medium">Actual</th>
              <th className="px-2 py-1.5 font-medium">Effort (pl / ac)</th>
              <th className="px-2 py-1.5 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-navy/5">
            {filtered.map((d) => (
              <tr key={d.id} className="bg-white">
                <td className="px-2 py-1.5">
                  <Badge tone={DELIVERABLE_TYPE_TONE[d.deliverable_type ?? ""] ?? "neutral"}>
                    {d.deliverable_type ?? "—"}
                  </Badge>
                </td>
                <td className="px-2 py-1.5 font-medium text-navy">{d.title}</td>
                <td className="px-2 py-1.5 text-navy/80">{d.owner ?? "—"}</td>
                <td className="px-2 py-1.5 font-mono text-navy/70">{formatDate(d.planned_end)}</td>
                <td className="px-2 py-1.5 font-mono text-navy/70">{formatDate(d.actual_end)}</td>
                <td className="px-2 py-1.5 font-mono text-navy/70">
                  {d.effort_days_planned?.toFixed(1) ?? "—"} / {d.effort_days_actual?.toFixed(1) ?? "—"}
                </td>
                <td className="px-2 py-1.5">
                  <Badge tone={DELIVERABLE_STATUS_TONE[d.status] ?? "neutral"}>
                    {d.status}
                  </Badge>
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="bg-navy/5 font-semibold text-navy">
              <td className="px-2 py-1.5" colSpan={5}>
                {filter === "all" ? "All" : filter} · {filtered.length} items
              </td>
              <td className="px-2 py-1.5 font-mono">
                {plannedSum.toFixed(1)}d / {actualSum.toFixed(1)}d
              </td>
              <td />
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
}
