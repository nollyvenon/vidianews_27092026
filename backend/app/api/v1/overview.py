"""Overview figures for the quality, publishing, analytics and monitoring dashboards.

Every figure is computed from stored records. Within the signed-in user's organization, a figure
with no underlying records is reported as ``null`` rather than as a number that looks measured.
"""

import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import psutil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.advanced_platform import BackgroundJob, JobStatus
from app.models.analytics_admin import AnalyticsEvent, AnalyticsEventType
from app.models.content_quality import BrandVoiceCheck, PlagiarismCheck, ProofreadingCheck, ReadabilityScore
from app.models.memberships import MembershipSubscription, MembershipType, SubscriptionStatus
from app.models.organizations import OrganizationMember
from app.models.publishing_distribution import (
    ABTestCampaign, ABTestStatus, EngagementMetric as PublishingEngagement, PublishingJob, PublishingStatus,
)
from app.models.streaming_premium import LiveStream, StreamViewer
from app.models.user import User

router = APIRouter(tags=["overview"])


def _organization(user: User) -> int:
    if user.organization_id is None:
        raise HTTPException(status_code=422, detail="Your account has no organization yet. Create one under Organizations first.")
    return user.organization_id


def _rounded(value: Optional[float], places: int = 2) -> Optional[float]:
    return None if value is None else round(float(value), places)


async def _average_and_count(db: AsyncSession, column, model, organization_id: int):
    row = (await db.execute(
        select(func.avg(column), func.count(model.id)).where(model.organization_id == organization_id)
    )).one()
    return {"checks": int(row[1] or 0), "average": _rounded(row[0])}


@router.get("/content-quality/overview")
async def content_quality_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Average results of the quality checks run in the organization"""
    org = _organization(current_user)
    proofreading = await _average_and_count(db, ProofreadingCheck.quality_score, ProofreadingCheck, org)
    readability = await _average_and_count(db, ReadabilityScore.flesch_kincaid_grade, ReadabilityScore, org)
    brand_voice = await _average_and_count(db, BrandVoiceCheck.compliance_score, BrandVoiceCheck, org)
    plagiarism = await _average_and_count(db, PlagiarismCheck.similarity_percentage, PlagiarismCheck, org)
    return {
        "proofreading": {"checks": proofreading["checks"], "average_score": proofreading["average"]},
        "readability": {"checks": readability["checks"], "average_grade": readability["average"]},
        "brand_voice": {"checks": brand_voice["checks"], "average_compliance": brand_voice["average"]},
        "plagiarism": {"checks": plagiarism["checks"], "average_similarity": plagiarism["average"]},
    }


@router.get("/publishing/overview")
async def publishing_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Publishing queue, engagement, reach and click-through figures for the organization"""
    org = _organization(current_user)
    pending = (await db.execute(
        select(func.count(PublishingJob.id)).where(
            PublishingJob.organization_id == org,
            PublishingJob.status.in_([PublishingStatus.SCHEDULED, PublishingStatus.QUEUED]),
        )
    )).scalar_one()
    engagement = (await db.execute(
        select(
            func.avg(PublishingEngagement.engagement_score),
            func.sum(PublishingEngagement.total_views),
            func.sum(PublishingEngagement.total_clicks),
        ).where(PublishingEngagement.organization_id == org)
    )).one()
    views = int(engagement[1] or 0)
    clicks = int(engagement[2] or 0)
    running_tests = (await db.execute(
        select(func.count(ABTestCampaign.id)).where(
            ABTestCampaign.organization_id == org, ABTestCampaign.status == ABTestStatus.RUNNING
        )
    )).scalar_one()
    return {
        "pending_publications": int(pending or 0),
        "average_engagement": _rounded(engagement[0], 1),
        "distribution_reach": views if views else None,
        "click_through_rate": _rounded(clicks / views * 100) if views else None,
        "running_ab_tests": int(running_tests or 0),
    }


@router.get("/analytics/summary")
async def analytics_summary(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Views, live watch time and active subscribers for the organization over the last ``days`` days"""
    org = _organization(current_user)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    views = (await db.execute(
        select(func.count(AnalyticsEvent.id)).where(
            AnalyticsEvent.organization_id == org,
            AnalyticsEvent.event_type.in_([AnalyticsEventType.PAGE_VIEW, AnalyticsEventType.CONTENT_VIEW]),
            AnalyticsEvent.created_at >= since.replace(tzinfo=None),
        )
    )).scalar_one()

    member_ids = select(OrganizationMember.user_id).where(OrganizationMember.organization_id == org)
    watch_seconds = (await db.execute(
        select(func.coalesce(func.sum(StreamViewer.watch_duration_seconds), 0))
        .join(LiveStream, StreamViewer.stream_id == LiveStream.id)
        .where(LiveStream.creator_id.in_(member_ids), StreamViewer.joined_at >= since)
    )).scalar_one()

    subscribers = (await db.execute(
        select(func.count(MembershipSubscription.id))
        .join(MembershipType, MembershipSubscription.membership_type_id == MembershipType.id)
        .where(MembershipType.organization_id == org, MembershipSubscription.status == SubscriptionStatus.ACTIVE)
    )).scalar_one()

    return {
        "days": days,
        "views": int(views or 0),
        "watch_hours": round(float(watch_seconds or 0) / 3600, 2),
        "subscribers": int(subscribers or 0),
    }


@router.get("/system/health/checks")
async def system_health_checks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Live figures for this server and checks of its dependencies: the database answers, and background jobs are not failing"""
    started = time.perf_counter()
    await db.execute(text("SELECT 1"))
    database_ms = round((time.perf_counter() - started) * 1000, 2)

    counts = dict((await db.execute(
        select(BackgroundJob.status, func.count(BackgroundJob.id)).group_by(BackgroundJob.status)
    )).all())
    pending = int(counts.get(JobStatus.PENDING, 0) or 0)
    running = int(counts.get(JobStatus.RUNNING, 0) or 0)
    failed = int(counts.get(JobStatus.FAILED, 0) or 0)

    metrics = {
        "cpu_percent": round(psutil.cpu_percent(interval=0.1), 1),
        "memory_percent": round(psutil.virtual_memory().percent, 1),
        "disk_percent": round(psutil.disk_usage(os.path.abspath(os.sep)).percent, 1),
        "database_latency_ms": database_ms,
    }
    return {
        "metrics": metrics,
        "checks": [
            {"name": "Database", "status": "healthy", "latency_ms": database_ms},
            {
                "name": "Background jobs",
                "status": "degraded" if failed else "healthy",
                "pending": pending,
                "running": running,
                "failed": failed,
            },
        ]
    }
