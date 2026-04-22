import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  BarChart2,
  Bot,
  BookOpen,
  FileDown,
  FileText,
  LayoutDashboard,
  Loader2,
  Package,
  ShieldAlert,
  Sparkles,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
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
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  auditPackageUrl,
  fetchForecast,
  fetchKpiDefinitions,
  generateReport,
  qbrPdfUrl,
  type Forecast,
  type ReportType,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";

// ---------- report type definitions ----------

type ReportMeta = {
  code: ReportType;
  label: string;
  description: string;
  icon: React.ElementType;
  accentClass: string;
  needsKpi?: boolean;
};

const REPORT_TYPES: ReportMeta[] = [
  {
    code: "executive_summary",
    label: "Executive Summary",
    description: "Portfolio RAG status, revenue, CPI/SPI/margin snapshot, top risks",
    icon: LayoutDashboard,
    accentClass: "text-navy",
  },
  {
    code: "qbr_pack",
    label: "QBR Pack",
    description: "One section per programme — CSAT, margins, EVM, top risks, open actions",
    icon: FileDown,
    accentClass: "text-amber-500",
  },
  {
    code: "board_pack",
    label: "Board Pack",
    description: "Strategic overview, customer health, SLA breaches, financials, risk",
    icon: BookOpen,
    accentClass: "text-navy",
  },
  {
    code: "margin_loss",
    label: "Margin & Loss",
    description: "Commercial waterfall (gross → net), loss category breakdown, variance",
    icon: TrendingDown,
    accentClass: "text-red-500",
  },
  {
    code: "evm_portfolio",
    label: "EVM Portfolio",
    description: "CPI, SPI, EAC, VAC, TCPI over the selected period per programme",
    icon: BarChart2,
    accentClass: "text-success-600",
  },
  {
    code: "kpi_trend",
    label: "KPI Trend",
    description: "Pick any KPIs and get trend snapshots across programmes and time",
    icon: TrendingUp,
    accentClass: "text-amber-500",
    needsKpi: true,
  },
  {
    code: "delivery_health",
    label: "Delivery Health",
    description: "Sprint velocity, milestone tracking, SLA incident register",
    icon: Activity,
    accentClass: "text-success-600",
  },
  {
    code: "risk_audit",
    label: "Risk & Audit",
    description: "Risk register by severity, SLA breach log, change audit trail",
    icon: ShieldAlert,
    accentClass: "text-red-500",
  },
  {
    code: "ai_governance",
    label: "AI Governance",
    description: "Trust scores, usage metrics, compliance config across programmes",
    icon: Bot,
    accentClass: "text-purple-500",
  },
];

const FORECAST_KPIS = [
  { code: "CPI", label: "Cost Performance Index" },
  { code: "SPI", label: "Schedule Performance Index" },
  { code: "MARGIN", label: "Blended Margin" },
  { code: "AI_TRUST", label: "AI Trust Score" },
];

// ---------- component ----------

