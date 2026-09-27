"""Logging, Analytics & Documentation endpoints: Modules 46-50"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.models.logging_analytics import *
from app.services.logging_analytics_service import *
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["logging-analytics"])


# ==================== MODULE 46: LOGGING ====================

@router.post("/logs/entry")
async def log_entry(level: str, service: str, message: str, db: AsyncSession = Depends(get_db)):
    service_obj = LoggingService(db)
    entry = await service_obj.log_message(level, service, message)
    return {"id": entry.id, "level": entry.level, "service": entry.service}


@router.get("/logs/{service}")
async def get_logs(service: str, level: str = None, db: AsyncSession = Depends(get_db)):
    service_obj = LoggingService(db)
    logs = await service_obj.get_logs(service, level)
    return [{"id": l.id, "level": l.level, "message": l.message, "timestamp": l.timestamp} for l in logs]


@router.post("/logs/aggregate")
async def aggregate_logs(service: str, db: AsyncSession = Depends(get_db)):
    service_obj = LoggingService(db)
    agg = await service_obj.aggregate_logs(service)
    return {"service": agg.service, "error_count": agg.error_count, "warning_count": agg.warning_count}


# ==================== MODULE 47: ERROR TRACKING ====================

@router.post("/errors/report")
async def report_error(error_type: str, message: str, severity: str = "medium", db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ErrorTrackingService(db)
    error = await service.report_error(error_type, message, user["id"], severity=severity)
    return {"id": error.id, "error_type": error.error_type, "severity": error.severity}


@router.get("/errors/unresolved")
async def get_unresolved_errors(db: AsyncSession = Depends(get_db)):
    service = ErrorTrackingService(db)
    errors = await service.get_unresolved_errors()
    return [{"id": e.id, "error_type": e.error_type, "occurrence_count": e.occurrence_count} for e in errors]


@router.put("/errors/{error_id}/resolve")
async def resolve_error(error_id: int, db: AsyncSession = Depends(get_db)):
    service = ErrorTrackingService(db)
    await service.resolve_error(error_id)
    return {"resolved": True}


# ==================== MODULE 48: FEATURE FLAGS ====================

@router.post("/feature-flags")
async def create_flag(name: str, description: str, db: AsyncSession = Depends(get_db)):
    service = FeatureFlagService(db)
    flag = await service.create_feature_flag(name, description)
    return {"id": flag.id, "name": flag.name, "status": flag.status}


@router.get("/feature-flags/{name}")
async def get_flag(name: str, db: AsyncSession = Depends(get_db)):
    service = FeatureFlagService(db)
    flag = await service.get_feature_flag(name)
    if not flag:
        return {"error": "Flag not found"}
    return {"id": flag.id, "name": flag.name, "status": flag.status, "rollout": flag.rollout_percentage}


@router.put("/feature-flags/{flag_id}/rollout")
async def update_rollout(flag_id: int, percentage: int, db: AsyncSession = Depends(get_db)):
    service = FeatureFlagService(db)
    await service.update_rollout(flag_id, percentage)
    return {"updated": True}


@router.post("/ab-tests")
async def create_ab_test(name: str, flag_id: int, variant_a: str, variant_b: str, db: AsyncSession = Depends(get_db)):
    service = FeatureFlagService(db)
    test = await service.create_ab_test(name, flag_id, variant_a, variant_b)
    return {"id": test.id, "name": test.name}


# ==================== MODULE 49: ANALYTICS ====================

@router.post("/analytics/event")
async def track_event(event_type: str, event_data: dict = {}, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AnalyticsService(db)
    event = await service.track_event(user["id"], event_type, event_data)
    return {"id": event.id, "event_type": event.event_type}


@router.post("/analytics/session")
async def create_session(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AnalyticsService(db)
    session = await service.create_session(user["id"])
    return {"id": session.id, "session_id": session.session_id}


@router.get("/analytics/stats/{event_type}")
async def get_event_stats(event_type: str, db: AsyncSession = Depends(get_db)):
    service = AnalyticsService(db)
    stats = await service.get_event_stats(event_type)
    return stats


# ==================== MODULE 50: DOCUMENTATION ====================

@router.post("/docs")
async def create_documentation(title: str, slug: str, content: str, doc_type: str, db: AsyncSession = Depends(get_db)):
    service = DocumentationService(db)
    doc = await service.create_doc(title, slug, content, doc_type)
    return {"id": doc.id, "title": doc.title, "slug": doc.slug}


@router.get("/docs/{slug}")
async def get_documentation(slug: str, db: AsyncSession = Depends(get_db)):
    service = DocumentationService(db)
    doc = await service.get_doc(slug)
    if not doc:
        return {"error": "Documentation not found"}
    return {"id": doc.id, "title": doc.title, "content": doc.content, "published": doc.published}


@router.put("/docs/{doc_id}/publish")
async def publish_documentation(doc_id: int, db: AsyncSession = Depends(get_db)):
    service = DocumentationService(db)
    await service.publish_doc(doc_id)
    return {"published": True}


@router.post("/docs/api")
async def document_api(endpoint: str, method: str, description: str, db: AsyncSession = Depends(get_db)):
    service = DocumentationService(db)
    api_doc = await service.document_api(endpoint, method, description, {}, {})
    return {"id": api_doc.id, "endpoint": api_doc.endpoint}


@router.get("/docs/api/all")
async def get_api_docs(db: AsyncSession = Depends(get_db)):
    service = DocumentationService(db)
    docs = await service.get_api_docs()
    return [{"id": d.id, "endpoint": d.endpoint, "method": d.method} for d in docs]
