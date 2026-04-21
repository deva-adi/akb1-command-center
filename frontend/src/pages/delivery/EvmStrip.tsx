import { useCurrency } from "@/hooks/useCurrency";
import type { EvmSnapshot, ProjectListItem } from "@/lib/api";
import { formatPct, formatRatio, type RagBucket } from "@/lib/format";
import { MetricCard } from "@/components/ui/MetricCard";

export function EvmStrip({
  evm,
  project,
  sourceCurrency,
  programmeCode,
  onNavigate,
}: {
  evm: EvmSnapshot[];
  project: ProjectListItem;
  sourceCurrency: string;
  programmeCode?: string;
  onNavigate?: (path: string) => void;
}) {
  const currency = useCurrency();
  const latest = evm.length > 0 ? evm[evm.length - 1] : null;

  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
      <MetricCard
        metricId="cpi"
        value={formatRatio(latest?.cpi)}
        tone={toneForIndex(latest?.cpi ?? null)}
        onClick={onNavigate ? () => onNavigate(programmeCode ? `/margin?programme=${programmeCode}` : '/margin') : undefined}
      />
      <MetricCard
        metricId="spi"
        value={formatRatio(latest?.spi)}
        tone={toneForIndex(latest?.spi ?? null)}
        onClick={onNavigate ? () => onNavigate(programmeCode ? `/margin?programme=${programmeCode}` : '/margin') : undefined}
      />
      <MetricCard
        metricId="eac"
        value={currency.format(latest?.eac ?? null, sourceCurrency)}
        sub={`BAC ${currency.format(project.id ? latest?.bac ?? null : null, sourceCurrency)}`}
      />
      <MetricCard
        metricId="tcpi"
        value={formatRatio(latest?.tcpi)}
        tone={toneForIndex(latest?.tcpi ?? null, true)}
      />
      <MetricCard
        metricId="percent_complete"
        value={formatPct(latest ? (latest.percent_complete ?? 0) / 100 : null)}
      />
    </div>
  );
}

function toneForIndex(
  value: number | null,
  isTcpi = false,
): RagBucket | "neutral" {
  if (value === null) return "neutral";
  if (isTcpi) {
    if (value <= 1.05) return "green";
    if (value <= 1.15) return "amber";
    return "red";
  }
  if (value >= 1.0) return "green";
  if (value >= 0.9) return "amber";
  return "red";
}
