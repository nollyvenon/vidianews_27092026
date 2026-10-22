"""Admin authentication: password rules, server-side sessions, CSRF, roles, throttling.

The session cookie is a random 256-bit value; only its SHA-256 is stored, so a
database leak does not hand out live sessions. Every state-changing request must
also carry the session's CSRF token in `X-CSRF-Token`.
"""

import asyncio
import hashlib
import hmac
import re
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.db.session import AsyncSessionLocal, get_session
from app.models.site import AdminLoginAttempt, AdminSession, AdminUser, AuditLog
from app.services.news.geo import client_ip

COOKIE_NAME = "admin_session"
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
ROLES = ("admin", "editor")
MAX_EMAIL_FAILURES = 5
MAX_IP_FAILURES = 20
LOCKOUT_WINDOW = timedelta(minutes=15)
_EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,255}\.[^@\s]{2,}$")
# Verified against when the account does not exist, so response time does not reveal valid emails.
_DUMMY_HASH = hash_password(secrets.token_urlsafe(16))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def ip_fingerprint(request: Request) -> str:
    """Short keyed hash of the client IP: enough to throttle and audit, not to identify."""
    ip = client_ip(request) or "unknown"
    return hmac.new(settings.SECRET_KEY.encode(), ip.encode(), hashlib.sha256).hexdigest()[:16]


def normalize_email(email: str) -> str:
    email = (email or "").strip().lower()
    if not _EMAIL.match(email):
        raise HTTPException(status_code=422, detail="Enter a valid email address")
    return email


def check_password_policy(password: str, email: str = "") -> None:
    problems = []
    if len(password) < 12:
        problems.append("at least 12 characters")
    if len(password.encode()) > 72:
        problems.append("no more than 72 bytes")
    if not re.search(r"[A-Za-z]", password) or not re.search(r"[^A-Za-z]", password):
        problems.append("letters and at least one number or symbol")
    if email and password.lower() == email.lower():
        problems.append("must differ from the email address")
    if problems:
        raise HTTPException(status_code=422, detail="Password needs: " + ", ".join(problems))


async def _hash(password: str) -> str:
    return await asyncio.to_thread(hash_password, password)


async def _verify(password: str, hashed: str) -> bool:
    try:
        return await asyncio.to_thread(verify_password, password, hashed)
    except ValueError:
        return False


async def create_admin(db: AsyncSession, email: str, password: str, role: str = "admin", name: Optional[str] = None) -> AdminUser:
    email = normalize_email(email)
    if role not in ROLES:
        raise HTTPException(status_code=422, detail=f"role must be one of {ROLES}")
    check_password_policy(password, email)
    if (await db.execute(select(AdminUser.id).where(AdminUser.email == email))).first():
        raise HTTPException(status_code=409, detail="An admin with this email already exists")
    user = AdminUser(email=email, name=(name or "").strip()[:120] or None, role=role,
                     password_hash=await _hash(password))
    db.add(user)
    await db.flush()
    return user


async def bootstrap_admin() -> None:
    """First run only: create the admin named in ADMIN_EMAIL / ADMIN_PASSWORD, if there is none."""
    if not (settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD):
        return
    async with AsyncSessionLocal() as db:
        if (await db.execute(select(func.count()).select_from(AdminUser))).scalar_one():
            return
        await create_admin(db, settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD, "admin", "Administrator")
        await db.commit()


def cookie_secure(request: Request) -> bool:
    if settings.ADMIN_COOKIE_SECURE is not None:
        return settings.ADMIN_COOKIE_SECURE
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    return settings.APP_ENV.lower() == "production" or proto == "https"


