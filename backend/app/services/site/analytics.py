"""Privacy-conscious website analytics.

Stored per view: path, time, country, referrer *host*, traffic-source class and
device class. Never stored: IP address, user agent, cookies, or anything that can
follow a person from one day to the next (the visitor key is salted with the date).
"""

import hashlib
import hmac
import re
import time
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from sqlalchemy import and_, delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.news import NewsArticle
from app.models.site import PageView
from app.services.news.sources import country_name

VISIT_GAP = timedelta(minutes=30)

_BOT = re.compile(
    r"bot|crawl|spider|slurp|headless|lighthouse|pingdom|uptime|monitor|facebookexternalhit|preview|"
    r"curl|wget|python-|httpx|go-http|java/|okhttp|libwww|scrapy|axios|node-fetch|postman", re.I)
_TABLET = re.compile(r"ipad|tablet|kindle|silk|(android(?!.*mobile))", re.I)
_MOBILE = re.compile(r"mobi|iphone|ipod|android|windows phone|blackberry|opera mini", re.I)

SEARCH_HOSTS = ("google.", "bing.", "duckduckgo.", "yahoo.", "baidu.", "yandex.", "ecosia.", "startpage.", "brave.com", "qwant.")
SOCIAL_HOSTS = (
    "facebook.", "fb.com", "fb.me", "instagram.", "twitter.", "t.co", "x.com", "linkedin.", "lnkd.in", "reddit.",
    "youtube.", "youtu.be", "whatsapp.", "wa.me", "telegram.", "t.me", "tiktok.", "pinterest.", "threads.net",
)

_visit_cache: Dict[str, float] = {}  # visitor -> last view (monotonic), avoids a query per view
_rate: Dict[str, List[float]] = defaultdict(list)


def is_bot(user_agent: Optional[str]) -> bool:
    return not user_agent or bool(_BOT.search(user_agent))


def device_class(user_agent: str) -> str:
    if _TABLET.search(user_agent):
        return "tablet"
    return "mobile" if _MOBILE.search(user_agent) else "desktop"


def clean_path(path: Any) -> Optional[str]:
    """Normalise to a bare path (no query/fragment/host). None if not trackable."""
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//") or len(path) > 300:
        return None
    path = re.split(r"[?#]", path, maxsplit=1)[0]
    if re.search(r"[\x00-\x1f\s<>\"']", path):
        return None
    if path.startswith(("/admin", "/api", "/_next")):
        return None
    return path.rstrip("/") or "/"


def referrer_host(referrer: Any) -> Optional[str]:
    if not isinstance(referrer, str) or not referrer:
        return None
    try:
        host = (urlparse(referrer[:500]).hostname or "").lower()
    except ValueError:
        return None
    host = host[4:] if host.startswith("www.") else host
    return host[:255] or None


def classify_source(host: Optional[str], own_host: Optional[str]) -> str:
    if not host:
        return "direct"
    own = (own_host or "").lower().removeprefix("www.")
    if own and (host == own or host.endswith("." + own)):
        return "internal"
    if any(h in host for h in SEARCH_HOSTS):
        return "search"
    if any(host == h.strip(".") or h in host for h in SOCIAL_HOSTS):
        return "social"
    return "referral"


def visitor_key(ip: str, user_agent: str, day: Optional[date] = None) -> str:
    """Daily-rotating anonymous key: the same browser gets a different key tomorrow."""
    day = day or datetime.now(timezone.utc).date()
    salt = hmac.new(settings.SECRET_KEY.encode(), day.isoformat().encode(), hashlib.sha256).digest()
    return hmac.new(salt, f"{ip}|{user_agent}".encode(), hashlib.sha256).hexdigest()[:16]


def rate_limited(key: str, limit: int = 90, window: float = 60.0) -> bool:
    now = time.monotonic()
    hits = [t for t in _rate[key] if now - t < window]
    hits.append(now)
    _rate[key] = hits
    if len(_rate) > 5000:
        for k in [k for k, v in _rate.items() if not v or now - v[-1] > window]:
            _rate.pop(k, None)
    return len(hits) > limit


async def record_view(*, path: str, visitor: str, country: Optional[str], referrer: Optional[str],
                      user_agent: str, own_host: Optional[str]) -> None:
    host = referrer_host(referrer)
    source = classify_source(host, own_host)
    now = datetime.now(timezone.utc)
    mono = time.monotonic()
    async with AsyncSessionLocal() as db:
        last = _visit_cache.get(visitor)
        if last is None:  # not seen by this process recently: ask the database
            seen = (await db.execute(
                select(func.max(PageView.ts)).where(PageView.visitor == visitor, PageView.ts > now - VISIT_GAP)
            )).scalar_one()
            new_visit = seen is None
        else:
            new_visit = mono - last > VISIT_GAP.total_seconds()
        _visit_cache[visitor] = mono
        if len(_visit_cache) > 20000:
            _visit_cache.clear()
        db.add(PageView(
            ts=now, path=path, visitor=visitor, is_visit_start=new_visit, country=(country or None),
            referrer_host=host if source != "internal" else None, source=source,
            device=device_class(user_agent),
        ))
        await db.commit()


async def purge_old(retention_days: int) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    async with AsyncSessionLocal() as db:
        res = await db.execute(delete(PageView).where(PageView.ts < cutoff))
        await db.commit()
        return res.rowcount or 0


# ---------------------------------------------------------------- reporting

PERIODS = {"today": 1, "7d": 7, "30d": 30, "90d": 90, "12m": 365}


def _start_of(period: str) -> datetime:
    now = datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight - timedelta(days=PERIODS[period] - 1)


