"""Admin panel API: sign-in, session, account, site settings, audit trail, SEO report.

Everything except /auth/login requires a valid admin session; writes also need the
CSRF header (see app.services.site.adminauth).
"""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.news import NewsArticle as A
from app.models.site import AdminSession, AdminUser, AuditLog, SitePage
from app.services.news.quality import sweep as quality_sweep
from app.services.site import adminauth as auth
from app.services.site.sitesettings import DEFINITIONS, load_settings, save_settings

router = APIRouter()


class LoginBody(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=200)


@router.post("/auth/login")
async def login(body: LoginBody, request: Request, response: Response, db: AsyncSession = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    return await auth.login(db, request, response, body.email, body.password)


@router.post("/auth/logout")
async def logout(response: Response, ctx: auth.AdminCtx = Depends(auth.require_staff),
                 db: AsyncSession = Depends(get_session)):
    await auth.revoke_session(db, ctx.session)
    response.delete_cookie(auth.COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/auth/me")
async def me(response: Response, ctx: auth.AdminCtx = Depends(auth.require_staff)):
    response.headers["Cache-Control"] = "no-store"
    return {"user": auth.public_user(ctx.user), "csrf_token": ctx.session.csrf_token,
            "session_expires_at": ctx.session.expires_at.isoformat()}


class PasswordBody(BaseModel):
    current_password: str = Field(max_length=200)
    new_password: str = Field(max_length=200)


@router.post("/auth/change-password")
async def change_password(body: PasswordBody, ctx: auth.AdminCtx = Depends(auth.require_staff),
                          db: AsyncSession = Depends(get_session)):
    await auth.change_password(db, ctx, body.current_password, body.new_password)
    return {"ok": True}


# ------------------------------------------------------------------ settings

@router.get("/settings")
async def get_settings(ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    return {"settings": await load_settings(db, fresh=True),
            "definitions": {k: {"type": v[0].__name__, "max": v[2]} for k, v in DEFINITIONS.items()}}


class SettingsBody(BaseModel):
    values: Dict[str, Any]


@router.put("/settings")
async def put_settings(body: SettingsBody, ctx: auth.AdminCtx = Depends(auth.require_admin),
                       db: AsyncSession = Depends(get_session)):
    before = await load_settings(db, fresh=True)
    saved = await save_settings(db, body.values, ctx.email)
    auth.audit(db, ctx, "settings.update", "settings", "", {
        k: [before.get(k), v] for k, v in saved.items() if before.get(k) != v})
    await db.commit()
    current = await load_settings(db, fresh=True)
    if before.get("news_min_content_chars") != current["news_min_content_chars"]:
        asyncio.create_task(quality_sweep(current["news_min_content_chars"]))  # apply the new minimum to stored stories
    return {"settings": current}


# --------------------------------------------------------------------- audit

@router.get("/audit")
async def audit_log(page: int = Query(1, ge=1, le=1000), page_size: int = Query(30, ge=1, le=100),
                    action: Optional[str] = Query(None, max_length=64),
                    ctx: auth.AdminCtx = Depends(auth.require_admin), db: AsyncSession = Depends(get_session)):
    conds = [AuditLog.action.like(action.replace("%", "") + "%")] if action else []
    total = (await db.execute(select(func.count()).select_from(AuditLog).where(*conds))).scalar_one()
    rows = (await db.execute(select(AuditLog).where(*conds).order_by(AuditLog.id.desc())
                             .offset((page - 1) * page_size).limit(page_size))).scalars().all()
    return {"total": total, "page": page, "page_size": page_size, "items": [
        {"id": r.id, "at": r.at.isoformat(), "admin": r.admin_email, "action": r.action,
         "entity_type": r.entity_type, "entity_id": r.entity_id, "detail": r.detail} for r in rows]}


@router.get("/sessions")
async def my_sessions(ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    now = datetime.now(timezone.utc)
    rows = (await db.execute(select(AdminSession).where(
        AdminSession.admin_id == ctx.user.id, AdminSession.revoked_at.is_(None), AdminSession.expires_at > now
    ).order_by(AdminSession.last_seen_at.desc()))).scalars().all()
    return {"items": [{"id": s.id, "created_at": s.created_at.isoformat(), "last_seen_at": s.last_seen_at.isoformat(),
                       "user_agent": s.user_agent, "current": s.id == ctx.session.id} for s in rows]}


@router.get("/users")
async def list_admins(ctx: auth.AdminCtx = Depends(auth.require_admin), db: AsyncSession = Depends(get_session)):
    rows = (await db.execute(select(AdminUser).order_by(AdminUser.id))).scalars().all()
    return {"items": [{**auth.public_user(u), "is_active": u.is_active} for u in rows]}


class NewAdmin(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=200)
    role: str = Field("editor", pattern="^(admin|editor)$")
    name: Optional[str] = Field(None, max_length=120)


@router.post("/users", status_code=201)
async def add_admin(body: NewAdmin, ctx: auth.AdminCtx = Depends(auth.require_admin),
                    db: AsyncSession = Depends(get_session)):
    user = await auth.create_admin(db, body.email, body.password, body.role, body.name)
    auth.audit(db, ctx, "user.create", "admin_user", user.id, {"email": user.email, "role": user.role})
    await db.commit()
    return auth.public_user(user)


class UserPatch(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = Field(None, pattern="^(admin|editor)$")


@router.patch("/users/{user_id}")
async def patch_admin(user_id: int, body: UserPatch, ctx: auth.AdminCtx = Depends(auth.require_admin),
                      db: AsyncSession = Depends(get_session)):
    user = await db.get(AdminUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Admin not found")
    if user.id == ctx.user.id:
        raise HTTPException(status_code=400, detail="You cannot change your own role or disable yourself")
    changes = body.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(user, key, value)
    if changes.get("is_active") is False:
        for s in (await db.execute(select(AdminSession).where(
                AdminSession.admin_id == user.id, AdminSession.revoked_at.is_(None)))).scalars():
            s.revoked_at = datetime.now(timezone.utc)
    auth.audit(db, ctx, "user.update", "admin_user", user.id, changes)
    await db.commit()
    return {**auth.public_user(user), "is_active": user.is_active}


# ---------------------------------------------------------------- SEO report

@router.get("/seo/report")
async def seo_report(ctx: auth.AdminCtx = Depends(auth.require_staff), db: AsyncSession = Depends(get_session)):
    live = (A.is_published.is_(True), A.deleted_at.is_(None), A.review_status != "rejected")

    async def count(*conds) -> int:
        return (await db.execute(select(func.count()).select_from(A).where(*live, *conds))).scalar_one()

    pages = (await db.execute(select(func.count()).select_from(SitePage).where(SitePage.is_published.is_(True)))).scalar_one()
    total = await count()
    return {
        "indexable_articles": total,
        "published_pages": pages,
        "sitemap_urls": min(total, 45000) + pages + 1,
        "missing_image": await count(A.image_url.is_(None)),
        "missing_summary": await count(A.summary.is_(None)),
        "with_custom_meta": await count(A.meta_description.is_not(None)),
        "unpublished": (await db.execute(select(func.count()).select_from(A).where(
            A.is_published.is_(False), A.deleted_at.is_(None), A.content_issue.is_(None)))).scalar_one(),
        "held_back": (await db.execute(select(func.count()).select_from(A).where(
            A.is_published.is_(False), A.deleted_at.is_(None), A.content_issue.is_not(None)))).scalar_one(),
        "recent_24h": await count(A.published_at > datetime.now(timezone.utc) - timedelta(days=1)),
    }
