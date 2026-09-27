"""AI Provider integration models"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class ProviderType(str, enum.Enum):
    """AI Provider types"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LLAMA = "llama"
    LOCAL = "local"
    MISTRAL = "mistral"
    COHERE = "cohere"


class ModelFamily(str, enum.Enum):
    """Model families"""
    GPT = "gpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    LLAMA = "llama"
    MISTRAL = "mistral"
    COMMAND = "command"


class APIKeyStatus(str, enum.Enum):
    """API key status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    REVOKED = "revoked"
    EXPIRED = "expired"


class AIProvider(Base):
    """AI Provider configuration"""
    __tablename__ = "ai_providers"

    id = Column(Integer, primary_key=True, index=True)

    # Provider info
    name = Column(String(255), nullable=False, unique=True, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    provider_type = Column(SQLEnum(ProviderType), nullable=False, index=True)
    description = Column(Text)

    # Provider configuration
    api_url = Column(String(500), nullable=False)
    api_version = Column(String(100))

    # Rate limits
    requests_per_minute = Column(Integer, default=60)
    requests_per_day = Column(Integer, default=10000)
    max_tokens_per_request = Column(Integer)

    # Capabilities
    supports_streaming = Column(Boolean, default=False)
    supports_function_calling = Column(Boolean, default=False)
    supports_vision = Column(Boolean, default=False)
    supports_audio = Column(Boolean, default=False)

    # Status and metadata
    is_active = Column(Boolean, default=True, index=True)
    is_public = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # For load balancing

    # Usage tracking
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_provider_type", "provider_type"),
        Index("idx_provider_active", "is_active"),
        Index("idx_provider_slug", "slug"),
    )

    # Relationships
    api_keys = relationship("AIProviderAPIKey", back_populates="provider", cascade="all, delete-orphan")
    models = relationship("AIModel", back_populates="provider", cascade="all, delete-orphan")
    usage = relationship("ProviderUsage", back_populates="provider", cascade="all, delete-orphan")


class AIProviderAPIKey(Base):
    """API keys for AI providers"""
    __tablename__ = "ai_provider_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("ai_providers.id", ondelete="CASCADE"), nullable=False, index=True)

    # Key information (encrypted in production)
    key_name = Column(String(255), nullable=False)
    key_value = Column(String(500), nullable=False)  # Should be encrypted

    # Organization
    organization_id = Column(Integer, nullable=True)

    # Status
    status = Column(SQLEnum(APIKeyStatus), default=APIKeyStatus.ACTIVE, index=True)
    is_primary = Column(Boolean, default=False)

    # Rate limiting
    current_requests_today = Column(Integer, default=0)
    last_request_at = Column(DateTime(timezone=True))

    # Metadata
    extra_config = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_api_key_provider", "provider_id"),
        Index("idx_api_key_status", "status"),
    )

    # Relationships
    provider = relationship("AIProvider", back_populates="api_keys")


class AIModel(Base):
    """AI Models available through providers"""
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("ai_providers.id", ondelete="CASCADE"), nullable=False, index=True)

    # Model info
    name = Column(String(255), nullable=False, index=True)
    model_id = Column(String(255), nullable=False)  # Provider's model ID
    family = Column(SQLEnum(ModelFamily), nullable=False, index=True)
    version = Column(String(100))
    description = Column(Text)

    # Capabilities
    context_window = Column(Integer)  # Max tokens
    supports_vision = Column(Boolean, default=False)
    supports_audio = Column(Boolean, default=False)
    supports_streaming = Column(Boolean, default=False)
    supports_function_calling = Column(Boolean, default=False)

    # Pricing (per 1k tokens)
    input_cost = Column(Float, default=0.0)
    output_cost = Column(Float, default=0.0)

    # Status
    is_available = Column(Boolean, default=True, index=True)
    is_deprecated = Column(Boolean, default=False)
    deprecation_date = Column(DateTime(timezone=True), nullable=True)

    # Usage
    total_calls = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Metadata
    extra_config = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_model_provider", "provider_id"),
        Index("idx_model_available", "is_available"),
        Index("idx_model_family", "family"),
    )

    # Relationships
    provider = relationship("AIProvider", back_populates="models")
    calls = relationship("AIModelCall", back_populates="model", cascade="all, delete-orphan")


class AIModelCall(Base):
    """Calls/usage tracking for AI models"""
    __tablename__ = "ai_model_calls"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Request info
    request_tokens = Column(Integer, nullable=False)
    response_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)

    # Cost
    input_cost = Column(Float, default=0.0)
    output_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)

    # Status
    status = Column(String(50), default="success")  # success, error, timeout
    error_message = Column(Text, nullable=True)

    # Duration
    duration_ms = Column(Integer)  # How long the call took

    # Metadata
    request_id = Column(String(100), index=True)
    extra_data = Column(JSON, default={})

    # Timestamp
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    __table_args__ = (
        Index("idx_call_model", "model_id"),
        Index("idx_call_user", "user_id"),
        Index("idx_call_created", "created_at"),
    )

    # Relationships
    model = relationship("AIModel", back_populates="calls")
    user = relationship("User", backref="ai_model_calls")


class ProviderUsage(Base):
    """Daily usage tracking per provider"""
    __tablename__ = "provider_usage"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("ai_providers.id", ondelete="CASCADE"), nullable=False, index=True)

    # Date
    usage_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Usage metrics
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)

    # Success/Error rates
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)

    # Performance
    avg_latency_ms = Column(Float, default=0.0)
    min_latency_ms = Column(Float, default=0.0)
    max_latency_ms = Column(Float, default=0.0)

    # Rate limiting
    rate_limited_requests = Column(Integer, default=0)

    # Timestamp
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_usage_provider", "provider_id"),
        Index("idx_usage_date", "usage_date"),
    )

    # Relationships
    provider = relationship("AIProvider", back_populates="usage")
