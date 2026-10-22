"""Second ingest stage: read each article's own page for its body text and a
story-specific image, and fall back to Wikimedia Commons when it has none.

Feeds often carry only a teaser and, for some publishers, one site logo for every
story. This stage replaces those with the page's own `og:image` and article text.
Image provenance is stored so the UI can credit it and label non-publisher images.
"""

import asyncio
import html
import logging
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urljoin

import httpx
from sqlalchemy import func, select, update

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.news import NewsArticle as A
from app.services.news.cleaning import clean_body

_log = logging.getLogger(__name__)

MAX_PAGE_BYTES = 2_000_000
MIN_BODY_CHARS = 300
MAX_BODY_CHARS = 20_000
GENERIC_IMAGE_REPEATS = 5  # a "story" image shared by this many articles is a logo/placeholder

_GENERIC_IMAGE = re.compile(
    r"(logo|placeholder|/og-image|favicon|avatar|gravatar|no[-_]?image|spacer|sprite|fallback|/default|default[-_.]|"
    r"[-_/.]icon|/brand|blank\.|1x1|pixel\.)", re.I)

_SKIP_TAGS = {"script", "style", "nav", "footer", "aside", "form", "header", "noscript", "figure",
              "button", "svg", "iframe", "select", "template"}
_BOILERPLATE = re.compile(
    r"^(advertisement|ads?\b|read also|read more|related|follow us|subscribe|sign up|click (here|to)|"
    r"copyright|all rights reserved|share this|download the|join our|get the latest|also read|watch:|"
    r"click the link|newsletter|support (our|the) journalism)", re.I)


