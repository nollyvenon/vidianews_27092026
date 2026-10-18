"""Security utilities: JWT, password hashing, permissions"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import AuthenticationError
from app.core.config import settings
from app.db.session import get_db

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except (JWTError, ValidationError):
        return None


def verify_token_not_expired(token: str) -> bool:
    """Verify that a token has not expired"""
    payload = decode_token(token)
    if not payload:
        return False

    exp = payload.get("exp")
    if not exp:
        return False

    return datetime.now(timezone.utc) < datetime.fromtimestamp(exp, tz=timezone.utc)


# auto_error=False lets get_current_user answer a missing header with 401, not HTTPBearer's 403.
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials = Depends(security),
    session: AsyncSession = Depends(get_db),
):
    """Get current authenticated user from JWT token"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    email = payload.get("sub")

    if not email or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from app.models.user import User

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await attach_memberships(session, user)
    return user


async def attach_memberships(session: AsyncSession, user) -> None:
    """Attach the user's organization_id and tenant_id for this request.

    Routers scope data by these values. They come from membership rows, because the User row
    holds neither. Both are None when the user belongs to no organization or tenant.
    """
    from sqlalchemy import select
    from app.models.organizations import Organization, OrganizationMember
    from app.models.tenants import TenantMember

    membership = (
        await session.execute(
            select(OrganizationMember)
            .where(OrganizationMember.user_id == user.id, OrganizationMember.status == "active")
            .order_by(OrganizationMember.id)
        )
    ).scalars().first()

    organization_id = membership.organization_id if membership else None
    tenant_id = None
    if membership:
        organization = await session.get(Organization, membership.organization_id)
        tenant_id = organization.tenant_id if organization else None
    if tenant_id is None:
        tenant_membership = (
            await session.execute(
                select(TenantMember)
                .where(TenantMember.user_id == user.id, TenantMember.status == "active")
                .order_by(TenantMember.id)
            )
        ).scalars().first()
        tenant_id = tenant_membership.tenant_id if tenant_membership else None

    user.organization_id = organization_id
    user.tenant_id = tenant_id


async def get_optional_current_user(
    credentials = Depends(security),
    session: AsyncSession = Depends(get_db),
):
    """Like get_current_user, but anonymous requests (no token) get None instead of 401."""
    if credentials is None:
        return None
    return await get_current_user(credentials, session)
