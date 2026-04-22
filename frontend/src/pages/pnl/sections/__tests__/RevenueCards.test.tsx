import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { RevenueCards } from "@/pages/pnl/sections/RevenueCards";
import * as pnlApi from "@/api/pnlApi";

const MAR_REVENUE: pnlApi.RevenueOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-03-01",
  scenario_name: "Monthly Actuals",
  cards: [
    {
      card_key: "committed_revenue",
      label: "Committed revenue",
      value: 850_000,
      source_column: "planned_revenue",
    },
    {
      card_key: "booked_revenue",
      label: "Booked revenue",
      value: 820_000,
      source_column: "actual_revenue",
    },
    {
      card_key: "billed_revenue",
      label: "Billed revenue",
      value: 721_600,
      source_column: "billed_revenue",
    },
    {
      card_key: "collected_revenue",
      label: "Collected revenue",
      value: 577_280,
      source_column: "collected_revenue",
    },
    {
      card_key: "unbilled_wip",
      label: "Unbilled WIP",
      value: 98_400,
      source_column: "unbilled_wip",
    },
  ],
  filters_applied: {
    programme: ["PHOENIX"],
    from: null,
    to: null,
    tier: null,
    scenario_name: null,
    portfolio: null,
    month: null,
  },
  lineage: {
    formula: "select cards from financials",
    formula_ref: null,
    entries: [],
    entries_total_count: 1,
    sampling: "full",
    sampling_rule: null,
  },
};

const FEB_REVENUE: pnlApi.RevenueOut = {
  ...MAR_REVENUE,
  snapshot_date: "2026-02-01",
  cards: [
    { ...MAR_REVENUE.cards[0], value: 850_000 },
    { ...MAR_REVENUE.cards[1], value: 845_000 },
    { ...MAR_REVENUE.cards[2], value: 743_600 },
    { ...MAR_REVENUE.cards[3], value: 594_880 },
    { ...MAR_REVENUE.cards[4], value: 101_400 },
  ],
};

const MAR_DSO: pnlApi.DsoOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-03-01",
  scenario_name: "Monthly Actuals",
  billed_revenue: 721_600,
  collected_revenue: 577_280,
  ar_balance: 144_320,
  unbilled_wip: 98_400,
  dso_days: 6.0,
  filters_applied: MAR_REVENUE.filters_applied,
  lineage: MAR_REVENUE.lineage,
};

const FEB_DSO: pnlApi.DsoOut = {
  ...MAR_DSO,
  snapshot_date: "2026-02-01",
  billed_revenue: 743_600,
  collected_revenue: 594_880,
  ar_balance: 148_720,
  unbilled_wip: 101_400,
};

function renderAt(url: string) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route path="*" element={<RevenueCards />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("RevenueCards", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts the user to pick a programme when ?programme= is absent", () => {
    const rev = vi.spyOn(pnlApi, "fetchPnlRevenue");
    const dso = vi.spyOn(pnlApi, "fetchPnlDso");
    renderAt("/pnl");
    expect(screen.getByText(/Pick a programme to see revenue/i)).toBeInTheDocument();
    expect(rev).not.toHaveBeenCalled();
    expect(dso).not.toHaveBeenCalled();
  });

  it("shows a skeleton grid while current-period queries are in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlRevenue").mockImplementation(
      () => new Promise(() => {}),
    );
    vi.spyOn(pnlApi, "fetchPnlDso").mockImplementation(
      () => new Promise(() => {}),
    );
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("revenue-cards-loading")).toBeInTheDocument();
  });

  it("renders an error banner carrying the envelope message when a query fails", async () => {
    const envelopeError = new AxiosError(
      "Request failed",
      "ERR_BAD_REQUEST",
      undefined,
      null,
      {
        status: 404,
        data: {
          error: {
            code: "not_found",
            message: "no commercial_scenarios rows for 'PHOENIX'",
            details: null,
          },
          filters_applied: null,
        },
        statusText: "Not Found",
        headers: new AxiosHeaders(),
        config: { headers: new AxiosHeaders() } as never,
      },
    );
    vi.spyOn(pnlApi, "fetchPnlRevenue").mockRejectedValue(envelopeError);
    vi.spyOn(pnlApi, "fetchPnlDso").mockResolvedValue(MAR_DSO);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(
        /no commercial_scenarios rows for 'PHOENIX'/,
      ),
    );
  });

  it("renders five cards with current values and period-over-period deltas", async () => {
    vi.spyOn(pnlApi, "fetchPnlRevenue").mockImplementation(async (_code, filters) => {
      // Current request has no `from`; prior request sets `from=2026-02-01`.
      if (filters?.from === "2026-02-01") return FEB_REVENUE;
      return MAR_REVENUE;
    });
    vi.spyOn(pnlApi, "fetchPnlDso").mockImplementation(async (_code, filters) => {
      if (filters?.from === "2026-02-01") return FEB_DSO;
      return MAR_DSO;
    });

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("revenue-cards")).toBeInTheDocument(),
    );

    const grid = screen.getByTestId("revenue-cards");

    // Labels present for every card.
    expect(grid).toHaveTextContent("Booked revenue");
    expect(grid).toHaveTextContent("Billed revenue");
    expect(grid).toHaveTextContent("Collected revenue");
    expect(grid).toHaveTextContent("Unbilled WIP");
    expect(grid).toHaveTextContent("AR balance");

    // Current values formatted via formatCurrency with K suffix.
    expect(grid).toHaveTextContent("$820.0 K"); // booked current
    expect(grid).toHaveTextContent("$721.6 K"); // billed current
    expect(grid).toHaveTextContent("$144.3 K"); // AR current

    // Deltas from prior month wait for the prior-period fetches to
    // land before rendering.
    await waitFor(() => {
      const g = screen.getByTestId("revenue-cards");
      // Booked Mar 820K - Feb 845K = -25K drop.
      expect(g).toHaveTextContent("−$25.0 K");
      // AR Mar 144.32K - Feb 148.72K = -4.4K (cash moved favourably).
      expect(g).toHaveTextContent("−$4.4 K");
    });
  });
});
