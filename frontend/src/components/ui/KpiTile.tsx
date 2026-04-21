import type { ReactNode } from "react";
import { ChevronRight } from "lucide-react";
import { cn } from "@/lib/cn";

type KpiTileProps = {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  trend?: "up" | "down" | "flat";
  className?: string;
  onClick?: () => void;
};

const trendChar: Record<NonNullable<KpiTileProps["trend"]>, string> = {
  up: "↑",
  down: "↓",
  flat: "→",
};

export function KpiTile({ label, value, sub, trend, className, onClick }: KpiTileProps) {
  const Tag = onClick ? "button" : "div";
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
        {onClick ? <ChevronRight className="size-3 text-navy/40" aria-hidden="true" /> : null}
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
    </Tag>
  );
}
