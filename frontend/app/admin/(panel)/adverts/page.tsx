"use client";

import { useRef, useState } from "react";
import { fmtDate, fmtNum, useAdmin } from "../../lib";
import { Alert, Badge, Button, Card, Field, Input, Modal, PageTitle, Select, Spinner, Toggle, useLoad, useNotice } from "../../ui";

interface Advert {
  advert_id: string;
  name: string;
  image_url: string;
  image_src: string;
  destination_url: string;
  alt_text: string;
  placements: string[];
  is_active: boolean;
  starts_at: string | null;
  ends_at: string | null;
  weight: number;
  impressions: number;
  clicks: number;
  ctr: number;
  state: "live" | "scheduled" | "expired" | "inactive";
}
type Placements = { placements: { key: string; label: string }[] };

const STATE_TONE = { live: "green", scheduled: "blue", expired: "gray", inactive: "amber" } as const;

/** <input type=datetime-local> works in local time; the API stores UTC. */
const toLocalInput = (iso: string | null) => {
  if (!iso) return "";
  const d = new Date(iso);
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
};
const fromLocalInput = (v: string) => (v ? new Date(v).toISOString() : null);

export default function AdvertsPage() {
  const { call } = useAdmin();
  const [state, setState] = useState("");
  const [q, setQ] = useState("");
  const list = useLoad(() => call<{ items: Advert[] }>("GET", `/ads?${state ? `state=${state}&` : ""}${q ? `q=${encodeURIComponent(q)}` : ""}`), [state, q]);
  const places = useLoad(() => call<Placements>("GET", "/ads/placements"), []);
  const [editing, setEditing] = useState<Advert | "new" | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const { ok, fail, node } = useNotice();
  const label = (k: string) => places.data?.placements.find((p) => p.key === k)?.label ?? k;

  async function toggle(ad: Advert) {
    setBusy(ad.advert_id);
    try {
      await call("PATCH", `/ads/${ad.advert_id}`, { is_active: !ad.is_active });
      ok(`${ad.advert_id} ${ad.is_active ? "deactivated" : "activated"}.`);
      list.reload();
    } catch (e) {
      fail(e);
    } finally {
      setBusy(null);
    }
  }
  async function remove(ad: Advert) {
    if (!confirm(`Delete advert ${ad.advert_id} “${ad.name}”?\nIts ${fmtNum(ad.impressions)} impressions and ${fmtNum(ad.clicks)} clicks are deleted with it.`)) return;
    try {
      await call("DELETE", `/ads/${ad.advert_id}`);
      ok("Advert deleted.");
      list.reload();
    } catch (e) {
      fail(e);
    }
  }

  return (
    <>
      <PageTitle title="Adverts" hint="Image adverts shown in the slots you choose, for as long as you schedule them." actions={<Button tone="primary" onClick={() => setEditing("new")}>New advert</Button>} />
      {node}
      <div className="my-4 flex flex-wrap gap-2">
        <Input placeholder="Search by Advert ID or name…" value={q} onChange={(e) => setQ(e.target.value)} className="!w-64" aria-label="Search adverts" />
        <Select value={state} onChange={(e) => setState(e.target.value)} className="!w-40" aria-label="State">
          <option value="">All states</option>
          <option value="live">Live</option>
          <option value="scheduled">Scheduled</option>
          <option value="expired">Expired</option>
          <option value="inactive">Inactive</option>
        </Select>
      </div>
      {list.error && <Alert>{list.error}</Alert>}
      {!list.data ? (
        <Spinner />
      ) : list.data.items.length === 0 ? (
        <Card><p className="py-6 text-center text-sm text-gray-500">No adverts {state || q ? "match" : "yet"}. Create one to start showing it on the site.</p></Card>
      ) : (
        <div className="grid gap-4 lg:grid-cols-2">
          {list.data.items.map((ad) => (
            <Card key={ad.advert_id}>
              <div className="flex gap-4">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={ad.image_src} alt={ad.alt_text} className="h-24 w-32 flex-none rounded-lg border border-gray-200 bg-gray-50 object-contain" />
                <div className="min-w-0 flex-1 space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="truncate font-semibold text-gray-900">{ad.name}</h3>
                    <Badge tone={STATE_TONE[ad.state]}>{ad.state}</Badge>
                  </div>
                  <p className="font-mono text-xs text-gray-500">{ad.advert_id}</p>
                  <a href={ad.destination_url} target="_blank" rel="noopener noreferrer nofollow" className="block truncate text-xs text-blue-700 hover:underline">{ad.destination_url}</a>
                  <p className="text-xs text-gray-600">{ad.placements.map(label).join(" · ")}</p>
                  <p className="text-xs text-gray-500">
                    {ad.starts_at ? `From ${fmtDate(ad.starts_at)}` : "Starts immediately"} — {ad.ends_at ? `until ${fmtDate(ad.ends_at)}` : "no end date"}
                  </p>
                </div>
              </div>
              <div className="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-gray-100 pt-3">
                <p className="text-xs text-gray-600">
                  <strong>{fmtNum(ad.impressions)}</strong> impressions · <strong>{fmtNum(ad.clicks)}</strong> clicks · {ad.ctr}% CTR
                </p>
                <div className="flex gap-1">
                  <Button small onClick={() => setEditing(ad)}>Edit</Button>
                  <Button small busy={busy === ad.advert_id} onClick={() => toggle(ad)}>{ad.is_active ? "Deactivate" : "Activate"}</Button>
                  <Button small tone="ghost" className="!text-red-700 hover:!bg-red-50" onClick={() => remove(ad)}>Delete</Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
      {editing && (
        <AdvertEditor
          ad={editing === "new" ? null : editing}
          placements={places.data?.placements ?? []}
          onClose={() => setEditing(null)}
          onSaved={(msg) => { setEditing(null); ok(msg); list.reload(); }}
        />
      )}
    </>
  );
}

function AdvertEditor({ ad, placements, onClose, onSaved }: { ad: Advert | null; placements: { key: string; label: string }[]; onClose: () => void; onSaved: (msg: string) => void }) {
  const { call, upload } = useAdmin();
  const [f, setF] = useState({
    name: ad?.name ?? "",
    image_url: ad?.image_url ?? "",
    image_src: ad?.image_src ?? "",
    destination_url: ad?.destination_url ?? "",
    alt_text: ad?.alt_text ?? "",
    placements: ad?.placements ?? [],
    is_active: ad?.is_active ?? true,
    starts_at: toLocalInput(ad?.starts_at ?? null),
    ends_at: toLocalInput(ad?.ends_at ?? null),
    weight: ad?.weight ?? 1,
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  async function pickFile(file: File | undefined) {
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      const r = await upload<{ image_url: string; image_src: string }>("/ads/upload", file);
      setF((s) => ({ ...s, image_url: r.image_url, image_src: r.image_src }));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  }

  async function save() {
    setSaving(true);
    setError(null);
    const body = {
      name: f.name,
      image_url: f.image_url,
      destination_url: f.destination_url,
      alt_text: f.alt_text,
      placements: f.placements,
      is_active: f.is_active,
      starts_at: fromLocalInput(f.starts_at),
      ends_at: fromLocalInput(f.ends_at),
      weight: Number(f.weight) || 1,
    };
    try {
      if (ad) {
        await call("PATCH", `/ads/${ad.advert_id}`, body);
        onSaved(`Advert ${ad.advert_id} updated.`);
      } else {
        const created = await call<Advert>("POST", "/ads", body);
        onSaved(`Advert created with ID ${created.advert_id}.`);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save");
      setSaving(false);
    }
  }

  const togglePlacement = (key: string) =>
    setF((s) => ({ ...s, placements: s.placements.includes(key) ? s.placements.filter((p) => p !== key) : [...s.placements, key] }));

  return (
    <Modal title={ad ? `Edit advert ${ad.advert_id}` : "New advert"} onClose={onClose} wide>
      <div className="space-y-4">
        {error && <Alert>{error}</Alert>}
        <Field label="Name" hint="For your own reference."><Input value={f.name} maxLength={160} onChange={(e) => setF({ ...f, name: e.target.value })} /></Field>

        <div className="space-y-2">
          <span className="text-xs font-medium text-gray-700">Image</span>
          <div className="flex flex-wrap items-center gap-3">
            {f.image_src && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={f.image_src} alt="Preview" className="h-20 w-auto max-w-[12rem] rounded-lg border border-gray-200 object-contain" />
            )}
            <input ref={fileRef} type="file" accept="image/png,image/jpeg,image/gif,image/webp" className="hidden" onChange={(e) => pickFile(e.target.files?.[0])} />
            <Button busy={uploading} onClick={() => fileRef.current?.click()}>{f.image_url ? "Replace image" : "Upload image"}</Button>
            <span className="text-xs text-gray-500">PNG, JPEG, GIF or WebP, up to 2 MB</span>
          </div>
          <Field label="…or an image address (https)">
            <Input value={f.image_url.startsWith("/media/") ? "" : f.image_url} placeholder="https://…" onChange={(e) => setF({ ...f, image_url: e.target.value, image_src: e.target.value })} />
          </Field>
        </div>

        <Field label="Destination URL" hint="Where a click on the advert goes."><Input type="url" value={f.destination_url} placeholder="https://…" onChange={(e) => setF({ ...f, destination_url: e.target.value })} /></Field>
        <Field label="Image description" hint="Read aloud by screen readers."><Input value={f.alt_text} maxLength={200} onChange={(e) => setF({ ...f, alt_text: e.target.value })} /></Field>

        <fieldset>
          <legend className="mb-1 text-xs font-medium text-gray-700">Where it appears</legend>
          <div className="grid gap-1.5 sm:grid-cols-2">
            {placements.map((p) => (
              <Toggle key={p.key} label={p.label} checked={f.placements.includes(p.key)} onChange={() => togglePlacement(p.key)} />
            ))}
          </div>
        </fieldset>

        <div className="grid gap-4 sm:grid-cols-3">
          <Field label="Starts" hint="Empty = immediately"><Input type="datetime-local" value={f.starts_at} onChange={(e) => setF({ ...f, starts_at: e.target.value })} /></Field>
          <Field label="Ends" hint="Empty = never"><Input type="datetime-local" value={f.ends_at} onChange={(e) => setF({ ...f, ends_at: e.target.value })} /></Field>
          <Field label="Weight (1–10)" hint="Higher = shown more often when slots compete"><Input type="number" min={1} max={10} value={f.weight} onChange={(e) => setF({ ...f, weight: Number(e.target.value) })} /></Field>
        </div>
        <Toggle label="Active" checked={f.is_active} onChange={(v) => setF({ ...f, is_active: v })} />

        <div className="flex justify-end gap-2">
          <Button onClick={onClose}>Cancel</Button>
          <Button tone="primary" busy={saving} onClick={save}>{ad ? "Save changes" : "Create advert"}</Button>
        </div>
      </div>
    </Modal>
  );
}
