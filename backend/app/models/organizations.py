"""Organization models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class Organization(Base):
    """Organization model - represents a sub-division within a tenant"""
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(255))
    status = Column(String(50), default="active", index=True)

    # Settings (JSON)
    settings = Column(JSON, default={})
    metadata = Column(JSON, default={})

    # Org type/category
    org_type = Column(String(50), default="department")

    # Parent organization (for hierarchies)
    parent_id = Column(Integer, ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    tenant = relationship("Tenant", backref="organizations")
    members = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    settings_override = relationship("OrganizationSettings", back_populates="organization", cascade="all, delete-orphan")
    children = relationship("Organization", remote_side=[parent_id], backref="parent")

    __table_args__ = (
        Index("idx_tenant_slug", "tenant_id", "slug"),
        Index("idx_tenant_status", "tenant_id", "status"),
        Index("idx_parent", "parent_id"),
    )


class OrganizationMember(Base):
    """Organization member - user's membership in an organization"""
    __tablename__ = "organization_members"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), default="member", index=True)

    # Permissions (JSON) - override for this organization
    permissions = Column(JSON, default=[])

    # Status
    status = Column(String(50), default="active")
    is_lead = Column(Boolean, default=False, index=True)

    # Timestamps
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    invited_at = Column(DateTime(timezone=True), nullable=True)
    invited_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    left_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    organization = relationship("Organization", back_populates="members")
    user = relationship("User")

    __table_args__ = (
        Index("idx_org_user", "organization_id", "user_id"),
        Index("idx_org_status", "organization_id", "status"),
    )


class OrganizationSettings(Base):
    """Organization settings - configuration per organization"""
    __tablename__ = "organization_settings"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    key = Column(String(255), nullable=False)
    value = Column(JSON)
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    organization = relationship("Organization", back_populates="settings_override")

    __table_args__ = (
        Index("idx_org_key", "organization_id", "key"),
    )


class OrganizationInvitation(Base):
    """Organization invitation - pending user invitations"""
    __tablename__ = "organization_invitations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    role = Column(String(50), default="member")
    token = Column(String(255), unique=True, nullable=False, index=True)

    invited_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_org_email", "organization_id", "email"),
        Index("idx_token_expires", "token", "expires_at"),
    )
