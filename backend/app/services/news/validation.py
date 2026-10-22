"""Article validation and review flagging.

What this does:
  * structural checks (title, URL scheme/host, publication date, content length)
  * source checks (link must live on the source's own domains; community sources
    are never marked as passed)
  * language heuristics that mark an article for human review (sensational
    wording, hedged / unattributed claims)

What this does NOT do: verify that a claim is true. Flagged and unverified
articles are surfaced to the reader with a label and queued for an editor.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from ipaddress import ip_address
from typing import List, Optional
from urllib.parse import urlparse

STATUS_PASSED = "passed"
STATUS_UNVERIFIED = "unverified"
STATUS_FLAGGED = "flagged"
STATUS_REJECTED = "rejected"

_SENSATIONAL = re.compile(
    r"you won'?t believe|shocking|jaw[- ]dropping|what happened next|this is why|"
    r"will (blow|shock) your|secret they|doctors hate|goes viral|\bmust see\b|"
    r"\bexposed\b|\bbombshell\b|\bleaked\b",
    re.I,
)
_HEDGED = re.compile(
    r"\ballegedly\b|\bpurportedly\b|\bunconfirmed\b|\brumou?rs?\b|\bsources? (say|said|claim)\b|"
    r"\breportedly\b|\bclaims? that\b|\bunverified\b|\bhoax\b|\bconspiracy\b|\bfake news\b|"
    r"\bin a viral (video|post)\b|\bsocial media users?\b",
    re.I,
)


@dataclass
class ValidationResult:
    status: str = STATUS_PASSED
    score: float = 1.0
    flags: List[str] = field(default_factory=list)
    reject_reason: Optional[str] = None
    needs_review: bool = False


def normalize_url(url: str) -> str:
    parts = urlparse(url.strip())
    query = "&".join(
        p for p in parts.query.split("&")
        if p and not p.lower().startswith(("utm_", "fbclid", "gclid", "ref=", "cmp="))
    )
    path = parts.path.rstrip("/") or "/"
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}{path}" + (f"?{query}" if query else "")


def _host_ok(host: str, domains: List[str]) -> bool:
    host = host.lower().split(":")[0]
    return any(host == d or host.endswith("." + d) for d in domains)


def _is_ip(host: str) -> bool:
    host = host.split("@")[-1]
    if host.startswith("["):
        return True  # IPv6 literal
    try:
        ip_address(host.split(":")[0])
        return True
    except ValueError:
        return False


def validate_article(title: str, url: str, content: str, published_at: Optional[datetime],
                     source_domains: List[str], source_trust: float, source_kind: str,
                     max_age_days: int = 14, now: Optional[datetime] = None) -> ValidationResult:
    now = now or datetime.now(timezone.utc)
    res = ValidationResult(score=0.5 + 0.5 * source_trust)

    def reject(reason: str) -> ValidationResult:
        res.status, res.reject_reason, res.score = STATUS_REJECTED, reason, 0.0
        return res

    # Title
    t = title.strip()
    if len(t) < 15:
        return reject("title_too_short")
    if len(t) > 300:
        return reject("title_too_long")
    letters = [c for c in t if c.isalpha()]
    if len(letters) > 12 and sum(c.isupper() for c in letters) / len(letters) > 0.7:
        res.flags.append("all_caps_title")
        res.score -= 0.15

    # URL
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return reject("invalid_url")
    if len(url) > 2000 or _is_ip(parsed.netloc):
        return reject("invalid_url")
    if not _host_ok(parsed.netloc, source_domains):
        return reject("url_domain_mismatch")

    # Date
    if published_at is None:
        res.flags.append("missing_date")
        res.score -= 0.2
    else:
        if published_at > now + timedelta(hours=1):
            return reject("future_date")
        if published_at < now - timedelta(days=max_age_days):
            return reject("too_old")

    # Content quality
    body_len = len(content or "")
    if body_len < 40:
        res.flags.append("thin_content")
        res.score -= 0.15

    # Language heuristics (review triggers, not verdicts)
    text = f"{t} {content or ''}"
    if _SENSATIONAL.search(text):
        res.flags.append("sensational_language")
        res.score -= 0.2
    if _HEDGED.search(text):
        res.flags.append("unverified_claim_language")
        res.score -= 0.15
    if t.endswith("?") and len(t.split()) <= 12:
        res.flags.append("question_headline")
        res.score -= 0.05

    res.score = round(max(0.0, min(1.0, res.score)), 2)

    if source_kind == "community":
        res.flags.append("community_source")
        res.status = STATUS_UNVERIFIED
        res.needs_review = "sensational_language" in res.flags or "unverified_claim_language" in res.flags
    elif "sensational_language" in res.flags or (
        "unverified_claim_language" in res.flags and res.score < 0.75
    ):
        res.status = STATUS_FLAGGED
        res.needs_review = True
    elif res.score < 0.5:
        res.status = STATUS_UNVERIFIED
    return res


_TOKEN = re.compile(r"[a-z0-9]+")


def title_tokens(title: str) -> frozenset:
    return frozenset(t for t in _TOKEN.findall(title.lower()) if len(t) > 2)


def is_near_duplicate(tokens: frozenset, other: frozenset, threshold: float = 0.8) -> bool:
    if not tokens or not other:
        return False
    inter = len(tokens & other)
    return inter / len(tokens | other) >= threshold
