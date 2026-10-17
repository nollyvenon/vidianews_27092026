"""Social login provider configuration, managed by administrators."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class SocialLoginProvider(Base):
    """OAuth client credentials for one external identity provider.

    ``client_secret_encrypted`` holds a Fernet ciphertext; the plaintext secret is
    never returned by the API and is only decrypted server-side during a token exchange.
    """

    __tablename__ = "social_login_providers"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), unique=True, nullable=False, index=True)
    enabled = Column(Boolean, nullable=False, default=False)
    client_id = Column(String(255))
    client_secret_encrypted = Column(Text)
    redirect_uri = Column(String(500))
    scopes = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    updated_by = relationship("User", foreign_keys=[updated_by_user_id])


class SocialLoginHandoff(Base):
    """One pending or completed mobile sign-in.

    Created when the app starts a sign-in with a ticket, filled with encrypted tokens when the
    browser step completes, and deleted when the app claims them. Keyed by a hash of the ticket,
    so a leaked OAuth state cannot be used to claim tokens without the ticket itself.
    """

    __tablename__ = "social_login_handoffs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_hash = Column(String(64), unique=True, nullable=False, index=True)
    payload_encrypted = Column(Text, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
