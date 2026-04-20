import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchCurrencyRates } from "@/lib/api";
import { useUiStore } from "@/stores/uiStore";
import { formatCurrency, type CurrencyCode } from "@/lib/format";

/**
 * Multi-currency conversion + formatting.
 *
 * Rates come from GET /api/v1/currency/rates and are anchored to USD
 * (rate_to_base[X] = "how many X equal 1 USD"). Amounts in the DB are
 * stored in each programme's native currency; this hook converts them to
 * the user-selected display currency and formats with the right symbol and
 * unit suffix.
 *
 *     convert(amount, source, display) = amount * (rate_display / rate_source)
 *
 * e.g. INR 10_000_000 at 83.5 INR/USD → USD 119_760;
 *      that USD amount at 0.79 GBP/USD → GBP 94_610.
 */
export function useCurrency() {
  const baseCurrency = useUiStore((s) => s.baseCurrency);
  const setBaseCurrency = useUiStore((s) => s.setBaseCurrency);

  const rates = useQuery({
    queryKey: ["currency-rates"],
    queryFn: fetchCurrencyRates,
    staleTime: 10 * 60_000,
  });

  const rateMap = useMemo(() => {
    const map = new Map<string, number>();
    for (const r of rates.data ?? []) {
      const parsed = Number(r.rate_to_base);
      if (Number.isFinite(parsed) && parsed > 0) {
        map.set(r.code, parsed);
      }
    }
    // Guarantee USD always resolves, even before the API call settles.
    if (!map.has("USD")) map.set("USD", 1);
    return map;
  }, [rates.data]);

  const availableCurrencies = useMemo<CurrencyCode[]>(() => {
    const knownOrder: CurrencyCode[] = ["USD", "INR", "GBP", "EUR"];
    return knownOrder.filter((code) => rateMap.has(code));
  }, [rateMap]);

  function convert(
    amount: number | null | undefined,
    sourceCode: string,
    displayCode: CurrencyCode = baseCurrency,
  ): number | null {
    if (amount === null || amount === undefined) return null;
    const source = sourceCode.toUpperCase();
    if (source === displayCode) return amount;
    const sourceRate = rateMap.get(source);
    const displayRate = rateMap.get(displayCode);
    if (!sourceRate || !displayRate) return amount;
    // amount_in_usd = amount / sourceRate; display = amount_in_usd * displayRate.
    return (amount / sourceRate) * displayRate;
  }

  function format(
    amount: number | null | undefined,
    sourceCode = "USD",
    displayCode: CurrencyCode = baseCurrency,
  ): string {
    const converted = convert(amount, sourceCode, displayCode);
    return formatCurrency(converted, displayCode);
  }

  return {
    baseCurrency,
    setBaseCurrency,
    availableCurrencies,
    rates: rates.data ?? [],
    rateMap,
    convert,
    format,
    isLoading: rates.isLoading,
  };
}
