"""Unit tests for the admin panel rules (no network, no database)."""

from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.services.site import adminauth, adverts, analytics
from app.services.site.sitesettings import DEFINITIONS, _coerce, public_settings

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32


# ---------------------------------------------------------------- passwords

def test_password_policy_rejects_weak_passwords():
    for bad in ("short1!", "alllettersandnonumbers", "123456789012", "a" * 80 + "1"):
        with pytest.raises(HTTPException) as exc:
            adminauth.check_password_policy(bad)
        assert exc.value.status_code == 422
    with pytest.raises(HTTPException):
        adminauth.check_password_policy("same.address@x.io", "same.address@x.io")
    adminauth.check_password_policy("a-long-enough-pass-9")


def test_email_normalised_and_validated():
    assert adminauth.normalize_email("  Admin@Example.COM ") == "admin@example.com"
    with pytest.raises(HTTPException):
        adminauth.normalize_email("not-an-email")


def test_session_token_is_stored_hashed():
    token = "abc"
    assert adminauth.hash_token(token) != token
    assert len(adminauth.hash_token(token)) == 64
    assert adminauth.hash_token(token) == adminauth.hash_token(token)


# ---------------------------------------------------------------- analytics

def test_bot_and_device_detection():
    assert analytics.is_bot("Googlebot/2.1 (+http://www.google.com/bot.html)")
    assert analytics.is_bot("curl/8.0")
    assert analytics.is_bot("")
    ios = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
    assert not analytics.is_bot(ios)
    assert analytics.device_class(ios) == "mobile"
    assert analytics.device_class("Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X)") == "tablet"
    assert analytics.device_class("Mozilla/5.0 (Windows NT 10.0; Win64) Chrome/120") == "desktop"


def test_clean_path_strips_query_and_rejects_private_areas():
    assert analytics.clean_path("/news/12-title?utm=x#top") == "/news/12-title"
    assert analytics.clean_path("/news/") == "/news"
    assert analytics.clean_path("/") == "/"
    for bad in ("/admin", "/admin/analytics", "/api/v1/x", "//evil.com", "http://x.com", "news", "/a b", "/" + "x" * 400):
        assert analytics.clean_path(bad) is None


def test_traffic_source_classification():
    own = "news.example.com"
    assert analytics.classify_source(None, own) == "direct"
    assert analytics.classify_source("news.example.com", own) == "internal"
    assert analytics.classify_source("google.com", own) == "search"
    assert analytics.classify_source("duckduckgo.com", own) == "search"
    assert analytics.classify_source("t.co", own) == "social"
    assert analytics.classify_source("m.facebook.com", own) == "social"
    assert analytics.classify_source("blog.other.org", own) == "referral"
    assert analytics.referrer_host("https://www.Google.com/search?q=secret") == "google.com"
    assert analytics.referrer_host("not a url") is None


def test_visitor_key_is_anonymous_and_rotates_daily():
    today = analytics.visitor_key("203.0.113.9", "UA", date(2026, 10, 22))
    assert today == analytics.visitor_key("203.0.113.9", "UA", date(2026, 10, 22))
    assert today != analytics.visitor_key("203.0.113.9", "UA", date(2026, 10, 23))
    assert today != analytics.visitor_key("203.0.113.10", "UA", date(2026, 10, 22))
    assert "203.0.113.9" not in today and len(today) == 16


def test_tracking_rate_limit():
    key = "rate-test"
    assert not any(analytics.rate_limited(key, limit=5) for _ in range(5))
    assert analytics.rate_limited(key, limit=5)


# ------------------------------------------------------------------- adverts

def test_advert_ids_are_unique_looking_and_unambiguous():
    ids = {adverts.new_advert_id() for _ in range(200)}
    assert len(ids) == 200
    assert all(i.startswith("AD-") and len(i) == 11 and not set("01OI") & set(i[3:]) for i in ids)


