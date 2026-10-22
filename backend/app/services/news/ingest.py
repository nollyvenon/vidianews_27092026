"""Fetch, validate, enrich, de-duplicate and store articles."""

import asyncio
import hashlib
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import httpx
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.news import NewsArticle, NewsFetchRun
from app.services.news import nlp
from app.services.news.cache import cache_invalidate
from app.services.news.enrich import clean_image_url, enrich_pending
from app.services.news.feed_parser import RawItem, parse_feed
from app.services.news.sources import SOURCES, SOURCE_BY_KEY, Source
from app.services.news.validation import (
    STATUS_FLAGGED, STATUS_REJECTED, is_near_duplicate, normalize_url, title_tokens, validate_article,
)

_log = logging.getLogger(__name__)

MAX_ITEMS_PER_FEED = 60
CONCURRENCY = 6
_run_lock = asyncio.Lock()


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _title_key(title: str) -> str:
    return _sha(" ".join(sorted(title_tokens(title))))


async def _download(client: httpx.AsyncClient, url: str, attempts: int = 3) -> bytes:
    last: Optional[Exception] = None
    for attempt in range(attempts):
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            if len(resp.content) > 5_000_000:
                raise ValueError("feed larger than 5MB")
            return resp.content
        except (httpx.HTTPError, ValueError) as exc:
            last = exc
            if attempt < attempts - 1:
                await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{type(last).__name__}: {last}")


async def _ingest_source(client: httpx.AsyncClient, source: Source) -> Dict:
    stats = {"source": source["key"], "success": False, "seen": 0, "new": 0, "duplicate": 0,
             "rejected": 0, "error": None}
    started = time.monotonic()
    try:
        items: List[RawItem] = parse_feed(await _download(client, source["feed_url"]))
        stats["seen"] = len(items)
        now = datetime.now(timezone.utc)
        items.sort(key=lambda i: i.published_at or now, reverse=True)
        items = items[:MAX_ITEMS_PER_FEED]

        # 1. validate and drop in-feed duplicates
        candidates = []
        seen_urls, seen_titles = set(), []
        for item in items:
            url = normalize_url(item.url)
            result = validate_article(
                item.title, url, item.content, item.published_at, source["domains"],
                source["trust"], source.get("kind", "rss"), settings.NEWS_MAX_AGE_DAYS, now,
            )
            if result.status == STATUS_REJECTED:
                stats["rejected"] += 1
                continue
            toks = title_tokens(item.title)
            if url in seen_urls or any(is_near_duplicate(toks, t) for t in seen_titles):
                stats["duplicate"] += 1
                continue
            seen_urls.add(url)
            seen_titles.append(toks)
            candidates.append((item, url, toks, result))

        # 2. drop what is already stored (exact URL / title, or a near-identical recent headline)
        if candidates:
            async with AsyncSessionLocal() as session:
                url_hashes = [_sha(c[1]) for c in candidates]
                title_hashes = [_title_key(c[0].title) for c in candidates]
                known = await session.execute(
                    select(NewsArticle.url_hash, NewsArticle.title_hash).where(
                        (NewsArticle.url_hash.in_(url_hashes)) | (NewsArticle.title_hash.in_(title_hashes))
                    )
                )
                known_urls, known_titles = set(), set()
                for uh, th in known.all():
                    known_urls.add(uh)
                    known_titles.add(th)
                recent = await session.execute(
                    select(NewsArticle.title).where(
                        NewsArticle.published_at > now - timedelta(days=3)
                    )
                )
                recent_tokens = [title_tokens(t) for (t,) in recent.all()]

            fresh = []
            for item, url, toks, result in candidates:
                if (_sha(url) in known_urls or _title_key(item.title) in known_titles
                        or any(is_near_duplicate(toks, t) for t in recent_tokens)):
                    stats["duplicate"] += 1
                    continue
                fresh.append((item, url, result))

            # 3. NLP enrichment off the event loop
            payloads = [
                dict(title=i.title, content=i.content, feed_categories=i.feed_categories,
                     source_name=source["name"], published_at=i.published_at or now,
                     default_category=source.get("default_category"))
                for i, _, _ in fresh
            ]
            analyses = await asyncio.to_thread(nlp.analyze_many, payloads) if payloads else []

            rows = []
            for (item, url, result), a in zip(fresh, analyses):
                image = clean_image_url(item.image_url)
                rows.append(dict(
                    source_key=source["key"], source_name=source["name"], source_country=source["country"],
                    source_type=source.get("kind", "rss"), title=item.title[:500], url=url[:2048],
                    url_hash=_sha(url), title_hash=_title_key(item.title),
                    author=None,  # bylines are deliberately not stored or shown
                    image_url=image, image_source="publisher" if image else None,
                    image_credit=f"Image: {source['name']}" if image else None,
                    image_credit_url=url[:2048] if image else None,
                    content=item.content[:5000], summary=a.summary, description=a.description,
                    published_at=item.published_at or now, fetched_at=now, category=a.category,
                    keywords=a.keywords, topics=a.topics, people=a.people, organizations=a.organizations,
                    locations=a.locations, mentioned_countries=a.mentioned_countries,
                    nlp_engine=a.engine, quality_score=result.score,
                    validation_status=result.status, validation_flags=result.flags,
                    review_status="pending" if result.needs_review else "none",
                    click_count=0, is_featured=False,
                ))
            if rows:
                async with AsyncSessionLocal() as session:
                    res = await session.execute(
                        pg_insert(NewsArticle).values(rows).on_conflict_do_nothing(index_elements=["url_hash"])
                        .returning(NewsArticle.id)
                    )
                    stats["new"] = len(res.all())
                    stats["duplicate"] += len(rows) - stats["new"]
                    await session.commit()
        stats["success"] = True
    except Exception as exc:  # noqa: BLE001 - one bad source must not stop the others
        stats["error"] = f"{type(exc).__name__}: {exc}"[:500]
        _log.warning("news source %s failed: %s", source["key"], stats["error"])

    try:
        async with AsyncSessionLocal() as session:
            session.add(NewsFetchRun(
                source_key=source["key"], duration_ms=int((time.monotonic() - started) * 1000),
                success=stats["success"], items_seen=stats["seen"], items_new=stats["new"],
                items_duplicate=stats["duplicate"], items_rejected=stats["rejected"], error=stats["error"],
            ))
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        _log.warning("could not record fetch run for %s: %r", source["key"], exc)
    return stats


