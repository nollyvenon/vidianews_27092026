"""Public site API: anonymous page-view tracking, adverts, editable pages, settings, sitemap data."""

import json
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_session
from app.models.news import NewsArticle as A
from app.models.site import Advert, SitePage
from app.services.news.geo import client_ip, detect_country
from app.services.site import adverts as ads
from app.services.site import analytics
from app.services.site.sitesettings import load_settings, public_settings

router = APIRouter()


class TrackBody(BaseModel):
    path: str = Field(max_length=400)
    referrer: Optional[str] = Field(None, max_length=600)


async def _store_view(request: Request, path: str, visitor: str, referrer: Optional[str], ua: str) -> None:
    try:
        geo = await detect_country(request)
        country = geo["country"] if geo.get("country") != "XX" else None
        await analytics.record_view(
            path=path, visitor=visitor, country=country, referrer=referrer, user_agent=ua,
            own_host=(urlparse(settings.SITE_URL).hostname or None),
        )
    except Exception:  # noqa: BLE001 - analytics must never surface errors to readers
        pass


@router.post("/track", status_code=204)
async def track(body: TrackBody, request: Request, background: BackgroundTasks):
    """Record one anonymous page view. Honours Do Not Track / Global Privacy Control."""
    site = await load_settings()
    ua = request.headers.get("user-agent", "")
    path = analytics.clean_path(body.path)
    skip = (
        not site["analytics_enabled"] or path is None or analytics.is_bot(ua)
        or (site["respect_dnt"] and (request.headers.get("dnt") == "1" or request.headers.get("sec-gpc") == "1"))
    )
    if skip:
        return Response(status_code=204)
    ip = client_ip(request) or "unknown"
    visitor = analytics.visitor_key(ip, ua)
    if analytics.rate_limited(visitor):
        return Response(status_code=204)
    background.add_task(_store_view, request, path, visitor, body.referrer, ua)
    return Response(status_code=204)


@router.get("/settings")
async def get_settings(response: Response):
    response.headers["Cache-Control"] = "public, max-age=60"
    return public_settings(await load_settings())


def _page(p: SitePage) -> Dict[str, Any]:
    return {"slug": p.slug, "title": p.title, "body": p.body, "meta_description": p.meta_description,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None}


@router.get("/pages")
async def list_pages(db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(SitePage).where(SitePage.is_published.is_(True)).order_by(SitePage.title))).scalars()
    return {"items": [{"slug": p.slug, "title": p.title} for p in rows]}


@router.get("/pages/{slug}")
async def get_page(slug: str, db: AsyncSession = Depends(get_session)):
    page = (await db.execute(select(SitePage).where(SitePage.slug == slug, SitePage.is_published.is_(True)))).scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return _page(page)


@router.get("/sitemap")
async def sitemap(db: AsyncSession = Depends(get_session)):
    """Everything a crawler may index: published stories (newest first) and static pages."""
    articles = (await db.execute(
        select(A.id, A.title, A.published_at, A.edited_at, A.category)
        .where(A.is_published.is_(True), A.deleted_at.is_(None), A.review_status != "rejected")
        .order_by(A.published_at.desc()).limit(45000)
    )).all()
    pages = (await db.execute(select(SitePage.slug, SitePage.updated_at).where(SitePage.is_published.is_(True)))).all()
    categories = sorted({a.category for a in articles})
    return {
        "articles": [{"id": a.id, "title": a.title, "category": a.category,
                      "modified": (a.edited_at or a.published_at).isoformat()} for a in articles],
        "pages": [{"slug": s, "modified": u.isoformat() if u else None} for s, u in pages],
        "categories": categories,
    }


# ------------------------------------------------------------------ adverts

@router.get("/ads")
async def serve_ad(request: Request, placement: str = Query(..., max_length=32),
                   db: AsyncSession = Depends(get_session)):
    """One live advert for a slot. Counting the impression here is accurate because the
    slot component calls this only when it is shown to a reader."""
    if placement not in ads.PLACEMENTS or not (await load_settings(db))["ads_enabled"]:
        return Response(content='{"ad":null}', media_type="application/json", headers={"Cache-Control": "no-store"})
    ad = await ads.pick_for_placement(db, placement)
    if not ad:
        return Response(content='{"ad":null}', media_type="application/json", headers={"Cache-Control": "no-store"})
    if not analytics.is_bot(request.headers.get("user-agent")):
        await db.execute(update(Advert).where(Advert.id == ad.id).values(impressions=Advert.impressions + 1))
        await db.commit()
    return Response(
        content=json.dumps({"ad": {
            "advert_id": ad.advert_id, "image_src": ads.absolute_image(ad.image_url), "alt_text": ad.alt_text,
            "click_url": f"{settings.PUBLIC_API_URL.rstrip('/')}{settings.API_PREFIX}/site/ads/{ad.advert_id}/click",
        }}),
        media_type="application/json", headers={"Cache-Control": "no-store"})


@router.get("/ads/{advert_id}/click")
async def ad_click(advert_id: str, request: Request, db: AsyncSession = Depends(get_session)):
    ad = (await db.execute(select(Advert).where(Advert.advert_id == advert_id))).scalar_one_or_none()
    if not ad or not ads.valid_destination(ad.destination_url):
        raise HTTPException(status_code=404, detail="Advert not found")
    if not analytics.is_bot(request.headers.get("user-agent")) and ads.advert_state(ad) == "live":
        await db.execute(update(Advert).where(Advert.id == ad.id).values(clicks=Advert.clicks + 1))
        await db.commit()
    return RedirectResponse(ad.destination_url, status_code=302, headers={"Cache-Control": "no-store"})
