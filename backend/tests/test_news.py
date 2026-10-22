"""Unit tests for the news pipeline (no network, no database)."""

from datetime import datetime, timedelta, timezone

from app.services.news import nlp
from app.services.news.feed_parser import parse_feed, strip_html
from app.services.news.validation import (
    STATUS_FLAGGED, STATUS_PASSED, STATUS_REJECTED, STATUS_UNVERIFIED,
    is_near_duplicate, normalize_url, title_tokens, validate_article,
)

NOW = datetime(2026, 10, 22, 12, 0, tzinfo=timezone.utc)

RSS = b"""<?xml version="1.0"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
<channel><title>t</title>
<item><title>Senate passes new budget bill</title><link>https://punchng.com/a/?utm_source=x</link>
<pubDate>Wed, 21 Oct 2026 10:00:00 +0000</pubDate><dc:creator>Jane Doe</dc:creator>
<category>Politics</category><media:thumbnail url="https://punchng.com/i.jpg"/>
<content:encoded><![CDATA[<p>The Senate on Wednesday passed the budget.</p><script>x()</script>]]></content:encoded></item>
<item><title></title><link>https://punchng.com/b</link></item>
</channel></rss>"""


def test_parse_feed_extracts_fields_and_skips_bad_items():
    items = parse_feed(RSS)
    assert len(items) == 1
    item = items[0]
    assert item.author == "Jane Doe"
    assert item.image_url == "https://punchng.com/i.jpg"
    assert item.content == "The Senate on Wednesday passed the budget."
    assert item.published_at == datetime(2026, 10, 21, 10, 0, tzinfo=timezone.utc)
    assert item.feed_categories == ["Politics"]


def test_parse_feed_rejects_entity_bomb():
    bomb = b'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;">]><rss><channel><item><title>&b;</title></item></channel></rss>'
    try:
        parse_feed(bomb)
    except Exception:
        return
    raise AssertionError("DTD/entity expansion should be refused")


def test_strip_html():
    assert strip_html("<p>Hello&nbsp;<b>world</b></p><style>x{}</style>") == "Hello world"


def _validate(**kw):
    args = dict(title="Senate passes new budget bill today", url="https://www.punchng.com/a",
                content="The Senate passed the budget on Wednesday after a long debate.",
                published_at=NOW - timedelta(hours=2), source_domains=["punchng.com"],
                source_trust=0.8, source_kind="rss", now=NOW)
    args.update(kw)
    return validate_article(**args)


def test_clean_article_passes():
    r = _validate()
    assert r.status == STATUS_PASSED and r.score > 0.8 and not r.flags


def test_rejections():
    assert _validate(url="https://evil.example.com/a").reject_reason == "url_domain_mismatch"
    assert _validate(url="https://punchng.com.evil.com/a").reject_reason == "url_domain_mismatch"
    assert _validate(url="http://127.0.0.1/a").reject_reason == "invalid_url"
    assert _validate(url="javascript:alert(1)").reject_reason == "invalid_url"
    assert _validate(title="Short").reject_reason == "title_too_short"
    assert _validate(published_at=NOW + timedelta(days=2)).reject_reason == "future_date"
    assert _validate(published_at=NOW - timedelta(days=60)).reject_reason == "too_old"


def test_flags_for_review_not_truth_claims():
    r = _validate(title="SHOCKING leaked memo exposed, you won't believe it")
    assert r.status == STATUS_FLAGGED and r.needs_review
    r = _validate(content="Sources say the minister allegedly resigned, unconfirmed reports claim.")
    assert "unverified_claim_language" in r.flags


def test_community_sources_are_never_passed():
    r = _validate(source_kind="community", source_trust=0.35)
    assert r.status == STATUS_UNVERIFIED and "community_source" in r.flags


def test_missing_date_is_flagged_but_allowed():
    r = _validate(published_at=None)
    assert r.status != STATUS_REJECTED and "missing_date" in r.flags


def test_url_normalisation_and_duplicates():
    assert normalize_url("https://Punchng.com/a/?utm_source=x&id=1") == "https://punchng.com/a?id=1"
    a = title_tokens("Senate passes new budget bill after long debate")
    b = title_tokens("Senate passes new budget bill after a long debate")
    c = title_tokens("Super Eagles beat Ghana in friendly")
    assert is_near_duplicate(a, b)
    assert not is_near_duplicate(a, c)


def test_nlp_category_summary_and_countries():
    text = ("Nigeria's Senate on Wednesday passed the 2027 budget after a heated debate in Abuja. "
            "Senator Godswill Akpabio said the bill would support infrastructure and defence. "
            "Lawmakers from the opposition PDP walked out in protest. "
            "The president is expected to sign the bill next week.")
    res = nlp.analyze("Senate passes 2027 budget in Abuja", text, source_name="Punch", published_at=NOW)
    assert res.category == "politics"
    assert "NG" in res.mentioned_countries
    # extractive: the summary only contains words from the article
    assert res.summary and set(res.summary.split()) <= set(text.split())
    assert res.keywords
    assert "Punch" in res.description


def test_nlp_never_fails_on_empty_text():
    res = nlp.analyze("A headline with no body at all", "")
    assert res.category and res.summary == ""


def test_parse_feed_repairs_html_entities_and_bare_ampersands():
    xml = (b'<?xml version="1.0"?><rss><channel><item><title>Tom &amp; Jerry&nbsp;win big award &copy; today</title>'
           b'<link>https://punchng.com/x</link><description>AT&T deal &hellip; done</description></item></channel></rss>')
    items = parse_feed(xml)
    assert len(items) == 1 and "Tom & Jerry" in items[0].title and "AT&T" in items[0].content


def test_wordpress_boilerplate_and_escaped_image_url():
    xml = (b'<?xml version="1.0"?><rss xmlns:media="http://search.yahoo.com/mrss/"><channel><item><title>A decent headline for testing</title>'
           b'<link>https://punchng.com/x</link><media:thumbnail url="https://punchng.com/i.jpg?a=1&amp;amp;b=2"/>'
           b'<description>Real text here. The post A decent headline for testing appeared first on Punch.</description></item></channel></rss>')
    item = parse_feed(xml)[0]
    assert item.content == "Real text here."
    assert item.image_url == "https://punchng.com/i.jpg?a=1&b=2"


def test_read_more_links_are_removed_from_content():
    xml = (b'<?xml version="1.0"?><rss><channel><item><title>A decent headline for testing</title>'
           b'<link>https://punchng.com/x</link>'
           b'<description>Real text here. Read More: https://punchng.com/x/</description></item></channel></rss>')
    assert parse_feed(xml)[0].content == "Real text here."
