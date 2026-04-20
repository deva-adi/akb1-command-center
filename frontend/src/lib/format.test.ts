import { describe, expect, it } from "vitest";
import {
  bucketForMargin,
  bucketForStatus,
  formatCurrencyINR,
  formatPct,
  formatRatio,
} from "./format";

describe("formatCurrencyINR", () => {
  it("uses crore suffix past 1 crore", () => {
    expect(formatCurrencyINR(12_500_000)).toBe("₹1.25 Cr");
  });
  it("uses lakh suffix between 1 lakh and 1 crore", () => {
    expect(formatCurrencyINR(500_000)).toBe("₹5.00 L");
  });
  it("falls back to Indian digit grouping below 1 lakh", () => {
    expect(formatCurrencyINR(45_678)).toMatch(/^₹45,678$/);
  });
  it("returns em dash for null", () => {
    expect(formatCurrencyINR(null)).toBe("—");
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
