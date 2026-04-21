import { Fragment, useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { AlertOctagon, ChevronDown, ChevronUp, Home, Sparkles } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { ProgrammeFilterBar } from "@/components/ProgrammeFilterBar";
import { PROGRAMME_CROSS_LINKS } from "@/components/programmeCrossLinks";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
import {
  fetchCustomerActions,
  fetchCustomerExpectations,
  fetchCustomerSatisfaction,
  fetchSlaIncidents,
  type CustomerSatisfaction,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { useCurrency } from "@/hooks/useCurrency";
import { formatDate, type RagBucket } from "@/lib/format";

function renewalTone(score: number | null): RagBucket {
  if (score === null) return "amber";
  if (score >= 80) return "green";
  if (score >= 60) return "amber";
  return "red";
}

function csatTone(score: number | null): RagBucket {
  if (score === null) return "amber";
  if (score >= 8) return "green";
  if (score >= 7) return "amber";
  return "red";
}

function npsTone(score: number | null): RagBucket {
  if (score === null) return "amber";
  if (score >= 30) return "green";
  if (score >= 0) return "amber";
  return "red";
}

export function CustomerIntelligence() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();
  const currency = useCurrency();

  const [activeProgrammeId, setActiveProgrammeId] = useState<number | null>(null);
  const [expandedAction, setExpandedAction] = useState<number | null>(null);
  const [expandedIncident, setExpandedIncident] = useState<number | null>(null);

  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );

  // Default to the programme from the URL filter, else the first programme.
  useEffect(() => {
    if (filteredProgramme) {
      setActiveProgrammeId(filteredProgramme.id);
    } else if (!activeProgrammeId && programmes.data && programmes.data.length > 0) {
      setActiveProgrammeId(programmes.data[0].id);
    }
  }, [filteredProgramme, programmes.data, activeProgrammeId]);

  const activeProgramme = useMemo(
    () => programmes.data?.find((p) => p.id === activeProgrammeId) ?? null,
    [programmes.data, activeProgrammeId],
  );

  const satisfaction = useQuery({
    queryKey: ["satisfaction", activeProgrammeId],
    queryFn: () =>
      activeProgrammeId
        ? fetchCustomerSatisfaction(activeProgrammeId)
        : Promise.resolve([] as CustomerSatisfaction[]),
    enabled: activeProgrammeId !== null,
  });
  const expectations = useQuery({
    queryKey: ["expectations", activeProgrammeId],
    queryFn: () =>
      activeProgrammeId
        ? fetchCustomerExpectations(activeProgrammeId)
        : Promise.resolve([]),
    enabled: activeProgrammeId !== null,
  });
  const actions = useQuery({
    queryKey: ["actions", activeProgrammeId],
    queryFn: () =>
      activeProgrammeId
        ? fetchCustomerActions(activeProgrammeId)
        : Promise.resolve([]),
    enabled: activeProgrammeId !== null,
  });
  const incidents = useQuery({
    queryKey: ["sla-incidents", activeProgrammeId],
    queryFn: () =>
      activeProgrammeId
        ? fetchSlaIncidents(activeProgrammeId)
        : Promise.resolve([]),
    enabled: activeProgrammeId !== null,
  });

  const handleProgrammeChange = (next: { id: number } | null) => {
    setActiveProgrammeId(next?.id ?? null);
    const params = new URLSearchParams(searchParams);
    if (next) {
      const code =
        programmes.data?.find((p) => p.id === next.id)?.code ?? "";
      if (code) {
        params.set("programme", code);
      } else {
        params.delete("programme");
      }
    } else {
      params.delete("programme");
    }
    setSearchParams(params);
  };

  const latest = useMemo(() => {
    const rows = satisfaction.data ?? [];
    return rows.length > 0 ? rows[rows.length - 1] : null;
  }, [satisfaction.data]);

  const trendData = useMemo(() => {
    return (satisfaction.data ?? []).map((r) => ({
      month: r.snapshot_date.slice(0, 7),
      monthLabel: monthLabel(r.snapshot_date),
      csat: r.csat_score,
      nps: r.nps_score,
      renewal: r.renewal_score,
    }));
  }, [satisfaction.data]);

  const radarData = useMemo(() => {
    // Aggregate by dimension (pick latest snapshot per dimension).
    const byDim = new Map<string, { expected: number; delivered: number }>();
    for (const row of expectations.data ?? []) {
      byDim.set(row.dimension, {
        expected: row.expected_score ?? 0,
        delivered: row.delivered_score ?? 0,
      });
    }
    const allDims = [
      "timeline",
      "quality",
      "communication",
      "innovation",
      "cost",
      "responsiveness",
      "stability",
    ];
    return allDims.map((dim) => {
      const row = byDim.get(dim);
      return {
        dimension: dim,
        expected: row?.expected ?? 0,
        delivered: row?.delivered ?? 0,
      };
    });
  }, [expectations.data]);

  const breadcrumbItems = [
    { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
    { label: "Customer Intelligence", to: filteredProgramme ? "/customer" : undefined },
    ...(activeProgramme ? [{ label: activeProgramme.name }] : []),
  ];

  const sourceCurrency = activeProgramme?.currency_code ?? "INR";

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumbItems} />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Customer Intelligence</h1>
        <p className="mt-1 text-sm text-navy/70">
          Will this customer renew? Where is their expectation gap widest?
          What escalations are open?
        </p>
      </div>

      <ProgrammeFilterBar
        currentRoute="/customer"
        activeProgramme={activeProgramme}
        onSelect={(next) => handleProgrammeChange(next)}
        crossLinks={PROGRAMME_CROSS_LINKS}
      />

      {!filteredProgramme ? (
        <Card>
          <CardHeader title="Pick a programme" subtitle="Customer intelligence is per-programme" />
          <div className="flex flex-wrap gap-2">
            {(programmes.data ?? []).map((p) => {
              const isActive = p.id === activeProgrammeId;
              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setActiveProgrammeId(p.id)}
                  className={`rounded-md border px-3 py-2 text-sm transition ${
                    isActive
                      ? "border-navy bg-navy text-white"
                      : "border-ice-100 bg-white text-navy hover:bg-ice-50"
                  }`}
                >
                  {p.code}
                </button>
              );
            })}
          </div>
        </Card>
      ) : null}

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <MetricCard
          metricId="csat"
          value={latest?.csat_score != null ? latest.csat_score.toFixed(1) : "—"}
          tone={csatTone(latest?.csat_score ?? null)}
          sub="0-10"
        />
        <MetricCard
          metricId="nps"
          value={latest?.nps_score != null ? latest.nps_score.toFixed(0) : "—"}
          tone={npsTone(latest?.nps_score ?? null)}
        />
        <MetricCard
          metricId="escalation_count"
          label="Open escalations"
          value={`${latest?.escalation_open ?? 0}`}
          tone={(latest?.escalation_open ?? 0) === 0 ? "green" : (latest?.escalation_open ?? 0) > 3 ? "red" : "amber"}
          sub={`total ${latest?.escalation_count ?? 0}`}
        />
        <MetricCard
          metricId="renewal_probability"
          value={latest?.renewal_score != null ? `${latest.renewal_score.toFixed(0)}%` : "—"}
          tone={renewalTone(latest?.renewal_score ?? null)}
        />
      </section>

      <Card>
        <CardHeader
          title="CSAT / NPS / Renewal trend"
          subtitle="Click any data point to drill into that programme's Risk & Audit log"
        />
        <div className="h-72">
          {trendData.length === 0 ? (
            <p className="grid h-full place-items-center text-sm text-navy/70">
              No customer-satisfaction rows yet.
            </p>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={trendData}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
                onClick={() => {
                  const code = filteredProgramme?.code
                    ?? (activeProgrammeId
                        ? programmes.data?.find((p) => p.id === activeProgrammeId)?.code
                        : undefined);
                  navigate(code ? `/raid?programme=${code}` : "/raid");
                }}
                style={{ cursor: "pointer" }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="monthLabel" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <YAxis
                  yAxisId="left"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                  domain={[0, 100]}
                />
                <YAxis
                  yAxisId="right"
                  orientation="right"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                  domain={[-100, 100]}
                />
                <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="csat"
                  name="CSAT (scaled ×10)"
                  stroke="#10B981"
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 6, style: { cursor: "pointer" } }}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="nps"
                  name="NPS"
                  stroke="#1B2A4A"
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 6, style: { cursor: "pointer" } }}
                />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="renewal"
                  name="Renewal %"
                  stroke="#F59E0B"
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 6, style: { cursor: "pointer" } }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </Card>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader
            title="Expectation gap — 7 dimensions"
            subtitle="Expected vs delivered score per ARCHITECTURE.md §4.10"
          />
          <div className="h-80">
            {radarData.every((r) => r.expected === 0 && r.delivered === 0) ? (
              <p className="grid h-full place-items-center text-sm text-navy/70">
                No expectation rows seeded for this programme.
              </p>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#D5E8F0" />
                  <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 11 }} />
                  <PolarRadiusAxis domain={[0, 10]} tick={{ fontSize: 10 }} />
                  <Radar
                    name="Expected"
                    dataKey="expected"
                    stroke="#1B2A4A"
                    fill="#1B2A4A"
                    fillOpacity={0.1}
                  />
                  <Radar
                    name="Delivered"
                    dataKey="delivered"
                    stroke="#F59E0B"
                    fill="#F59E0B"
                    fillOpacity={0.25}
                  />
                  <Legend wrapperStyle={{ fontSize: 12 }} />
                  <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
                </RadarChart>
              </ResponsiveContainer>
            )}
          </div>
        </Card>

        <Card>
          <CardHeader
            title="Communication tracker"
            subtitle="Steering cadence + action items"
          />
          {latest ? (
            <>
              <dl className="grid grid-cols-2 gap-3 text-sm md:grid-cols-4">
                <Tile
                  label="Meetings (this month)"
                  value={`${latest.steering_meetings_held ?? 0} / ${latest.steering_meetings_planned ?? 0}`}
                />
                <Tile
                  label="Action items open"
                  value={`${latest.action_items_open ?? 0}`}
                />
                <Tile
                  label="Closed"
                  value={`${latest.action_items_closed ?? 0}`}
                />
                <Tile
                  label="Escalations open"
                  value={`${latest.escalation_open}`}
                />
              </dl>
              <div className="mt-4 flex flex-col gap-2 text-sm">
                <p>
                  <span className="kpi-label">Positive themes</span>
                  <br />
                  {latest.positive_themes ?? "—"}
                </p>
                <p>
                  <span className="kpi-label">Concern themes</span>
                  <br />
                  <span className="text-danger-600">
                    {latest.concern_themes ?? "—"}
                  </span>
                </p>
              </div>
            </>
          ) : (
            <p className="text-sm text-navy/70">No communication data yet.</p>
          )}
        </Card>
      </section>

      <Card>
        <CardHeader
          title="Action items"
          subtitle={`${actions.data?.length ?? 0} tracked`}
          action={<Sparkles className="size-4 text-amber-500" aria-hidden="true" />}
        />
        {(actions.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/70">No steering-committee actions recorded.</p>
        ) : (
          <ul className="flex flex-col gap-2 text-sm">
            {(actions.data ?? []).map((a) => {
              const isOpen = expandedAction === a.id;
              return (
                <li
                  key={a.id}
                  className="rounded border border-ice-100 bg-white"
                >
                  <button
                    type="button"
                    onClick={() => setExpandedAction(isOpen ? null : a.id)}
                    aria-expanded={isOpen}
                    className="flex w-full items-center justify-between gap-3 px-3 py-2 text-left transition hover:bg-ice-50"
                  >
                    <div>
                      <p className="font-medium">{a.description}</p>
                      <p className="text-xs text-navy/70">
                        Meeting {formatDate(a.meeting_date)}
                        {a.owner ? ` · ${a.owner}` : ""}
                        {a.due_date ? ` · due ${formatDate(a.due_date)}` : ""}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      {a.escalated ? (
                        <Badge tone="red">
                          <AlertOctagon className="size-3" /> escalated
                        </Badge>
                      ) : null}
                      <Badge tone={a.priority === "P1" ? "red" : a.priority === "P2" ? "amber" : "neutral"}>
                        {a.priority ?? "—"}
                      </Badge>
                      <Badge
                        tone={
                          a.status === "Closed"
                            ? "green"
                            : a.status === "Open"
                              ? "amber"
                              : "neutral"
                        }
                      >
                        {a.status}
                      </Badge>
                      {isOpen ? (
                        <ChevronUp className="size-4 text-navy/40" aria-hidden="true" />
                      ) : (
                        <ChevronDown className="size-4 text-navy/40" aria-hidden="true" />
                      )}
                    </div>
                  </button>
                  {isOpen ? (
                    <dl className="grid grid-cols-2 gap-3 px-3 pb-3 text-xs md:grid-cols-4">
                      <Detail label="Priority" value={a.priority ?? "—"} />
                      <Detail label="Owner" value={a.owner ?? "—"} />
                      <Detail label="Due" value={formatDate(a.due_date)} />
                      <Detail label="Closed" value={formatDate(a.closed_date)} />
                      {a.resolution_notes ? (
                        <div className="md:col-span-4">
                          <span className="kpi-label">Resolution</span>
                          <p className="text-navy/80 italic">{a.resolution_notes}</p>
                        </div>
                      ) : null}
                    </dl>
                  ) : null}
                </li>
              );
            })}
          </ul>
        )}
      </Card>

      <Card>
        <CardHeader
          title="SLA incident ledger"
          subtitle="Breaches incur penalty amounts — shown in the active base currency"
        />
        {(incidents.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/70">
            No SLA incidents recorded for this programme.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-navy/70">
                  <th className="py-2">ID</th>
                  <th>Priority</th>
                  <th>Summary</th>
                  <th className="text-right">Response</th>
                  <th className="text-right">Resolution</th>
                  <th className="text-right">Penalty</th>
                  <th className="text-right">Breach?</th>
                </tr>
              </thead>
              <tbody>
                {(incidents.data ?? []).map((i) => {
                  const isOpen = expandedIncident === i.id;
                  return (
                    <Fragment key={i.id}>
                      <tr
                        role="button"
                        tabIndex={0}
                        onClick={() => setExpandedIncident(isOpen ? null : i.id)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" || e.key === " ") {
                            e.preventDefault();
                            setExpandedIncident(isOpen ? null : i.id);
                          }
                        }}
                        className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50"
                        aria-expanded={isOpen}
                      >
                        <td className="py-2 font-mono text-xs">{i.incident_id ?? "—"}</td>
                        <td>
                          <Badge
                            tone={
                              i.priority === "P1"
                                ? "red"
                                : i.priority === "P2"
                                  ? "amber"
                                  : "neutral"
                            }
                          >
                            {i.priority}
                          </Badge>
                        </td>
                        <td>
                          <p className="font-medium">{i.summary ?? "—"}</p>
                          {i.root_cause ? (
                            <p className="text-xs text-navy/70">{i.root_cause}</p>
                          ) : null}
                        </td>
                        <td className="text-right font-mono">
                          {i.response_time_minutes === null
                            ? "—"
                            : `${i.response_time_minutes.toFixed(0)}m`}
                        </td>
                        <td className="text-right font-mono">
                          {i.resolution_time_minutes === null
                            ? "—"
                            : `${(i.resolution_time_minutes / 60).toFixed(1)}h`}
                        </td>
                        <td className="text-right font-mono">
                          {currency.format(i.penalty_amount, sourceCurrency)}
                        </td>
                        <td className="text-right">
                          {i.sla_breached ? (
                            <Badge tone="red">breach</Badge>
                          ) : (
                            <Badge tone="green">met</Badge>
                          )}
                        </td>
                      </tr>
                      {isOpen ? (
                        <tr className="bg-ice-50/40">
                          <td colSpan={7} className="px-3 py-3 text-xs">
                            <dl className="grid grid-cols-2 gap-3 md:grid-cols-4">
                              <Detail
                                label="Reported"
                                value={new Date(i.reported_at).toLocaleString("en-GB")}
                              />
                              <Detail
                                label="Responded"
                                value={
                                  i.responded_at
                                    ? new Date(i.responded_at).toLocaleString("en-GB")
                                    : "—"
                                }
                              />
                              <Detail
                                label="Resolved"
                                value={
                                  i.resolved_at
                                    ? new Date(i.resolved_at).toLocaleString("en-GB")
                                    : "—"
                                }
                              />
                              <Detail
                                label="Penalty"
                                value={currency.format(i.penalty_amount, sourceCurrency)}
                              />
                              {i.root_cause ? (
                                <div className="md:col-span-4">
                                  <span className="kpi-label">Root cause</span>
                                  <p className="italic text-navy/80">{i.root_cause}</p>
                                </div>
                              ) : null}
                            </dl>
                          </td>
                        </tr>
                      ) : null}
                    </Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}


function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="kpi-label">{label}</span>
      <span className="font-mono text-navy">{value}</span>
    </div>
  );
}

function Tile({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="kpi-label">{label}</span>
      <span className="font-mono text-lg font-semibold text-navy">{value}</span>
    </div>
  );
}

function monthLabel(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { month: "short", year: "2-digit" });
}
