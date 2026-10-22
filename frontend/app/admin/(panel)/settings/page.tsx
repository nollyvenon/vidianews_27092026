"use client";

import { useEffect, useState } from "react";
import { fmtDate, fmtNum, useAdmin } from "../../lib";
import { Alert, Badge, Button, Card, Field, Input, PageTitle, Select, Spinner, Textarea, Toggle, useLoad, useNotice } from "../../ui";

type Values = Record<string, string | boolean | number>;
interface Seo {
  indexable_articles: number;
  published_pages: number;
  sitemap_urls: number;
  missing_image: number;
  missing_summary: number;
  with_custom_meta: number;
  unpublished: number;
  held_back: number;
}
interface AuditItem { id: number; at: string; admin: string; action: string; entity_type: string | null; entity_id: string | null; detail: Record<string, unknown> }
interface AdminRow { id: number; email: string; name: string | null; role: string; is_active: boolean; last_login_at: string | null }

export default function SettingsPage() {
  const { user } = useAdmin();
  return (
    <>
      <PageTitle title="Settings & SEO" hint="Site details used by search engines and social sharing, privacy options, and your account." />
      <div className="space-y-5">
        <SiteSettings isAdmin={user.role === "admin"} />
        <SeoHealth />
        <Account />
        {user.role === "admin" && <Admins />}
        {user.role === "admin" && <Audit />}
      </div>
    </>
  );
}

