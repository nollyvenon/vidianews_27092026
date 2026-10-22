"""Read-side queries for the news API."""

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Text, and_, case, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news import NewsArticle as A, NewsFetchRun
from app.services.news.sources import COUNTRY_NAMES, SOURCES, country_name

# Forum posts are not reporting; they rank as if this much older.
COMMUNITY_PENALTY = timedelta(hours=12)

# A local story is ranked as if it were this much newer than it is.
LOCAL_BOOST = timedelta(hours=18)


def _visible():
    """Flagged stories stay hidden until an editor approves them; rejected never show."""
    return and_(
        A.is_published.is_(True),
        A.deleted_at.is_(None),
        A.review_status != "rejected",
        or_(A.validation_status != "flagged", A.review_status == "approved"),
    )


def is_public(a: Optional[A]) -> bool:
    """Single-article counterpart of _visible() for detail pages (flagged stories stay reachable by link)."""
    return bool(a and a.is_published and a.deleted_at is None and a.review_status != "rejected")


def _community_penalty():
    return case((A.source_type == "community", COMMUNITY_PENALTY), else_=timedelta(0))


def _is_local(country: str):
    return or_(A.source_country == country, cast(A.mentioned_countries, Text).like(f'%"{country}"%'))


def article_body(a: A) -> List[str]:
    """Paragraphs to show on the article page: the extracted page text when we have more than the feed teaser."""
    text = a.full_content if a.full_content and len(a.full_content) > len(a.content or "") else (a.content or "")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) == 1 and len(paragraphs[0]) > 700:  # feed text arrives as one block: split on sentences
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", paragraphs[0])
        paragraphs, current = [], ""
        for sentence in sentences:
            current = f"{current} {sentence}".strip()
            if len(current) >= 350:
                paragraphs.append(current)
                current = ""
        if current:
            paragraphs.append(current)
    return paragraphs


def article_to_dict(a: A, brief: bool = False) -> Dict[str, Any]:
    data = {
        "id": a.id,
        "title": a.title,
        "url": a.url,
        "source": {"key": a.source_key, "name": a.source_name, "country": a.source_country, "type": a.source_type},
        "image_url": a.image_url,
        "image_source": a.image_source,
        "image_credit": a.image_credit,
        "image_credit_url": a.image_credit_url,
        "summary": a.summary,
        "description": a.description,
        "category": a.category,
        "keywords": a.keywords or [],
        "published_at": a.published_at.isoformat() if a.published_at else None,
        "is_featured": bool(a.is_featured),
        "validation": {
            "status": a.validation_status,
            "score": a.quality_score,
            "flags": a.validation_flags or [],
            "review_status": a.review_status,
        },
    }
    if not brief:
        data.update({
            "topics": a.topics or [], "people": a.people or [], "organizations": a.organizations or [],
            "locations": a.locations or [], "mentioned_countries": a.mentioned_countries or [],
            "nlp_engine": a.nlp_engine, "click_count": a.click_count,
            "body": article_body(a),
            "modified_at": (a.edited_at or a.enriched_at or a.published_at).isoformat() if (a.edited_at or a.enriched_at or a.published_at) else None,
            "meta_title": a.meta_title, "meta_description": a.meta_description,
        })
    return data


