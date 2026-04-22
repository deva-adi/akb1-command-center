export type TabEntry = {
  path: string;
  number: string;
  label: string;
};

export const TABS: readonly TabEntry[] = [
  { path: "/", number: "01", label: "Executive" },
  { path: "/kpi", number: "02", label: "KPI Studio" },
  { path: "/delivery", number: "03", label: "Delivery" },
  { path: "/velocity", number: "04", label: "Velocity & Flow" },
  { path: "/margin", number: "05", label: "Margin & EVM" },
  { path: "/customer", number: "06", label: "Customer" },
  { path: "/ai", number: "07", label: "AI Governance" },
  { path: "/smart-ops", number: "08", label: "Smart Ops" },
  { path: "/raid", number: "09", label: "Risk & Audit" },
  { path: "/reports", number: "10", label: "Reports" },
  { path: "/data-hub", number: "11", label: "Data Hub" },
  { path: "/pnl", number: "12", label: "P&L Cockpit" },
];

export function findTabByPath(pathname: string): TabEntry | undefined {
  if (pathname === "/" || pathname === "") return TABS[0];
  return TABS.find((t) => t.path !== "/" && pathname.startsWith(t.path));
}