export function Reports() {
  const navigate = useNavigate();
  const programmes = useProgrammes();
  const kpiDefs = useQuery({ queryKey: ["kpi-defs"], queryFn: () => fetchKpiDefinitions() });

  // Report Builder state
  const [reportType, setReportType] = useState<ReportType | "">("");
  const [selectedProgs, setSelectedProgs] = useState<string[]>([]);
  const [periodMonths, setPeriodMonths] = useState<3 | 6 | 12 | 24>(12);
  const [kpiCodes, setKpiCodes] = useState<string[]>([]);
  const [currency, setCurrency] = useState("INR");
  const [format, setFormat] = useState<"pdf" | "csv">("pdf");
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState<string | null>(null);

  // Forecast state
  const [forecastKpi, setForecastKpi] = useState("CPI");
  const [forecastProgramme, setForecastProgramme] = useState<string>("");

  const forecast = useQuery({
    queryKey: ["forecast", forecastKpi, forecastProgramme || "all"],
    queryFn: () => fetchForecast(forecastKpi, forecastProgramme || undefined, 3),
  });

  const selectedMeta = REPORT_TYPES.find((r) => r.code === reportType);

  function toggleProg(code: string) {
    setSelectedProgs((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code],
    );
  }

  function toggleKpi(code: string) {
    setKpiCodes((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code],
    );
  }

  async function handleGenerate() {
    if (!reportType) return;
    setGenerating(true);
    setGenError(null);
    try {
      const blob = await generateReport({
        report_type: reportType,
        programme_codes: selectedProgs,
        period_months: periodMonths,
        kpi_codes: kpiCodes,
        format,
        currency,
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${reportType}-${new Date().toISOString().slice(0, 10)}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setGenError(err instanceof Error ? err.message : "Report generation failed");
    } finally {
      setGenerating(false);
    }
  }

  const allProgs = programmes.data ?? [];
  const canGenerate = !!reportType && !generating;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-navy">Reports & Exports</h1>
        <p className="mt-1 text-sm text-navy/70">
          Configure any of 9 report types, select programmes and period, then download as PDF or CSV.
          Quick downloads and the predictive forecast are below.
        </p>
      </div>

      {/* ── Report Builder ── */}
      <Card>
        <CardHeader
          title="Report Builder"
          subtitle="Step 1 — choose report type · Step 2 — scope & parameters · Step 3 — generate"
          action={<FileText className="size-4 text-navy" aria-hidden="true" />}
        />

        {/* Step 1: Type grid */}
        <p className="kpi-label mb-2">1 · Choose report type</p>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {REPORT_TYPES.map((rt) => {
            const Icon = rt.icon;
            const active = reportType === rt.code;
            return (
              <button
                key={rt.code}
                type="button"
                onClick={() => setReportType(rt.code)}
                className={[
                  "flex items-start gap-3 rounded-lg border px-3 py-3 text-left transition",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy/40",
                  active
                    ? "border-navy bg-navy/5 shadow-sm"
                    : "border-ice-100 bg-white hover:border-navy/30 hover:bg-ice-50",
                ].join(" ")}
                aria-pressed={active}
              >
                <Icon className={["mt-0.5 size-4 shrink-0", rt.accentClass].join(" ")} aria-hidden="true" />
                <div className="min-w-0">
                  <p className={["text-sm font-medium", active ? "text-navy" : "text-navy/90"].join(" ")}>
                    {rt.label}
                  </p>
                  <p className="mt-0.5 text-xs text-navy/60 leading-snug">{rt.description}</p>
                </div>
                {active && (
                  <span className="ml-auto shrink-0 rounded-full bg-navy px-1.5 py-0.5 text-[10px] font-semibold text-white">
                    ✓
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Step 2: Scope */}
        <div className="mt-5 border-t border-ice-100 pt-4">
          <p className="kpi-label mb-3">2 · Scope & parameters</p>
          <div className="flex flex-wrap gap-5">
            {/* Programme multi-select */}
            <div className="min-w-[200px] flex-1">
              <p className="kpi-label mb-1.5">Programmes</p>
              <div className="flex flex-col gap-1">
                <label className="flex cursor-pointer items-center gap-2 text-xs">
                  <input
                    type="checkbox"
                    checked={selectedProgs.length === 0}
                    onChange={() => setSelectedProgs([])}
                    className="accent-navy"
                  />
                  <span className="font-medium text-navy">All programmes</span>
                </label>
                {allProgs.map((p) => (
                  <label key={p.id} className="flex cursor-pointer items-center gap-2 text-xs">
                    <input
                      type="checkbox"
                      checked={selectedProgs.includes(p.code)}
                      onChange={() => toggleProg(p.code)}
                      className="accent-navy"
                    />
                    <span className="font-mono text-navy">
                      {p.code}
                    </span>
                    <span className="text-navy/60">{p.name}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Period + Currency */}
            <div className="flex flex-col gap-3">
              <div>
                <p className="kpi-label mb-1.5">Period</p>
                <div className="flex gap-1">
                  {([3, 6, 12, 24] as const).map((m) => (
                    <button
                      key={m}
                      type="button"
                      onClick={() => setPeriodMonths(m)}
                      className={[
                        "rounded px-2.5 py-1 text-xs font-medium transition",
                        periodMonths === m
                          ? "bg-navy text-white"
                          : "border border-ice-100 bg-white text-navy hover:bg-ice-50",
                      ].join(" ")}
                    >
                      {m}M
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="kpi-label mb-1.5">Currency label</p>
                <select
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="rounded border border-ice-100 px-2.5 py-1 font-mono text-xs text-navy"
                >
                  <option value="INR">INR — ₹</option>
                  <option value="USD">USD — $</option>
                  <option value="GBP">GBP — £</option>
                  <option value="EUR">EUR — €</option>
                </select>
              </div>

              {/* KPI selector — only for kpi_trend */}
              {selectedMeta?.needsKpi && (
                <div>
                  <p className="kpi-label mb-1.5">KPIs to include</p>
                  <div className="flex flex-col gap-1 max-h-36 overflow-y-auto pr-1">
                    {(kpiDefs.data ?? []).map((k) => (
                      <label key={k.id} className="flex cursor-pointer items-center gap-2 text-xs">
                        <input
                          type="checkbox"
                          checked={kpiCodes.includes(k.code)}
                          onChange={() => toggleKpi(k.code)}
                          className="accent-navy"
                        />
                        <span className="font-mono text-navy">{k.code}</span>
                        <span className="text-navy/60 truncate max-w-[140px]">{k.name}</span>
                      </label>
                    ))}
                  </div>
                  {kpiCodes.length === 0 && (
                    <p className="mt-1 text-[11px] text-navy/50">No KPIs selected → all KPIs included</p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Step 3: Format + Generate */}
        <div className="mt-5 border-t border-ice-100 pt-4">
          <p className="kpi-label mb-3">3 · Format & generate</p>
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex rounded-lg border border-ice-100 overflow-hidden">
              {(["pdf", "csv"] as const).map((f) => (
                <button
                  key={f}
                  type="button"
                  onClick={() => setFormat(f)}
                  className={[
                    "px-4 py-2 text-xs font-medium uppercase tracking-wide transition",
                    format === f
                      ? "bg-navy text-white"
                      : "bg-white text-navy hover:bg-ice-50",
                  ].join(" ")}
                >
                  {f}
                </button>
              ))}
            </div>

            <button
              type="button"
              onClick={handleGenerate}
              disabled={!canGenerate}
              className={[
                "btn-primary gap-2",
                !canGenerate && "opacity-50 cursor-not-allowed",
              ].join(" ")}
            >
              {generating ? (
                <Loader2 className="size-4 animate-spin" aria-hidden="true" />
              ) : (
                <FileDown className="size-4" aria-hidden="true" />
              )}
              {generating
                ? "Generating…"
                : reportType
                ? `Generate ${selectedMeta?.label ?? ""} (${format.toUpperCase()})`
                : "Select a report type first"}
            </button>

            {selectedProgs.length > 0 && (
              <span className="text-xs text-navy/60">
                {selectedProgs.length} programme{selectedProgs.length > 1 ? "s" : ""} selected
              </span>
            )}
          </div>

          {genError && (
            <p className="mt-2 text-xs text-red-600">{genError}</p>
          )}

          {!reportType && (
            <p className="mt-2 text-xs text-navy/50">
              Choose a report type above to enable generation.
            </p>
          )}
        </div>
      </Card>

      {/* ── Quick Downloads ── */}
      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader
            title="QBR brief per programme"
            subtitle="One-page PDF (ReportLab): snapshot + commentary + top risks + open actions"
            action={<FileDown className="size-4 text-amber-500" aria-hidden="true" />}
          />
          <ul className="flex flex-col gap-2 text-sm">
            {allProgs.map((p) => (
              <li
                key={p.id}
                className="flex items-center justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2"
              >
                <div>
                  <p className="font-medium">{p.name}</p>
                  <p className="text-xs text-navy/70">
                    {p.code} · {p.client ?? "—"}
                  </p>
                </div>
                <a
                  href={qbrPdfUrl(p.id)}
                  className="btn-primary text-xs"
                  download={`qbr-${p.code.toLowerCase()}.pdf`}
                >
                  <FileDown className="size-3" /> Download QBR
                </a>
              </li>
            ))}
          </ul>
        </Card>

        <Card>
          <CardHeader
            title="Audit evidence package"
            subtitle="ZIP of risks, CRs, SLA incidents, KPI snapshots, customer satisfaction and audit_log"
            action={<Package className="size-4 text-navy/70" aria-hidden="true" />}
          />
          <div className="flex flex-col gap-3">
            <a
              href={auditPackageUrl()}
              className="btn-primary w-max text-xs"
              download="audit-portfolio.zip"
            >
              <Package className="size-3" /> Portfolio-wide audit ZIP
            </a>
            <p className="kpi-label">Per programme</p>
            <ul className="flex flex-col gap-1 text-sm">
              {allProgs.map((p) => (
                <li key={p.id}>
                  <a
                    href={auditPackageUrl(p.id)}
                    className="inline-flex items-center gap-2 rounded px-2 py-1 font-mono text-xs text-navy hover:bg-ice-50"
                    download={`audit-${p.code.toLowerCase()}.zip`}
                  >
                    <Package className="size-3" aria-hidden="true" /> {p.code} audit ZIP
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </Card>
      </section>

      {/* ── Predictive Forecast ── */}
      <Card>
        <CardHeader
          title="Predictive forecast"
          subtitle="Linear trend + weighted MA + exponential smoothing, 3-month horizon"
          action={<TrendingUp className="size-4 text-success-600" aria-hidden="true" />}
        />
        <div className="flex flex-wrap items-end gap-3">
          <label className="flex flex-col gap-1 text-xs">
            <span className="kpi-label">KPI</span>
            <select
              value={forecastKpi}
              onChange={(e) => setForecastKpi(e.target.value)}
              className="rounded border border-ice-100 px-3 py-1 font-mono text-xs text-navy"
            >
              {FORECAST_KPIS.map((k) => (
                <option key={k.code} value={k.code}>
                  {k.code} — {k.label}
                </option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-xs">
            <span className="kpi-label">Programme</span>
            <select
              value={forecastProgramme}
              onChange={(e) => setForecastProgramme(e.target.value)}
              className="rounded border border-ice-100 px-3 py-1 font-mono text-xs text-navy"
            >
              <option value="">Portfolio (aggregate)</option>
              {allProgs.map((p) => (
                <option key={p.id} value={p.code}>
                  {p.code} — {p.name}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="mt-4 h-80">
          {forecast.isLoading ? (
            <p className="grid h-full place-items-center text-sm text-navy/70">
              Running forecast…
            </p>
          ) : forecast.error ? (
            <p className="text-sm text-danger-600">
              {(forecast.error as Error).message}
            </p>
          ) : forecast.data && forecast.data.historical_values.length === 0 ? (
            <p className="grid h-full place-items-center text-sm text-navy/70">
              No snapshots seeded for this KPI/programme combination.
            </p>
          ) : forecast.data ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={buildChartData(forecast.data)}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
                onClick={() => {
                  navigate(forecastProgramme ? `/kpi?programme=${forecastProgramme}` : "/kpi");
                }}
                style={{ cursor: "pointer" }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis dataKey="label" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <ReferenceLine
                  x={buildBoundaryLabel(forecast.data)}
                  stroke="#F59E0B"
                  strokeDasharray="3 4"
                  label={{ value: "Forecast →", position: "insideTopLeft", fill: "#F59E0B", fontSize: 11 }}
                />
                <Line type="monotone" dataKey="historical" name="Historical" stroke="#1B2A4A" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="linear" name="Linear trend" stroke="#F59E0B" strokeWidth={2} strokeDasharray="4 4" dot={false} />
                <Line type="monotone" dataKey="wma" name="Weighted MA" stroke="#10B981" strokeWidth={2} strokeDasharray="4 4" dot={false} />
                <Line type="monotone" dataKey="exp" name="Exp. smoothing" stroke="#8B5CF6" strokeWidth={2} strokeDasharray="4 4" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : null}
        </div>
        <p className="mt-2 text-xs text-navy/70">
          <Sparkles className="inline size-3 text-amber-500" aria-hidden="true" />
          {" "}
          The three curves diverge after the vertical line — treat each as a different prior on the next 3 months.
          Click the chart to open the KPI Studio.
        </p>
      </Card>

      {/* ── Report guide ── */}
      <Card>
        <CardHeader
          title="Report types at a glance"
          subtitle="What each report contains and when to use it"
        />
        <ul className="flex flex-col gap-2 text-sm text-navy/80">
          {REPORT_TYPES.map((rt) => {
            const Icon = rt.icon;
            return (
              <li key={rt.code} className="flex items-start gap-2">
                <Icon className={["mt-0.5 size-3.5 shrink-0", rt.accentClass].join(" ")} aria-hidden="true" />
                <span>
                  <Badge tone="neutral">{rt.label}</Badge>{" "}
                  {rt.description}
                </span>
              </li>
            );
          })}
          <li className="mt-1 flex items-start gap-2">
            <Package className="mt-0.5 size-3.5 shrink-0 text-navy/70" aria-hidden="true" />
            <span>
              <Badge tone="neutral">Audit ZIP</Badge> Raw JSON per evidence table with README.txt timestamp, suitable for offline review and auditor submission.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <Sparkles className="mt-0.5 size-3.5 shrink-0 text-amber-500" aria-hidden="true" />
            <span>
              <Badge tone="amber">Forecast</Badge> Three parallel models — when they agree confidence is higher; when linear-trend sprints away, treat it as a volatility flag.
            </span>
          </li>
        </ul>
      </Card>
    </div>
  );
}

// ---------- chart helpers ----------

type ChartRow = {
  label: string;
  historical: number | null;
  linear: number | null;
  wma: number | null;
  exp: number | null;
};

function buildChartData(forecast: Forecast): ChartRow[] {
  const rows: ChartRow[] = [];
  forecast.historical_dates.forEach((d, idx) => {
    rows.push({
      label: d.slice(0, 7),
      historical: forecast.historical_values[idx],
      linear: null,
      wma: null,
      exp: null,
    });
  });
  const linear = forecast.series.find((s) => s.label === "Linear trend");
  const wma = forecast.series.find((s) => s.label === "Weighted moving avg");
  const exp = forecast.series.find((s) => s.label === "Exponential smoothing");
  forecast.horizon_labels.forEach((lbl, idx) => {
    rows.push({
      label: lbl,
      historical: null,
      linear: linear?.values[idx] ?? null,
      wma: wma?.values[idx] ?? null,
      exp: exp?.values[idx] ?? null,
    });
  });
  return rows;
}

function buildBoundaryLabel(forecast: Forecast): string | undefined {
  if (forecast.historical_dates.length === 0) return undefined;
  return forecast.historical_dates[forecast.historical_dates.length - 1].slice(0, 7);
}
