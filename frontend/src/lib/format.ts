const RUPEE_LAKH = 100_000;
const RUPEE_CRORE = 10_000_000;

export function formatCurrencyINR(amount: number | null | undefined): string {
  if (amount === null || amount === undefined) return "—";
  const abs = Math.abs(amount);
  if (abs >= RUPEE_CRORE) {
    return `₹${(amount / RUPEE_CRORE).toFixed(2)} Cr`;
  }
  if (abs >= RUPEE_LAKH) {
    return `₹${(amount / RUPEE_LAKH).toFixed(2)} L`;
  }
  return `₹${amount.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
}

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
