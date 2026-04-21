import { useMemo, useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ChevronLeft, ChevronRight, Home, Layers, X } from "lucide-react";
import { Link } from "react-router-dom";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Breadcrumb } from "@/components/Breadcrumb";
import {
  fetchEvm,
  fetchProjectsForProgramme,
  type ProjectListItem,
} from "@/lib/api";
import { useProgrammes } from "@/hooks/usePortfolio";
import { formatRatio } from "@/lib/format";
import { EvmStrip } from "@/pages/delivery/EvmStrip";
import { ScrumView } from "@/pages/delivery/ScrumView";
import { KanbanView } from "@/pages/delivery/KanbanView";
import { WaterfallView } from "@/pages/delivery/WaterfallView";

const METHODOLOGY_TONE: Record<string, "green" | "amber" | "red" | "neutral"> = {
  Scrum: "neutral",
  Kanban: "neutral",
  Waterfall: "neutral",
  SAFe: "neutral",
  Hybrid: "neutral",
};

export function DeliveryHealth() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const programmeFilter = searchParams.get("programme");
  const programmes = useProgrammes();
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);

  const allProjectsQuery = useQuery({
    queryKey: ["projects", "all", (programmes.data ?? []).map((p) => p.id).join(",")],
    queryFn: async () => {
      if (!programmes.data) return [] as ProjectListItem[];
      const lists = await Promise.all(
        programmes.data.map((p) => fetchProjectsForProgramme(p.id)),
      );
      return lists.flat();
    },
    enabled: (programmes.data?.length ?? 0) > 0,
  });

  const allProjects = useMemo(
    () => allProjectsQuery.data ?? [],
    [allProjectsQuery.data],
  );

  // If ?programme=CODE is present, narrow the visible projects to that programme.
  const filteredProgramme = useMemo(() => {
    if (!programmeFilter) return null;
    return programmes.data?.find((p) => p.code === programmeFilter) ?? null;
  }, [programmeFilter, programmes.data]);

  const projects = useMemo(() => {
    if (!filteredProgramme) return allProjects;
    return allProjects.filter((p) => p.program_id === filteredProgramme.id);
  }, [allProjects, filteredProgramme]);

  const selected = useMemo(
    () => projects.find((p) => p.id === selectedProjectId) ?? null,
    [projects, selectedProjectId],
  );

  // When the visible-project list changes (filter applied/removed), make sure
  // we pick a project that's actually in it.
  useEffect(() => {
    if (projects.length === 0) return;
    if (!projects.some((p) => p.id === selectedProjectId)) {
      setSelectedProjectId(projects[0].id);
    }
  }, [projects, selectedProjectId]);

  const clearProgrammeFilter = () => {
    const next = new URLSearchParams(searchParams);
    next.delete("programme");
    setSearchParams(next);
  };

  const programmeByProject = useMemo(() => {
    const map = new Map<number, string>();
    for (const p of programmes.data ?? []) {
      map.set(p.id, p.currency_code);
    }
    return map;
  }, [programmes.data]);

  const evm = useQuery({
    queryKey: ["evm", selected?.id ?? null],
    queryFn: () => (selected ? fetchEvm(selected.id) : Promise.resolve([])),
    enabled: selected !== null,
  });

  const sourceCurrency =
    (selected && selected.program_id && programmeByProject.get(selected.program_id)) ||
    "USD";

  const evmTrend = useMemo(() => {
    const rows = evm.data ?? [];
    return rows.map((r) => ({
      month: r.snapshot_date.slice(0, 7),
      monthLabel: shortMonth(r.snapshot_date),
      cpi: r.cpi,
      spi: r.spi,
    }));
  }, [evm.data]);

  if (programmes.isLoading || allProjectsQuery.isLoading) {
    return <p className="text-sm text-navy/70">Loading projects…</p>;
  }

  if (projects.length === 0) {
    return (
      <Card>
        <CardHeader title="No projects yet" />
        <p className="text-sm text-navy/70">
          Seed the NovaTech demo or import <code>projects.csv</code> to see
          Delivery Health.
        </p>
      </Card>
    );
  }

  const selectedProgrammeCode =
    (selected && programmes.data?.find((p) => p.id === selected.program_id)?.code) ||
    filteredProgramme?.code ||
    null;

  // Drill-across helpers: prev/next project, wrapping at both ends.
  const selectedIdx = selected
    ? projects.findIndex((p) => p.id === selected.id)
    : -1;
  const prevProject =
    selectedIdx > 0
      ? projects[selectedIdx - 1]
      : projects.length > 0
        ? projects[projects.length - 1]
        : null;
  const nextProject =
    selectedIdx >= 0 && selectedIdx < projects.length - 1
      ? projects[selectedIdx + 1]
      : projects.length > 0
        ? projects[0]
        : null;

  const breadcrumbItems = [
    { label: "Portfolio", to: "/", icon: <Home className="size-3" aria-hidden="true" /> },
    { label: "Delivery Health", to: filteredProgramme ? "/delivery" : undefined },
    ...(filteredProgramme
      ? [
          {
            label: filteredProgramme.name,
            to: selected ? `/delivery?programme=${filteredProgramme.code}` : undefined,
          },
        ]
      : []),
    ...(selected ? [{ label: selected.code }] : []),
  ];

  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={breadcrumbItems} />
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-navy">Delivery Health</h1>
          <p className="mt-1 text-sm text-navy/70">
            Methodology-adaptive view. Pick a project below — the page reshapes
            to Scrum, Kanban or Waterfall based on the project's{" "}
            <code>delivery_methodology</code>.
          </p>
        </div>
        {selectedProgrammeCode ? (
          <Link
            to={`/kpi?programme=${selectedProgrammeCode}`}
            className="btn-ghost"
          >
            <Layers className="size-3" /> View KPIs for {selectedProgrammeCode}
          </Link>
        ) : null}
      </div>

      {filteredProgramme ? (
        <div className="inline-flex items-center gap-2 self-start rounded-full border border-navy/30 bg-navy/5 px-3 py-1 text-xs text-navy">
          Filtered to <strong>{filteredProgramme.name}</strong>
          <button
            type="button"
            onClick={clearProgrammeFilter}
            className="inline-flex items-center rounded-full bg-navy/10 px-1.5 py-0.5 transition hover:bg-navy/20"
            aria-label="Clear programme filter (drill up)"
          >
            <X className="size-3" /> clear
          </button>
        </div>
      ) : null}

      <Card>
        <CardHeader
          title="Project picker"
          subtitle={`${projects.length} ${filteredProgramme ? "matching" : ""} project${projects.length === 1 ? "" : "s"}`}
          action={
            projects.length > 1 && selected ? (
              <div className="flex items-center gap-1">
                <button
                  type="button"
                  onClick={() =>
                    prevProject && setSelectedProjectId(prevProject.id)
                  }
                  disabled={!prevProject}
                  className="btn-ghost px-2 py-1 text-xs"
                  aria-label="Previous project (drill across)"
                >
                  <ChevronLeft className="size-3" />
                </button>
                <button
                  type="button"
                  onClick={() =>
                    nextProject && setSelectedProjectId(nextProject.id)
                  }
                  disabled={!nextProject}
                  className="btn-ghost px-2 py-1 text-xs"
                  aria-label="Next project (drill across)"
                >
                  <ChevronRight className="size-3" />
                </button>
              </div>
            ) : null
          }
        />
        <div className="flex flex-wrap gap-2">
          {projects.map((p) => {
            const isActive = p.id === selectedProjectId;
            return (
              <button
                key={p.id}
                type="button"
                onClick={() => setSelectedProjectId(p.id)}
                className={`rounded-md border px-3 py-2 text-left text-sm transition ${
                  isActive
                    ? "border-navy bg-navy text-white"
                    : "border-ice-100 bg-white text-navy hover:bg-ice-50"
                }`}
              >
                <div className="font-medium">{p.code}</div>
                <div className="mt-0.5 flex items-center gap-2 text-xs">
                  <Badge tone={METHODOLOGY_TONE[p.delivery_methodology] ?? "neutral"}>
                    {p.delivery_methodology}
                  </Badge>
                  {p.is_ai_augmented ? (
                    <span className="text-amber-500">AI</span>
                  ) : null}
                </div>
              </button>
            );
          })}
        </div>
      </Card>

      {selected ? (
        <>
          <Card>
            <CardHeader
              title={selected.name}
              subtitle={`Programme ${programmes.data?.find((p) => p.id === selected.program_id)?.code ?? "—"} · ${selected.delivery_methodology}`}
              action={<Badge tone="neutral">{selected.status}</Badge>}
            />
            <EvmStrip
              evm={evm.data ?? []}
              project={selected}
              sourceCurrency={sourceCurrency}
            />
          </Card>

          <Card>
            <CardHeader
              title="EVM trend"
              subtitle="Click any data point to drill into Margin & EVM for this programme"
            />
            <div className="h-72">
              {evmTrend.length === 0 ? (
                <p className="grid h-full place-items-center text-sm text-navy/70">
                  No EVM snapshots for this project yet.
                </p>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={evmTrend}
                    margin={{ top: 8, right: 24, left: 0, bottom: 8 }}
                    onClick={() => {
                      const prog = programmeFilter;
                      navigate(prog ? `/margin?programme=${prog}` : "/margin");
                    }}
                    style={{ cursor: "pointer" }}
                  >
                    <CartesianGrid stroke="#E4EEF4" strokeDasharray="4 4" />
                    <XAxis dataKey="monthLabel" stroke="#1B2A4A" tick={{ fontSize: 12 }} />
                    <YAxis
                      stroke="#1B2A4A"
                      tick={{ fontSize: 12 }}
                      tickFormatter={(v) => formatRatio(Number(v))}
                    />
                    <Tooltip
                      formatter={(v: number) => formatRatio(v)}
                      contentStyle={{ border: "1px solid #D5E8F0" }}
                    />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                    <Line
                      type="monotone"
                      dataKey="cpi"
                      name="CPI"
                      stroke="#1B2A4A"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 6, style: { cursor: "pointer" } }}
                    />
                    <Line
                      type="monotone"
                      dataKey="spi"
                      name="SPI"
                      stroke="#F59E0B"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 6, style: { cursor: "pointer" } }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>
          </Card>

          {selected.delivery_methodology === "Scrum" ? (
            <ScrumView project={selected} />
          ) : selected.delivery_methodology === "Kanban" ? (
            <KanbanView project={selected} />
          ) : selected.delivery_methodology === "Waterfall" ? (
            <WaterfallView project={selected} />
          ) : (
            <Card>
              <p className="text-sm text-navy/70">
                {selected.delivery_methodology} view is scheduled for a future
                iteration. Scrum, Kanban and Waterfall views are live today.
              </p>
            </Card>
          )}
        </>
      ) : null}
    </div>
  );
}

function shortMonth(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { month: "short", year: "2-digit" });
}
