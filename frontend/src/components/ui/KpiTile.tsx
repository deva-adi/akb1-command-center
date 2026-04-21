import { useState, type ReactNode } from "react";
import { ChevronRight, Eye, EyeOff } from "lucide-react";
import { cn } from "@/lib/cn";
import { getMetric } from "@/lib/metrics";

type KpiTileProps = {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  trend?: "up" | "down" | "flat";
  className?: string;
  onClick?: () => void;
  /** Optional: wire to a MetricDef for inline formula reveal */
  metricId?: string;
};

const trendChar: Record<NonNullable<KpiTileProps["trend"]>, string> = {
  up: "↑",
  down: "↓",
  flat: "→",
};

export function KpiTile({ label, value, sub, trend, className, onClick, metricId }: KpiTileProps) {
  const [formulaOpen, setFormulaOpen] = useState(false);
  const def = metricId ? getMetric(metricId) : undefined;
  const hasFormula = !!def;

  const Tag = onClick ? "button" : "div";

  function handleFormulaToggle(e: React.MouseEvent) {
    e.stopPropagation();
    setFormulaOpen((v) => !v);
  }

  return (
    <Tag
      type={onClick ? "button" : undefined}
      onClick={onClick}
      className={cn(
        "card flex flex-col justify-between gap-2",
        onClick && "cursor-pointer transition hover:ring-2 hover:ring-navy/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy/40",
        className,
      )}
      aria-label={onClick ? `Drill into ${label}` : undefined}
    >
      <div className="flex items-center justify-between gap-1">
        <span className="kpi-label">{label}</span>
        <div className="flex items-center gap-1">
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
          {onClick ? <ChevronRight className="size-3 text-navy/40" aria-hidden="true" /> : null}
        </div>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="kpi-value">{value}</span>
        {trend ? (
          <span
            className={cn(
              "text-sm font-semibold",
              trend === "up" && "text-success-600",
              trend === "down" && "text-danger-600",
              trend === "flat" && "text-navy/70",
            )}
          >
            {trendChar[trend]}
          </span>
        ) : null}
      </div>
      {sub ? <span className="kpi-sub">{sub}</span> : null}

      {formulaOpen && def && (
        <div className="mt-1 rounded bg-navy/[0.04] px-3 py-2 text-xs space-y-2 border border-navy/10">
          <div>
            <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">Formula</p>
            <code className="font-mono text-navy break-all">{def.formula}</code>
          </div>
          {def.description && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">What it measures</p>
              <p className="text-navy/80 leading-relaxed">{def.description}</p>
            </div>
          )}
          {def.interpretation && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">How to use it</p>
              <p className="text-navy/80 leading-relaxed">{def.interpretation}</p>
            </div>
          )}
          {def.thresholds && (
            <div>
              <p className="font-semibold text-navy/70 uppercase tracking-wide text-[10px] mb-0.5">Thresholds</p>
              <p className="text-navy/70">Green: {def.thresholds.green} · Amber: {def.thresholds.amber} · Red: {def.thresholds.red}</p>
            </div>
          )}
        </div>
      )}
    </Tag>
  );
}
