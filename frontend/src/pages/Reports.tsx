import { useState } from "react";
import { FileDown, Home, Package, Sparkles, TrendingUp } from "lucide-react";
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
import { Breadcrumb } from "@/components/Breadcrumb";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  auditPackageUrl,
  fetchForecast,
  qbrPdfUrl,
  type Forecast,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";

const FORECAST_KPIS = [
  { code: "CPI", label: "Cost Performance Index" },
  { code: "SPI", label: "Schedule Performance Index" },
  { code: "MARGIN", label: "Blended Margin" },
  { code: "AI_TRUST", label: "AI Trust Score" },
];

export function Reports() {
  const programmes = useProgrammes();
  const [forecastKpi, setForecastKpi] = useState("CPI");
  const [forecastProgramme, setForecastProgramme] = useState<string | "">(
    "",
  );

  const forecast = useQuery({
    queryKey: ["forecast", forecastKpi, forecastProgramme || "all"],
    queryFn: () => fetchForecast(forecastKpi, forecastProgramme || undefined, 3),
  });

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb
        items={[
          { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
          { label: "Reports & Exports" },
        ]}
      />

      <div>
        <h1 className="text-2xl font-semibold text-navy">Reports & Exports</h1>
        <p className="mt-1 text-sm text-navy/70">
          One-click PDF briefs, audit evidence packages, and a forward-looking
          view that runs the three forecast primitives from
          <code> app/services/forecast.py</code> against any seeded KPI.
        </p>
      </div>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader
            title="QBR brief per programme"
            subtitle="One-page PDF (ReportLab): snapshot + commentary + top risks + open actions"
            action={<FileDown className="size-4 text-amber-500" aria-hidden="true" />}
          />
          <ul className="flex flex-col gap-2 text-sm">
            {(programmes.data ?? []).map((p) => (
              <li
                key={p.id}
                className="flex items-center justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2"
              >
                <div>
                  <p className="font-medium">{p.name}</p>
                  <p className="text-xs text-navy/60">
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
            subtitle="ZIP of risks, CRs, SLA incidents, KPI snapshots, customer satisfaction and audit_log — filtered if you pick a programme"
            action={<Package className="size-4 text-navy/60" aria-hidden="true" />}
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
              {(programmes.data ?? []).map((p) => (
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
              {(programmes.data ?? []).map((p) => (
                <option key={p.id} value={p.code}>
                  {p.code} — {p.name}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="mt-4 h-80">
          {forecast.isLoading ? (
            <p className="grid h-full place-items-center text-sm text-navy/60">
              Running forecast…
            </p>
          ) : forecast.error ? (
            <p className="text-sm text-danger-600">
              {(forecast.error as Error).message}
            </p>
          ) : forecast.data && forecast.data.historical_values.length === 0 ? (
            <p className="grid h-full place-items-center text-sm text-navy/60">
              No snapshots seeded for this KPI/programme combination.
            </p>
          ) : forecast.data ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={buildChartData(forecast.data)}
                margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
              >
                <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                <XAxis
                  dataKey="label"
                  stroke="#1B2A4A"
                  tick={{ fontSize: 12 }}
                />
                <YAxis stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ border: "1px solid #D5E8F0" }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <ReferenceLine
                  x={buildBoundaryLabel(forecast.data)}
                  stroke="#F59E0B"
                  strokeDasharray="3 4"
                  label={{
                    value: "Forecast →",
                    position: "insideTopLeft",
                    fill: "#F59E0B",
                    fontSize: 11,
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="historical"
                  name="Historical"
                  stroke="#1B2A4A"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="linear"
                  name="Linear trend"
                  stroke="#F59E0B"
                  strokeWidth={2}
                  strokeDasharray="4 4"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="wma"
                  name="Weighted MA"
                  stroke="#10B981"
                  strokeWidth={2}
                  strokeDasharray="4 4"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="exp"
                  name="Exp. smoothing"
                  stroke="#8B5CF6"
                  strokeWidth={2}
                  strokeDasharray="4 4"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : null}
        </div>
        <p className="mt-2 text-xs text-navy/60">
          <Sparkles className="inline size-3 text-amber-500" aria-hidden="true" />
          {" "}
          The three curves diverge after the vertical line — treat each as a
          different prior on the next 3 months.
        </p>
      </Card>

      <Card>
        <CardHeader
          title="How to read each export"
          subtitle="Before you forward to a customer or auditor"
        />
        <ul className="flex flex-col gap-2 text-sm text-navy/80">
          <li>
            <Badge tone="neutral">QBR PDF</Badge> Single page, portrait A4, safe
            to print or email. Page title uses the programme's full name; the
            top table captures the latest CPI/SPI/margin/renewal snapshot.
          </li>
          <li>
            <Badge tone="neutral">Audit ZIP</Badge> Contains a <code>.json</code>
            file per evidence table plus a <code>README.txt</code> with a
            timestamp and a reference to <code>docs/SECURITY_GUIDE.md</code>.
            Payloads are the raw rows — suitable for offline review.
          </li>
          <li>
            <Badge tone="amber">Forecast</Badge> Three parallel models. When
            they agree, confidence is higher. When linear-trend sprints away
            from the other two, treat that as a volatility flag.
          </li>
        </ul>
      </Card>
    </div>
  );
}

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
