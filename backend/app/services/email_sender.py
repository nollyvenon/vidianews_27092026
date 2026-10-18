"""Outgoing email delivery.

Mail is sent through the SMTP server named by ``SMTP_HOST``. When no SMTP server is configured
nothing is sent; the message is written to the server log at WARNING level so a developer can
complete the flow locally. Production deployments must configure SMTP.
"""

import asyncio
import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


def _deliver(message: EmailMessage) -> None:
    """Blocking SMTP delivery; run in a worker thread."""
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as smtp:
        if settings.SMTP_STARTTLS:
            smtp.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(message)


async def send_email(to: str, subject: str, body: str) -> bool:
    """Send a plain-text email.

    Returns True when the message was handed to the SMTP server, False when SMTP is not
    configured (the message is logged instead). SMTP failures raise to the caller.
    """
    if not settings.SMTP_HOST:
        logger.warning("SMTP is not configured; not sending %r to %s. Body:\n%s", subject, to, body)
        return False

    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    await asyncio.to_thread(_deliver, message)
    return True


async def send_verification_email(to: str, verification_url: str) -> bool:
    """Send the account confirmation link."""
    body = (
        "Welcome to AetherCMS AI.\n\n"
        "Confirm your email address to activate your account:\n"
        f"{verification_url}\n\n"
        "If you did not create this account, you can ignore this message."
    )
    return await send_email(to, "Confirm your AetherCMS AI account", body)


async def send_password_reset_email(to: str, reset_url: str) -> bool:
    """Send the link that starts a password reset. The link expires after one hour."""
    body = (
        "A password reset was requested for your AetherCMS AI account.\n\n"
        "Choose a new password using this link (valid for one hour):\n"
        f"{reset_url}\n\n"
        "If you did not request a reset, you can ignore this message; your password is unchanged."
    )
    return await send_email(to, "Reset your AetherCMS AI password", body)


def reset_url_for(token: str, base: Optional[str] = None) -> str:
    """Build the public link that opens the password reset form."""
    origin = (base or settings.FRONTEND_URL).rstrip("/")
    return f"{origin}/auth/reset-password?token={token}"


def verification_url_for(token: str, base: Optional[str] = None) -> str:
    """Build the public link that completes email verification."""
    origin = (base or settings.FRONTEND_URL).rstrip("/")
    return f"{origin}/auth/verify-email?token={token}"
