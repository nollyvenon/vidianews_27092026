"""Site administration models: admin accounts, sessions, audit trail, settings,
static pages, analytics, adverts and fetch-cycle history.

They live in the news registry (see app.models.news) so they are created with the
same startup pass and stay independent of the legacy mapper graph.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, Boolean, Column, DateTime, ForeignKey, Index, Integer, JSON, String, Text,
)

from app.models.news import NewsBase


def _utcnow():
    return datetime.now(timezone.utc)


class AdminUser(NewsBase):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(120))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(16), nullable=False, default="editor")  # admin | editor
    is_active = Column(Boolean, nullable=False, default=True)
    last_login_at = Column(DateTime(timezone=True))
    password_changed_at = Column(DateTime(timezone=True), default=_utcnow)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class AdminSession(NewsBase):
    """Server-side session. Only a hash of the cookie value is stored."""
    __tablename__ = "admin_sessions"

    id = Column(Integer, primary_key=True)
    token_hash = Column(String(64), nullable=False, unique=True, index=True)
    csrf_token = Column(String(64), nullable=False)
    admin_id = Column(Integer, ForeignKey("admin_users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    last_seen_at = Column(DateTime(timezone=True), default=_utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True))
    ip_hash = Column(String(16))
    user_agent = Column(String(200))


class AdminLoginAttempt(NewsBase):
    __tablename__ = "admin_login_attempts"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), index=True)
    ip_hash = Column(String(16), index=True)
    success = Column(Boolean, default=False)
    at = Column(DateTime(timezone=True), default=_utcnow, index=True)


class AuditLog(NewsBase):
    """Who changed what: content edits, ad changes, settings, logins."""
    __tablename__ = "admin_audit_log"

    id = Column(Integer, primary_key=True)
    at = Column(DateTime(timezone=True), default=_utcnow, index=True)
    admin_id = Column(Integer, index=True)
    admin_email = Column(String(255))
    action = Column(String(64), nullable=False, index=True)  # e.g. article.update
    entity_type = Column(String(32))
    entity_id = Column(String(64))
    detail = Column(JSON, default=dict)


class SiteSetting(NewsBase):
    __tablename__ = "site_settings"

    key = Column(String(64), primary_key=True)
    value = Column(JSON)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)
    updated_by = Column(String(255))


class SitePage(NewsBase):
    """An editable static page (About, Privacy, ...) served at /p/<slug>."""
    __tablename__ = "site_pages"

    id = Column(Integer, primary_key=True)
    slug = Column(String(80), nullable=False, unique=True, index=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False, default="")
    meta_description = Column(String(320))
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)
    updated_by = Column(String(255))


class PageView(NewsBase):
    """One anonymous page view. No IP address, cookie or user id is stored; the
    visitor key is a hash that changes every day, so people cannot be followed
    across days."""
    __tablename__ = "analytics_page_views"

    id = Column(BigInteger, primary_key=True)
    ts = Column(DateTime(timezone=True), nullable=False, default=_utcnow, index=True)
    path = Column(String(300), nullable=False)
    visitor = Column(String(16), nullable=False)
    is_visit_start = Column(Boolean, nullable=False, default=False)
    country = Column(String(2))
    referrer_host = Column(String(255))
    source = Column(String(16), nullable=False, default="direct")  # direct|search|social|referral|internal
    device = Column(String(10), nullable=False, default="desktop")  # desktop|mobile|tablet

    __table_args__ = (
        Index("idx_pv_path_ts", "path", "ts"),
        Index("idx_pv_visitor_ts", "visitor", "ts"),
    )


class Advert(NewsBase):
    __tablename__ = "adverts"

    id = Column(Integer, primary_key=True)
    advert_id = Column(String(16), nullable=False, unique=True, index=True)  # public unique ID, e.g. AD-7K2M9QXA
    name = Column(String(160), nullable=False)
    image_url = Column(String(2048), nullable=False)  # /media/ads/<file> (uploaded) or an https URL
    destination_url = Column(String(2048), nullable=False)
    alt_text = Column(String(200), nullable=False, default="")
    placements = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    starts_at = Column(DateTime(timezone=True))
    ends_at = Column(DateTime(timezone=True))
    weight = Column(Integer, nullable=False, default=1)
    impressions = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)


class NewsFetchCycle(NewsBase):
    """One complete fetch over all (or one) source(s)."""
    __tablename__ = "news_fetch_cycles"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime(timezone=True), default=_utcnow, index=True)
    finished_at = Column(DateTime(timezone=True))
    status = Column(String(16), nullable=False, default="running")  # running|completed|partial|failed|interrupted
    trigger = Column(String(16), nullable=False, default="scheduled")  # scheduled|manual|startup
    triggered_by = Column(String(255))
    sources_total = Column(Integer, default=0)
    sources_ok = Column(Integer, default=0)
    sources_failed = Column(Integer, default=0)
    items_seen = Column(Integer, default=0)
    items_new = Column(Integer, default=0)
    items_duplicate = Column(Integer, default=0)
    items_rejected = Column(Integer, default=0)
    enriched = Column(Integer, default=0)
    error = Column(Text)
