import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import SiteFooter from "../../SiteFooter";
import { apiGet, getSettings } from "../../server";

export const dynamic = "force-dynamic";

interface PageData {
  slug: string;
  title: string;
  body: string;
  meta_description: string | null;
  updated_at: string | null;
}

type Props = { params: Promise<{ slug: string }> };

const load = (slug: string) => apiGet<PageData>(`/site/pages/${encodeURIComponent(slug)}`);

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const page = await load(slug);
  if (!page) return { title: "Page not found", robots: { index: false, follow: false } };
  const description = page.meta_description || page.body.replace(/[#\n]+/g, " ").slice(0, 155).trim();
  return {
    title: page.title,
    description,
    alternates: { canonical: `/p/${page.slug}` },
    openGraph: { type: "website", title: page.title, description, url: `/p/${page.slug}` },
  };
}

/** Paragraphs separated by blank lines; a line starting with "## " is a heading. */
function Body({ text }: { text: string }) {
  return (
    <div className="space-y-4 text-base leading-relaxed text-gray-800">
      {text
        .split(/\n{2,}/)
        .map((block) => block.trim())
        .filter(Boolean)
        .map((block, i) =>
          block.startsWith("## ") ? (
            <h2 key={i} className="pt-2 text-xl font-bold text-gray-900">
              {block.slice(3)}
            </h2>
          ) : (
            <p key={i} className="whitespace-pre-line">
              {block}
            </p>
          )
        )}
    </div>
  );
}

export default async function StaticPage({ params }: Props) {
  const { slug } = await params;
  const [page, settings] = await Promise.all([load(slug), getSettings()]);
  if (!page) notFound();
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-4 py-3">
          <Link href="/" className="text-lg font-bold text-gray-900">
            {settings.site_name}
          </Link>
          <Link href="/" className="text-sm font-medium text-blue-700 hover:underline">
            ← All news
          </Link>
        </div>
      </header>
      <main className="mx-auto max-w-3xl space-y-6 px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900">{page.title}</h1>
        <Body text={page.body} />
      </main>
      <SiteFooter name={settings.site_name} />
    </div>
  );
}
