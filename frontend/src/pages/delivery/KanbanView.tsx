import { Fragment } from "react";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useRef, useState, useCallback } from "react";
import ReactECharts from "echarts-for-react";
import { Eye, EyeOff, X } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/ui/MetricCard";
import { fetchFlow, fetchBacklogItems, type ProjectListItem, type BacklogItem } from "@/lib/api";

// ─── types ───────────────────────────────────────────────────────────────────

type FlowRow = {
  period_start: string | null;
  throughput_items: number | null;
  wip_avg: number | null;
  wip_limit: number | null;
  cycle_time_p50: number | null;
  cycle_time_p85: number | null;
  cycle_time_p95: number | null;
  lead_time_avg: number | null;
  blocked_time_hours: number | null;
};

type MetricKey = "throughput" | "wip" | "cycle_p50" | "cycle_p85" | "cycle_p95" | "lead_time" | "blocked";
type ItemFilter = "all" | "completed" | "in_progress";

// ─── formula definitions ─────────────────────────────────────────────────────

const FORMULAS: Record<MetricKey, { title: string; formula: string; note: string; filter: ItemFilter; dataNote?: string }> = {
  throughput: {
    title: "Throughput",
    formula: "COUNT(items WHERE status = 'completed' AND week = N)",
    note: "Items that crossed the Done boundary in this period. Higher is better. Trend matters more than absolute value — compare week-on-week.",
    filter: "completed",
  },
  wip: {
    title: "WIP avg vs limit",
    formula: "AVG(daily in-flight count during week) / WIP_LIMIT (policy)",
    note: "Average number of items simultaneously in progress. When WIP avg > WIP limit the team is over-capacity — expect cycle time to degrade. Little's Law: Throughput = WIP / Cycle Time.",
    filter: "in_progress",
  },
  cycle_p50: {
    title: "Cycle time p50",
    formula: "PERCENTILE(50, done_date − first_in_progress_date) for items completed this week",
    note: "Median cycle time. Half of items finished faster than this. Use as your primary predictability gauge — a stable p50 means the process is controlled.",
    filter: "completed",
  },
  cycle_p85: {
    title: "Cycle time p85",
    formula: "PERCENTILE(85, cycle_days) — 85% of items complete within this many days",
    note: "SLA commitment benchmark. If a stakeholder asks 'how long will this take?', p85 is the safe answer. Rising p85 ÷ p50 ratio signals outlier accumulation.",
    filter: "completed",
  },
  cycle_p95: {
    title: "Cycle time p95",
    formula: "PERCENTILE(95, cycle_days) — tail latency indicator",
    note: "Flags the slowest 5% of items (bugs, blocked work, scope creep). When p95 > 3× p50, investigate age of oldest WIP items — they are dragging the tail.",
    filter: "completed",
  },
  lead_time: {
    title: "Lead time avg",
    formula: "AVG(done_date − request_date) including queue time before pick-up",
    note: "Total elapsed time from request to delivery — includes waiting in backlog. Lead time > Cycle time by the backlog queue. Reduce lead time by limiting WIP and prioritising ruthlessly.",
    filter: "all",
  },
  blocked: {
    title: "Blocked time",
    formula: "Σ hours items were blocked by dependencies, missing inputs or impediments",
    note: "Aggregate impediment cost. Each blocked hour = lost throughput capacity. Track which impediment types recur — systemic blockers need process fixes, not just unblocking.",
    filter: "in_progress",
    dataNote: "Blocked time is stored as a weekly aggregate — per-item blocker attribution isn't captured in backlog_items today, so the list below shows in-progress items as the nearest proxy. Row-level rework_hours won't sum to the card value.",
  },
};

// ─── KanbanView ──────────────────────────────────────────────────────────────

