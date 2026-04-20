import { create } from "zustand";

type UiState = {
  baseCurrency: string;
  fiscalYearLabel: string;
  setBaseCurrency: (currency: string) => void;
  setFiscalYearLabel: (label: string) => void;
};

export const useUiStore = create<UiState>((set) => ({
  baseCurrency: "INR",
  fiscalYearLabel: "FY 2025–26 (Apr–Mar)",
  setBaseCurrency: (currency) => set({ baseCurrency: currency }),
  setFiscalYearLabel: (label) => set({ fiscalYearLabel: label }),
}));
