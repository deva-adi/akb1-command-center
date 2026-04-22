import { Fragment, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
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
import {
  ChevronDown,
  ChevronUp,
  ClipboardList,
  FileText,
  Home,
  ShieldCheck,
} from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { ProgrammeFilterBar } from "@/components/ProgrammeFilterBar";
import { PROGRAMME_CROSS_LINKS } from "@/components/programmeCrossLinks";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
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
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const [tableFilter, setTableFilter] = useState<string | null>(null);
  const [expandedRisk, setExpandedRisk] = useState<number | null>(null);
  const [expandedAudit, setExpandedAudit] = useState<number | null>(null);
  const [riskStatusFilter, setRiskStatusFilter] = useState<string | null>(null);
  const [riskSeverityFilter, setRiskSeverityFilter] = useState<string | null>(null);
  const [sortByExpectedLoss, setSortByExpectedLoss] = useState(false);
  const riskTableRef = useRef<HTMLDivElement>(null);
  const auditTrailRef = useRef<HTMLDivElement>(null);
  const programmes = useProgrammes();
  const currency = useCurrency();

  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );

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

  // Programme-scoped risk set — drives the "Open risks" count and exposure card.
  // This is independent of the status/severity chips so those card values stay
  // stable when the user toggles a chip.
  const programmeRisks = useMemo(() => {
    const all = risks.data ?? [];
    if (!filteredProgramme) return all;
    return all.filter((r) => r.program_id === filteredProgramme.id);
  }, [risks.data, filteredProgramme]);

  const openRiskCount = useMemo(
    () => programmeRisks.filter((r) => (r.status ?? "").toLowerCase() !== "closed" && (r.status ?? "").toLowerCase() !== "mitigated").length,
    [programmeRisks],
  );

  const visibleRisks = useMemo(() => {
    let rows = programmeRisks;
    if (riskStatusFilter === "__open__") {
      rows = rows.filter((r) => {
        const s = (r.status ?? "").toLowerCase();
        return s !== "closed" && s !== "mitigated";
      });
    } else if (riskStatusFilter) {
      rows = rows.filter((r) => r.status === riskStatusFilter);
    }
    if (riskSeverityFilter) {
      rows = rows.filter((r) => r.severity === riskSeverityFilter);
    }
    if (sortByExpectedLoss) {
      rows = [...rows].sort((a, b) =>
        ((b.impact ?? 0) * (b.probability ?? 0)) - ((a.impact ?? 0) * (a.probability ?? 0)),
      );
    }
    return rows;
  }, [programmeRisks, riskStatusFilter, riskSeverityFilter, sortByExpectedLoss]);

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
          { label: "Risk & Audit", to: filteredProgramme ? "/raid" : undefined },
          ...(filteredProgramme ? [{ label: filteredProgramme.name }] : []),
        ]}
      />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Risk & Audit</h1>
        <p className="mt-1 text-sm text-navy/70">
          If an auditor walked in today, could we demonstrate governance?
          RAID register, compliance scorecard, data-change trail.
        </p>
        <ProgrammeFilterBar
          currentRoute="/raid"
          crossLinks={PROGRAMME_CROSS_LINKS}
        />
      </div>

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <MetricCard
          metricId="open_risks"
          value={`${openRiskCount}`}
          sub={`${programmeRisks.length} total`}
          onClick={() => {
            setRiskStatusFilter(riskStatusFilter === "__open__" ? null : "__open__");
            setRiskSeverityFilter(null);
            setSortByExpectedLoss(false);
            riskTableRef.current?.scrollIntoView({ behavior: 'smooth' });
          }}
        />
        <MetricCard
          label="Controls tracked"
          value={`${governance.data?.length ?? 0}`}
          sub={`${(governance.data ?? []).filter((g) => g.config_type === "policy").length} policies · ${(governance.data ?? []).filter((g) => g.config_type === "control").length} controls`}
          onClick={() => navigate(filteredProgramme ? `/ai?programme=${filteredProgramme.code}` : '/ai')}
        />
        <MetricCard
          label="Audit entries"
          value={`${audit.data?.length ?? 0}`}
          sub={`${auditTables.length} tables tracked`}
          onClick={() => {
            setTableFilter(null);
            auditTrailRef.current?.scrollIntoView({ behavior: 'smooth' });
          }}
        />
        <MetricCard
          metricId="risk_exposure"
          value={currency.format(
            programmeRisks.reduce(
              (sum, r) => sum + (r.impact ?? 0) * (r.probability ?? 0),
              0,
            ),
            "INR",
          )}
          sub="Σ impact × probability · click to rank"
          onClick={() => {
            setSortByExpectedLoss(!sortByExpectedLoss);
            setRiskStatusFilter(null);
            setRiskSeverityFilter(null);
            riskTableRef.current?.scrollIntoView({ behavior: 'smooth' });
          }}
        />
      </section>

      <div ref={riskTableRef}>
      <Card>
        <CardHeader
          title="Risk register"
          subtitle={(() => {
            const parts: string[] = [];
            if (riskStatusFilter === "__open__") parts.push("open only");
            else if (riskStatusFilter) parts.push(`status = ${riskStatusFilter}`);
            if (riskSeverityFilter) parts.push(`severity = ${riskSeverityFilter}`);
            if (sortByExpectedLoss) parts.push("ranked by expected loss");
            if (parts.length === 0) return "All risks across the current scope";
            return `${visibleRisks.length} of ${programmeRisks.length} — ${parts.join(" · ")}`;
          })()}
          action={
            (riskStatusFilter || riskSeverityFilter || sortByExpectedLoss) ? (
              <button
                type="button"
                onClick={() => {
                  setRiskStatusFilter(null);
                  setRiskSeverityFilter(null);
                  setSortByExpectedLoss(false);
                }}
                className="inline-flex items-center gap-1 rounded-full border border-navy/30 bg-navy/5 px-2 py-0.5 text-xs text-navy hover:bg-navy/10"
                aria-label="Clear all risk filters"
              >
                Clear filters
                <span aria-hidden="true">×</span>
              </button>
            ) : null
          }
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/70">
                <th className="py-2">Title</th>
                <th>Programme</th>
                <th>Category</th>
                <th>Severity</th>
                <th className="text-right">Probability</th>
                <th className="text-right">Impact</th>
                <th>Owner</th>
                <th aria-hidden="true" />
              </tr>
            </thead>
            <tbody>
              {visibleRisks.map((r) => {
                const programmeInfo =
                  r.program_id !== null ? programmeByName.get(r.program_id) : null;
                const isOpen = expandedRisk === r.id;
                return (
                  <Fragment key={r.id}>
                    <tr
                      role="button"
                      tabIndex={0}
                      onClick={() => setExpandedRisk(isOpen ? null : r.id)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          e.preventDefault();
                          setExpandedRisk(isOpen ? null : r.id);
                        }
                      }}
                      className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50"
                      aria-expanded={isOpen}
                    >
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
                      <td className="pr-2 text-right text-navy/40">
                        {isOpen ? (
                          <ChevronUp className="inline size-4" aria-hidden="true" />
                        ) : (
                          <ChevronDown className="inline size-4" aria-hidden="true" />
                        )}
                      </td>
                    </tr>
                    {isOpen ? (
                      <tr className="bg-ice-50/40">
                        <td colSpan={8} className="px-3 py-3 text-xs">
                          <dl className="grid grid-cols-1 gap-3 md:grid-cols-2">
                            <div className="md:col-span-2">
                              <span className="kpi-label">Description</span>
                              <p className="text-navy/80">{r.description ?? "—"}</p>
                            </div>
                            <div className="md:col-span-2">
                              <span className="kpi-label">Mitigation plan</span>
                              <p className="italic text-navy/80">
                                {r.mitigation_plan ?? "—"}
                              </p>
                            </div>
                            <Detail
                              label="Expected loss (impact × prob.)"
                              value={currency.format(
                                (r.impact ?? 0) * (r.probability ?? 0),
                                programmeInfo?.currency_code ?? "INR",
                              )}
                            />
                            <Detail
                              label="Status"
                              value={r.status}
                            />
                          </dl>
                          {programmeInfo ? (
                            <div className="mt-3 flex flex-wrap gap-2 text-xs text-navy/70">
                              <span className="text-navy/50">Open programme in:</span>
                              <Link
                                to={`/delivery?programme=${programmeInfo.code}`}
                                className="rounded-full border border-ice-100 bg-white px-2 py-0.5 hover:bg-ice-50"
                              >
                                Delivery
                              </Link>
                              <Link
                                to={`/kpi?programme=${programmeInfo.code}`}
                                className="rounded-full border border-ice-100 bg-white px-2 py-0.5 hover:bg-ice-50"
                              >
                                KPIs
                              </Link>
                              <Link
                                to={`/customer?programme=${programmeInfo.code}`}
                                className="rounded-full border border-ice-100 bg-white px-2 py-0.5 hover:bg-ice-50"
                              >
                                Customer
                              </Link>
                            </div>
                          ) : null}
                        </td>
                      </tr>
                    ) : null}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
      </div>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader
            title="Risk exposure by programme"
            subtitle="Click a bar to drill into that programme's filtered risk register"
          />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={risksByProgramme}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
                onClick={(chartData) => {
                  const code = chartData?.activePayload?.[0]?.payload?.code as string | undefined;
                  if (code) navigate(`/raid?programme=${code}`);
                }}
                style={{ cursor: "pointer" }}
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
            <p className="text-sm text-navy/70">No governance rows loaded yet.</p>
          ) : (
            <ul className="flex flex-col gap-2 text-sm">
              {complianceByControl.map((row) => (
                <li
                  key={row.control}
                  role="button"
                  tabIndex={0}
                  onClick={() => navigate(filteredProgramme ? `/ai?programme=${filteredProgramme.code}` : '/ai')}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); navigate(filteredProgramme ? `/ai?programme=${filteredProgramme.code}` : '/ai'); } }}
                  className="flex items-center justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2 cursor-pointer hover:bg-ice-50 transition"
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

      <div ref={auditTrailRef}>
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
          <p className="text-sm text-navy/70">No audit entries match the filter.</p>
        ) : (
          <ul className="flex flex-col gap-2 text-sm">
            {(audit.data ?? []).map((a) => (
              <li
                key={a.id}
                role="button"
                tabIndex={0}
                className="flex flex-col rounded border border-ice-100 bg-white px-3 py-2 cursor-pointer hover:bg-ice-50 transition"
                onClick={() => setExpandedAudit(expandedAudit === a.id ? null : a.id)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setExpandedAudit(expandedAudit === a.id ? null : a.id);
                  }
                }}
              >
                <div className="flex items-start gap-3">
                  <FileText className="mt-0.5 size-3 text-navy/70" aria-hidden="true" />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <Badge tone={a.action === "DELETE" ? "red" : a.action === "UPDATE" ? "amber" : "neutral"}>
                        {a.action ?? "—"}
                      </Badge>
                      <span className="font-mono text-xs">{a.table_name ?? "—"}</span>
                      <span className="text-xs text-navy/70">
                        #{a.record_id ?? "—"}
                      </span>
                    </div>
                    <p className="text-xs text-navy/70">{a.user_action ?? "—"}</p>
                    {a.old_value || a.new_value ? (
                      <p className="mt-1 font-mono text-[11px] text-navy/70">
                        {a.old_value ? <span className="text-danger-600">{a.old_value}</span> : null}
                        {a.old_value && a.new_value ? " → " : null}
                        {a.new_value ? <span className="text-success-600">{a.new_value}</span> : null}
                      </p>
                    ) : null}
                  </div>
                  <span className="text-xs text-navy/70">
                    {formatDate(a.timestamp)}
                  </span>
                </div>
                {expandedAudit === a.id && (a.old_value || a.new_value) ? (
                  <div className="mt-2 grid grid-cols-2 gap-2 border-t border-ice-100 pt-2">
                    {a.old_value ? (
                      <div>
                        <span className="kpi-label text-danger-600">Old value</span>
                        <pre className="mt-1 overflow-x-auto rounded bg-danger-50 p-2 font-mono text-[10px] text-danger-700 whitespace-pre-wrap break-all">{a.old_value}</pre>
                      </div>
                    ) : null}
                    {a.new_value ? (
                      <div>
                        <span className="kpi-label text-success-700">New value</span>
                        <pre className="mt-1 overflow-x-auto rounded bg-success-50 p-2 font-mono text-[10px] text-success-700 whitespace-pre-wrap break-all">{a.new_value}</pre>
                      </div>
                    ) : null}
                  </div>
                ) : null}
              </li>
            ))}
          </ul>
        )}
      </Card>
      </div>

      <Card>
        <CardHeader
          title="Audit readiness scorecard"
          subtitle="What the auditor asks · where the evidence lives"
          action={<ClipboardList className="size-4 text-navy/70" aria-hidden="true" />}
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/70">
                <th className="py-2">Dimension</th>
                <th>Auditor asks</th>
                <th>Evidence source</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <AuditRow dimension="Financial Controls" ask="Are costs tracked against budget?" source="evm_snapshots + commercial_scenarios" status="Monthly CPI/SPI available" tone="green" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["Financial Controls"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["Financial Controls"])} />
              <AuditRow dimension="AI Governance" ask="Is AI output reviewed before production?" source="ai_override_log + ai_code_metrics" status="Branch protection + reviewer gate" tone="green" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["AI Governance"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["AI Governance"])} />
              <AuditRow dimension="Risk Management" ask="Are risks identified, assessed, mitigated?" source="risks + risk_history" status="All risks have owner + plan" tone="green" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["Risk Management"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["Risk Management"])} />
              <AuditRow dimension="Change Management" ask="Are changes tracked and approved?" source="scope_creep_log + audit_log" status="All CRs logged with CAB approval" tone="amber" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["Change Management"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["Change Management"])} />
              <AuditRow dimension="Quality Assurance" ask="Is quality measured and improving?" source="sprint_data (defects, rework)" status="Sentinel improving; Phoenix trending amber" tone="amber" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["Quality Assurance"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["Quality Assurance"])} />
              <AuditRow dimension="Process Adherence" ask="Are governance meetings happening?" source="customer_satisfaction (meeting tracker)" status="≥90% for Atlas/Sentinel/Titan" tone="green" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["Process Adherence"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["Process Adherence"])} />
              <AuditRow dimension="Data Integrity" ask="Can you trace every number?" source="Data lineage + audit_log" status="Lineage documented, lineage tab planned in I-4" tone="amber" onClick={() => navigate(filteredProgramme ? `${DIMENSION_ROUTE["Data Integrity"]}?programme=${filteredProgramme.code}` : DIMENSION_ROUTE["Data Integrity"])} />
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

const DIMENSION_ROUTE: Record<string, string> = {
  "Financial Controls": "/margin",
  "AI Governance": "/ai",
  "Risk Management": "/raid",
  "Change Management": "/raid",
  "Quality Assurance": "/delivery",
  "Process Adherence": "/customer",
  "Data Integrity": "/raid",
};

function AuditRow({
  dimension,
  ask,
  source,
  status,
  tone,
  onClick,
}: {
  dimension: string;
  ask: string;
  source: string;
  status: string;
  tone: RagBucket;
  onClick?: () => void;
}) {
  return (
    <tr
      className={`border-t border-ice-100 align-top${onClick ? " cursor-pointer hover:bg-ice-50 transition" : ""}`}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClick(); } } : undefined}
      title={onClick ? `Click to navigate to ${dimension}` : undefined}
    >
      <td className="py-2 font-medium">{dimension}</td>
      <td className="text-xs italic text-navy/70">{ask}</td>
      <td className="font-mono text-xs">{source}</td>
      <td>
        <Badge tone={tone}>{status}</Badge>
      </td>
    </tr>
  );
}


function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="kpi-label">{label}</span>
      <span className="font-mono text-sm text-navy">{value}</span>
    </div>
  );
}

