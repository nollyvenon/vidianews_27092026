"""Test reports: CI uploads results per suite; the dashboard reads them back.

Counts and pass rates are computed from the uploaded per-test results, never taken from the client.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_monitoring import TestResult, TestSuite


def _pass_rate(passed: int, failed: int) -> Optional[float]:
    executed = passed + failed
    return round(passed / executed * 100, 1) if executed else None


def suite_view(suite: TestSuite) -> Dict[str, Any]:
    return {
        "id": suite.id,
        "name": suite.name,
        "test_count": suite.test_count or 0,
        "passed": suite.passed or 0,
        "failed": suite.failed or 0,
        "skipped": suite.skipped or 0,
        "pass_rate": _pass_rate(suite.passed or 0, suite.failed or 0),
        "coverage_percentage": suite.coverage_percentage,
        "last_run_at": suite.last_run_at,
    }


def result_view(result: TestResult) -> Dict[str, Any]:
    return {
        "id": result.id,
        "test_name": result.test_name,
        "status": result.status,
        "duration_ms": result.duration_ms,
        "error_message": result.error_message,
        "run_at": result.run_at,
    }


class TestReportsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def ingest_run(
        self,
        suite_name: str,
        results: List[Dict[str, Any]],
        coverage_percentage: Optional[float],
    ) -> TestSuite:
        now = datetime.now(timezone.utc)
        suite = (await self.session.execute(
            select(TestSuite).where(TestSuite.name == suite_name)
        )).scalar_one_or_none()
        if suite is None:
            suite = TestSuite(name=suite_name)
            self.session.add(suite)
            await self.session.flush()

        statuses = [item["status"] for item in results]
        suite.test_count = len(results)
        suite.passed = statuses.count("passed")
        suite.failed = statuses.count("failed")
        suite.skipped = statuses.count("skipped")
        if coverage_percentage is not None:
            suite.coverage_percentage = coverage_percentage
        suite.last_run_at = now

        for item in results:
            self.session.add(TestResult(
                test_suite_id=suite.id,
                test_name=item["name"],
                status=item["status"],
                duration_ms=item["duration_ms"],
                error_message=item.get("error_message"),
                run_at=now,
            ))
        await self.session.commit()
        await self.session.refresh(suite)
        return suite

    async def list_suites(self) -> List[TestSuite]:
        result = await self.session.execute(select(TestSuite).order_by(TestSuite.name))
        return list(result.scalars().all())

    async def get_suite(self, suite_id: int) -> Optional[TestSuite]:
        return await self.session.get(TestSuite, suite_id)

    async def recent_results(self, suite_id: int, limit: int, status: Optional[str] = None) -> List[TestResult]:
        stmt = select(TestResult).where(TestResult.test_suite_id == suite_id)
        if status is not None:
            stmt = stmt.where(TestResult.status == status)
        result = await self.session.execute(
            stmt.order_by(TestResult.run_at.desc(), TestResult.id.desc()).limit(limit)
        )
        return list(result.scalars().all())
