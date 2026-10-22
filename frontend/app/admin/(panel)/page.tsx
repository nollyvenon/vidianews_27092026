"use client";

import Link from "next/link";
import { RankList } from "../charts";
import { fmtDate, fmtNum, relTime, useAdmin } from "../lib";
import { Alert, Badge, Card, PageTitle, Spinner, Stat, useLoad } from "../ui";
import { STATE, FetchStatus } from "../fetchtypes";

interface Summary {
  page_views: number;
  visits: number;
  unique_visitors: number;
  popular_pages: { path: string; title: string | null; views: number }[];
}
interface Seo {
  indexable_articles: number;
  missing_image: number;
  unpublished: number;
  sitemap_urls: number;
}
interface Ads {
  items: { advert_id: string; name: string; state: string; impressions: number; clicks: number }[];
}

export default function Overview() {
  const { call, user } = useAdmin();
  const today = useLoad(() => call<Summary>("GET", "/analytics/summary?period=today"), []);
  const week = useLoad(() => call<Summary>("GET", "/analytics/summary?period=7d"), []);
  const news = useLoad(() => call<FetchStatus>("GET", "/news/status"), []);
  const seo = useLoad(() => call<Seo>("GET", "/seo/report"), []);
  const ads = useLoad(() => call<Ads>("GET", "/ads"), []);
  const live = ads.data?.items.filter((a) => a.state === "live") ?? [];
  const st = STATE[news.data?.state ?? "unknown"];

  return (
    <>
      <PageTitle title="Overview" hint={`Signed in as ${user.email}`} />
      <div className="space-y-5">
        {(today.error || news.error) && <Alert>{today.error ?? news.error}</Alert>}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Stat label="Page views today" value={today.data ? fmtNum(today.data.page_views) : "…"} sub={`${fmtNum(week.data?.page_views)} in the last 7 days`} />
          <Stat label="Visitors today" value={today.data ? fmtNum(today.data.unique_visitors) : "…"} sub={`${fmtNum(week.data?.unique_visitors)} in the last 7 days`} />
          <Stat label="Stories stored" value={news.data ? fmtNum(news.data.articles_total) : "…"} sub={`${fmtNum(news.data?.articles_added_24h)} added in 24 h`} />
          <Stat label="Live adverts" value={ads.data ? live.length : "…"} sub={`${fmtNum(live.reduce((n, a) => n + a.impressions, 0))} impressions in total`} />
        </div>

        <div className="grid gap-5 lg:grid-cols-2">
          <Card title="News fetching" actions={<Link href="/admin/news-fetch" className="text-xs text-blue-700 hover:underline">Details →</Link>}>
            {!news.data ? (
              <Spinner />
            ) : (
              <dl className="grid grid-cols-2 gap-y-3 text-sm">
                <dt className="text-gray-500">Status</dt>
                <dd><Badge tone={st.tone}>{st.text}</Badge></dd>
                <dt className="text-gray-500">Last fetched</dt>
                <dd title={fmtDate(news.data.last_fetch_at)}>{relTime(news.data.last_fetch_at)}</dd>
                <dt className="text-gray-500">Next fetch</dt>
                <dd>{news.data.scheduler.enabled ? relTime(news.data.scheduler.next_run_at) : "Schedule off"}</dd>
                <dt className="text-gray-500">Failed requests (24 h)</dt>
                <dd className={news.data.failed_requests_24h ? "font-medium text-red-700" : ""}>{news.data.failed_requests_24h}</dd>
              </dl>
            )}
          </Card>

          <Card title="Most read today" actions={<Link href="/admin/analytics" className="text-xs text-blue-700 hover:underline">All analytics →</Link>}>
            <RankList rows={(today.data?.popular_pages ?? []).slice(0, 6).map((p) => ({ label: p.title ?? p.path, value: p.views }))} empty="No visits recorded today." />
          </Card>

          <Card title="Search visibility" actions={<Link href="/admin/settings" className="text-xs text-blue-700 hover:underline">SEO settings →</Link>}>
            {!seo.data ? (
              <Spinner />
            ) : (
              <dl className="grid grid-cols-2 gap-y-3 text-sm">
                <dt className="text-gray-500">URLs in the sitemap</dt>
                <dd>{fmtNum(seo.data.sitemap_urls)}</dd>
                <dt className="text-gray-500">Stories without an image</dt>
                <dd>{fmtNum(seo.data.missing_image)}</dd>
                <dt className="text-gray-500">Unpublished stories</dt>
                <dd>{fmtNum(seo.data.unpublished)}</dd>
                <dt className="text-gray-500">Sitemap &amp; robots</dt>
                <dd className="space-x-3">
                  <a href="/sitemap.xml" target="_blank" className="text-blue-700 hover:underline">sitemap.xml</a>
                  <a href="/robots.txt" target="_blank" className="text-blue-700 hover:underline">robots.txt</a>
                </dd>
              </dl>
            )}
          </Card>

          <Card title="Adverts" actions={<Link href="/admin/adverts" className="text-xs text-blue-700 hover:underline">Manage →</Link>}>
            {!ads.data ? (
              <Spinner />
            ) : ads.data.items.length === 0 ? (
              <p className="text-sm text-gray-500">No adverts yet.</p>
            ) : (
              <ul className="divide-y divide-gray-100 text-sm">
                {ads.data.items.slice(0, 5).map((a) => (
                  <li key={a.advert_id} className="flex items-center justify-between gap-3 py-2">
                    <span className="min-w-0 truncate">{a.name} <span className="text-xs text-gray-500">{a.advert_id}</span></span>
                    <span className="flex-none text-xs text-gray-500">{fmtNum(a.impressions)} views · {fmtNum(a.clicks)} clicks</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>
      </div>
    </>
  );
}
