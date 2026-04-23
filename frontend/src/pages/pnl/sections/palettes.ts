/**
 * RAG palette helpers for the Tab 12 P&L sections.
 *
 * Pure functions split out from EarnedValueReceivables.tsx so the
 * section file only exports React components (avoids the
 * react-refresh/only-export-components warning) and so the boundary
 * tests can import the pure helpers without mounting a tree.
 */

export type Palette = "neutral" | "green" | "amber" | "red";

export function cpiSpiPalette(value: number | null): Palette {
  if (value === null) return "neutral";
  if (value >= 1.0) return "green";
  if (value >= 0.9) return "amber";
  return "red";
}

export function dsoPalette(days: number | null): Palette {
  if (days === null) return "neutral";
  if (days < 45) return "green";
  if (days <= 60) return "amber";
  return "red";
}
