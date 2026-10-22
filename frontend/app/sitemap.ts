import type { MetadataRoute } from "next";
import { articlePath } from "./news/slug";
import { SITE_URL, apiGet } from "./server";

export const dynamic = "force-dynamic";

interface SitemapData {
  articles: { id: number; title: string; modified: string }[];
  pages: { slug: string; modified: string | null }[];
  categories: string[];
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const data = await apiGet<SitemapData>("/site/sitemap");
  const entries: MetadataRoute.Sitemap = [{ url: `${SITE_URL}/`, changeFrequency: "hourly", priority: 1 }];
  if (!data) return entries;
  for (const c of data.categories) entries.push({ url: `${SITE_URL}/category/${c}`, changeFrequency: "hourly", priority: 0.6 });
  for (const p of data.pages)
    entries.push({ url: `${SITE_URL}/p/${p.slug}`, lastModified: p.modified ?? undefined, changeFrequency: "monthly", priority: 0.3 });
  for (const a of data.articles)
    entries.push({
      url: `${SITE_URL}${articlePath(a)}`,
      lastModified: a.modified,
      changeFrequency: "weekly",
      priority: 0.7,
    });
  return entries;
}
