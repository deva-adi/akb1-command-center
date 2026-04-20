import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Badge } from "./Badge";

describe("Badge", () => {
  it("renders children with the neutral tone by default", () => {
    render(<Badge>On track</Badge>);
    const el = screen.getByText("On track");
    expect(el).toHaveClass("bg-ice-100");
  });

  it("applies red tone classes", () => {
    render(<Badge tone="red">Breach</Badge>);
    expect(screen.getByText("Breach")).toHaveClass("status-red");
  });
});
