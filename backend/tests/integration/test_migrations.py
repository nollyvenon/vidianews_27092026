"""Schema migrations: the revisions build exactly the models' schema and can be reversed.

Each test migrates a fresh scratch database, so the suite's own database is never
touched. The scratch database name ends in ``_test``, like every other test database.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url

import app.models  # noqa: F401  registers every table on Base.metadata
from app.db.base import Base
from tests.db_config import TEST_DATABASE_URL, TEST_SYNC_DATABASE_URL

BACKEND_DIR = Path(__file__).resolve().parents[2]


def _scratch_database_name() -> str:
    """Name the migration scratch database after the suite's database, ending in ``_test``."""
    base = make_url(TEST_SYNC_DATABASE_URL).database or "vidianews_test"
    root = base[: -len("_test")] if base.endswith("_test") else base
    return f"{root}_migrations_test"


@pytest.fixture
def scratch_urls():
    """Create an empty scratch database and yield its (asyncpg, psycopg2) URLs."""
    name = _scratch_database_name()
    assert name.endswith("_test")
    admin_engine = create_engine(
        make_url(TEST_SYNC_DATABASE_URL).set(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )
    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{name}"'))
    try:
        yield (
            make_url(TEST_DATABASE_URL).set(database=name).render_as_string(hide_password=False),
            make_url(TEST_SYNC_DATABASE_URL).set(database=name).render_as_string(hide_password=False),
        )
    finally:
        with admin_engine.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        admin_engine.dispose()


def _run_in_worker_thread(function, *args):
    """Run an alembic command on a worker thread.

    The migration environment drives its async engine with ``asyncio.run``, which
    clears the event loop of the thread it runs on. Running it on a worker keeps
    the event loop that the rest of the test session depends on intact.
    """
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(function, *args).result()


def _alembic_config(async_url: str) -> Config:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    config.attributes["sqlalchemy_url"] = async_url
    return config


def test_migrations_have_a_single_head():
    config = _alembic_config(TEST_DATABASE_URL)

    heads = ScriptDirectory.from_config(config).get_heads()

    assert len(heads) == 1, f"Migration branches diverged: {heads}"


def test_upgrade_head_builds_exactly_the_models_schema(scratch_urls):
    async_url, sync_url = scratch_urls
    _run_in_worker_thread(command.upgrade, _alembic_config(async_url), "head")

    engine = create_engine(sync_url)
    try:
        with engine.connect() as conn:
            differences = compare_metadata(
                MigrationContext.configure(conn, opts={"compare_type": True}),
                Base.metadata,
            )
            table_names = set(inspect(conn).get_table_names()) - {"alembic_version"}
    finally:
        engine.dispose()

    assert differences == [], f"Migrated schema differs from the models: {differences}"
    assert table_names == set(Base.metadata.tables)


def test_downgrade_base_removes_every_table(scratch_urls):
    async_url, sync_url = scratch_urls
    config = _alembic_config(async_url)
    _run_in_worker_thread(command.upgrade, config, "head")
    _run_in_worker_thread(command.downgrade, config, "base")

    engine = create_engine(sync_url)
    try:
        remaining = set(inspect(engine).get_table_names())
    finally:
        engine.dispose()

    assert remaining == {"alembic_version"}
