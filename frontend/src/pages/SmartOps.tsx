import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertOctagon, CheckCircle2, Clock, Home, Users } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  fetchResources,
  fetchScenarios,
  type ScenarioExecution,
  type ResourceRow,
} from "@/lib/api";
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
  const [filter, setFilter] = useState<string | null>(null);
  const scenarios = useQuery({
    queryKey: ["scenarios", filter],
    queryFn: () => fetchScenarios(filter ?? undefined),
  });
  const resources = useQuery({
    queryKey: ["resources"],
    queryFn: () => fetchResources(),
  });
  const currency = useCurrency();

  const activeCount = (scenarios.data ?? []).filter(
    (s) => s.status === "Active",
  ).length;
  const mitigatingCount = (scenarios.data ?? []).filter(
    (s) => s.status === "Mitigating",
  ).length;
  const totalFinancialImpact = (scenarios.data ?? []).reduce(
    (sum, s) => sum + (s.financial_impact ?? 0),
    0,
  );
  const bench = (resources.data ?? []).filter((r) => r.status === "Bench");
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

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
          { label: "Smart Ops" },
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

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <Stat label="Active alerts" value={`${activeCount}`} tone={activeCount === 0 ? "green" : "red"} />
        <Stat label="Mitigating" value={`${mitigatingCount}`} tone={mitigatingCount > 0 ? "amber" : "green"} />
        <Stat
          label="Financial impact"
          value={currency.format(totalFinancialImpact, "INR")}
          sub="Sum across active + mitigating alerts"
        />
        <Stat
          label="Bench cost (YTD-ish)"
          value={currency.format(benchCost, "INR")}
          sub={`${bench.length} FTE on bench`}
        />
      </section>

      <Card>
        <CardHeader
          title="Scenario alerts"
          subtitle="Filter by status"
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
        {(scenarios.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/60">No scenario executions match the filter.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {(scenarios.data ?? []).map((s) => (
              <ScenarioRow key={s.id} scenario={s} sourceCurrency="INR" />
            ))}
          </ul>
        )}
      </Card>

      <Card>
        <CardHeader
          title="Resource pool"
          subtitle={`${resources.data?.length ?? 0} people · ${bench.length} on bench`}
          action={<Users className="size-4 text-navy/60" aria-hidden="true" />}
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/60">
                <th className="py-2">Name</th>
                <th>Role</th>
                <th>Tier</th>
                <th className="text-right">Utilisation</th>
                <th className="text-right">Bench days</th>
                <th className="text-right">Loaded cost/yr</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {(resources.data ?? []).map((r) => (
                <ResourceRowView key={r.id} row={r} currencyFormat={currency.format} />
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

function ScenarioRow({
  scenario,
  sourceCurrency,
}: {
  scenario: ScenarioExecution;
  sourceCurrency: string;
}) {
  const currency = useCurrency();
  const tone = STATUS_TONE[scenario.status ?? ""] ?? "neutral";
  return (
    <li className="flex items-start justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2">
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
        {scenario.details ? (
          <p className="rounded bg-ice-50 px-2 py-1 font-mono text-xs">{scenario.details}</p>
        ) : null}
        {scenario.outcome_notes ? (
          <p className="text-xs italic text-navy/70">Action: {scenario.outcome_notes}</p>
        ) : null}
        <p className="text-xs text-navy/60">
          <Clock className="inline size-3" aria-hidden="true" />{" "}
          {scenario.execution_date
            ? new Date(scenario.execution_date).toLocaleString("en-GB")
            : "—"}
          {" · "}
          triggered by {scenario.triggered_by ?? "—"}
        </p>
      </div>
      <div className="text-right font-mono text-sm">
        {currency.format(scenario.financial_impact, sourceCurrency)}
      </div>
    </li>
  );
}

function ResourceRowView({
  row,
  currencyFormat,
}: {
  row: ResourceRow;
  currencyFormat: (amount: number | null, src: string) => string;
}) {
  return (
    <tr className="border-t border-ice-100">
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
