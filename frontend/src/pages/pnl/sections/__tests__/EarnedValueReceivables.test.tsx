import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { EarnedValueReceivables } from "@/pages/pnl/sections/EarnedValueReceivables";
import { cpiSpiPalette, dsoPalette } from "@/pages/pnl/sections/palettes";
import * as pnlApi from "@/api/pnlApi";

vi.mock("recharts", async () => {
  const actual = await vi.importActual<typeof import("recharts")>("recharts");
  return {
    ...actual,
    ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
      <div style={{ width: 200, height: 52 }}>{children}</div>
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

const FILTERS_PHX: pnlApi.FiltersApplied = {
  programme: ["PHOENIX"],
  from: null,
  to: null,
  tier: null,
  scenario_name: null,
  portfolio: null,
  month: null,
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
  filters_applied: FILTERS_PHX,
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
  filters_applied: FILTERS_PHX,
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
  filters_applied: FILTERS_PHX,
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

function makeAxiosError(message: string): AxiosError {
  return new AxiosError(
    "Request failed",
    "ERR_BAD_REQUEST",
    undefined,
    null,
    {
      status: 500,
      data: {
        error: { code: "server_error", message, details: null },
        filters_applied: null,
      },
      statusText: "Internal Server Error",
      headers: new AxiosHeaders(),
      config: { headers: new AxiosHeaders() } as never,
    },
  );
}

function renderAt(url: string) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route path="*" element={<EarnedValueReceivables />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("cpiSpiPalette", () => {
  it("0.89 below 0.9 is red", () => {
    expect(cpiSpiPalette(0.89)).toBe("red");
  });
  it("0.90 is amber", () => {
    expect(cpiSpiPalette(0.9)).toBe("amber");
  });
  it("0.99 is amber", () => {
    expect(cpiSpiPalette(0.99)).toBe("amber");
  });
  it("1.00 is green", () => {
    expect(cpiSpiPalette(1.0)).toBe("green");
  });
  it("1.01 is green", () => {
    expect(cpiSpiPalette(1.01)).toBe("green");
  });
  it("null is neutral", () => {
    expect(cpiSpiPalette(null)).toBe("neutral");
  });
});

describe("dsoPalette", () => {
  it("44 days is green (under 45)", () => {
    expect(dsoPalette(44)).toBe("green");
  });
  it("45 days is amber (45 to 60 inclusive)", () => {
    expect(dsoPalette(45)).toBe("amber");
  });
  it("60 days is amber (60 still inside band)", () => {
    expect(dsoPalette(60)).toBe("amber");
  });
  it("61 days is red (above 60)", () => {
    expect(dsoPalette(61)).toBe("red");
  });
  it("null is neutral", () => {
    expect(dsoPalette(null)).toBe("neutral");
  });
});

describe("EarnedValueReceivables", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts when no programme is in the URL and skips all three fetchers", () => {
    const evm = vi.spyOn(pnlApi, "fetchPnlEvm");
    const pfa = vi.spyOn(pnlApi, "fetchPnlPfa");
    const dso = vi.spyOn(pnlApi, "fetchPnlDso");
    renderAt("/pnl");
    expect(
      screen.getByText(/Pick a programme to see earned value and receivables/i),
    ).toBeInTheDocument();
    expect(evm).not.toHaveBeenCalled();
    expect(pfa).not.toHaveBeenCalled();
    expect(dso).not.toHaveBeenCalled();
  });

  it("shows an EVM loading skeleton while /evm is in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlEvm").mockImplementation(
      () => new Promise(() => {}),
    );
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("evr-evm-loading")).toBeInTheDocument();
  });

  it("shows a Receivables loading skeleton while /dso is in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlEvm").mockResolvedValue(PHOENIX_EVM);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);
    vi.spyOn(pnlApi, "fetchPnlDso").mockImplementation(
      () => new Promise(() => {}),
    );
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("evr-dso-loading")).toBeInTheDocument();
  });

  it("surfaces an EVM error banner without breaking the Receivables card", async () => {
    vi.spyOn(pnlApi, "fetchPnlEvm").mockRejectedValue(
      makeAxiosError("evm_snapshots join failed"),
    );
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);
    renderAt("/pnl?programme=PHOENIX");
    await waitFor(() =>
      expect(screen.getByText(/evm_snapshots join failed/)).toBeInTheDocument(),
    );
    await waitFor(() =>
      expect(screen.getByTestId("evr-receivables-card")).toBeInTheDocument(),
    );
  });

  it("surfaces a Receivables error banner without breaking the EVM card", async () => {
    vi.spyOn(pnlApi, "fetchPnlEvm").mockResolvedValue(PHOENIX_EVM);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);
    vi.spyOn(pnlApi, "fetchPnlDso").mockRejectedValue(
      makeAxiosError("dso_snapshots not found"),
    );
    renderAt("/pnl?programme=PHOENIX");
    await waitFor(() =>
      expect(screen.getByText(/dso_snapshots not found/)).toBeInTheDocument(),
    );
    await waitFor(() =>
      expect(screen.getByTestId("evr-evm-card")).toBeInTheDocument(),
    );
  });

  it("renders CPI, SPI, sparkline, DSO days, AR and Unbilled WIP for Phoenix", async () => {
    vi.spyOn(pnlApi, "fetchPnlEvm").mockResolvedValue(PHOENIX_EVM);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockImplementation(async (_code, metric) =>
      metric === "cpi" ? PHOENIX_PFA_CPI : PHOENIX_PFA_SPI,
    );

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("evr-evm-card")).toBeInTheDocument(),
    );

    const cpi = screen.getByTestId("evr-cpi");
    expect(cpi).toHaveTextContent("0.87");
    expect(screen.getByTestId("evr-cpi-rag")).toHaveAttribute(
      "data-rag-palette",
      "red",
    );

    const spi = screen.getByTestId("evr-spi");
    expect(spi).toHaveTextContent("0.84");
    expect(screen.getByTestId("evr-spi-rag")).toHaveAttribute(
      "data-rag-palette",
      "red",
    );

    expect(screen.getByTestId("evr-formula")).toHaveTextContent(
      "CPI = EV / AC",
    );
    expect(screen.getByTestId("evr-formula")).toHaveTextContent(
      "SPI = EV / PV",
    );

    expect(screen.getByTestId("evr-sparkline")).toBeInTheDocument();

    expect(screen.getByTestId("evr-dso-days")).toHaveTextContent("6.0 days");
    expect(screen.getByTestId("evr-dso-rag")).toHaveAttribute(
      "data-rag-palette",
      "green",
    );
    expect(screen.getByTestId("evr-dso-ar")).toHaveTextContent("$0.14 M");
    expect(screen.getByTestId("evr-dso-unbilled")).toHaveTextContent("$0.10 M");
  });

  it("renders the Phoenix snapshot dates in each sub-card subtitle", async () => {
    vi.spyOn(pnlApi, "fetchPnlEvm").mockResolvedValue(PHOENIX_EVM);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(PHOENIX_DSO);
    vi.spyOn(pnlApi, "fetchPnlPfa").mockResolvedValue(PHOENIX_PFA_CPI);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() => {
      const evmCard = screen.getByTestId("evr-evm-card");
      expect(evmCard).toHaveTextContent("Snapshot 2026-04-01");
    });
    const dsoCard = screen.getByTestId("evr-receivables-card");
    expect(dsoCard).toHaveTextContent("Snapshot 2026-03-01");
  });
});