export function KanbanView({ project }: { project: ProjectListItem }) {
  const [selectedWeekIdx, setSelectedWeekIdx] = useState<number | null>(null);
  // seriesName captured from chart click — maps to a pre-filter in the drill panel
  const [clickedSeries, setClickedSeries] = useState<string | null>(null);
  // topCardMetric captured from summary-row clicks — pre-selects the metric cell
  // inside the drill panel and applies its formula filter to the L5 list.
  const [topCardMetric, setTopCardMetric] = useState<MetricKey | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ["flow", project.id],
    queryFn: () => fetchFlow(project.id),
  });

  const sorted = useMemo(() => {
    if (!data) return [];
    return data.slice().sort((a, b) =>
      (a.period_start ?? "").localeCompare(b.period_start ?? ""),
    );
  }, [data]);

  // Keep a ref so ZRender callbacks don't get stale closures
  const sortedRef = useRef(sorted);
  sortedRef.current = sorted;

  // Build chart options
  const cfdOption = useMemo(() => buildCfdOption(sorted), [sorted]);
  const cycleOption = useMemo(() => buildCyclePercentileOption(sorted), [sorted]);

  // ── ECharts `onEvents` handler — fires for clicks on data-point markers ──
  const chartEvents = useMemo(
    () => ({
      click: (params: { dataIndex?: number; seriesName?: string }) => {
        const idx = params.dataIndex ?? null;
        if (idx === null) return;
        setClickedSeries(params.seriesName ?? null);
        setTopCardMetric(null); // chart click overrides any top-card selection
        setSelectedWeekIdx((prev) => (prev === idx ? null : idx));
      },
    }),
    [],
  );

  // ── ZRender raw-canvas click — fires anywhere on the chart ──
  const makeCfdReady = useCallback(
    (instance: any) => {
      instance.getZr().on("click", (e: { offsetX: number; offsetY: number }) => {
        const point = instance.convertFromPixel({ gridIndex: 0 }, [e.offsetX, e.offsetY]);
        if (!Array.isArray(point) || point.length < 1) return;
        const dataIdx = Math.round(point[0]);
        const len = sortedRef.current.length;
        if (len === 0) return;
        const clamped = Math.max(0, Math.min(dataIdx, len - 1));
        setClickedSeries(null); // area click — no specific series
        setTopCardMetric(null);
        setSelectedWeekIdx((prev) => (prev === clamped ? null : clamped));
      });
    },
    [],
  );

  const makeCycleReady = useCallback(
    (instance: any) => {
      instance.getZr().on("click", (e: { offsetX: number; offsetY: number }) => {
        const point = instance.convertFromPixel({ gridIndex: 0 }, [e.offsetX, e.offsetY]);
        if (!Array.isArray(point) || point.length < 1) return;
        const dataIdx = Math.round(point[0]);
        const len = sortedRef.current.length;
        if (len === 0) return;
        const clamped = Math.max(0, Math.min(dataIdx, len - 1));
        setTopCardMetric(null);
        setSelectedWeekIdx((prev) => (prev === clamped ? null : clamped));
      });
    },
    [],
  );

  // Click handler for summary-row MetricCards: opens the latest-week drill
  // panel with the clicked metric's formula filter pre-applied.
  const openLatestWithMetric = (metric: MetricKey) => {
    setTopCardMetric(metric);
    setClickedSeries(null);
    setSelectedWeekIdx(sorted.length - 1);
  };

  const selectedWeek = selectedWeekIdx !== null ? sorted[selectedWeekIdx] ?? null : null;
  const selectedWeekNumber = selectedWeekIdx !== null ? selectedWeekIdx + 1 : null;

  // Derive initial filter — top-card click wins over CFD-band click.
  const topCardFilter: ItemFilter | null = topCardMetric ? FORMULAS[topCardMetric].filter : null;
  const initialFilter: ItemFilter =
    topCardFilter ?? (
      clickedSeries === "Done (cumulative)"
        ? "completed"
        : clickedSeries === "In Progress"
          ? "in_progress"
          : "all"
    );
  const cycleInitialFilter: ItemFilter = topCardFilter ?? "all";

  if (isLoading) return <p className="text-sm text-navy/70">Loading flow metrics…</p>;
  if (error) return <p className="text-sm text-danger-600">{(error as Error).message}</p>;
  if (sorted.length === 0)
    return <p className="text-sm text-navy/70">No flow metrics seeded for this project.</p>;

  const latest = sorted[sorted.length - 1];
  const avgThroughput =
    sorted.reduce((sum, r) => sum + (r.throughput_items ?? 0), 0) / sorted.length;
  const wipBreach =
    latest.wip_avg !== null &&
    latest.wip_limit !== null &&
    latest.wip_avg > latest.wip_limit;

  return (
    <div className="flex flex-col gap-4">
      {/* ── Summary row — click to open latest week drill panel, pre-filtered to the clicked metric ── */}
      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <MetricCard metricId="throughput" value={`${latest.throughput_items ?? 0}`} sub={`avg ${avgThroughput.toFixed(1)}`} drillFilter="completed" onClick={() => openLatestWithMetric("throughput")} />
        <MetricCard metricId="wip" value={`${(latest.wip_avg ?? 0).toFixed(1)}`} sub={`limit ${latest.wip_limit ?? "—"}`} tone={wipBreach ? "red" : "green"} drillFilter="in_progress" onClick={() => openLatestWithMetric("wip")} />
        <MetricCard metricId="cycle_p50" value={`${(latest.cycle_time_p50 ?? 0).toFixed(1)}d`} sub={`p95 ${(latest.cycle_time_p95 ?? 0).toFixed(1)}d`} drillFilter="completed" onClick={() => openLatestWithMetric("cycle_p50")} />
        <MetricCard metricId="blocked" value={`${(latest.blocked_time_hours ?? 0).toFixed(1)}h`} tone={(latest.blocked_time_hours ?? 0) > 8 ? "red" : (latest.blocked_time_hours ?? 0) > 4 ? "amber" : "green"} drillFilter="in_progress" onClick={() => openLatestWithMetric("blocked")} />
      </section>

      {/* ── CFD ── */}
      <Card>
        <CardHeader
          title="Cumulative flow diagram"
          subtitle="Click anywhere on the chart to drill into that week — click a coloured band to pre-filter work items"
        />
        <div className="h-80 cursor-pointer">
          <ReactECharts
            option={cfdOption}
            style={{ height: "100%", width: "100%" }}
            notMerge
            onEvents={chartEvents}
            onChartReady={makeCfdReady}
          />
        </div>
        {selectedWeek && selectedWeekNumber !== null && (
          <FlowDrillPanel
            row={selectedWeek}
            projectId={project.id}
            weekNumber={selectedWeekNumber}
            initialFilter={initialFilter}
            initialMetric={topCardMetric}
            onClose={() => { setSelectedWeekIdx(null); setClickedSeries(null); setTopCardMetric(null); }}
          />
        )}
        <p className="mt-2 text-xs text-navy/70">
          CFD = stacked Backlog + In Progress + Done. Widening In-Progress band → WIP
          exceeding limit. Flattening Done slope → throughput degrading.
        </p>
      </Card>

      {/* ── Cycle Time ── */}
      <Card>
        <CardHeader
          title="Cycle-time percentiles"
          subtitle="p50 · p85 · p95 per week (days) — click any point or line to open week detail"
        />
        <div className="h-72 cursor-pointer">
          <ReactECharts
            option={cycleOption}
            style={{ height: "100%", width: "100%" }}
            notMerge
            onEvents={chartEvents}
            onChartReady={makeCycleReady}
          />
        </div>
        {selectedWeek && selectedWeekNumber !== null && (
          <FlowDrillPanel
            row={selectedWeek}
            projectId={project.id}
            weekNumber={selectedWeekNumber}
            initialFilter={cycleInitialFilter}
            initialMetric={topCardMetric}
            onClose={() => { setSelectedWeekIdx(null); setClickedSeries(null); setTopCardMetric(null); }}
          />
        )}
      </Card>
    </div>
  );
}