def public_user(u: AdminUser) -> dict:
    return {"id": u.id, "email": u.email, "name": u.name, "role": u.role,
            "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None}


async def login(db: AsyncSession, request: Request, response: Response, email: str, password: str) -> dict:
    email = (email or "").strip().lower()
    fp = ip_fingerprint(request)
    since = _now() - LOCKOUT_WINDOW

    def failures(*cond):
        return select(func.count()).select_from(AdminLoginAttempt).where(
            AdminLoginAttempt.success.is_(False), AdminLoginAttempt.at > since, *cond)

    if ((await db.execute(failures(AdminLoginAttempt.email == email))).scalar_one() >= MAX_EMAIL_FAILURES
            or (await db.execute(failures(AdminLoginAttempt.ip_hash == fp))).scalar_one() >= MAX_IP_FAILURES):
        raise HTTPException(status_code=429, detail="Too many failed sign-in attempts. Try again in 15 minutes.",
                            headers={"Retry-After": "900"})

    user = (await db.execute(select(AdminUser).where(AdminUser.email == email))).scalar_one_or_none()
    ok = await _verify(password or "", user.password_hash if user else _DUMMY_HASH)
    ok = bool(ok and user and user.is_active)
    db.add(AdminLoginAttempt(email=email[:255], ip_hash=fp, success=ok))
    if not ok:
        await db.commit()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    now = _now()
    db.add(AdminSession(
        token_hash=hash_token(token), csrf_token=csrf, admin_id=user.id, ip_hash=fp,
        user_agent=(request.headers.get("user-agent") or "")[:200],
        expires_at=now + timedelta(hours=settings.ADMIN_SESSION_HOURS),
    ))
    user.last_login_at = now
    db.add(AuditLog(admin_id=user.id, admin_email=user.email, action="auth.login", detail={"ip": fp}))
    await db.commit()
    response.set_cookie(
        COOKIE_NAME, token, max_age=settings.ADMIN_SESSION_HOURS * 3600, httponly=True,
        samesite="lax", secure=cookie_secure(request), path="/",
    )
    return {"user": public_user(user), "csrf_token": csrf}


@dataclass
class AdminCtx:
    user: AdminUser
    session: AdminSession
    ip_hash: str

    @property
    def email(self) -> str:
        return self.user.email


def _origin_allowed(request: Request) -> bool:
    origin = request.headers.get("origin")
    if not origin:
        return True  # non-browser client; the CSRF token is still required
    allowed = {o.rstrip("/") for o in settings.CORS_ORIGINS} | {settings.SITE_URL.rstrip("/")}
    return origin.rstrip("/") in allowed


def admin_required(role: Optional[str] = None):
    """Dependency: valid session, active account, CSRF on writes, and (optionally) a role."""

    async def dependency(request: Request, db: AsyncSession = Depends(get_session)) -> AdminCtx:
        token = request.cookies.get(COOKIE_NAME)
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        sess = (await db.execute(
            select(AdminSession).where(AdminSession.token_hash == hash_token(token))
        )).scalar_one_or_none()
        now = _now()
        if (not sess or sess.revoked_at or sess.expires_at <= now
                or now - sess.last_seen_at > timedelta(minutes=settings.ADMIN_IDLE_MINUTES)):
            raise HTTPException(status_code=401, detail="Session expired")
        user = await db.get(AdminUser, sess.admin_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Account disabled")
        if request.method not in SAFE_METHODS:
            sent = request.headers.get("x-csrf-token", "")
            if not _origin_allowed(request) or not hmac.compare_digest(sent, sess.csrf_token):
                raise HTTPException(status_code=403, detail="CSRF check failed")
        if role and user.role != role:
            raise HTTPException(status_code=403, detail=f"{role} role required")
        if now - sess.last_seen_at > timedelta(seconds=60):
            sess.last_seen_at = now
            await db.commit()
        return AdminCtx(user=user, session=sess, ip_hash=ip_fingerprint(request))

    return dependency


require_staff = admin_required()  # admin or editor
require_admin = admin_required("admin")


async def revoke_session(db: AsyncSession, sess: AdminSession) -> None:
    sess.revoked_at = _now()
    await db.commit()


async def change_password(db: AsyncSession, ctx: AdminCtx, current: str, new: str) -> None:
    if not await _verify(current or "", ctx.user.password_hash):
        raise HTTPException(status_code=403, detail="Current password is incorrect")
    check_password_policy(new, ctx.user.email)
    ctx.user.password_hash = await _hash(new)
    ctx.user.password_changed_at = _now()
    await db.execute(update(AdminSession).where(
        AdminSession.admin_id == ctx.user.id, AdminSession.id != ctx.session.id, AdminSession.revoked_at.is_(None)
    ).values(revoked_at=_now()))
    db.add(AuditLog(admin_id=ctx.user.id, admin_email=ctx.user.email, action="auth.password_change"))
    await db.commit()


def audit(db: AsyncSession, ctx: AdminCtx, action: str, entity_type: str = "", entity_id="", detail: Optional[dict] = None) -> None:
    """Queue an audit row on the caller's transaction."""
    db.add(AuditLog(admin_id=ctx.user.id, admin_email=ctx.user.email, action=action,
                    entity_type=entity_type or None, entity_id=str(entity_id) if entity_id != "" else None,
                    detail=detail or {}))
