const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BASE = `${API_URL}/api/v1/news`;

export interface Article {
  id: number;
  title: string;
  url: string;
  source: { key: string; name: string; country: string; type: string };
  image_url: string | null;
  image_source: "publisher" | "page" | "wikimedia" | null;
  image_credit: string | null;
  image_credit_url: string | null;
  summary: string | null;
  description: string | null;
  category: string;
  keywords: string[];
  published_at: string;
  is_featured: boolean;
  validation: { status: "passed" | "unverified" | "flagged"; score: number; flags: string[]; review_status: string };
}

export interface ArticleDetail extends Article {
  body: string[];
  people: string[];
  organizations: string[];
  locations: string[];
  topics: string[];
  modified_at: string | null;
  meta_title: string | null;
  meta_description: string | null;
}

export interface Location {
  country: string;
  country_name: string;
  source: string;
  has_local_sources: boolean;
}

export interface ArticlePage {
  items: Article[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  location?: Location;
}

export interface Params {
  page?: number;
  page_size?: number;
  category?: string;
  country?: string;
  scope?: "all" | "local";
  source?: string;
  q?: string;
  sort?: "latest" | "trending";
}

async function get<T>(path: string, params: Record<string, string | number | undefined> = {}, signal?: AbortSignal): Promise<T> {
  const qs = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== "" && v !== null) qs.set(k, String(v));
  });
  const res = await fetch(`${BASE}${path}${qs.toString() ? `?${qs}` : ""}`, { signal });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      /* non-JSON error body */
    }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

export const newsApi = {
  articles: (p: Params, signal?: AbortSignal) => get<ArticlePage>("/articles", p as Record<string, string | number>, signal),
  featured: (country?: string) => get<{ items: Article[]; location: Location }>("/featured", { country }),
  trending: (country?: string) => get<ArticlePage>("/trending", { country, limit: 6 }),
  categories: (country?: string, scope?: string) =>
    get<{ categories: { category: string; count: number }[] }>("/categories", { country, scope }),
  countries: () => get<{ countries: { code: string; name: string; sources: number }[] }>("/countries"),
  sources: () =>
    get<{ sources: { key: string; name: string; country: string; articles: number; kind: string }[] }>("/sources"),
  article: (id: number) => get<ArticleDetail>(`/articles/${id}`),
  related: (id: number) => get<{ items: Article[] }>(`/articles/${id}/related`),
  location: (country?: string) => get<Location>("/location", { country }),
  click: (id: number) => fetch(`${BASE}/articles/${id}/click`, { method: "POST", keepalive: true }).catch(() => undefined),
};

export function timeAgo(iso: string): string {
  const diff = Math.max(0, Date.now() - new Date(iso).getTime());
  const m = Math.floor(diff / 60000);
  if (m < 1) return "just now";
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  if (d < 7) return `${d}d ago`;
  return new Date(iso).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
}
