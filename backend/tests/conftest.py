"""Pytest configuration and fixtures"""

import asyncio
import os

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient

from tests.db_config import TEST_DATABASE_URL, TEST_SYNC_DATABASE_URL, truncate_all_tables

# app.core.config reads DATABASE_URL at import time. Point it at the test
# database before any app module is imported so the suite never touches dev data.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
# Never pool connections across event loops (TestClient runs the app on its own loop).
os.environ["DB_NULL_POOL"] = "true"

from app.db.base import Base  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def reset_test_database():
    """Recreate this run's PostgreSQL test database from the current models.

    Dropping and recreating the whole database (rather than its schema) takes no
    per-table locks, so parallel workers cannot exhaust the server's lock table.
    Refuses to touch any database whose name does not end in ``_test``.
    """
    url = make_url(TEST_SYNC_DATABASE_URL)
    database = url.database or ""
    if not database.endswith("_test"):
        raise RuntimeError(f"Refusing to reset non-test database {database!r}")

    admin_engine = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{database}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{database}"'))
    admin_engine.dispose()

    engine = create_engine(TEST_SYNC_DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        Base.metadata.create_all(conn)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def isolate_database(reset_test_database):
    """Empty every table before each test so no test sees another test's rows."""
    with reset_test_database.connect() as conn:
        truncate_all_tables(conn)
    yield


@pytest.fixture
def reference_data(isolate_database, reset_test_database):
    """Commit the reference rows (users 1-2, tenant, organization, content 1) for this test."""
    from sqlalchemy.orm import Session

    from tests.seed import seed_reference_data

    with Session(reset_test_database) as session:
        seed_reference_data(session)
    yield


@pytest.fixture
async def test_engine():
    """Create test database engine"""
    # The schema is created once per session by reset_test_database.
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

    yield engine

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create test database session"""
    async_session_local = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_local() as session:
        yield session


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
async def async_client(test_session):
    """Create async test client with test database"""
    async def override_get_db():
        yield test_session

    # The app has two async session dependencies (get_db and get_session); route
    # every request through the test session so writes made by fixtures are visible.
    from app.db.session import get_db, get_session
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session] = override_get_db

    # ASGITransport replaces the `app=` argument, which httpx 0.28 removed; it works on the pinned 0.25 too.
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def session(test_session):
    """The per-test async session, shared with async_client so fixture writes are visible to requests"""
    yield test_session


@pytest.fixture
async def db(session):
    """Alias of `session` for tests that name the async session `db`"""
    yield session


@pytest.fixture(autouse=True)
def _isolated_usage_recorder():
    """Counts are batched in one process-wide recorder; drop anything a previous test left unwritten."""
    from app.main import api_usage_recorder

    api_usage_recorder.discard_pending()
    yield
    api_usage_recorder.discard_pending()


@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
    }
