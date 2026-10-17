"""Shared PostgreSQL configuration for the backend test suite.

The whole suite runs against a real PostgreSQL database; SQLite is not used.
Set TEST_DATABASE_URL to point at a different server. The database name must
end in ``_test`` because the test session drops and recreates its ``public``
schema, and that guard keeps the development database out of reach.
"""

import os

from sqlalchemy.engine import make_url

DEFAULT_TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/vidianews_test"


def _with_driver(url: str, driver: str) -> str:
    """Return ``url`` rewritten to use the given PostgreSQL driver."""
    return make_url(url).set(drivername=f"postgresql+{driver}").render_as_string(hide_password=False)


def _per_worker_url(url: str) -> str:
    """Give each pytest-xdist worker its own database so parallel runs never share rows.

    ``vidianews_test`` becomes ``vidianews_gw0_test`` for worker ``gw0``. The name
    still ends in ``_test``, so the reset guard in conftest keeps applying.
    """
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    if not worker:
        return url
    parsed = make_url(url)
    name = parsed.database or ""
    root = name[: -len("_test")] if name.endswith("_test") else name
    return parsed.set(database=f"{root}_{worker}_test").render_as_string(hide_password=False)


TEST_DATABASE_URL = _with_driver(
    _per_worker_url(os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DATABASE_URL)), "asyncpg"
)
TEST_SYNC_DATABASE_URL = _with_driver(TEST_DATABASE_URL, "psycopg2")


def truncate_all_tables(connection) -> None:
    """Empty every table in the schema, keeping the schema itself.

    Use an autocommit connection. Each DELETE then commits on its own and
    releases its locks, so parallel workers never exhaust PostgreSQL's shared
    lock table. Foreign-key triggers are skipped so tables can be emptied in
    any order.
    """
    from sqlalchemy import text

    from app.db.base import Base

    connection.execute(text("SET lock_timeout = '10s'"))
    connection.execute(text("SET session_replication_role = replica"))
    try:
        for table in Base.metadata.sorted_tables:
            connection.execute(text(f'DELETE FROM "{table.name}"'))
    finally:
        connection.execute(text("SET session_replication_role = origin"))
