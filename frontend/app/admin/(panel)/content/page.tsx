"use client";

import { useEffect, useState } from "react";
import { fmtDate, useAdmin } from "../../lib";
import { Alert, Badge, Button, Card, Field, Input, Modal, PageTitle, Select, Spinner, Textarea, Toggle, useLoad, useNotice } from "../../ui";

interface Row {
  id: number;
  title: string;
  source: string;
  category: string;
  published_at: string;
  status: "published" | "unpublished" | "deleted";
  has_image: boolean;
  clicks: number;
  validation: string;
  edited_by: string | null;
}
interface List {
  items: Row[];
  total: number;
  page: number;
  total_pages: number;
  categories: string[];
}
interface Detail extends Row {
  url: string;
  summary: string | null;
  description: string | null;
  body_text: string;
  image_url: string | null;
  image_credit: string | null;
  meta_title: string | null;
  meta_description: string | null;
}
interface SitePage {
  id: number;
  slug: string;
  title: string;
  body: string;
  meta_description: string | null;
  is_published: boolean;
  updated_at: string | null;
  updated_by: string | null;
}

const STATUS_TONE = { published: "green", unpublished: "amber", deleted: "red" } as const;

export default function ContentPage() {
  const [tab, setTab] = useState<"articles" | "pages">("articles");
  const tabCls = (t: string) => `border-b-2 px-4 py-2 text-sm font-medium ${tab === t ? "border-blue-600 text-blue-700" : "border-transparent text-gray-600 hover:text-gray-900"}`;
  return (
    <>
      <PageTitle title="Content" hint="Edit, publish, unpublish or delete news articles and the site's own pages." />
      <div className="mb-4 flex border-b border-gray-200" role="tablist">
        <button role="tab" aria-selected={tab === "articles"} className={tabCls("articles")} onClick={() => setTab("articles")}>
          News articles
        </button>
        <button role="tab" aria-selected={tab === "pages"} className={tabCls("pages")} onClick={() => setTab("pages")}>
          Site pages
        </button>
      </div>
      {tab === "articles" ? <Articles /> : <Pages />}
    </>
  );
}

