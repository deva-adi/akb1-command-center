import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/cn";

type CardProps = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
};

export function Card({ className, children, ...rest }: CardProps) {
  return (
    <div className={cn("card", className)} {...rest}>
      {children}
    </div>
  );
}

type CardHeaderProps = {
  title: string;
  subtitle?: string;
  action?: ReactNode;
  className?: string;
};

export function CardHeader({ title, subtitle, action, className }: CardHeaderProps) {
  return (
    <div
      className={cn(
        "mb-4 flex items-start justify-between gap-3 border-b border-ice-100 pb-3",
        className,
      )}
    >
      <div>
        <h3 className="text-base font-semibold text-navy">{title}</h3>
        {subtitle ? (
          <p className="mt-0.5 text-xs text-navy/60">{subtitle}</p>
        ) : null}
      </div>
      {action ? <div className="shrink-0">{action}</div> : null}
    </div>
  );
}
