"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Article, ArticleDetail, newsApi, timeAgo } from "../api";
import { ArticleCard, CardSkeletons, CategoryBadge, FallbackImage, ValidationBadge } from "../components";

function ArticleImage({ article }: { article: ArticleDetail }) {
  const [failed, setFailed] = useState(false);
  if (!article.image_url || failed) {
    return <FallbackImage category={article.category} className="h-56 w-full rounded-xl sm:h-80" />;
  }
  return (
    <figure>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={article.image_url}
        alt={article.title}
        referrerPolicy="no-referrer"
        className="max-h-[32rem] w-full rounded-xl bg-slate-100 object-cover"
        onError={() => setFailed(true)}
      />
      <figcaption className="mt-1 text-xs text-gray-500">
        {article.image_source === "wikimedia" && <span className="mr-1 font-medium">Illustrative image.</span>}
        {article.image_credit_url ? (
          <a href={article.image_credit_url} target="_blank" rel="noopener noreferrer" className="underline hover:text-gray-700">
            {article.image_credit}
          </a>
        ) : (
          article.image_credit
        )}
      </figcaption>
    </figure>
  );
}

export default function ArticlePage() {
  const params = useParams<{ id: string }>();
  const id = Number(params?.id);
  const [article, setArticle] = useState<ArticleDetail | null>(null);
  const [related, setRelated] = useState<Article[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!Number.isInteger(id) || id < 1) {
      setError("404: Article not found");
      return;
    }
    let cancelled = false;
    setArticle(null);
    setRelated(null);
    setError(null);
    window.scrollTo({ top: 0 });
    newsApi
      .article(id)
      .then((a) => {
        if (cancelled) return;
        setArticle(a);
        document.title = `${a.title} | VidiaNews`;
        newsApi.click(a.id);
      })
      .catch((e: Error) => !cancelled && setError(e.message));
    newsApi
      .related(id)
      .then((r) => !cancelled && setRelated(r.items))
      .catch(() => !cancelled && setRelated([]));
    return () => {
      cancelled = true;
    };
  }, [id]);

  const notFound = error?.startsWith("404");
  const teaserOnly = article ? article.body.join(" ").length < 600 : false;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
          <Link href="/" className="text-lg font-bold text-gray-900">
            VidiaNews
          </Link>
          <Link href="/" className="text-sm font-medium text-blue-700 hover:underline">
            ← All news
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-4xl space-y-8 px-4 py-6">
        {error && (
          <div role="alert" className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
            <p className="font-semibold text-red-800">{notFound ? "This article could not be found." : "Could not load this article."}</p>
            {!notFound && <p className="mt-1 text-sm text-red-700">{error}</p>}
            <Link href="/" className="mt-3 inline-block text-sm font-medium text-blue-700 hover:underline">
              Back to the news
            </Link>
          </div>
        )}

        {!error && !article && (
          <div className="animate-pulse space-y-4" aria-busy="true">
            <div className="h-8 w-3/4 rounded bg-gray-200" />
            <div className="h-80 rounded-xl bg-gray-200" />
            <div className="h-4 w-full rounded bg-gray-200" />
            <div className="h-4 w-5/6 rounded bg-gray-200" />
          </div>
        )}

        {article && (
          <article className="space-y-5">
            <div className="flex flex-wrap items-center gap-2">
              <CategoryBadge category={article.category} />
              <ValidationBadge article={article} />
            </div>
            <h1 className="text-2xl font-bold leading-tight text-gray-900 sm:text-4xl">{article.title}</h1>
            <p className="text-sm text-gray-600">
              <span className="font-semibold text-gray-800">{article.source.name}</span>
              {" • "}
              <time dateTime={article.published_at} title={new Date(article.published_at).toLocaleString()}>
                {new Date(article.published_at).toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" })}
                {" · "}
                {timeAgo(article.published_at)}
              </time>
            </p>

            <ArticleImage article={article} />

            {article.summary && !teaserOnly && (
              <p className="rounded-lg border-l-4 border-blue-600 bg-blue-50 px-4 py-3 text-base font-medium text-gray-800">
                {article.summary}
              </p>
            )}

            <div className="space-y-4 text-base leading-relaxed text-gray-800">
              {article.body.length > 0 ? (
                article.body.map((p, i) => <p key={i}>{p}</p>)
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

            <footer className="rounded-xl border border-gray-200 bg-white p-4 text-sm text-gray-600">
              <p>
                {teaserOnly ? "This is an excerpt. " : ""}
                Published by <span className="font-semibold text-gray-800">{article.source.name}</span>.
              </p>
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 inline-block font-medium text-blue-700 hover:underline"
              >
                Read the original article at {article.source.name} ↗
              </a>
            </footer>
          </article>
        )}

        {article && (
          <section aria-label="Related news" className="space-y-4">
            <h2 className="text-lg font-bold text-gray-900">Related news</h2>
            {related === null ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <CardSkeletons count={3} />
              </div>
            ) : related.length === 0 ? (
              <p className="text-sm text-gray-500">No related stories yet.</p>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {related.map((r) => (
                  <ArticleCard key={r.id} article={r} />
                ))}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
