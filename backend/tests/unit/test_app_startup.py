"""Startup schema creation: DB_AUTO_CREATE_SCHEMA and its per-environment default."""

from contextlib import asynccontextmanager

import pytest

from app import main
from app.core.config import Settings


@pytest.mark.parametrize(
    ("app_env", "explicit", "expected"),
    [
        ("development", None, True),
        ("staging", None, True),
        ("test", None, True),
        ("production", None, False),
        ("Production ", None, False),
        ("production", True, True),
        ("development", False, False),
    ],
)
def test_auto_create_schema_defaults_by_environment(monkeypatch, app_env, explicit, expected):
    monkeypatch.delenv("DB_AUTO_CREATE_SCHEMA", raising=False)

    settings = Settings(APP_ENV=app_env, DB_AUTO_CREATE_SCHEMA=explicit)

    assert settings.auto_create_schema is expected


class _RecordingConnection:
    def __init__(self, calls):
        self._calls = calls

    async def run_sync(self, function):
        self._calls.append(function)


class _RecordingEngine:
    def __init__(self):
        self.calls = []
        self.disposed = False

    @asynccontextmanager
    async def begin(self):
        yield _RecordingConnection(self.calls)

    async def dispose(self):
        self.disposed = True


class _NoopUsageRecorder:
    async def flush(self):
        return 0


@pytest.mark.parametrize("enabled", [True, False])
async def test_lifespan_creates_tables_only_when_enabled(monkeypatch, enabled):
    engine = _RecordingEngine()
    monkeypatch.setattr(main, "engine", engine)
    monkeypatch.setattr(main, "api_usage_recorder", _NoopUsageRecorder())
    monkeypatch.setattr(main.settings, "DB_AUTO_CREATE_SCHEMA", enabled)

    async with main.lifespan(main.app):
        pass

    expected = [main.Base.metadata.create_all] if enabled else []
    assert engine.calls == expected
    assert engine.disposed is True
