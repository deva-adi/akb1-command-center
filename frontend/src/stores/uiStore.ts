import { create } from "zustand";
import type { CurrencyCode } from "@/lib/format";

type UiState = {
  baseCurrency: CurrencyCode;
  fiscalYearLabel: string;
  setBaseCurrency: (currency: CurrencyCode) => void;
  setFiscalYearLabel: (label: string) => void;
};

export const useUiStore = create<UiState>((set) => ({
  baseCurrency: "USD",
  fiscalYearLabel: "FY 2025–26 (Apr–Mar)",
  setBaseCurrency: (currency) => set({ baseCurrency: currency }),
  setFiscalYearLabel: (label) => set({ fiscalYearLabel: label }),
}));
