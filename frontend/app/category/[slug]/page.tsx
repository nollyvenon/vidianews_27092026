import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import AdSlot from "../../AdSlot";
import SiteFooter from "../../SiteFooter";
import type { ArticlePage } from "../../news/api";
import { ArticleCard } from "../../news/components";
import { SITE_URL, apiGet, getSettings } from "../../server";

export const dynamic = "force-dynamic";

const PAGE_SIZE = 24;
const valid = (slug: string) => /^[a-z]{3,20}$/.test(slug);
const label = (slug: string) => slug.charAt(0).toUpperCase() + slug.slice(1);

type Props = { params: Promise<{ slug: string }>; searchParams: Promise<{ page?: string }> };

export async function generateMetadata({ params, searchParams }: Props): Promise<Metadata> {
  const { slug } = await params;
  const page = Math.max(1, Number((await searchParams).page) || 1);
  const s = await getSettings();
  const title = `${label(slug)} news`;
  const description = `The latest ${slug} news and headlines from trusted publishers, on ${s.site_name}.`;
  return {
    title,
    description,
    alternates: { canonical: page > 1 ? `/category/${slug}?page=${page}` : `/category/${slug}` },
    openGraph: { type: "website", title, description, url: `/category/${slug}` },
  };
}

export default async function CategoryPage({ params, searchParams }: Props) {
  const { slug } = await params;
  if (!valid(slug)) notFound();
  const page = Math.max(1, Math.min(500, Number((await searchParams).page) || 1));
  const [data, settings] = await Promise.all([
    apiGet<ArticlePage>(`/news/articles?category=${slug}&page=${page}&page_size=${PAGE_SIZE}`, { forwardClient: true }),
    getSettings(),
  ]);
  if (!data || (data.total === 0 && page === 1)) notFound();

  const crumbs = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: `${SITE_URL}/` },
      { "@type": "ListItem", position: 2, name: label(slug), item: `${SITE_URL}/category/${slug}` },
    ],
  };
  const link = "rounded-md border border-gray-300 px-3 py-1.5 text-sm hover:bg-gray-50";
  return (
    <div className="min-h-screen bg-gray-50">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(crumbs) }} />
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
          <Link href="/" className="text-lg font-bold text-gray-900">
            {settings.site_name}
          </Link>
          <Link href="/" className="text-sm font-medium text-blue-700 hover:underline">
            ← All news
          </Link>
        </div>
      </header>
      <main className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-bold capitalize text-gray-900">{slug} news</h1>
        <AdSlot placement="category_top" />
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {data.items.map((a) => (
            <ArticleCard key={a.id} article={a} />
          ))}
        </div>
        <nav aria-label="Pagination" className="flex items-center justify-center gap-3">
          {page > 1 && (
            <Link className={link} href={`/category/${slug}?page=${page - 1}`} rel="prev">
              ← Newer
            </Link>
          )}
          <span className="text-sm text-gray-500">
            Page {page} of {data.total_pages}
          </span>
          {page < data.total_pages && (
            <Link className={link} href={`/category/${slug}?page=${page + 1}`} rel="next">
              Older →
            </Link>
          )}
        </nav>
      </main>
      <SiteFooter name={settings.site_name} />
    </div>
  );
}
