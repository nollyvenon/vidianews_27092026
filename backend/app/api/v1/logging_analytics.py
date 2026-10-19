"""Logging, Analytics & Documentation endpoints: Modules 46-50"""

from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.session import get_db
from app.models.logging_analytics import *
from app.services.logging_analytics_service import *
from app.core.security import get_current_user

router = APIRouter(tags=["logging-analytics"])


# ==================== MODULE 46: LOGGING ====================

@router.post("/logs/entry")
async def log_entry(level: str, service: str, message: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service_obj = LoggingService(db)
    entry = await service_obj.log_message(level, service, message)
    return {"id": entry.id, "level": entry.level, "service": entry.service}


@router.get("/logs/{service}")
async def get_logs(service: str, level: str = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service_obj = LoggingService(db)
    logs = await service_obj.get_logs(service, level)
    return [{"id": l.id, "level": l.level, "message": l.message, "timestamp": l.timestamp} for l in logs]


@router.post("/logs/aggregate")
async def aggregate_logs(service: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service_obj = LoggingService(db)
    agg = await service_obj.aggregate_logs(service)
    return {"service": agg.service, "error_count": agg.error_count, "warning_count": agg.warning_count}


# ==================== MODULE 47: ERROR TRACKING ====================

@router.post("/errors/report")
async def report_error(error_type: str, message: str, severity: str = "medium", db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = ErrorTrackingService(db)
    error = await service.report_error(error_type, message, user.id, severity=severity)
    return {"id": error.id, "error_type": error.error_type, "severity": error.severity}


@router.get("/errors/unresolved")
async def get_unresolved_errors(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ErrorTrackingService(db)
    errors = await service.get_unresolved_errors()
    return [{"id": e.id, "error_type": e.error_type, "occurrence_count": e.occurrence_count} for e in errors]


@router.put("/errors/{error_id}/resolve")
async def resolve_error(error_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ErrorTrackingService(db)
    await service.resolve_error(error_id)
    return {"resolved": True}


# ==================== MODULE 48: FEATURE FLAGS ====================

@router.post("/feature-flags")
async def create_flag(name: str, description: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FeatureFlagService(db)
    flag = await service.create_feature_flag(name, description)
    return {"id": flag.id, "name": flag.name, "status": flag.status}


@router.get("/feature-flags/{name}")
async def get_flag(name: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FeatureFlagService(db)
    flag = await service.get_feature_flag(name)
    if not flag:
        return {"error": "Flag not found"}
    return {"id": flag.id, "name": flag.name, "status": flag.status, "rollout": flag.rollout_percentage}


@router.put("/feature-flags/{flag_id}/rollout")
async def update_rollout(flag_id: int, percentage: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FeatureFlagService(db)
    await service.update_rollout(flag_id, percentage)
    return {"updated": True}


@router.post("/logging/ab-tests")
async def create_ab_test(name: str, flag_id: int, variant_a: str, variant_b: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FeatureFlagService(db)
    test = await service.create_ab_test(name, flag_id, variant_a, variant_b)
    return {"id": test.id, "name": test.name}


# ==================== MODULE 49: ANALYTICS ====================

@router.post("/analytics/event")
async def track_event(event_type: str, event_data: Optional[dict] = None, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = AnalyticsService(db)
    event = await service.track_event(user.id, event_type, event_data)
    return {"id": event.id, "event_type": event.event_type}


@router.post("/analytics/session")
async def create_session(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    service = AnalyticsService(db)
    session = await service.create_session(user.id)
    return {"id": session.id, "session_id": session.session_id}


@router.get("/analytics/stats/{event_type}")
async def get_event_stats(event_type: AnalyticsEventType, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = AnalyticsService(db)
    stats = await service.get_event_stats(event_type)
    return stats


# ==================== MODULE 50: DOCUMENTATION ====================

class DocumentationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    slug: str = Field(min_length=1, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    content: str = Field(min_length=1, max_length=100_000)
    doc_type: DocType


@router.get("/docs")
async def list_documentation(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Published documents, most viewed first"""
    service = DocumentationService(db)
    docs = await service.list_published_docs()
    return [
        {"id": d.id, "title": d.title, "slug": d.slug, "doc_type": d.doc_type.value, "views": d.views or 0, "version": d.version}
        for d in docs
    ]


@router.post("/docs", status_code=201)
async def create_documentation(request: DocumentationRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentationService(db)
    if await service.get_doc(request.slug) is not None:
        raise HTTPException(status_code=409, detail="A document with this slug already exists")
    doc = await service.create_doc(request.title, request.slug, request.content, request.doc_type, current_user.email)
    return {"id": doc.id, "title": doc.title, "slug": doc.slug, "published": bool(doc.published)}


@router.get("/docs/{slug}")
async def get_documentation(slug: str, db: AsyncSession = Depends(get_db)):
    """A published document. Each read counts as a view."""
    service = DocumentationService(db)
    doc = await service.get_published_doc(slug)
    if doc is None:
        raise HTTPException(status_code=404, detail="Documentation not found")
    # Read the count before recording the view: the update may refresh the loaded object in the session.
    views_after_this_read = (doc.views or 0) + 1
    await service.record_view(doc.id)
    return {"id": doc.id, "title": doc.title, "content": doc.content, "published": bool(doc.published), "views": views_after_this_read}


@router.put("/docs/{doc_id}/publish")
async def publish_documentation(doc_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentationService(db)
    await service.publish_doc(doc_id)
    return {"published": True}


@router.post("/docs/api")
async def document_api(endpoint: str, method: str, description: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentationService(db)
    api_doc = await service.document_api(endpoint, method, description, {}, {})
    return {"id": api_doc.id, "endpoint": api_doc.endpoint}


@router.get("/docs/api/all")
async def get_api_docs(db: AsyncSession = Depends(get_db)):
    service = DocumentationService(db)
    docs = await service.get_api_docs()
    return [{"id": d.id, "endpoint": d.endpoint, "method": d.method} for d in docs]
