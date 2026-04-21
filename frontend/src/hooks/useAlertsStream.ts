import { useEffect, useState } from "react";

export type StreamAlert = {
  id: number;
  name: string;
  status: string;
  impact: number | null;
  date: string | null;
};

export function useAlertsStream(): StreamAlert[] {
  const [alerts, setAlerts] = useState<StreamAlert[]>([]);

  useEffect(() => {
    const es = new EventSource("/api/v1/smart-ops/alerts/stream");

    es.onmessage = (e: MessageEvent<string>) => {
      try {
        setAlerts(JSON.parse(e.data) as StreamAlert[]);
      } catch {
        // Ignore malformed frames
      }
    };

    es.onerror = () => {
      // EventSource auto-reconnects; no action needed here
    };

    return () => {
      es.close();
    };
  }, []);

  return alerts;
}