// ─── FlowDrillPanel ───────────────────────────────────────────────────────────

function FlowDrillPanel({
  row,
  projectId,
  weekNumber,
  initialFilter,
  initialMetric,
  onClose,
}: {
  row: FlowRow;
  projectId: number;
  weekNumber: number;
  initialFilter: ItemFilter;
  initialMetric?: MetricKey | null;
  onClose: () => void;
}) {
  const [activeMetric, setActiveMetric] = useState<MetricKey | null>(initialMetric ?? null);
  const [activeFilter, setActiveFilter] = useState<ItemFilter>(initialFilter);
  const [showFormula, setShowFormula] = useState(false);

  // When the parent pushes a new initialMetric (e.g. user clicks a different
  // summary-row card while the panel is still open), re-sync the active cell
  // and its filter so the panel reflects the new selection.
  useEffect(() => {
    if (initialMetric) {
      setActiveMetric(initialMetric);
      setActiveFilter(FORMULAS[initialMetric].filter);
      setShowFormula(false);
    }
  }, [initialMetric]);

  const { data: flowItems } = useQuery({
    queryKey: ["flow-items", projectId, weekNumber],
    queryFn: () => fetchBacklogItems(projectId, weekNumber),
  });

  const wipBreach = row.wip_avg !== null && row.wip_limit !== null && row.wip_avg > row.wip_limit;

  // Map metric → current value string and tone
  const metricDefs: Array<{ key: MetricKey; label: string; value: string; tone: "green" | "amber" | "red" | "neutral" }> = [
    {
      key: "throughput",
      label: "Throughput",
      value: `${row.throughput_items ?? 0} items`,
      tone: "neutral",
    },
    {
      key: "wip",
      label: "WIP avg / limit",
      value: `${(row.wip_avg ?? 0).toFixed(1)} / ${row.wip_limit ?? "—"}`,
      tone: wipBreach ? "red" : "green",
    },
    {
      key: "cycle_p50",
      label: "Cycle time p50",
      value: `${(row.cycle_time_p50 ?? 0).toFixed(1)}d`,
      tone: "neutral",
    },
    {
      key: "cycle_p85",
      label: "Cycle time p85",
      value: `${(row.cycle_time_p85 ?? 0).toFixed(1)}d`,
      tone: (row.cycle_time_p85 ?? 0) > (row.cycle_time_p50 ?? 0) * 2 ? "amber" : "neutral",
    },
    {
      key: "cycle_p95",
      label: "Cycle time p95",
      value: `${(row.cycle_time_p95 ?? 0).toFixed(1)}d`,
      tone: (row.cycle_time_p95 ?? 0) > (row.cycle_time_p50 ?? 0) * 3 ? "red" : "neutral",
    },
    {
      key: "lead_time",
      label: "Lead time avg",
      value: `${(row.lead_time_avg ?? 0).toFixed(1)}d`,
      tone: "neutral",
    },
    {
      key: "blocked",
      label: "Blocked time",
      value: `${(row.blocked_time_hours ?? 0).toFixed(1)}h`,
      tone: (row.blocked_time_hours ?? 0) > 8 ? "red" : (row.blocked_time_hours ?? 0) > 4 ? "amber" : "green",
    },
  ];

  const handleMetricClick = (key: MetricKey) => {
    if (activeMetric === key) {
      // Toggle off
      setActiveMetric(null);
      setShowFormula(false);
      setActiveFilter("all");
    } else {
      setActiveMetric(key);
      setShowFormula(false);
      setActiveFilter(FORMULAS[key].filter);
    }
  };

  const toggleFormula = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowFormula((v) => !v);
  };

  // Compute CFD band breakdown from L5 items
  const doneCount = flowItems?.filter((i) => i.status === "completed" || i.status === "added").length ?? 0;
  const wipCount = flowItems?.filter((i) => i.status === "in_progress").length ?? 0;
  const totalItems = flowItems?.length ?? 0;

  const filteredItems = useMemo(() => {
    if (!flowItems) return [];
    if (activeFilter === "completed") return flowItems.filter((i) => i.status === "completed" || i.status === "added");
    if (activeFilter === "in_progress") return flowItems.filter((i) => i.status === "in_progress");
    return flowItems;
  }, [flowItems, activeFilter]);

  return (
    <div className="mt-3 rounded-lg border border-navy/20 bg-navy/[0.03] p-4">
      {/* ── Header ── */}
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-semibold text-navy">
            Week {weekNumber} · {row.period_start?.slice(0, 10) ?? "—"}
          </p>
          <p className="text-xs text-navy/60 mt-0.5">
            L4 flow metrics — click any metric cell to filter L5 items ↓ · 👁 shows the formula
          </p>
          {totalItems > 0 && (
            <div className="mt-1 flex gap-3 text-xs">
              <span className="text-emerald-600 font-medium">✓ {doneCount} done</span>
              <span className="text-amber-600 font-medium">⟳ {wipCount} in progress</span>
              <span className="text-navy/50">{totalItems} total this week</span>
            </div>
          )}
        </div>
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1 hover:bg-ice-100"
          aria-label="Close"
        >
          <X className="size-3.5 text-navy/60" />
        </button>
      </div>

      {/* ── Metric cells ── */}
      <div className="mt-3 grid grid-cols-2 gap-2 md:grid-cols-4">
        {metricDefs.map(({ key, label, value, tone }) => (
          <MetricCell
            key={key}
            label={label}
            value={value}
            tone={tone}
            active={activeMetric === key}
            formulaVisible={activeMetric === key && showFormula}
            onClick={() => handleMetricClick(key)}
            onFormulaToggle={toggleFormula}
          />
        ))}
      </div>

      {/* ── Inline formula panel ── */}
      {activeMetric && (
        <div className="mt-3 rounded border border-navy/10 bg-white p-3">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-navy">
              {FORMULAS[activeMetric].title} — calculation
            </p>
            <button
              type="button"
              onClick={toggleFormula}
              className="text-navy/40 hover:text-navy/70"
              aria-label={showFormula ? "Hide formula" : "Show formula"}
            >
              {showFormula ? <EyeOff className="size-3.5" /> : <Eye className="size-3.5" />}
            </button>
          </div>

          {showFormula ? (
            <>
              <code className="mt-1 block text-xs text-[#1B2A4A] bg-ice-50 rounded px-2 py-1 font-mono">
                {FORMULAS[activeMetric].formula}
              </code>
              <p className="mt-2 text-xs text-navy/70 leading-relaxed">
                {FORMULAS[activeMetric].note}
              </p>
            </>
          ) : (
            <p className="mt-1 text-xs text-navy/60">
              Filtering L5 items to:{" "}
              <strong>
                {activeFilter === "all" ? "all items" : activeFilter === "completed" ? "completed items" : "in-progress items"}
              </strong>
              {" "}· Click 👁 to see the formula
            </p>
          )}
          {FORMULAS[activeMetric].dataNote ? (
            <div className="mt-2 rounded border border-amber-200 bg-amber-50 px-2 py-1.5 text-[11px] leading-relaxed text-amber-900">
              <strong className="uppercase tracking-wide text-amber-800">Data note · </strong>
              {FORMULAS[activeMetric].dataNote}
            </div>
          ) : null}
        </div>
      )}

      {/* ── L5 items table ── */}
      {flowItems && flowItems.length > 0 ? (
        <FlowItemsTable
          items={filteredItems}
          allCount={flowItems.length}
          activeFilter={activeFilter}
          activeMetric={activeMetric}
        />
      ) : (
        <p className="mt-4 text-xs text-navy/40">
          No work items seeded for week {weekNumber}. Upload backlog_items.csv with
          sprint_number={weekNumber} to enable L5 drill.
        </p>
      )}
    </div>
  );
}

