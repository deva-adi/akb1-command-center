import { AlertOctagon, Radio } from "lucide-react";
import { useAlertsStream, type StreamAlert } from "@/hooks/useAlertsStream";
import { formatCurrency } from "@/lib/format";
import { useUiStore } from "@/stores/uiStore";

const STATUS_DOT: Record<string, string> = {
  Active: "bg-danger-500",
  Monitoring: "bg-amber-500",
};

function AlertChip({ alert, currency }: { alert: StreamAlert; currency: string }) {
  const dot = STATUS_DOT[alert.status] ?? "bg-navy/30";
  return (
    <span className="inline-flex shrink-0 items-center gap-2 rounded-full border border-ice-100 bg-white px-3 py-1 text-xs font-medium text-navy shadow-sm dark:border-navy-500 dark:bg-navy-600 dark:text-navy-100">
      <span className={`size-2 rounded-full ${dot}`} aria-hidden="true" />
      <span className="font-semibold">{alert.status.toUpperCase()}</span>
      <span>{alert.name}</span>
      {alert.impact !== null && alert.impact !== 0 ? (
        <span className="font-mono text-navy/70 dark:text-navy-100/70">
          {formatCurrency(alert.impact, currency as "USD")}
        </span>
      ) : null}
    </span>
  );
}

export function AlertsTicker() {
  const alerts = useAlertsStream();
  const baseCurrency = useUiStore((s) => s.baseCurrency);

  if (alerts.length === 0) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      aria-label="Smart Ops live alerts"
      className="flex items-center gap-3 overflow-hidden rounded-lg border border-ice-100 bg-ice-50 px-4 py-2 dark:border-navy-500 dark:bg-navy-700"
    >
      <span className="flex shrink-0 items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-navy/70 dark:text-navy-100/70">
        <Radio className="size-3 text-danger-500" aria-hidden="true" />
        Live alerts
      </span>
      <div
        className="flex min-w-0 flex-1 gap-3 overflow-x-auto pb-0.5"
        tabIndex={0}
        role="region"
        aria-label="Alert chips scrollable list"
      >
        {alerts.map((a) => (
          <AlertChip key={a.id} alert={a} currency={baseCurrency} />
        ))}
        {alerts.length === 0 ? (
          <span className="flex items-center gap-1 text-xs text-navy/70 dark:text-navy-100/70">
            <AlertOctagon className="size-3" aria-hidden="true" />
            No active alerts
          </span>
        ) : null}
      </div>
    </div>
  );
}
