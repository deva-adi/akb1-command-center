import { create } from "zustand";
import type { CurrencyCode } from "@/lib/format";

type Theme = "light" | "dark";

type UiState = {
  baseCurrency: CurrencyCode;
  fiscalYearLabel: string;
  theme: Theme;
  setBaseCurrency: (currency: CurrencyCode) => void;
  setFiscalYearLabel: (label: string) => void;
  toggleTheme: () => void;
};

function loadTheme(): Theme {
  try {
    const stored = localStorage.getItem("akb1-theme");
    if (stored === "dark" || stored === "light") return stored;
  } catch { /* SSR / private browsing */ }
  return "light";
}

export const useUiStore = create<UiState>((set) => ({
  baseCurrency: "USD",
  fiscalYearLabel: "FY 2025–26 (Apr–Mar)",
  theme: loadTheme(),
  setBaseCurrency: (currency) => set({ baseCurrency: currency }),
  setFiscalYearLabel: (label) => set({ fiscalYearLabel: label }),
  toggleTheme: () =>
    set((state) => {
      const next: Theme = state.theme === "light" ? "dark" : "light";
      try {
        localStorage.setItem("akb1-theme", next);
      } catch { /* ignore */ }
      return { theme: next };
    }),
}));
