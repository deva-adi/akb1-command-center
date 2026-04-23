import { Info } from "lucide-react";

/**
 * Inline info icon with a hover popover, used at section, column, and
 * metric-label scope across the Tab 12 cockpit. Single component for
 * all three scopes since the visual treatment is identical and only
 * the placement varies.
 *
 * Hover-to-open behaviour relies on a CSS group hover so the popover
 * appears without a controlled-state click. Touch users do not get a
 * popover today; that's a known limitation tracked alongside the rest
 * of the cockpit interactivity in TECH_DEBT.md if it becomes a real
 * problem.
 */

export type PnlSectionInfoProps = {
  title: string;
  whatItShows: string;
  formula?: string;
  howToRead: string;
  thresholds?: string;
  /** Aria label used by screen readers and Playwright locators. */
  ariaLabel?: string;
};

export function PnlSectionInfo({
  title,
  whatItShows,
  formula,
  howToRead,
  thresholds,
  ariaLabel,
}: PnlSectionInfoProps) {
  return (
    <span
      className="group relative ml-1.5 inline-flex items-center align-middle"
      data-testid="pnl-section-info"
    >
      <Info
        size={13}
        className="text-slate-400"
        aria-label={ariaLabel ?? `Info about ${title}`}
      />
      <span
        role="tooltip"
        className="pointer-events-none absolute left-1/2 top-full z-50 mt-1.5 hidden w-[300px] -translate-x-1/2 rounded-lg border border-slate-200 bg-white p-3 text-xs text-navy shadow-md group-hover:block dark:border-navy-500 dark:bg-navy-700 dark:text-navy-50"
      >
        <p className="text-sm font-semibold text-navy dark:text-navy-50">
          {title}
        </p>
        <p className="mt-2 text-navy/80 dark:text-navy-100/80">
          <span className="font-semibold">What it shows: </span>
          {whatItShows}
        </p>
        {formula && (
          <p className="mt-2">
            <span className="font-semibold">Formula: </span>
            <code className="font-mono text-[11px] text-navy dark:text-navy-50">
              {formula}
            </code>
          </p>
        )}
        <p className="mt-2 text-navy/80 dark:text-navy-100/80">
          <span className="font-semibold">How to read it: </span>
          {howToRead}
        </p>
        {thresholds && (
          <p className="mt-2 text-navy/80 dark:text-navy-100/80">
            <span className="font-semibold">Thresholds: </span>
            {thresholds}
          </p>
        )}
      </span>
    </span>
  );
}
