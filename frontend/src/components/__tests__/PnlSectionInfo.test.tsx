import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { PnlSectionInfo } from "@/components/PnlSectionInfo";

describe("PnlSectionInfo", () => {
  it("renders the info icon and the popover title with stub props", () => {
    render(
      <PnlSectionInfo
        title="Smoke title"
        whatItShows="A smoke test"
        howToRead="Verify it renders"
      />,
    );
    // Icon is present via the testid wrapper
    expect(screen.getByTestId("pnl-section-info")).toBeInTheDocument();
    // Popover content is in the DOM (hidden until hover, but always rendered)
    expect(screen.getByText("Smoke title")).toBeInTheDocument();
    expect(screen.getByText(/A smoke test/)).toBeInTheDocument();
    expect(screen.getByText(/Verify it renders/)).toBeInTheDocument();
  });

  it("renders optional formula and thresholds blocks when provided", () => {
    render(
      <PnlSectionInfo
        title="With extras"
        whatItShows="Has both formula and thresholds"
        formula="A = B / C"
        howToRead="Read it carefully"
        thresholds="Green above 1, red below 1"
      />,
    );
    expect(screen.getByText("A = B / C")).toBeInTheDocument();
    expect(screen.getByText(/Green above 1/)).toBeInTheDocument();
  });

  it("omits the formula and thresholds blocks when not provided", () => {
    render(
      <PnlSectionInfo
        title="No extras"
        whatItShows="Bare minimum content"
        howToRead="Just the basics"
      />,
    );
    expect(screen.queryByText(/^Formula:/)).not.toBeInTheDocument();
    expect(screen.queryByText(/^Thresholds:/)).not.toBeInTheDocument();
  });
});
