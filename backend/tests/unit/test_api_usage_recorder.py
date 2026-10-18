"""Unit tests for the API usage recorder: aggregation, batching, failure handling and the database write."""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.advanced_platform import APIUsageMetrics
from app.services import api_usage_recorder as recorder_module
from app.services.api_usage_recorder import ApiUsageRecorder


class _Clock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


class _FailingSessionFactory:
    """Stands in for a database that cannot be reached."""

    def __call__(self):
        return self

    async def __aenter__(self):
        raise ConnectionError("database unavailable")

    async def __aexit__(self, *exc):
        return False


@pytest.fixture
def factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)


async def _rows(factory):
    async with factory() as session:
        return (await session.execute(select(APIUsageMetrics).order_by(APIUsageMetrics.id))).scalars().all()


async def test_flush_writes_call_error_and_timing_totals(factory):
    recorder = ApiUsageRecorder(factory, clock=_Clock())
    await recorder.record("GET", "/api/v1/things", 200, 10.0)
    await recorder.record("GET", "/api/v1/things", 200, 30.0)
    await recorder.record("GET", "/api/v1/things", 500, 20.0)

    written = await recorder.flush()

    assert written == 3
    row, = await _rows(factory)
    assert (row.endpoint, row.method) == ("/api/v1/things", "GET")
    assert row.call_count == 3
    assert row.error_count == 1
    assert row.average_response_time_ms == pytest.approx(20.0)
    assert row.max_response_time_ms == pytest.approx(30.0)
    assert row.min_response_time_ms == pytest.approx(10.0)


async def test_later_flushes_extend_the_running_totals(factory):
    recorder = ApiUsageRecorder(factory, clock=_Clock())
    await recorder.record("POST", "/api/v1/things", 201, 100.0)
    await recorder.flush()
    await recorder.record("POST", "/api/v1/things", 201, 300.0)
    await recorder.record("POST", "/api/v1/things", 201, 50.0)
    await recorder.flush()

    row, = await _rows(factory)
    assert row.call_count == 3
    assert row.average_response_time_ms == pytest.approx(150.0)
    assert row.max_response_time_ms == pytest.approx(300.0)
    assert row.min_response_time_ms == pytest.approx(50.0)


async def test_methods_and_endpoints_are_kept_apart(factory):
    recorder = ApiUsageRecorder(factory, clock=_Clock())
    await recorder.record("GET", "/api/v1/a", 200, 1.0)
    await recorder.record("POST", "/api/v1/a", 200, 1.0)
    await recorder.record("GET", "/api/v1/b", 200, 1.0)
    await recorder.flush()

    keys = sorted((row.method, row.endpoint) for row in await _rows(factory))
    assert keys == [("GET", "/api/v1/a"), ("GET", "/api/v1/b"), ("POST", "/api/v1/a")]


async def test_flush_with_nothing_pending_writes_nothing(factory):
    recorder = ApiUsageRecorder(factory, clock=_Clock())

    assert await recorder.flush() == 0
    assert await _rows(factory) == []


async def test_a_batch_is_written_automatically_at_the_threshold(factory):
    recorder = ApiUsageRecorder(factory, clock=_Clock())
    for _ in range(recorder_module.FLUSH_THRESHOLD):
        await recorder.record("GET", "/api/v1/busy", 200, 2.0)

    row, = await _rows(factory)
    assert row.call_count == recorder_module.FLUSH_THRESHOLD


async def test_a_batch_is_written_automatically_after_the_interval(factory):
    clock = _Clock()
    recorder = ApiUsageRecorder(factory, clock=clock)
    await recorder.record("GET", "/api/v1/quiet", 200, 2.0)
    assert await _rows(factory) == []

    clock.now += recorder_module.FLUSH_INTERVAL_SECONDS
    await recorder.record("GET", "/api/v1/quiet", 200, 2.0)

    row, = await _rows(factory)
    assert row.call_count == 2


async def test_a_failed_write_keeps_the_counts_for_the_next_flush(factory):
    recorder = ApiUsageRecorder(_FailingSessionFactory(), clock=_Clock())
    await recorder.record("GET", "/api/v1/things", 200, 4.0)
    await recorder.record("GET", "/api/v1/things", 503, 6.0)

    assert await recorder.flush() == 0

    recorder._session_factory = factory  # the database is reachable again
    assert await recorder.flush() == 2
    row, = await _rows(factory)
    assert (row.call_count, row.error_count) == (2, 1)
    assert row.average_response_time_ms == pytest.approx(5.0)


async def test_long_endpoint_names_are_truncated_to_the_column_length(factory):
    recorder = ApiUsageRecorder(factory, clock=_Clock())
    await recorder.record("GET", "/api/v1/" + "x" * 600, 200, 1.0)
    await recorder.flush()

    row, = await _rows(factory)
    assert len(row.endpoint) == recorder_module.ENDPOINT_COLUMN_LENGTH
