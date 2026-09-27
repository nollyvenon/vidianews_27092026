"""Multi-tenancy models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class Tenant(Base):
    """Tenant model - represents an isolated organization"""
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(255))
    status = Column(String(50), default="active", index=True)
    plan = Column(String(50), default="free")

    # Settings (JSON)
    settings = Column(JSON, default={})
    metadata = Column(JSON, default={})

    # Limits
    max_users = Column(Integer, default=10)
    max_storage_gb = Column(Integer, default=5)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    members = relationship("TenantMember", back_populates="tenant", cascade="all, delete-orphan")
    settings_override = relationship("TenantSettings", back_populates="tenant", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_slug", "slug"),
        Index("idx_status_created", "status", "created_at"),
    )


class TenantMember(Base):
    """Tenant member - user's membership in a tenant"""
    __tablename__ = "tenant_members"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), default="member", index=True)

    # Permissions (JSON) - override for this tenant
    permissions = Column(JSON, default=[])

    # Status
    status = Column(String(50), default="active")
    is_owner = Column(Boolean, default=False, index=True)

    # Timestamps
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    invited_at = Column(DateTime(timezone=True), nullable=True)
    invited_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    left_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    tenant = relationship("Tenant", back_populates="members")
    user = relationship("User")

    __table_args__ = (
        Index("idx_tenant_user", "tenant_id", "user_id"),
        Index("idx_tenant_status", "tenant_id", "status"),
    )


class TenantSettings(Base):
    """Tenant settings - configuration per tenant"""
    __tablename__ = "tenant_settings"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    key = Column(String(255), nullable=False)
    value = Column(JSON)
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    tenant = relationship("Tenant", back_populates="settings_override")

    __table_args__ = (
        Index("idx_tenant_key", "tenant_id", "key"),
    )


class TenantInvitation(Base):
    """Tenant invitation - pending user invitations"""
    __tablename__ = "tenant_invitations"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    role = Column(String(50), default="member")
    token = Column(String(255), unique=True, nullable=False, index=True)

    invited_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_tenant_email", "tenant_id", "email"),
        Index("idx_token_expires", "token", "expires_at"),
    )
