import { useEffect } from "react";
import { NavLink, Outlet, useSearchParams } from "react-router-dom";
import { CurrencySelector } from "@/components/CurrencySelector";
import { ContextRail } from "@/components/ContextRail";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useUiStore } from "@/stores/uiStore";
import { cn } from "@/lib/cn";
import { TABS } from "@/lib/tabRegistry";

const APP_VERSION = "v5.7.0";

const tabs = TABS.map((t) => ({ to: t.path, label: t.label, num: t.number }));

export function Layout() {
  const fiscalYearLabel = useUiStore((s) => s.fiscalYearLabel);
  const theme = useUiStore((s) => s.theme);
  const [searchParams] = useSearchParams();
  // P&L Cockpit (Tab 12) is the only tab that participates in the
  // ContextRail programme filter today. Forward an active ?programme=
  // through the sidebar click so users do not lose context when they
  // jump from a programme-filtered tab into /pnl. Other tabs ignore
  // this on purpose.
  const activeProgramme = searchParams.get("programme");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  return (
    <div className="flex min-h-screen flex-col bg-ice-50 text-navy dark:bg-navy-700 dark:text-navy-50">
      <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-navy-600/60 bg-navy px-6 text-white shadow">
        <div className="flex items-center gap-3">
          <div className="flex size-8 items-center justify-center rounded bg-amber-500 font-bold text-navy">
            A
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold">AKB1 Command Center</div>
            <div className="text-xs text-white/80">Delivery Intelligence · {APP_VERSION}</div>
          </div>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <ThemeToggle />
          <CurrencySelector />
          <span className="rounded bg-white/10 px-3 py-1 text-xs">{fiscalYearLabel}</span>
        </div>
      </header>

      <div className="flex flex-1">
        <nav
          aria-label="Primary"
          className="sticky top-14 flex h-[calc(100vh-3.5rem)] w-60 shrink-0 flex-col gap-1 overflow-y-auto border-r border-ice-100 bg-white p-3 dark:border-navy-500 dark:bg-navy-700"
        >
          {tabs.map((tab) => {
            const targetTo =
              tab.to === "/pnl" && activeProgramme
                ? `${tab.to}?programme=${encodeURIComponent(activeProgramme)}`
                : tab.to;
            return (
              <NavLink
                key={tab.to}
                to={targetTo}
                end={tab.to === "/"}
                aria-label={tab.label}
                className={({ isActive }) =>
                  cn(
                    "group flex items-center justify-between rounded-md px-3 py-2 text-sm font-medium transition",
                    "text-navy hover:bg-ice-50 dark:text-navy-100 dark:hover:bg-navy-600",
                    isActive && "bg-navy text-white shadow-sm dark:bg-navy-500 dark:text-white",
                  )
                }
              >
                <span>{tab.label}</span>
                <span className="font-mono text-xs text-navy/70 group-hover:text-navy dark:text-navy-100/50 dark:group-hover:text-navy-100">
                  {tab.num}
                </span>
              </NavLink>
            );
          })}
        </nav>

        <main className="flex-1 overflow-x-hidden">
          <ContextRail />
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>

      <footer className="border-t border-ice-100 bg-white px-6 py-3 text-xs text-navy/70 dark:border-navy-500 dark:bg-navy-700 dark:text-navy-100/70">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span>
            {APP_VERSION} ·{" "}
            <a
              href="https://github.com/deva-adi/akb1-command-center"
              target="_blank"
              rel="noreferrer"
              className="underline-offset-2 hover:underline"
            >
              github.com/deva-adi/akb1-command-center
            </a>
          </span>
          <span>&copy; Adi Kompalli · MIT licensed</span>
        </div>
      </footer>
    </div>
  );
}
