export interface Cycle {
  id: number;
  started_at: string;
  finished_at: string | null;
  duration_s: number | null;
  status: string;
  trigger: string;
  triggered_by: string | null;
  sources_total: number;
  sources_ok: number;
  sources_failed: number;
  items_seen: number;
  items_new: number;
  items_duplicate: number;
  items_rejected: number;
  enriched: number;
  error: string | null;
}
export interface FetchStatus {
  state: "running" | "never_run" | "healthy" | "degraded" | "failing" | "unknown";
  running: boolean;
  last_fetch_at: string | null;
  last_cycle: Cycle | null;
  scheduler: { enabled: boolean; running: boolean; interval_minutes: number; next_run_at: string | null };
  articles_total: number;
  articles_added_24h: number;
  requests_24h: number;
  failed_requests_24h: number;
  cycles: Cycle[];
  sources: { key: string; name: string; country: string; articles: number; last_fetch: { at: string; success: boolean; new: number; error: string | null } | null }[];
}

export const STATE: Record<string, { tone: "green" | "amber" | "red" | "blue" | "gray"; text: string }> = {
  running: { tone: "blue", text: "Fetching now" },
  healthy: { tone: "green", text: "Healthy" },
  degraded: { tone: "amber", text: "Some sources failed" },
  failing: { tone: "red", text: "Failing" },
  never_run: { tone: "gray", text: "Not run yet" },
  unknown: { tone: "gray", text: "Unknown" },
};
