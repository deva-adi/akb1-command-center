export type CurrencyCode = "USD" | "INR" | "GBP" | "EUR";

const SYMBOLS: Record<CurrencyCode, string> = {
  USD: "$",
  INR: "₹",
  GBP: "£",
  EUR: "€",
};

const LAKH = 100_000;
const CRORE = 10_000_000;
const MILLION = 1_000_000;
const BILLION = 1_000_000_000;

export function formatCurrency(
  amount: number | null | undefined,
  code: CurrencyCode = "USD",
): string {
  if (amount === null || amount === undefined) return "—";
  const symbol = SYMBOLS[code];
  const abs = Math.abs(amount);

  if (code === "INR") {
    if (abs >= CRORE) return `${symbol}${(amount / CRORE).toFixed(2)} Cr`;
    if (abs >= LAKH) return `${symbol}${(amount / LAKH).toFixed(2)} L`;
    return `${symbol}${amount.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
  }

  // USD / GBP / EUR — Western formatting with K / M / B suffixes
  if (abs >= BILLION) return `${symbol}${(amount / BILLION).toFixed(2)} B`;
  if (abs >= MILLION) return `${symbol}${(amount / MILLION).toFixed(2)} M`;
  if (abs >= 1_000) return `${symbol}${(amount / 1_000).toFixed(1)} K`;
  return `${symbol}${amount.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
}

/** @deprecated — kept for backwards-compat while call sites migrate. */
export const formatCurrencyINR = (amount: number | null | undefined) =>
  formatCurrency(amount, "INR");

export function formatPct(value: number | null | undefined, fractionDigits = 1): string {
  if (value === null || value === undefined) return "—";
  return `${(value * 100).toFixed(fractionDigits)}%`;
}

export function formatRatio(value: number | null | undefined, fractionDigits = 2): string {
  if (value === null || value === undefined) return "—";
  return value.toFixed(fractionDigits);
}

export function formatDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export type RagBucket = "green" | "amber" | "red";

export function bucketForMargin(margin: number | null | undefined): RagBucket {
  if (margin === null || margin === undefined) return "amber";
  if (margin >= 0.22) return "green";
  if (margin >= 0.15) return "amber";
  return "red";
}

export function bucketForStatus(status: string | null | undefined): RagBucket {
  const normalized = (status ?? "").toLowerCase();
  if (normalized.includes("on track")) return "green";
  if (normalized.includes("at risk") || normalized === "red") return "red";
  return "amber";
}
