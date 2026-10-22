"""News aggregation models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, Text, Index
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base

# Separate registry: the news tables do not relate to any legacy model, and a
# separate registry keeps their mappers independent of the legacy mapper graph.
NewsBase = declarative_base()


def _utcnow():
    return datetime.now(timezone.utc)


class NewsArticle(NewsBase):
    """An article aggregated from an external news source"""
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)

    # Source attribution
    source_key = Column(String(64), nullable=False, index=True)
    source_name = Column(String(255), nullable=False)
    source_country = Column(String(2), nullable=False, index=True)  # ISO-3166 alpha-2, "XX" = international
    source_type = Column(String(32), default="rss")  # rss | api | community

    # Content
    title = Column(String(500), nullable=False)
    url = Column(String(2048), nullable=False)
    url_hash = Column(String(64), nullable=False, unique=True, index=True)
    title_hash = Column(String(64), nullable=False, index=True)
    author = Column(String(255))
    image_url = Column(String(2048))
    content = Column(Text)  # cleaned text supplied by the feed (may be a teaser)
    summary = Column(Text)  # generated extractive summary
    description = Column(Text)  # generated contextual description
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    fetched_at = Column(DateTime(timezone=True), default=_utcnow)

    # NLP output
    category = Column(String(32), nullable=False, default="general", index=True)
    keywords = Column(JSON, default=list)
    topics = Column(JSON, default=list)
    people = Column(JSON, default=list)
    organizations = Column(JSON, default=list)
    locations = Column(JSON, default=list)
    mentioned_countries = Column(JSON, default=list)
    language = Column(String(8), default="en")
    nlp_engine = Column(String(32), default="rules")  # spacy | rules

    # Validation
    quality_score = Column(Float, default=0.0)
    validation_status = Column(String(16), default="passed", index=True)  # passed | unverified | flagged
    validation_flags = Column(JSON, default=list)
    review_status = Column(String(16), default="none", index=True)  # none | pending | approved | rejected
    reviewed_by = Column(Integer)
    reviewed_at = Column(DateTime(timezone=True))

    # Engagement / ranking
    click_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False, index=True)

    __table_args__ = (
        Index("idx_news_published", "published_at"),
        Index("idx_news_cat_pub", "category", "published_at"),
        Index("idx_news_country_pub", "source_country", "published_at"),
    )


class NewsFetchRun(NewsBase):
    """Audit record for one fetch of one source"""
    __tablename__ = "news_fetch_runs"

    id = Column(Integer, primary_key=True, index=True)
    source_key = Column(String(64), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), default=_utcnow)
    duration_ms = Column(Integer, default=0)
    success = Column(Boolean, default=False)
    items_seen = Column(Integer, default=0)
    items_new = Column(Integer, default=0)
    items_duplicate = Column(Integer, default=0)
    items_rejected = Column(Integer, default=0)
    error = Column(Text)
