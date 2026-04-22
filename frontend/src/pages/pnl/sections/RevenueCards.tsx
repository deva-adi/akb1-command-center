import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { Card, CardHeader } from "@/components/ui/Card";
import { MetricCard } from "@/components/ui/MetricCard";
import {
  fetchPnlDso,
  fetchPnlRevenue,
  type DsoOut,
  type PnlErrorEnvelope,
  type PnlFilters,
  type RevenueOut,
} from "@/api/pnlApi";
import { formatCurrency } from "@/lib/format";
import type { RagBucket } from "@/lib/format";

/**
 * Section 1 of Tab 12: Revenue cards with period-over-period deltas.
 *
 * Five cards: Booked, Billed, Collected, Unbilled WIP, AR Balance.
 * First four come from /api/v1/pnl/revenue; AR Balance comes from
 * /api/v1/pnl/dso. Deltas compute client-side: fire a second fetch
 * for the snapshot one month prior to the current response, subtract,
 * render absolute + percentage with a sign.
 *
 * State handling:
 *   1. No ?programme= in the URL -> prompt the user to pick one from
 *      ContextRail. No network activity.
 *   2. Queries in-flight -> five skeleton cards so the layout stays
 *      stable.
 *   3. Either query errored -> single error banner with the message
 *      from the backend's error envelope.
 *   4. Populated -> five MetricCards with current value + delta sub.
 */

type CardKey = "booked" | "billed" | "collected" | "unbilled_wip" | "ar";

type CardSpec = {
  key: CardKey;
  label: string;
  metricId?: string;
  // Positive delta is "good" for revenue earned; "bad" for balances stuck.
  positiveIsGood: boolean;
};

const CARDS: CardSpec[] = [
  { key: "booked", label: "Booked revenue", metricId: "revenue", positiveIsGood: true },
  { key: "billed", label: "Billed revenue", positiveIsGood: true },
  { key: "collected", label: "Collected revenue", positiveIsGood: true },
  { key: "unbilled_wip", label: "Unbilled WIP", positiveIsGood: false },
  { key: "ar", label: "AR balance", positiveIsGood: false },
];

function priorPeriodFilters(currentSnapshot: string | null): PnlFilters | null {
  if (!currentSnapshot) return null;
  const d = new Date(`${currentSnapshot}T00:00:00Z`);
  if (Number.isNaN(d.getTime())) return null;
  // Pick "the day before the current snapshot" as `to` so the backend
  // picks the previous monthly snapshot via its <= latest-of logic.
  const priorEnd = new Date(d);
  priorEnd.setUTCDate(priorEnd.getUTCDate() - 1);
  // Anchor `from` to the first of the prior month so the window is
  // self-documenting in the URL echo.
  const priorStart = new Date(
    Date.UTC(priorEnd.getUTCFullYear(), priorEnd.getUTCMonth(), 1),
  );
  const toIso = (dt: Date) => dt.toISOString().slice(0, 10);
  return { from: toIso(priorStart), to: toIso(priorEnd) };
}

function errorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const envelope = err.response?.data as PnlErrorEnvelope | undefined;
    if (envelope?.error?.message) return envelope.error.message;
    return err.message;
  }
  if (err instanceof Error) return err.message;
  return "Unknown error";
}

function cardValue(
  key: CardKey,
  revenue: RevenueOut | undefined,
  dso: DsoOut | undefined,
): number | null {
  if (key === "ar") return dso?.ar_balance ?? null;
  const card = revenue?.cards.find(
    (c) =>
      c.card_key ===
      (
        {
          booked: "booked_revenue",
          billed: "billed_revenue",
          collected: "collected_revenue",
          unbilled_wip: "unbilled_wip",
        } as const
      )[key],
  );
  return card?.value ?? null;
}

function toneFor(
  positiveIsGood: boolean,
  delta: number | null,
): RagBucket | "neutral" {
  if (delta === null) return "neutral";
  if (delta === 0) return "neutral";
  const favourable = positiveIsGood ? delta > 0 : delta < 0;
  return favourable ? "green" : "red";
}

function formatDeltaSub(
  current: number | null,
  prior: number | null,
): string {
  if (current === null) return "—";
  if (prior === null) return "— (no prior snapshot)";
  const delta = current - prior;
  const sign = delta > 0 ? "+" : delta < 0 ? "−" : "";
  const abs = formatCurrency(Math.abs(delta));
  if (prior === 0) return `${sign}${abs} (—)`;
  const pct = ((delta / Math.abs(prior)) * 100).toFixed(1);
  const pctSign = delta > 0 ? "+" : delta < 0 ? "−" : "";
  return `${sign}${abs} (${pctSign}${Math.abs(Number(pct))}%)`;
}

