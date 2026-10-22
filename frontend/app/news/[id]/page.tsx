import { cache } from "react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound, permanentRedirect } from "next/navigation";
import AdSlot from "../../AdSlot";
import SiteFooter from "../../SiteFooter";
import { SITE_URL, apiGet, getSettings } from "../../server";
import type { Article, ArticleDetail } from "../api";
import { ArticleCard, CategoryBadge, ValidationBadge } from "../components";
import { articlePath } from "../slug";
import { ArticleImage, ClickBeacon } from "./client";

export const dynamic = "force-dynamic";

const loadArticle = cache((id: number) => apiGet<ArticleDetail>(`/news/articles/${id}`));

function parseId(raw: string): number | null {
  const m = /^(\d{1,9})(?:-|$)/.exec(decodeURIComponent(raw));
  return m ? Number(m[1]) : null;
}

const trim = (text: string, max: number) => {
  const flat = text.replace(/\s+/g, " ").trim();
  return flat.length <= max ? flat : `${flat.slice(0, max - 1).replace(/\s+\S*$/, "")}…`;
};

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const id = parseId((await params).id);
  const article = id ? await loadArticle(id) : null;
  if (!article) return { title: "Article not found", robots: { index: false, follow: false } };
  const description = trim(article.meta_description || article.summary || article.body[0] || article.title, 160);
  const title = article.meta_title || article.title;
  const path = articlePath(article);
  return {
    title,
    description,
    alternates: { canonical: path },
    openGraph: {
      type: "article",
      title,
      description,
      url: path,
      publishedTime: article.published_at,
      modifiedTime: article.modified_at ?? undefined,
      section: article.category,
      tags: article.keywords.slice(0, 8),
      images: article.image_url ? [{ url: article.image_url, alt: article.title }] : undefined,
    },
    twitter: { card: article.image_url ? "summary_large_image" : "summary", title, description },
  };
}

export default async function ArticlePage({ params }: { params: Promise<{ id: string }> }) {
  const raw = (await params).id;
  const id = parseId(raw);
  if (!id) notFound();
  const [article, relatedData, settings] = await Promise.all([
    loadArticle(id),
    apiGet<{ items: Article[] }>(`/news/articles/${id}/related`),
    getSettings(),
  ]);
  if (!article) notFound();
  const canonical = articlePath(article);
  if (decodeURIComponent(raw) !== canonical.replace("/news/", "")) permanentRedirect(canonical);

  const related = relatedData?.items ?? [];
  const teaserOnly = article.body.join(" ").length < 600;
  const published = new Date(article.published_at);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: article.title.slice(0, 110),
    description: trim(article.summary || article.body[0] || article.title, 200),
    datePublished: article.published_at,
    dateModified: article.modified_at ?? article.published_at,
    mainEntityOfPage: { "@type": "WebPage", "@id": `${SITE_URL}${canonical}` },
    image: article.image_url ? [article.image_url] : undefined,
    articleSection: article.category,
    keywords: article.keywords.slice(0, 8).join(", "),
    publisher: { "@type": "Organization", name: settings.site_name, url: SITE_URL },
  };
  const breadcrumbs = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: `${SITE_URL}/` },
      { "@type": "ListItem", position: 2, name: article.category, item: `${SITE_URL}/category/${article.category}` },
      { "@type": "ListItem", position: 3, name: article.title, item: `${SITE_URL}${canonical}` },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbs).replace(/</g, "\\u003c") }} />
      <ClickBeacon id={article.id} />
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
          <Link href="/" className="text-lg font-bold text-gray-900">
            {settings.site_name}
          </Link>
          <Link href="/" className="text-sm font-medium text-blue-700 hover:underline">
            ← All news
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-4xl space-y-8 px-4 py-6">
        <article className="space-y-5">
          <nav aria-label="Breadcrumb" className="text-xs text-gray-500">
            <Link href="/" className="hover:underline">
              Home
            </Link>
            {" / "}
            <Link href={`/category/${article.category}`} className="capitalize hover:underline">
              {article.category}
            </Link>
          </nav>
          <div className="flex flex-wrap items-center gap-2">
            <CategoryBadge category={article.category} />
            <ValidationBadge article={article} />
          </div>
          <h1 className="text-2xl font-bold leading-tight text-gray-900 sm:text-4xl">{article.title}</h1>
          <p className="text-sm text-gray-600">
            <time dateTime={article.published_at}>
              {published.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" })}
            </time>
          </p>

          <ArticleImage
            title={article.title}
            category={article.category}
            image_url={article.image_url}
            image_source={article.image_source}
            image_credit={article.image_credit}
          />

          <AdSlot placement="article_top" />

          {article.summary && !teaserOnly && (
            <p className="rounded-lg border-l-4 border-blue-600 bg-blue-50 px-4 py-3 text-base font-medium text-gray-800">
              {article.summary}
            </p>
          )}

          <div className="space-y-4 text-base leading-relaxed text-gray-800">
            {article.body.length > 0 ? (
              article.body.map((p, i) => (
                <div key={i} className="space-y-4">
                  <p>{p}</p>
                  {i === 1 && article.body.length > 3 && <AdSlot placement="article_inline" />}
                </div>
              ))
            ) : (
              <p>{article.summary ?? "No article text is available for this story."}</p>
            )}
          </div>

          {article.keywords.length > 0 && (
            <ul className="flex flex-wrap gap-2" aria-label="Topics">
              {article.keywords.slice(0, 8).map((k) => (
                <li key={k} className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-600">
                  {k}
                </li>
              ))}
            </ul>
          )}

          <AdSlot placement="article_bottom" />

          <footer className="rounded-xl border border-gray-200 bg-white p-4 text-sm text-gray-600">
            <p>{teaserOnly ? "This is an excerpt." : "Summaries and tags are generated automatically."}</p>
          </footer>
        </article>

        <section aria-label="Related news" className="space-y-4">
          <h2 className="text-lg font-bold text-gray-900">Related news</h2>
          {related.length === 0 ? (
            <p className="text-sm text-gray-500">No related stories yet.</p>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {related.map((r) => (
                <ArticleCard key={r.id} article={r} />
              ))}
            </div>
          )}
        </section>
      </main>
      <SiteFooter name={settings.site_name} />
    </div>
  );
}