function Articles() {
  const { call } = useAdmin();
  const [q, setQ] = useState("");
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("all");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);
  const [editing, setEditing] = useState<number | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);
  const { ok, fail, node } = useNotice();

  useEffect(() => {
    const t = setTimeout(() => {
      setQuery(q.trim());
      setPage(1);
    }, 350);
    return () => clearTimeout(t);
  }, [q]);

  const list = useLoad(
    () => call<List>("GET", `/articles?page=${page}&page_size=25&status=${status}${category ? `&category=${category}` : ""}${query ? `&q=${encodeURIComponent(query)}` : ""}`),
    [page, status, category, query]
  );

  async function act(row: Row, action: "publish" | "unpublish" | "restore" | "delete") {
    if (action === "delete" && !confirm(`Delete “${row.title}”?\n\nIt disappears from the site immediately. You can restore it later from the Deleted filter.`)) return;
    setBusyId(row.id);
    try {
      if (action === "delete") await call("DELETE", `/articles/${row.id}`);
      else await call("POST", `/articles/${row.id}/${action}`);
      ok(`Article ${action === "delete" ? "deleted" : action === "restore" ? "restored as an unpublished draft" : action + "ed"}.`);
      list.reload();
    } catch (e) {
      fail(e);
    } finally {
      setBusyId(null);
    }
  }

  const d = list.data;
  return (
    <div className="space-y-4">
      {node}
      <div className="flex flex-wrap gap-2">
        <Input placeholder="Search title, source or ID…" value={q} onChange={(e) => setQ(e.target.value)} className="!w-64" aria-label="Search" />
        <Select value={status} onChange={(e) => { setStatus(e.target.value); setPage(1); }} className="!w-40" aria-label="Status">
          <option value="all">All (not deleted)</option>
          <option value="published">Published</option>
          <option value="unpublished">Unpublished</option>
          <option value="deleted">Deleted</option>
        </Select>
        <Select value={category} onChange={(e) => { setCategory(e.target.value); setPage(1); }} className="!w-40" aria-label="Category">
          <option value="">All categories</option>
          {(d?.categories ?? []).map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </Select>
        {d && <span className="self-center text-sm text-gray-500">{d.total.toLocaleString()} articles</span>}
      </div>
      {list.error && <Alert>{list.error}</Alert>}
      <Card className="!p-0">
        {list.loading && !d ? (
          <div className="p-4"><Spinner /></div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-sm">
              <thead>
                <tr className="bg-gray-50 text-left text-xs text-gray-500">
                  {["Article", "Category", "Published", "Status", ""].map((h) => (
                    <th key={h} className="px-4 py-2 font-medium">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className={list.loading ? "opacity-50" : ""}>
                {d?.items.map((r) => (
                  <tr key={r.id} className="border-t border-gray-100 align-top">
                    <td className="max-w-md px-4 py-2.5">
                      <button className="text-left font-medium text-gray-900 hover:text-blue-700" onClick={() => setEditing(r.id)}>
                        {r.title}
                      </button>
                      <div className="text-xs text-gray-500">#{r.id} · {r.source}{r.edited_by ? ` · edited by ${r.edited_by}` : ""}{!r.has_image ? " · no image" : ""}</div>
                    </td>
                    <td className="px-4 py-2.5 capitalize">{r.category}</td>
                    <td className="whitespace-nowrap px-4 py-2.5">{fmtDate(r.published_at, false)}</td>
                    <td className="px-4 py-2.5"><Badge tone={STATUS_TONE[r.status]}>{r.status}</Badge></td>
                    <td className="whitespace-nowrap px-4 py-2.5 text-right">
                      <div className="flex justify-end gap-1">
                        {r.status !== "deleted" && <Button small onClick={() => setEditing(r.id)}>Edit</Button>}
                        {r.status === "published" && <Button small busy={busyId === r.id} onClick={() => act(r, "unpublish")}>Unpublish</Button>}
                        {r.status === "unpublished" && <Button small tone="primary" busy={busyId === r.id} onClick={() => act(r, "publish")}>Publish</Button>}
                        {r.status === "deleted" ? (
                          <Button small busy={busyId === r.id} onClick={() => act(r, "restore")}>Restore</Button>
                        ) : (
                          <Button small tone="ghost" className="!text-red-700 hover:!bg-red-50" busy={busyId === r.id} onClick={() => act(r, "delete")}>Delete</Button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
                {d?.items.length === 0 && (
                  <tr><td colSpan={5} className="px-4 py-8 text-center text-gray-500">No articles match.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </Card>
      {d && d.total_pages > 1 && (
        <div className="flex items-center justify-center gap-3 text-sm">
          <Button small disabled={page <= 1} onClick={() => setPage(page - 1)}>← Prev</Button>
          <span className="text-gray-600">Page {page} of {d.total_pages}</span>
          <Button small disabled={page >= d.total_pages} onClick={() => setPage(page + 1)}>Next →</Button>
        </div>
      )}
      {editing !== null && (
        <ArticleEditor
          id={editing}
          categories={d?.categories ?? []}
          onClose={() => setEditing(null)}
          onSaved={() => { setEditing(null); ok("Article saved."); list.reload(); }}
        />
      )}
    </div>
  );
}

function ArticleEditor({ id, categories, onClose, onSaved }: { id: number; categories: string[]; onClose: () => void; onSaved: () => void }) {
  const { call } = useAdmin();
  const detail = useLoad(() => call<Detail>("GET", `/articles/${id}`), [id]);
  const [form, setForm] = useState<Detail | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (detail.data) setForm(detail.data);
  }, [detail.data]);

  const set = <K extends keyof Detail>(k: K, v: Detail[K]) => setForm((f) => (f ? { ...f, [k]: v } : f));

  async function save() {
    if (!form) return;
    setSaving(true);
    setError(null);
    try {
      await call("PATCH", `/articles/${id}`, {
        title: form.title,
        summary: form.summary ?? "",
        description: form.description ?? "",
        body_text: form.body_text,
        category: form.category,
        image_url: form.image_url ?? "",
        image_credit: form.image_credit ?? "",
        meta_title: form.meta_title ?? "",
        meta_description: form.meta_description ?? "",
        is_published: form.status !== "unpublished",
      });
      onSaved();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save");
      setSaving(false);
    }
  }

  return (
    <Modal title={`Edit article #${id}`} onClose={onClose} wide>
      {detail.error && <Alert>{detail.error}</Alert>}
      {!form ? (
        <Spinner />
      ) : (
        <div className="space-y-4">
          {error && <Alert>{error}</Alert>}
          <Field label="Headline"><Input value={form.title} maxLength={500} onChange={(e) => set("title", e.target.value)} /></Field>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Category">
              <Select value={form.category} onChange={(e) => set("category", e.target.value)}>
                {categories.map((c) => <option key={c} value={c}>{c}</option>)}
              </Select>
            </Field>
            <Field label="Visibility">
              <Select value={form.status === "unpublished" ? "no" : "yes"} onChange={(e) => set("status", e.target.value === "yes" ? "published" : "unpublished")}>
                <option value="yes">Published</option>
                <option value="no">Unpublished (hidden from the site)</option>
              </Select>
            </Field>
          </div>
          <Field label="Summary" hint="Shown on cards and used in search results unless a meta description is set.">
            <Textarea rows={3} value={form.summary ?? ""} onChange={(e) => set("summary", e.target.value)} />
          </Field>
          <Field label="Article text" hint="Separate paragraphs with a blank line.">
            <Textarea rows={10} value={form.body_text} onChange={(e) => set("body_text", e.target.value)} />
          </Field>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Image URL"><Input value={form.image_url ?? ""} placeholder="https://…" onChange={(e) => set("image_url", e.target.value)} /></Field>
            <Field label="Image credit"><Input value={form.image_credit ?? ""} onChange={(e) => set("image_credit", e.target.value)} /></Field>
          </div>
          <div className="rounded-lg bg-gray-50 p-3">
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">Search engines</p>
            <div className="space-y-3">
              <Field label="Page title" hint={`${(form.meta_title ?? "").length}/200 · leave empty to use the headline`}>
                <Input value={form.meta_title ?? ""} maxLength={200} onChange={(e) => set("meta_title", e.target.value)} />
              </Field>
              <Field label="Meta description" hint={`${(form.meta_description ?? "").length}/320 · about 150 characters displays best`}>
                <Textarea rows={2} value={form.meta_description ?? ""} maxLength={320} onChange={(e) => set("meta_description", e.target.value)} />
              </Field>
            </div>
          </div>
          <p className="text-xs text-gray-500">
            Source: <a href={form.url} target="_blank" rel="noopener noreferrer" className="text-blue-700 hover:underline">{form.source} ↗</a>
          </p>
          <div className="flex justify-end gap-2">
            <Button onClick={onClose}>Cancel</Button>
            <Button tone="primary" busy={saving} onClick={save}>Save changes</Button>
          </div>
        </div>
      )}
    </Modal>
  );
}

function Pages() {
  const { call, user } = useAdmin();
  const list = useLoad(() => call<{ items: SitePage[] }>("GET", "/pages"), []);
  const [editing, setEditing] = useState<SitePage | "new" | null>(null);
  const { ok, fail, node } = useNotice();

  async function remove(p: SitePage) {
    if (!confirm(`Permanently delete the page “${p.title}”?`)) return;
    try {
      await call("DELETE", `/pages/${p.id}`);
      ok("Page deleted.");
      list.reload();
    } catch (e) {
      fail(e);
    }
  }

  return (
    <div className="space-y-4">
      {node}
      <div className="flex justify-end"><Button tone="primary" onClick={() => setEditing("new")}>New page</Button></div>
      {list.error && <Alert>{list.error}</Alert>}
      <Card className="!p-0">
        {!list.data ? <div className="p-4"><Spinner /></div> : (
          <table className="w-full text-sm">
            <thead><tr className="bg-gray-50 text-left text-xs text-gray-500">
              {["Page", "Address", "Status", "Updated", ""].map((h) => <th key={h} className="px-4 py-2 font-medium">{h}</th>)}
            </tr></thead>
            <tbody>
              {list.data.items.map((p) => (
                <tr key={p.id} className="border-t border-gray-100">
                  <td className="px-4 py-2.5 font-medium text-gray-900">{p.title}</td>
                  <td className="px-4 py-2.5"><a href={`/p/${p.slug}`} target="_blank" className="text-blue-700 hover:underline">/p/{p.slug}</a></td>
                  <td className="px-4 py-2.5"><Badge tone={p.is_published ? "green" : "amber"}>{p.is_published ? "published" : "draft"}</Badge></td>
                  <td className="px-4 py-2.5 text-xs text-gray-500">{fmtDate(p.updated_at)}{p.updated_by ? ` · ${p.updated_by}` : ""}</td>
                  <td className="px-4 py-2.5 text-right">
                    <div className="flex justify-end gap-1">
                      <Button small onClick={() => setEditing(p)}>Edit</Button>
                      {user.role === "admin" && <Button small tone="ghost" className="!text-red-700 hover:!bg-red-50" onClick={() => remove(p)}>Delete</Button>}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
      {editing && (
        <PageEditor
          page={editing === "new" ? null : editing}
          onClose={() => setEditing(null)}
          onSaved={() => { setEditing(null); ok("Page saved."); list.reload(); }}
        />
      )}
    </div>
  );
}

function PageEditor({ page, onClose, onSaved }: { page: SitePage | null; onClose: () => void; onSaved: () => void }) {
  const { call } = useAdmin();
  const [f, setF] = useState({
    slug: page?.slug ?? "",
    title: page?.title ?? "",
    body: page?.body ?? "",
    meta_description: page?.meta_description ?? "",
    is_published: page?.is_published ?? true,
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function save() {
    setSaving(true);
    setError(null);
    try {
      const body = { ...f, meta_description: f.meta_description || null };
      if (page) await call("PATCH", `/pages/${page.id}`, body);
      else await call("POST", "/pages", body);
      onSaved();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save");
      setSaving(false);
    }
  }

  return (
    <Modal title={page ? `Edit page: ${page.title}` : "New page"} onClose={onClose} wide>
      <div className="space-y-4">
        {error && <Alert>{error}</Alert>}
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Title"><Input value={f.title} maxLength={200} onChange={(e) => setF({ ...f, title: e.target.value })} /></Field>
          <Field label="Address" hint="Lowercase letters, numbers and hyphens. Shown as /p/…">
            <Input value={f.slug} maxLength={80} onChange={(e) => setF({ ...f, slug: e.target.value.toLowerCase() })} />
          </Field>
        </div>
        <Field label="Text" hint="Blank line = new paragraph. Start a line with “## ” for a heading.">
          <Textarea rows={12} value={f.body} onChange={(e) => setF({ ...f, body: e.target.value })} />
        </Field>
        <Field label="Meta description" hint={`${f.meta_description.length}/320`}>
          <Textarea rows={2} maxLength={320} value={f.meta_description} onChange={(e) => setF({ ...f, meta_description: e.target.value })} />
        </Field>
        <Toggle label="Published" checked={f.is_published} onChange={(v) => setF({ ...f, is_published: v })} />
        <div className="flex justify-end gap-2">
          <Button onClick={onClose}>Cancel</Button>
          <Button tone="primary" busy={saving} onClick={save}>Save page</Button>
        </div>
      </div>
    </Modal>
  );
}