// ─── MetricCell ───────────────────────────────────────────────────────────────

function MetricCell({
  label,
  value,
  tone,
  active,
  formulaVisible,
  onClick,
  onFormulaToggle,
}: {
  label: string;
  value: string;
  tone: "green" | "amber" | "red" | "neutral";
  active: boolean;
  formulaVisible: boolean;
  onClick: () => void;
  onFormulaToggle: (e: React.MouseEvent) => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={[
        "group relative flex flex-col gap-1 rounded border p-2 text-left transition-all",
        active
          ? "border-[#1B2A4A] bg-white ring-2 ring-[#1B2A4A]/20"
          : "border-ice-100 bg-white hover:border-navy/30 hover:shadow-sm",
      ].join(" ")}
      aria-pressed={active}
    >
      <div className="flex items-center justify-between gap-1">
        <span className="kpi-label text-[10px]">{label}</span>
        <span
          role="button"
          tabIndex={-1}
          onClick={onFormulaToggle}
          className="opacity-0 group-hover:opacity-100 transition-opacity"
          title="Show formula"
          aria-label="Toggle formula"
        >
          {formulaVisible ? (
            <EyeOff className="size-2.5 text-navy/50" />
          ) : (
            <Eye className="size-2.5 text-navy/40" />
          )}
        </span>
      </div>
      <Badge tone={tone}>{value}</Badge>
      {active && (
        <span className="absolute bottom-1 right-1.5 text-[9px] font-semibold text-navy/40 uppercase tracking-wide">
          active
        </span>
      )}
    </button>
  );
}

