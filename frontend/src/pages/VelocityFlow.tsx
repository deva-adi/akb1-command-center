import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { CheckCircle2, Home, XCircle } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { ProgrammeFilterBar } from "@/components/ProgrammeFilterBar";
import { PROGRAMME_CROSS_LINKS } from "@/components/programmeCrossLinks";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  fetchBlendRules,
  fetchDualVelocity,
  type DualVelocity,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { formatPct, formatRatio } from "@/lib/format";

export function VelocityFlow() {
  const [searchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();

  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );

  const dual = useQuery({
    queryKey: ["dual-velocity", filteredProgramme?.id ?? null],
    queryFn: () => fetchDualVelocity(filteredProgramme?.id),
  });
  const blendRules = useQuery({
    queryKey: ["blend-rules", filteredProgramme?.id ?? null],
    queryFn: () => fetchBlendRules(filteredProgramme?.id),
  });

  const projectSeries = useMemo(() => {
    const rows = dual.data ?? [];
    const byProject = new Map<number, DualVelocity[]>();
    for (const r of rows) {
      if (r.project_id === null) continue;
      const list = byProject.get(r.project_id) ?? [];
      list.push(r);
      byProject.set(r.project_id, list);
    }
    return Array.from(byProject.entries()).map(([projectId, list]) => ({
      projectId,
      rows: list
        .slice()
        .sort((a, b) => (a.sprint_number ?? 0) - (b.sprint_number ?? 0)),
    }));
  }, [dual.data]);

  const aggregate = useMemo(() => {
    const rows = dual.data ?? [];
    if (rows.length === 0) return null;
    const lastBySprint = new Map<number, DualVelocity>();
    for (const r of rows) {
      if (r.sprint_number === null) continue;
      const existing = lastBySprint.get(r.sprint_number);
      if (!existing || (r.snapshot_date ?? "") > (existing.snapshot_date ?? "")) {
        lastBySprint.set(r.sprint_number, r);
      }
    }
    const totalStandard = rows.reduce(
      (sum, r) => sum + (r.standard_velocity ?? 0),
      0,
    );
    const totalAiRaw = rows.reduce((sum, r) => sum + (r.ai_raw_velocity ?? 0), 0);
    const totalAiAdj = rows.reduce(
      (sum, r) => sum + (r.ai_quality_adjusted_velocity ?? 0),
      0,
    );
    const avgParity =
      rows.filter((r) => r.quality_parity_ratio !== null).length === 0
        ? null
        : rows
            .filter((r) => r.quality_parity_ratio !== null)
            .reduce((s, r) => s + (r.quality_parity_ratio ?? 0), 0) /
          rows.filter((r) => r.quality_parity_ratio !== null).length;
    const mergeEligibleCount = rows.filter((r) => r.merge_eligible).length;
    return {
      totalStandard,
      totalAiRaw,
      totalAiAdj,
      avgParity,
      mergeEligibleCount,
      totalRows: rows.length,
    };
  }, [dual.data]);

  const breadcrumbItems = [
    { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
    { label: "Velocity & Flow", to: filteredProgramme ? "/velocity" : undefined },
    ...(filteredProgramme ? [{ label: filteredProgramme.name }] : []),
  ];

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumbItems} />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Velocity & Flow</h1>
        <p className="mt-1 text-sm text-navy/70">
          Is AI-augmented velocity real or illusory? This tab pairs raw AI
          output with a quality-adjusted view and the blend-rule gates that
          decide whether AI velocity can count towards the plan.
        </p>
      </div>

      <ProgrammeFilterBar
        currentRoute="/velocity"
        crossLinks={PROGRAMME_CROSS_LINKS}
      />

      {aggregate ? (
        <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <Stat
            label="Standard velocity (sum)"
            value={`${aggregate.totalStandard.toFixed(0)} pts`}
          />
          <Stat
            label="AI raw velocity (sum)"
            value={`${aggregate.totalAiRaw.toFixed(0)} pts`}
          />
          <Stat
            label="AI quality-adjusted"
            value={`${aggregate.totalAiAdj.toFixed(0)} pts`}
            sub={`${formatPct(aggregate.totalAiRaw > 0 ? aggregate.totalAiAdj / aggregate.totalAiRaw : null)} retained after rework`}
          />
          <Stat
            label="Merge-eligible sprints"
            value={`${aggregate.mergeEligibleCount} / ${aggregate.totalRows}`}
            tone={aggregate.mergeEligibleCount === aggregate.totalRows ? "green" : "amber"}
          />
        </section>
      ) : null}

      <Card>
        <CardHeader
          title="Dual velocity per project"
          subtitle="Standard vs AI-raw vs AI-quality-adjusted, per sprint"
        />
        {projectSeries.length === 0 ? (
          <p className="text-sm text-navy/70">
            No dual-velocity data yet. Only AI-augmented projects contribute —
            try filtering to Phoenix or Sentinel or clear the filter.
          </p>
        ) : (
          <div className="flex flex-col gap-6">
            {projectSeries.map(({ projectId, rows }) => (
              <DualVelocityChart
                key={projectId}
                projectId={projectId}
                rows={rows}
              />
            ))}
          </div>
        )}
      </Card>

      <Card>
        <CardHeader
          title="Blend-rule gates"
          subtitle="AI velocity only counts against the plan when every gate passes"
        />
        {blendRules.isLoading ? (
          <p className="text-sm text-navy/70">Loading gates…</p>
        ) : (blendRules.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/70">
            No blend rules configured for the current scope.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-navy/70">
                  <th className="py-2">Programme</th>
                  <th>Gate</th>
                  <th className="text-right">Current</th>
                  <th className="text-right">Threshold</th>
                  <th className="text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {(blendRules.data ?? []).map((g) => {
                  const programmeName =
                    programmes.data?.find((p) => p.id === g.program_id)?.code ??
                    "—";
                  return (
                    <tr key={g.id} className="border-t border-ice-100">
                      <td className="py-2 font-medium">{programmeName}</td>
                      <td>
                        <div>{g.gate_name}</div>
                        {g.gate_condition ? (
                          <div className="text-xs text-navy/70">
                            <code>{g.gate_condition}</code>
                          </div>
                        ) : null}
                      </td>
                      <td className="text-right font-mono">
                        {formatRatio(g.current_value)}
                      </td>
                      <td className="text-right font-mono text-navy/70">
                        {formatRatio(g.threshold)}
                      </td>
                      <td className="text-right">
                        {g.passed ? (
                          <Badge tone="green">
                            <CheckCircle2 className="size-3" /> pass
                          </Badge>
                        ) : (
                          <Badge tone="red">
                            <XCircle className="size-3" /> fail
                          </Badge>
                        )}
                      </td>
                    </tr>
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

function DualVelocityChart({
  projectId,
  rows,
}: {
  projectId: number;
  rows: DualVelocity[];
}) {
  const data = rows.map((r) => ({
    sprint: `#${r.sprint_number ?? "?"}`,
    standard: r.standard_velocity ?? 0,
    aiRaw: r.ai_raw_velocity ?? 0,
    aiAdjusted: r.ai_quality_adjusted_velocity ?? 0,
    parity: r.quality_parity_ratio ?? 0,
  }));
  const latest = rows[rows.length - 1];

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-navy">
          Project id {projectId}
        </p>
        {latest ? (
          <Badge tone={latest.merge_eligible ? "green" : "red"}>
            {latest.merge_eligible ? "merge-eligible" : "merge blocked"}
          </Badge>
        ) : null}
      </div>
      <div className="h-60">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
            <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
            <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
            <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
            <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="standard" name="Standard" fill="#1B2A4A" />
            <Bar dataKey="aiRaw" name="AI raw" fill="#F59E0B" />
            <Bar dataKey="aiAdjusted" name="AI adjusted" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="h-32">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 20, left: 0, bottom: 8 }}>
            <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
            <XAxis dataKey="sprint" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
            <YAxis
              stroke="#1B2A4A"
              domain={[0, 1]}
              tick={{ fontSize: 12 }}
              tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
            />
            <ReferenceLine
              y={0.95}
              stroke="#10B981"
              strokeDasharray="4 4"
              label={{
                value: "Parity gate",
                position: "insideTopRight",
                fill: "#10B981",
                fontSize: 11,
              }}
            />
            <Tooltip
              formatter={(v: number) => `${(v * 100).toFixed(1)}%`}
              contentStyle={{ border: "1px solid #D5E8F0" }}
            />
            <Line
              type="monotone"
              dataKey="parity"
              stroke="#F59E0B"
              strokeWidth={2}
              dot={false}
              name="Quality parity"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

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
