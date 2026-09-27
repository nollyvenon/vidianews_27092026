"""Community, Gamification & Compliance endpoints: Modules 61-65"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.models.community_compliance import *
from app.services.community_compliance_service import *
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["community-compliance"])


# MODULE 61: COMMUNITY & FORUMS
@router.post("/forum/thread")
async def create_thread(category: str, title: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = CommunityService(db)
    thread = await service.create_thread(user["id"], category, title)
    return {"id": thread.id, "title": thread.title}

@router.get("/forum/threads")
async def get_threads(category: str = None, db: AsyncSession = Depends(get_db)):
    service = CommunityService(db)
    threads = await service.get_threads(category)
    return [{"id": t.id, "title": t.title, "replies": t.reply_count} for t in threads]

@router.post("/forum/thread/{thread_id}/reply")
async def add_reply(thread_id: int, content: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = CommunityService(db)
    reply = await service.add_reply(thread_id, user["id"], content)
    return {"id": reply.id, "created_at": reply.created_at}


# MODULE 62: GAMIFICATION
@router.post("/badges")
async def create_badge(name: str, description: str, db: AsyncSession = Depends(get_db)):
    service = GamificationService(db)
    badge = await service.create_badge(name, description, "achievement")
    return {"id": badge.id, "name": badge.name}

@router.post("/badges/{badge_id}/award")
async def award_badge(badge_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = GamificationService(db)
    user_badge = await service.award_badge(user["id"], badge_id)
    return {"earned": True}

@router.get("/leaderboard")
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, desc
    stmt = select(Leaderboard).order_by(desc(Leaderboard.points)).limit(10)
    result = await db.execute(stmt)
    entries = result.scalars().all()
    return [{"rank": idx+1, "points": e.points, "views": e.views} for idx, e in enumerate(entries)]


# MODULE 63: REPORTS & EXPORTS
@router.post("/reports")
async def generate_report(report_type: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ReportingService(db)
    report = await service.generate_report(user["id"], report_type, {})
    return {"id": report.id, "type": report.report_type}

@router.get("/reports")
async def get_reports(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ReportingService(db)
    reports = await service.get_creator_reports(user["id"])
    return [{"id": r.id, "type": r.report_type, "generated": r.generated_at} for r in reports]

@router.post("/data-export")
async def request_export(export_type: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ReportingService(db)
    export = await service.request_data_export(user["id"], export_type)
    return {"id": export.id, "status": export.status}


# MODULE 64: COMPLIANCE
@router.post("/compliance/policies")
async def create_policy(name: str, description: str, db: AsyncSession = Depends(get_db)):
    service = ComplianceService(db)
    policy = await service.create_policy(name, description, {})
    return {"id": policy.id, "name": policy.name}

@router.get("/compliance/status")
async def check_compliance(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ComplianceService(db)
    compliance = await service.check_user_compliance(user["id"])
    if not compliance:
        return {"compliant": False}
    return {"gdpr": compliance.gdpr_compliant, "ccpa": compliance.ccpa_compliant}

@router.post("/audit/log")
async def audit_log(action: str, resource: str = None, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = ComplianceService(db)
    log = await service.log_audit(user["id"], action, resource)
    return {"id": log.id, "logged": True}


# MODULE 65: INTERNATIONALIZATION
@router.get("/languages")
async def get_languages(db: AsyncSession = Depends(get_db)):
    stmt = select(Language).where(Language.is_active == True)
    result = await db.execute(stmt)
    langs = result.scalars().all()
    return [{"code": l.code, "name": l.name} for l in langs]

@router.post("/localization/language")
async def set_language(language_code: str, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    service = LocalizationService(db)
    lang = await service.get_or_create_language(language_code, "")
    localization = await service.set_user_language(user["id"], lang.id)
    return {"set": True}

@router.get("/translations/{language_code}/{key}")
async def get_translation(language_code: str, key: str, db: AsyncSession = Depends(get_db)):
    service = LocalizationService(db)
    translation = await service.get_translation(language_code, key)
    if not translation:
        return {"value": key}
    return {"value": translation.value}
