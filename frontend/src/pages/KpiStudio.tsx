import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
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
import { BookOpen, ChevronRight, Home, Pencil, Save, X } from "lucide-react";
import { Breadcrumb } from "@/components/Breadcrumb";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  fetchKpiDefinitions,
  fetchKpiSnapshots,
  fetchProgrammes,
  type KpiDefinition,
  updateKpiWeight,
} from "@/lib/api";
import { cn } from "@/lib/cn";
import type { RagBucket } from "@/lib/format";

type ToneOrNeutral = RagBucket | "neutral";

function thresholdTone(value: number, kpi: KpiDefinition): ToneOrNeutral {
  const { green_threshold: g, amber_threshold: a, red_threshold: r } = kpi;
  if (g === null || a === null || r === null) return "neutral";
  if (kpi.is_higher_better) {
    if (value >= g) return "green";
    if (value >= a) return "amber";
    return "red";
  }
  if (value <= g) return "green";
  if (value <= a) return "amber";
  return "red";
}

function formatValue(value: number, kpi: KpiDefinition): string {
  const unit = kpi.unit ?? "";
  if (unit === "pct") return `${(value * 100).toFixed(1)}%`;
  if (unit === "ratio") return value.toFixed(2);
  if (unit === "score_0_100") return value.toFixed(0);
  if (unit.includes("defects")) return value.toFixed(2);
  return value.toFixed(2);
}

