import { Link } from "react-router-dom";
import { X } from "lucide-react";

/**
 * Centred modal listing every active programme as a clickable button.
 * Replaces the empty-state placeholder on bare /pnl by giving the
 * user a one-click path into a programme-filtered cockpit. Dismissable
 * with the X button, in which case the per-section "pick a programme"
 * placeholders remain as the secondary fallback.
 */

export type ProgrammeOption = {
  code: string;
  name: string;
};

export type ProgrammePickerModalProps = {
  open: boolean;
  onClose: () => void;
  programmes: ProgrammeOption[];
};

export function ProgrammePickerModal({
  open,
  onClose,
  programmes,
}: ProgrammePickerModalProps) {
  if (!open) return null;
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="programme-picker-title"
      className="fixed inset-0 z-50 flex items-center justify-center bg-navy/40 p-4"
      data-testid="programme-picker-modal"
    >
      <div className="w-full max-w-md rounded-lg border border-ice-100 bg-white p-5 shadow-md dark:border-navy-500 dark:bg-navy-700">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3
              id="programme-picker-title"
              className="text-base font-semibold text-navy dark:text-navy-50"
            >
              Pick a programme to open the P&L Cockpit
            </h3>
            <p className="mt-1 text-xs text-navy/70 dark:text-navy-100/70">
              The cockpit renders one programme at a time. Pick from the list below.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close programme picker"
            className="rounded p-1 text-navy/50 hover:bg-ice-50 hover:text-navy dark:hover:bg-navy-600 dark:hover:text-navy-50"
          >
            <X className="size-4" />
          </button>
        </div>
        <ul className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
          {programmes.map((p) => (
            <li key={p.code}>
              <Link
                to={`/pnl?programme=${encodeURIComponent(p.code)}`}
                onClick={onClose}
                className="block rounded border border-ice-100 px-3 py-2 text-sm text-navy hover:border-navy/30 hover:bg-ice-50 dark:border-navy-500 dark:text-navy-50 dark:hover:bg-navy-600"
                data-testid={`programme-picker-option-${p.code}`}
              >
                <div className="font-medium">{p.name}</div>
                <div className="text-[11px] text-navy/60 dark:text-navy-100/60">
                  {p.code}
                </div>
              </Link>
            </li>
          ))}
        </ul>
        {programmes.length === 0 && (
          <p className="mt-4 rounded border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-800">
            No programmes returned by the API. Check that the backend is up and
            seeded.
          </p>
        )}
      </div>
    </div>
  );
}
