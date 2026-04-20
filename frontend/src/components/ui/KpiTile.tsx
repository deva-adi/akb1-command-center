import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

type KpiTileProps = {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  trend?: "up" | "down" | "flat";
  className?: string;
};

const trendChar: Record<NonNullable<KpiTileProps["trend"]>, string> = {
  up: "↑",
  down: "↓",
  flat: "→",
};

export function KpiTile({ label, value, sub, trend, className }: KpiTileProps) {
  return (
    <div className={cn("card flex flex-col justify-between gap-2", className)}>
      <span className="kpi-label">{label}</span>
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
    </div>
  );
}