async def summary(db: AsyncSession, period: str) -> Dict[str, Any]:
    start = _start_of(period)
    prev_start = start - (datetime.now(timezone.utc) - start)
    window = PageView.ts >= start

    async def totals(since: datetime, until: Optional[datetime] = None) -> Tuple[int, int, int]:
        conds = [PageView.ts >= since] + ([PageView.ts < until] if until else [])
        row = (await db.execute(select(
            func.count(), func.count().filter(PageView.is_visit_start), func.count(func.distinct(PageView.visitor))
        ).where(*conds))).one()
        return row[0], row[1], row[2]

    views, visits, uniques = await totals(start)
    p_views, p_visits, p_uniques = await totals(prev_start, start)

    async def breakdown(col, *extra, limit=12, visits_only=False) -> List[Dict[str, Any]]:
        conds = [window, *extra] + ([PageView.is_visit_start] if visits_only else [])
        rows = (await db.execute(
            select(col, func.count().label("n")).where(*conds).group_by(col).order_by(func.count().desc()).limit(limit)
        )).all()
        return [{"key": k, "count": n} for k, n in rows]

    top_rows = (await db.execute(
        select(PageView.path, func.count().label("views"), func.count(func.distinct(PageView.visitor)).label("uniques"))
        .where(window).group_by(PageView.path).order_by(func.count().desc()).limit(15)
    )).all()
    ids = {}
    for path, *_ in top_rows:
        m = re.match(r"^/news/(\d+)", path)
        if m:
            ids[path] = int(m.group(1))
    titles = {}
    if ids:
        titles = dict((await db.execute(
            select(NewsArticle.id, NewsArticle.title).where(NewsArticle.id.in_(set(ids.values())))
        )).all())
    popular = [{"path": p, "title": titles.get(ids.get(p)), "views": v, "visitors": u} for p, v, u in top_rows]

    countries = [{"code": c or "XX", "name": country_name(c or "XX"), "count": n}
                 for c, n in [(r["key"], r["count"]) for r in await breakdown(PageView.country, visits_only=True)]]
    sources = await breakdown(PageView.source, PageView.source != "internal", visits_only=True, limit=10)
    referrers = await breakdown(PageView.referrer_host, PageView.referrer_host.is_not(None), visits_only=True, limit=10)
    devices = await breakdown(PageView.device, visits_only=True, limit=5)

    def delta(now_v: int, before: int) -> Optional[float]:
        return round((now_v - before) / before * 100, 1) if before else None

    return {
        "period": period, "since": start.isoformat(),
        "page_views": views, "visits": visits, "unique_visitors": uniques,
        "pages_per_visit": round(views / visits, 2) if visits else 0,
        "change": {"page_views": delta(views, p_views), "visits": delta(visits, p_visits),
                   "unique_visitors": delta(uniques, p_uniques)},
        "popular_pages": popular, "countries": countries, "sources": sources, "referrers": referrers,
        "devices": devices,
    }


async def timeseries(db: AsyncSession, granularity: str) -> Dict[str, Any]:
    unit, count = {"day": ("day", 30), "week": ("week", 12), "month": ("month", 12)}[granularity]
    now = datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if unit == "day":
        first = today - timedelta(days=count - 1)
    elif unit == "week":
        first = today - timedelta(days=today.weekday()) - timedelta(weeks=count - 1)
    else:
        month = today.replace(day=1)
        y, m = month.year, month.month - (count - 1)
        while m < 1:
            y, m = y - 1, m + 12
        first = month.replace(year=y, month=m)
    bucket = func.date_trunc(unit, PageView.ts)
    rows = (await db.execute(
        select(bucket, func.count(), func.count().filter(PageView.is_visit_start),
               func.count(func.distinct(PageView.visitor)))
        .where(PageView.ts >= first).group_by(bucket).order_by(bucket)
    )).all()
    found = {r[0].astimezone(timezone.utc).date(): r for r in rows}
    points, cursor = [], first
    while cursor <= now:
        r = found.get(cursor.date())
        points.append({"date": cursor.date().isoformat(), "page_views": r[1] if r else 0,
                       "visits": r[2] if r else 0, "unique_visitors": r[3] if r else 0})
        if unit == "day":
            cursor += timedelta(days=1)
        elif unit == "week":
            cursor += timedelta(weeks=1)
        else:
            cursor = cursor.replace(year=cursor.year + (cursor.month == 12), month=cursor.month % 12 + 1)
    return {"granularity": granularity, "points": points}


async def activity(db: AsyncSession) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    active = (await db.execute(
        select(func.count(func.distinct(PageView.visitor))).where(PageView.ts > now - timedelta(minutes=5))
    )).scalar_one()
    since = now - timedelta(hours=24)
    hour = func.date_trunc("hour", PageView.ts)
    hourly = dict((await db.execute(
        select(hour, func.count()).where(PageView.ts >= since).group_by(hour)
    )).all())
    hours, cursor = [], now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=23)
    while cursor <= now:
        hours.append({"hour": cursor.isoformat(), "page_views": hourly.get(cursor, 0)})
        cursor += timedelta(hours=1)
    recent = (await db.execute(select(PageView).order_by(PageView.ts.desc()).limit(25))).scalars().all()
    return {
        "active_now": active, "hourly": hours,
        "recent": [{"ts": r.ts.isoformat(), "path": r.path, "country": r.country,
                    "country_name": country_name(r.country or "XX"), "device": r.device,
                    "source": r.referrer_host or r.source, "new_visit": r.is_visit_start} for r in recent],
    }
