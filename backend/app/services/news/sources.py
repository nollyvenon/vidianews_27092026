"""Registry of news sources.

Only official RSS/Atom feeds are used. Each source lists the domains its
article links are expected to live on; links elsewhere fail validation.
`trust` is a 0-1 editorial-credibility prior used in the quality score.
Community sources (forums) are never treated as verified reporting.
"""

from typing import Dict, List, Optional, TypedDict


class Source(TypedDict, total=False):
    key: str
    name: str
    country: str          # ISO-3166 alpha-2 of the outlet's home market, "XX" = international
    feed_url: str
    domains: List[str]
    trust: float
    kind: str             # rss | community
    default_category: Optional[str]


def _s(key, name, country, feed_url, domains, trust=0.8, kind="rss", default_category=None) -> Source:
    return Source(key=key, name=name, country=country, feed_url=feed_url, domains=domains,
                  trust=trust, kind=kind, default_category=default_category)


SOURCES: List[Source] = [
    # Nigeria
    # The Nation and The Guardian Nigeria answer automated feed requests with HTTP 403 (bot
    # protection), so they are disabled rather than worked around. Re-enable if they allow access.
    _s("punch", "Punch Nigeria", "NG", "https://punchng.com/feed/", ["punchng.com"], 0.8),
    # _s("thenation", "The Nation", "NG", "https://thenationonlineng.net/feed", ["thenationonlineng.net"], 0.8),
    _s("nairaland", "Nairaland", "NG", "https://www.nairaland.com/feed", ["nairaland.com"], 0.35, kind="community"),
    # _s("guardian_ng", "The Guardian Nigeria", "NG", "https://guardian.ng/feed", ["guardian.ng"], 0.8),
    _s("premiumtimes", "Premium Times", "NG", "https://www.premiumtimesng.com/feed", ["premiumtimesng.com"], 0.85),
    _s("vanguard", "Vanguard", "NG", "https://www.vanguardngr.com/feed/", ["vanguardngr.com"], 0.8),
    _s("channels", "Channels TV", "NG", "https://www.channelstv.com/feed/", ["channelstv.com"], 0.8),
    # International
    _s("bbc", "BBC News", "XX", "https://feeds.bbci.co.uk/news/world/rss.xml", ["bbc.co.uk", "bbc.com"], 0.95),
    _s("bbc_africa", "BBC News Africa", "XX", "https://feeds.bbci.co.uk/news/world/africa/rss.xml", ["bbc.co.uk", "bbc.com"], 0.95),
    # CNN: its public RSS feeds (rss.cnn.com) have not been updated since 2023/2024, so every
    # item fails the freshness check. Re-enable when CNN publishes a current feed.
    # _s("cnn", "CNN", "XX", "http://rss.cnn.com/rss/cnn_latest.rss", ["cnn.com"], 0.85),
    _s("aljazeera", "Al Jazeera", "XX", "https://www.aljazeera.com/xml/rss/all.xml", ["aljazeera.com"], 0.85),
    _s("dw", "Deutsche Welle", "XX", "https://rss.dw.com/rdf/rss-en-all", ["dw.com"], 0.9),
    # United States / United Kingdom
    _s("npr", "NPR", "US", "https://feeds.npr.org/1001/rss.xml", ["npr.org"], 0.9),
    _s("guardian_uk", "The Guardian", "GB", "https://www.theguardian.com/uk/rss", ["theguardian.com"], 0.9),
    _s("sky", "Sky News", "GB", "https://feeds.skynews.com/feeds/rss/uk.xml", ["news.sky.com", "skynews.com"], 0.85),
    # Africa
    _s("capitalfm_ke", "Capital FM Kenya", "KE", "https://www.capitalfm.co.ke/news/feed/", ["capitalfm.co.ke", "capitalfm.africa"], 0.75),
    _s("nation_ke", "Nation Africa (Kenya)", "KE", "https://www.nation.africa/kenya/rss.xml", ["nation.africa"], 0.8),
    _s("myjoyonline", "MyJoyOnline", "GH", "https://www.myjoyonline.com/feed/", ["myjoyonline.com"], 0.75),
    # Other regions
    _s("hindu", "The Hindu", "IN", "https://www.thehindu.com/news/national/feeder/default.rss", ["thehindu.com"], 0.85),
    _s("ndtv", "NDTV", "IN", "https://feeds.feedburner.com/ndtvnews-latest", ["ndtv.com"], 0.8),
    _s("cbc", "CBC News", "CA", "https://www.cbc.ca/webfeed/rss/rss-topstories", ["cbc.ca"], 0.9),
    _s("abc_au", "ABC News Australia", "AU", "https://www.abc.net.au/news/feed/51120/rss.xml", ["abc.net.au"], 0.9),
]

COUNTRY_NAMES: Dict[str, str] = {
    "NG": "Nigeria", "US": "United States", "GB": "United Kingdom", "ZA": "South Africa",
    "KE": "Kenya", "GH": "Ghana", "IN": "India", "CA": "Canada", "AU": "Australia",
    "XX": "International", "DE": "Germany", "FR": "France", "EG": "Egypt",
    "AE": "United Arab Emirates", "CN": "China", "RU": "Russia", "BR": "Brazil",
    "JP": "Japan", "IE": "Ireland",
}

SOURCE_BY_KEY: Dict[str, Source] = {s["key"]: s for s in SOURCES}


def country_name(code: str) -> str:
    return COUNTRY_NAMES.get(code.upper(), code.upper())


def local_country_codes() -> List[str]:
    return sorted({s["country"] for s in SOURCES if s["country"] != "XX"})
