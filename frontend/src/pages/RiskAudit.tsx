import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ClipboardList, FileText, Home, ShieldCheck } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  fetchAiGovernance,
  fetchAuditLog,
  fetchTopRisks,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { useCurrency } from "@/hooks/useCurrency";
import { formatDate, formatPct, type RagBucket } from "@/lib/format";

function riskSeverityTone(severity: string | null): RagBucket {
  const s = (severity ?? "").toLowerCase();
  if (s === "high" || s === "critical") return "red";
  if (s === "medium") return "amber";
  return "green";
}

export function RiskAudit() {
  const [tableFilter, setTableFilter] = useState<string | null>(null);
  const programmes = useProgrammes();
  const currency = useCurrency();

  const risks = useQuery({
    queryKey: ["risks", "all", 50],
    queryFn: () => fetchTopRisks(50),
  });
  const audit = useQuery({
    queryKey: ["audit", tableFilter],
    queryFn: () => fetchAuditLog(tableFilter ?? undefined, 100),
  });
  const governance = useQuery({
    queryKey: ["audit-governance"],
    queryFn: () => fetchAiGovernance(),
  });

  const auditTables = useMemo(() => {
    const set = new Set<string>();
    for (const a of audit.data ?? []) {
      if (a.table_name) set.add(a.table_name);
    }
    return [...set].sort();
  }, [audit.data]);

  const programmeByName = useMemo(
    () =>
      new Map(
        (programmes.data ?? []).map((p) => [p.id, { code: p.code, name: p.name, currency_code: p.currency_code }]),
      ),
    [programmes.data],
  );

  const risksByProgramme = useMemo(() => {
    const buckets = new Map<string, { count: number; impact: number }>();
    for (const r of risks.data ?? []) {
      const code =
        r.program_id !== null ? programmeByName.get(r.program_id)?.code ?? "—" : "—";
      const row = buckets.get(code) ?? { count: 0, impact: 0 };
      row.count += 1;
      row.impact += r.impact ?? 0;
      buckets.set(code, row);
    }
    return Array.from(buckets.entries()).map(([code, v]) => ({
      code,
      count: v.count,
      impact: v.impact,
    }));
  }, [risks.data, programmeByName]);

  const complianceByControl = useMemo(() => {
    return (governance.data ?? []).map((g) => ({
      control: g.name,
      complianceDisplay: g.compliance_pct ?? 0,
      compliance: (g.compliance_pct ?? 0) / 100,
    }));
  }, [governance.data]);

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
          { label: "Risk & Audit" },
        ]}
      />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Risk & Audit</h1>
        <p className="mt-1 text-sm text-navy/70">
          If an auditor walked in today, could we demonstrate governance?
          RAID register, compliance scorecard, data-change trail.
        </p>
      </div>

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <Stat label="Open risks" value={`${risks.data?.length ?? 0}`} />
        <Stat
          label="Controls tracked"
          value={`${governance.data?.length ?? 0}`}
          sub={`${(governance.data ?? []).filter((g) => g.config_type === "policy").length} policies · ${(governance.data ?? []).filter((g) => g.config_type === "control").length} controls`}
        />
        <Stat
          label="Audit entries"
          value={`${audit.data?.length ?? 0}`}
          sub={`${auditTables.length} tables tracked`}
        />
        <Stat
          label="Risk-weighted exposure"
          value={currency.format(
            (risks.data ?? []).reduce(
              (sum, r) => sum + (r.impact ?? 0) * (r.probability ?? 0),
              0,
            ),
            "INR",
          )}
          sub="Σ impact × probability"
        />
      </section>

      <Card>
        <CardHeader
          title="Risk register"
          subtitle="All open and mitigated risks across the portfolio"
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/60">
                <th className="py-2">Title</th>
                <th>Programme</th>
                <th>Category</th>
                <th>Severity</th>
                <th className="text-right">Probability</th>
                <th className="text-right">Impact</th>
                <th>Owner</th>
                <th>Mitigation</th>
              </tr>
            </thead>
            <tbody>
              {(risks.data ?? []).map((r) => {
                const programmeInfo =
                  r.program_id !== null ? programmeByName.get(r.program_id) : null;
                return (
                  <tr key={r.id} className="border-t border-ice-100 align-top">
                    <td className="py-2 font-medium">{r.title}</td>
                    <td>{programmeInfo?.code ?? "—"}</td>
                    <td>{r.category ?? "—"}</td>
                    <td>
                      <Badge tone={riskSeverityTone(r.severity)}>{r.severity ?? "—"}</Badge>
                    </td>
                    <td className="text-right font-mono">
                      {r.probability === null ? "—" : formatPct(r.probability)}
                    </td>
                    <td className="text-right font-mono">
                      {currency.format(r.impact, programmeInfo?.currency_code ?? "INR")}
                    </td>
                    <td>{r.owner ?? "—"}</td>
                    <td className="text-xs text-navy/70">{r.mitigation_plan ?? "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader
            title="Risk exposure by programme"
            subtitle="Count + summed impact"
          />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={risksByProgramme}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="code" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <YAxis
                  yAxisId="left"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                />
                <YAxis
                  yAxisId="right"
                  orientation="right"
                  stroke="#F59E0B"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(v) => currency.format(Number(v), "INR")}
                />
                <Tooltip
                  contentStyle={{ border: "1px solid #D5E8F0" }}
                  formatter={(value: number, name: string) =>
                    name === "Impact Σ"
                      ? currency.format(value, "INR")
                      : value
                  }
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar yAxisId="left" dataKey="count" name="Risk count" fill="#1B2A4A" />
                <Bar yAxisId="right" dataKey="impact" name="Impact Σ" fill="#F59E0B" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <CardHeader
            title="Compliance scorecard"
            subtitle="Compliance % per governance control"
            action={<ShieldCheck className="size-4 text-success-600" aria-hidden="true" />}
          />
          {complianceByControl.length === 0 ? (
            <p className="text-sm text-navy/60">No governance rows loaded yet.</p>
          ) : (
            <ul className="flex flex-col gap-2 text-sm">
              {complianceByControl.map((row) => (
                <li
                  key={row.control}
                  className="flex items-center justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2"
                >
                  <p className="font-medium">{row.control}</p>
                  <Badge
                    tone={
                      row.complianceDisplay >= 95
                        ? "green"
                        : row.complianceDisplay >= 80
                          ? "amber"
                          : "red"
                    }
                  >
                    {formatPct(row.compliance)}
                  </Badge>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </section>

      <Card>
        <CardHeader
          title="Audit trail"
          subtitle={`Last ${audit.data?.length ?? 0} entries — filter by affected table`}
          action={
            <div className="flex flex-wrap gap-1">
              <button
                type="button"
                onClick={() => setTableFilter(null)}
                className={`rounded-full px-3 py-1 text-xs transition ${
                  tableFilter === null ? "bg-navy text-white" : "bg-ice-50 text-navy hover:bg-ice-100"
                }`}
              >
                All
              </button>
              {auditTables.map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setTableFilter(t)}
                  className={`rounded-full px-3 py-1 text-xs transition ${
                    tableFilter === t ? "bg-navy text-white" : "bg-ice-50 text-navy hover:bg-ice-100"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          }
        />
        {(audit.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/60">No audit entries match the filter.</p>
        ) : (
          <ul className="flex flex-col gap-2 text-sm">
            {(audit.data ?? []).map((a) => (
              <li
                key={a.id}
                className="flex items-start gap-3 rounded border border-ice-100 bg-white px-3 py-2"
              >
                <FileText className="mt-0.5 size-3 text-navy/60" aria-hidden="true" />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Badge tone={a.action === "DELETE" ? "red" : a.action === "UPDATE" ? "amber" : "neutral"}>
                      {a.action ?? "—"}
                    </Badge>
                    <span className="font-mono text-xs">{a.table_name ?? "—"}</span>
                    <span className="text-xs text-navy/60">
                      #{a.record_id ?? "—"}
                    </span>
                  </div>
                  <p className="text-xs text-navy/70">{a.user_action ?? "—"}</p>
                  {a.old_value || a.new_value ? (
                    <p className="mt-1 font-mono text-[11px] text-navy/60">
                      {a.old_value ? <span className="text-danger-600">{a.old_value}</span> : null}
                      {a.old_value && a.new_value ? " → " : null}
                      {a.new_value ? <span className="text-success-600">{a.new_value}</span> : null}
                    </p>
                  ) : null}
                </div>
                <span className="text-xs text-navy/60">
                  {formatDate(a.timestamp)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card>
        <CardHeader
          title="Audit readiness scorecard"
          subtitle="What the auditor asks · where the evidence lives"
          action={<ClipboardList className="size-4 text-navy/60" aria-hidden="true" />}
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/60">
                <th className="py-2">Dimension</th>
                <th>Auditor asks</th>
                <th>Evidence source</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <AuditRow dimension="Financial Controls" ask="Are costs tracked against budget?" source="evm_snapshots + commercial_scenarios" status="Monthly CPI/SPI available" tone="green" />
              <AuditRow dimension="AI Governance" ask="Is AI output reviewed before production?" source="ai_override_log + ai_code_metrics" status="Branch protection + reviewer gate" tone="green" />
              <AuditRow dimension="Risk Management" ask="Are risks identified, assessed, mitigated?" source="risks + risk_history" status="All risks have owner + plan" tone="green" />
              <AuditRow dimension="Change Management" ask="Are changes tracked and approved?" source="scope_creep_log + audit_log" status="All CRs logged with CAB approval" tone="amber" />
              <AuditRow dimension="Quality Assurance" ask="Is quality measured and improving?" source="sprint_data (defects, rework)" status="Sentinel improving; Phoenix trending amber" tone="amber" />
              <AuditRow dimension="Process Adherence" ask="Are governance meetings happening?" source="customer_satisfaction (meeting tracker)" status="≥90% for Atlas/Sentinel/Titan" tone="green" />
              <AuditRow dimension="Data Integrity" ask="Can you trace every number?" source="Data lineage + audit_log" status="Lineage documented, lineage tab planned in I-4" tone="amber" />
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

function AuditRow({
  dimension,
  ask,
  source,
  status,
  tone,
}: {
  dimension: string;
  ask: string;
  source: string;
  status: string;
  tone: RagBucket;
}) {
  return (
    <tr className="border-t border-ice-100 align-top">
      <td className="py-2 font-medium">{dimension}</td>
      <td className="text-xs italic text-navy/70">{ask}</td>
      <td className="font-mono text-xs">{source}</td>
      <td>
        <Badge tone={tone}>{status}</Badge>
      </td>
    </tr>
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
      {sub ? <p className="text-xs text-navy/60">{sub}</p> : null}
    </div>
  );
}
