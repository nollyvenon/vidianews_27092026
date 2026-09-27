"""AI Core models: Prompts, Workflows, and Agents"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
import enum


class PromptStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class WorkflowStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class AgentStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class Prompt(Base):
    """Prompt templates"""
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    template = Column(Text, nullable=False)

    model_family = Column(String(100))
    category = Column(String(100), index=True)
    tags = Column(JSON, default=[])

    variables = Column(JSON, default={})
    system_message = Column(Text)
    parameters = Column(JSON, default={})

    status = Column(SQLEnum(PromptStatus), default=PromptStatus.DRAFT, index=True)
    version = Column(Integer, default=1)
    is_public = Column(Boolean, default=True)

    usage_count = Column(Integer, default=0)
    avg_quality_score = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_prompt_status", "status"),
        Index("idx_prompt_category", "category"),
        Index("idx_prompt_creator", "creator_user_id"),
    )

    creator = relationship("User", backref="prompts")


class Workflow(Base):
    """AI Workflows - chains of operations"""
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)

    steps = Column(JSON, nullable=False)
    connections = Column(JSON, default={})
    config = Column(JSON, default={})

    prompt_ids = Column(JSON, default=[])
    model_ids = Column(JSON, default=[])

    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.DRAFT, index=True)
    is_public = Column(Boolean, default=True)

    execution_count = Column(Integer, default=0)
    avg_execution_time_ms = Column(Integer, default=0)
    success_rate = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_workflow_status", "status"),
        Index("idx_workflow_creator", "creator_user_id"),
    )

    creator = relationship("User", backref="workflows")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowExecution(Base):
    """Workflow execution history"""
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    status = Column(String(50), default="pending")
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text, nullable=True)

    execution_time_ms = Column(Integer)
    tokens_used = Column(Integer, default=0)
    cost = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_execution_workflow", "workflow_id"),
        Index("idx_execution_user", "user_id"),
    )

    workflow = relationship("Workflow", back_populates="executions")
    user = relationship("User", backref="workflow_executions")


class Agent(Base):
    """AI Agents - autonomous entities"""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)

    system_prompt = Column(Text)
    model_id = Column(Integer)

    tools = Column(JSON, default=[])
    memory_config = Column(JSON, default={})
    constraints = Column(JSON, default={})

    status = Column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT, index=True)
    is_public = Column(Boolean, default=True)

    execution_count = Column(Integer, default=0)
    success_rate = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_agent_status", "status"),
        Index("idx_agent_creator", "creator_user_id"),
    )

    creator = relationship("User", backref="agents")
    conversations = relationship("AgentConversation", back_populates="agent", cascade="all, delete-orphan")


class AgentConversation(Base):
    """Agent conversations and interactions"""
    __tablename__ = "agent_conversations"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255))
    messages = Column(JSON, default=[])

    status = Column(String(50), default="active")
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_conversation_agent", "agent_id"),
        Index("idx_conversation_user", "user_id"),
    )

    agent = relationship("Agent", back_populates="conversations")
    user = relationship("User", backref="agent_conversations")