export function RevenueCards() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");

  const filters: PnlFilters = {
    from: searchParams.get("from") ?? undefined,
    to: searchParams.get("to") ?? undefined,
    scenario_name: searchParams.get("scenario_name") ?? undefined,
  };

  const revenueQuery = useQuery<RevenueOut, AxiosError>({
    queryKey: ["pnl", "revenue", programme, filters],
    queryFn: () => fetchPnlRevenue(programme!, filters),
    enabled: !!programme,
  });

  const dsoQuery = useQuery<DsoOut, AxiosError>({
    queryKey: ["pnl", "dso", programme, filters],
    queryFn: () => fetchPnlDso(programme!, filters),
    enabled: !!programme,
  });

  const currentSnapshot =
    revenueQuery.data?.snapshot_date ??
    dsoQuery.data?.snapshot_date ??
    null;
  const priorFilters = priorPeriodFilters(currentSnapshot);

  const priorRevenueQuery = useQuery<RevenueOut, AxiosError>({
    queryKey: ["pnl", "revenue", "prior", programme, priorFilters],
    queryFn: () => fetchPnlRevenue(programme!, priorFilters!),
    enabled: !!programme && !!priorFilters,
  });

  const priorDsoQuery = useQuery<DsoOut, AxiosError>({
    queryKey: ["pnl", "dso", "prior", programme, priorFilters],
    queryFn: () => fetchPnlDso(programme!, priorFilters!),
    enabled: !!programme && !!priorFilters,
  });

  if (!programme) {
    return (
      <Card>
        <CardHeader
          title="Pick a programme to see revenue"
          subtitle="Select a programme from the ContextRail breadcrumb, the sidebar link, or add ?programme=PHOENIX to the URL."
        />
      </Card>
    );
  }

  const loading = revenueQuery.isLoading || dsoQuery.isLoading;
  const firstError = revenueQuery.error ?? dsoQuery.error;

  if (firstError) {
    return (
      <Card>
        <CardHeader
          title="Revenue section failed to load"
          subtitle="Try refreshing or check the backend logs at /api/v1/pnl."
        />
        <div
          role="alert"
          className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {errorMessage(firstError)}
        </div>
      </Card>
    );
  }

  if (loading || !revenueQuery.data || !dsoQuery.data) {
    return (
      <Card>
        <CardHeader
          title="Revenue"
          subtitle="Loading current and prior snapshots from the backend."
        />
        <div
          className="grid grid-cols-2 gap-3 md:grid-cols-5"
          data-testid="revenue-cards-loading"
        >
          {CARDS.map((c) => (
            <div
              key={c.key}
              className="h-24 animate-pulse rounded border border-ice-100 bg-ice-50"
              aria-label={`${c.label} loading`}
            />
          ))}
        </div>
      </Card>
    );
  }

  const subtitleParts = [
    revenueQuery.data.snapshot_date
      ? `Snapshot ${revenueQuery.data.snapshot_date}`
      : null,
    revenueQuery.data.scenario_name
      ? `scenario ${revenueQuery.data.scenario_name}`
      : null,
  ].filter(Boolean);

  return (
    <Card>
      <CardHeader
        title="Revenue"
        subtitle={
          subtitleParts.length
            ? subtitleParts.join(" · ")
            : "Revenue cards for the active programme."
        }
      />
      <div
        className="grid grid-cols-2 gap-3 md:grid-cols-5"
        data-testid="revenue-cards"
      >
        {CARDS.map((spec) => {
          const current = cardValue(
            spec.key,
            revenueQuery.data,
            dsoQuery.data,
          );
          const prior = cardValue(
            spec.key,
            priorRevenueQuery.data,
            priorDsoQuery.data,
          );
          const delta =
            current !== null && prior !== null ? current - prior : null;
          return (
            <MetricCard
              key={spec.key}
              metricId={spec.metricId}
              label={spec.label}
              value={formatCurrency(current)}
              sub={formatDeltaSub(current, prior)}
              tone={toneFor(spec.positiveIsGood, delta)}
            />
          );
        })}
      </div>
    </Card>
  );
}