async def _refresh_featured() -> None:
    """Feature up to 6 recent, well-sourced stories with images (max 2 per source)."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(
            select(NewsArticle.id, NewsArticle.source_key).where(
                NewsArticle.published_at > cutoff,
                NewsArticle.validation_status == "passed",
                NewsArticle.image_url.is_not(None),
                NewsArticle.review_status != "rejected",
            ).order_by(NewsArticle.quality_score.desc(), NewsArticle.published_at.desc()).limit(80)
        )).all()
        per_source: Dict[str, int] = {}
        chosen = []
        for article_id, source_key in rows:
            if per_source.get(source_key, 0) >= 2:
                continue
            per_source[source_key] = per_source.get(source_key, 0) + 1
            chosen.append(article_id)
            if len(chosen) >= 6:
                break
        await session.execute(update(NewsArticle).where(NewsArticle.is_featured.is_(True)).values(is_featured=False))
        if chosen:
            await session.execute(update(NewsArticle).where(NewsArticle.id.in_(chosen)).values(is_featured=True))
        await session.commit()


async def run_fetch(source_keys: Optional[List[str]] = None) -> Dict:
    """Fetch all (or selected) sources. Only one run at a time."""
    if _run_lock.locked():
        return {"status": "already_running"}
    async with _run_lock:
        sources = [SOURCE_BY_KEY[k] for k in source_keys if k in SOURCE_BY_KEY] if source_keys else SOURCES
        sem = asyncio.Semaphore(CONCURRENCY)
        headers = {"User-Agent": settings.NEWS_USER_AGENT, "Accept": "application/rss+xml, application/xml, text/xml, */*"}
        started = time.monotonic()
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True, headers=headers) as client:
            async def guarded(src):
                async with sem:
                    return await _ingest_source(client, src)
            results = await asyncio.gather(*(guarded(s) for s in sources))
        enrichment = {}
        try:
            for _ in range(4):  # drain a backlog without making one run unbounded
                batch = await enrich_pending()
                for k, v in batch.items():
                    enrichment[k] = enrichment.get(k, 0) + v
                if batch["enriched"] < 250:
                    break
        except Exception as exc:  # noqa: BLE001
            _log.warning("article enrichment failed: %r", exc)
        try:
            await _refresh_featured()
        except Exception as exc:  # noqa: BLE001
            _log.warning("featured refresh failed: %r", exc)
        await cache_invalidate()
        summary = {
            "status": "completed",
            "duration_s": round(time.monotonic() - started, 1),
            "sources": len(results),
            "sources_ok": sum(1 for r in results if r["success"]),
            "new": sum(r["new"] for r in results),
            "duplicate": sum(r["duplicate"] for r in results),
            "rejected": sum(r["rejected"] for r in results),
            "enrichment": enrichment,
            "nlp_engine": "spacy" if nlp.spacy_available() else "rules",
            "results": results,
        }
        _log.info("news fetch done: %s new, %s/%s sources ok", summary["new"], summary["sources_ok"], summary["sources"])
        return summary
