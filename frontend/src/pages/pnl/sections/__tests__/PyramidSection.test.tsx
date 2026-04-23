import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { PyramidSection } from "@/pages/pnl/sections/PyramidSection";
import * as pnlApi from "@/api/pnlApi";

vi.mock("recharts", async () => {
  const actual = await vi.importActual<typeof import("recharts")>("recharts");
  return {
    ...actual,
    ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
      <div style={{ width: 800, height: 300 }}>{children}</div>
    ),
  };
});

const LINEAGE: pnlApi.LineageBlock = {
  formula: "",
  formula_ref: null,
  entries: [],
  entries_total_count: 0,
  sampling: "full",
  sampling_rule: null,
};

const EMPTY_FILTERS: pnlApi.FiltersApplied = {
  programme: ["PHOENIX"],
  from: null,
  to: null,
  tier: null,
  scenario_name: null,
  portfolio: null,
  month: null,
};

const PHOENIX_PYRAMID: pnlApi.PyramidOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-12-01",
  tiers: [
    {
      role_tier: "Junior",
      planned_headcount: 7,
      actual_headcount: 7,
      planned_weight: 0.3,
      actual_weight: 1.4,
      planned_rate: 70,
      actual_rate: 81,
      utilisation_pct: null,
    },
    {
      role_tier: "Mid",
      planned_headcount: 15,
      actual_headcount: 14,
      planned_weight: 0.5,
      actual_weight: -0.435,
      planned_rate: 110,
      actual_rate: 154,
      utilisation_pct: null,
    },
    {
      role_tier: "Senior",
      planned_headcount: 3,
      actual_headcount: 4,
      planned_weight: 0.2,
      actual_weight: 0.035,
      planned_rate: 180,
      actual_rate: 152.5,
      utilisation_pct: 86,
    },
  ],
  realisation_rate_pct: 33.33,
  rag: "red",
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const PHOENIX_EVM: pnlApi.EvmOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-04-01",
  planned_value: 3_864_000,
  earned_value: 3_245_760,
  actual_cost: 3_730_758.62,
  percent_complete: 77.28,
  bac: 4_200_000,
  cpi: 0.87,
  spi: 0.84,
  eac: 4_827_586.21,
  tcpi: 2.0336,
  vac: -627_586.21,
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const PHOENIX_DSO: pnlApi.DsoOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-03-01",
  scenario_name: "Monthly Actuals",
  billed_revenue: 721_600,
  collected_revenue: 577_280,
  ar_balance: 144_320,
  unbilled_wip: 98_400,
  dso_days: 6.0,
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const PHOENIX_WATERFALL: pnlApi.WaterfallOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-03-01",
  scenario_name: "Monthly Actuals",
  revenue: 820_000,
  layers: [],
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const PHOENIX_PFA_CPI: pnlApi.PfaOut = {
  programme_code: "PHOENIX",
  metric: "cpi",
  series: {
    plan: [],
    forecast: [],
    actual: [
      { snapshot_date: "2025-11-01", value: 0.94 },
      { snapshot_date: "2025-12-01", value: 0.92 },
      { snapshot_date: "2026-01-01", value: 0.9 },
      { snapshot_date: "2026-02-01", value: 0.88 },
      { snapshot_date: "2026-03-01", value: 0.87 },
    ],
  },
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const PHOENIX_PFA_SPI: pnlApi.PfaOut = {
  ...PHOENIX_PFA_CPI,
  metric: "spi",
  series: {
    plan: [],
    forecast: [],
    actual: [
      { snapshot_date: "2025-11-01", value: 0.92 },
      { snapshot_date: "2025-12-01", value: 0.9 },
      { snapshot_date: "2026-01-01", value: 0.88 },
      { snapshot_date: "2026-02-01", value: 0.86 },
      { snapshot_date: "2026-03-01", value: 0.84 },
    ],
  },
};

function renderAt(url: string) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route path="*" element={<PyramidSection />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("PyramidSection", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts the user to pick a programme when ?programme= is absent", () => {
    const pyramid = vi.spyOn(pnlApi, "fetchPnlPyramid");
    const evm = vi.spyOn(pnlApi, "fetchPnlEvm");
    const dso = vi.spyOn(pnlApi, "fetchPnlDso");
    renderAt("/pnl");
    expect(
      screen.getByText(/Pick a programme to see the resource pyramid/i),
    ).toBeInTheDocument();
    expect(pyramid).not.toHaveBeenCalled();
    expect(evm).not.toHaveBeenCalled();
    expect(dso).not.toHaveBeenCalled();
  });

  it("shows independent loading state for pyramid while sub-cards are already populated", async () => {
    vi.spyOn(pnlApi, "fetchPnlPyramid").mockImplementation(
      () => new Promise(() => {}),
    );
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);
    vi.spyOn(pnlApi, "fetchPnlEvm").mockResolvedValue(PHOENIX_EVM);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);

    renderAt("/pnl?programme=PHOENIX");

    expect(screen.getByTestId("pyramid-loading")).toBeInTheDocument();
    // EVM and DSO sub-cards render independently.
    await waitFor(() =>
      expect(screen.getByTestId("evm-sub-card")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("dso-sub-card")).toBeInTheDocument();
  });

  it("surfaces an error banner on a sub-card without breaking the rest", async () => {
    vi.spyOn(pnlApi, "fetchPnlPyramid").mockResolvedValue(PHOENIX_PYRAMID);
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);

    const evmErr = new AxiosError(
      "Request failed",
      "ERR_BAD_REQUEST",
      undefined,
      null,
      {
        status: 500,
        data: {
          error: {
            code: "server_error",
            message: "evm_snapshots join failed",
            details: null,
          },
          filters_applied: null,
        },
        statusText: "Internal Server Error",
        headers: new AxiosHeaders(),
        config: { headers: new AxiosHeaders() } as never,
      },
    );
    vi.spyOn(pnlApi, "fetchPnlEvm").mockRejectedValue(evmErr);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("pyramid-block")).toBeInTheDocument(),
    );
    // EVM sub-card shows its own error banner.
    await waitFor(() =>
      expect(screen.getByText(/evm_snapshots join failed/)).toBeInTheDocument(),
    );
    // DSO still rendered.
    expect(screen.getByTestId("dso-sub-card")).toBeInTheDocument();
    expect(screen.getByTestId("dso-value")).toHaveTextContent("6.0 d");
  });

  it("renders the pyramid chart, EVM numbers + sparklines, and DSO values for Phoenix", async () => {
    vi.spyOn(pnlApi, "fetchPnlPyramid").mockResolvedValue(PHOENIX_PYRAMID);
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);
    vi.spyOn(pnlApi, "fetchPnlEvm").mockResolvedValue(PHOENIX_EVM);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockImplementation(async (_code, metric) =>
      metric === "cpi" ? PHOENIX_PFA_CPI : PHOENIX_PFA_SPI,
    );

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("pyramid-chart")).toBeInTheDocument(),
    );

    // Pyramid RAG chip carries red for the anomalous PHOENIX weights.
    const rag = screen.getByTestId("pyramid-rag");
    expect(rag).toHaveAttribute("data-rag-palette", "red");

    // Tier weight anomaly footnote renders because of the out-of-range weights.
    expect(screen.getByTestId("pyramid-chart-footnote")).toHaveTextContent(
      /Tier weight anomaly detected — see TECH_DEBT\.md/,
    );

    // EVM numbers present.
    const cpiBlock = screen.getByTestId("evm-cpi");
    expect(cpiBlock).toHaveTextContent("0.87");
    expect(cpiBlock).toHaveTextContent("CPI = EV / AC");
    // CPI palette = red (0.87 < 0.9).
    expect(
      cpiBlock.querySelector("[data-rag-palette]"),
    ).toHaveAttribute("data-rag-palette", "red");

    const spiBlock = screen.getByTestId("evm-spi");
    expect(spiBlock).toHaveTextContent("0.84");
    expect(spiBlock).toHaveTextContent("SPI = EV / PV");
    expect(
      spiBlock.querySelector("[data-rag-palette]"),
    ).toHaveAttribute("data-rag-palette", "red");

    // Sparkline containers present (data feeds from mocked /pfa).
    expect(screen.getByTestId("evm-cpi-sparkline")).toBeInTheDocument();
    expect(screen.getByTestId("evm-spi-sparkline")).toBeInTheDocument();

    // DSO numbers: 6.0 days green, AR 144.3 K, Unbilled 98.4 K.
    expect(screen.getByTestId("dso-value")).toHaveTextContent("6.0 d");
    expect(screen.getByTestId("dso-rag")).toHaveAttribute(
      "data-rag-palette",
      "green",
    );
    expect(screen.getByTestId("dso-ar")).toHaveTextContent("$144.3 K");
    expect(screen.getByTestId("dso-unbilled")).toHaveTextContent("$98.4 K");
  });
});
