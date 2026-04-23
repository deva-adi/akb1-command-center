import { Link } from "react-router-dom";
import { ArrowRight, X } from "lucide-react";
import type { ReactNode } from "react";

/**
 * Inline expand-collapse drill panel used across the Tab 12 cockpit.
 * Renders below a section card. Title and close button at the top,
 * caller-provided children in the body, optional cross-tab Link at
 * the bottom that uses React Router so the active programme query
 * param travels with the user.
 */

export type DrillPanelProps = {
  title: string;
  onClose: () => void;
  /** Optional v5.8-stub note shown above the children when backend
   * granularity is not yet seeded. */
  stubNote?: string;
  /** Cross-tab "view in" link rendered at the bottom. */
  crossTab?: { label: string; href: string };
  children: ReactNode;
};

export function DrillPanel({
  title,
  onClose,
  stubNote,
  crossTab,
  children,
}: DrillPanelProps) {
  return (
    <div
      className="mt-4 rounded border border-ice-100 bg-slate-50 p-4 dark:border-navy-500 dark:bg-navy-700/40"
      data-testid="drill-panel"
    >
      <div className="flex items-start justify-between gap-3">
        <h4
          className="text-sm font-semibold text-navy dark:text-navy-50"
          data-testid="drill-panel-title"
        >
          {title}
        </h4>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close drill panel"
          className="rounded p-1 text-navy/50 hover:bg-white hover:text-navy dark:hover:bg-navy-600 dark:hover:text-navy-50"
        >
          <X className="size-4" />
        </button>
      </div>
      {stubNote && (
        <p
          className="mt-2 rounded border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-800"
          data-testid="drill-panel-stub-note"
        >
          {stubNote}
        </p>
      )}
      <div className="mt-3 text-xs text-navy/80 dark:text-navy-100/80">
        {children}
      </div>
      {crossTab && (
        <div className="mt-3 border-t border-ice-100 pt-3 dark:border-navy-500">
          <Link
            to={crossTab.href}
            className="inline-flex items-center gap-1 text-xs font-medium text-navy hover:underline dark:text-navy-50"
            data-testid="drill-panel-cross-tab"
          >
            {crossTab.label}
            <ArrowRight className="size-3" />
          </Link>
        </div>
      )}
    </div>
  );
}
