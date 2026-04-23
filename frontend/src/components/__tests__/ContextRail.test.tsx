import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter, Routes, Route, useLocation } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { ContextRail } from "@/components/ContextRail";

vi.mock("@/hooks/usePortfolio", () => ({
  useProgrammes: () => ({
    data: [
      {
        id: 1,
        code: "PHOENIX",
        name: "Phoenix",
        client: "Acme",
        start_date: "2025-04-01",
        end_date: null,
        status: "Active",
        bac: null,
        revenue: null,
        team_size: null,
        offshore_ratio: null,
        delivery_model: null,
      },
      {
        id: 2,
        code: "ATLAS",
        name: "Atlas",
        client: "Acme",
        start_date: "2025-04-01",
        end_date: null,
        status: "Active",
        bac: null,
        revenue: null,
        team_size: null,
        offshore_ratio: null,
        delivery_model: null,
      },
    ],
    isLoading: false,
    error: null,
  }),
}));

function LocationProbe() {
  const loc = useLocation();
  return (
    <div data-testid="current-url">
      {loc.pathname}
      {loc.search}
    </div>
  );
}

function renderAt(url: string, metricOptions?: Array<{ value: string; label: string }>) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route
            path="*"
            element={
              <>
                <ContextRail metricOptions={metricOptions} />
                <LocationProbe />
              </>
            }
          />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("ContextRail", () => {
  beforeEach(() => {
    // jsdom does not ship with a non-placeholder scrollIntoView; prevent noise.
    Element.prototype.scrollIntoView = vi.fn();
  });

  it("renders Portfolio + tab segments on a filter-free URL", () => {
    renderAt("/margin");
    expect(screen.getByText("Portfolio")).toBeInTheDocument();
    expect(screen.getByText("Margin & EVM")).toBeInTheDocument();
    // No programme, metric, period, or tier segment should be present.
    expect(screen.queryByText("Phoenix")).not.toBeInTheDocument();
  });

  it("renders every active filter segment when the URL carries them", () => {
    renderAt(
      "/pnl?programme=PHOENIX&metric=pnl.gross_margin_pct.programme.month&from=2026-03-01&to=2026-03-31&tier=Senior",
    );
    expect(screen.getByText("Portfolio")).toBeInTheDocument();
    expect(screen.getByText("P&L Cockpit")).toBeInTheDocument();
    expect(screen.getByText("Phoenix")).toBeInTheDocument();
    // Metric humanised from the dotted key's last segment.
    expect(screen.getByText("month")).toBeInTheDocument();
    expect(screen.getByText("2026-03-01 → 2026-03-31")).toBeInTheDocument();
    expect(screen.getByText("Senior")).toBeInTheDocument();
  });

  it("drill-up on the tab segment drops every filter but keeps the route", () => {
    renderAt(
      "/margin?programme=PHOENIX&metric=gross_margin_pct&from=2026-03-01&to=2026-03-31",
    );
    const tabLink = screen.getByText("Margin & EVM").closest("a");
    expect(tabLink).toHaveAttribute("href", "/margin");
  });

  it("drill-up on the programme segment keeps only ?programme=", () => {
    renderAt(
      "/margin?programme=PHOENIX&metric=gross_margin_pct&from=2026-03-01&to=2026-03-31",
    );
    const progLink = screen.getByText("Phoenix").closest("a");
    expect(progLink).toHaveAttribute("href", "/margin?programme=PHOENIX");
  });

  it("drill-up on the metric segment keeps programme + metric, drops period", () => {
    renderAt(
      "/pnl?programme=PHOENIX&metric=pnl.gross_margin_pct.programme.month&from=2026-03-01&to=2026-03-31",
    );
    const metricLink = screen.getByText("month").closest("a");
    expect(metricLink).toHaveAttribute(
      "href",
      "/pnl?programme=PHOENIX&metric=pnl.gross_margin_pct.programme.month",
    );
  });

  it("Portfolio segment clears every filter", () => {
    renderAt("/margin?programme=PHOENIX&metric=foo&tier=Senior");
    const home = screen.getByText("Portfolio").closest("a");
    expect(home).toHaveAttribute("href", "/");
  });

  it("drill-across on Programme opens a dropdown and switching rewrites only ?programme=", () => {
    renderAt(
      "/margin?programme=PHOENIX&metric=gross_margin_pct&from=2026-03-01&to=2026-03-31",
    );
    // Open the programme switcher.
    fireEvent.click(screen.getByLabelText("Switch programme"));
    // Dropdown now lists Atlas. Clicking it rewrites only the programme param.
    const atlasLink = screen.getByRole("menuitem", { name: /Atlas/i });
    expect(atlasLink).toHaveAttribute(
      "href",
      "/margin?programme=ATLAS&metric=gross_margin_pct&from=2026-03-01&to=2026-03-31",
    );
  });

  it("metric switcher only renders when metricOptions are provided", () => {
    renderAt("/margin?metric=gross_margin_pct");
    expect(screen.queryByLabelText("Switch metric")).not.toBeInTheDocument();

    renderAt("/pnl?metric=pnl.gross_margin_pct.programme.month", [
      { value: "pnl.gross_margin_pct.programme.month", label: "Gross margin" },
      { value: "pnl.net_margin_pct.programme.month", label: "Net margin" },
    ]);
    expect(screen.getByLabelText("Switch metric")).toBeInTheDocument();
  });
});
