import { Moon, Sun } from "lucide-react";
import { useUiStore } from "@/stores/uiStore";

export function ThemeToggle() {
  const theme = useUiStore((s) => s.theme);
  const toggleTheme = useUiStore((s) => s.toggleTheme);

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
      className="flex size-8 items-center justify-center rounded-md text-white/70 transition hover:bg-white/10 hover:text-white"
    >
      {theme === "light" ? (
        <Moon className="size-4" aria-hidden="true" />
      ) : (
        <Sun className="size-4" aria-hidden="true" />
      )}
    </button>
  );
}
