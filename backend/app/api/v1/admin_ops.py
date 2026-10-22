"""Admin operations: analytics, news-fetch monitoring and adverts."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_session
from app.models.news import NewsArticle as A, NewsFetchRun
from app.models.site import Advert, NewsFetchCycle
from app.services.news import ingest, queries, scheduler
from app.services.news.sources import SOURCE_BY_KEY
from app.services.site import adminauth as auth
from app.services.site import adverts as ads
from app.services.site import analytics

router = APIRouter()


# ---------------------------------------------------------------- analytics

@router.get("/analytics/summary")
async def analytics_summary(period: Literal["today", "7d", "30d", "90d", "12m"] = "7d",
                            ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    return await analytics.summary(db, period)


@router.get("/analytics/timeseries")
async def analytics_timeseries(granularity: Literal["day", "week", "month"] = "day",
                               ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    return await analytics.timeseries(db, granularity)


@router.get("/analytics/activity")
async def analytics_activity(ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    return await analytics.activity(db)


# --------------------------------------------------------------- news fetch

def _cycle(c: NewsFetchCycle) -> Dict[str, Any]:
    duration = (c.finished_at - c.started_at).total_seconds() if c.finished_at and c.started_at else None
    return {
        "id": c.id, "started_at": c.started_at.isoformat() if c.started_at else None,
        "finished_at": c.finished_at.isoformat() if c.finished_at else None,
        "duration_s": round(duration, 1) if duration is not None else None,
        "status": c.status, "trigger": c.trigger, "triggered_by": c.triggered_by,
        "sources_total": c.sources_total, "sources_ok": c.sources_ok, "sources_failed": c.sources_failed,
        "items_seen": c.items_seen, "items_new": c.items_new, "items_duplicate": c.items_duplicate,
        "items_rejected": c.items_rejected, "enriched": c.enriched, "error": c.error,
    }


@router.get("/news/status")
async def news_status(ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    cycles = (await db.execute(select(NewsFetchCycle).order_by(NewsFetchCycle.id.desc()).limit(15))).scalars().all()
    last_done = next((c for c in cycles if c.finished_at and c.status in ("completed", "partial")), None)
    day_ago = datetime.now(timezone.utc) - timedelta(hours=24)
    failed_24h = (await db.execute(select(func.count()).select_from(NewsFetchRun).where(
        NewsFetchRun.started_at > day_ago, NewsFetchRun.success.is_(False)))).scalar_one()
    requests_24h = (await db.execute(select(func.count()).select_from(NewsFetchRun).where(
        NewsFetchRun.started_at > day_ago))).scalar_one()
    new_24h = (await db.execute(select(func.coalesce(func.sum(NewsFetchRun.items_new), 0)).where(
        NewsFetchRun.started_at > day_ago))).scalar_one()
    total = (await db.execute(select(func.count()).select_from(A).where(A.deleted_at.is_(None)))).scalar_one()
    last_any = cycles[0] if cycles else None
    running = ingest.is_running()
    if running:
        state = "running"
    elif last_any is None:
        state = "never_run"
    else:
        state = {"completed": "healthy", "partial": "degraded", "failed": "failing"}.get(last_any.status, "unknown")
    return {
        "state": state, "running": running,
        "last_fetch_at": last_done.finished_at.isoformat() if last_done else None,
        "last_cycle": _cycle(last_any) if last_any else None,
        "scheduler": scheduler.status(),
        "articles_total": total, "articles_added_24h": int(new_24h),
        "requests_24h": requests_24h, "failed_requests_24h": failed_24h,
        "cycles": [_cycle(c) for c in cycles],
        "sources": await queries.source_stats(db),
    }


@router.post("/news/fetch", status_code=202)
async def start_fetch(source: Optional[str] = Query(None, max_length=64),
                      ctx: auth.AdminCtx = Depends(auth.require_admin), db: AsyncSession = Depends(get_session)):
    if source and source not in SOURCE_BY_KEY:
        raise HTTPException(status_code=422, detail=f"Unknown source: {source}")
    if ingest.is_running():
        raise HTTPException(status_code=409, detail="A fetch is already running")
    auth.audit(db, ctx, "news.fetch", "news", source or "all", {})
    await db.commit()
    ingest.start_background([source] if source else None, "manual", ctx.email)
    return {"status": "started", "source": source}


# ------------------------------------------------------------------ adverts

class AdvertIn(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    image_url: str = Field(min_length=1, max_length=2048)
    destination_url: str = Field(min_length=1, max_length=2048)
    alt_text: str = Field("", max_length=200)
    placements: List[str] = Field(default_factory=list, max_length=len(ads.PLACEMENTS))
    is_active: bool = True
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    weight: int = Field(1, ge=1, le=10)


class AdvertPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=160)
    image_url: Optional[str] = Field(None, min_length=1, max_length=2048)
    destination_url: Optional[str] = Field(None, min_length=1, max_length=2048)
    alt_text: Optional[str] = Field(None, max_length=200)
    placements: Optional[List[str]] = Field(None, max_length=len(ads.PLACEMENTS))
    is_active: Optional[bool] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    weight: Optional[int] = Field(None, ge=1, le=10)


def _aware(value: Optional[datetime]) -> Optional[datetime]:
    return value.replace(tzinfo=timezone.utc) if value and value.tzinfo is None else value


@router.get("/ads/placements")
async def ad_placements(ctx: auth.AdminCtx = Depends(auth.require_staff)):
    return {"placements": [{"key": k, "label": v} for k, v in ads.PLACEMENTS.items()]}


@router.get("/ads")
async def list_ads(state: Optional[Literal["live", "scheduled", "expired", "inactive"]] = None,
                   q: Optional[str] = Query(None, max_length=80),
                   ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(Advert).order_by(Advert.id.desc()))).scalars().all()
    items = [ads.to_dict(a) for a in rows]
    if state:
        items = [i for i in items if i["state"] == state]
    if q:
        needle = q.strip().lower()
        items = [i for i in items if needle in i["advert_id"].lower() or needle in i["name"].lower()]
    return {"items": items, "total": len(items)}


@router.post("/ads/upload", status_code=201)
async def upload_ad_image(file: UploadFile = File(...), ctx: auth.AdminCtx = Depends(auth.require_staff),
                          db: AsyncSession = Depends(get_session)):
    data = await file.read(ads.MAX_UPLOAD + 1)
    url = ads.store_image(data)
    auth.audit(db, ctx, "ad.upload", "advert", "", {"file": url, "bytes": len(data)})
    await db.commit()
    return {"image_url": url, "image_src": ads.absolute_image(url)}


@router.post("/ads", status_code=201)
async def create_ad(body: AdvertIn, ctx: auth.AdminCtx = Depends(auth.require_staff),
                    db: AsyncSession = Depends(get_session)):
    starts, ends = _aware(body.starts_at), _aware(body.ends_at)
    ads.check_schedule(starts, ends)
    for _ in range(8):  # collisions are astronomically unlikely, but IDs must be unique
        advert_id = ads.new_advert_id()
        if not (await db.execute(select(Advert.id).where(Advert.advert_id == advert_id))).first():
            break
    else:
        raise HTTPException(status_code=500, detail="Could not allocate an advert ID")
    ad = Advert(
        advert_id=advert_id, name=body.name.strip(), image_url=ads.valid_image(body.image_url),
        destination_url=ads.valid_destination(body.destination_url), alt_text=body.alt_text.strip(),
        placements=ads.valid_placements(body.placements), is_active=body.is_active,
        starts_at=starts, ends_at=ends, weight=body.weight,
    )
    db.add(ad)
    await db.flush()
    auth.audit(db, ctx, "ad.create", "advert", ad.advert_id, {"name": ad.name, "placements": ad.placements})
    await db.commit()
    return ads.to_dict(ad)


@router.patch("/ads/{advert_id}")
async def update_ad(advert_id: str, body: AdvertPatch, ctx: auth.AdminCtx = Depends(auth.require_staff),
                    db: AsyncSession = Depends(get_session)):
    ad = (await db.execute(select(Advert).where(Advert.advert_id == advert_id))).scalar_one_or_none()
    if not ad:
        raise HTTPException(status_code=404, detail="Advert not found")
    changes = body.model_dump(exclude_unset=True)
    if "starts_at" in changes:
        changes["starts_at"] = _aware(changes["starts_at"])
    if "ends_at" in changes:
        changes["ends_at"] = _aware(changes["ends_at"])
    ads.check_schedule(changes.get("starts_at", ad.starts_at), changes.get("ends_at", ad.ends_at))
    if "name" in changes:
        changes["name"] = changes["name"].strip()
    if "image_url" in changes:
        changes["image_url"] = ads.valid_image(changes["image_url"])
    if "destination_url" in changes:
        changes["destination_url"] = ads.valid_destination(changes["destination_url"])
    if "placements" in changes:
        changes["placements"] = ads.valid_placements(changes["placements"])
    for key in ("name", "is_active", "weight", "placements"):
        if key in changes and changes[key] is None:
            raise HTTPException(status_code=422, detail=f"{key} cannot be empty")
    diff = {}
    for key, new in changes.items():
        old = getattr(ad, key)
        if old != new:
            diff[key] = [str(old) if isinstance(old, datetime) else old, str(new) if isinstance(new, datetime) else new]
            setattr(ad, key, new)
    if diff:
        auth.audit(db, ctx, "ad.update", "advert", ad.advert_id, diff)
        await db.commit()
    return ads.to_dict(ad)


@router.delete("/ads/{advert_id}")
async def delete_ad(advert_id: str, ctx: auth.AdminCtx = Depends(auth.require_staff),
                    db: AsyncSession = Depends(get_session)):
    ad = (await db.execute(select(Advert).where(Advert.advert_id == advert_id))).scalar_one_or_none()
    if not ad:
        raise HTTPException(status_code=404, detail="Advert not found")
    auth.audit(db, ctx, "ad.delete", "advert", ad.advert_id, {"name": ad.name, "impressions": ad.impressions,
                                                              "clicks": ad.clicks})
    await db.delete(ad)
    await db.commit()
    return {"ok": True}
