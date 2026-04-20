import { NavLink, Outlet } from "react-router-dom";
import { CurrencySelector } from "@/components/CurrencySelector";
import { useUiStore } from "@/stores/uiStore";
import { cn } from "@/lib/cn";

const tabs = [
  { to: "/", label: "Executive", num: "01" },
  { to: "/kpi", label: "KPI Studio", num: "02" },
  { to: "/delivery", label: "Delivery", num: "03", disabled: true },
  { to: "/velocity", label: "Velocity & Flow", num: "04", disabled: true },
  { to: "/margin", label: "Margin & EVM", num: "05", disabled: true },
  { to: "/customer", label: "Customer", num: "06", disabled: true },
  { to: "/ai", label: "AI Governance", num: "07", disabled: true },
  { to: "/smart-ops", label: "Smart Ops", num: "08", disabled: true },
  { to: "/raid", label: "Risk & Audit", num: "09", disabled: true },
  { to: "/reports", label: "Reports", num: "10", disabled: true },
  { to: "/data-hub", label: "Data Hub", num: "11" },
];

export function Layout() {
  const fiscalYearLabel = useUiStore((s) => s.fiscalYearLabel);

  return (
    <div className="flex min-h-screen flex-col bg-ice-50 text-navy">
      <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-navy-600/60 bg-navy px-6 text-white shadow">
        <div className="flex items-center gap-3">
          <div className="flex size-8 items-center justify-center rounded bg-amber-500 font-bold text-navy">
            A
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold">AKB1 Command Center</div>
            <div className="text-xs text-white/70">Delivery Intelligence · v5.2</div>
          </div>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <CurrencySelector />
          <span className="rounded bg-white/10 px-3 py-1 text-xs">{fiscalYearLabel}</span>
        </div>
      </header>

      <div className="flex flex-1">
        <nav
          aria-label="Primary"
          className="sticky top-14 flex h-[calc(100vh-3.5rem)] w-60 shrink-0 flex-col gap-1 overflow-y-auto border-r border-ice-100 bg-white p-3"
        >
          {tabs.map((tab) => (
            <NavLink
              key={tab.to}
              to={tab.to}
              end={tab.to === "/"}
              aria-disabled={tab.disabled ? true : undefined}
              className={({ isActive }) =>
                cn(
                  "group flex items-center justify-between rounded-md px-3 py-2 text-sm font-medium transition",
                  tab.disabled
                    ? "pointer-events-none text-navy/40"
                    : "text-navy hover:bg-ice-50",
                  isActive && !tab.disabled && "bg-navy text-white shadow-sm",
                )
              }
            >
              <span>{tab.label}</span>
              <span
                className={cn(
                  "font-mono text-xs",
                  tab.disabled ? "text-navy/30" : "text-navy/50 group-hover:text-navy",
                )}
              >
                {tab.num}
              </span>
            </NavLink>
          ))}
          <p className="mt-4 px-3 text-[11px] leading-snug text-navy/50">
            Tabs 02–10 light up across Iterations 2–4. See
            <span className="font-mono"> docs/ROADMAP.md</span>.
          </p>
        </nav>

        <main className="flex-1 overflow-x-hidden p-6">
          <Outlet />
        </main>
      </div>

      <footer className="border-t border-ice-100 bg-white px-6 py-3 text-xs text-navy/60">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span>
            v5.2 ·{" "}
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