// ─── L5 Flow items table ──────────────────────────────────────────────────────

const FLOW_STATUS_TONE: Record<string, "green" | "amber" | "red" | "neutral"> = {
  completed: "green",
  added: "green",
  in_progress: "amber",
  carried_over: "amber",
  planned: "neutral",
};

const FLOW_TYPE_TONE: Record<string, "green" | "amber" | "red" | "neutral"> = {
  bug: "red",
  spike: "amber",
  story: "neutral",
  task: "neutral",
};

function FlowItemsTable({
  items,
  allCount,
  activeFilter,
  activeMetric,
}: {
  items: BacklogItem[];
  allCount: number;
  activeFilter: ItemFilter;
  activeMetric: MetricKey | null;
}) {
  const [expandedItem, setExpandedItem] = useState<number | null>(null);
  const totalPoints = items.reduce((s, i) => s + (i.story_points ?? 0), 0);
  const aiCount = items.filter((i) => i.is_ai_assisted).length;

  const filterLabel =
    activeFilter === "completed"
      ? "completed items"
      : activeFilter === "in_progress"
        ? "in-progress items"
        : "all items";

  return (
    <div className="mt-4 border-t border-navy/10 pt-3">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs font-semibold text-navy">
          Level 5 work items
          {activeMetric ? (
            <span className="ml-1 font-normal text-navy/60">
              · {filterLabel} ({items.length} of {allCount})
            </span>
          ) : (
            <span className="ml-1 font-normal text-navy/60">· {items.length} items</span>
          )}
        </p>
        <div className="flex gap-3 text-xs text-navy/60">
          <span>{totalPoints} pts total</span>
          {aiCount > 0 && (
            <span className="text-[#7C3AED] font-medium">{aiCount} AI-assisted</span>
          )}
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-navy/10 text-left text-navy/50">
              <th className="pb-1 pr-3 font-medium">Type</th>
              <th className="pb-1 pr-3 font-medium">Title</th>
              <th className="pb-1 pr-3 font-medium">Pts</th>
              <th className="pb-1 pr-3 font-medium">Assignee</th>
              <th className="pb-1 pr-3 font-medium">Status</th>
              <th className="pb-1 pr-3 font-medium">AI</th>
              <th className="pb-1 pr-3 font-medium">Defects</th>
              <th className="pb-1 font-medium">Priority</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <Fragment key={item.id}>
                <tr
                  role="button"
                  tabIndex={0}
                  className="border-b border-navy/5 hover:bg-ice-50 cursor-pointer"
                  onClick={() => setExpandedItem(expandedItem === item.id ? null : item.id)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setExpandedItem(expandedItem === item.id ? null : item.id);
                    }
                  }}
                >
                  <td className="py-1 pr-3">
                    <Badge tone={FLOW_TYPE_TONE[item.item_type] ?? "neutral"}>
                      {item.item_type}
                    </Badge>
                  </td>
                  <td className={`py-1 pr-3 font-medium text-navy${expandedItem === item.id ? "" : " max-w-[260px] truncate"}`}>
                    {item.title}
                  </td>
                  <td className="py-1 pr-3 font-mono text-navy">{item.story_points ?? "—"}</td>
                  <td className="py-1 pr-3 text-navy/70">{item.assignee ?? "—"}</td>
                  <td className="py-1 pr-3">
                    <Badge tone={FLOW_STATUS_TONE[item.status] ?? "neutral"}>
                      {item.status.replace("_", " ")}
                    </Badge>
                  </td>
                  <td className="py-1 pr-3">
                    {item.is_ai_assisted ? (
                      <span className="font-semibold text-[#7C3AED]">AI</span>
                    ) : (
                      <span className="text-navy/30">—</span>
                    )}
                  </td>
                  <td className="py-1 pr-3 text-navy/70">{item.defects_raised}</td>
                  <td className="py-1 text-navy/70">{item.priority ?? "—"}</td>
                </tr>
                {expandedItem === item.id ? (
                  <tr key={`${item.id}-expand`} className="bg-ice-50/60">
                    <td colSpan={8} className="px-3 py-2">
                      <dl className="grid grid-cols-2 gap-2 md:grid-cols-4">
                        <div className="flex flex-col"><span className="kpi-label">Title</span><span className="font-medium text-navy">{item.title}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Assignee</span><span className="font-mono text-navy">{item.assignee ?? "—"}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Story points</span><span className="font-mono text-navy">{item.story_points ?? "—"}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Type</span><span className="font-mono text-navy">{item.item_type}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Status</span><span className="font-mono text-navy">{item.status.replace("_", " ")}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">AI-assisted</span><span className="font-mono text-navy">{item.is_ai_assisted ? "Yes" : "No"}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Defects raised</span><span className="font-mono text-navy">{item.defects_raised}</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Rework hours</span><span className="font-mono text-navy">{item.rework_hours.toFixed(1)}h</span></div>
                        <div className="flex flex-col"><span className="kpi-label">Priority</span><span className="font-mono text-navy">{item.priority ?? "—"}</span></div>
                        <div className="col-span-2 md:col-span-4 text-navy/50 italic mt-1">
                          L6: Item-level detail — cycle time, acceptance criteria, and commit history available in your source issue tracker.
                        </div>
                      </dl>
                    </td>
                  </tr>
                ) : null}
              </Fragment>
            ))}
          </tbody>
          <tfoot>
            <tr className="border-t border-navy/20 font-semibold text-navy">
              <td colSpan={2} className="pt-1 pr-3 text-navy/60">Totals</td>
              <td className="pt-1 pr-3 font-mono">{totalPoints}</td>
              <td colSpan={5} className="pt-1 text-navy/50 font-normal">
                {items.filter((i) => i.status === "completed" || i.status === "added").length} done ·{" "}
                {items.filter((i) => i.status === "in_progress").length} in progress
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
}

