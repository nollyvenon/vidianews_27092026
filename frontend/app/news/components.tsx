"use client";

import { Article, newsApi, timeAgo } from "./api";

const CATEGORY_STYLES: Record<string, string> = {
  politics: "bg-red-50 text-red-700",
  business: "bg-emerald-50 text-emerald-700",
  sports: "bg-orange-50 text-orange-700",
  technology: "bg-indigo-50 text-indigo-700",
  entertainment: "bg-pink-50 text-pink-700",
  health: "bg-teal-50 text-teal-700",
  science: "bg-cyan-50 text-cyan-700",
  world: "bg-blue-50 text-blue-700",
  crime: "bg-slate-100 text-slate-700",
  education: "bg-amber-50 text-amber-700",
  lifestyle: "bg-purple-50 text-purple-700",
  general: "bg-gray-100 text-gray-700",
};

export function CategoryBadge({ category }: { category: string }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${CATEGORY_STYLES[category] ?? CATEGORY_STYLES.general}`}>
      {category}
    </span>
  );
}

const FLAG_TEXT: Record<string, string> = {
  community_source: "User-generated forum post",
  sensational_language: "Sensational wording",
  unverified_claim_language: "Contains unconfirmed or attributed-only claims",
  thin_content: "Very little text in the feed",
  missing_date: "Publication date missing",
  all_caps_title: "Headline in capitals",
  question_headline: "Question headline",
};

export function ValidationBadge({ article }: { article: Article }) {
  const { status, flags } = article.validation;
  if (status === "passed") return null;
  const label = status === "flagged" ? "Under review" : "Unverified";
  const tone = status === "flagged" ? "bg-red-50 text-red-700 ring-red-200" : "bg-amber-50 text-amber-800 ring-amber-200";
  const title = flags.map((f) => FLAG_TEXT[f] ?? f).join(" · ") || "Not independently verified";
  return (
    <span title={title} className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${tone}`}>
      <span aria-hidden>⚠</span>
      {label}
    </span>
  );
}

function Thumb({ article, className }: { article: Article; className: string }) {
  if (!article.image_url) {
    return (
      <div className={`${className} flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200 text-slate-400`} aria-hidden>
        <span className="text-3xl">📰</span>
      </div>
    );
  }
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={article.image_url}
      alt=""
      loading="lazy"
      referrerPolicy="no-referrer"
      className={`${className} object-cover bg-slate-100`}
      onError={(e) => {
        (e.currentTarget as HTMLImageElement).style.visibility = "hidden";
      }}
    />
  );
}

function ReadLink({ article, children }: { article: Article; children: React.ReactNode }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      onClick={() => newsApi.click(article.id)}
      className="font-medium text-blue-700 hover:text-blue-900 hover:underline"
    >
      {children}
    </a>
  );
}

export function Meta({ article }: { article: Article }) {
  return (
    <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-gray-500">
      <span className="font-semibold text-gray-700">{article.source.name}</span>
      <span aria-hidden>•</span>
      <time dateTime={article.published_at} title={new Date(article.published_at).toLocaleString()}>
        {timeAgo(article.published_at)}
      </time>
      {article.author && (
        <>
          <span aria-hidden>•</span>
          <span className="truncate max-w-[12rem]">{article.author}</span>
        </>
      )}
    </div>
  );
}

export function ArticleCard({ article }: { article: Article }) {
  return (
    <article className="flex flex-col overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition hover:shadow-md">
      <Thumb article={article} className="h-44 w-full" />
      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex flex-wrap items-center gap-2">
          <CategoryBadge category={article.category} />
          <ValidationBadge article={article} />
        </div>
        <h3 className="text-base font-semibold leading-snug text-gray-900">
          <a href={article.url} target="_blank" rel="noopener noreferrer" onClick={() => newsApi.click(article.id)} className="hover:text-blue-700">
            {article.title}
          </a>
        </h3>
        {article.summary && <p className="line-clamp-3 text-sm text-gray-600">{article.summary}</p>}
        <div className="mt-auto flex items-end justify-between gap-2 pt-2">
          <Meta article={article} />
          <ReadLink article={article}>
            <span className="whitespace-nowrap text-sm">Read →</span>
          </ReadLink>
        </div>
      </div>
    </article>
  );
}