def test_destination_must_be_http_url():
    assert adverts.valid_destination(" https://example.com/x?a=1 ") == "https://example.com/x?a=1"
    for bad in ("javascript:alert(1)", "data:text/html,x", "example.com", "ftp://x.com", ""):
        with pytest.raises(HTTPException):
            adverts.valid_destination(bad)


def test_image_must_be_upload_or_https():
    assert adverts.valid_image("/media/ads/abc.png") == "/media/ads/abc.png"
    assert adverts.valid_image("https://cdn.example.com/a.jpg")
    for bad in ("/media/ads/../../etc/passwd", "http://x.com/a.png", "javascript:1", "/other/a.png"):
        with pytest.raises(HTTPException):
            adverts.valid_image(bad)


def test_placements_validated():
    assert adverts.valid_placements(["home_top", "home_top", "article_top"]) == ["article_top", "home_top"]
    for bad in ([], ["nowhere"]):
        with pytest.raises(HTTPException):
            adverts.valid_placements(bad)


def test_upload_type_comes_from_file_content():
    assert adverts.detect_image_type(PNG[:16]) == "png"
    assert adverts.detect_image_type(b"\xff\xd8\xff\xe0" + b"0" * 12) == "jpg"
    assert adverts.detect_image_type(b"GIF89a" + b"0" * 10) == "gif"
    assert adverts.detect_image_type(b"RIFF\x00\x00\x00\x00WEBP" + b"0" * 4) == "webp"
    assert adverts.detect_image_type(b"<svg onload=alert(1)>") is None
    assert adverts.detect_image_type(b"<?php echo 1;") is None


def test_store_image_rejects_bad_uploads(tmp_path, monkeypatch):
    monkeypatch.setattr(adverts.settings, "UPLOAD_DIR", str(tmp_path))
    with pytest.raises(HTTPException) as exc:
        adverts.store_image(b"")
    assert exc.value.status_code == 422
    with pytest.raises(HTTPException) as exc:
        adverts.store_image(b"<svg/>" * 10)
    assert exc.value.status_code == 415
    with pytest.raises(HTTPException) as exc:
        adverts.store_image(PNG + b"0" * adverts.MAX_UPLOAD)
    assert exc.value.status_code == 413
    url = adverts.store_image(PNG)
    assert url.startswith("/media/ads/") and url.endswith(".png")
    assert (tmp_path / "ads" / url.rsplit("/", 1)[1]).read_bytes() == PNG


def test_advert_state_follows_schedule():
    now = datetime(2026, 10, 22, 12, 0, tzinfo=timezone.utc)
    def ad(active=True, **kw):
        return SimpleNamespace(**{"is_active": active, "starts_at": None, "ends_at": None, **kw})

    assert adverts.advert_state(ad(), now) == "live"
    assert adverts.advert_state(ad(active=False), now) == "inactive"
    assert adverts.advert_state(ad(starts_at=now + timedelta(days=1)), now) == "scheduled"
    assert adverts.advert_state(ad(ends_at=now - timedelta(seconds=1)), now) == "expired"
    assert adverts.advert_state(ad(starts_at=now - timedelta(days=1), ends_at=now + timedelta(days=1)), now) == "live"
    with pytest.raises(HTTPException):
        adverts.check_schedule(now, now - timedelta(days=1))


# ------------------------------------------------------------------ settings

def test_settings_are_type_checked_and_private_ones_hidden():
    assert _coerce("site_name", "  My News ") == "My News"
    for key, bad in (("site_name", ""), ("site_name", 5), ("analytics_enabled", "yes"),
                     ("analytics_retention_days", 0), ("analytics_retention_days", True),
                     ("default_og_image", "javascript:1"), ("nope", 1), ("site_tagline", "x" * 500)):
        with pytest.raises(HTTPException):
            _coerce(key, bad)
    visible = public_settings({k: v[1] for k, v in DEFINITIONS.items()})
    assert "site_name" in visible
    assert "analytics_enabled" not in visible and "ads_enabled" not in visible
