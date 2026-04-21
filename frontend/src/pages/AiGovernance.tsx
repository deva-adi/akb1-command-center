import { useMemo } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
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
import { AlertOctagon, Home, ShieldCheck, Sparkles } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { ProgrammeFilterBar } from "@/components/ProgrammeFilterBar";
import { PROGRAMME_CROSS_LINKS } from "@/components/programmeCrossLinks";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  fetchAiGovernance,
  fetchAiOverrides,
  fetchAiSdlcMetrics,
  fetchAiTools,
  fetchAiTrustScores,
  fetchAiUsage,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { formatDate, formatPct, type RagBucket } from "@/lib/format";

function trustTone(score: number | null): RagBucket {
  if (score === null) return "amber";
  if (score >= 75) return "green";
  if (score >= 60) return "amber";
  return "red";
}

const MATURITY_TONE: Record<string, RagBucket> = {
  "L1-Initial": "red",
  "L2-Managed": "amber",
  "L3-Defined": "amber",
  "L4-Optimising": "green",
  "L5-Autonomous": "green",
};

export function AiGovernance() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();

  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );

  const tools = useQuery({ queryKey: ["ai-tools"], queryFn: fetchAiTools });
  const trust = useQuery({
    queryKey: ["ai-trust", filteredProgramme?.id ?? null],
    queryFn: () => fetchAiTrustScores(filteredProgramme?.id),
  });
  const usage = useQuery({
    queryKey: ["ai-usage", filteredProgramme?.id ?? null],
    queryFn: () => fetchAiUsage(filteredProgramme?.id),
  });
  const sdlc = useQuery({
    queryKey: ["ai-sdlc", filteredProgramme?.id ?? null],
    queryFn: () => fetchAiSdlcMetrics(filteredProgramme?.id),
  });
  const governance = useQuery({
    queryKey: ["ai-governance", filteredProgramme?.id ?? null],
    queryFn: () => fetchAiGovernance(filteredProgramme?.id),
  });
  const overrides = useQuery({
    queryKey: ["ai-overrides", filteredProgramme?.id ?? null],
    queryFn: () => fetchAiOverrides(filteredProgramme?.id),
  });


  const programmeByName = useMemo(
    () =>
      new Map(
        (programmes.data ?? []).map((p) => [p.id, { code: p.code, name: p.name }]),
      ),
    [programmes.data],
  );

  const trustRadarData = useMemo(() => {
    // Aggregate per programme (latest score per programme). The radar shows
    // the 6 composite factors for each programme we have a score for.
    const rows = trust.data ?? [];
    const aggregated: Record<string, number>[] = [];
    for (const row of rows) {
      const programmeName =
        row.program_id !== null
          ? programmeByName.get(row.program_id)?.code ?? "—"
          : "—";
      aggregated.push({
        programme: programmeName,
        Provenance: row.provenance_score ?? 0,
        Review: row.review_status_score ?? 0,
        Coverage: row.test_coverage_score ?? 0,
        Drift: row.drift_check_score ?? 0,
        Override: row.override_rate_score ?? 0,
        Defect: row.defect_rate_score ?? 0,
      } as unknown as Record<string, number>);
    }
    return aggregated;
  }, [trust.data, programmeByName]);

  // Reshape trust data into a radar-friendly array: one row per factor with a
  // column per programme.
  const trustRadarShaped = useMemo(() => {
    const factors = [
      "Provenance",
      "Review",
      "Coverage",
      "Drift",
      "Override",
      "Defect",
    ];
    return factors.map((factor) => {
      const row: Record<string, number | string> = { factor };
      for (const p of trustRadarData) {
        row[p.programme as unknown as string] = p[factor] as unknown as number;
      }
      return row;
    });
  }, [trustRadarData]);

  const sdlcComparison = useMemo(() => {
    const rows = sdlc.data ?? [];
    if (rows.length === 0) return null;
    const latestBySprint = new Map<number, (typeof rows)[number]>();
    for (const r of rows) {
      if (r.sprint_number === null) continue;
      latestBySprint.set(r.sprint_number, r);
    }
    const arr = Array.from(latestBySprint.values());
    const avg = (pick: (r: (typeof arr)[number]) => number | null) =>
      arr.reduce((s, r) => s + (pick(r) ?? 0), 0) / arr.length;
    return [
      {
        metric: "Estimation accuracy",
        withAi: avg((r) => r.estimation_accuracy_with_ai),
        withoutAi: avg((r) => r.estimation_accuracy_without_ai),
      },
      {
        metric: "Code review hrs (↓ better)",
        withAi: avg((r) => r.code_review_hours_with_ai),
        withoutAi: avg((r) => r.code_review_hours_without_ai),
      },
      {
        metric: "Planning velocity (pts)",
        withAi: avg((r) => r.planning_velocity_with_ai),
        withoutAi: avg((r) => r.planning_velocity_without_ai),
      },
      {
        metric: "Docs hrs (↓ better)",
        withAi: avg((r) => r.documentation_hours_with_ai),
        withoutAi: avg((r) => r.documentation_hours_without_ai),
      },
    ];
  }, [sdlc.data]);

  const totalTimeSaved = (usage.data ?? []).reduce(
    (sum, r) => sum + (r.time_saved_hours ?? 0),
    0,
  );
  const totalCost = (usage.data ?? []).reduce((sum, r) => sum + (r.cost ?? 0), 0);
  const avgAcceptance = (() => {
    const rows = usage.data ?? [];
    const prompts = rows.reduce((s, r) => s + (r.prompts_count ?? 0), 0);
    const accepted = rows.reduce((s, r) => s + (r.suggestions_accepted ?? 0), 0);
    return prompts > 0 ? accepted / prompts : null;
  })();

  const breadcrumbItems = [
    { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
    { label: "AI Governance", to: filteredProgramme ? "/ai" : undefined },
    ...(filteredProgramme ? [{ label: filteredProgramme.name }] : []),
  ];

  const programmeCodes = useMemo(
    () => [...new Set(trustRadarData.map((r) => r.programme as unknown as string))],
    [trustRadarData],
  );

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumbItems} />

      <div>
        <h1 className="text-2xl font-semibold text-navy">AI Governance</h1>
        <p className="mt-1 text-sm text-navy/70">
          Are AI tools trustworthy, compliant, and productive? 6-factor
          composite trust score per programme, plus the productivity-tax
          with/without AI comparison.
        </p>
      </div>

      <ProgrammeFilterBar
        currentRoute="/ai"
        crossLinks={PROGRAMME_CROSS_LINKS}
      />

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <Stat
          label="AI tools in use"
          value={`${tools.data?.length ?? 0}`}
          sub={`${(tools.data ?? []).filter((t) => t.status === "Active").length} active`}
        />
        <Stat
          label="Time saved"
          value={`${totalTimeSaved.toFixed(0)}h`}
          sub="Accepted suggestions × hrs saved"
        />
        <Stat
          label="Acceptance rate"
          value={avgAcceptance === null ? "—" : formatPct(avgAcceptance)}
          tone={
            avgAcceptance === null
              ? "neutral"
              : avgAcceptance >= 0.6
                ? "green"
                : avgAcceptance >= 0.45
                  ? "amber"
                  : "red"
          }
        />
        <Stat
          label="AI spend"
          value={`$${totalCost.toLocaleString()}`}
          sub="Monthly seat + usage cost"
        />
      </section>

      <Card>
        <CardHeader
          title="Trust composite — 6 factors per programme"
          subtitle="Click the score badges below to drill into that programme's AI detail"
        />
        {programmeCodes.length === 0 ? (
          <p className="text-sm text-navy/70">
            No trust scores seeded for the current scope.
          </p>
        ) : (
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart
                data={trustRadarShaped}
                onClick={(chartData) => {
                  const code = chartData?.activePayload?.[0]?.dataKey as string | undefined;
                  if (code && code !== "factor") navigate(`/ai?programme=${code}`);
                }}
                style={{ cursor: "pointer" }}
              >
                <PolarGrid stroke="#D5E8F0" />
                <PolarAngleAxis dataKey="factor" tick={{ fontSize: 11 }} />
                <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
                {programmeCodes.map((code, idx) => (
                  <Radar
                    key={code}
                    name={code}
                    dataKey={code}
                    stroke={RADAR_COLORS[idx % RADAR_COLORS.length]}
                    fill={RADAR_COLORS[idx % RADAR_COLORS.length]}
                    fillOpacity={0.15}
                  />
                ))}
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}
        <ul className="mt-3 flex flex-wrap gap-2 text-xs">
          {(trust.data ?? []).map((t) => {
            const prog =
              t.program_id !== null ? programmeByName.get(t.program_id) : null;
            const programmeName = prog?.code ?? "—";
            return (
              <li key={t.id} className="flex items-center gap-1">
                <button
                  type="button"
                  onClick={() => prog ? navigate(`/ai?programme=${prog.code}`) : undefined}
                  className={prog ? "cursor-pointer" : undefined}
                  aria-label={prog ? `Drill into ${prog.code} AI detail` : undefined}
                >
                  <Badge tone={trustTone(t.composite_score)}>
                    {programmeName}: {t.composite_score?.toFixed(0) ?? "—"} ↗
                  </Badge>
                </button>
                <Badge tone={MATURITY_TONE[t.maturity_level ?? ""] ?? "neutral"}>
                  {t.maturity_level ?? "—"}
                </Badge>
              </li>
            );
          })}
        </ul>
      </Card>

      {sdlcComparison ? (
        <Card>
          <CardHeader
            title="Productivity tax — with AI vs without AI"
            subtitle="Click a bar to drill into Velocity & Flow for this programme"
          />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={sdlcComparison}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
                onClick={() => {
                  const code = filteredProgramme?.code;
                  navigate(code ? `/velocity?programme=${code}` : "/velocity");
                }}
                style={{ cursor: "pointer" }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="metric" stroke="#1B2A4A" tick={{ fontSize: 11 }} />
                <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="withoutAi" name="Without AI" fill="#1B2A4A" />
                <Bar dataKey="withAi" name="With AI" fill="#F59E0B" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      ) : null}

      <Card>
        <CardHeader
          title="Governance controls & policies"
          subtitle="Compliance % against each documented control"
          action={<ShieldCheck className="size-4 text-success-600" aria-hidden="true" />}
        />
        {(governance.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/70">No governance config rows loaded.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-navy/70">
                  <th className="py-2">Type</th>
                  <th>Name</th>
                  <th>Scope</th>
                  <th className="text-right">Compliance</th>
                  <th className="text-right">Last audit</th>
                  <th>Owner</th>
                </tr>
              </thead>
              <tbody>
                {(governance.data ?? []).map((g) => (
                  <tr key={g.id} className="border-t border-ice-100 align-top">
                    <td className="py-2">
                      <Badge tone={g.config_type === "policy" ? "neutral" : "amber"}>
                        {g.config_type}
                      </Badge>
                    </td>
                    <td>
                      <p className="font-medium">{g.name}</p>
                      {g.description ? (
                        <p className="text-xs text-navy/70">{g.description}</p>
                      ) : null}
                    </td>
                    <td>
                      {g.scope ?? "—"}
                      {g.program_id !== null
                        ? ` / ${programmeByName.get(g.program_id)?.code ?? "—"}`
                        : ""}
                    </td>
                    <td className="text-right font-mono">
                      <Badge
                        tone={
                          (g.compliance_pct ?? 0) >= 95
                            ? "green"
                            : (g.compliance_pct ?? 0) >= 80
                              ? "amber"
                              : "red"
                        }
                      >
                        {formatPct((g.compliance_pct ?? 0) / 100)}
                      </Badge>
                    </td>
                    <td className="text-right text-xs text-navy/70">
                      {formatDate(g.last_audit_date)}
                    </td>
                    <td>{g.owner ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Card>
        <CardHeader
          title="Override log"
          subtitle="Every human override of an AI suggestion captured with rationale"
          action={<AlertOctagon className="size-4 text-danger-600" aria-hidden="true" />}
        />
        {(overrides.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/70">No overrides in the current scope.</p>
        ) : (
          <ul className="flex flex-col gap-2 text-sm">
            {(overrides.data ?? []).map((o) => {
              const programmeName =
                o.program_id !== null
                  ? programmeByName.get(o.program_id)?.code ?? "—"
                  : "—";
              return (
                <li
                  key={o.id}
                  className="flex items-start justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2"
                >
                  <div className="flex-1">
                    <p className="font-medium">{o.reason ?? "—"}</p>
                    <p className="text-xs text-navy/70">
                      {o.override_date
                        ? new Date(o.override_date).toLocaleString("en-GB")
                        : "—"}{" "}
                      · {programmeName} · {o.override_type ?? "—"}
                      {o.approver ? ` · approver: ${o.approver}` : ""}
                    </p>
                    {o.outcome ? (
                      <p className="mt-1 text-xs italic text-navy/70">
                        Outcome: {o.outcome}
                      </p>
                    ) : null}
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </Card>

      <Card>
        <CardHeader
          title="Tool catalogue"
          subtitle={`${tools.data?.length ?? 0} tools registered`}
          action={<Sparkles className="size-4 text-amber-500" aria-hidden="true" />}
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/70">
                <th className="py-2">Tool</th>
                <th>Vendor</th>
                <th>Category</th>
                <th>License</th>
                <th className="text-right">$/seat/mo</th>
                <th className="text-right">Status</th>
              </tr>
            </thead>
            <tbody>
              {(tools.data ?? []).map((t) => (
                <tr key={t.id} className="border-t border-ice-100">
                  <td className="py-2 font-medium">{t.name}</td>
                  <td>{t.vendor ?? "—"}</td>
                  <td>{t.category ?? "—"}</td>
                  <td>{t.license_type ?? "—"}</td>
                  <td className="text-right font-mono">
                    ${t.cost_per_seat?.toFixed(0) ?? "—"}
                  </td>
                  <td className="text-right">
                    <Badge tone={t.status === "Active" ? "green" : "amber"}>
                      {t.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

const RADAR_COLORS = ["#1B2A4A", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6"];

function Stat({
  label,
  value,
  sub,
  tone,
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
        {tone && tone !== "neutral" ? <Badge tone={tone}>·</Badge> : null}
      </div>
      {sub ? <p className="text-xs text-navy/70">{sub}</p> : null}
    </div>
  );
}
