import { AlertTriangle, ChevronRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { useTopRisks, useProgrammes } from "@/hooks/usePortfolio";
import { useCurrency } from "@/hooks/useCurrency";
import type { RagBucket } from "@/lib/format";

function severityTone(severity: string | null): RagBucket {
  const s = (severity ?? "").toLowerCase();
  if (s === "high" || s === "critical") return "red";
  if (s === "medium") return "amber";
  return "green";
}

export function TopRisksCard({ limit = 5 }: { limit?: number }) {
  const { data, isLoading, error } = useTopRisks(limit);
  const programmes = useProgrammes();
  const currency = useCurrency();
  const navigate = useNavigate();

  // Map program_id → native currency so we can convert impact amounts
  // correctly regardless of the selected display currency.
  const currencyByProgramme = new Map(
    (programmes.data ?? []).map((p) => [p.id, p.currency_code]),
  );
  const codeByProgramme = new Map(
    (programmes.data ?? []).map((p) => [p.id, p.code]),
  );

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
          {data.map((risk, idx) => {
            const programmeCode =
              risk.program_id !== null
                ? codeByProgramme.get(risk.program_id)
                : null;
            const sourceCurrency =
              (risk.program_id !== null &&
                currencyByProgramme.get(risk.program_id)) ||
              "USD";
            const drillTo = programmeCode
              ? `/delivery?programme=${programmeCode}`
              : null;
            return (
              <li key={risk.id}>
                <button
                  type="button"
                  onClick={() => drillTo && navigate(drillTo)}
                  disabled={!drillTo}
                  className="group flex w-full items-center justify-between gap-3 rounded border border-ice-100 bg-white px-3 py-2 text-left transition hover:bg-ice-50 disabled:cursor-default disabled:hover:bg-white"
                  aria-label={
                    drillTo
                      ? `Drill into ${programmeCode} for ${risk.title}`
                      : risk.title
                  }
                >
                  <div className="flex items-start gap-3">
                    <span className="mt-0.5 font-mono text-xs text-navy/60">
                      {idx + 1}.
                    </span>
                    <div>
                      <p className="font-medium">{risk.title}</p>
                      <p className="text-xs text-navy/60">
                        {programmeCode ? `${programmeCode} · ` : ""}
                        {risk.owner ? `Owner: ${risk.owner}` : ""}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge tone={severityTone(risk.severity)}>
                      {risk.severity ?? "—"}
                    </Badge>
                    <span className="font-mono text-xs text-navy/80">
                      {currency.format(risk.impact, sourceCurrency)}
                    </span>
                    {drillTo ? (
                      <ChevronRight
                        className="size-4 text-navy/40 transition group-hover:text-navy"
                        aria-hidden="true"
                      />
                    ) : null}
                  </div>
                </button>
              </li>
            );
          })}
        </ol>
      )}
    </Card>
  );
}
