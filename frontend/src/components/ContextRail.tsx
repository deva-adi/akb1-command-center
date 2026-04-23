import { useMemo, useRef, useState, useEffect } from "react";
import { Link, useLocation, useSearchParams } from "react-router-dom";
import { ChevronRight, Home, ChevronDown } from "lucide-react";
import { findTabByPath, TABS } from "@/lib/tabRegistry";
import { useProgrammes } from "@/hooks/usePortfolio";

type MetricOption = { value: string; label: string };

type ContextRailProps = {
  metricOptions?: MetricOption[];
};

type FilterKey =
  | "programme"
  | "metric"
  | "from"
  | "to"
  | "month"
  | "tier"
  | "scenario_name"
  | "portfolio";

function buildUrl(pathname: string, params: URLSearchParams, keep: FilterKey[]): string {
  const next = new URLSearchParams();
  for (const key of keep) {
    const v = params.get(key);
    if (v !== null && v !== "") next.set(key, v);
  }
  const qs = next.toString();
  return qs ? `${pathname}?${qs}` : pathname;
}

function formatPeriod(params: URLSearchParams): string | null {
  const month = params.get("month");
  if (month) {
    const d = new Date(`${month}T00:00:00Z`);
    if (!Number.isNaN(d.getTime())) {
      return d.toLocaleString("en-GB", { month: "short", year: "numeric", timeZone: "UTC" });
    }
  }
  const from = params.get("from");
  const to = params.get("to");
  if (from && to) return `${from} → ${to}`;
  if (from) return `from ${from}`;
  if (to) return `to ${to}`;
  return null;
}

function humaniseMetric(value: string): string {
  const last = value.split(".").pop() ?? value;
  return last.replace(/_/g, " ");
}

export function ContextRail({ metricOptions }: ContextRailProps) {
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const programmesQuery = useProgrammes();

  const tab = useMemo(() => findTabByPath(location.pathname), [location.pathname]);

  const programmeCode = searchParams.get("programme");
  const metric = searchParams.get("metric");
  const tier = searchParams.get("tier");
  const period = useMemo(() => formatPeriod(searchParams), [searchParams]);

  const programmeLabel = useMemo(() => {
    if (!programmeCode) return null;
    const hit = programmesQuery.data?.find((p) => p.code === programmeCode);
    return hit?.name ?? programmeCode;
  }, [programmeCode, programmesQuery.data]);

  const path = location.pathname;
  const portfolioUrl = "/";
  const tabUrl = tab ? buildUrl(tab.path, searchParams, []) : path;
  const programmeUrl = tab ? buildUrl(tab.path, searchParams, ["programme"]) : path;
  const metricUrl = tab
    ? buildUrl(tab.path, searchParams, ["programme", "metric"])
    : path;
  const periodUrl = tab
    ? buildUrl(tab.path, searchParams, ["programme", "metric", "from", "to", "month"])
    : path;

  return (
    <nav
      aria-label="Context breadcrumb"
      data-testid="context-rail"
      className="flex flex-wrap items-center gap-1 border-b border-ice-100 bg-white px-6 py-2 text-xs text-navy/70 dark:border-navy-500 dark:bg-navy-700 dark:text-navy-100/80"
    >
      <Link
        to={portfolioUrl}
        className="inline-flex items-center gap-1 rounded px-1 py-0.5 hover:bg-ice-50 hover:text-navy dark:hover:bg-navy-600"
        data-rail-segment="portfolio"
      >
        <Home className="size-3" aria-hidden="true" />
        Portfolio
      </Link>

      {tab && (
        <>
          <Separator />
          <Link
            to={tabUrl}
            className="rounded px-1 py-0.5 hover:bg-ice-50 hover:text-navy dark:hover:bg-navy-600"
            data-rail-segment="tab"
          >
            {tab.label}
          </Link>
        </>
      )}

      {programmeCode && (
        <>
          <Separator />
          <ProgrammeSegment
            label={programmeLabel ?? programmeCode}
            code={programmeCode}
            drillUpHref={programmeUrl}
            searchParams={searchParams}
            pathname={path}
          />
        </>
      )}

      {metric && (
        <>
          <Separator />
          <MetricSegment
            label={humaniseMetric(metric)}
            value={metric}
            options={metricOptions}
            drillUpHref={metricUrl}
            searchParams={searchParams}
            pathname={path}
          />
        </>
      )}

      {period && (
        <>
          <Separator />
          <Link
            to={periodUrl}
            className="rounded px-1 py-0.5 hover:bg-ice-50 hover:text-navy dark:hover:bg-navy-600"
            data-rail-segment="period"
          >
            {period}
          </Link>
        </>
      )}

      {tier && (
        <>
          <Separator />
          <span
            className="rounded px-1 py-0.5 font-semibold text-navy dark:text-navy-50"
            aria-current="page"
            data-rail-segment="tier"
          >
            {tier}
          </span>
        </>
      )}
    </nav>
  );
}