async def list_articles(
    session: AsyncSession, *, page: int, page_size: int, category: Optional[str] = None,
    country: Optional[str] = None, scope: str = "all", source: Optional[str] = None,
    q: Optional[str] = None, sort: str = "latest", days: Optional[int] = None,
    include_flagged: bool = False, min_quality: Optional[float] = None,
) -> Dict[str, Any]:
    conds = [_visible()] if not include_flagged else [
        A.is_published.is_(True), A.deleted_at.is_(None), A.review_status != "rejected"]
    if category:
        conds.append(A.category == category)
    if source:
        conds.append(A.source_key == source)
    if days:
        conds.append(A.published_at > datetime.now(timezone.utc) - timedelta(days=days))
    if min_quality is not None:
        conds.append(A.quality_score >= min_quality)
    if q:
        term = "%" + q.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        conds.append(or_(
            A.title.ilike(term), A.summary.ilike(term), A.source_name.ilike(term),
            cast(A.keywords, Text).ilike(term), cast(A.people, Text).ilike(term),
            cast(A.organizations, Text).ilike(term),
        ))
    if country and scope == "local":
        conds.append(_is_local(country))

    if sort == "trending":
        age_hours = func.extract("epoch", func.now() - A.published_at) / 3600.0
        order = (A.click_count * 5 + A.quality_score * 3 - age_hours / 12.0).desc()
    elif country and scope == "all" and sort == "latest":
        boost = case((_is_local(country), LOCAL_BOOST), else_=timedelta(0))
        order = (A.published_at + boost - _community_penalty()).desc()
    else:
        order = (A.published_at - _community_penalty()).desc()

    total = (await session.execute(select(func.count()).select_from(A).where(*conds))).scalar_one()
    rows = (await session.execute(
        select(A).where(*conds).order_by(order, A.id.desc()).offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()
    return {
        "items": [article_to_dict(r, brief=True) for r in rows],
        "page": page, "page_size": page_size, "total": total,
        "total_pages": max(1, -(-total // page_size)),
    }


async def featured(session: AsyncSession, country: Optional[str], limit: int = 5) -> List[Dict]:
    rows = (await session.execute(
        select(A).where(_visible(), A.is_featured.is_(True)).order_by(A.published_at.desc()).limit(20)
    )).scalars().all()
    if country:
        rows = sorted(rows, key=lambda r: not (r.source_country == country or country in (r.mentioned_countries or [])))
    return [article_to_dict(r, brief=True) for r in rows[:limit]]


async def category_counts(session: AsyncSession, country: Optional[str], scope: str) -> List[Dict]:
    conds = [_visible()]
    if country and scope == "local":
        conds.append(_is_local(country))
    rows = (await session.execute(
        select(A.category, func.count()).where(*conds).group_by(A.category).order_by(func.count().desc())
    )).all()
    return [{"category": c, "count": n} for c, n in rows]


async def source_stats(session: AsyncSession) -> List[Dict]:
    counts = dict((await session.execute(
        select(A.source_key, func.count()).where(_visible()).group_by(A.source_key)
    )).all())
    last = {}
    runs = (await session.execute(
        select(NewsFetchRun).order_by(NewsFetchRun.started_at.desc()).limit(len(SOURCES) * 3)
    )).scalars().all()
    for r in runs:
        last.setdefault(r.source_key, r)
    out = []
    for s in SOURCES:
        run = last.get(s["key"])
        out.append({
            "key": s["key"], "name": s["name"], "country": s["country"],
            "kind": s.get("kind", "rss"), "trust": s["trust"], "articles": counts.get(s["key"], 0),
            "last_fetch": {
                "at": run.started_at.isoformat(), "success": run.success, "new": run.items_new, "error": run.error,
            } if run else None,
        })
    return out


def country_list() -> List[Dict]:
    by_country: Dict[str, int] = {}
    for s in SOURCES:
        by_country[s["country"]] = by_country.get(s["country"], 0) + 1
    return [
        {"code": code, "name": country_name(code), "sources": n}
        for code, n in sorted(by_country.items(), key=lambda kv: (kv[0] == "XX", country_name(kv[0])))
    ]


def has_local_sources(country: str) -> bool:
    return any(s["country"] == country for s in SOURCES)


def valid_country(code: Optional[str]) -> Optional[str]:
    if code and len(code) == 2 and code.upper() in COUNTRY_NAMES:
        return code.upper()
    return None


async def related(session: AsyncSession, article: A, limit: int = 6) -> List[Dict]:
    """Recent stories on the same topic: shared keywords/entities first, then the same category."""
    window = datetime.now(timezone.utc) - timedelta(days=14)
    pool = (await session.execute(
        select(A).where(_visible(), A.id != article.id, A.published_at > window,
                        or_(A.category == article.category, A.source_key == article.source_key))
        .order_by(A.published_at.desc()).limit(300)
    )).scalars().all()
    mine_terms = {t.lower() for t in (article.keywords or []) + (article.people or []) + (article.organizations or [])}
    mine_title = set(article.title.lower().split())

    def score(r: A) -> float:
        terms = {t.lower() for t in (r.keywords or []) + (r.people or []) + (r.organizations or [])}
        shared = len(mine_terms & terms)
        overlap = len(mine_title & set(r.title.lower().split()))
        return shared * 3 + overlap * 0.5 + (2 if r.category == article.category else 0) + (1 if r.image_url else 0)

    ranked = sorted(pool, key=lambda r: (score(r), r.published_at), reverse=True)
    return [article_to_dict(r, brief=True) for r in ranked[:limit]]
