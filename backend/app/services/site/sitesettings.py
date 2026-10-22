"""Site settings stored in the database, with validated types and defaults, and
the default editable pages created on first run."""

import time
from typing import Any, Dict, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.site import SitePage, SiteSetting

# key -> (type, default, max length / max value, public)
DEFINITIONS: Dict[str, tuple] = {
    "site_name": (str, "VidiaNews", 80, True),
    "site_tagline": (str, "News from trusted sources, in one place", 140, True),
    "site_description": (
        str,
        "Headlines and summaries from newspapers and broadcasters across Africa and the world, "
        "organised by topic and country, with links to the original reports.",
        320, True),
    "default_og_image": (str, "", 2048, True),  # absolute https URL used when a page has no image of its own
    "twitter_handle": (str, "", 40, True),
    "contact_email": (str, "", 255, True),
    "analytics_enabled": (bool, True, None, False),
    "respect_dnt": (bool, True, None, False),  # skip tracking when the browser sends Do Not Track / GPC
    "analytics_retention_days": (int, 395, 3650, False),
    "ads_enabled": (bool, True, None, False),  # global switch for every advert
    # stories with less article text than this are held back from the public site
    "news_min_content_chars": (int, settings.NEWS_MIN_CONTENT_CHARS, 5000, False),
}

_cache: Dict[str, Any] = {}
_cache_at = 0.0
_TTL = 20.0


def _coerce(key: str, value: Any) -> Any:
    if key not in DEFINITIONS:
        raise HTTPException(status_code=422, detail=f"Unknown setting: {key}")
    kind, _default, limit, _public = DEFINITIONS[key]
    if kind is bool:
        if not isinstance(value, bool):
            raise HTTPException(status_code=422, detail=f"{key} must be true or false")
        return value
    if kind is int:
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= limit:
            raise HTTPException(status_code=422, detail=f"{key} must be a whole number between 1 and {limit}")
        return value
    if not isinstance(value, str):
        raise HTTPException(status_code=422, detail=f"{key} must be text")
    value = value.strip()
    if len(value) > limit:
        raise HTTPException(status_code=422, detail=f"{key} is limited to {limit} characters")
    if key == "default_og_image" and value and not value.lower().startswith(("https://", "http://")):
        raise HTTPException(status_code=422, detail="default_og_image must be an http(s) URL")
    if key == "site_name" and not value:
        raise HTTPException(status_code=422, detail="site_name cannot be empty")
    return value


async def load_settings(db: Optional[AsyncSession] = None, fresh: bool = False) -> Dict[str, Any]:
    global _cache, _cache_at
    if not fresh and _cache and time.monotonic() - _cache_at < _TTL:
        return dict(_cache)

    async def read(session: AsyncSession) -> Dict[str, Any]:
        stored = dict((await session.execute(select(SiteSetting.key, SiteSetting.value))).all())
        out = {}
        for key, (kind, default, _limit, _public) in DEFINITIONS.items():
            value = stored.get(key, default)
            out[key] = value if isinstance(value, kind) else default
        return out

    try:
        if db is not None:
            data = await read(db)
        else:
            async with AsyncSessionLocal() as session:
                data = await read(session)
    except Exception:  # noqa: BLE001 - settings must never take the site down
        return {k: v[1] for k, v in DEFINITIONS.items()}
    _cache, _cache_at = data, time.monotonic()
    return dict(data)


def public_settings(all_settings: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in all_settings.items() if DEFINITIONS[k][3]}


async def save_settings(db: AsyncSession, changes: Dict[str, Any], who: str) -> Dict[str, Any]:
    global _cache_at
    clean = {k: _coerce(k, v) for k, v in changes.items()}
    existing = {s.key: s for s in (await db.execute(
        select(SiteSetting).where(SiteSetting.key.in_(list(clean)))
    )).scalars()}
    for key, value in clean.items():
        row = existing.get(key)
        if row:
            row.value, row.updated_by = value, who
        else:
            db.add(SiteSetting(key=key, value=value, updated_by=who))
    await db.flush()
    _cache_at = 0.0
    return clean


DEFAULT_PAGES = [
    {
        "slug": "about",
        "title": "About",
        "meta_description": "What this site is, where its stories come from and how it works.",
        "body": (
            "This site collects headlines and short summaries from the public RSS feeds of newspapers and "
            "broadcasters, and groups them by topic and country.\n\n"
            "## Where the stories come from\n\n"
            "Every story links back to the publisher that wrote it. We show the publisher's name, the "
            "headline, a summary and the text we can read from the public page, and we credit the images "
            "that go with it. To read the full report, open the original article.\n\n"
            "## How stories are selected\n\n"
            "Stories are checked automatically for duplicates and for wording that suggests unconfirmed "
            "claims. Anything doubtful is marked or held back until an editor has reviewed it."
        ),
    },
    {
        "slug": "privacy",
        "title": "Privacy policy",
        "meta_description": "What visitor information this site records, and what it does not.",
        "body": (
            "We measure how the site is used so we can improve it. We do this without tracking you as a person.\n\n"
            "## What we record\n\n"
            "For each page you open we record the page address, the time, your country, the website you came "
            "from, and whether you use a phone, tablet or computer.\n\n"
            "## What we do not record\n\n"
            "We do not store your IP address, set tracking cookies, or build a profile of you. To count "
            "visitors we create a short code from your connection details that is replaced every day, so we "
            "cannot recognise you from one day to the next.\n\n"
            "## Your choices\n\n"
            "If your browser sends a Do Not Track or Global Privacy Control signal, we do not record your visit."
        ),
    },
]


async def seed_default_pages() -> None:
    try:
        async with AsyncSessionLocal() as db:
            have = set((await db.execute(select(SitePage.slug))).scalars())
            if have:
                return
            for page in DEFAULT_PAGES:
                db.add(SitePage(**page, updated_by="system"))
            await db.commit()
    except Exception:  # noqa: BLE001
        pass
