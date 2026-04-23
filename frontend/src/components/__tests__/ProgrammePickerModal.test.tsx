import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProgrammePickerModal } from "@/components/ProgrammePickerModal";

function renderWithRouter(node: React.ReactNode) {
  return render(<MemoryRouter>{node}</MemoryRouter>);
}

const PROGRAMMES = [
  { code: "PHOENIX", name: "Phoenix" },
  { code: "ATLAS", name: "Atlas" },
];

describe("ProgrammePickerModal", () => {
  it("renders nothing when open is false", () => {
    const { container } = renderWithRouter(
      <ProgrammePickerModal
        open={false}
        onClose={() => {}}
        programmes={PROGRAMMES}
      />,
    );
    expect(container).toBeEmptyDOMElement();
  });

  it("renders the modal with one button per programme when open", () => {
    renderWithRouter(
      <ProgrammePickerModal
        open
        onClose={() => {}}
        programmes={PROGRAMMES}
      />,
    );
    expect(screen.getByTestId("programme-picker-modal")).toBeInTheDocument();
    const phoenix = screen.getByTestId("programme-picker-option-PHOENIX");
    const atlas = screen.getByTestId("programme-picker-option-ATLAS");
    expect(phoenix).toHaveAttribute("href", "/pnl?programme=PHOENIX");
    expect(atlas).toHaveAttribute("href", "/pnl?programme=ATLAS");
  });

  it("calls onClose when the X button is clicked", () => {
    const onClose = vi.fn();
    renderWithRouter(
      <ProgrammePickerModal open onClose={onClose} programmes={PROGRAMMES} />,
    );
    fireEvent.click(screen.getByRole("button", { name: /close programme picker/i }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("shows the empty state when no programmes are returned", () => {
    renderWithRouter(
      <ProgrammePickerModal open onClose={() => {}} programmes={[]} />,
    );
    expect(
      screen.getByText(/No programmes returned by the API/i),
    ).toBeInTheDocument();
  });
});
