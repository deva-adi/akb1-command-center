import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { DrillPanel } from "@/components/DrillPanel";

function renderWithRouter(node: React.ReactNode) {
  return render(<MemoryRouter>{node}</MemoryRouter>);
}

describe("DrillPanel", () => {
  it("renders title, children, and a working close button", () => {
    const onClose = vi.fn();
    renderWithRouter(
      <DrillPanel title="Smoke title" onClose={onClose}>
        <p>Smoke body</p>
      </DrillPanel>,
    );
    expect(screen.getByTestId("drill-panel")).toBeInTheDocument();
    expect(screen.getByText("Smoke title")).toBeInTheDocument();
    expect(screen.getByText("Smoke body")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /close drill panel/i }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("renders the optional cross-tab link with the supplied href", () => {
    renderWithRouter(
      <DrillPanel
        title="With cross-tab"
        onClose={() => {}}
        crossTab={{ label: "Open in tab", href: "/kpi?programme=PHOENIX" }}
      >
        <p>body</p>
      </DrillPanel>,
    );
    const link = screen.getByTestId("drill-panel-cross-tab");
    expect(link).toHaveAttribute("href", "/kpi?programme=PHOENIX");
    expect(link).toHaveTextContent("Open in tab");
  });

  it("renders the optional stub note when supplied", () => {
    renderWithRouter(
      <DrillPanel
        title="Stub"
        onClose={() => {}}
        stubNote="Coming v5.8 stub copy."
      >
        <p>body</p>
      </DrillPanel>,
    );
    expect(screen.getByTestId("drill-panel-stub-note")).toHaveTextContent(
      "Coming v5.8 stub copy.",
    );
  });
});
