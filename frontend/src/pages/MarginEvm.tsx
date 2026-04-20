import { useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
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
import { ChevronRight, Home, X } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
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
  const [searchParams, setSearchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();
  const currency = useCurrency();

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

  const clearProgrammeFilter = () => {
    const next = new URLSearchParams(searchParams);
    next.delete("programme");
    setSearchParams(next);
  };

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

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-navy">Margin & EVM</h1>
          <p className="mt-1 text-sm text-navy/70">
            Where is margin leaking and by how much? 4-layer margin waterfall
            plus the 7 delivery-loss categories from ARCHITECTURE.md §6.
          </p>
        </div>
        {filteredProgramme ? (
          <Link
            to={`/delivery?programme=${filteredProgramme.code}`}
            className="btn-ghost"
          >
            View Delivery Health <ChevronRight className="size-3" />
          </Link>
        ) : null}
      </div>

      {filteredProgramme ? (
        <div className="inline-flex items-center gap-2 self-start rounded-full border border-navy/30 bg-navy/5 px-3 py-1 text-xs text-navy">
          Filtered to <strong>{filteredProgramme.name}</strong>
          <button
            type="button"
            onClick={clearProgrammeFilter}
            className="inline-flex items-center rounded-full bg-navy/10 px-1.5 py-0.5 transition hover:bg-navy/20"
            aria-label="Clear programme filter (drill up)"
          >
            <X className="size-3" /> clear
          </button>
        </div>
      ) : null}

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
                </tr>
              </thead>
              <tbody>
                {(changeRequests.data ?? []).map((cr) => (
                  <tr key={cr.id} className="border-t border-ice-100">
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
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