function Separator() {
  return <ChevronRight className="size-3 text-navy/40" aria-hidden="true" />;
}

type ProgrammeSegmentProps = {
  label: string;
  code: string;
  drillUpHref: string;
  searchParams: URLSearchParams;
  pathname: string;
};

function ProgrammeSegment({
  label,
  drillUpHref,
  searchParams,
  pathname,
}: ProgrammeSegmentProps) {
  const [open, setOpen] = useState(false);
  const programmesQuery = useProgrammes();
  const ref = useOutsideClick(() => setOpen(false));

  return (
    <span ref={ref} className="relative inline-flex items-center">
      <Link
        to={drillUpHref}
        className="rounded px-1 py-0.5 font-semibold text-navy hover:bg-ice-50 dark:text-navy-50 dark:hover:bg-navy-600"
        data-rail-segment="programme"
      >
        {label}
      </Link>
      <button
        type="button"
        className="ml-0.5 rounded p-0.5 text-navy/60 hover:bg-ice-50 hover:text-navy dark:hover:bg-navy-600"
        aria-label="Switch programme"
        data-rail-segment-toggle="programme"
        onClick={() => setOpen((v) => !v)}
      >
        <ChevronDown className="size-3" aria-hidden="true" />
      </button>
      {open && (
        <div
          role="menu"
          aria-label="Programmes"
          className="absolute left-0 top-full z-20 mt-1 max-h-80 w-52 overflow-y-auto rounded border border-ice-100 bg-white p-1 text-sm shadow-lg dark:border-navy-500 dark:bg-navy-700"
        >
          {(programmesQuery.data ?? []).map((p) => {
            const next = new URLSearchParams(searchParams);
            next.set("programme", p.code);
            const href = `${pathname}?${next.toString()}`;
            return (
              <Link
                key={p.code}
                to={href}
                role="menuitem"
                className="block rounded px-2 py-1 text-navy hover:bg-ice-50 dark:text-navy-50 dark:hover:bg-navy-600"
                onClick={() => setOpen(false)}
              >
                <span className="font-medium">{p.name}</span>
                <span className="ml-2 font-mono text-xs text-navy/60 dark:text-navy-100/60">
                  {p.code}
                </span>
              </Link>
            );
          })}
        </div>
      )}
    </span>
  );
}

type MetricSegmentProps = {
  label: string;
  value: string;
  options?: MetricOption[];
  drillUpHref: string;
  searchParams: URLSearchParams;
  pathname: string;
};

function MetricSegment({
  label,
  options,
  drillUpHref,
  searchParams,
  pathname,
}: MetricSegmentProps) {
  const [open, setOpen] = useState(false);
  const ref = useOutsideClick(() => setOpen(false));
  const hasSwitcher = (options?.length ?? 0) > 0;

  return (
    <span ref={ref} className="relative inline-flex items-center">
      <Link
        to={drillUpHref}
        className="rounded px-1 py-0.5 font-semibold text-navy hover:bg-ice-50 dark:text-navy-50 dark:hover:bg-navy-600"
        data-rail-segment="metric"
      >
        {label}
      </Link>
      {hasSwitcher && (
        <button
          type="button"
          className="ml-0.5 rounded p-0.5 text-navy/60 hover:bg-ice-50 hover:text-navy dark:hover:bg-navy-600"
          aria-label="Switch metric"
          data-rail-segment-toggle="metric"
          onClick={() => setOpen((v) => !v)}
        >
          <ChevronDown className="size-3" aria-hidden="true" />
        </button>
      )}
      {open && options && (
        <div
          role="menu"
          aria-label="Metrics"
          className="absolute left-0 top-full z-20 mt-1 max-h-80 w-56 overflow-y-auto rounded border border-ice-100 bg-white p-1 text-sm shadow-lg dark:border-navy-500 dark:bg-navy-700"
        >
          {options.map((opt) => {
            const next = new URLSearchParams(searchParams);
            next.set("metric", opt.value);
            const href = `${pathname}?${next.toString()}`;
            return (
              <Link
                key={opt.value}
                to={href}
                role="menuitem"
                className="block rounded px-2 py-1 text-navy hover:bg-ice-50 dark:text-navy-50 dark:hover:bg-navy-600"
                onClick={() => setOpen(false)}
              >
                {opt.label}
              </Link>
            );
          })}
        </div>
      )}
    </span>
  );
}

function useOutsideClick(handler: () => void) {
  const ref = useRef<HTMLSpanElement | null>(null);
  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (!ref.current) return;
      if (ref.current.contains(e.target as Node)) return;
      handler();
    }
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [handler]);
  return ref;
}

// Re-export for tests.
export { TABS };