export function KpiStudio() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const [selectedKpiId, setSelectedKpiId] = useState<number | null>(null);
  const [formulaOpen, setFormulaOpen] = useState(false);
  const [editingWeight, setEditingWeight] = useState<{ id: number; value: string } | null>(null);
  const [weightError, setWeightError] = useState<string | null>(null);

  const definitions = useQuery({
    queryKey: ["kpi-definitions"],
    queryFn: () => fetchKpiDefinitions(),
  });
  const programmes = useQuery({
    queryKey: ["programmes"],
    queryFn: fetchProgrammes,
  });

  const selectedKpi = useMemo(
    () => definitions.data?.find((k) => k.id === selectedKpiId) ?? null,
    [definitions.data, selectedKpiId],
  );

  useEffect(() => {
    if (!selectedKpi && definitions.data && definitions.data.length > 0) {
      setSelectedKpiId(definitions.data[0].id);
    }
  }, [definitions.data, selectedKpi]);

  // When a programme filter is set, pass it through to the snapshot query so
  // the chart + table focus on a single programme for drill-down.
  const filteredProgramme = useMemo(
    () => programmes.data?.find((p) => p.code === programmeFilter) ?? null,
    [programmes.data, programmeFilter],
  );

  const snapshots = useQuery({
    queryKey: [
      "kpi-snapshots",
      "studio",
      selectedKpi?.code ?? null,
      filteredProgramme?.id ?? null,
    ],
    queryFn: () =>
      selectedKpi
        ? fetchKpiSnapshots({
            kpiCode: selectedKpi.code,
            programId: filteredProgramme?.id,
          })
        : Promise.resolve([]),
    enabled: selectedKpi !== null,
  });

  const clearProgrammeFilter = () => {
    const next = new URLSearchParams(searchParams);
    next.delete("programme");
    setSearchParams(next);
  };

  const weightMutation = useMutation({
    mutationFn: ({ id, weight }: { id: number; weight: number }) =>
      updateKpiWeight(id, weight),
    onSuccess: (updated) => {
      queryClient.setQueryData<KpiDefinition[] | undefined>(
        ["kpi-definitions"],
        (prev) => prev?.map((k) => (k.id === updated.id ? updated : k)),
      );
      setEditingWeight(null);
      setWeightError(null);
    },
    onError: (err) => {
      setWeightError((err as Error).message);
    },
  });

  const grouped = useMemo(() => {
    const categories = new Map<string, KpiDefinition[]>();
    for (const kpi of definitions.data ?? []) {
      const key = kpi.category ?? "Uncategorised";
      const list = categories.get(key) ?? [];
      list.push(kpi);
      categories.set(key, list);
    }
    return Array.from(categories.entries()).sort(([a], [b]) => a.localeCompare(b));
  }, [definitions.data]);

  const chartData = useMemo(() => {
    if (!snapshots.data || !programmes.data) return [];
    const codeById = new Map(programmes.data.map((p) => [p.id, p.code]));
    const byMonth = new Map<string, Record<string, number | string>>();
    for (const s of snapshots.data) {
      if (s.program_id === null) continue;
      const code = codeById.get(s.program_id);
      if (!code) continue;
      const monthKey = s.snapshot_date.slice(0, 7);
      const bucket = byMonth.get(monthKey) ?? {
        month: monthKey,
        monthLabel: monthLabel(monthKey),
      };
      bucket[code] = s.value;
      byMonth.set(monthKey, bucket);
    }
    return Array.from(byMonth.values()).sort((a, b) =>
      String(a.month).localeCompare(String(b.month)),
    );
  }, [snapshots.data, programmes.data]);

  const activeProgrammes = useMemo(() => {
    if (!snapshots.data || !programmes.data) return [];
    const ids = new Set(snapshots.data.map((s) => s.program_id).filter((v): v is number => v !== null));
    return programmes.data.filter((p) => ids.has(p.id));
  }, [snapshots.data, programmes.data]);

  if (definitions.isLoading) {
    return <p className="text-sm text-navy/70">Loading KPI library…</p>;
  }
  if (definitions.error) {
    return <p className="text-sm text-danger-600">{(definitions.error as Error).message}</p>;
  }

  const breadcrumbItems = [
    { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
    { label: "KPI Studio", to: filteredProgramme || selectedKpi ? "/kpi" : undefined },
    ...(filteredProgramme
      ? [
          {
            label: filteredProgramme.name,
            to: selectedKpi ? `/kpi?programme=${filteredProgramme.code}` : undefined,
          },
        ]
      : []),
    ...(selectedKpi ? [{ label: selectedKpi.name }] : []),
  ];

  return (
    <div className="flex flex-col gap-4">
      <Breadcrumb items={breadcrumbItems} />

      {filteredProgramme ? (
        <div className="inline-flex items-center gap-2 self-start rounded-full border border-navy/30 bg-navy/5 px-3 py-1 text-xs text-navy">
          Focused on <strong>{filteredProgramme.name}</strong>
          <button
            type="button"
            onClick={clearProgrammeFilter}
            className="inline-flex items-center rounded-full bg-navy/10 px-1.5 py-0.5 transition hover:bg-navy/20"
            aria-label="Clear programme filter (drill up)"
          >
            <X className="size-3" /> clear
          </button>
          <Link
            to={`/delivery?programme=${filteredProgramme.code}`}
            className="ml-1 inline-flex items-center gap-1 text-navy hover:underline"
          >
            View in Delivery Health
            <ChevronRight className="size-3" />
          </Link>
        </div>
      ) : null}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr]">
      <aside className="flex flex-col gap-4">
        <Card>
          <CardHeader
            title="KPI library"
            subtitle={`${definitions.data?.length ?? 0} definitions`}
          />
          <div className="flex flex-col gap-3">
            {grouped.map(([category, kpis]) => (
              <div key={category}>
                <p className="kpi-label">{category}</p>
                <ul className="mt-1 flex flex-col gap-1">
                  {kpis.map((kpi) => (
                    <li key={kpi.id}>
                      <button
                        type="button"
                        onClick={() => setSelectedKpiId(kpi.id)}
                        className={cn(
                          "flex w-full items-center justify-between rounded px-2 py-1.5 text-left text-sm",
                          selectedKpiId === kpi.id
                            ? "bg-navy text-white"
                            : "text-navy hover:bg-ice-50",
                        )}
                      >
                        <span>{kpi.name}</span>
                        <span className="font-mono text-xs text-current/70">
                          ×{kpi.weight.toFixed(1)}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </Card>
      </aside>

      <section className="flex flex-col gap-6">
        {selectedKpi ? (
          <>
            <Card>
              <CardHeader
                title={selectedKpi.name}
                subtitle={`${selectedKpi.category ?? "—"} · higher is ${selectedKpi.is_higher_better ? "better" : "worse"}`}
                action={
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setFormulaOpen(true)}
                      className="btn-ghost"
                    >
                      <BookOpen className="size-3.5" /> Formula
                    </button>
                  </div>
                }
              />
              <dl className="grid grid-cols-2 gap-4 text-sm md:grid-cols-4">
                <StatCell
                  label="Green threshold"
                  value={selectedKpi.green_threshold !== null ? formatValue(selectedKpi.green_threshold, selectedKpi) : "—"}
                  tone="green"
                />
                <StatCell
                  label="Amber threshold"
                  value={selectedKpi.amber_threshold !== null ? formatValue(selectedKpi.amber_threshold, selectedKpi) : "—"}
                  tone="amber"
                />
                <StatCell
                  label="Red threshold"
                  value={selectedKpi.red_threshold !== null ? formatValue(selectedKpi.red_threshold, selectedKpi) : "—"}
                  tone="red"
                />
                <div>
                  <dt className="kpi-label">Weight</dt>
                  {editingWeight?.id === selectedKpi.id ? (
                    <div className="mt-1 flex items-center gap-2">
                      <input
                        type="number"
                        min={0}
                        max={10}
                        step={0.1}
                        value={editingWeight.value}
                        onChange={(e) =>
                          setEditingWeight({ ...editingWeight, value: e.target.value })
                        }
                        className="w-20 rounded border border-ice-100 px-2 py-1 font-mono text-sm"
                        autoFocus
                      />
                      <button
                        type="button"
                        onClick={() => {
                          const parsed = Number(editingWeight.value);
                          if (Number.isNaN(parsed) || parsed < 0 || parsed > 10) {
                            setWeightError("Weight must be between 0 and 10");
                            return;
                          }
                          weightMutation.mutate({ id: selectedKpi.id, weight: parsed });
                        }}
                        className="btn-primary px-2 py-1 text-xs"
                        disabled={weightMutation.isPending}
                      >
                        <Save className="size-3" /> Save
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setEditingWeight(null);
                          setWeightError(null);
                        }}
                        className="btn-ghost px-2 py-1 text-xs"
                      >
                        <X className="size-3" />
                      </button>
                    </div>
                  ) : (
                    <div className="mt-1 flex items-center gap-2">
                      <dd className="font-mono text-2xl font-semibold">
                        {selectedKpi.weight.toFixed(1)}
                      </dd>
                      <button
                        type="button"
                        onClick={() =>
                          setEditingWeight({
                            id: selectedKpi.id,
                            value: selectedKpi.weight.toString(),
                          })
                        }
                        className="btn-ghost px-2 py-1 text-xs"
                      >
                        <Pencil className="size-3" /> Edit
                      </button>
                    </div>
                  )}
                  {weightError ? (
                    <p className="mt-1 text-xs text-danger-600">{weightError}</p>
                  ) : null}
                </div>
              </dl>
              {selectedKpi.description ? (
                <p className="mt-4 text-sm text-navy/70">{selectedKpi.description}</p>
              ) : null}
            </Card>

            <Card>
              <CardHeader
                title="Trend"
                subtitle="12-month snapshots, per programme"
              />
              <div className="h-80">
                {chartData.length === 0 ? (
                  <p className="grid h-full place-items-center text-sm text-navy/70">
                    No snapshots for this KPI yet.
                  </p>
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData} margin={{ top: 8, right: 24, left: 0, bottom: 8 }}>
                      <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                      <XAxis dataKey="monthLabel" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                      <YAxis
                        stroke="#1B2A4A"
                        tick={{ fontSize: 12 }}
                        tickFormatter={(v) => formatValue(Number(v), selectedKpi)}
                      />
                      <Tooltip
                        formatter={(value: number) => formatValue(value, selectedKpi)}
                        contentStyle={{ border: "1px solid #D5E8F0" }}
                      />
                      <Legend wrapperStyle={{ fontSize: 12 }} />
                      {selectedKpi.green_threshold !== null ? (
                        <ReferenceLine
                          y={selectedKpi.green_threshold}
                          stroke="#10B981"
                          strokeDasharray="4 4"
                          label={{
                            value: "Green",
                            position: "right",
                            fill: "#10B981",
                            fontSize: 11,
                          }}
                        />
                      ) : null}
                      {selectedKpi.amber_threshold !== null ? (
                        <ReferenceLine
                          y={selectedKpi.amber_threshold}
                          stroke="#F59E0B"
                          strokeDasharray="4 4"
                          label={{
                            value: "Amber",
                            position: "right",
                            fill: "#F59E0B",
                            fontSize: 11,
                          }}
                        />
                      ) : null}
                      {selectedKpi.red_threshold !== null ? (
                        <ReferenceLine
                          y={selectedKpi.red_threshold}
                          stroke="#EF4444"
                          strokeDasharray="4 4"
                          label={{
                            value: "Red",
                            position: "right",
                            fill: "#EF4444",
                            fontSize: 11,
                          }}
                        />
                      ) : null}
                      {activeProgrammes.map((p, idx) => (
                        <Line
                          key={p.id}
                          type="monotone"
                          dataKey={p.code}
                          stroke={seriesColors[idx % seriesColors.length]}
                          strokeWidth={2}
                          dot={false}
                          name={p.code}
                        />
                      ))}
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </div>
            </Card>

            <Card>
              <CardHeader
                title="Latest values"
                subtitle="Click any programme to drill into Delivery Health"
              />
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs uppercase text-navy/70">
                      <th className="py-2">Programme</th>
                      <th className="text-right">Latest</th>
                      <th className="text-right">Status</th>
                      <th aria-hidden="true" />
                    </tr>
                  </thead>
                  <tbody>
                    {activeProgrammes.map((p) => {
                      const latest = latestForProgramme(p.id, snapshots.data ?? []);
                      if (latest === null) return null;
                      const tone = thresholdTone(latest, selectedKpi);
                      return (
                        <tr
                          key={p.id}
                          role="button"
                          tabIndex={0}
                          onClick={() => navigate(`/delivery?programme=${p.code}`)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") {
                              e.preventDefault();
                              navigate(`/delivery?programme=${p.code}`);
                            }
                          }}
                          className="cursor-pointer border-t border-ice-100 transition hover:bg-ice-50 focus-visible:bg-ice-50"
                          aria-label={`Drill into ${p.name}`}
                        >
                          <td className="py-2 font-medium">{p.code}</td>
                          <td className="text-right font-mono">
                            {formatValue(latest, selectedKpi)}
                          </td>
                          <td className="text-right">
                            <Badge tone={tone}>{tone}</Badge>
                          </td>
                          <td className="pr-2 text-right text-navy/40">
                            <ChevronRight className="inline size-4" aria-hidden="true" />
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </Card>
          </>
        ) : (
          <Card>
            <p className="text-sm text-navy/70">Select a KPI from the library.</p>
          </Card>
        )}
      </section>

      {formulaOpen && selectedKpi ? (
        <FormulaModal kpi={selectedKpi} onClose={() => setFormulaOpen(false)} />
      ) : null}
      </div>
    </div>
  );
}

function StatCell({ label, value, tone }: { label: string; value: string; tone: ToneOrNeutral }) {
  return (
    <div>
      <dt className="kpi-label">{label}</dt>
      <dd className="mt-1">
        <Badge tone={tone}>{value}</Badge>
      </dd>
    </div>
  );
}

function FormulaModal({ kpi, onClose }: { kpi: KpiDefinition; onClose: () => void }) {
  return (
    <div
      className="fixed inset-0 z-20 grid place-items-center bg-navy/40 p-6"
      role="dialog"
      aria-modal="true"
      aria-label={`${kpi.name} formula reference`}
      onClick={onClose}
    >
      <div
        className="max-w-lg rounded-lg bg-white p-6 shadow-card-hover"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3 border-b border-ice-100 pb-3">
          <div>
            <h3 className="text-base font-semibold text-navy">{kpi.name}</h3>
            <p className="text-xs text-navy/70">{kpi.category ?? "—"}</p>
          </div>
          <button onClick={onClose} type="button" className="btn-ghost">
            <X className="size-3" /> Close
          </button>
        </div>
        <dl className="mt-4 flex flex-col gap-3 text-sm">
          <div>
            <dt className="kpi-label">Formula</dt>
            <dd className="mt-1 rounded bg-ice-50 p-2 font-mono text-sm">
              {kpi.formula}
            </dd>
          </div>
          <div>
            <dt className="kpi-label">Unit</dt>
            <dd className="font-mono">{kpi.unit ?? "—"}</dd>
          </div>
          {kpi.description ? (
            <div>
              <dt className="kpi-label">Description</dt>
              <dd>{kpi.description}</dd>
            </div>
          ) : null}
          <div>
            <dt className="kpi-label">Thresholds</dt>
            <dd className="flex flex-wrap gap-2 pt-1">
              {kpi.green_threshold !== null ? (
                <Badge tone="green">G ≥ {formatValue(kpi.green_threshold, kpi)}</Badge>
              ) : null}
              {kpi.amber_threshold !== null ? (
                <Badge tone="amber">A ≥ {formatValue(kpi.amber_threshold, kpi)}</Badge>
              ) : null}
              {kpi.red_threshold !== null ? (
                <Badge tone="red">R &lt; {formatValue(kpi.red_threshold, kpi)}</Badge>
              ) : null}
            </dd>
          </div>
        </dl>
        <p className="mt-4 text-xs text-navy/70">
          Source: docs/FORMULAS.md — 45 formulas documented for every KPI and
          composite in AKB1 v5.2.
        </p>
      </div>
    </div>
  );
}

function latestForProgramme(
  programId: number,
  snapshots: { program_id: number | null; snapshot_date: string; value: number }[],
): number | null {
  const filtered = snapshots
    .filter((s) => s.program_id === programId)
    .sort((a, b) => a.snapshot_date.localeCompare(b.snapshot_date));
  if (filtered.length === 0) return null;
  return filtered[filtered.length - 1].value;
}

function monthLabel(yyyyMm: string): string {
  const [year, month] = yyyyMm.split("-");
  const d = new Date(Number(year), Number(month) - 1, 1);
  return d.toLocaleDateString("en-GB", { month: "short", year: "2-digit" });
}

const seriesColors = ["#1B2A4A", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6"];
