import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { MarginWaterfall } from "@/pages/pnl/sections/MarginWaterfall";
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

const PHOENIX_WATERFALL: pnlApi.WaterfallOut = {
  programme_code: "PHOENIX",
  snapshot_date: "2026-03-01",
  scenario_name: "Monthly Actuals",
  revenue: 820_000,
  layers: [
    { layer: "gross", label: "Gross margin", margin_pct: 0.28, margin_value: 229_600 },
    { layer: "contribution", label: "Contribution margin", margin_pct: 0.125, margin_value: 102_500 },
    { layer: "portfolio", label: "Portfolio margin", margin_pct: 0.082, margin_value: 67_240 },
    { layer: "net", label: "Net margin", margin_pct: 0.041, margin_value: 33_620 },
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
    formula: "layers = [gross, contribution, portfolio, net] from commercial_scenarios",
    formula_ref: null,
    entries: [],
    entries_total_count: 1,
    sampling: "full",
    sampling_rule: null,
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
          <Route path="*" element={<MarginWaterfall />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("MarginWaterfall", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts the user to pick a programme when ?programme= is absent", () => {
    const spy = vi.spyOn(pnlApi, "fetchPnlWaterfall");
    renderAt("/pnl");
    expect(
      screen.getByText(/Pick a programme to see the margin waterfall/i),
    ).toBeInTheDocument();
    expect(spy).not.toHaveBeenCalled();
  });

  it("shows a skeleton while the waterfall query is in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockImplementation(
      () => new Promise(() => {}),
    );
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("margin-waterfall-loading")).toBeInTheDocument();
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
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockRejectedValue(err);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(
        /no commercial_scenarios rows for 'PHOENIX'/,
      ),
    );
  });

  it("renders the four-layer cascade with drop annotations between bars", async () => {
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("margin-waterfall-chart")).toBeInTheDocument(),
    );

    const chart = screen.getByTestId("margin-waterfall-chart");

    // Accessibility label packs every layer + every drop.
    const label = chart.getAttribute("aria-label") ?? "";
    expect(label).toContain("Gross margin 28.0%");
    expect(label).toContain("Contribution margin 12.5%");
    expect(label).toContain("Portfolio margin 8.2%");
    expect(label).toContain("Net margin 4.1%");
    // Drops in bps: gross->contribution 1550, contribution->portfolio 430, portfolio->net 410.
    expect(label).toContain("gross to contribution −1550 bps");
    expect(label).toContain("contribution to portfolio −430 bps");
    expect(label).toContain("portfolio to net −410 bps");

    // Subtitle carries the snapshot metadata.
    expect(
      screen.getByText(
        /Snapshot 2026-03-01 · scenario Monthly Actuals · revenue base 820,000/,
      ),
    ).toBeInTheDocument();

    // Drop pills row exists and shows three pills.
    const drops = screen.getByTestId("margin-waterfall-drops");
    expect(drops).toHaveTextContent("−1550 bps");
    expect(drops).toHaveTextContent("−430 bps");
    expect(drops).toHaveTextContent("−410 bps");
  });
});
