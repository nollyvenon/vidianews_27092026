"""Country detection for news personalisation (IP geolocation)."""

import logging
import re
import time
from ipaddress import ip_address
from typing import Dict, Optional, Tuple

import httpx
from fastapi import Request

from app.services.news.sources import country_name

_log = logging.getLogger(__name__)

_CACHE_TTL = 24 * 3600
_cache: Dict[str, Tuple[float, Optional[str]]] = {}

# Ordered fallbacks: (url template, JSON key holding the ISO country code)
_PROVIDERS = [
    ("http://ip-api.com/json/{ip}?fields=status,countryCode", "countryCode"),
    ("https://ipwho.is/{ip}", "country_code"),
    ("https://ipapi.co/{ip}/json/", "country_code"),
]


def client_ip(request: Request) -> Optional[str]:
    """Best-effort client IP, honouring reverse-proxy headers."""
    fwd = request.headers.get("x-forwarded-for")
    candidates = [fwd.split(",")[0].strip()] if fwd else []
    candidates.append(request.headers.get("x-real-ip", ""))
    candidates.append(request.client.host if request.client else "")
    for c in candidates:
        if c:
            return c
    return None


def _is_public(ip: Optional[str]) -> bool:
    try:
        return bool(ip) and ip_address(ip).is_global
    except ValueError:
        return False


async def _lookup(ip: str) -> Optional[str]:
    """Look up an IP ('' = the server's own public IP). Result is cached."""
    now = time.time()
    hit = _cache.get(ip)
    if hit and now - hit[0] < _CACHE_TTL:
        return hit[1]
    code = None
    async with httpx.AsyncClient(timeout=4.0) as client:
        for template, key in _PROVIDERS:
            try:
                resp = await client.get(template.format(ip=ip))
                data = resp.json()
                value = data.get(key)
                if resp.status_code == 200 and isinstance(value, str) and len(value) == 2:
                    code = value.upper()
                    break
            except Exception as exc:  # noqa: BLE001 - try the next provider
                _log.debug("geo provider %s failed: %r", template, exc)
    # Cache failures only briefly so a provider outage does not stick for a day.
    _cache[ip] = (now if code else now - _CACHE_TTL + 300, code)
    return code


def _accept_language_country(request: Request) -> Optional[str]:
    header = request.headers.get("accept-language", "")
    m = re.search(r"[a-z]{2,3}-([A-Z]{2})", header)
    return m.group(1) if m else None


async def detect_country(request: Request, override: Optional[str] = None) -> Dict[str, str]:
    """Resolve the reader's country.

    Order: explicit override -> client IP -> server's public IP (when the client
    IP is private, e.g. local development) -> Accept-Language region -> default.
    """
    if override and re.fullmatch(r"[A-Za-z]{2}", override):
        code = override.upper()
        return {"country": code, "country_name": country_name(code), "source": "manual"}

    ip = client_ip(request)
    if _is_public(ip):
        code = await _lookup(ip)
        if code:
            return {"country": code, "country_name": country_name(code), "source": "ip", "ip": ip}
    else:
        code = await _lookup("")
        if code:
            return {"country": code, "country_name": country_name(code), "source": "server_ip"}

    code = _accept_language_country(request)
    if code:
        return {"country": code, "country_name": country_name(code), "source": "accept_language"}
    return {"country": "XX", "country_name": country_name("XX"), "source": "default"}
