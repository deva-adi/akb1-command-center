import { useQuery } from "@tanstack/react-query";
import {
  fetchHealth,
  fetchKpiDefinitions,
  fetchKpiSnapshots,
  fetchProgrammes,
} from "@/lib/api";

export function useHealth() {
  return useQuery({ queryKey: ["health"], queryFn: fetchHealth });
}

export function useProgrammes() {
  return useQuery({ queryKey: ["programmes"], queryFn: fetchProgrammes });
}

export function useKpiDefinitions() {
  return useQuery({ queryKey: ["kpi-definitions"], queryFn: fetchKpiDefinitions });
}

export function useMarginSnapshots() {
  return useQuery({
    queryKey: ["kpi-snapshots", "MARGIN"],
    queryFn: () => fetchKpiSnapshots({ kpiCode: "MARGIN" }),
  });
}

export function useCpiSnapshots() {
  return useQuery({
    queryKey: ["kpi-snapshots", "CPI"],
    queryFn: () => fetchKpiSnapshots({ kpiCode: "CPI" }),
  });
}
