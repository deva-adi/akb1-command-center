import { Fragment, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ChevronDown, ChevronUp, Home } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { ProgrammeFilterBar } from "@/components/ProgrammeFilterBar";
import { PROGRAMME_CROSS_LINKS } from "@/components/programmeCrossLinks";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  fetchChangeRequests,
  fetchCommercial,
  fetchLosses,
  fetchRateCards,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { useCurrency } from "@/hooks/useCurrency";
import { formatPct } from "@/lib/format";

export function MarginEvm() {
  const [searchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();
  const currency = useCurrency();
  const [expandedCr, setExpandedCr] = useState<number | null>(null);

  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );
  const sourceCurrency = filteredProgramme?.currency_code ?? "INR";

  const commercial = useQuery({
    queryKey: ["commercial", filteredProgramme?.id ?? null],
    queryFn: () => fetchCommercial(filteredProgramme?.id),
  });
  const losses = useQuery({
    queryKey: ["losses", filteredProgramme?.id ?? null],
    queryFn: () => fetchLosses(filteredProgramme?.id),
  });
  const rateCards = useQuery({
    queryKey: ["rate-cards", filteredProgramme?.id ?? null],
    queryFn: () => fetchRateCards(filteredProgramme?.id),
  });
  const changeRequests = useQuery({
    queryKey: ["change-requests", filteredProgramme?.id ?? null],
    queryFn: () => fetchChangeRequests(filteredProgramme?.id),
  });


  // Latest commercial per programme — for the 4-layer margin waterfall.
  const latestCommercial = useMemo(() => {
    const rows = commercial.data ?? [];
    const byProgramme = new Map<number, (typeof rows)[number]>();
    for (const r of rows) {
      if (r.program_id === null) continue;
      const existing = byProgramme.get(r.program_id);
      if (
        !existing ||
        (r.snapshot_date ?? "") > (existing.snapshot_date ?? "")
      ) {
        byProgramme.set(r.program_id, r);
      }
    }
    return Array.from(byProgramme.values());
  }, [commercial.data]);

  const marginWaterfall = useMemo(() => {
    if (latestCommercial.length === 0) return [];
    const avg = (pick: (row: (typeof latestCommercial)[number]) => number | null) =>
      latestCommercial.reduce((sum, r) => sum + (pick(r) ?? 0), 0) /
      latestCommercial.length;
    return [
      { label: "Gross", value: avg((r) => r.gross_margin_pct), tone: "#1B2A4A" },
      {
        label: "Contribution",
        value: avg((r) => r.contribution_margin_pct),
        tone: "#3B82F6",
      },
      {
        label: "Portfolio",
        value: avg((r) => r.portfolio_margin_pct),
        tone: "#F59E0B",
      },
      { label: "Net", value: avg((r) => r.net_margin_pct), tone: "#10B981" },
    ];
  }, [latestCommercial]);

  // Rate-card drift rows (actual vs planned) per role tier × programme.
  const rateCardRows = useMemo(() => {
    return (rateCards.data ?? []).map((row) => {
      const drift =
        row.actual_rate !== null && row.planned_rate > 0
          ? (row.actual_rate - row.planned_rate) / row.planned_rate
          : null;
      return {
        ...row,
        drift,
        programmeCode:
          programmes.data?.find((p) => p.id === row.program_id)?.code ?? "—",
      };
    });
  }, [rateCards.data, programmes.data]);

  const totalLosses = (losses.data ?? []).reduce(
    (sum, l) => sum + (l.amount ?? 0),
    0,
  );

  const breadcrumbItems = [
    { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
    { label: "Margin & EVM", to: filteredProgramme ? "/margin" : undefined },
    ...(filteredProgramme ? [{ label: filteredProgramme.name }] : []),
  ];

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumbItems} />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Margin & EVM</h1>
        <p className="mt-1 text-sm text-navy/70">
          Where is margin leaking and by how much? 4-layer margin waterfall
          plus the 7 delivery-loss categories from ARCHITECTURE.md §6.
        </p>
      </div>

      <ProgrammeFilterBar
        currentRoute="/margin"
        crossLinks={PROGRAMME_CROSS_LINKS}
      />

      <Card>
        <CardHeader
          title="4-layer margin waterfall"
          subtitle={
            filteredProgramme
              ? `Latest scenario for ${filteredProgramme.name}`
              : "Latest portfolio average across programmes"
          }
        />
        {marginWaterfall.length === 0 ? (
          <p className="text-sm text-navy/60">No commercial scenarios seeded yet.</p>
        ) : (
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={marginWaterfall}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="label" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <YAxis
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                />
                <Tooltip
                  formatter={(v: number) => `${(v * 100).toFixed(1)}%`}
                  contentStyle={{ border: "1px solid #D5E8F0" }}
                />
                <Bar dataKey="value" name="Margin">
                  {marginWaterfall.map((row, idx) => (
                    <Cell key={idx} fill={row.tone} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </Card>

      <Card>
        <CardHeader
          title="7 delivery losses"
          subtitle={`Total exposure ${currency.format(totalLosses, sourceCurrency)} across seven categories (ARCHITECTURE.md §6)`}
        />
        {(losses.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/60">No loss exposure rows seeded.</p>
        ) : (
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={(losses.data ?? []).map((l) => ({
                  category: l.loss_category,
                  amount: l.amount ?? 0,
                  pct: l.percentage_of_revenue ?? 0,
                  programmeCode:
                    programmes.data?.find((p) => p.id === l.program_id)?.code ?? "",
                  status: l.mitigation_status,
                }))}
                margin={{ top: 8, right: 24, left: 0, bottom: 40 }}
                layout="vertical"
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis
                  type="number"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 11 }}
                  tickFormatter={(v) =>
                    currency.format(Number(v), sourceCurrency)
                  }
                />
                <YAxis
                  type="category"
                  dataKey="category"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 11 }}
                  width={180}
                />
                <Tooltip
                  formatter={(v: number) => currency.format(v, sourceCurrency)}
                  contentStyle={{ border: "1px solid #D5E8F0" }}
                />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="amount" name="Loss amount" fill="#EF4444" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </Card>

      <Card>
        <CardHeader
          title="Rate-card drift"
          subtitle="Planned vs actual blended rate per role tier"
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/60">
                <th className="py-2">Programme</th>
                <th>Role tier</th>
                <th className="text-right">Planned</th>
                <th className="text-right">Actual</th>
                <th className="text-right">Drift</th>
                <th className="text-right">HC (plan → actual)</th>
              </tr>
            </thead>
            <tbody>
              {rateCardRows.map((row) => (
                <tr key={row.id} className="border-t border-ice-100">
                  <td className="py-2 font-medium">{row.programmeCode}</td>
                  <td>{row.role_tier}</td>
                  <td className="text-right font-mono">
                    {row.planned_rate.toFixed(0)}
                  </td>
                  <td className="text-right font-mono">
                    {(row.actual_rate ?? 0).toFixed(0)}
                  </td>
                  <td className="text-right font-mono">
                    {row.drift === null ? (
                      "—"
                    ) : (
                      <Badge
                        tone={
                          Math.abs(row.drift) < 0.05
                            ? "green"
                            : Math.abs(row.drift) < 0.1
                              ? "amber"
                              : "red"
                        }
                      >
                        {formatPct(row.drift)}
                      </Badge>
                    )}
                  </td>
                  <td className="text-right font-mono text-navy/70">
                    {row.planned_headcount ?? "—"} → {row.actual_headcount ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card>
        <CardHeader
          title="Change requests"
          subtitle="CR log with margin impact and billable flag"
        />
        {(changeRequests.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/60">No change requests recorded.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-navy/60">
                  <th className="py-2">Date</th>
                  <th>Description</th>
                  <th className="text-right">Effort (h)</th>
                  <th className="text-right">Value</th>
                  <th className="text-right">Margin Δ</th>
                  <th>Status</th>
                  <th aria-hidden="true" />
                </tr>
              </thead>
              <tbody>
                {(changeRequests.data ?? []).map((cr) => {
                  const isOpen = expandedCr === cr.id;
                  const cost =
                    currency.format(cr.processing_cost, sourceCurrency);
                  return (
                    <Fragment key={cr.id}>
                      <tr
                        role="button"
                        tabIndex={0}
                        onClick={() => setExpandedCr(isOpen ? null : cr.id)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" || e.key === " ") {
                            e.preventDefault();
                            setExpandedCr(isOpen ? null : cr.id);
                          }
                        }}
                        className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50"
                        aria-expanded={isOpen}
                      >
                        <td className="py-2 font-mono text-xs">{cr.cr_date}</td>
                        <td>
                          <p className="font-medium">{cr.cr_description ?? "—"}</p>
                          {cr.is_billable === false ? (
                            <span className="text-xs text-danger-600">non-billable</span>
                          ) : null}
                        </td>
                        <td className="text-right font-mono">
                          {cr.effort_hours ?? "—"}
                        </td>
                        <td className="text-right font-mono">
                          {currency.format(cr.cr_value, sourceCurrency)}
                        </td>
                        <td className="text-right font-mono">
                          <Badge
                            tone={
                              cr.margin_impact === null
                                ? "neutral"
                                : cr.margin_impact >= 0
                                  ? "green"
                                  : cr.margin_impact >= -1
                                    ? "amber"
                                    : "red"
                            }
                          >
                            {formatPct(cr.margin_impact === null ? null : cr.margin_impact / 100)}
                          </Badge>
                        </td>
                        <td>
                          <Badge
                            tone={
                              cr.status === "Approved"
                                ? "green"
                                : cr.status === "Pending" || cr.status === "In Review"
                                  ? "amber"
                                  : "neutral"
                            }
                          >
                            {cr.status ?? "—"}
                          </Badge>
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
                          <td colSpan={7} className="px-3 py-3 text-xs text-navy/80">
                            <dl className="grid grid-cols-2 gap-3 md:grid-cols-4">
                              <Detail label="Processing cost" value={cost} />
                              <Detail
                                label="Net impact"
                                value={currency.format(
                                  (cr.cr_value ?? 0) - (cr.processing_cost ?? 0),
                                  sourceCurrency,
                                )}
                              />
                              <Detail
                                label="Billable"
                                value={cr.is_billable === false ? "No" : "Yes"}
                              />
                              <Detail
                                label="Programme"
                                value={
                                  programmes.data?.find(
                                    (p) => p.id === cr.program_id,
                                  )?.code ?? "—"
                                }
                              />
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

