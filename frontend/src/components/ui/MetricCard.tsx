/**
 * Universal metric display component with inline formula / business-context reveal.
 * Replaces SprintStat, EvmCell, FlowStat, KpiMini across all tabs.
 *
 * Usage:
 *   <MetricCard metricId="cpi" value="1.04" tone="green" onClick={...} active={...} />
 *   <MetricCard label="Custom metric" value="42" formula="x/y" description="..." />
 */

import { useState, type ReactNode } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/cn";
import { getMetric, type MetricDef, type DrillFilter } from "@/lib/metrics";
import type { RagBucket } from "@/lib/format";

type MetricCardProps = {
  /** Key into ALL_METRICS — pulls label/formula/description automatically */
  metricId?: string;

  /** Override or provide label directly (used when metricId is absent) */
  label?: string;
  formula?: string;
  description?: string;
  interpretation?: string;
  thresholdsText?: string;

  value: ReactNode;
  sub?: ReactNode;
  tone?: RagBucket | "neutral";

  /** Highlight the card as the active drill target */
  active?: boolean;

  /** Make the card clickable; shows drill hint */
  onClick?: () => void;

  /** What filter this card drills into — shown in the hint text */
  drillFilter?: DrillFilter;

  className?: string;
};

export function MetricCard({
  metricId,
  label: labelProp,
  formula: formulaProp,
  description: descProp,
  interpretation: interpProp,
  thresholdsText,
  value,
  sub,
  tone = "neutral",
  active,
  onClick,
  drillFilter,
  className,
}: MetricCardProps) {
  const [formulaOpen, setFormulaOpen] = useState(false);

  const def: MetricDef | undefined = metricId ? getMetric(metricId) : undefined;

  const label = labelProp ?? def?.label ?? metricId ?? "Metric";
  const formula = formulaProp ?? def?.formula;
  const description = descProp ?? def?.description;
  const interpretation = interpProp ?? def?.interpretation;
  const thresholds =
    thresholdsText ??
    (def?.thresholds
      ? `Green: ${def.thresholds.green} · Amber: ${def.thresholds.amber} · Red: ${def.thresholds.red}`
      : undefined);

  const hasFormula = !!(formula || description);
  const isClickable = !!onClick;

  function handleFormulaToggle(e: React.MouseEvent) {
    e.stopPropagation();
    setFormulaOpen((v) => !v);
  }

  return (
    <div
      className={cn(
        "flex flex-col gap-1 rounded border px-3 py-2 bg-white transition",
        isClickable && "cursor-pointer hover:bg-ice-50",
        active ? "border-navy/30 ring-2 ring-navy/20 bg-navy/[0.03]" : "border-ice-100",
        className,
      )}
      onClick={onClick}
      role={isClickable ? "button" : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onKeyDown={isClickable ? (e) => e.key === "Enter" && onClick?.() : undefined}
      aria-pressed={isClickable ? active : undefined}
    >
      {/* ── Header row ── */}
      <div className="flex items-center justify-between gap-1">
        <span className="kpi-label">{label}</span>
        {hasFormula && (
          <button
            type="button"
            onClick={handleFormulaToggle}
            className="shrink-0 rounded p-0.5 text-navy/40 transition hover:bg-ice-100 hover:text-navy"
            aria-label={formulaOpen ? `Hide how ${label} is calculated` : `How ${label} is calculated`}
            title={formulaOpen ? "Hide formula" : "How is this calculated?"}
          >
            {formulaOpen ? <EyeOff className="size-3" /> : <Eye className="size-3" />}
          </button>
        )}
      </div>

      {/* ── Value ── */}
      <div className="flex items-center gap-2">
        <Badge tone={tone}>{value}</Badge>
      </div>

      {/* ── Optional sub-text (e.g. "avg 42") ── */}
      {sub && <span className="text-xs text-navy/60">{sub}</span>}

      {/* ── Drill hint ── */}
      {isClickable && (
        <span className="text-[10px] text-navy/40">
          {active
            ? "▲ close table"
            : drillFilter
              ? `▼ drill → ${drillFilter.replace("_", " ")} items`
              : "▼ click to drill"}
        </span>
      )}

      {/* ── Inline formula panel ── */}
      {formulaOpen && (
        <div className="mt-2 rounded bg-navy/[0.04] px-3 py-2 text-xs space-y-2 border border-navy/10">
          {formula && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">Formula</p>
              <code className="font-mono text-navy break-all">{formula}</code>
            </div>
          )}
          {description && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">What it measures</p>
              <p className="text-navy/80 leading-relaxed">{description}</p>
            </div>
          )}
          {interpretation && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">How to use it</p>
              <p className="text-navy/80 leading-relaxed">{interpretation}</p>
            </div>
          )}
          {thresholds && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">Thresholds</p>
              <p className="text-navy/70">{thresholds}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
