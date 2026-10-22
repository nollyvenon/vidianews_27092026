"""Advert rules: placements, scheduling, validation, image uploads and selection."""

import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.site import Advert

PLACEMENTS = {
    "home_top": "Home page — top banner",
    "home_sidebar": "Home page — sidebar",
    "category_top": "Category pages — top banner",
    "article_top": "Article — above the text",
    "article_inline": "Article — inside the text",
    "article_bottom": "Article — below the text",
}
MAX_UPLOAD = 2 * 1024 * 1024
_ID_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O/1/I


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def new_advert_id() -> str:
    return "AD-" + "".join(secrets.choice(_ID_ALPHABET) for _ in range(8))


def valid_destination(url: str) -> str:
    url = (url or "").strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or len(url) > 2048:
        raise HTTPException(status_code=422, detail="Destination must be a full http(s) URL")
    return url


def valid_image(url: str) -> str:
    url = (url or "").strip()
    if url.startswith("/media/ads/") and ".." not in url and len(url) < 200:
        return url
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or len(url) > 2048:
        raise HTTPException(status_code=422, detail="Image must be an uploaded file or an https URL")
    return url


def valid_placements(values: List[str]) -> List[str]:
    clean = sorted({v for v in values or []})
    if not clean:
        raise HTTPException(status_code=422, detail="Choose at least one placement")
    bad = [v for v in clean if v not in PLACEMENTS]
    if bad:
        raise HTTPException(status_code=422, detail=f"Unknown placement: {', '.join(bad)}")
    return clean


def check_schedule(starts: Optional[datetime], ends: Optional[datetime]) -> None:
    if starts and ends and ends <= starts:
        raise HTTPException(status_code=422, detail="The end date must be after the start date")


def advert_state(ad: Advert, at: Optional[datetime] = None) -> str:
    """inactive | scheduled | expired | live"""
    at = at or now_utc()
    if not ad.is_active:
        return "inactive"
    if ad.starts_at and ad.starts_at > at:
        return "scheduled"
    if ad.ends_at and ad.ends_at <= at:
        return "expired"
    return "live"


def detect_image_type(head: bytes) -> Optional[str]:
    """Extension from the file's magic bytes (never from the client-supplied name or type)."""
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None


def upload_dir() -> Path:
    path = Path(settings.UPLOAD_DIR) / "ads"
    path.mkdir(parents=True, exist_ok=True)
    return path


def store_image(data: bytes) -> str:
    if not data:
        raise HTTPException(status_code=422, detail="The file is empty")
    if len(data) > MAX_UPLOAD:
        raise HTTPException(status_code=413, detail="Images are limited to 2 MB")
    ext = detect_image_type(data[:16])
    if not ext:
        raise HTTPException(status_code=415, detail="Upload a PNG, JPEG, GIF or WebP image")
    name = f"{secrets.token_hex(12)}.{ext}"
    (upload_dir() / name).write_bytes(data)
    return f"/media/ads/{name}"


def absolute_image(url: str) -> str:
    """Uploaded files are served by the API; external URLs are used as they are."""
    return url if url.startswith("http") else f"{settings.PUBLIC_API_URL.rstrip('/')}{url}"


def to_dict(ad: Advert) -> Dict[str, Any]:
    state = advert_state(ad)
    return {
        "id": ad.id, "advert_id": ad.advert_id, "name": ad.name, "image_url": ad.image_url,
        "image_src": absolute_image(ad.image_url), "destination_url": ad.destination_url,
        "alt_text": ad.alt_text, "placements": ad.placements or [], "is_active": ad.is_active,
        "starts_at": ad.starts_at.isoformat() if ad.starts_at else None,
        "ends_at": ad.ends_at.isoformat() if ad.ends_at else None,
        "weight": ad.weight, "impressions": ad.impressions, "clicks": ad.clicks,
        "ctr": round(ad.clicks / ad.impressions * 100, 2) if ad.impressions else 0,
        "state": state, "created_at": ad.created_at.isoformat() if ad.created_at else None,
    }


async def pick_for_placement(db: AsyncSession, placement: str) -> Optional[Advert]:
    """One live advert for the slot, chosen at random in proportion to its weight."""
    at = now_utc()
    rows = (await db.execute(select(Advert).where(
        Advert.is_active.is_(True),
        or_(Advert.starts_at.is_(None), Advert.starts_at <= at),
        or_(Advert.ends_at.is_(None), Advert.ends_at > at),
    ))).scalars().all()
    live = [a for a in rows if placement in (a.placements or [])]
    if not live:
        return None
    return secrets.SystemRandom().choices(live, weights=[max(1, a.weight) for a in live], k=1)[0]
