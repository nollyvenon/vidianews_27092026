"""Test reports: CI uploads per-suite results (admin); signed-in users read them."""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import require_admin
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.test_reports_service import TestReportsService, result_view, suite_view

router = APIRouter(prefix="/test-reports", tags=["test-reports"])

require_test_report_admin = require_admin("test_reports")


class TestCaseIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    status: Literal["passed", "failed", "skipped"]
    duration_ms: float = Field(..., ge=0, le=3_600_000)
    error_message: Optional[str] = Field(None, max_length=2000)


class TestRunIn(BaseModel):
    suite: str = Field(..., min_length=1, max_length=255)
    results: List[TestCaseIn] = Field(..., min_length=1, max_length=5000)
    coverage_percentage: Optional[float] = Field(None, ge=0, le=100)


class SuiteOut(BaseModel):
    id: int
    name: str
    test_count: int
    passed: int
    failed: int
    skipped: int
    pass_rate: Optional[float]
    coverage_percentage: Optional[float]
    last_run_at: Optional[datetime]


class TestResultOut(BaseModel):
    id: int
    test_name: str
    status: Optional[str]
    duration_ms: Optional[float]
    error_message: Optional[str]
    run_at: Optional[datetime]


class SuiteDetailOut(BaseModel):
    suite: SuiteOut
    results: List[TestResultOut]


@router.post("/runs", response_model=SuiteOut, status_code=status.HTTP_201_CREATED)
async def record_run(
    payload: TestRunIn,
    _admin: User = Depends(require_test_report_admin),
    session: AsyncSession = Depends(get_db),
):
    """Record one test run for a suite. Counts are computed from ``results``."""
    results: List[Dict[str, Any]] = [item.model_dump() for item in payload.results]
    suite = await TestReportsService(session).ingest_run(payload.suite, results, payload.coverage_percentage)
    return suite_view(suite)


@router.get("/suites", response_model=List[SuiteOut])
async def list_suites(_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    suites = await TestReportsService(session).list_suites()
    return [suite_view(suite) for suite in suites]


@router.get("/suites/{suite_id}", response_model=SuiteDetailOut)
async def get_suite(
    suite_id: int,
    limit: int = Query(50, ge=1, le=200),
    status_filter: Optional[Literal["passed", "failed", "skipped"]] = Query(None, alias="status"),
    _user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = TestReportsService(session)
    suite = await service.get_suite(suite_id)
    if suite is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test suite not found")
    results = await service.recent_results(suite_id, limit, status_filter)
    return {"suite": suite_view(suite), "results": [result_view(result) for result in results]}
