import { useCurrency } from "@/hooks/useCurrency";
import type { CurrencyCode } from "@/lib/format";

const LABELS: Record<CurrencyCode, string> = {
  USD: "$ USD",
  INR: "₹ INR",
  GBP: "£ GBP",
  EUR: "€ EUR",
};

export function CurrencySelector() {
  const { baseCurrency, setBaseCurrency, availableCurrencies, isLoading } = useCurrency();

  return (
    <label className="flex items-center gap-2 text-xs">
      <span className="sr-only">Base currency</span>
      <span aria-hidden="true" className="text-white/80">
        Base
      </span>
      <select
        value={baseCurrency}
        onChange={(e) => setBaseCurrency(e.target.value as CurrencyCode)}
        disabled={isLoading}
        className="cursor-pointer rounded border border-white/20 bg-white/10 px-3 py-1 font-mono text-xs text-white outline-none transition hover:bg-white/20 focus-visible:outline-2 focus-visible:outline-amber-500"
        aria-label="Base currency"
      >
        {availableCurrencies.map((code) => (
          <option key={code} value={code} className="text-navy">
            {LABELS[code]}
          </option>
        ))}
      </select>
    </label>
  );
}
