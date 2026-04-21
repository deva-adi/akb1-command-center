import { useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  CheckCircle2,
  Download,
  RefreshCw,
  RotateCcw,
  Upload,
  UploadCloud,
} from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  commitCsv,
  fetchCurrencyRates,
  fetchImportLog,
  fetchImportSchemas,
  fetchSettings,
  previewCsv,
  refreshCurrencyRates,
  rollbackImport,
} from "@/lib/api";
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

type CommitState = {
  importId: number;
  rowsImported: number;
  affectedTables: string[];
} | null;

export function DataHub() {
  const csvImportRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<PreviewState>(null);
  const [pendingFile, setPendingFile] = useState<File | null>(null);
  const [entityType, setEntityType] = useState<string>("");
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [commitResult, setCommitResult] = useState<CommitState>(null);
  const [commitError, setCommitError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const queryClient = useQueryClient();
  const settings = useQuery({ queryKey: ["settings"], queryFn: fetchSettings });
  const imports = useQuery({ queryKey: ["imports"], queryFn: fetchImportLog });
  const rates = useQuery({
    queryKey: ["currency-rates"],
    queryFn: fetchCurrencyRates,
  });
  const schemas = useQuery({ queryKey: ["import-schemas"], queryFn: fetchImportSchemas });

  const settingMap = new Map((settings.data ?? []).map((s) => [s.key, s.value ?? "—"]));

  const refreshRates = useMutation({
    mutationFn: refreshCurrencyRates,
    onSuccess: (fresh) => {
      queryClient.setQueryData(["currency-rates"], fresh);
    },
  });

  const doCommit = useMutation({
    mutationFn: ({ file, type }: { file: File; type: string }) =>
      commitCsv(file, type),
    onSuccess: (result) => {
      setCommitResult({
        importId: result.import_id,
        rowsImported: result.rows_imported,
        affectedTables: result.affected_tables,
      });
      setCommitError(null);
      setPreview(null);
      setPendingFile(null);
      setEntityType("");
      void queryClient.invalidateQueries({ queryKey: ["imports"] });
    },
    onError: (err) => {
      setCommitError((err as Error).message);
    },
  });

  const doRollback = useMutation({
    mutationFn: (importId: number) => rollbackImport(importId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["imports"] });
    },
  });

  async function handleFile(file: File) {
    setPreviewError(null);
    setCommitResult(null);
    setCommitError(null);
    setUploading(true);
    try {
      const response = await previewCsv(file);
      setPreview({
        filename: response.filename,
        columns: response.columns,
        rowCount: response.row_count,
        sample: response.sample,
      });
      setPendingFile(file);
    } catch (err) {
      setPreview(null);
      setPendingFile(null);
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

      <section ref={csvImportRef} className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader
            title="Ingest programme data"
            subtitle="Preview → pick entity type → Commit. Rollback restores the pre-import snapshot."
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
            <span className="text-xs text-navy/70">
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
            <p className="mt-3 text-sm text-navy/70">Parsing upload…</p>
          ) : null}

          {previewError ? (
            <p className="mt-3 text-sm text-danger-600">{previewError}</p>
          ) : null}

          {commitResult ? (
            <div className="mt-4 flex items-start gap-2 rounded-md border border-success-200 bg-success-50 p-3">
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success-600" aria-hidden="true" />
              <p className="text-sm">
                <strong>Committed</strong> — {commitResult.rowsImported} rows into{" "}
                {commitResult.affectedTables.join(", ")} (import #{commitResult.importId})
              </p>
            </div>
          ) : null}

          {commitError ? (
            <p className="mt-3 text-sm text-danger-600">{commitError}</p>
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
              <div className="flex items-center gap-3">
                <select
                  value={entityType}
                  onChange={(e) => setEntityType(e.target.value)}
                  className="rounded border border-ice-200 bg-white px-3 py-1.5 text-sm text-navy focus:outline-none focus:ring-2 focus:ring-amber-500"
                  aria-label="Entity type"
                >
                  <option value="">— select entity type —</option>
                  {Object.entries(schemas.data ?? {}).map(([key, cfg]) => (
                    <option key={key} value={key}>
                      {cfg.label}
                    </option>
                  ))}
                </select>
                <button
                  type="button"
                  className="btn-primary text-sm"
                  disabled={!entityType || !pendingFile || doCommit.isPending}
                  onClick={() => {
                    if (pendingFile && entityType) {
                      doCommit.mutate({ file: pendingFile, type: entityType });
                    }
                  }}
                >
                  {doCommit.isPending ? "Committing…" : "Commit"}
                </button>
                <button
                  type="button"
                  className="btn-ghost text-sm"
                  onClick={() => {
                    setPreview(null);
                    setPendingFile(null);
                    setEntityType("");
                  }}
                >
                  Discard
                </button>
              </div>
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
            <p className="text-sm text-navy/70">Loading…</p>
          ) : (imports.data ?? []).length === 0 ? (
            <p className="text-sm text-navy/70">
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
                    <p className="text-xs text-navy/70">
                      {entry.rows_imported ?? 0} rows · source{" "}
                      {entry.source ?? "—"}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge tone={entry.status === "committed" ? "green" : "amber"}>
                      {entry.status ?? "pending"}
                    </Badge>
                    <button
                      className="btn-ghost"
                      type="button"
                      disabled={entry.status === "rolled_back" || doRollback.isPending}
                      onClick={() => doRollback.mutate(entry.id)}
                      title={
                        entry.status === "rolled_back"
                          ? "Already rolled back"
                          : "Restore pre-import snapshot"
                      }
                    >
                      <RotateCcw className="size-3" />{" "}
                      {doRollback.isPending ? "…" : "Rollback"}
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
          <p className="mt-4 text-xs text-navy/70">
            Inline edit lands with the Tab 11 wizard in Iteration 2. API is live —{" "}
            <code>PUT /api/v1/settings/&#123;key&#125;</code>.
          </p>
        </Card>
      </section>

      <Card>
        <CardHeader
          title="Currency rates"
          subtitle={
            rates.data && rates.data.length > 0
              ? `Last updated ${formatDate(rates.data[0].last_updated)} · source ${rates.data[0].source}`
              : "No rates loaded yet"
          }
          action={
            <button
              type="button"
              onClick={() => refreshRates.mutate()}
              disabled={refreshRates.isPending}
              className="btn-primary text-xs"
            >
              <RefreshCw
                className={`size-3 ${refreshRates.isPending ? "animate-spin" : ""}`}
                aria-hidden="true"
              />{" "}
              {refreshRates.isPending ? "Refreshing…" : "Refresh from ECB"}
            </button>
          }
        />
        {refreshRates.isError ? (
          <p className="mb-2 text-xs text-danger-600">
            {(refreshRates.error as Error).message}
          </p>
        ) : null}
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase text-navy/70">
              <th className="py-2">Code</th>
              <th>Symbol</th>
              <th className="text-right">Rate per 1 USD</th>
              <th>Source</th>
              <th>Last updated</th>
            </tr>
          </thead>
          <tbody>
            {(rates.data ?? []).map((r) => (
              <tr key={r.code} className="border-t border-ice-100">
                <td className="py-2 font-mono font-semibold">{r.code}</td>
                <td>{r.symbol ?? "—"}</td>
                <td className="text-right font-mono">
                  {Number(r.rate_to_base).toFixed(4)}
                </td>
                <td className="font-mono text-xs">{r.source}</td>
                <td className="text-xs text-navy/70">
                  {formatDate(r.last_updated)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="mt-3 text-xs text-navy/70">
          Refresh hits{" "}
          <a
            className="underline"
            href="https://www.frankfurter.app/"
            target="_blank"
            rel="noreferrer"
          >
            frankfurter.app
          </a>{" "}
          (European Central Bank mirror, no API key). If the container can't
          reach the internet, the dashboard keeps using the last stored rates
          and shows a 502 message here — no chart data is lost.
        </p>
      </Card>

      <Card>
        <CardHeader
          title="Guided onboarding wizard (preview)"
          subtitle="Four steps — base currency, fiscal year, programmes, data"
          action={
            <button
              type="button"
              className="btn-primary"
              onClick={() =>
                csvImportRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
              }
            >
              <Upload className="size-4" /> Start Import
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
                <span className="font-mono text-xs text-navy/70">
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