function SiteSettings({ isAdmin }: { isAdmin: boolean }) {
  const { call } = useAdmin();
  const load = useLoad(() => call<{ settings: Values }>("GET", "/settings"), []);
  const [v, setV] = useState<Values | null>(null);
  const [busy, setBusy] = useState(false);
  const { ok, fail, node } = useNotice();
  useEffect(() => { if (load.data) setV(load.data.settings); }, [load.data]);
  if (!v) return <Card title="Site settings"><Spinner /></Card>;

  const str = (k: string) => String(v[k] ?? "");
  const set = (k: string, val: string | boolean | number) => setV({ ...v, [k]: val });
  async function save() {
    setBusy(true);
    try {
      await call("PUT", "/settings", { values: v });
      ok("Settings saved. Public pages pick them up within a minute.");
    } catch (e) {
      fail(e);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card title="Site settings" actions={isAdmin ? <Button tone="primary" small busy={busy} onClick={save}>Save settings</Button> : <Badge>Admins only</Badge>}>
      <fieldset disabled={!isAdmin} className="space-y-6">
        {node}
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Site name" hint="Used in page titles and structured data."><Input value={str("site_name")} maxLength={80} onChange={(e) => set("site_name", e.target.value)} /></Field>
          <Field label="Tagline" hint="Appended to the home page title."><Input value={str("site_tagline")} maxLength={140} onChange={(e) => set("site_tagline", e.target.value)} /></Field>
        </div>
        <Field label="Site description" hint={`${str("site_description").length}/320 · the default meta description (home page and pages without their own)`}>
          <Textarea rows={3} maxLength={320} value={str("site_description")} onChange={(e) => set("site_description", e.target.value)} />
        </Field>
        <div className="grid gap-4 sm:grid-cols-3">
          <Field label="Default share image" hint="Absolute https URL, ideally 1200×630."><Input value={str("default_og_image")} placeholder="https://…" onChange={(e) => set("default_og_image", e.target.value)} /></Field>
          <Field label="X / Twitter handle"><Input value={str("twitter_handle")} placeholder="@yourname" onChange={(e) => set("twitter_handle", e.target.value)} /></Field>
          <Field label="Contact email"><Input type="email" value={str("contact_email")} onChange={(e) => set("contact_email", e.target.value)} /></Field>
        </div>
        <div className="space-y-3 border-t border-gray-100 pt-4">
          <h3 className="text-sm font-semibold text-gray-900">Privacy & analytics</h3>
          <Toggle label="Collect anonymous visitor statistics" checked={Boolean(v.analytics_enabled)} onChange={(x) => set("analytics_enabled", x)} />
          <Toggle label="Respect browsers' Do Not Track / Global Privacy Control" checked={Boolean(v.respect_dnt)} onChange={(x) => set("respect_dnt", x)} />
          <Field label="Keep visit records for (days)">
            <Input type="number" min={1} max={3650} value={Number(v.analytics_retention_days)} onChange={(e) => set("analytics_retention_days", Number(e.target.value))} className="!w-32" />
          </Field>
          <Field label="Minimum article length (characters)" hint="Stories with less article text than this are kept off the public site and listed under Content → Held back. Applies to new fetches and to the next quality check.">
            <Input type="number" min={1} max={5000} value={Number(v.news_min_content_chars ?? 300)} onChange={(e) => set("news_min_content_chars", Number(e.target.value))} className="!w-32" />
          </Field>
          <Toggle label="Show adverts on the site (master switch)" checked={Boolean(v.ads_enabled)} onChange={(x) => set("ads_enabled", x)} />
        </div>
      </fieldset>
    </Card>
  );
}

function SeoHealth() {
  const { call } = useAdmin();
  const seo = useLoad(() => call<Seo>("GET", "/seo/report"), []);
  const s = seo.data;
  const row = (label: string, value: number, good: boolean, note?: string) => (
    <li className="flex items-center justify-between gap-3 py-2 text-sm">
      <span className="text-gray-700">{label}{note && <span className="block text-xs text-gray-500">{note}</span>}</span>
      <Badge tone={good ? "green" : "amber"}>{fmtNum(value)}</Badge>
    </li>
  );
  return (
    <Card title="Search engine visibility">
      {!s ? <Spinner /> : (
        <>
          <ul className="divide-y divide-gray-100">
            {row("Stories search engines can index", s.indexable_articles, s.indexable_articles > 0)}
            {row("URLs listed in the sitemap", s.sitemap_urls, s.sitemap_urls > 1)}
            {row("Stories missing an image", s.missing_image, s.missing_image === 0, "Shared links look better with an image")}
            {row("Stories missing a summary", s.missing_summary, s.missing_summary === 0)}
            {row("Stories with a hand-written meta description", s.with_custom_meta, true, "Optional: automatic descriptions are used otherwise")}
            {row("Unpublished stories (hidden from search)", s.unpublished, true)}
            {row("Held back: text too short, cut off or only promotion", s.held_back, true, "Review them under Content → Held back")}
          </ul>
          <p className="mt-3 flex flex-wrap gap-4 text-sm">
            <a href="/sitemap.xml" target="_blank" className="text-blue-700 hover:underline">sitemap.xml ↗</a>
            <a href="/robots.txt" target="_blank" className="text-blue-700 hover:underline">robots.txt ↗</a>
          </p>
          <p className="mt-2 text-xs text-gray-500">The admin area and the API are excluded in robots.txt and carry a “noindex” header.</p>
        </>
      )}
    </Card>
  );
}

function Account() {
  const { call } = useAdmin();
  const [cur, setCur] = useState("");
  const [next, setNext] = useState("");
  const [busy, setBusy] = useState(false);
  const { ok, fail, node } = useNotice();
  async function change() {
    setBusy(true);
    try {
      await call("POST", "/auth/change-password", { current_password: cur, new_password: next });
      setCur(""); setNext("");
      ok("Password changed. Your other sessions were signed out.");
    } catch (e) {
      fail(e);
    } finally {
      setBusy(false);
    }
  }
  return (
    <Card title="Change your password">
      <div className="max-w-md space-y-3">
        {node}
        <Field label="Current password"><Input type="password" autoComplete="current-password" value={cur} onChange={(e) => setCur(e.target.value)} /></Field>
        <Field label="New password" hint="At least 12 characters, with letters and a number or symbol."><Input type="password" autoComplete="new-password" value={next} onChange={(e) => setNext(e.target.value)} /></Field>
        <Button tone="primary" busy={busy} disabled={!cur || !next} onClick={change}>Change password</Button>
      </div>
    </Card>
  );
}

function Admins() {
  const { call, user } = useAdmin();
  const list = useLoad(() => call<{ items: AdminRow[] }>("GET", "/users"), []);
  const [f, setF] = useState({ email: "", password: "", role: "editor", name: "" });
  const [busy, setBusy] = useState(false);
  const { ok, fail, node } = useNotice();

  async function add() {
    setBusy(true);
    try {
      await call("POST", "/users", { ...f, name: f.name || null });
      setF({ email: "", password: "", role: "editor", name: "" });
      ok("Account created.");
      list.reload();
    } catch (e) { fail(e); } finally { setBusy(false); }
  }
  async function toggle(a: AdminRow) {
    try {
      await call("PATCH", `/users/${a.id}`, { is_active: !a.is_active });
      list.reload();
    } catch (e) { fail(e); }
  }
  return (
    <Card title="Admin accounts">
      {node}
      {!list.data ? <Spinner /> : (
        <ul className="mb-5 divide-y divide-gray-100 text-sm">
          {list.data.items.map((a) => (
            <li key={a.id} className="flex flex-wrap items-center justify-between gap-2 py-2">
              <span>{a.email} <Badge tone={a.role === "admin" ? "blue" : "gray"}>{a.role}</Badge> {!a.is_active && <Badge tone="red">disabled</Badge>}
                <span className="block text-xs text-gray-500">Last sign-in {fmtDate(a.last_login_at)}</span></span>
              {a.id !== user.id && <Button small onClick={() => toggle(a)}>{a.is_active ? "Disable" : "Enable"}</Button>}
            </li>
          ))}
        </ul>
      )}
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Field label="Email"><Input type="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} /></Field>
        <Field label="Temporary password"><Input type="password" autoComplete="new-password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} /></Field>
        <Field label="Name"><Input value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} /></Field>
        <Field label="Role" hint="Editors manage content and adverts; only admins change settings or start fetches.">
          <Select value={f.role} onChange={(e) => setF({ ...f, role: e.target.value })}><option value="editor">Editor</option><option value="admin">Admin</option></Select>
        </Field>
      </div>
      <div className="mt-3"><Button tone="primary" busy={busy} disabled={!f.email || !f.password} onClick={add}>Add account</Button></div>
    </Card>
  );
}

