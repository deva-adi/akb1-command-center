import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { Layout } from "@/components/Layout";
import { queryClient } from "@/lib/queryClient";
import { ExecutiveOverview } from "@/pages/ExecutiveOverview";
import { DataHub } from "@/pages/DataHub";
import { NotFound } from "@/pages/NotFound";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <ExecutiveOverview /> },
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
