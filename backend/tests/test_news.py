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
    assert "Punch" not in res.description and "VidiaNews" in res.description


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


# --- article pages, images, bodies -------------------------------------------------

from types import SimpleNamespace

from app.services.news.enrich import _query_for, clean_image_url, is_generic_image, parse_page
from app.services.news.feed_parser import fix_mojibake
from app.services.news.queries import article_body

PAGE = """<html><head>
<meta property="og:image" content="/img/story.jpg?a=1&amp;b=2"><title>x</title></head><body>
<nav><p>Home news sport world and other navigation text that is long enough to count</p></nav>
<article><h1>Headline</h1>
<p>The Senate on Wednesday passed the national budget after a long and tense debate in the chamber, with several amendments tabled and voted on late into the evening.</p>
<p>Advertisement</p>
<p>Lawmakers said the bill would be sent to the president for assent within the next two weeks, according to the leadership of both chambers of parliament.</p>
<aside><p>Related story that should be ignored because it lives in a sidebar element.</p></aside>
<p>Opposition members objected to several lines of the capital expenditure plan during the session and promised to challenge them in court if necessary.</p>
</article><footer><p>Copyright 2026 all rights reserved by the publisher of this website.</p></footer>
</body></html>"""


def test_parse_page_extracts_article_paragraphs_and_image():
    page = parse_page(PAGE)
    assert page["image"] == "/img/story.jpg?a=1&b=2"
    assert len(page["paragraphs"]) == 3
    assert all("navigation" not in p and "sidebar" not in p and "Copyright" not in p for p in page["paragraphs"])


def test_parse_page_too_little_text_returns_no_body():
    assert parse_page("<article><p>Short teaser only, nothing more than this one line of text here.</p></article>")["paragraphs"] == []


def test_clean_image_url_resolves_and_rejects_junk():
    assert clean_image_url("/a.jpg", "https://x.com/news/1") == "https://x.com/a.jpg"
    assert clean_image_url("undefined") is None
    assert clean_image_url("data:image/png;base64,AAAA") is None
    assert clean_image_url(None) is None


def test_generic_images_are_detected():
    assert is_generic_image("https://cdn.punchng.com/uploads/punch-logo-500x179-1.png", set())
    assert is_generic_image("https://x.com/a.jpg", {"https://x.com/a.jpg"})  # reused across many stories
    assert is_generic_image(None, set())
    assert not is_generic_image("https://x.com/uploads/2026/senate-budget.jpg", set())


def test_wikimedia_query_uses_headline_names_not_photo_credits():
    title = "Martha Karua urges Opposition to remain open"
    assert _query_for(title, ["Martha Karua"], []) == "Martha Karua"
    assert _query_for("Dream study", ["Justin Sullivan"], ["Getty Images"]) is None  # not in the headline
    assert _query_for("Photos by Getty Images today", [], ["Getty Images"]) is None  # credit agency
    assert _query_for("Tinubu wins", ["Tinubu"], []) is None  # single word is too ambiguous


def test_fix_mojibake_only_touches_broken_text():
    assert fix_mojibake("Abuse \u00e2\u20ac\u201d Expert") == "Abuse \u2014 Expert"
    assert fix_mojibake("Caf\u00e9 \u2014 fine") == "Caf\u00e9 \u2014 fine"


def test_article_body_prefers_longer_full_content_and_splits_teasers():
    full = SimpleNamespace(full_content="First paragraph.\n\nSecond paragraph.", content="Short")
    assert article_body(full) == ["First paragraph.", "Second paragraph."]
    teaser = SimpleNamespace(full_content=None, content=" ".join(["A sentence that is of a decent length."] * 40))
    parts = article_body(teaser)
    assert len(parts) > 1 and all(p.endswith(".") for p in parts)
    assert article_body(SimpleNamespace(full_content=None, content="")) == []


# ------------------------------------------------------------ boilerplate cleaning

