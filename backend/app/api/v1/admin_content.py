"""Admin content management: news articles and static pages."""

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.news import NewsArticle as A
from app.models.site import SitePage
from app.services.news import nlp, queries
from app.services.news.cache import cache_invalidate
from app.services.news.enrich import clean_image_url
from app.services.site import adminauth as auth

router = APIRouter()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _status(a: A) -> str:
    if a.deleted_at:
        return "deleted"
    return "published" if a.is_published else "unpublished"


def _row(a: A) -> Dict[str, Any]:
    return {
        "id": a.id, "title": a.title, "source": a.source_name, "category": a.category,
        "published_at": a.published_at.isoformat() if a.published_at else None,
        "status": _status(a), "has_image": bool(a.image_url), "clicks": a.click_count or 0,
        "validation": a.validation_status, "review_status": a.review_status,
        "edited_at": a.edited_at.isoformat() if a.edited_at else None, "edited_by": a.edited_by,
    }


def _detail(a: A) -> Dict[str, Any]:
    return {
        **_row(a), "url": a.url, "summary": a.summary, "description": a.description,
        "body_text": "\n\n".join(queries.article_body(a)), "image_url": a.image_url,
        "image_credit": a.image_credit, "meta_title": a.meta_title, "meta_description": a.meta_description,
        "keywords": a.keywords or [], "is_published": a.is_published,
    }


