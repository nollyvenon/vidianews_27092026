"use client";

import { useEffect, useState } from "react";
import { fmtDate, fmtNum, relTime, useAdmin } from "../../lib";
import { STATE, FetchStatus } from "../../fetchtypes";
import { Alert, Badge, Button, Card, PageTitle, Spinner, Stat, useLoad, useNotice } from "../../ui";

const CYCLE_TONE: Record<string, "green" | "amber" | "red" | "blue" | "gray"> = {
  completed: "green", partial: "amber", failed: "red", running: "blue", interrupted: "gray",
};

export default function NewsFetchPage() {
  const { call, user } = useAdmin();
  const status = useLoad(() => call<FetchStatus>("GET", "/news/status"), []);
  const { ok, fail, node } = useNotice();
  const [starting, setStarting] = useState<string | null>(null);
  const s = status.data;
  const running = s?.running;

  // While a fetch runs, poll quickly; otherwise refresh once a minute.
  useEffect(() => {
    const t = setInterval(status.reload, running ? 3000 : 60000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [running]);

  async function start(source?: string) {
    setStarting(source ?? "all");
    try {
      await call("POST", `/news/fetch${source ? `?source=${encodeURIComponent(source)}` : ""}`);
      ok(source ? `Fetching ${source}…` : "Fetch started. This page updates while it runs.");
      setTimeout(status.reload, 800);
    } catch (e) {
      fail(e);
    } finally {
      setStarting(null);
    }
  }

  const canFetch = user.role === "admin";
  const st = STATE[s?.state ?? "unknown"];

  return (
    <>
      <PageTitle
        title="News fetching"
        hint="When stories were last collected from the publishers, and when the next collection runs."
        actions={
          <Button tone="primary" busy={starting === "all" || !!running} disabled={!canFetch} onClick={() => start()} title={canFetch ? "" : "Admins only"}>
            {running ? "Fetching…" : "Fetch news now"}
          </Button>
        }
      />
      {node}
      {status.error && <Alert>{status.error}</Alert>}
      {!s ? (
        <Spinner />
      ) : (
        <div className="space-y-5">
          {s.scheduler.enabled === false && <Alert tone="amber">The automatic schedule is switched off (NEWS_ENABLE_SCHEDULER). Only manual fetches run.</Alert>}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Stat label="Status" value={<Badge tone={st.tone}>{st.text}</Badge>} sub={s.last_cycle?.error ? "See the errors below" : undefined} />
            <Stat label="Last fetched" value={relTime(s.last_fetch_at)} sub={fmtDate(s.last_fetch_at)} />
            <Stat
              label="Next scheduled fetch"
              value={s.scheduler.enabled ? relTime(s.scheduler.next_run_at) : "Off"}
              sub={s.scheduler.enabled ? `${fmtDate(s.scheduler.next_run_at)} · every ${s.scheduler.interval_minutes} min` : undefined}
            />
            <Stat label="Failed requests (24 h)" value={fmtNum(s.failed_requests_24h)} tone={s.failed_requests_24h ? "text-red-700" : undefined} sub={`of ${fmtNum(s.requests_24h)} source requests`} />
            <Stat label="Articles retrieved, last fetch" value={fmtNum(s.last_cycle?.items_new)} sub={`${fmtNum(s.last_cycle?.items_seen)} seen · ${fmtNum(s.last_cycle?.items_duplicate)} already stored`} />
            <Stat label="Articles added (24 h)" value={fmtNum(s.articles_added_24h)} />
            <Stat label="Articles stored" value={fmtNum(s.articles_total)} />
            <Stat label="Sources OK, last fetch" value={s.last_cycle ? `${s.last_cycle.sources_ok}/${s.last_cycle.sources_total}` : "—"} />
          </div>

          <Card title="Recent fetches">
            {s.cycles.length === 0 ? (
              <p className="text-sm text-gray-500">No fetch has been recorded since monitoring was added. Use “Fetch news now”.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full min-w-[720px] text-sm">
                  <thead>
                    <tr className="text-left text-xs text-gray-500">
                      {["Started", "Status", "Trigger", "Sources", "New", "Duplicates", "Rejected", "Duration"].map((h) => (
                        <th key={h} className="py-1.5 pr-3 font-medium">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {s.cycles.map((c) => (
                      <tr key={c.id} className="border-t border-gray-100 align-top">
                        <td className="py-2 pr-3 whitespace-nowrap">{fmtDate(c.started_at)}</td>
                        <td className="py-2 pr-3">
                          <Badge tone={CYCLE_TONE[c.status] ?? "gray"}>{c.status}</Badge>
                          {c.error && <div className="mt-1 max-w-xs text-xs text-red-700">{c.error.slice(0, 160)}</div>}
                        </td>
                        <td className="py-2 pr-3">
                          {c.trigger}
                          {c.triggered_by && <div className="text-xs text-gray-500">{c.triggered_by}</div>}
                        </td>
                        <td className="py-2 pr-3 tabular-nums">{c.status === "running" ? "…" : `${c.sources_ok}/${c.sources_total}`}</td>
                        <td className="py-2 pr-3 tabular-nums font-medium">{fmtNum(c.items_new)}</td>
                        <td className="py-2 pr-3 tabular-nums">{fmtNum(c.items_duplicate)}</td>
                        <td className="py-2 pr-3 tabular-nums">{fmtNum(c.items_rejected)}</td>
                        <td className="py-2 pr-3 tabular-nums">{c.duration_s !== null ? `${c.duration_s}s` : "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>

          <Card title="Sources">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[640px] text-sm">
                <thead>
                  <tr className="text-left text-xs text-gray-500">
                    {["Source", "Country", "Articles", "Last request", "Result", ""].map((h) => (
                      <th key={h} className="py-1.5 pr-3 font-medium">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {s.sources.map((src) => (
                    <tr key={src.key} className="border-t border-gray-100 align-top">
                      <td className="py-2 pr-3 font-medium text-gray-900">{src.name}</td>
                      <td className="py-2 pr-3">{src.country}</td>
                      <td className="py-2 pr-3 tabular-nums">{fmtNum(src.articles)}</td>
                      <td className="py-2 pr-3 whitespace-nowrap">{src.last_fetch ? relTime(src.last_fetch.at) : "never"}</td>
                      <td className="py-2 pr-3">
                        {!src.last_fetch ? (
                          <Badge>no data</Badge>
                        ) : src.last_fetch.success ? (
                          <Badge tone="green">OK · {src.last_fetch.new} new</Badge>
                        ) : (
                          <>
                            <Badge tone="red">Failed</Badge>
                            <div className="mt-1 max-w-sm break-words text-xs text-red-700">{src.last_fetch.error}</div>
                          </>
                        )}
                      </td>
                      <td className="py-2 text-right">
                        {canFetch && (
                          <Button small tone="ghost" disabled={!!running} busy={starting === src.key} onClick={() => start(src.key)}>
                            Fetch
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}
    </>
  );
}
