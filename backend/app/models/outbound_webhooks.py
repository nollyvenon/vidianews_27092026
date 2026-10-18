"""Outbound webhooks: endpoints a user registers to receive signed event notifications."""

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class OutboundWebhook(Base):
    __tablename__ = "outbound_webhooks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    description = Column(String(255), nullable=True)
    events = Column(JSON, nullable=False, default=list)
    secret_encrypted = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    deliveries = relationship(
        "OutboundWebhookDelivery",
        back_populates="webhook",
        cascade="all, delete-orphan",
        order_by="OutboundWebhookDelivery.id.desc()",
    )


class OutboundWebhookDelivery(Base):
    __tablename__ = "outbound_webhook_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("outbound_webhooks.id", ondelete="CASCADE"), nullable=False, index=True)
    event = Column(String(100), nullable=False, index=True)
    payload = Column(JSON, nullable=False)
    status = Column(String(20), nullable=False, index=True)  # delivered | failed
    response_status = Column(Integer, nullable=True)
    error = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    webhook = relationship("OutboundWebhook", back_populates="deliveries")