class _PageParser(HTMLParser):
    """Collects <meta> tags and paragraph text (preferring text inside <article>)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: Dict[str, str] = {}
        self.in_article: List[str] = []
        self.anywhere: List[str] = []
        self._skip = 0
        self._article = 0
        self._p: Optional[List[str]] = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = (a.get("property") or a.get("name") or "").lower()
            if key and a.get("content") and key not in self.meta:
                self.meta[key] = a["content"]
        elif tag in _SKIP_TAGS:
            self._skip += 1
        elif tag == "article":
            self._article += 1
        elif tag == "p" and not self._skip:
            self._p = []

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
        elif tag == "article":
            self._article = max(0, self._article - 1)
        elif tag == "p" and self._p is not None:
            text = re.sub(r"\s+", " ", "".join(self._p)).strip()
            self._p = None
            if len(text) >= 40 and not _BOILERPLATE.match(text):
                (self.in_article if self._article else self.anywhere).append(text)

    def handle_data(self, data):
        if self._p is not None and not self._skip:
            self._p.append(data)


def parse_page(markup: str) -> Dict[str, Any]:
    parser = _PageParser()
    try:
        parser.feed(markup)
        parser.close()
    except Exception:  # noqa: BLE001 - broken markup: use whatever was collected
        pass
    paragraphs = parser.in_article if len(parser.in_article) >= 2 else parser.in_article + parser.anywhere
    deduped: List[str] = []
    for p in paragraphs:
        if p not in deduped:
            deduped.append(p)
    body, total = [], 0
    for p in deduped:
        if total + len(p) > MAX_BODY_CHARS:
            break
        body.append(p)
        total += len(p)
    meta = parser.meta
    return {
        "image": meta.get("og:image") or meta.get("og:image:url") or meta.get("twitter:image")
        or meta.get("twitter:image:src"),
        "paragraphs": body if total >= MIN_BODY_CHARS and len(body) >= 2 else [],
    }


def clean_image_url(value: Optional[str], base: Optional[str] = None) -> Optional[str]:
    if not value:
        return None
    value = html.unescape(value).strip()
    if base:
        value = urljoin(base, value)
    if not re.match(r"^https?://[^\s]+\.[^\s]+$", value) or len(value) > 2048:
        return None
    return value


def is_generic_image(url: Optional[str], repeated: Set[str]) -> bool:
    return not url or url in repeated or bool(_GENERIC_IMAGE.search(url))


async def _fetch_page(client: httpx.AsyncClient, url: str) -> Optional[str]:
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        if "html" not in resp.headers.get("content-type", "html"):
            return None
        return resp.content[:MAX_PAGE_BYTES].decode(resp.encoding or "utf-8", errors="replace")
    except (httpx.HTTPError, LookupError) as exc:
        _log.debug("page fetch failed for %s: %r", url, exc)
        return None


_CREDIT_NAMES = re.compile(r"getty|afp|reuters|associated press|ap|shutterstock|alamy|npr|bbc", re.I)


def _query_for(title: str, people: List[str], organizations: List[str]) -> Optional[str]:
    """A multi-word person/organisation named in the headline itself (not a photo credit)."""
    headline = title.lower()
    for name in list(people or []) + list(organizations or []):
        if (name and len(name.split()) >= 2 and name.lower() in headline
                and not _CREDIT_NAMES.search(name)):
            return name
    return None


async def _wikimedia_image(client: httpx.AsyncClient, query: str) -> Optional[Dict[str, str]]:
    """A freely licensed photo of the person/organisation named in the story, if one clearly matches."""
    try:
        resp = await client.get("https://commons.wikimedia.org/w/api.php", params={
            "action": "query", "format": "json", "generator": "search", "gsrsearch": query,
            "gsrnamespace": 6, "gsrlimit": 10, "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 800,
        })
        resp.raise_for_status()
        pages = (resp.json().get("query") or {}).get("pages") or {}
    except (httpx.HTTPError, ValueError):
        return None
    tokens = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2]
    for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        info = (page.get("imageinfo") or [None])[0]
        title = page.get("title", "").lower()
        if not info or info.get("mime") not in ("image/jpeg", "image/png") or info.get("width", 0) < 600:
            continue
        title_words = set(re.findall(r"[a-z0-9]+", title))
        if not tokens or not all(t in title_words for t in tokens):
            continue
        ext = info.get("extmetadata") or {}
        artist = re.sub(r"<[^>]+>", "", (ext.get("Artist") or {}).get("value", "")).strip()
        licence = (ext.get("LicenseShortName") or {}).get("value", "")
        credit = "Wikimedia Commons" + (f" / {artist[:120]}" if artist else "") + (f" ({licence})" if licence else "")
        return {"url": info.get("thumburl") or info["url"], "credit": credit, "credit_url": info.get("descriptionurl")}
    return None


async def enrich_row(client: httpx.AsyncClient, row: Dict[str, Any], repeated: Set[str]) -> Dict[str, Any]:
    """Return the column updates for one article (never raises)."""
    updates: Dict[str, Any] = {"enriched_at": datetime.now(timezone.utc)}
    image = clean_image_url(row["image_url"])
    source = "publisher"
    credit = f"Image: {row['source_name']}"
    credit_url = row["url"]
    if is_generic_image(image, repeated):
        image = None
    try:
        markup = await _fetch_page(client, row["url"])
        if markup:
            page = await asyncio.to_thread(parse_page, markup)
            if page["paragraphs"]:
                full = clean_body("\n\n".join(page["paragraphs"]), row["source_key"])
                if len(full) > len(row["content"] or ""):
                    updates["full_content"] = full
            page_image = clean_image_url(page["image"], row["url"])
            if image is None and not is_generic_image(page_image, repeated):
                image, source = page_image, "page"
        if image is None:
            query = _query_for(row["title"], row["people"], row["organizations"])
            found = await _wikimedia_image(client, query) if query else None
            if found:
                image, source, credit, credit_url = found["url"], "wikimedia", found["credit"], found["credit_url"]
    except Exception as exc:  # noqa: BLE001 - one article must not break the batch
        _log.warning("enrich failed for %s: %r", row["url"], exc)
    updates.update(
        image_url=image, image_source=source if image else None,
        image_credit=credit[:500] if image else None, image_credit_url=credit_url if image else None,
    )
    return updates


_COLUMNS = (A.id, A.url, A.title, A.source_key, A.source_name, A.image_url, A.content, A.people, A.organizations)


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=12.0, follow_redirects=True,
        headers={"User-Agent": settings.NEWS_USER_AGENT, "Accept": "text/html,application/xhtml+xml,*/*"},
    )


async def repeated_images(session) -> Set[str]:
    rows = await session.execute(
        select(A.image_url).where(A.image_url.is_not(None)).group_by(A.image_url)
        .having(func.count() >= GENERIC_IMAGE_REPEATS)
    )
    return {u for (u,) in rows.all()}


async def enrich_pending(limit: int = 250, concurrency: int = 8) -> Dict[str, int]:
    """Enrich the newest articles that have not been enriched yet."""
    async with AsyncSessionLocal() as session:
        repeated = await repeated_images(session)
        rows = [dict(zip((c.key for c in _COLUMNS), r)) for r in (await session.execute(
            select(*_COLUMNS).where(A.enriched_at.is_(None)).order_by(A.published_at.desc()).limit(limit)
        )).all()]
    if not rows:
        return {"enriched": 0, "with_body": 0, "with_image": 0}

    sem = asyncio.Semaphore(concurrency)
    async with _client() as client:
        async def one(row):
            async with sem:
                return row["id"], await enrich_row(client, row, repeated)
        results = await asyncio.gather(*(one(r) for r in rows))

    async with AsyncSessionLocal() as session:
        for article_id, updates in results:
            await session.execute(update(A).where(A.id == article_id).values(**updates))
        await session.commit()
    return {
        "enriched": len(results),
        "with_body": sum(1 for _, u in results if u.get("full_content")),
        "with_image": sum(1 for _, u in results if u.get("image_url")),
    }


async def enrich_one(article_id: int) -> None:
    """Enrich a single article on demand (a reader opened one that is still pending)."""
    async with AsyncSessionLocal() as session:
        repeated = await repeated_images(session)
        found = (await session.execute(select(*_COLUMNS).where(A.id == article_id, A.enriched_at.is_(None)))).first()
        if not found:
            return
        row = dict(zip((c.key for c in _COLUMNS), found))
    async with _client() as client:
        updates = await enrich_row(client, row, repeated)
    async with AsyncSessionLocal() as session:
        await session.execute(update(A).where(A.id == article_id).values(**updates))
        await session.commit()
