"""News endpoints.

Reading is public. Triggering a fetch requires a signed-in user; reviewing
flagged stories requires an admin/editor role or the `news.review` permission.
"""

import asyncio
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token, verify_token_not_expired
from app.db.session import get_session
from app.models.news import NewsArticle
from app.models.user import Role, User, user_roles
from app.services.news import nlp, queries
from app.services.news.cache import cache_get, cache_invalidate, cache_set
from app.services.news.enrich import enrich_one
from app.services.news.geo import detect_country
from app.services.news.ingest import run_fetch
from app.services.news.sources import SOURCE_BY_KEY
from app.services.news.validation import STATUS_FLAGGED

router = APIRouter()

CATEGORIES = nlp.CATEGORIES
EDITOR_ROLES = {"admin", "super_admin", "superadmin", "editor", "news_editor"}


async def _resolve_country(request: Request, country: Optional[str]) -> dict:
    forced = queries.valid_country(country)
    info = await detect_country(request, forced)
    info["has_local_sources"] = queries.has_local_sources(info["country"])
    return info


_bearer = HTTPBearer(auto_error=False)


async def current_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
                          session: AsyncSession = Depends(get_session)) -> int:
    """Validate the platform's JWT and return the user id.

    Uses Core queries (not the ORM User class) so it does not depend on the
    legacy relationship graph.
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("user_id") if payload else None
    if not user_id or not verify_token_not_expired(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    row = (await session.execute(
        select(User.__table__.c.status, User.__table__.c.deleted_at).where(User.__table__.c.id == user_id)
    )).first()
    if row is None or row.status != "active" or row.deleted_at is not None:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return int(user_id)


async def require_editor(user_id: int = Depends(current_user_id), session: AsyncSession = Depends(get_session)) -> int:
    roles, links = Role.__table__, user_roles
    rows = (await session.execute(
        select(roles.c.name, roles.c.permissions).join(links, links.c.role_id == roles.c.id)
        .where(links.c.user_id == user_id)
    )).all()
    if not any((name or "").lower() in EDITOR_ROLES or "news.review" in (perms or []) or "*" in (perms or [])
               for name, perms in rows):
        raise HTTPException(status_code=403, detail="Editor or admin role required")
    return user_id


@router.get("/location")
async def get_location(request: Request, country: Optional[str] = None):
    """Detected (or manually selected) country for this reader."""
    return await _resolve_country(request, country)


@router.get("/countries")
async def get_countries():
    return {"countries": queries.country_list()}


@router.get("/articles")
async def get_articles(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1, le=500),
    page_size: int = Query(12, ge=1, le=50),
    category: Optional[str] = Query(None, pattern="^[a-z]+$"),
    country: Optional[str] = Query(None, min_length=2, max_length=2),
    scope: str = Query("all", pattern="^(all|local)$"),
    source: Optional[str] = None,
    q: Optional[str] = Query(None, max_length=120),
    sort: str = Query("latest", pattern="^(latest|trending)$"),
    days: Optional[int] = Query(None, ge=1, le=60),
    include_flagged: bool = False,
):
    """Paginated articles. Local-country stories are ranked higher unless sort=trending."""
    if category and category not in CATEGORIES:
        raise HTTPException(status_code=422, detail=f"Unknown category: {category}")
    if source and source not in SOURCE_BY_KEY:
        raise HTTPException(status_code=422, detail=f"Unknown source: {source}")
    geo = await _resolve_country(request, country)

    key = f"list:{geo['country']}:{page}:{page_size}:{category}:{scope}:{source}:{q}:{sort}:{days}:{include_flagged}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await queries.list_articles(
        session, page=page, page_size=page_size, category=category, country=geo["country"], scope=scope,
        source=source, q=q, sort=sort, days=days, include_flagged=include_flagged,
    )
    data["location"] = geo
    await cache_set(key, data, ttl=60)
    return data


@router.get("/featured")
async def get_featured(request: Request, country: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    geo = await _resolve_country(request, country)
    key = f"featured:{geo['country']}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = {"items": await queries.featured(session, geo["country"]), "location": geo}
    await cache_set(key, data, ttl=120)
    return data


@router.get("/trending")
async def get_trending(request: Request, country: Optional[str] = None, limit: int = Query(8, ge=1, le=20),
                       session: AsyncSession = Depends(get_session)):
    geo = await _resolve_country(request, country)
    key = f"trending:{geo['country']}:{limit}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await queries.list_articles(session, page=1, page_size=limit, sort="trending", days=2)
    await cache_set(key, data, ttl=120)
    return data


@router.get("/categories")
async def get_categories(request: Request, country: Optional[str] = None, scope: str = Query("all", pattern="^(all|local)$"),
                         session: AsyncSession = Depends(get_session)):
    geo = await _resolve_country(request, country)
    key = f"cats:{geo['country']}:{scope}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = {"categories": await queries.category_counts(session, geo["country"], scope)}
    await cache_set(key, data, ttl=120)
    return data




@router.get("/status")
async def get_status():
    return {
        "nlp_engine": "spacy" if nlp.spacy_available() else "rules",
        "fetch_interval_minutes": settings.NEWS_FETCH_INTERVAL_MINUTES,
        "scheduler_enabled": settings.NEWS_ENABLE_SCHEDULER,
        "sources_configured": len(SOURCE_BY_KEY),
    }


@router.get("/articles/{article_id}")
async def get_article(article_id: int, session: AsyncSession = Depends(get_session)):
    article = await session.get(NewsArticle, article_id)
    if not queries.is_public(article):
        raise HTTPException(status_code=404, detail="Article not found")
    if article.enriched_at is None:  # not processed yet: fetch the page now so the reader sees the full story
        try:
            await asyncio.wait_for(enrich_one(article_id), timeout=20)
            await session.refresh(article)
        except (asyncio.TimeoutError, Exception):  # noqa: BLE001 - show the stored teaser instead
            pass
    return queries.article_to_dict(article)


@router.get("/articles/{article_id}/related")
async def get_related(article_id: int, limit: int = Query(6, ge=1, le=12), session: AsyncSession = Depends(get_session)):
    article = await session.get(NewsArticle, article_id)
    if not queries.is_public(article):
        raise HTTPException(status_code=404, detail="Article not found")
    return {"items": await queries.related(session, article, limit)}


@router.post("/articles/{article_id}/click")
async def record_click(article_id: int, session: AsyncSession = Depends(get_session)):
    """Count an outbound click; feeds the trending score."""
    result = await session.execute(
        update(NewsArticle).where(NewsArticle.id == article_id, NewsArticle.deleted_at.is_(None))
        .values(click_count=NewsArticle.click_count + 1)
    )
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"ok": True}


@router.post("/refresh", status_code=202)
async def refresh(background: BackgroundTasks, source: Optional[str] = None, user_id: int = Depends(current_user_id)):
    """Start a fetch of all (or one) sources in the background."""
    if source and source not in SOURCE_BY_KEY:
        raise HTTPException(status_code=422, detail=f"Unknown source: {source}")
    background.add_task(run_fetch, [source] if source else None, "manual", f"user:{user_id}")
    return {"status": "started", "source": source}


@router.post("/refresh/sync")
async def refresh_sync(source: Optional[str] = None, user_id: int = Depends(require_editor)):
    """Run a fetch and wait for the result (editors/admins)."""
    if source and source not in SOURCE_BY_KEY:
        raise HTTPException(status_code=422, detail=f"Unknown source: {source}")
    return await run_fetch([source] if source else None, "manual", f"user:{user_id}")


@router.get("/review")
async def review_queue(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=50),
                       user_id: int = Depends(require_editor), session: AsyncSession = Depends(get_session)):
    """Articles flagged or unverified and waiting for an editor."""
    from sqlalchemy import func
    conds = (NewsArticle.review_status == "pending",)
    total = (await session.execute(select(func.count()).select_from(NewsArticle).where(*conds))).scalar_one()
    rows = (await session.execute(
        select(NewsArticle).where(*conds).order_by(NewsArticle.published_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()
    return {"items": [queries.article_to_dict(r) for r in rows], "page": page, "page_size": page_size, "total": total}


class ReviewDecision(BaseModel):
    decision: str  # approved | rejected


@router.post("/articles/{article_id}/review")
async def review_article(article_id: int, body: ReviewDecision, user_id: int = Depends(require_editor),
                         session: AsyncSession = Depends(get_session)):
    if body.decision not in ("approved", "rejected"):
        raise HTTPException(status_code=422, detail="decision must be 'approved' or 'rejected'")
    article = await session.get(NewsArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.review_status = body.decision
    article.reviewed_by = user_id
    article.reviewed_at = datetime.now(timezone.utc)
    await session.commit()
    await cache_invalidate()
    return queries.article_to_dict(article)
