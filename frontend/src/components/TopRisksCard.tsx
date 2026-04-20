import { AlertTriangle } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { useTopRisks } from "@/hooks/usePortfolio";
import { formatCurrencyINR, type RagBucket } from "@/lib/format";

function severityTone(severity: string | null): RagBucket {
  const s = (severity ?? "").toLowerCase();
  if (s === "high" || s === "critical") return "red";
  if (s === "medium") return "amber";
  return "green";
}

export function TopRisksCard({ limit = 5 }: { limit?: number }) {
  const { data, isLoading, error } = useTopRisks(limit);

  return (
    <Card>
      <CardHeader
        title={`Top ${limit} risks`}
        subtitle="Sorted by financial impact (desc)"
        action={
          <AlertTriangle className="size-4 text-amber-500" aria-hidden="true" />
        }
      />
      {isLoading ? (
        <p className="text-sm text-navy/60">Loading…</p>
      ) : error ? (
        <p className="text-sm text-danger-600">
          {(error as Error).message}
        </p>
      ) : !data || data.length === 0 ? (
        <p className="text-sm text-navy/60">
          No risks recorded. Seed the NovaTech demo or import{" "}
          <code>risks.csv</code>.
        </p>
      ) : (
        <ol className="flex flex-col gap-2 text-sm">
          {data.map((risk, idx) => (
            <li
              key={risk.id}
              className="flex items-center justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2"
            >
              <div className="flex items-start gap-3">
                <span className="mt-0.5 font-mono text-xs text-navy/60">
                  {idx + 1}.
                </span>
                <div>
                  <p className="font-medium">{risk.title}</p>
                  {risk.owner ? (
                    <p className="text-xs text-navy/60">Owner: {risk.owner}</p>
                  ) : null}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge tone={severityTone(risk.severity)}>
                  {risk.severity ?? "—"}
                </Badge>
                <span className="font-mono text-xs text-navy/80">
                  {formatCurrencyINR(risk.impact)}
                </span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </Card>
  );
}
