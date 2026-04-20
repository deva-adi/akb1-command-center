import { useCurrency } from "@/hooks/useCurrency";
import type { EvmSnapshot, ProjectListItem } from "@/lib/api";
import { formatPct, formatRatio, type RagBucket } from "@/lib/format";
import { Badge } from "@/components/ui/Badge";

export function EvmStrip({
  evm,
  project,
  sourceCurrency,
}: {
  evm: EvmSnapshot[];
  project: ProjectListItem;
  sourceCurrency: string;
}) {
  const currency = useCurrency();
  const latest = evm.length > 0 ? evm[evm.length - 1] : null;

  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
      <EvmCell
        label="CPI"
        value={formatRatio(latest?.cpi)}
        tone={toneForIndex(latest?.cpi ?? null)}
      />
      <EvmCell
        label="SPI"
        value={formatRatio(latest?.spi)}
        tone={toneForIndex(latest?.spi ?? null)}
      />
      <EvmCell
        label="EAC"
        value={currency.format(latest?.eac ?? null, sourceCurrency)}
        sub={`BAC ${currency.format(project.id ? latest?.bac ?? null : null, sourceCurrency)}`}
      />
      <EvmCell
        label="TCPI"
        value={formatRatio(latest?.tcpi)}
        tone={toneForIndex(latest?.tcpi ?? null, true)}
      />
      <EvmCell
        label="% Complete"
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
  // CPI/SPI: ≥1.0 green, 0.9–1.0 amber, <0.9 red
  // TCPI: <1.05 green, 1.05–1.15 amber, >1.15 red (higher = more work per $)
  if (isTcpi) {
    if (value <= 1.05) return "green";
    if (value <= 1.15) return "amber";
    return "red";
  }
  if (value >= 1.0) return "green";
  if (value >= 0.9) return "amber";
  return "red";
}

function EvmCell({
  label,
  value,
  sub,
  tone = "neutral",
}: {
  label: string;
  value: string;
  sub?: string;
  tone?: RagBucket | "neutral";
}) {
  return (
    <div className="flex flex-col gap-1 rounded border border-ice-100 bg-white px-3 py-2">
      <span className="kpi-label">{label}</span>
      <div className="flex items-center gap-2">
        <Badge tone={tone}>{value}</Badge>
      </div>
      {sub ? <span className="text-xs text-navy/70">{sub}</span> : null}
    </div>
  );
}
