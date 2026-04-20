import { useMemo } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { FileDown, Sparkles } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { KpiTile } from "@/components/ui/KpiTile";
import { TopRisksCard } from "@/components/TopRisksCard";
import {
  useCpiSnapshots,
  useMarginSnapshots,
  useProgrammes,
} from "@/hooks/usePortfolio";
import {
  bucketForStatus,
  formatCurrencyINR,
  formatPct,
  formatRatio,
  type RagBucket,
} from "@/lib/format";

type ProgrammeRow = {
  code: string;
  name: string;
  status: string;
  revenue: number;
  latestMargin: number | null;
  latestCpi: number | null;
};

function deriveBucket(margin: number | null, status: string): RagBucket {
  if (margin !== null && margin < 0.10) return "red";
  if (bucketForStatus(status) === "red") return "red";
  if (margin !== null && margin < 0.18) return "amber";
  if (bucketForStatus(status) === "amber") return "amber";
  return "green";
}

export function ExecutiveOverview() {
  const programmes = useProgrammes();
  const margin = useMarginSnapshots();
  const cpi = useCpiSnapshots();

  const rows: ProgrammeRow[] = useMemo(() => {
    if (!programmes.data) return [];
    const marginByProgram = groupLatest(margin.data ?? []);
    const cpiByProgram = groupLatest(cpi.data ?? []);
    return programmes.data.map((p) => ({
      code: p.code,
      name: p.name,
      status: p.status,
      revenue: p.revenue ?? 0,
      latestMargin: marginByProgram.get(p.id) ?? null,
      latestCpi: cpiByProgram.get(p.id) ?? null,
    }));
  }, [programmes.data, margin.data, cpi.data]);

  const buckets = useMemo(() => {
    const counts = { green: 0, amber: 0, red: 0 } as Record<RagBucket, number>;
    rows.forEach((r) => {
      counts[deriveBucket(r.latestMargin, r.status)] += 1;
    });
    return counts;
  }, [rows]);

  const totals = useMemo(() => {
    const revenue = rows.reduce((sum, r) => sum + r.revenue, 0);
    const avgMargin =
      rows.filter((r) => r.latestMargin !== null).length === 0
        ? null
        : rows
            .filter((r) => r.latestMargin !== null)
            .reduce((sum, r) => sum + (r.latestMargin ?? 0), 0) /
          rows.filter((r) => r.latestMargin !== null).length;
    const avgCpi =
      rows.filter((r) => r.latestCpi !== null).length === 0
        ? null
        : rows
            .filter((r) => r.latestCpi !== null)
            .reduce((sum, r) => sum + (r.latestCpi ?? 0), 0) /
          rows.filter((r) => r.latestCpi !== null).length;
    return { revenue, avgMargin, avgCpi };
  }, [rows]);

  const marginSeries = useMemo(
    () => buildSeries(margin.data ?? [], programmes.data ?? []),
    [margin.data, programmes.data],
  );

  const narrative = useMemo(
    () => buildNarrative(buckets, totals, rows),
    [buckets, totals, rows],
  );

  const loading =
    programmes.isLoading || margin.isLoading || cpi.isLoading;
  const error = programmes.error ?? margin.error ?? cpi.error;

  if (loading) {
    return (
      <div className="grid place-items-center py-20 text-sm text-navy/60">
        Loading portfolio snapshot…
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader title="Unable to load portfolio" />
        <p className="text-sm text-danger-600">
          {(error as Error).message}. Check the backend is healthy at{" "}
          <code>/health</code>.
        </p>
      </Card>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-navy">Executive Summary</h1>
          <p className="mt-1 text-sm text-navy/70">
            Portfolio snapshot — answers CEO/COO pre-board questions. Data is
            live from the seeded NovaTech demo (5 programmes × 12 months).
          </p>
        </div>
        <button type="button" className="btn-primary" disabled>
          <FileDown className="size-4" /> Generate QBR Brief
        </button>
      </div>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardHeader title="Portfolio Health" subtitle="RAG roll-up across programmes" />
          <div className="flex items-center justify-around gap-3 pt-1 text-center">
            <RagStat count={buckets.green} label="Green" tone="green" />
            <RagStat count={buckets.amber} label="Amber" tone="amber" />
            <RagStat count={buckets.red} label="Red" tone="red" />
          </div>
          <p className="mt-4 text-xs text-navy/60">
            Derived from programme status and the latest monthly margin KPI.
          </p>
        </Card>

        <Card>
          <CardHeader title="Financials" subtitle="Annualised portfolio revenue" />
          <div className="grid grid-cols-2 gap-3">
            <KpiMini label="Revenue" value={formatCurrencyINR(totals.revenue)} />
            <KpiMini
              label="Avg margin"
              value={formatPct(totals.avgMargin)}
              tone={
                totals.avgMargin === null
                  ? "neutral"
                  : totals.avgMargin >= 0.22
                    ? "green"
                    : totals.avgMargin >= 0.15
                      ? "amber"
                      : "red"
              }
            />
          </div>
        </Card>

        <Card>
          <CardHeader title="Delivery" subtitle="Earned-value indicators" />
          <div className="grid grid-cols-2 gap-3">
            <KpiMini label="Avg CPI" value={formatRatio(totals.avgCpi)} />
            <KpiMini
              label="Programmes"
              value={`${rows.length}`}
              tone="neutral"
            />
          </div>
        </Card>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <KpiTile label="Revenue realised" value={formatCurrencyINR(totals.revenue)} sub="YTD across 5 programmes" />
        <KpiTile
          label="Blended margin"
          value={formatPct(totals.avgMargin)}
          sub="Target 22% · Amber 15%"
          trend={totals.avgMargin !== null && totals.avgMargin < 0.18 ? "down" : "flat"}
        />
        <KpiTile
          label="Avg Cost Performance Index"
          value={formatRatio(totals.avgCpi)}
          sub="Green ≥ 1.00 · Amber 0.90"
          trend={totals.avgCpi !== null && totals.avgCpi < 0.95 ? "down" : "flat"}
        />
      </section>

      <Card>
        <CardHeader
          title="12-month margin trend"
          subtitle="Programme-level gross margin (seeded data)"
        />
        <div className="h-72">
          {marginSeries.length === 0 ? (
            <p className="grid h-full place-items-center text-sm text-navy/60">
              No KPI snapshots yet — run the seeder (SEED_DEMO_DATA=true).
            </p>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={marginSeries} margin={{ top: 8, right: 24, left: 0, bottom: 8 }}>
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis
                  dataKey="monthLabel"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                />
                <YAxis
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                  domain={[0, "dataMax + 0.05"]}
                />
                <Tooltip
                  formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
                  contentStyle={{ border: "1px solid #D5E8F0" }}
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                {(programmes.data ?? []).map((p, idx) => (
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

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader title="Programme status" subtitle="Margin and CPI by programme" />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase text-navy/60">
                  <th className="py-2">Programme</th>
                  <th>Status</th>
                  <th className="text-right">Revenue</th>
                  <th className="text-right">Margin</th>
                  <th className="text-right">CPI</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => {
                  const tone = deriveBucket(r.latestMargin, r.status);
                  return (
                    <tr key={r.code} className="border-t border-ice-100">
                      <td className="py-2 font-medium">{r.name}</td>
                      <td>
                        <Badge tone={tone}>{r.status}</Badge>
                      </td>
                      <td className="text-right font-mono">
                        {formatCurrencyINR(r.revenue)}
                      </td>
                      <td className="text-right font-mono">
                        {formatPct(r.latestMargin)}
                      </td>
                      <td className="text-right font-mono">
                        {formatRatio(r.latestCpi)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>

        <TopRisksCard limit={5} />
      </section>

      <Card>
        <CardHeader
          title="Narrative"
          subtitle="Template-driven commentary (Iteration 2 upgrades to LLM-optional)"
          action={<Sparkles className="size-4 text-amber-500" aria-hidden="true" />}
        />
        <p className="whitespace-pre-line text-sm leading-relaxed text-navy/80">
          {narrative}
        </p>
      </Card>
    </div>
  );
}

function RagStat({ count, label, tone }: { count: number; label: string; tone: RagBucket }) {
  return (
    <div className="flex flex-col items-center gap-1">
      <Badge tone={tone} className="px-3 py-1 text-sm">
        {count}
      </Badge>
      <span className="text-xs text-navy/60">{label}</span>
    </div>
  );
}

function KpiMini({
  label,
  value,
  tone = "neutral",
}: {
  label: string;
  value: string;
  tone?: RagBucket | "neutral";
}) {
  return (
    <div className="flex flex-col gap-1">
      <span className="kpi-label">{label}</span>
      <Badge tone={tone}>{value}</Badge>
    </div>
  );
}

function groupLatest(snapshots: { program_id: number | null; value: number }[]) {
  const map = new Map<number, number>();
  for (const s of snapshots) {
    if (s.program_id === null) continue;
    map.set(s.program_id, s.value);
  }
  return map;
}

function buildSeries(
  snapshots: { program_id: number | null; snapshot_date: string; value: number }[],
  programmes: { id: number; code: string }[],
) {
  const codeById = new Map(programmes.map((p) => [p.id, p.code]));
  const byMonth = new Map<string, Record<string, number | string>>();
  for (const s of snapshots) {
    if (s.program_id === null) continue;
    const code = codeById.get(s.program_id);
    if (!code) continue;
    const key = s.snapshot_date.slice(0, 7);
    const bucket = byMonth.get(key) ?? { monthLabel: formatMonthLabel(key) };
    bucket[code] = s.value;
    byMonth.set(key, bucket);
  }
  return Array.from(byMonth.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([, row]) => row);
}

function formatMonthLabel(yyyyMm: string): string {
  const [year, month] = yyyyMm.split("-");
  const dt = new Date(Number(year), Number(month) - 1, 1);
  return dt.toLocaleDateString("en-GB", { month: "short", year: "2-digit" });
}

function buildNarrative(
  buckets: Record<RagBucket, number>,
  totals: { revenue: number; avgMargin: number | null; avgCpi: number | null },
  rows: ProgrammeRow[],
): string {
  const weakest = [...rows]
    .filter((r) => r.latestMargin !== null)
    .sort((a, b) => (a.latestMargin ?? 0) - (b.latestMargin ?? 0))[0];
  const strongest = [...rows]
    .filter((r) => r.latestMargin !== null)
    .sort((a, b) => (b.latestMargin ?? 0) - (a.latestMargin ?? 0))[0];

  const lines = [
    `Portfolio revenue stands at ${formatCurrencyINR(totals.revenue)} across ${rows.length} programmes, with ${buckets.green} green, ${buckets.amber} amber and ${buckets.red} red on the RAG scorecard.`,
    totals.avgMargin === null
      ? "Blended margin is unavailable until the margin KPI snapshots land."
      : `Blended margin sits at ${formatPct(totals.avgMargin)} — ${
          totals.avgMargin >= 0.22
            ? "ahead of the 22% target."
            : totals.avgMargin >= 0.15
              ? "below the 22% target and inside the amber corridor."
              : "materially below target and in the red corridor."
        }`,
  ];
  if (weakest && strongest) {
    lines.push(
      `${strongest.name} is the strongest performer at ${formatPct(strongest.latestMargin)}, while ${weakest.name} is compressing at ${formatPct(weakest.latestMargin)} — flagged for remediation.`,
    );
  }
  return lines.join("\n\n");
}

const seriesColors = ["#1B2A4A", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6"];