def test_cleaning_removes_publisher_promotion_but_keeps_the_story():
    from app.services.news.cleaning import clean_body
    body = "\n\n".join([
        "Gilbert Ekugbe is a journalist at Punch Newspapers with over a decade of experience. He covers markets.",
        "ATTENTION NIGERIANS: You can now comfortably earn US Dollars when you acquire premium domains for as low as $3000.",
        "The central bank raised rates by 50 basis points on Thursday, citing inflation.",
        "Stay informed and ahead of the curve! Follow The Punch Newspaper on WhatsApp for real-time updates. Don't miss a headline – join now!",
        "Stay in the know—fast. Get instant alerts with the Punch News App. Download now and never miss a beat.",
        "Officials told BBC News that the airport remains closed.",
    ])
    out = clean_body(body, "punch")
    assert out == ("The central bank raised rates by 50 basis points on Thursday, citing inflation.\n\n"
                   "Officials told BBC News that the airport remains closed.")


def test_cleaning_handles_subscription_copyright_and_credit_lines():
    from app.services.news.cleaning import clean_body, clean_title
    assert clean_body("All content is Copyrighted © 2025 The Premium Times, Nigeria", "premiumtimes") == ""
    assert clean_body("Comments have to be in English, and in full sentences.", "hindu") == ""
    assert clean_body("Published - October 22, 2026 06:46 pm IST", "hindu") == ""
    assert clean_body("Polling officials. | Photo Credit: ANI", "hindu") == "Polling officials."
    assert clean_body("A market (PHOTO CREDIT: PREMIUM TIMES)", "premiumtimes") == "A market"
    assert clean_body("taken down, external following complaints", "bbc") == "taken down following complaints"
    assert clean_body("forces from the north, external actors", "aljazeera") == "forces from the north, external actors"
    assert clean_title("Fuel prices rise | Margaret Sullivan", "guardian_uk") == "Fuel prices rise"
    assert clean_title("Fuel prices rise - The Punch", "punch") == "Fuel prices rise"
    assert clean_title("Gunmen attack NDTV World Summit venue", "ndtv") == "Gunmen attack NDTV World Summit venue"


def test_cleaning_does_not_drop_ordinary_news_mentioning_apps_or_following():
    from app.services.news.cleaning import clean_body
    for sentence in (
        "Apple said the App Store fee change takes effect next month.",
        "The ceasefire followed weeks of talks mediated by Qatar.",
        "He urged supporters to join the march on Saturday.",
        "The minister is a journalist by training and will address the press.",
    ):
        assert clean_body(sentence, "punch") == sentence


def test_cleaning_drops_correspondent_bios_and_publisher_signoffs():
    from app.services.news.cleaning import clean_body
    bio = "With three years of experience, Stephen, The PUNCH correspondent, has been covering Nigeria’s presidency, politics and security."
    assert clean_body(bio, "punch") == ""
    assert clean_body("Voting continued without delay. Vanguard News", "vanguard") == "Voting continued without delay."
    assert clean_body("He told Vanguard that voting continued.", "vanguard") == "He told Vanguard that voting continued."


from app.services.news.quality import assess

_FULL_STORY = " ".join(
    ["The minister said on Tuesday that the new road between the two cities will open to traffic next month."] * 4)


def test_quality_gate_holds_short_empty_and_promo_only_text():
    assert assess("", None, 300) == "empty"
    assert assess("Follow The Punch Newspaper on WhatsApp\n\nDownload the Punch News App", None, 300, "punch") == "promo_only"
    assert assess("A man has died after a gravestone gave way at a cemetery.", None, 300) == "too_short"
    assert assess("The centre's draft rules propose removing fees for several services and giving...", None, 300) == "incomplete"


def test_quality_gate_passes_complete_stories_and_prefers_full_text():
    assert assess(_FULL_STORY, None, 300) is None
    assert assess("Short teaser only.", _FULL_STORY, 300) is None  # page text longer than the feed teaser wins
    assert assess(_FULL_STORY, None, 1000) == "too_short"  # the minimum is configurable


def test_quality_gate_judges_text_after_promo_is_removed():
    padded = "Follow The Punch Newspaper on WhatsApp for more updates and the latest breaking news " * 6
    assert assess(padded + "\n\nA man has died.", None, 300, "punch") in ("promo_only", "too_short")
    assert assess(_FULL_STORY + "\n\nDownload the Punch News App", None, 300, "punch") is None