// ─── Chart option builders ────────────────────────────────────────────────────

function buildCfdOption(
  rows: { period_start: string | null; throughput_items: number | null; wip_avg: number | null }[],
) {
  const weeks = rows.map((r) => weekLabel(r.period_start));
  const doneRunning: number[] = [];
  let running = 0;
  for (const r of rows) {
    running += r.throughput_items ?? 0;
    doneRunning.push(running);
  }
  const inProgress = rows.map((r) => r.wip_avg ?? 0);
  const backlog = rows.map((_, i) => Math.max(5, inProgress[i] * 1.3 + i * 0.8));

  const sharedSeriesStyle = {
    type: "line",
    stack: "cfd",
    lineStyle: { width: 1.5 },
    // Small circles make the area hittable and show data points
    symbol: "circle",
    symbolSize: 5,
    emphasis: { symbolSize: 8, focus: "series" },
    smooth: false,
  };

  return {
    tooltip: {
      trigger: "axis",
      formatter: (params: any[]) => {
        const week = params[0]?.name ?? "";
        return params
          .map((p: any) => `${p.marker}${p.seriesName}: <b>${p.value}</b>`)
          .join("<br/>") + `<br/><span style="font-size:10px;color:#888">Week: ${week} · click to drill ↓</span>`;
      },
    },
    legend: { data: ["Done (cumulative)", "In Progress", "Backlog"], bottom: 0 },
    grid: { top: 20, right: 20, bottom: 40, left: 50 },
    xAxis: { type: "category", data: weeks, boundaryGap: false },
    yAxis: { type: "value", name: "Items" },
    series: [
      {
        ...sharedSeriesStyle,
        name: "Done (cumulative)",
        areaStyle: { color: "#10B981", opacity: 0.8 },
        itemStyle: { color: "#10B981" },
        lineStyle: { ...sharedSeriesStyle.lineStyle, color: "#059669" },
        data: doneRunning,
      },
      {
        ...sharedSeriesStyle,
        name: "In Progress",
        areaStyle: { color: "#F59E0B", opacity: 0.7 },
        itemStyle: { color: "#F59E0B" },
        lineStyle: { ...sharedSeriesStyle.lineStyle, color: "#D97706" },
        data: inProgress,
      },
      {
        ...sharedSeriesStyle,
        name: "Backlog",
        areaStyle: { color: "#1B2A4A", opacity: 0.15 },
        itemStyle: { color: "#1B2A4A", opacity: 0.4 },
        lineStyle: { ...sharedSeriesStyle.lineStyle, color: "#1B2A4A", opacity: 0.4 },
        data: backlog,
      },
    ],
  };
}

