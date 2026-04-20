import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { ChevronRight } from "lucide-react";
import { cn } from "@/lib/cn";

export type BreadcrumbItem = {
  label: string;
  /** Absolute path. Leaf item should omit `to` (it's not a link). */
  to?: string;
  icon?: ReactNode;
};

export function Breadcrumb({ items, className }: { items: BreadcrumbItem[]; className?: string }) {
  return (
    <nav
      aria-label="Breadcrumb"
      className={cn("flex flex-wrap items-center gap-1 text-xs text-navy/60", className)}
    >
      {items.map((item, idx) => {
        const isLast = idx === items.length - 1;
        const content = (
          <span className="inline-flex items-center gap-1">
            {item.icon}
            {item.label}
          </span>
        );
        return (
          <span key={`${item.label}-${idx}`} className="inline-flex items-center gap-1">
            {item.to && !isLast ? (
              <Link
                to={item.to}
                className="rounded px-1 py-0.5 text-navy/70 transition hover:bg-ice-100 hover:text-navy"
              >
                {content}
              </Link>
            ) : (
              <span
                className={cn(
                  "px-1 py-0.5",
                  isLast ? "font-semibold text-navy" : "text-navy/70",
                )}
                aria-current={isLast ? "page" : undefined}
              >
                {content}
              </span>
            )}
            {!isLast ? (
              <ChevronRight className="size-3 text-navy/40" aria-hidden="true" />
            ) : null}
          </span>
        );
      })}
    </nav>
  );
}
