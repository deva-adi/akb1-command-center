import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, it, vi } from "vitest";
import { PnlCockpit } from "@/pages/PnlCockpit";
import { ContextRail } from "@/components/ContextRail";

// Revenue (M7.1) and MarginBridge (M7.2) both fire axios queries on
// mount. Stub the client so this page-level test exercises the
// placeholder copy and the ContextRail wiring without network.
vi.mock("@/api/pnlApi", () => ({
  fetchPnlRevenue: vi.fn(() => new Promise(() => {})),
  fetchPnlDso: vi.fn(() => new Promise(() => {})),
  fetchPnlBridge: vi.fn(() => new Promise(() => {})),
  fetchPnlWaterfall: vi.fn(() => new Promise(() => {})),
}));

vi.mock("@/hooks/usePortfolio", () => ({
  useProgrammes: () => ({
    data: [
      {
        id: 1,
        code: "PHOENIX",
        name: "Phoenix",
        client: "NovaTech",
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

function renderAt(url: string) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[url]}>
        <Routes>
          <Route
            path="*"
            element={
              <>
                <ContextRail />
                <PnlCockpit />
              </>
            }
          />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("PnlCockpit", () => {
  it("renders the page title and the remaining-sections placeholder", () => {
    renderAt("/pnl");
    expect(
      screen.getByRole("heading", { level: 1, name: /P&L Cockpit/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Remaining sections land in M7\.3 through M7\.7/i),
    ).toBeInTheDocument();
  });

  it("ContextRail shows the P&L Cockpit tab segment on /pnl", () => {
    renderAt("/pnl");
    const rail = screen.getByTestId("context-rail");
    expect(rail).toBeInTheDocument();
    expect(rail).toHaveTextContent("Portfolio");
    expect(rail).toHaveTextContent("P&L Cockpit");
  });

  it("ContextRail adds the programme segment when ?programme= is set", () => {
    renderAt("/pnl?programme=PHOENIX");
    const rail = screen.getByTestId("context-rail");
    expect(rail).toHaveTextContent("Portfolio");
    expect(rail).toHaveTextContent("P&L Cockpit");
    expect(rail).toHaveTextContent("Phoenix");
  });
});