@router.get("/articles")
async def list_articles(
    page: int = Query(1, ge=1, le=2000), page_size: int = Query(25, ge=1, le=100),
    q: Optional[str] = Query(None, max_length=120),
    status: Literal["all", "published", "unpublished", "deleted"] = "all",
    category: Optional[str] = Query(None, pattern="^[a-z]+$"),
    ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session),
):
    conds = []
    if status == "deleted":
        conds.append(A.deleted_at.is_not(None))
    else:
        conds.append(A.deleted_at.is_(None))
        if status == "published":
            conds.append(A.is_published.is_(True))
        elif status == "unpublished":
            conds.append(A.is_published.is_(False))
    if category:
        conds.append(A.category == category)
    if q:
        term = "%" + q.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        matches = [A.title.ilike(term), A.source_name.ilike(term)]
        if q.strip().isdigit() and len(q.strip()) < 10:
            matches.append(A.id == int(q.strip()))
        conds.append(or_(*matches))
    total = (await db.execute(select(func.count()).select_from(A).where(*conds))).scalar_one()
    rows = (await db.execute(select(A).where(*conds).order_by(A.published_at.desc(), A.id.desc())
                             .offset((page - 1) * page_size).limit(page_size))).scalars().all()
    return {"items": [_row(r) for r in rows], "total": total, "page": page, "page_size": page_size,
            "total_pages": max(1, -(-total // page_size)), "categories": nlp.CATEGORIES}


async def _get(db: AsyncSession, article_id: int) -> A:
    article = await db.get(A, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/articles/{article_id}")
async def get_article(article_id: int, ctx: auth.AdminCtx = Depends(auth.require_staff),
                      db: AsyncSession = Depends(get_session)):
    return _detail(await _get(db, article_id))


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=500)
    summary: Optional[str] = Field(None, max_length=3000)
    description: Optional[str] = Field(None, max_length=3000)
    body_text: Optional[str] = Field(None, max_length=60000)
    category: Optional[str] = Field(None, max_length=32)
    image_url: Optional[str] = Field(None, max_length=2048)
    image_credit: Optional[str] = Field(None, max_length=500)
    meta_title: Optional[str] = Field(None, max_length=200)
    meta_description: Optional[str] = Field(None, max_length=320)
    is_published: Optional[bool] = None
    review_status: Optional[Literal["none", "approved", "rejected"]] = None


def _short(value: Any) -> Any:
    return value[:1000] + "…" if isinstance(value, str) and len(value) > 1000 else value


@router.patch("/articles/{article_id}")
async def update_article(article_id: int, body: ArticleUpdate, ctx: auth.AdminCtx = Depends(auth.require_staff),
                         db: AsyncSession = Depends(get_session)):
    article = await _get(db, article_id)
    if article.deleted_at:
        raise HTTPException(status_code=409, detail="Restore the article before editing it")
    changes = body.model_dump(exclude_unset=True)
    values: Dict[str, Any] = {}
    for key, value in changes.items():
        if isinstance(value, str):
            value = value.replace("\r\n", "\n").strip()
        if key in ("title", "category", "is_published", "review_status") and value in (None, ""):
            raise HTTPException(status_code=422, detail=f"{key} cannot be empty")
        if key == "category" and value not in nlp.CATEGORIES:
            raise HTTPException(status_code=422, detail=f"Unknown category: {value}")
        if key == "image_url" and value:
            if not (value.startswith("/media/") or clean_image_url(value)):
                raise HTTPException(status_code=422, detail="Image must be an http(s) URL")
        if key == "body_text":
            if value and len(value) < 40:
                raise HTTPException(status_code=422, detail="Article text is too short")
            values["full_content"] = value or None
            values["content"] = value or article.content
            continue
        values[key] = value or None if key not in ("is_published",) else value
    if not values:
        return _detail(article)
    diff = {}
    for key, new in values.items():
        old = getattr(article, key)
        if old != new:
            diff[key] = [_short(old), _short(new)]
            setattr(article, key, new)
    if diff:
        article.edited_at, article.edited_by = _now(), ctx.email
        auth.audit(db, ctx, "article.update", "article", article.id, diff)
        await db.commit()
        await cache_invalidate()
    return _detail(article)


@router.post("/articles/{article_id}/publish")
async def publish_article(article_id: int, ctx: auth.AdminCtx = Depends(auth.require_staff),
                          db: AsyncSession = Depends(get_session)):
    return await _set_published(db, ctx, article_id, True)


@router.post("/articles/{article_id}/unpublish")
async def unpublish_article(article_id: int, ctx: auth.AdminCtx = Depends(auth.require_staff),
                            db: AsyncSession = Depends(get_session)):
    return await _set_published(db, ctx, article_id, False)


async def _set_published(db: AsyncSession, ctx: auth.AdminCtx, article_id: int, value: bool) -> Dict[str, Any]:
    article = await _get(db, article_id)
    if article.deleted_at:
        raise HTTPException(status_code=409, detail="Restore the article first")
    if article.is_published != value:
        article.is_published = value
        article.edited_at, article.edited_by = _now(), ctx.email
        auth.audit(db, ctx, "article.publish" if value else "article.unpublish", "article", article.id,
                   {"title": _short(article.title)})
        await db.commit()
        await cache_invalidate()
    return _row(article)


@router.delete("/articles/{article_id}")
async def delete_article(article_id: int, ctx: auth.AdminCtx = Depends(auth.require_staff),
                         db: AsyncSession = Depends(get_session)):
    """Soft delete: the row stays so the same story is not fetched again."""
    article = await _get(db, article_id)
    if not article.deleted_at:
        article.deleted_at = _now()
        article.edited_at, article.edited_by = _now(), ctx.email
        article.is_featured = False
        auth.audit(db, ctx, "article.delete", "article", article.id, {"title": _short(article.title)})
        await db.commit()
        await cache_invalidate()
    return _row(article)


@router.post("/articles/{article_id}/restore")
async def restore_article(article_id: int, ctx: auth.AdminCtx = Depends(auth.require_staff),
                          db: AsyncSession = Depends(get_session)):
    article = await _get(db, article_id)
    if article.deleted_at:
        article.deleted_at = None
        article.is_published = False  # comes back as a draft; publish it deliberately
        article.edited_at, article.edited_by = _now(), ctx.email
        auth.audit(db, ctx, "article.restore", "article", article.id, {"title": _short(article.title)})
        await db.commit()
        await cache_invalidate()
    return _row(article)


# ------------------------------------------------------------------- pages

_SLUG = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"


def _page(p: SitePage) -> Dict[str, Any]:
    return {"id": p.id, "slug": p.slug, "title": p.title, "body": p.body, "meta_description": p.meta_description,
            "is_published": p.is_published, "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            "updated_by": p.updated_by}


class PageIn(BaseModel):
    slug: str = Field(min_length=1, max_length=80, pattern=_SLUG)
    title: str = Field(min_length=1, max_length=200)
    body: str = Field("", max_length=100000)
    meta_description: Optional[str] = Field(None, max_length=320)
    is_published: bool = True


class PagePatch(BaseModel):
    slug: Optional[str] = Field(None, min_length=1, max_length=80, pattern=_SLUG)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = Field(None, max_length=100000)
    meta_description: Optional[str] = Field(None, max_length=320)
    is_published: Optional[bool] = None


@router.get("/pages")
async def list_pages(ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(SitePage).order_by(SitePage.slug))).scalars().all()
    return {"items": [_page(p) for p in rows]}


@router.post("/pages", status_code=201)
async def create_page(body: PageIn, ctx: auth.AdminCtx = Depends(auth.require_staff),
                      db: AsyncSession = Depends(get_session)):
    if (await db.execute(select(SitePage.id).where(SitePage.slug == body.slug))).first():
        raise HTTPException(status_code=409, detail="A page with this address already exists")
    page = SitePage(**body.model_dump(), updated_by=ctx.email)
    db.add(page)
    await db.flush()
    auth.audit(db, ctx, "page.create", "page", page.id, {"slug": page.slug})
    await db.commit()
    return _page(page)


@router.patch("/pages/{page_id}")
async def update_page(page_id: int, body: PagePatch, ctx: auth.AdminCtx = Depends(auth.require_staff),
                      db: AsyncSession = Depends(get_session)):
    page = await db.get(SitePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    changes = body.model_dump(exclude_unset=True)
    if "slug" in changes and changes["slug"] != page.slug and (await db.execute(
            select(SitePage.id).where(SitePage.slug == changes["slug"]))).first():
        raise HTTPException(status_code=409, detail="A page with this address already exists")
    diff = {}
    for key, new in changes.items():
        if getattr(page, key) != new:
            diff[key] = [_short(getattr(page, key)), _short(new)]
            setattr(page, key, new)
    if diff:
        page.updated_by = ctx.email
        auth.audit(db, ctx, "page.update", "page", page.id, diff)
        await db.commit()
    return _page(page)


@router.delete("/pages/{page_id}")
async def delete_page(page_id: int, ctx: auth.AdminCtx = Depends(auth.require_admin),
                      db: AsyncSession = Depends(get_session)):
    page = await db.get(SitePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    auth.audit(db, ctx, "page.delete", "page", page.id, {"slug": page.slug, "title": page.title})
    await db.delete(page)
    await db.commit()
    return {"ok": True}