function buildCyclePercentileOption(
  rows: {
    period_start: string | null;
    cycle_time_p50: number | null;
    cycle_time_p85: number | null;
    cycle_time_p95: number | null;
  }[],
) {
  const weeks = rows.map((r) => weekLabel(r.period_start));
  const sharedStyle = {
    type: "line",
    smooth: true,
    symbolSize: 6,
    emphasis: { symbolSize: 10, focus: "series" },
  };
  return {
    tooltip: {
      trigger: "axis",
      formatter: (params: any[]) => {
        const week = params[0]?.name ?? "";
        return params
          .map((p: any) => `${p.marker}${p.seriesName}: <b>${p.value}d</b>`)
          .join("<br/>") + `<br/><span style="font-size:10px;color:#888">Week: ${week} · click to drill ↓</span>`;
      },
    },
    legend: { data: ["p50", "p85", "p95"], bottom: 0 },
    grid: { top: 20, right: 20, bottom: 40, left: 50 },
    xAxis: { type: "category", data: weeks },
    yAxis: { type: "value", name: "Days" },
    series: [
      {
        ...sharedStyle,
        name: "p50",
        lineStyle: { color: "#10B981", width: 2 },
        itemStyle: { color: "#10B981" },
        data: rows.map((r) => r.cycle_time_p50 ?? 0),
      },
      {
        ...sharedStyle,
        name: "p85",
        lineStyle: { color: "#F59E0B", width: 2 },
        itemStyle: { color: "#F59E0B" },
        data: rows.map((r) => r.cycle_time_p85 ?? 0),
      },
      {
        ...sharedStyle,
        name: "p95",
        lineStyle: { color: "#EF4444", width: 2 },
        itemStyle: { color: "#EF4444" },
        data: rows.map((r) => r.cycle_time_p95 ?? 0),
      },
    ],
  };
}

function weekLabel(iso: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short" });
}
