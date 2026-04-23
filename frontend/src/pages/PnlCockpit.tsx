import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { ProgrammePickerModal } from "@/components/ProgrammePickerModal";
import { UnavailableSection } from "@/components/UnavailableSection";
import { useProgrammes } from "@/hooks/usePortfolio";
import { EarnedValueReceivables } from "@/pages/pnl/sections/EarnedValueReceivables";
import { LossesAttribution } from "@/pages/pnl/sections/LossesAttribution";
import { MarginBridge } from "@/pages/pnl/sections/MarginBridge";
import { MarginWaterfall } from "@/pages/pnl/sections/MarginWaterfall";
import { PfaTable } from "@/pages/pnl/sections/PfaTable";
import { PyramidSection } from "@/pages/pnl/sections/PyramidSection";
import { RevenueCards } from "@/pages/pnl/sections/RevenueCards";

export function PnlCockpit() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get("programme");
  // On bare /pnl (no programme) the per-section "pick a programme"
  // placeholders are confusing. Open a modal listing every programme
  // by default. The user can dismiss it (X) to fall back to the
  // section-level placeholders.
  const [pickerOpen, setPickerOpen] = useState(true);
  const programmesQuery = useProgrammes();
  const programmes = (programmesQuery.data ?? []).map((p) => ({
    code: p.code,
    name: p.name,
  }));
  const showPicker = !programme && pickerOpen;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-navy">P&L Cockpit</h1>
        <p className="mt-1 text-sm text-navy/70">
          Revenue, margin waterfall, margin bridge, plan-forecast-actual
          triangle, losses with attribution, pyramid with EVM and DSO
          sub-cards, and a standalone earned value and receivables section.
          Seven sections active in v5.7.0. Three sections (KPI Board,
          Commercial Levers, Narrative) are deferred to v5.8 per
          docs/TECH_DEBT.md.
        </p>
      </div>

      <RevenueCards />
      <MarginBridge />
      <MarginWaterfall />
      <PfaTable />
      <LossesAttribution />
      <PyramidSection />
      <EarnedValueReceivables />

      <UnavailableSection title="KPI Board" />
      <UnavailableSection title="Commercial Levers" />
      <UnavailableSection title="Narrative" />

      <ProgrammePickerModal
        open={showPicker}
        onClose={() => setPickerOpen(false)}
        programmes={programmes}
      />
    </div>
  );
}