function Audit() {
  const { call } = useAdmin();
  const [page, setPage] = useState(1);
  const log = useLoad(() => call<{ items: AuditItem[]; total: number; page_size: number }>("GET", `/audit?page=${page}&page_size=15`), [page]);
  const d = log.data;
  return (
    <Card title="Activity log" actions={d && <span className="text-xs text-gray-500">{fmtNum(d.total)} entries</span>}>
      {!d ? <Spinner /> : (
        <>
          <ul className="divide-y divide-gray-100 text-sm">
            {d.items.map((i) => (
              <li key={i.id} className="py-2">
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <span><span className="font-mono text-xs font-semibold text-gray-800">{i.action}</span>{i.entity_id ? <span className="text-gray-500"> #{i.entity_id}</span> : null}</span>
                  <span className="text-xs text-gray-500">{i.admin} · {fmtDate(i.at)}</span>
                </div>
                {Object.keys(i.detail ?? {}).length > 0 && (
                  <pre className="mt-1 max-h-24 overflow-auto whitespace-pre-wrap break-words rounded bg-gray-50 p-2 text-xs text-gray-600">{JSON.stringify(i.detail, null, 1)}</pre>
                )}
              </li>
            ))}
          </ul>
          <div className="mt-3 flex items-center justify-center gap-3 text-sm">
            <Button small disabled={page <= 1} onClick={() => setPage(page - 1)}>← Newer</Button>
            <Button small disabled={page * d.page_size >= d.total} onClick={() => setPage(page + 1)}>Older →</Button>
          </div>
        </>
      )}
      {log.error && <Alert>{log.error}</Alert>}
    </Card>
  );
}
