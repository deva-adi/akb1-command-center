import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, Download, RotateCcw, Upload, UploadCloud } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { fetchImportLog, fetchSettings, previewCsv } from "@/lib/api";
import { formatDate } from "@/lib/format";

type PreviewState = {
  filename: string;
  columns: string[];
  rowCount: number;
  sample: Record<string, string>[];
} | null;

const templates = [
  "programmes.csv",
  "projects.csv",
  "sprints.csv",
  "kpi_monthly.csv",
  "financials.csv",
  "evm_monthly.csv",
  "risks.csv",
  "resources.csv",
  "bench.csv",
  "losses.csv",
  "change_requests.csv",
  "ai_metrics.csv",
  "ai_tools.csv",
  "flow_metrics.csv",
  "project_phases.csv",
];

export function DataHub() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<PreviewState>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const settings = useQuery({ queryKey: ["settings"], queryFn: fetchSettings });
  const imports = useQuery({ queryKey: ["imports"], queryFn: fetchImportLog });

  const settingMap = new Map((settings.data ?? []).map((s) => [s.key, s.value ?? "—"]));

  async function handleFile(file: File) {
    setPreviewError(null);
    setUploading(true);
    try {
      const response = await previewCsv(file);
      setPreview({
        filename: response.filename,
        columns: response.columns,
        rowCount: response.row_count,
        sample: response.sample,
      });
    } catch (err) {
      setPreview(null);
      setPreviewError((err as Error).message);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-navy">Data Hub & Settings</h1>
        <p className="mt-1 text-sm text-navy/70">
          Configure portfolio defaults, bulk-import CSV/XLSX, and review import history.
          CSV validation runs in-browser against the seeded templates.
        </p>
      </div>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader
            title="Ingest programme data"
            subtitle="Preview parses headers client-side; committed imports arrive in Iteration 2."
          />
          <label
            htmlFor="csv-upload"
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              const file = e.dataTransfer.files[0];
              if (file) void handleFile(file);
            }}
            className={`flex cursor-pointer flex-col items-center gap-2 rounded-lg border-2 border-dashed px-4 py-10 text-center text-sm transition ${
              dragOver
                ? "border-amber-500 bg-amber-500/5 text-navy"
                : "border-ice-600 bg-ice-50 text-navy/70 hover:border-navy/40 hover:text-navy"
            }`}
          >
            <UploadCloud className="size-8 text-amber-500" aria-hidden="true" />
            <span className="font-medium">
              Drop a CSV here, or click to browse
            </span>
            <span className="text-xs text-navy/60">
              Max 10 MB · UTF-8 · Headers row required
            </span>
            <input
              id="csv-upload"
              ref={inputRef}
              type="file"
              accept=".csv,text/csv"
              className="sr-only"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) void handleFile(file);
              }}
            />
          </label>

          {uploading ? (
            <p className="mt-3 text-sm text-navy/60">Parsing upload…</p>
          ) : null}

          {previewError ? (
            <p className="mt-3 text-sm text-danger-600">{previewError}</p>
          ) : null}

          {preview ? (
            <div className="mt-4 space-y-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="size-4 text-success-600" aria-hidden="true" />
                <p className="text-sm">
                  <strong>{preview.filename}</strong> parsed: {preview.rowCount}{" "}
                  rows · {preview.columns.length} columns
                </p>
              </div>
              <div className="overflow-x-auto rounded-md border border-ice-100">
                <table className="w-full text-xs">
                  <thead className="bg-ice-50 text-navy/70">
                    <tr>
                      {preview.columns.map((col) => (
                        <th key={col} className="px-2 py-1 text-left font-semibold">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {preview.sample.map((row, idx) => (
                      <tr key={idx} className="border-t border-ice-100">
                        {preview.columns.map((col) => (
                          <td key={col} className="px-2 py-1 font-mono">
                            {row[col] ?? ""}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-xs text-navy/60">
                Commit and rollback land with the{" "}
                <code>data_import_snapshots</code> pipeline in Iteration 2.
              </p>
            </div>
          ) : null}
        </Card>

        <Card>
          <CardHeader
            title="CSV templates"
            subtitle="Shipped in docs/csv-templates/"
          />
          <ul className="flex flex-col gap-1 text-sm">
            {templates.map((t) => (
              <li key={t}>
                <a
                  className="flex items-center justify-between rounded px-2 py-1 text-navy hover:bg-ice-50"
                  href={`https://github.com/deva-adi/akb1-command-center/blob/main/docs/csv-templates/${t}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  <span className="font-mono text-xs">{t}</span>
                  <Download className="size-3.5 text-navy/50" aria-hidden="true" />
                </a>
              </li>
            ))}
          </ul>
        </Card>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Recent imports" subtitle="Committed to the data_imports ledger" />
          {imports.isLoading ? (
            <p className="text-sm text-navy/60">Loading…</p>
          ) : (imports.data ?? []).length === 0 ? (
            <p className="text-sm text-navy/60">
              No imports yet. Try uploading a CSV from{" "}
              <span className="font-mono">docs/csv-templates/</span>.
            </p>
          ) : (
            <ul className="flex flex-col gap-2 text-sm">
              {(imports.data ?? []).map((entry) => (
                <li
                  key={entry.id}
                  className="flex items-center justify-between rounded border border-ice-100 bg-white px-3 py-2"
                >
                  <div>
                    <p className="font-medium">{entry.file_name ?? "unknown"}</p>
                    <p className="text-xs text-navy/60">
                      {entry.rows_imported ?? 0} rows · source{" "}
                      {entry.source ?? "—"}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge tone={entry.status === "committed" ? "green" : "amber"}>
                      {entry.status ?? "pending"}
                    </Badge>
                    <button className="btn-ghost" type="button" disabled>
                      <RotateCcw className="size-3" /> Rollback
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card>
          <CardHeader title="Settings" subtitle="Portfolio defaults" />
          <dl className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
            <SettingRow label="Organisation" value={settingMap.get("org_name")} />
            <SettingRow label="Base currency" value={settingMap.get("base_currency")} />
            <SettingRow
              label="Fiscal year"
              value={`Starts month ${settingMap.get("fiscal_year_start_month") ?? "—"}`}
            />
            <SettingRow label="Locale" value={settingMap.get("locale")} />
            <SettingRow label="Industry preset" value={settingMap.get("industry_preset")} />
            <SettingRow label="Demo mode" value={settingMap.get("demo_mode")} />
            <SettingRow label="Last sync" value={formatDate(new Date().toISOString())} />
            <SettingRow label="Schema version" value="5.2" />
          </dl>
          <p className="mt-4 text-xs text-navy/60">
            Inline edit lands with the Tab 11 wizard in Iteration 2. API is live —{" "}
            <code>PUT /api/v1/settings/&#123;key&#125;</code>.
          </p>
        </Card>
      </section>

      <Card>
        <CardHeader
          title="Guided onboarding wizard (preview)"
          subtitle="Four steps — base currency, fiscal year, programmes, data"
          action={
            <button type="button" className="btn-primary" disabled>
              <Upload className="size-4" /> Launch wizard
            </button>
          }
        />
        <ol className="grid grid-cols-1 gap-3 text-sm md:grid-cols-4">
          {["Pick base currency", "Set fiscal year", "Add programmes", "Upload data"].map(
            (step, idx) => (
              <li
                key={step}
                className="flex flex-col gap-2 rounded-md border border-ice-100 bg-ice-50/50 p-3"
              >
                <span className="font-mono text-xs text-navy/60">
                  Step {idx + 1}
                </span>
                <span className="font-medium">{step}</span>
              </li>
            ),
          )}
        </ol>
      </Card>
    </div>
  );
}

function SettingRow({
  label,
  value,
}: {
  label: string;
  value: string | null | undefined;
}) {
  return (
    <div className="flex flex-col">
      <dt className="kpi-label">{label}</dt>
      <dd className="font-mono text-sm text-navy">{value ?? "—"}</dd>
    </div>
  );
}