export function FeaturedHero({ items }: { items: Article[] }) {
  if (items.length === 0) return null;
  const [lead, ...rest] = items;
  return (
    <section aria-label="Featured stories" className="grid gap-4 lg:grid-cols-3">
      <article className="group relative overflow-hidden rounded-2xl bg-slate-900 lg:col-span-2">
        <Thumb article={lead} className="h-72 w-full opacity-70 transition group-hover:opacity-80 sm:h-96" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 space-y-2 p-5 text-white">
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-white/90 px-2 py-0.5 text-xs font-semibold text-gray-900">Featured</span>
            <CategoryBadge category={lead.category} />
          </div>
          <h2 className="text-xl font-bold leading-tight sm:text-3xl">
            <a href={lead.url} target="_blank" rel="noopener noreferrer" onClick={() => newsApi.click(lead.id)}>
              {lead.title}
            </a>
          </h2>
          {lead.summary && <p className="line-clamp-2 max-w-3xl text-sm text-gray-200">{lead.summary}</p>}
          <p className="text-xs text-gray-300">
            {lead.source.name} • {timeAgo(lead.published_at)}
          </p>
        </div>
      </article>
      <div className="flex flex-col gap-4">
        {rest.slice(0, 2).map((a) => (
          <article key={a.id} className="flex flex-1 gap-3 rounded-xl border border-gray-200 bg-white p-3 shadow-sm">
            <Thumb article={a} className="h-24 w-24 flex-none rounded-lg" />
            <div className="flex min-w-0 flex-col gap-1">
              <CategoryBadge category={a.category} />
              <h3 className="line-clamp-3 text-sm font-semibold leading-snug">
                <a href={a.url} target="_blank" rel="noopener noreferrer" onClick={() => newsApi.click(a.id)} className="hover:text-blue-700">
                  {a.title}
                </a>
              </h3>
              <Meta article={a} />
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export function TrendingList({ items }: { items: Article[] }) {
  return (
    <aside aria-label="Trending" className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500">🔥 Trending</h2>
      {items.length === 0 ? (
        <p className="text-sm text-gray-500">Nothing trending yet.</p>
      ) : (
        <ol className="space-y-3">
          {items.map((a, i) => (
            <li key={a.id} className="flex gap-3">
              <span className="w-5 flex-none text-lg font-bold text-gray-300">{i + 1}</span>
              <div className="min-w-0">
                <a
                  href={a.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() => newsApi.click(a.id)}
                  className="line-clamp-2 text-sm font-medium leading-snug text-gray-900 hover:text-blue-700"
                >
                  {a.title}
                </a>
                <Meta article={a} />
              </div>
            </li>
          ))}
        </ol>
      )}
    </aside>
  );
}

export function CardSkeletons({ count = 6 }: { count?: number }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="animate-pulse overflow-hidden rounded-xl border border-gray-200 bg-white" aria-hidden>
          <div className="h-44 bg-gray-200" />
          <div className="space-y-3 p-4">
            <div className="h-3 w-1/4 rounded bg-gray-200" />
            <div className="h-4 w-11/12 rounded bg-gray-200" />
            <div className="h-4 w-3/4 rounded bg-gray-200" />
            <div className="h-3 w-1/2 rounded bg-gray-200" />
          </div>
        </div>
      ))}
    </>
  );
}

export function Pagination({ page, totalPages, onChange }: { page: number; totalPages: number; onChange: (p: number) => void }) {
  if (totalPages <= 1) return null;
  const pages: (number | "…")[] = [];
  for (let p = 1; p <= totalPages; p++) {
    if (p === 1 || p === totalPages || Math.abs(p - page) <= 1) pages.push(p);
    else if (pages[pages.length - 1] !== "…") pages.push("…");
  }
  const btn = "rounded-md border px-3 py-1.5 text-sm";
  return (
    <nav aria-label="Pagination" className="flex flex-wrap items-center justify-center gap-1 pt-2">
      <button className={`${btn} border-gray-300 disabled:opacity-40`} disabled={page <= 1} onClick={() => onChange(page - 1)}>
        ← Prev
      </button>
      {pages.map((p, i) =>
        p === "…" ? (
          <span key={`e${i}`} className="px-2 text-gray-400">
            …
          </span>
        ) : (
          <button
            key={p}
            aria-current={p === page ? "page" : undefined}
            className={`${btn} ${p === page ? "border-blue-600 bg-blue-600 text-white" : "border-gray-300 hover:bg-gray-50"}`}
            onClick={() => onChange(p)}
          >
            {p}
          </button>
        )
      )}
      <button className={`${btn} border-gray-300 disabled:opacity-40`} disabled={page >= totalPages} onClick={() => onChange(page + 1)}>
        Next →
      </button>
    </nav>
  );
}
