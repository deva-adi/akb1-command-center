import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { Layout } from "@/components/Layout";
import { queryClient } from "@/lib/queryClient";
import { AiGovernance } from "@/pages/AiGovernance";
import { CustomerIntelligence } from "@/pages/CustomerIntelligence";
import { ExecutiveOverview } from "@/pages/ExecutiveOverview";
import { DataHub } from "@/pages/DataHub";
import { DeliveryHealth } from "@/pages/DeliveryHealth";
import { KpiStudio } from "@/pages/KpiStudio";
import { MarginEvm } from "@/pages/MarginEvm";
import { NotFound } from "@/pages/NotFound";
import { RiskAudit } from "@/pages/RiskAudit";
import { SmartOps } from "@/pages/SmartOps";
import { VelocityFlow } from "@/pages/VelocityFlow";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <ExecutiveOverview /> },
      { path: "kpi", element: <KpiStudio /> },
      { path: "delivery", element: <DeliveryHealth /> },
      { path: "velocity", element: <VelocityFlow /> },
      { path: "margin", element: <MarginEvm /> },
      { path: "customer", element: <CustomerIntelligence /> },
      { path: "ai", element: <AiGovernance /> },
      { path: "smart-ops", element: <SmartOps /> },
      { path: "raid", element: <RiskAudit /> },
      { path: "data-hub", element: <DataHub /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}
