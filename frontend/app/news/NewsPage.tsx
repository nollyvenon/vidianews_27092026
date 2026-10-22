"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Article, ArticlePage, Location, newsApi } from "./api";
import AdSlot from "../AdSlot";
import { ArticleCard, CardSkeletons, FeaturedHero, Pagination, TrendingList } from "./components";

const PAGE_SIZE = 12;
const COUNTRY_KEY = "news.country";

type Scope = "all" | "local";
type Sort = "latest" | "trending";

function safeStorage(op: "get" | "set" | "remove", value?: string): string | null {
  try {
    if (op === "get") return window.localStorage.getItem(COUNTRY_KEY);
    if (op === "set") window.localStorage.setItem(COUNTRY_KEY, value as string);
    else window.localStorage.removeItem(COUNTRY_KEY);
  } catch {
    /* storage blocked: preference just won't persist */
  }
  return null;
}

export interface InitialNews {
  location: Location;
  articles: ArticlePage;
  featured: Article[];
  trending: Article[];
  categories: { category: string; count: number }[];
}

/** `initial` is rendered on the server so crawlers and first paint get real headlines. */
export default function NewsPage({ initial }: { initial?: InitialNews }) {
  const [location, setLocation] = useState<Location | null>(initial?.location ?? null);
  const [manualCountry, setManualCountry] = useState<string | null>(null);
  const [countries, setCountries] = useState<{ code: string; name: string; sources: number }[]>([]);
  const [sources, setSources] = useState<{ key: string; name: string; articles: number }[]>([]);
  const [categories, setCategories] = useState<{ category: string; count: number }[]>(initial?.categories ?? []);
  const [featured, setFeatured] = useState<Article[]>(initial?.featured ?? []);
  const [trending, setTrending] = useState<Article[]>(initial?.trending ?? []);

  const [category, setCategory] = useState("");
  const [source, setSource] = useState("");
  const [scope, setScope] = useState<Scope>("all");
  const [sort, setSort] = useState<Sort>("latest");
  const [searchInput, setSearchInput] = useState("");
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  const [data, setData] = useState<ArticlePage | null>(initial?.articles ?? null);
  const [loading, setLoading] = useState(!initial);
  const [error, setError] = useState<string | null>(null);
  const [ready, setReady] = useState(!!initial);
  const usedInitial = useRef(false);
  const listTop = useRef<HTMLDivElement>(null);

  const country = location?.country;

  // Initial: stored preference -> else IP detection; plus static lists.
  useEffect(() => {
    const stored = safeStorage("get");
    if (stored) setManualCountry(stored);
    newsApi
      .location(stored ?? undefined)
      .then(setLocation)
      .catch(() => setLocation({ country: "XX", country_name: "International", source: "default", has_local_sources: false }))
      .finally(() => setReady(true));
    newsApi.countries().then((r) => setCountries(r.countries)).catch(() => undefined);
    newsApi.sources().then((r) => setSources(r.sources.filter((s) => s.articles > 0))).catch(() => undefined);
  }, []);

  // Debounce search input.
  useEffect(() => {
    const t = setTimeout(() => {
      setQuery(searchInput.trim());
      setPage(1);
    }, 350);
    return () => clearTimeout(t);
  }, [searchInput]);

  // Side panels depend on the country.
  useEffect(() => {
    if (!ready || !country) return;
    newsApi.featured(country).then((r) => setFeatured(r.items)).catch(() => setFeatured([]));
    newsApi.trending(country).then((r) => setTrending(r.items)).catch(() => setTrending([]));
  }, [ready, country]);

  useEffect(() => {
    if (!ready || !country) return;
    newsApi.categories(country, scope).then((r) => setCategories(r.categories)).catch(() => setCategories([]));
  }, [ready, country, scope]);

  const load = useCallback(
    (signal?: AbortSignal) => {
      if (!country) return;
      setLoading(true);
      setError(null);
      newsApi
        .articles({ page, page_size: PAGE_SIZE, category, country, scope, source, q: query, sort }, signal)
        .then(setData)
        .catch((e: Error) => {
          if (e.name !== "AbortError") setError(e.message);
        })
        .finally(() => {
          if (!signal?.aborted) setLoading(false);
        });
    },
    [country, page, category, scope, source, query, sort]
  );

  useEffect(() => {
    if (!ready) return;
    if (initial && !usedInitial.current) {
      usedInitial.current = true; // the server already rendered this exact view
      return;
    }
    const ctrl = new AbortController();
    load(ctrl.signal);
    return () => ctrl.abort();
  }, [ready, load]);

  const resetTo = <T,>(setter: (v: T) => void) => (v: T) => {
    setter(v);
    setPage(1);
  };

  const changeCountry = (code: string) => {
    if (code === "auto") {
      safeStorage("remove");
      setManualCountry(null);
      newsApi.location().then(setLocation).catch(() => undefined);
    } else {
      safeStorage("set", code);
      setManualCountry(code);
      newsApi.location(code).then(setLocation).catch(() => undefined);
    }
    setPage(1);
  };

  const goToPage = (p: number) => {
    setPage(p);
    listTop.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const showHero = page === 1 && !category && !query && !source && sort === "latest" && featured.length > 0;
  const items = data?.items ?? [];

  const chip = (active: boolean) =>
    `whitespace-nowrap rounded-full border px-3 py-1.5 text-sm capitalize transition ${
      active ? "border-blue-600 bg-blue-600 text-white" : "border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
    }`;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="sticky top-0 z-20 border-b border-gray-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-3 px-4 py-3 sm:px-6 lg:px-8">
          <Link href="/" className="text-lg font-bold text-gray-900">
            VidiaNews
          </Link>
          <span className="text-gray-300">/</span>
          <h1 className="text-lg font-semibold text-gray-700">News</h1>

          <div className="order-last flex w-full items-center sm:order-none sm:ml-4 sm:w-auto sm:flex-1">
            <label htmlFor="news-search" className="sr-only">
              Search news
            </label>
            <input
              id="news-search"
              type="search"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder="Search headlines, people, organizations…"
              className="w-full max-w-xl rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div className="ml-auto flex items-center gap-2 text-sm">
            <label htmlFor="news-country" className="text-gray-500">
              📍
            </label>
            <select
              id="news-country"
              value={manualCountry ?? "auto"}
              onChange={(e) => changeCountry(e.target.value)}
              className="rounded-lg border border-gray-300 bg-white px-2 py-1.5"
              aria-label="Country"
            >
              <option value="auto">{location && !manualCountry ? `Auto: ${location.country_name}` : "Auto-detect"}</option>
              {countries.map((c) => (
                <option key={c.code} value={c.code}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
        {location && !location.has_local_sources && location.country !== "XX" && (
          <p className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-2 text-sm text-blue-800">
            We don&apos;t have a dedicated {location.country_name} source yet, so you&apos;re seeing international coverage plus stories that mention{" "}
            {location.country_name}.
          </p>
        )}

        <AdSlot placement="home_top" />

        {showHero && <FeaturedHero items={featured} />}

        <div className="flex gap-2 overflow-x-auto pb-1" role="tablist" aria-label="Categories">
          <button className={chip(!category)} onClick={() => resetTo(setCategory)("")}>
            All
          </button>
          {categories.map((c) => (
            <button key={c.category} className={chip(category === c.category)} onClick={() => resetTo(setCategory)(c.category)}>
              {c.category} <span className="opacity-60">({c.count})</span>
            </button>
          ))}
        </div>

        <div ref={listTop} className="flex flex-wrap items-center gap-3 text-sm">
          <div className="inline-flex overflow-hidden rounded-lg border border-gray-300 bg-white">
            {(["all", "local"] as Scope[]).map((s) => (
              <button
                key={s}
                onClick={() => resetTo(setScope)(s)}
                className={`px-3 py-1.5 ${scope === s ? "bg-gray-900 text-white" : "text-gray-700 hover:bg-gray-50"}`}
              >
                {s === "all" ? "Top stories" : `${location?.country_name ?? "Local"} only`}
              </button>
            ))}
          </div>
          <div className="inline-flex overflow-hidden rounded-lg border border-gray-300 bg-white">
            {(["latest", "trending"] as Sort[]).map((s) => (
              <button
                key={s}
                onClick={() => resetTo(setSort)(s)}
                className={`px-3 py-1.5 capitalize ${sort === s ? "bg-gray-900 text-white" : "text-gray-700 hover:bg-gray-50"}`}
              >
                {s}
              </button>
            ))}
          </div>
          <select
            value={source}
            onChange={(e) => resetTo(setSource)(e.target.value)}
            className="rounded-lg border border-gray-300 bg-white px-2 py-1.5"
            aria-label="Source"
          >
            <option value="">All sources</option>
            {sources.map((s) => (
              <option key={s.key} value={s.key}>
                {s.name} ({s.articles})
              </option>
            ))}
          </select>
          {(category || source || query || scope !== "all" || sort !== "latest") && (
            <button
              className="text-blue-700 hover:underline"
              onClick={() => {
                setCategory("");
                setSource("");
                setScope("all");
                setSort("latest");
                setSearchInput("");
                setQuery("");
                setPage(1);
              }}
            >
              Clear filters
            </button>
          )}
          {data && !loading && <span className="ml-auto text-gray-500">{data.total.toLocaleString()} stories</span>}
        </div>

        <div className="grid gap-6 lg:grid-cols-[1fr_20rem]">
          <section aria-live="polite" aria-busy={loading}>
            {error ? (
              <div role="alert" className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
                <p className="font-medium text-red-800">Couldn&apos;t load the news.</p>
                <p className="mt-1 text-sm text-red-700">{error}</p>
                <button onClick={() => load()} className="mt-4 rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700">
                  Try again
                </button>
              </div>
            ) : loading && items.length === 0 ? (
              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                <CardSkeletons />
              </div>
            ) : items.length === 0 ? (
              <div className="rounded-xl border border-dashed border-gray-300 bg-white p-10 text-center text-gray-600">
                <p className="text-lg font-medium">No stories found</p>
                <p className="mt-1 text-sm">
                  {query || category || source
                    ? "Try different filters or search terms."
                    : "News is still being collected — check back in a minute."}
                </p>
              </div>
            ) : (
              <div className={`grid gap-4 sm:grid-cols-2 xl:grid-cols-3 transition-opacity ${loading ? "opacity-50" : ""}`}>
                {items.map((a) => (
                  <ArticleCard key={a.id} article={a} />
                ))}
              </div>
            )}
            {data && !error && <div className="mt-6"><Pagination page={data.page} totalPages={data.total_pages} onChange={goToPage} /></div>}
          </section>

          <div className="space-y-4 lg:sticky lg:top-24 lg:self-start">
            <TrendingList items={trending} />
            <AdSlot placement="home_sidebar" />
            <p className="px-1 text-xs leading-relaxed text-gray-500">
              Headlines and summaries are collected from each publisher&apos;s public RSS feed; summaries and tags are generated automatically.
              Stories marked <em>Unverified</em> or <em>Under review</em> are not independently confirmed. Always read the original article.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
