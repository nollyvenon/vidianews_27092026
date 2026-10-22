"use client";

import { useState } from "react";
import { BarChart, RankList } from "../../charts";
import { fmtNum, relTime, useAdmin } from "../../lib";
import { Alert, Card, PageTitle, Select, Spinner, Stat, useLoad } from "../../ui";

type Period = "today" | "7d" | "30d" | "90d" | "12m";
type Metric = "page_views" | "visits" | "unique_visitors";
type Gran = "day" | "week" | "month";

interface Summary {
  page_views: number;
  visits: number;
  unique_visitors: number;
  pages_per_visit: number;
  change: Record<Metric, number | null>;
  popular_pages: { path: string; title: string | null; views: number; visitors: number }[];
  countries: { code: string; name: string; count: number }[];
  sources: { key: string; count: number }[];
  referrers: { key: string; count: number }[];
  devices: { key: string; count: number }[];
}
interface Series {
  points: { date: string; page_views: number; visits: number; unique_visitors: number }[];
}
interface Activity {
  active_now: number;
  hourly: { hour: string; page_views: number }[];
  recent: { ts: string; path: string; country_name: string; device: string; source: string; new_visit: boolean }[];
}

const METRICS: { key: Metric; label: string }[] = [
  { key: "page_views", label: "Page views" },
  { key: "visits", label: "Visits" },
  { key: "unique_visitors", label: "Unique visitors" },
];
const SOURCE_LABEL: Record<string, string> = { direct: "Direct", search: "Search engines", social: "Social media", referral: "Other websites" };

function Change({ value }: { value: number | null }) {
  if (value === null) return <span>no earlier data to compare</span>;
  return (
    <span className={value >= 0 ? "text-emerald-700" : "text-red-700"}>
      {value >= 0 ? "▲" : "▼"} {Math.abs(value)}% vs previous period
    </span>
  );
}

function label(date: string, g: Gran) {
  const d = new Date(date + "T00:00:00Z");
  return g === "month"
    ? d.toLocaleDateString("en-GB", { month: "short", year: "2-digit", timeZone: "UTC" })
    : d.toLocaleDateString("en-GB", { day: "numeric", month: "short", timeZone: "UTC" });
}

export default function AnalyticsPage() {
  const { call } = useAdmin();
  const [period, setPeriod] = useState<Period>("7d");
  const [gran, setGran] = useState<Gran>("day");
  const [metric, setMetric] = useState<Metric>("page_views");

  const summary = useLoad(() => call<Summary>("GET", `/analytics/summary?period=${period}`), [period]);
  const series = useLoad(() => call<Series>("GET", `/analytics/timeseries?granularity=${gran}`), [gran]);
  const activity = useLoad(() => call<Activity>("GET", "/analytics/activity"), []);
  const s = summary.data;
  const metricName = METRICS.find((m) => m.key === metric)!.label;

  return (
    <>
      <PageTitle
        title="Analytics"
        hint="Anonymous by design: no IP addresses or cookies are stored, and visitor codes change every day."
        actions={
          <Select value={period} onChange={(e) => setPeriod(e.target.value as Period)} aria-label="Period">
            <option value="today">Today</option>
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="12m">Last 12 months</option>
          </Select>
        }
      />
      {summary.error && <Alert>{summary.error}</Alert>}
      {summary.loading && !s ? (
        <Spinner />
      ) : (
        s && (
          <div className="space-y-5">
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <Stat label="Page views" value={fmtNum(s.page_views)} sub={<Change value={s.change.page_views} />} />
              <Stat label="Visits" value={fmtNum(s.visits)} sub={<Change value={s.change.visits} />} />
              <Stat label="Unique visitors" value={fmtNum(s.unique_visitors)} sub={<Change value={s.change.unique_visitors} />} />
              <Stat label="Pages per visit" value={s.pages_per_visit} sub={`${fmtNum(activity.data?.active_now)} reading now`} />
            </div>

            <Card
              title={`${metricName} over time`}
              actions={
                <>
                  <Select value={metric} onChange={(e) => setMetric(e.target.value as Metric)} aria-label="Metric" className="!w-auto !py-1 text-xs">
                    {METRICS.map((m) => (
                      <option key={m.key} value={m.key}>
                        {m.label}
                      </option>
                    ))}
                  </Select>
                  <Select value={gran} onChange={(e) => setGran(e.target.value as Gran)} aria-label="Grouping" className="!w-auto !py-1 text-xs">
                    <option value="day">Daily (30 days)</option>
                    <option value="week">Weekly (12 weeks)</option>
                    <option value="month">Monthly (12 months)</option>
                  </Select>
                </>
              }
            >
              {series.loading && !series.data ? (
                <Spinner />
              ) : (
                <BarChart name={metricName} points={(series.data?.points ?? []).map((p) => ({ label: label(p.date, gran), value: p[metric] }))} />
              )}
              {gran !== "day" && metric === "unique_visitors" && (
                <p className="mt-2 text-xs text-gray-500">Weekly and monthly figures add up each day&apos;s unique visitors, because visitors cannot be recognised across days.</p>
              )}
            </Card>

            <div className="grid gap-5 lg:grid-cols-2">
              <Card title="Popular pages">
                <RankList
                  rows={s.popular_pages.map((p) => ({ label: p.title ?? p.path, sub: p.title ? p.path : undefined, value: p.views }))}
                  empty="No page views recorded in this period."
                />
              </Card>
              <Card title="Visitor locations (visits)">
                <RankList rows={s.countries.map((c) => ({ label: c.name, value: c.count }))} empty="No visits with a known country yet." />
              </Card>
              <Card title="Traffic sources (visits)">
                <RankList rows={s.sources.map((c) => ({ label: SOURCE_LABEL[c.key] ?? c.key, value: c.count }))} />
                {s.referrers.length > 0 && (
                  <div className="mt-5 border-t border-gray-100 pt-4">
                    <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">Top referring sites</h3>
                    <RankList rows={s.referrers.map((c) => ({ label: c.key, value: c.count }))} />
                  </div>
                )}
              </Card>
              <Card title="Devices (visits)">
                <RankList rows={s.devices.map((c) => ({ label: c.key[0].toUpperCase() + c.key.slice(1), value: c.count }))} />
              </Card>
            </div>
          </div>
        )
      )}

      <div className="mt-5 grid gap-5 lg:grid-cols-2">
        <Card title="Last 24 hours (page views per hour)">
          {activity.data ? (
            <BarChart
              name="Page views"
              height={180}
              points={activity.data.hourly.map((h) => ({ label: new Date(h.hour).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }), value: h.page_views }))}
            />
          ) : (
            <Spinner />
          )}
        </Card>
        <Card title="Live activity" actions={<button className="text-xs text-blue-700 hover:underline" onClick={activity.reload}>Refresh</button>}>
          {!activity.data || activity.data.recent.length === 0 ? (
            <p className="py-4 text-sm text-gray-500">No visits recorded yet.</p>
          ) : (
            <ul className="max-h-72 divide-y divide-gray-100 overflow-y-auto text-sm">
              {activity.data.recent.map((r, i) => (
                <li key={i} className="flex items-baseline justify-between gap-3 py-1.5">
                  <span className="min-w-0 truncate text-gray-800" title={r.path}>
                    {r.new_visit && <span className="mr-1 rounded bg-blue-50 px-1 text-[10px] font-semibold text-blue-700">NEW</span>}
                    {r.path}
                  </span>
                  <span className="flex-none text-xs text-gray-500">
                    {r.country_name} · {r.device} · {r.source} · {relTime(r.ts)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </>
  );
}
