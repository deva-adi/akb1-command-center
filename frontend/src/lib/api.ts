import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL?.trim() || "";

export const api = axios.create({
  baseURL,
  timeout: 15_000,
  headers: {
    "Content-Type": "application/json",
  },
});

export type HealthResponse = {
  status: string;
  version: string;
  tables: number;
};

export type Programme = {
  id: number;
  name: string;
  code: string;
  client: string | null;
  start_date: string;
  end_date: string | null;
  status: string;
  bac: number | null;
  revenue: number | null;
  team_size: number | null;
  offshore_ratio: number | null;
  delivery_model: string | null;
  currency_code: string;
};

export type KpiDefinition = {
  id: number;
  name: string;
  code: string;
  formula: string;
  unit: string | null;
  green_threshold: number | null;
  amber_threshold: number | null;
  red_threshold: number | null;
  weight: number;
  category: string | null;
  is_higher_better: boolean;
};

export type KpiSnapshot = {
  id: number;
  program_id: number | null;
  project_id: number | null;
  kpi_id: number | null;
  snapshot_date: string;
  value: number;
  trend: string | null;
  notes: string | null;
};

export type AppSetting = {
  key: string;
  value: string | null;
};

export type DataImportLog = {
  id: number;
  file_name: string | null;
  source: string | null;
  rows_imported: number | null;
  status: string | null;
  notes: string | null;
};

export async function fetchHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>("/health");
  return data;
}

export async function fetchProgrammes(): Promise<Programme[]> {
  const { data } = await api.get<Programme[]>("/api/v1/programmes");
  return data;
}

export async function fetchKpiDefinitions(): Promise<KpiDefinition[]> {
  const { data } = await api.get<KpiDefinition[]>("/api/v1/kpi/definitions");
  return data;
}

export async function fetchKpiSnapshots(params: {
  kpiCode?: string;
  programId?: number;
}): Promise<KpiSnapshot[]> {
  const { data } = await api.get<KpiSnapshot[]>("/api/v1/kpi/snapshots", {
    params: {
      kpi_code: params.kpiCode,
      program_id: params.programId,
    },
  });
  return data;
}

export async function fetchSettings(): Promise<AppSetting[]> {
  const { data } = await api.get<AppSetting[]>("/api/v1/settings");
  return data;
}

export async function fetchImportLog(): Promise<DataImportLog[]> {
  const { data } = await api.get<DataImportLog[]>("/api/v1/import/log");
  return data;
}

export async function previewCsv(file: File): Promise<{
  filename: string;
  columns: string[];
  row_count: number;
  sample: Record<string, string>[];
}> {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/api/v1/import/csv/preview", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}
