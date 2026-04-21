import { Fragment, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  AlertOctagon,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Clock,
  Home,
  Users,
} from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { ProgrammeFilterBar } from "@/components/ProgrammeFilterBar";
import { PROGRAMME_CROSS_LINKS } from "@/components/programmeCrossLinks";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
import {
  fetchResources,
  fetchScenarios,
  type ResourceRow,
  type ScenarioExecution,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { useCurrency } from "@/hooks/useCurrency";
import { formatPct, type RagBucket } from "@/lib/format";

const STATUS_TONE: Record<string, RagBucket | "neutral"> = {
  Active: "red",
  Mitigating: "amber",
  Monitoring: "amber",
  Resolved: "green",
  Acknowledged: "neutral",
};

export function SmartOps() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();
  const [filter, setFilter] = useState<string | null>(null);
  const [expandedScenario, setExpandedScenario] = useState<number | null>(null);
  const [expandedResource, setExpandedResource] = useState<number | null>(null);

  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );

  const scenarios = useQuery({
    queryKey: ["scenarios", filter],
    queryFn: () => fetchScenarios(filter ?? undefined),
  });
  const resources = useQuery({
    queryKey: ["resources"],
    queryFn: () => fetchResources(),
  });
  const currency = useCurrency();

  // Filter scenarios client-side to the programme when ?programme= is set —
  // scenario details contain a JSON string with "program":"CODE" inside.
  const visibleScenarios = useMemo(() => {
    const all = scenarios.data ?? [];
    if (!filteredProgramme) return all;
    return all.filter((s) =>
      (s.details ?? "").includes(`"${filteredProgramme.code}"`),
    );
  }, [scenarios.data, filteredProgramme]);

  const visibleResources = useMemo(() => {
    const all = resources.data ?? [];
    if (!filteredProgramme) return all;
    return all.filter(
      (r) => r.current_program_id === filteredProgramme.id,
    );
  }, [resources.data, filteredProgramme]);

  const activeCount = visibleScenarios.filter((s) => s.status === "Active").length;
  const mitigatingCount = visibleScenarios.filter(
    (s) => s.status === "Mitigating",
  ).length;
  const totalFinancialImpact = visibleScenarios.reduce(
    (sum, s) => sum + (s.financial_impact ?? 0),
    0,
  );
  const bench = visibleResources.filter((r) => r.status === "Bench");
  const benchCost = bench.reduce(
    (sum, r) => sum + ((r.loaded_cost_annual ?? 0) / 365) * r.bench_days,
    0,
  );

  const statuses = useMemo(() => {
    const set = new Set<string>();
    for (const s of scenarios.data ?? []) {
      if (s.status) set.add(s.status);
    }
    return [...set].sort();
  }, [scenarios.data]);

  const resourcePoolRef = useRef<HTMLDivElement>(null);

  const programmesMap = useMemo(
    () => new Map((programmes.data ?? []).map(p => [p.id, p.code])),
    [programmes.data],
  );

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
          { label: "Smart Ops", to: filteredProgramme ? "/smart-ops" : undefined },
          ...(filteredProgramme ? [{ label: filteredProgramme.name }] : []),
        ]}
      />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Smart Ops</h1>
        <p className="mt-1 text-sm text-navy/70">
          8 proactive-detection scenarios running continuously over the
          portfolio. Each triggered alert surfaces a financial impact
          estimate and a suggested action.
        </p>
      </div>

      <ProgrammeFilterBar
        currentRoute="/smart-ops"
        crossLinks={PROGRAMME_CROSS_LINKS}
      />

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <MetricCard metricId="scenario_alerts" label="Active alerts" value={`${activeCount}`} tone={activeCount === 0 ? "green" : "red"} onClick={() => setFilter("Active")} />
        <MetricCard metricId="mitigating_scenarios" value={`${mitigatingCount}`} tone={mitigatingCount > 0 ? "amber" : "green"} onClick={() => setFilter("Mitigating")} />
        <MetricCard
          metricId="risk_exposure"
          label="Financial impact"
          value={currency.format(totalFinancialImpact, "INR")}
          sub="Sum across visible alerts"
          onClick={() => navigate("/raid")}
        />
        <MetricCard
          metricId="bench_cost"
          value={currency.format(benchCost, "INR")}
          sub={`${bench.length} FTE on bench`}
          onClick={() => resourcePoolRef.current?.scrollIntoView({ behavior: 'smooth' })}
        />
      </section>

      <Card>
        <CardHeader
          title="Scenario alerts"
          subtitle={`${visibleScenarios.length} shown · click any row to expand`}
          action={
            <div className="flex flex-wrap gap-1">
              <button
                type="button"
                onClick={() => setFilter(null)}
                className={`rounded-full px-3 py-1 text-xs transition ${
                  filter === null ? "bg-navy text-white" : "bg-ice-50 text-navy hover:bg-ice-100"
                }`}
              >
                All
              </button>
              {statuses.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setFilter(s)}
                  className={`rounded-full px-3 py-1 text-xs transition ${
                    filter === s ? "bg-navy text-white" : "bg-ice-50 text-navy hover:bg-ice-100"
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          }
        />
        {visibleScenarios.length === 0 ? (
          <p className="text-sm text-navy/70">No scenario executions match the current scope.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {visibleScenarios.map((s) => (
              <ScenarioRow
                key={s.id}
                scenario={s}
                isOpen={expandedScenario === s.id}
                onToggle={() =>
                  setExpandedScenario(expandedScenario === s.id ? null : s.id)
                }
                sourceCurrency="INR"
              />
            ))}
          </ul>
        )}
      </Card>

      <div ref={resourcePoolRef}>
      <Card>
        <CardHeader
          title="Resource pool"
          subtitle={`${visibleResources.length} people · ${bench.length} on bench`}
          action={<Users className="size-4 text-navy/70" aria-hidden="true" />}
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/70">
                <th className="py-2">Name</th>
                <th>Role</th>
                <th>Tier</th>
                <th className="text-right">Utilisation</th>
                <th className="text-right">Bench days</th>
                <th className="text-right">Loaded cost/yr</th>
                <th>Status</th>
                <th aria-hidden="true" />
              </tr>
            </thead>
            <tbody>
              {visibleResources.map((r) => (
                <ResourceRowView
                  key={r.id}
                  row={r}
                  isOpen={expandedResource === r.id}
                  onToggle={() =>
                    setExpandedResource(expandedResource === r.id ? null : r.id)
                  }
                  currencyFormat={currency.format}
                  programmesMap={programmesMap}
                />
              ))}
            </tbody>
          </table>
        </div>
      </Card>
      </div>
    </div>
  );
}

function ScenarioRow({
  scenario,
  sourceCurrency,
  isOpen,
  onToggle,
}: {
  scenario: ScenarioExecution;
  sourceCurrency: string;
  isOpen: boolean;
  onToggle: () => void;
}) {
  const currency = useCurrency();
  const tone = STATUS_TONE[scenario.status ?? ""] ?? "neutral";
  let parsedDetails: Record<string, unknown> | null = null;
  try {
    if (scenario.details) {
      parsedDetails = JSON.parse(scenario.details) as Record<string, unknown>;
    }
  } catch {
    parsedDetails = null;
  }
  return (
    <li className="rounded border border-ice-100 bg-white">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={isOpen}
        className="flex w-full items-start justify-between gap-3 px-3 py-2 text-left transition hover:bg-ice-50"
      >
        <div className="flex flex-1 flex-col gap-1">
          <div className="flex items-center gap-2">
            <AlertOctagon
              className={`size-4 ${
                scenario.status === "Active" ? "text-danger-600" : "text-amber-500"
              }`}
              aria-hidden="true"
            />
            <span className="font-semibold">{scenario.scenario_name}</span>
            <Badge tone={tone}>{scenario.status ?? "—"}</Badge>
          </div>
          <p className="text-xs text-navy/70">
            <Clock className="inline size-3" aria-hidden="true" />{" "}
            {scenario.execution_date
              ? new Date(scenario.execution_date).toLocaleString("en-GB")
              : "—"}
            {" · "}
            triggered by {scenario.triggered_by ?? "—"}
          </p>
        </div>
        <div className="flex items-center gap-2 font-mono text-sm">
          {currency.format(scenario.financial_impact, sourceCurrency)}
          {isOpen ? (
            <ChevronUp className="size-4 text-navy/40" aria-hidden="true" />
          ) : (
            <ChevronDown className="size-4 text-navy/40" aria-hidden="true" />
          )}
        </div>
      </button>
      {isOpen ? (
        <div className="flex flex-col gap-2 px-3 pb-3 text-xs">
          {parsedDetails ? (
            <dl className="grid grid-cols-2 gap-3 md:grid-cols-4">
              {Object.entries(parsedDetails).map(([k, v]) => (
                <div key={k} className="flex flex-col">
                  <span className="kpi-label">{k}</span>
                  <span className="font-mono text-navy">{String(v)}</span>
                </div>
              ))}
            </dl>
          ) : scenario.details ? (
            <pre className="overflow-x-auto rounded bg-ice-50 p-2 font-mono text-[11px]">
              {scenario.details}
            </pre>
          ) : null}
          {scenario.outcome_notes ? (
            <p className="italic text-navy/80">
              Proposed action: {scenario.outcome_notes}
            </p>
          ) : null}
          {(() => {
            const progCode = (parsedDetails?.programme ?? parsedDetails?.program ?? null) as string | null;
            if (!progCode) return null;
            return (
              <div className="mt-2 flex flex-wrap gap-2">
                <Link to={`/raid?programme=${progCode}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">→ Risk Register</Link>
                <Link to={`/delivery?programme=${progCode}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">→ Delivery Health</Link>
              </div>
            );
          })()}
        </div>
      ) : null}
    </li>
  );
}

function ResourceRowView({
  row,
  isOpen,
  onToggle,
  currencyFormat,
  programmesMap,
}: {
  row: ResourceRow;
  isOpen: boolean;
  onToggle: () => void;
  currencyFormat: (amount: number | null, src: string) => string;
  programmesMap: Map<number, string>;
}) {
  return (
    <Fragment>
      <tr
        role="button"
        tabIndex={0}
        onClick={onToggle}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            onToggle();
          }
        }}
        className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50"
        aria-expanded={isOpen}
      >
        <td className="py-2 font-medium">{row.name}</td>
        <td>{row.role ?? "—"}</td>
        <td>{row.role_tier ?? "—"}</td>
        <td className="text-right font-mono">
          {row.utilization_pct === null ? "—" : formatPct(row.utilization_pct / 100)}
        </td>
        <td className="text-right font-mono">
          <Badge tone={row.bench_days > 0 ? "red" : "green"}>
            {row.bench_days === 0 ? (
              <CheckCircle2 className="size-3" aria-hidden="true" />
            ) : null}
            {row.bench_days}d
          </Badge>
        </td>
        <td className="text-right font-mono">
          {currencyFormat(row.loaded_cost_annual, "INR")}
        </td>
        <td>
          <Badge tone={row.status === "Bench" ? "red" : "green"}>{row.status}</Badge>
        </td>
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
          <td colSpan={8} className="px-3 py-3 text-xs text-navy/80">
            <dl className="grid grid-cols-2 gap-3 md:grid-cols-4">
              <Detail label="Skills" value={row.skill_set ?? "—"} />
              <Detail
                label="Current programme"
                value={row.current_program_id ? (programmesMap.get(row.current_program_id) ?? `#${row.current_program_id}`) : "—"}
              />
              <Detail
                label="Current project"
                value={row.current_project_id ? `#${row.current_project_id}` : "—"}
              />
              <Detail
                label="Bench daily drag"
                value={
                  row.loaded_cost_annual
                    ? currencyFormat(row.loaded_cost_annual / 365, "INR")
                    : "—"
                }
              />
            </dl>
            {row.current_program_id && programmesMap.get(row.current_program_id) && (
              <div className="mt-3 flex flex-wrap gap-2">
                <Link to={`/delivery?programme=${programmesMap.get(row.current_program_id)}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">→ Delivery Health</Link>
                <Link to={`/velocity?programme=${programmesMap.get(row.current_program_id)}`} className="rounded-full border border-ice-100 bg-white px-2 py-0.5 text-xs text-navy hover:bg-ice-50">→ Velocity & Flow</Link>
              </div>
            )}
          </td>
        </tr>
      ) : null}
    </Fragment>
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

