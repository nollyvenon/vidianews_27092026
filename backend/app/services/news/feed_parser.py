"""RSS 2.0 / Atom / RDF feed parsing (safe XML via defusedxml)"""

import html
import html.entities as html_entities
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import List, Optional

from defusedxml import ElementTree as ET


@dataclass
class RawItem:
    title: str
    url: str
    content: str = ""
    author: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[datetime] = None
    feed_categories: List[str] = field(default_factory=list)


class _TextExtractor(HTMLParser):
    _BLOCK = {"p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in self._BLOCK:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def strip_html(raw: str) -> str:
    if not raw:
        return ""
    parser = _TextExtractor()
    try:
        parser.feed(raw)
        parser.close()
        text = "".join(parser.parts)
    except Exception:  # malformed markup: fall back to a regex strip
        text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _local(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1]


def _parse_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    value = value.strip()
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)


_XML_ENTITIES = {"amp", "lt", "gt", "quot", "apos"}
_BAD_ENTITY = re.compile(r"&(?!(?:[A-Za-z][A-Za-z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);)")
_NAMED_ENTITY = re.compile(r"&([A-Za-z][A-Za-z0-9]*);")
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _repair_xml(xml_bytes: bytes) -> bytes:
    """Fix common publisher feed defects: HTML entities, bare ampersands, control chars."""
    text = xml_bytes.decode("utf-8", errors="replace")
    text = _CTRL.sub("", text)

    def named(m):
        name = m.group(1)
        if name in _XML_ENTITIES:
            return m.group(0)
        code = html_entities.name2codepoint.get(name)
        return f"&#{code};" if code else "&amp;" + name + ";"

    text = _NAMED_ENTITY.sub(named, text)
    text = _BAD_ENTITY.sub("&amp;", text)
    return text.encode("utf-8")


# WordPress feeds append "The post <title> appeared first on <site>." to every excerpt.
_BOILERPLATE = re.compile(r"\s*The post .{0,400}? appeared first on .{0,120}?\.?\s*$", re.S)


_READ_MORE = re.compile(r"\s*(?:Read more|Continue reading|Read the full story)\s*:?\s*(?:https?://\S+)?\s*$", re.I)
_BARE_URL = re.compile(r"https?://\S+")


def _clean_body(text: str) -> str:
    text = _BOILERPLATE.sub("", text)
    text = _READ_MORE.sub("", text)
    return _BARE_URL.sub("", text).replace("[\u2026]", "").replace("[&hellip;]", "").strip()


def parse_feed(xml_bytes: bytes) -> List[RawItem]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        root = ET.fromstring(_repair_xml(xml_bytes))
    items: List[RawItem] = []
    for node in root.iter():
        if _local(node.tag) not in ("item", "entry"):
            continue
        data = {"categories": []}
        image = None
        for child in node:
            name = _local(child.tag)
            text = (child.text or "").strip()
            if name == "title":
                data["title"] = text
            elif name == "link":
                href = child.attrib.get("href")
                rel = child.attrib.get("rel", "alternate")
                if href and rel == "alternate":
                    data.setdefault("link", href)
                elif text:
                    data["link"] = text
            elif name in ("description", "summary") and "description" not in data:
                data["description"] = text
            elif name == "encoded" or (name == "content" and not child.attrib.get("url")):
                data["content"] = text
            elif name in ("pubDate", "published", "updated", "date") and "date" not in data:
                data["date"] = text
            elif name in ("creator", "author"):
                author = text or "".join(c.text or "" for c in child).strip()
                if author:
                    data["author"] = author
            elif name == "category":
                label = child.attrib.get("term") or text
                if label:
                    data["categories"].append(label)
            elif name in ("thumbnail", "content") and child.attrib.get("url"):
                image = image or child.attrib["url"]
            elif name == "enclosure" and child.attrib.get("type", "").startswith("image"):
                image = image or child.attrib.get("url")

        title = strip_html(data.get("title", ""))
        link = data.get("link", "").strip()
        if not title or not link:
            continue
        body_html = data.get("content") or data.get("description") or ""
        if image:
            for _ in range(3):  # some feeds double-escape attribute values
                image = html.unescape(image)
            image = image.strip()
        if not image:
            m = _IMG_RE.search(body_html) or _IMG_RE.search(data.get("description", ""))
            image = m.group(1) if m else None
        items.append(RawItem(
            title=title,
            url=link,
            content=_clean_body(strip_html(body_html)),
            author=strip_html(data["author"]) if data.get("author") else None,
            image_url=image,
            published_at=_parse_date(data.get("date")),
            feed_categories=[strip_html(c) for c in data["categories"]][:8],
        ))
    return items
