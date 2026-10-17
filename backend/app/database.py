"""Synchronous PostgreSQL session for the legacy blocking routers.

The advanced, platform-completion and enterprise routers use blocking
SQLAlchemy ``Session`` objects. This module supplies that session on the same
PostgreSQL database and the same declarative ``Base`` used by the async stack
in ``app.db``, so both stacks share one schema.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base

__all__ = ["Base", "SessionLocal", "engine", "get_db"]


def _sync_database_url(url: str) -> str:
    """Rewrite an async PostgreSQL URL to the psycopg2 driver used for blocking sessions."""
    return make_url(url).set(drivername="postgresql+psycopg2").render_as_string(hide_password=False)


engine = create_engine(
    _sync_database_url(settings.DATABASE_URL),
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a blocking SQLAlchemy session that is always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
