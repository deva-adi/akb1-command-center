import { describe, expect, it } from "vitest";
import {
  bucketForMargin,
  bucketForStatus,
  formatCurrency,
  formatCurrencyINR,
  formatPct,
  formatRatio,
} from "./format";

describe("formatCurrency — USD (default)", () => {
  it("uses M suffix past 1M", () => {
    expect(formatCurrency(1_250_000)).toBe("$1.25 M");
  });
  it("uses K suffix between 1K and 1M", () => {
    expect(formatCurrency(25_000)).toBe("$25.0 K");
  });
  it("uses plain grouping below 1K", () => {
    expect(formatCurrency(850)).toBe("$850");
  });
  it("returns em dash for null", () => {
    expect(formatCurrency(null)).toBe("—");
  });
});

describe("formatCurrency — INR", () => {
  it("uses Cr suffix past 1 crore", () => {
    expect(formatCurrency(12_500_000, "INR")).toBe("₹1.25 Cr");
  });
  it("uses L suffix between lakh and crore", () => {
    expect(formatCurrency(500_000, "INR")).toBe("₹5.00 L");
  });
});

describe("formatCurrency — GBP / EUR", () => {
  it("uses K suffix for GBP", () => {
    expect(formatCurrency(50_000, "GBP")).toBe("£50.0 K");
  });
  it("uses M suffix for EUR", () => {
    expect(formatCurrency(2_500_000, "EUR")).toBe("€2.50 M");
  });
});

describe("legacy formatCurrencyINR", () => {
  it("delegates to INR-flavoured formatter", () => {
    expect(formatCurrencyINR(12_500_000)).toBe("₹1.25 Cr");
  });
});

describe("formatPct / formatRatio", () => {
  it("formats fractional values as percentages", () => {
    expect(formatPct(0.138)).toBe("13.8%");
  });
  it("formats ratios to two decimals", () => {
    expect(formatRatio(0.8765)).toBe("0.88");
  });
});

describe("RAG buckets", () => {
  it("flags margin below 15% as red", () => {
    expect(bucketForMargin(0.09)).toBe("red");
  });
  it("flags margin between 15 and 22 as amber", () => {
    expect(bucketForMargin(0.18)).toBe("amber");
  });
  it("flags margin above 22% as green", () => {
    expect(bucketForMargin(0.26)).toBe("green");
  });
  it("maps programme status strings to buckets", () => {
    expect(bucketForStatus("On Track")).toBe("green");
    expect(bucketForStatus("At Risk")).toBe("red");
    expect(bucketForStatus("Watch")).toBe("amber");
  });
});
