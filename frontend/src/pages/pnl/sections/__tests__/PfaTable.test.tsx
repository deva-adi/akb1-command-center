import { render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { PfaTable } from "@/pages/pnl/sections/PfaTable";
import * as pnlApi from "@/api/pnlApi";

const EMPTY_FILTERS: pnlApi.FiltersApplied = {
  programme: ["PHOENIX"],
  from: null,
  to: null,
  tier: null,
  scenario_name: null,
  portfolio: null,
  month: null,
};

const LINEAGE: pnlApi.LineageBlock = {
  formula: "PFA triangle",
  formula_ref: null,
  entries: [],
  entries_total_count: 1,
  sampling: "full",
  sampling_rule: null,
};

const PHOENIX_REVENUE: pnlApi.PfaOut = {
  programme_code: "PHOENIX",
  metric: "revenue",
  series: {
    plan: [
      { snapshot_date: "2026-02-01", value: 850_000 },
      { snapshot_date: "2026-03-01", value: 850_000 },
    ],
    forecast: [],
    actual: [
      { snapshot_date: "2026-02-01", value: 845_000 },
      { snapshot_date: "2026-03-01", value: 820_000 },
    ],
  },
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

const PHOENIX_MARGIN: pnlApi.PfaOut = {
  programme_code: "PHOENIX",
  metric: "gross_pct",
  series: {
    plan: [
      { snapshot_date: "2026-02-01", value: 0.36470588235294116 },
      { snapshot_date: "2026-03-01", value: 0.35294117647058826 },
    ],
    forecast: [],
    actual: [
      { snapshot_date: "2026-02-01", value: 0.314 },
      { snapshot_date: "2026-03-01", value: 0.28 },
    ],
  },
  filters_applied: EMPTY_FILTERS,
  lineage: LINEAGE,
};

function renderAt(url: string) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route path="*" element={<PfaTable />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("PfaTable", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts the user to pick a programme when ?programme= is absent", () => {
    const spy = vi.spyOn(pnlApi, "fetchPnlPfa");
    renderAt("/pnl");
    expect(
      screen.getByText(/Pick a programme to see plan vs forecast vs actual/i),
    ).toBeInTheDocument();
    expect(spy).not.toHaveBeenCalled();
  });

  it("shows the skeleton while either query is in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlPfa").mockImplementation(
      () => new Promise(() => {}),
    );
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("pfa-loading")).toBeInTheDocument();
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
    vi.spyOn(pnlApi, "fetchPnlPfa").mockRejectedValue(err);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(
        /programme 'NOPE' not found/,
      ),
    );
  });

  it("renders three rows with Plan, Forecast, Actual, Variance for Phoenix", async () => {
    vi.spyOn(pnlApi, "fetchPnlPfa").mockImplementation(async (_code, metric) =>
      metric === "revenue" ? PHOENIX_REVENUE : PHOENIX_MARGIN,
    );

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("pfa-table")).toBeInTheDocument(),
    );

    // Revenue row: plan 850K, forecast —, actual 820K, variance −$30.0 K (−3.5%).
    const revRow = screen.getByTestId("pfa-row-revenue");
    expect(within(revRow).getByText(/\$850\.0 K/)).toBeInTheDocument();
    expect(within(revRow).getByText(/\$820\.0 K/)).toBeInTheDocument();
    expect(within(revRow).getByText(/−\$30\.0 K \(−3\.5%\)/)).toBeInTheDocument();
    // Neutral palette for the currency-variance cell.
    const revVariance = within(revRow).getByText(/−\$30\.0 K/);
    expect(revVariance).toHaveAttribute("data-variance-palette", "neutral");

    // Cost row: derived. Plan cost = 850_000 * (1 - 0.3529...) ≈ 550_000.
    // Actual cost = 820_000 * (1 - 0.28) = 590_400. Variance ≈ +$40.4 K.
    const costRow = screen.getByTestId("pfa-row-cost-derived");
    expect(within(costRow).getByText(/\$550\.0 K/)).toBeInTheDocument();
    expect(within(costRow).getByText(/\$590\.4 K/)).toBeInTheDocument();
    expect(within(costRow).getByText(/\+\$40\.4 K/)).toBeInTheDocument();

    // Gross margin row: plan 35.3%, actual 28.0%, variance −729 bps, red palette.
    const marRow = screen.getByTestId("pfa-row-gross-margin");
    expect(within(marRow).getByText(/35\.3%/)).toBeInTheDocument();
    expect(within(marRow).getByText(/28\.0%/)).toBeInTheDocument();
    const marVariance = within(marRow).getByText(/−729 bps/);
    expect(marVariance).toHaveAttribute("data-variance-palette", "red");

    // Forecast cells read — because the seed has no Forecast at Completion rows.
    expect(screen.getByTestId("pfa-forecast-footnote")).toHaveTextContent(
      /Forecast at Completion not seeded/,
    );
  });
});
