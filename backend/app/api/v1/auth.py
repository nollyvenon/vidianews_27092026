"""Authentication endpoints"""

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.auth import *
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.security import decode_token, verify_token_not_expired
from app.utils.exceptions import UnauthorizedError, ValidationError
from app.utils.logger import logger

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, session: AsyncSession = Depends(get_session)):
    """Register new user"""
    if request.password != request.password_confirm:
        raise ValidationError("Passwords do not match")

    try:
        auth_service = AuthService(session)
        user, verification_token = await auth_service.register_user(
            request.email,
            request.password,
            request.first_name,
            request.last_name,
        )

        # Log registration
        logger.info(f"User registered: {user.email}")

        # Auto-login after registration
        access_token, refresh_token, _ = await auth_service.login_user(
            request.email,
            request.password,
            "0.0.0.0",
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    http_request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Login user"""
    ip_address = http_request.client.host if http_request.client else "unknown"

    try:
        auth_service = AuthService(session)
        access_token, refresh_token, user = await auth_service.login_user(
            request.email,
            request.password,
            ip_address,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmailRequest,
    session: AsyncSession = Depends(get_session),
):
    """Verify email with token"""
    try:
        auth_service = AuthService(session)
        user = await auth_service.verify_email(request.token)

        return {
            "message": "Email verified successfully",
            "user": UserResponse.from_orm(user),
        }
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        raise


@router.post("/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    session: AsyncSession = Depends(get_session),
):
    """Request password reset"""
    try:
        auth_service = AuthService(session)
        token = await auth_service.request_password_reset(request.email)

        # TODO: Send email with reset link
        # In production: send token to user's email

        return {
            "message": "If email exists, password reset link has been sent",
        }
    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}")
        raise


@router.post("/reset-password")
async def reset_password(
    request: PasswordResetConfirmRequest,
    session: AsyncSession = Depends(get_session),
):
    """Reset password with token"""
    if request.new_password != request.password_confirm:
        raise ValidationError("Passwords do not match")

    try:
        auth_service = AuthService(session)
        user = await auth_service.reset_password(request.token, request.new_password)

        return {
            "message": "Password reset successfully",
            "user": UserResponse.from_orm(user),
        }
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise


@router.post("/logout")
async def logout(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    """Logout user"""
    if not authorization:
        raise UnauthorizedError("Missing authorization header")

    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)

        if not payload:
            raise UnauthorizedError("Invalid token")

        user_id = payload.get("user_id")
        auth_service = AuthService(session)
        await auth_service.logout_user(token, user_id)

        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    """Get current authenticated user"""
    if not authorization:
        raise UnauthorizedError("Missing authorization header")

    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)

        if not payload:
            raise UnauthorizedError("Invalid token")

        if not verify_token_not_expired(token):
            raise UnauthorizedError("Token expired")

        user_id = payload.get("user_id")
        if not user_id:
            raise UnauthorizedError("Invalid token")

        auth_service = AuthService(session)
        if await auth_service.is_token_blacklisted(token):
            raise UnauthorizedError("Token revoked")

        user = await session.get(User, user_id)
        if not user:
            raise UnauthorizedError("User not found")

        return UserResponse.from_orm(user)
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    """Refresh access token"""
    if not authorization:
        raise UnauthorizedError("Missing authorization header")

    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)

        if not payload:
            raise UnauthorizedError("Invalid token")

        user_id = payload.get("user_id")
        email = payload.get("sub")

        if not user_id or not email:
            raise UnauthorizedError("Invalid token")

        auth_service = AuthService(session)
        if await auth_service.is_token_blacklisted(token):
            raise UnauthorizedError("Token revoked")

        user = await session.get(User, user_id)
        if not user:
            raise UnauthorizedError("User not found")

        # Generate new tokens
        from app.core.security import create_access_token, create_refresh_token
        new_access_token = create_access_token({"sub": user.email, "user_id": user.id})
        new_refresh_token = create_refresh_token({"sub": user.email, "user_id": user.id})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise
