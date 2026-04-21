import { Fragment, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
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

const WATERFALL_FIELD: Record<string, keyof typeof WATERFALL_LABELS> = {
  Gross: "gross_margin_pct",
  Contribution: "contribution_margin_pct",
  Portfolio: "portfolio_margin_pct",
  Net: "net_margin_pct",
};
const WATERFALL_LABELS = {
  gross_margin_pct: "Gross margin",
  contribution_margin_pct: "Contribution margin",
  portfolio_margin_pct: "Portfolio margin",
  net_margin_pct: "Net margin",
};

export function MarginEvm() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const [selectedWaterfallLayer, setSelectedWaterfallLayer] = useState<string | null>(null);
  const [selectedLossCategory, setSelectedLossCategory] = useState<string | null>(null);
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
          <p className="text-sm text-navy/70">No commercial scenarios seeded yet.</p>
        ) : (
          <>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={marginWaterfall}
                  margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
                  onClick={(chartData) => {
                    const label = chartData?.activePayload?.[0]?.payload?.label as string | undefined;
                    if (label) setSelectedWaterfallLayer(selectedWaterfallLayer === label ? null : label);
                  }}
                  style={{ cursor: "pointer" }}
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
                    labelFormatter={(label) => `${label} — click to drill into programme breakdown`}
                  />
                  <Bar dataKey="value" name="Margin" cursor="pointer">
                    {marginWaterfall.map((row, idx) => (
                      <Cell
                        key={idx}
                        fill={row.tone}
                        opacity={selectedWaterfallLayer && selectedWaterfallLayer !== row.label ? 0.4 : 1}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {selectedWaterfallLayer ? (() => {
              const field = WATERFALL_FIELD[selectedWaterfallLayer] as keyof (typeof latestCommercial)[0] | undefined;
              return (
                <div className="mt-4 rounded border border-ice-100 bg-ice-50/60 p-3 dark:border-navy-500 dark:bg-navy-600/40">
                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-sm font-semibold text-navy dark:text-navy-50">
                      {selectedWaterfallLayer} margin — per programme
                    </p>
                    <button
                      type="button"
                      onClick={() => setSelectedWaterfallLayer(null)}
                      className="text-xs text-navy/50 hover:text-navy dark:text-navy-100/50"
                    >
                      × close
                    </button>
                  </div>
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-xs uppercase text-navy/70">
                        <th className="py-1">Programme</th>
                        <th className="text-right">{selectedWaterfallLayer} margin %</th>
                        <th className="text-right">Revenue</th>
                        <th aria-hidden="true" />
                      </tr>
                    </thead>
                    <tbody>
                      {latestCommercial.map((row) => {
                        const pct = field ? (row[field] as number | null) : null;
                        const prog = programmes.data?.find((p) => p.id === row.program_id);
                        return (
                          <tr
                            key={row.id}
                            role="button"
                            tabIndex={0}
                            onClick={() => prog && navigate(`/margin?programme=${prog.code}`)}
                            onKeyDown={(e) => {
                              if ((e.key === "Enter" || e.key === " ") && prog) {
                                e.preventDefault();
                                navigate(`/margin?programme=${prog.code}`);
                              }
                            }}
                            className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50 dark:hover:bg-navy-600"
                            aria-label={prog ? `Drill into ${prog.code}` : undefined}
                          >
                            <td className="py-1.5 font-medium">{prog?.code ?? "—"}</td>
                            <td className="text-right font-mono">
                              {pct !== null && pct !== undefined ? (
                                <Badge
                                  tone={
                                    pct >= 0.22 ? "green" : pct >= 0.15 ? "amber" : "red"
                                  }
                                >
                                  {formatPct(pct)}
                                </Badge>
                              ) : "—"}
                            </td>
                            <td className="text-right font-mono text-navy/70">
                              {currency.format(row.revenue ?? 0, prog?.currency_code ?? "INR")}
                            </td>
                            <td className="pr-1 text-right text-navy/40 text-xs">→</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                  <p className="mt-2 text-xs text-navy/50">Click a row to drill into that programme's full Margin & EVM view.</p>
                </div>
              );
            })() : null}
          </>
        )}
      </Card>

      <Card>
        <CardHeader
          title="7 delivery losses"
          subtitle={`Total exposure ${currency.format(totalLosses, sourceCurrency)} — click a bar to see the records for that category`}
        />
        {(losses.data ?? []).length === 0 ? (
          <p className="text-sm text-navy/70">No loss exposure rows seeded.</p>
        ) : (() => {
          const lossRows = (losses.data ?? []).map((l) => ({
            ...l,
            programmeCode: programmes.data?.find((p) => p.id === l.program_id)?.code ?? "",
            category: l.loss_category,
            amount: l.amount ?? 0,
          }));
          const categoryTotals = Object.entries(
            lossRows.reduce<Record<string, number>>((acc, r) => {
              acc[r.category] = (acc[r.category] ?? 0) + r.amount;
              return acc;
            }, {})
          ).map(([category, amount]) => ({ category, amount }));

          const selectedRows = selectedLossCategory
            ? lossRows.filter((r) => r.category === selectedLossCategory)
            : [];

          return (
            <>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={categoryTotals}
                    margin={{ top: 8, right: 24, left: 0, bottom: 40 }}
                    layout="vertical"
                  >
                    <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                    <XAxis
                      type="number"
                      stroke="#1B2A4A"
                      tick={{ fontSize: 11 }}
                      tickFormatter={(v) => currency.format(Number(v), sourceCurrency)}
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
                      labelFormatter={(label) => `${label} — click to see individual records`}
                    />
                    <Bar
                      dataKey="amount"
                      name="Loss amount"
                      cursor="pointer"
                      onClick={(data: { category?: string }) => {
                        setSelectedLossCategory(
                          selectedLossCategory === (data.category ?? null) ? null : (data.category ?? null)
                        );
                      }}
                    >
                      {categoryTotals.map((row, idx) => (
                        <Cell
                          key={idx}
                          fill="#EF4444"
                          opacity={selectedLossCategory && selectedLossCategory !== row.category ? 0.35 : 1}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {selectedLossCategory && selectedRows.length > 0 ? (
                <div className="mt-4 rounded border border-danger-200 bg-danger-50/30 p-3 dark:border-navy-500 dark:bg-navy-600/40">
                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-sm font-semibold text-navy dark:text-navy-50">
                      {selectedLossCategory} — {selectedRows.length} record{selectedRows.length !== 1 ? "s" : ""}
                    </p>
                    <button
                      type="button"
                      onClick={() => setSelectedLossCategory(null)}
                      className="text-xs text-navy/50 hover:text-navy dark:text-navy-100/50"
                    >
                      × close
                    </button>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="text-left text-xs uppercase text-navy/70">
                          <th className="py-1">Programme</th>
                          <th className="text-right">Amount</th>
                          <th className="text-right">% Revenue</th>
                          <th>Status</th>
                          <th aria-hidden="true" />
                        </tr>
                      </thead>
                      <tbody>
                        {selectedRows.map((row) => (
                          <tr
                            key={row.id}
                            role="button"
                            tabIndex={0}
                            onClick={() => navigate(`/raid?programme=${row.programmeCode}`)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault();
                                navigate(`/raid?programme=${row.programmeCode}`);
                              }
                            }}
                            className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50 dark:hover:bg-navy-600"
                            aria-label={`Drill into ${row.programmeCode} risk register`}
                          >
                            <td className="py-1.5 font-medium">{row.programmeCode || "—"}</td>
                            <td className="text-right font-mono">
                              {currency.format(row.amount, sourceCurrency)}
                            </td>
                            <td className="text-right font-mono">
                              {row.percentage_of_revenue != null
                                ? `${(row.percentage_of_revenue * 100).toFixed(1)}%`
                                : "—"}
                            </td>
                            <td>
                              <Badge
                                tone={
                                  row.mitigation_status === "Mitigated"
                                    ? "green"
                                    : row.mitigation_status === "In Progress"
                                      ? "amber"
                                      : "red"
                                }
                              >
                                {row.mitigation_status ?? "—"}
                              </Badge>
                            </td>
                            <td className="pr-1 text-right text-xs text-navy/40">→ Risk register</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <p className="mt-2 text-xs text-navy/50">Click a row to drill into that programme's Risk & Audit log.</p>
                </div>
              ) : null}
            </>
          );
        })()}
      </Card>

      <Card>
        <CardHeader
          title="Rate-card drift"
          subtitle="Click a row to drill into that programme's Delivery Health"
        />
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-navy/70">
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
                <tr
                  key={row.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => navigate(`/delivery?programme=${row.programmeCode}`)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      navigate(`/delivery?programme=${row.programmeCode}`);
                    }
                  }}
                  className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50 focus-visible:bg-ice-50"
                  aria-label={`Drill into ${row.programmeCode} Delivery Health`}
                >
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
          <p className="text-sm text-navy/70">No change requests recorded.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-navy/70">
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

