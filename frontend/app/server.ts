import { headers } from "next/headers";

/** Where server components reach the API (the Docker service name inside Compose). */
export const INTERNAL_API = process.env["INTERNAL_API_URL"] || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8100";
export const SITE_URL = (process.env["SITE_URL"] || process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3100").replace(/\/$/, "");

export interface SiteSettings {
  site_name: string;
  site_tagline: string;
  site_description: string;
  default_og_image: string;
  twitter_handle: string;
  contact_email: string;
}

export const DEFAULT_SETTINGS: SiteSettings = {
  site_name: "VidiaNews",
  site_tagline: "News from trusted sources, in one place",
  site_description: "Headlines and summaries from newspapers and broadcasters, organised by topic and country.",
  default_og_image: "",
  twitter_handle: "",
  contact_email: "",
};

/** GET from the API on the server. Returns null on 404 or any failure so pages can degrade. */
export async function apiGet<T>(path: string, opts: { forwardClient?: boolean } = {}): Promise<T | null> {
  const h: Record<string, string> = {};
  if (opts.forwardClient) {
    const incoming = await headers();
    for (const k of ["x-forwarded-for", "x-real-ip", "accept-language"]) {
      const v = incoming.get(k);
      if (v) h[k] = v;
    }
  }
  try {
    const res = await fetch(`${INTERNAL_API}/api/v1${path}`, { cache: "no-store", headers: h });
    return res.ok ? ((await res.json()) as T) : null;
  } catch {
    return null;
  }
}

export async function getSettings(): Promise<SiteSettings> {
  return { ...DEFAULT_SETTINGS, ...((await apiGet<SiteSettings>("/site/settings")) ?? {}) };
}

export { slugify } from "./news/slug";
