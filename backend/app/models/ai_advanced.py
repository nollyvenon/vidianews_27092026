"""Advanced AI models: Memory, Templates, Chat, Research, Monitoring, Safety"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class MemoryType(str, enum.Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class ChatStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class DocumentType(str, enum.Enum):
    TEXT = "text"
    PDF = "pdf"
    WEBPAGE = "webpage"
    CODE = "code"
    MARKDOWN = "markdown"


class MonitoringMetric(str, enum.Enum):
    TOKENS = "tokens"
    COST = "cost"
    LATENCY = "latency"
    SUCCESS_RATE = "success_rate"


class SafetyLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Module 15: Memory
class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    memory_type = Column(SQLEnum(MemoryType), nullable=False, index=True)
    key = Column(String(255), nullable=False, unique=True, index=True)
    value = Column(JSON, nullable=False)
    embeddings = Column(JSON, default=[])
    relevance_score = Column(Float, default=1.0)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    agent = relationship("Agent")


class ConversationMemory(Base):
    __tablename__ = "conversation_memories"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("agent_conversations.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text)
    key_points = Column(JSON, default=[])
    context_window = Column(Integer, default=4096)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# Module 16: Templates
class AITemplate(Base):
    __tablename__ = "ai_templates"
    id = Column(Integer, primary_key=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    template_type = Column(String(100), index=True)
    definition = Column(JSON, nullable=False)
    parameters = Column(JSON, default={})
    category = Column(String(100), index=True)
    is_public = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    creator = relationship("User", backref="templates")


# Module 17: Chat
class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255))
    messages = Column(JSON, default=[])
    status = Column(SQLEnum(ChatStatus), default=ChatStatus.ACTIVE, index=True)
    model_id = Column(Integer, nullable=True)
    system_prompt = Column(Text)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="chats")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chat = relationship("Chat", backref="messages")


# Module 18: Research/RAG
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    document_type = Column(SQLEnum(DocumentType), nullable=False, index=True)
    source_url = Column(String(500), nullable=True)
    embeddings = Column(JSON, default=[])
    chunks = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    is_indexed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="documents")


class ResearchQuery(Base):
    __tablename__ = "research_queries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    query = Column(Text, nullable=False)
    results = Column(JSON, default=[])
    sources = Column(JSON, default=[])
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="research_queries")


# Module 19: Monitoring
class UsageMetric(Base):
    __tablename__ = "usage_metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    model_id = Column(Integer, nullable=True)
    metric_type = Column(SQLEnum(MonitoringMetric), nullable=False, index=True)
    value = Column(Float, nullable=False)
    tags = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", backref="metrics")


class CostAlert(Base):
    __tablename__ = "cost_alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    threshold = Column(Float, nullable=False)
    period = Column(String(50))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="cost_alerts")


# Module 20: Safety
class SafetyCheck(Base):
    __tablename__ = "safety_checks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    severity = Column(SQLEnum(SafetyLevel), nullable=False, index=True)
    flags = Column(JSON, default=[])
    is_approved = Column(Boolean, default=False, index=True)
    review_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ComplianceLog(Base):
    __tablename__ = "compliance_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    resource = Column(String(255))
    status = Column(String(50), default="success")
    details = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", backref="compliance_logs")
