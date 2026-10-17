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
