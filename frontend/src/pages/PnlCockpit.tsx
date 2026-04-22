import { Card, CardHeader } from "@/components/ui/Card";

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

      <Card>
        <CardHeader
          title="Sections load in M7"
          subtitle="M6 delivers the route, the typed API client, and the nav entry. The five section components wire to the nine live /api/v1/pnl/ endpoints in M7."
        />
        <p className="text-sm text-navy/70">
          The nine backend endpoints are already live and reconciliation-tested
          (see docs/FORMULAS.md entries 50 through 55 and the harness at
          backend/tests/test_pnl_reconciliation.py). Pick a programme from the
          sidebar or add <code className="font-mono text-xs">?programme=PHOENIX</code>{" "}
          to the URL to see the ContextRail breadcrumb update.
        </p>
      </Card>
    </div>
  );
}
