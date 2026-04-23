import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { AxiosError, AxiosHeaders } from "axios";
import { MarginBridge } from "@/pages/pnl/sections/MarginBridge";
import * as pnlApi from "@/api/pnlApi";

// Recharts resizes via ResponsiveContainer which needs a measurable
// width in jsdom; stub the container to give the chart a fixed frame
// so Bars render and labels become queryable in the DOM.
vi.mock("recharts", async () => {
  const actual = await vi.importActual<typeof import("recharts")>("recharts");
  return {
    ...actual,
    ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
      <div style={{ width: 800, height: 300 }}>{children}</div>
    ),
  };
});

const PHOENIX_BRIDGE: pnlApi.BridgeOut = {
  metric_key: "pnl.gross_margin_pct.programme.month",
  programme_code: "PHOENIX",
  prior_snapshot_date: "2026-02-01",
  current_snapshot_date: "2026-03-01",
  prior_value: 0.314,
  current_value: 0.28,
  total_delta_bps: -340.0,
  drivers: {
    price_bps: 147.17,
    volume_bps: 61.71,
    mix_bps: -505.65,
    cost_bps_residual: -43.23,
  },
  filters_applied: {
    programme: ["PHOENIX"],
    from: "2026-02-01",
    to: "2026-03-01",
    tier: null,
    scenario_name: null,
    portfolio: null,
    month: null,
  },
  lineage: {
    formula:
      "Total delta bps = (current.gross_margin_pct - prior.gross_margin_pct) * 10000.",
    formula_ref: null,
    entries: [],
    entries_total_count: 2,
    sampling: "full",
    sampling_rule: null,
  },
};

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
  filters_applied: PHOENIX_BRIDGE.filters_applied,
  lineage: PHOENIX_BRIDGE.lineage,
};

function renderAt(url: string) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route path="*" element={<MarginBridge />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("MarginBridge", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("prompts the user to pick a programme when ?programme= is absent", () => {
    const bridge = vi.spyOn(pnlApi, "fetchPnlBridge");
    const waterfall = vi.spyOn(pnlApi, "fetchPnlWaterfall");
    renderAt("/pnl");
    expect(
      screen.getByText(/Pick a programme to see the margin bridge/i),
    ).toBeInTheDocument();
    expect(bridge).not.toHaveBeenCalled();
    expect(waterfall).not.toHaveBeenCalled();
  });

  it("shows a skeleton while the bridge query is in flight", () => {
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);
    vi.spyOn(pnlApi, "fetchPnlBridge").mockImplementation(
      () => new Promise(() => {}),
    );
    renderAt("/pnl?programme=PHOENIX");
    expect(screen.getByTestId("margin-bridge-loading")).toBeInTheDocument();
  });

  it("renders an error banner with the envelope message on failure", async () => {
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);
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
            message:
              "no commercial_scenarios rows for 'PHOENIX' at both 2026-02-01 and 2026-03-01",
            details: null,
          },
          filters_applied: null,
        },
        statusText: "Not Found",
        headers: new AxiosHeaders(),
        config: { headers: new AxiosHeaders() } as never,
      },
    );
    vi.spyOn(pnlApi, "fetchPnlBridge").mockRejectedValue(err);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(
        /no commercial_scenarios rows for 'PHOENIX'/,
      ),
    );
  });

  it("renders the bridge chart with prior, current, and four driver bars", async () => {
    vi.spyOn(pnlApi, "fetchPnlWaterfall").mockResolvedValue(PHOENIX_WATERFALL);
    vi.spyOn(pnlApi, "fetchPnlBridge").mockResolvedValue(PHOENIX_BRIDGE);

    renderAt("/pnl?programme=PHOENIX");

    await waitFor(() =>
      expect(screen.getByTestId("margin-bridge-chart")).toBeInTheDocument(),
    );

    const chart = screen.getByTestId("margin-bridge-chart");

    // The accessible label packs every bar value for screen readers.
    expect(chart).toHaveAttribute(
      "aria-label",
      expect.stringContaining("prior 31.4%"),
    );
    expect(chart).toHaveAttribute(
      "aria-label",
      expect.stringContaining("current 28.0%"),
    );
    expect(chart).toHaveAttribute(
      "aria-label",
      expect.stringContaining("total −340 bps"),
    );
    expect(chart).toHaveAttribute(
      "aria-label",
      expect.stringContaining("price +147 bps"),
    );
    expect(chart).toHaveAttribute(
      "aria-label",
      expect.stringContaining("mix −506 bps"),
    );

    // Subtitle records the two snapshots and the delta.
    expect(
      screen.getByText(
        /Gross margin 31\.4% on 2026-02-01 → 28\.0% on 2026-03-01 · total delta −340 bps/,
      ),
    ).toBeInTheDocument();
  });
});
