"""Authentication service"""
from typing import Optional

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.models.auth import EmailVerification, PasswordReset, TokenBlacklist, LoginAttempt
from app.services.mfa_service import verify_code
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.utils.exceptions import UnauthorizedError, ConflictError, NotFoundError, RateLimitError
from app.utils.logger import logger
import secrets
import hashlib


class AuthService:
    """Authentication service"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> User:
        """Register new user"""
        stmt = select(User).where(User.email == email)
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise ConflictError("Email already registered")

        user = User(
            email=email,
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            status="inactive",
        )
        self.session.add(user)
        await self.session.flush()

        verification_token = await self.create_email_verification(user.id, email)
        await self.session.commit()

        logger.info(f"User registered: {email}")
        return user, verification_token

    async def provision_personal_workspace(self, user: User) -> None:
        """Give a new account its own tenant and organization, with the user as owner.

        Organization-scoped features (content quality checks, brand guides) need a membership,
        so every account starts with one. The user can add more organizations later.
        """
        from app.services.tenant_service import TenantService
        from app.services.organization_service import OrganizationService

        display_name = " ".join(part for part in (user.first_name, user.last_name) if part) or user.email.split("@")[0]
        tenant = await TenantService(self.session).create_tenant(
            name=f"{display_name} workspace",
            slug=f"workspace-{user.id}",
            user_id=user.id,
        )
        await OrganizationService(self.session).create_organization(
            tenant_id=tenant.id,
            name=f"{display_name} team",
            slug=f"team-{user.id}",
            user_id=user.id,
        )

    async def activate_user(self, user_id: int) -> None:
        """Mark an account as active and email-verified (used when verification is disabled)."""
        user = await self.session.get(User, user_id)
        if user is None:
            raise NotFoundError("User")
        user.status = "active"
        user.email_verified_at = datetime.now(timezone.utc)
        await self.session.commit()

    async def login_user(
        self,
        email: str,
        password: str,
        ip_address: str,
        otp_code: Optional[str] = None,
    ) -> tuple:
        """Login user with email and password, plus a one-time code when two-factor authentication is on"""
        attempt = LoginAttempt(email=email, ip_address=ip_address, success=False)
        self.session.add(attempt)
        await self.session.flush()

        # Check rate limit (5 failed attempts per minute)
        one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)
        stmt = select(func.count(LoginAttempt.id)).where(
            LoginAttempt.email == email,
            LoginAttempt.success == False,
            LoginAttempt.created_at > one_minute_ago,
        )
        failed_attempts = (await self.session.execute(stmt)).scalar()
        if failed_attempts >= 5:
            await self.session.commit()
            raise RateLimitError("Too many failed login attempts. Try again in 1 minute.")

        stmt = select(User).where(User.email == email)
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        if not user:
            await self.session.commit()
            logger.warning(f"Login failed: user not found ({email})")
            raise UnauthorizedError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            await self.session.commit()
            logger.warning(f"Login failed: invalid password ({email})")
            raise UnauthorizedError("Invalid credentials")

        if user.status == "inactive":
            await self.session.commit()
            logger.warning(f"Login failed: account inactive ({email})")
            raise UnauthorizedError("Email not verified")

        if user.status != "active":
            await self.session.commit()
            logger.warning(f"Login failed: account not active ({email})")
            raise UnauthorizedError("Account inactive")

        if user.mfa_enabled:
            if not otp_code:
                await self.session.commit()
                raise UnauthorizedError("MFA code required")
            if not verify_code(user.mfa_secret, otp_code):
                await self.session.commit()
                logger.warning(f"Login failed: invalid MFA code ({email})")
                raise UnauthorizedError("Invalid authentication code")

        attempt.success = True
        user.last_login_at = datetime.now(timezone.utc)
        await self.session.commit()

        access_token = create_access_token({"sub": user.email, "user_id": user.id})
        refresh_token = create_refresh_token({"sub": user.email, "user_id": user.id})

        logger.info(f"User logged in: {email}")
        return access_token, refresh_token, user

    async def verify_email(self, token: str) -> User:
        """Verify email with token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        stmt = select(EmailVerification).where(
            EmailVerification.token_hash == token_hash
        )
        verification = (await self.session.execute(stmt)).scalar_one_or_none()
        if not verification:
            logger.warning("Email verification failed: invalid token")
            raise NotFoundError("Verification token")

        if verification.expires_at < datetime.now(timezone.utc):
            logger.warning("Email verification failed: token expired")
            raise UnauthorizedError("Verification token expired")

        if verification.verified_at:
            raise ConflictError("Email already verified")

        verification.verified_at = datetime.now(timezone.utc)
        user = await self.session.get(User, verification.user_id)
        user.status = "active"
        user.email_verified_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Email verified: {user.email}")
        return user

    async def create_email_verification(self, user_id: int, email: str) -> str:
        """Create email verification token"""
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        stmt = select(EmailVerification).where(
            EmailVerification.user_id == user_id
        )
        old = (await self.session.execute(stmt)).scalar_one_or_none()
        if old:
            await self.session.delete(old)

        verification = EmailVerification(
            user_id=user_id,
            email=email,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
        )
        self.session.add(verification)
        return token

    async def request_password_reset(self, email: str) -> str:
        """Request password reset"""
        stmt = select(User).where(User.email == email)
        user = (await self.session.execute(stmt)).scalar_one_or_none()

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        if user:
            reset = PasswordReset(
                user_id=user.id,
                token_hash=token_hash,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            )
            self.session.add(reset)
            await self.session.commit()
            logger.info(f"Password reset requested: {email}")
            return token

        logger.warning(f"Password reset requested for non-existent user: {email}")
        return None

    async def reset_password(self, token: str, new_password: str) -> User:
        """Reset password with token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        stmt = select(PasswordReset).where(
            PasswordReset.token_hash == token_hash
        )
        reset = (await self.session.execute(stmt)).scalar_one_or_none()
        if not reset:
            logger.warning("Password reset failed: invalid token")
            raise NotFoundError("Reset token")

        if reset.expires_at < datetime.now(timezone.utc):
            logger.warning("Password reset failed: token expired")
            raise UnauthorizedError("Reset token expired")

        if reset.used_at:
            logger.warning("Password reset failed: token already used")
            raise ConflictError("Token already used")

        user = await self.session.get(User, reset.user_id)
        user.password_hash = hash_password(new_password)
        user.password_changed_at = datetime.now(timezone.utc)

        reset.used_at = datetime.now(timezone.utc)
        await self.session.commit()

        logger.info(f"Password reset: {user.email}")
        return user

    async def logout_user(self, token: str, user_id: int = None):
        """Logout user by blacklisting token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        blacklist = TokenBlacklist(
            token_hash=token_hash,
            user_id=user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        self.session.add(blacklist)
        await self.session.commit()

        logger.info(f"User logged out: user_id={user_id}")

    async def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        stmt = select(TokenBlacklist).where(
            TokenBlacklist.token_hash == token_hash
        )
        return bool((await self.session.execute(stmt)).scalar_one_or_none())
