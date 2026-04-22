import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { LossesAttribution } from "@/pages/pnl/sections/LossesAttribution";
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
  formula: "losses",
  formula_ref: null,
  entries: [],
  entries_total_count: 4,
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

const PHOENIX_LOSSES: pnlApi.LossesOut = {
  programme_code: "PHOENIX",
  target_gross_margin_pct: 0.3,
  programme_revenue: 820_000,
  portfolio_revenue: 4_380_000,
  rows: [
    {
      loss_category: "Scope Creep",
      amount: 1_200_000,
      revenue_foregone: 1_714_286,
      margin_points_lost_programme_bps: 14634.15,
      margin_points_lost_portfolio_bps: 2739.73,
      snapshot_date: "2026-03-31",
      mitigation_status: "In Progress",
    },
    {
      loss_category: "Rework & Defect Leakage",
      amount: 420_000,
      revenue_foregone: 600_000,
      margin_points_lost_programme_bps: 5121.95,
      margin_points_lost_portfolio_bps: 958.9,
      snapshot_date: "2026-03-31",
      mitigation_status: "Monitoring",
    },
    {
      loss_category: "Bench Tax",
      amount: 180_000,
      revenue_foregone: 257_143,
      margin_points_lost_programme_bps: 2195.12,
      margin_points_lost_portfolio_bps: 410.96,
      snapshot_date: "2026-03-31",
      mitigation_status: "Mitigated",
    },
    {
      loss_category: "Estimation Miss",
      amount: 150_000,
      revenue_foregone: 214_286,
      margin_points_lost_programme_bps: 1829.27,
      margin_points_lost_portfolio_bps: 342.47,
      snapshot_date: "2026-03-31",
      mitigation_status: "Monitoring",
    },
  ],
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const EMPTY_LOSSES: pnlApi.LossesOut = {
  programme_code: "SENTINEL",
  target_gross_margin_pct: 0.3,
  programme_revenue: 1_100_000,
  portfolio_revenue: 4_380_000,
  rows: [],
  filters_applied: EMPTY_FILTERS,
  lineage: { ...LINEAGE, entries_total_count: 0 },
};

function renderAt(url: string) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route path="*" element={<LossesAttribution />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("LossesAttribution", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts the user to pick a programme when ?programme= is absent", () => {
    const spy = vi.spyOn(pnlApi, "fetchPnlLosses");
    renderAt("/pnl");
    expect(
      screen.getByText(/Pick a programme to see losses with attribution/i),
    ).toBeInTheDocument();
    expect(spy).not.toHaveBeenCalled();
  });

  it("shows the skeleton while the losses query is in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlLosses").mockImplementation(
      () => new Promise(() => {}),
    );
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("losses-loading")).toBeInTheDocument();
  });

  it("renders an error banner with the envelope message on failure", async () => {
    const err = new AxiosError(
      "Request failed",
      "ERR_BAD_REQUEST",
      undefined,
      null,
      {
        status: 404,
        data: {
          error: {
            code: "not_found",
            message: "programme 'NOPE' not found",
            details: null,
          },
          filters_applied: null,
        },
        statusText: "Not Found",
        headers: new AxiosHeaders(),
        config: { headers: new AxiosHeaders() } as never,
      },
    );
    vi.spyOn(pnlApi, "fetchPnlLosses").mockRejectedValue(err);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(
        /programme 'NOPE' not found/,
      ),
    );
  });

  it("renders the empty-state message when the losses array is empty", async () => {
    vi.spyOn(pnlApi, "fetchPnlLosses").mockResolvedValue(EMPTY_LOSSES);

    renderAt("/pnl?programme=SENTINEL");

    await waitFor(() =>
      expect(screen.getByTestId("losses-empty")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("losses-empty")).toHaveTextContent(
      /No loss events recorded for this programme/i,
    );
  });

  it("renders all four Phoenix rows with cumulative and red total RAG", async () => {
    vi.spyOn(pnlApi, "fetchPnlLosses").mockResolvedValue(PHOENIX_LOSSES);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("losses-table")).toBeInTheDocument(),
    );

    // Scope Creep row. Amount and cumulative are both $1.20 M because
    // it is the first row — use toHaveTextContent to avoid the
    // multiple-match ambiguity.
    const scope = screen.getByTestId("losses-row-scope-creep");
    expect(scope).toHaveTextContent("2026-03-31");
    expect(scope).toHaveTextContent("Scope Creep");
    expect(scope).toHaveTextContent("In Progress");
    expect(scope).toHaveTextContent("$1.20 M");
    expect(scope).toHaveTextContent("$1.71 M");
    expect(scope).toHaveTextContent("14,634 bps");

    // Rework row, second, cumulative = 1.2M + 420K = 1.62M.
    const rework = screen.getByTestId("losses-row-rework-defect-leakage");
    expect(rework).toHaveTextContent("$420.0 K");
    expect(rework).toHaveTextContent("$1.62 M");

    // Bench Tax, cumulative = 1.62M + 180K = 1.80M.
    const bench = screen.getByTestId("losses-row-bench-tax");
    expect(bench).toHaveTextContent("Mitigated");
    expect(bench).toHaveTextContent("$1.80 M");

    // Estimation Miss, cumulative = 1.80M + 150K = 1.95M.
    const est = screen.getByTestId("losses-row-estimation-miss");
    expect(est).toHaveTextContent("$1.95 M");

    // Total row: 1.95M amount, palette red (237.8% > 2% threshold).
    const totalRow = screen.getByTestId("losses-total-row");
    expect(totalRow).toHaveTextContent("$1.95 M");
    expect(totalRow).toHaveTextContent(/237\.8% of programme revenue/);
    const chip = screen.getByTestId("losses-total-rag");
    expect(chip).toHaveAttribute("data-rag-palette", "red");
    expect(chip).toHaveTextContent("Red");

    // Breakdown chart carries an aria-label with all four categories.
    const chart = screen.getByTestId("losses-breakdown-chart");
    const label = chart.getAttribute("aria-label") ?? "";
    expect(label).toContain("Scope Creep $1.20 M (61.5%)");
    expect(label).toContain("Rework & Defect Leakage $420.0 K (21.5%)");
    expect(label).toContain("Bench Tax $180.0 K (9.2%)");
    expect(label).toContain("Estimation Miss $150.0 K (7.7%)");
  });
});
