import type { Article, ArticlePage, Location } from "./news/api";
import NewsPage, { InitialNews } from "./news/NewsPage";
import SiteFooter from "./SiteFooter";
import { apiGet, getSettings, SITE_URL } from "./server";

export const dynamic = "force-dynamic";

export default async function Home() {
  const [articles, featured, trending, categories, settings] = await Promise.all([
    apiGet<ArticlePage>("/news/articles?page=1&page_size=12", { forwardClient: true }),
    apiGet<{ items: Article[]; location: Location }>("/news/featured", { forwardClient: true }),
    apiGet<ArticlePage>("/news/trending?limit=6", { forwardClient: true }),
    apiGet<{ categories: { category: string; count: number }[] }>("/news/categories", { forwardClient: true }),
    getSettings(),
  ]);
  const location = articles?.location ?? featured?.location;
  const initial: InitialNews | undefined =
    articles && location
      ? {
          location,
          articles,
          featured: featured?.items ?? [],
          trending: trending?.items ?? [],
          categories: categories?.categories ?? [],
        }
      : undefined; // API down: the page still loads and fetches in the browser

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: settings.site_name,
    url: SITE_URL,
    description: settings.site_description,
  };
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      <NewsPage initial={initial} />
      <SiteFooter name={settings.site_name} />
    </>
  );
}
