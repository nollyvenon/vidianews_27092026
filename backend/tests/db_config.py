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


# Runs on the server in one transaction. A table with no heap pages cannot hold
# rows, so the catalog's pg_relation_size selects the tables that might contain
# data in a single query, without planning a statement for each of the ~350
# tables. Only those are emptied. Foreign-key triggers are disabled for the
# transaction with SET LOCAL session_replication_role, so the tables can be
# emptied in any order. TRUNCATE is not used: it cascades through every
# referencing table and costs far more per table on this platform.
# synchronous_commit is off because this database is disposable; skipping the
# WAL flush at commit is safe here.
_TRUNCATE_WRITTEN_TABLES_SQL = """
BEGIN;
SET LOCAL synchronous_commit = off;
SET LOCAL session_replication_role = replica;
DO $$
DECLARE
    tbl record;
BEGIN
    FOR tbl IN
        SELECT c.relname
        FROM pg_class c
        WHERE c.relnamespace = 'public'::regnamespace
          AND c.relkind = 'r'
          AND pg_relation_size(c.oid) > 0
    LOOP
        EXECUTE 'DELETE FROM ' || quote_ident(tbl.relname);
    END LOOP;
END
$$;
COMMIT;
"""


def truncate_all_tables(connection) -> None:
    """Empty every table in the schema, keeping the schema itself.

    Use an autocommit connection. The reset is one transaction, so it either
    empties every table or leaves the data untouched.
    """
    connection.exec_driver_sql("SET lock_timeout = '10s'")
    try:
        connection.exec_driver_sql(_TRUNCATE_WRITTEN_TABLES_SQL)
    except Exception:
        connection.exec_driver_sql("ROLLBACK")
        raise
