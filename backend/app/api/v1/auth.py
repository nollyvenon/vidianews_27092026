"""Authentication endpoints"""

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.auth import *
from app.services.auth_service import AuthService
from app.services.mfa_service import generate_secret, provisioning_uri, verify_code
from app.services.email_sender import send_password_reset_email, reset_url_for, send_verification_email, verification_url_for
from app.core.config import settings
from app.models.user import User
from app.core.security import decode_token, get_current_user, verify_token_not_expired
from app.utils.exceptions import ConflictError, UnauthorizedError, ValidationError
from app.utils.logger import logger

router = APIRouter()


@router.post("/register", status_code=201, response_model=RegisterResponse)
async def register(request: RegisterRequest, session: AsyncSession = Depends(get_session)):
    """Register a new user.

    With verification required (the default) the account stays inactive and a confirmation
    link is emailed; the caller must confirm it before signing in. With verification disabled
    the account is activated and a session is returned immediately.
    """
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
        logger.info(f"User registered: {user.email}")
        await auth_service.provision_personal_workspace(user)

        if settings.EMAIL_VERIFICATION_REQUIRED:
            await send_verification_email(user.email, verification_url_for(verification_token))
            return RegisterResponse(
                requires_verification=True,
                message="Check your email to confirm your account before signing in.",
            )

        await auth_service.activate_user(user.id)
        access_token, refresh_token, _ = await auth_service.login_user(
            request.email,
            request.password,
            "0.0.0.0",
        )
        return RegisterResponse(
            requires_verification=False,
            message="Account created.",
            access_token=access_token,
            refresh_token=refresh_token,
        )
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
            request.otp_code,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise


class MfaCodeRequest(BaseModel):
    code: str = Field(..., pattern=r"^\d{6}$")


async def _signed_in_user(session: AsyncSession, current_user: User) -> User:
    user = await session.get(User, current_user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/mfa")
async def mfa_status(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Whether two-factor authentication is on for the signed-in user"""
    user = await _signed_in_user(session, current_user)
    return {"enabled": bool(user.mfa_enabled)}


@router.post("/mfa/setup")
async def mfa_setup(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new authenticator secret. It becomes active only after a correct code is confirmed."""
    user = await _signed_in_user(session, current_user)
    if user.mfa_enabled:
        raise ConflictError("Two-factor authentication is already enabled")
    user.mfa_secret = generate_secret()
    await session.commit()
    return {"secret": user.mfa_secret, "otpauth_uri": provisioning_uri(user.mfa_secret, user.email)}


@router.post("/mfa/enable")
async def mfa_enable(
    request: MfaCodeRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Turn two-factor authentication on after confirming a code from the authenticator app"""
    user = await _signed_in_user(session, current_user)
    if user.mfa_enabled:
        raise ConflictError("Two-factor authentication is already enabled")
    if not user.mfa_secret:
        raise ValidationError("Start the setup before confirming a code")
    if not verify_code(user.mfa_secret, request.code):
        raise ValidationError("Invalid authentication code")
    user.mfa_enabled = True
    await session.commit()
    return {"enabled": True}


@router.post("/mfa/disable")
async def mfa_disable(
    request: MfaCodeRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Turn two-factor authentication off; a current code is required"""
    user = await _signed_in_user(session, current_user)
    if not user.mfa_enabled:
        raise ConflictError("Two-factor authentication is not enabled")
    if not verify_code(user.mfa_secret, request.code):
        raise ValidationError("Invalid authentication code")
    user.mfa_enabled = False
    user.mfa_secret = None
    await session.commit()
    return {"enabled": False}


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
        if token is not None:
            # Only accounts that exist receive a link; the response is the same either way.
            await send_password_reset_email(request.email, reset_url_for(token))

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
