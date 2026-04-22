import { Card, CardHeader } from "@/components/ui/Card";
import { RevenueCards } from "@/pages/pnl/sections/RevenueCards";

export function PnlCockpit() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-navy">P&L Cockpit</h1>
        <p className="mt-1 text-sm text-navy/70">
          Revenue, margin waterfall, margin bridge, plan-forecast-actual
          triangle, losses with attribution, and pyramid with EVM and DSO
          sub-cards. Five sections active in v5.7.0. Three sections
          (KPI Board, Commercial Levers, Narrative) are deferred to v5.8
          per docs/TECH_DEBT.md.
        </p>
      </div>

      <RevenueCards />

      <Card>
        <CardHeader
          title="Remaining sections land in M7.2 through M7.7"
          subtitle="Margin Waterfall, Margin Bridge, PFA Triangle, Losses with Attribution, and Pyramid with EVM and DSO sub-cards. Revenue is live above."
        />
      </Card>
    </div>
  );
}
