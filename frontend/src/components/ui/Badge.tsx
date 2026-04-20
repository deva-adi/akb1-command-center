import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import type { RagBucket } from "@/lib/format";

type BadgeProps = {
  tone?: RagBucket | "neutral";
  className?: string;
  children: ReactNode;
};

const toneClasses: Record<NonNullable<BadgeProps["tone"]>, string> = {
  green: "status-green",
  amber: "status-amber",
  red: "status-red",
  neutral: "bg-ice-100 text-navy",
};

export function Badge({ tone = "neutral", className, children }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold",
        toneClasses[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}
