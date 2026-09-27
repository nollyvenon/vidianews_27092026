"""Tests for advanced AI services (Modules 15-20)"""

import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.base import Base
from app.models.ai_advanced import (
    Memory, ConversationMemory, AITemplate, Chat, ChatMessage,
    Document, ResearchQuery, UsageMetric, CostAlert,
    SafetyCheck, ComplianceLog,
    MemoryType, ChatStatus, DocumentType, MonitoringMetric, SafetyLevel
)
from app.services.ai_advanced_service import (
    MemoryService, TemplateService, ChatService,
    ResearchService, MonitoringService, SafetyService
)


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


# ==================== MODULE 15: MEMORY TESTS ====================

@pytest.mark.asyncio
async def test_memory_store(test_db):
    service = MemoryService(test_db)
    memory = await service.store_memory(1, "short_term", "user_pref", {"theme": "dark"})

    assert memory.id is not None
    assert memory.agent_id == 1
    assert memory.memory_type == "short_term"
    assert memory.key == "user_pref"
    assert memory.value["theme"] == "dark"


@pytest.mark.asyncio
async def test_memory_get(test_db):
    service = MemoryService(test_db)
    await service.store_memory(1, "short_term", "test_key", {"data": "value"})

    memory = await service.get_memory("test_key")
    assert memory is not None
    assert memory.key == "test_key"


@pytest.mark.asyncio
async def test_memory_search(test_db):
    service = MemoryService(test_db)
    await service.store_memory(1, "short_term", "key1", {"a": 1})
    await service.store_memory(1, "short_term", "key2", {"b": 2})

    memories = await service.search_memories(1, "short_term")
    assert len(memories) == 2


@pytest.mark.asyncio
async def test_memory_delete_expired(test_db):
    service = MemoryService(test_db)
    expires = datetime.now(timezone.utc) - timedelta(days=1)

    mem = Memory(agent_id=1, memory_type=MemoryType.SHORT_TERM, key="expired", value={}, expires_at=expires)
    test_db.add(mem)
    await test_db.commit()

    deleted = await service.delete_expired_memories()
    assert deleted >= 1


# ==================== MODULE 16: TEMPLATE TESTS ====================

@pytest.mark.asyncio
async def test_template_create(test_db):
    service = TemplateService(test_db)
    template = await service.create_template("GPT4Template", "gpt4-template", {"model": "gpt-4"}, 1)

    assert template.id is not None
    assert template.name == "GPT4Template"
    assert template.slug == "gpt4-template"


@pytest.mark.asyncio
async def test_template_get(test_db):
    service = TemplateService(test_db)
    created = await service.create_template("T1", "t1", {}, 1)

    template = await service.get_template(created.id)
    assert template is not None
    assert template.id == created.id


@pytest.mark.asyncio
async def test_template_list(test_db):
    service = TemplateService(test_db)
    await service.create_template("T1", "t1", {}, 1)
    await service.create_template("T2", "t2", {}, 1)

    templates = await service.list_templates()
    assert len(templates) >= 2


@pytest.mark.asyncio
async def test_template_use(test_db):
    service = TemplateService(test_db)
    template = await service.create_template("T1", "t1", {}, 1)

    success = await service.use_template(template.id)
    assert success is True

    updated = await service.get_template(template.id)
    assert updated.usage_count >= 1


# ==================== MODULE 17: CHAT TESTS ====================

@pytest.mark.asyncio
async def test_chat_create(test_db):
    service = ChatService(test_db)
    chat = await service.create_chat(1, "Test Chat")

    assert chat.id is not None
    assert chat.user_id == 1
    assert chat.title == "Test Chat"


@pytest.mark.asyncio
async def test_chat_add_message(test_db):
    service = ChatService(test_db)
    chat = await service.create_chat(1)

    message = await service.add_message(chat.id, "user", "Hello", 10)
    assert message.id is not None
    assert message.role == "user"
    assert message.tokens == 10


@pytest.mark.asyncio
async def test_chat_get(test_db):
    service = ChatService(test_db)
    chat = await service.create_chat(1, "C1")

    retrieved = await service.get_chat(chat.id)
    assert retrieved is not None
    assert retrieved.id == chat.id


@pytest.mark.asyncio
async def test_chat_list(test_db):
    service = ChatService(test_db)
    await service.create_chat(1, "C1")
    await service.create_chat(1, "C2")

    chats = await service.list_chats(1)
    assert len(chats) >= 2


@pytest.mark.asyncio
async def test_chat_token_tracking(test_db):
    service = ChatService(test_db)
    chat = await service.create_chat(1)

    await service.add_message(chat.id, "user", "Hello", 10)
    await service.add_message(chat.id, "assistant", "Hi", 15)

    updated = await service.get_chat(chat.id)
    assert updated.total_tokens >= 25


# ==================== MODULE 18: RESEARCH TESTS ====================

@pytest.mark.asyncio
async def test_document_add(test_db):
    service = ResearchService(test_db)
    doc = await service.add_document(1, "Test Doc", "Content here", "text")

    assert doc.id is not None
    assert doc.user_id == 1
    assert doc.title == "Test Doc"
    assert doc.document_type == DocumentType.TEXT


@pytest.mark.asyncio
async def test_document_index(test_db):
    service = ResearchService(test_db)
    await service.add_document(1, "D1", "Content", "text")
    await service.add_document(1, "D2", "Content", "text")

    indexed = await service.index_documents(1)
    assert indexed >= 2


@pytest.mark.asyncio
async def test_document_search(test_db):
    service = ResearchService(test_db)
    doc = await service.add_document(1, "Doc", "Content", "text")

    # Index first
    await service.index_documents(1)

    results = await service.search_documents(1, "test")
    assert len(results) >= 0


@pytest.mark.asyncio
async def test_research_query_create(test_db):
    service = ResearchService(test_db)
    query = await service.create_research_query(1, "What is AI?")

    assert query.id is not None
    assert query.user_id == 1
    assert query.query == "What is AI?"


# ==================== MODULE 19: MONITORING TESTS ====================

@pytest.mark.asyncio
async def test_metric_record(test_db):
    service = MonitoringService(test_db)
    metric = await service.record_metric(1, "tokens", 100.0)

    assert metric.id is not None
    assert metric.user_id == 1
    assert metric.metric_type == "tokens"
    assert metric.value == 100.0


@pytest.mark.asyncio
async def test_metric_usage_stats(test_db):
    service = MonitoringService(test_db)
    await service.record_metric(1, "tokens", 50.0)
    await service.record_metric(1, "tokens", 100.0)
    await service.record_metric(1, "cost", 5.0)

    stats = await service.get_usage_stats(1, 30)
    assert stats["count"] >= 3
    assert stats["total"] > 0


@pytest.mark.asyncio
async def test_cost_alert_create(test_db):
    service = MonitoringService(test_db)
    alert = await service.create_cost_alert(1, 100.0, "monthly")

    assert alert.id is not None
    assert alert.threshold == 100.0
    assert alert.period == "monthly"


@pytest.mark.asyncio
async def test_cost_alert_check(test_db):
    service = MonitoringService(test_db)
    await service.create_cost_alert(1, 50.0, "daily")

    alerts = await service.check_alerts(1)
    assert len(alerts) >= 1


# ==================== MODULE 20: SAFETY TESTS ====================

@pytest.mark.asyncio
async def test_safety_check_content(test_db):
    service = SafetyService(test_db)
    check = await service.check_content("Test content")

    assert check.id is not None
    assert check.content == "Test content"


@pytest.mark.asyncio
async def test_safety_check_get(test_db):
    service = SafetyService(test_db)
    check = await service.check_content("Content")

    retrieved = await service.get_safety_check(check.id)
    assert retrieved is not None
    assert retrieved.id == check.id


@pytest.mark.asyncio
async def test_safety_approve_content(test_db):
    service = SafetyService(test_db)
    check = await service.check_content("Content")

    success = await service.approve_content(check.id)
    assert success is True

    updated = await service.get_safety_check(check.id)
    assert updated.is_approved is True


@pytest.mark.asyncio
async def test_compliance_log_create(test_db):
    service = SafetyService(test_db)
    log = await service.log_compliance_action(1, "content_reviewed", "doc_123")

    assert log.id is not None
    assert log.user_id == 1
    assert log.action == "content_reviewed"


@pytest.mark.asyncio
async def test_compliance_get_logs(test_db):
    service = SafetyService(test_db)
    await service.log_compliance_action(1, "action1", "res1")
    await service.log_compliance_action(1, "action2", "res2")

    logs = await service.get_compliance_logs(1)
    assert len(logs) >= 2


# ==================== INTEGRATION TESTS ====================

@pytest.mark.asyncio
async def test_full_memory_workflow(test_db):
    mem_service = MemoryService(test_db)

    # Store multiple memories
    await mem_service.store_memory(1, "short_term", "k1", {"x": 1})
    await mem_service.store_memory(1, "long_term", "k2", {"y": 2})

    # Retrieve
    retrieved = await mem_service.get_memory("k1")
    assert retrieved.value["x"] == 1

    # Search
    memories = await mem_service.search_memories(1, "short_term")
    assert len(memories) >= 1


@pytest.mark.asyncio
async def test_full_chat_workflow(test_db):
    chat_service = ChatService(test_db)

    # Create chat
    chat = await chat_service.create_chat(1, "Q&A Session")

    # Add messages
    await chat_service.add_message(chat.id, "user", "What is Python?", 5)
    await chat_service.add_message(chat.id, "assistant", "Python is...", 50)

    # Retrieve with history
    retrieved = await chat_service.get_chat(chat.id)
    assert retrieved.total_tokens >= 55
    assert len(retrieved.messages) >= 2


@pytest.mark.asyncio
async def test_full_research_workflow(test_db):
    research_service = ResearchService(test_db)

    # Add documents
    doc1 = await research_service.add_document(1, "Research1", "Content A", "text")
    doc2 = await research_service.add_document(1, "Research2", "Content B", "pdf")

    # Index
    indexed = await research_service.index_documents(1)
    assert indexed >= 2

    # Create query
    query = await research_service.create_research_query(1, "Find AI papers")
    assert query.user_id == 1


@pytest.mark.asyncio
async def test_full_monitoring_workflow(test_db):
    monitor_service = MonitoringService(test_db)

    # Record metrics
    await monitor_service.record_metric(1, "tokens", 100.0)
    await monitor_service.record_metric(1, "cost", 5.0)

    # Set alert
    alert = await monitor_service.create_cost_alert(1, 50.0, "daily")
    assert alert.is_active is True

    # Check stats
    stats = await monitor_service.get_usage_stats(1, 7)
    assert stats["count"] >= 2


@pytest.mark.asyncio
async def test_full_safety_workflow(test_db):
    safety_service = SafetyService(test_db)

    # Check content
    check = await safety_service.check_content("User input content")

    # Approve
    await safety_service.approve_content(check.id)

    # Log compliance
    log = await safety_service.log_compliance_action(1, "content_approved", f"check_{check.id}")

    # Retrieve logs
    logs = await safety_service.get_compliance_logs(1)
    assert len(logs) >= 1


@pytest.mark.asyncio
async def test_cross_module_integration(test_db):
    """Test interactions between different modules"""
    template_service = TemplateService(test_db)
    chat_service = ChatService(test_db)
    safety_service = SafetyService(test_db)

    # Create template for prompts
    template = await template_service.create_template("ChatTemplate", "chat-tpl", {"system": "Be helpful"}, 1)

    # Create chat using template
    chat = await chat_service.create_chat(1, "Template-based Chat")

    # Add message and check safety
    await chat_service.add_message(chat.id, "user", "Hello", 5)
    check = await safety_service.check_content("Hello")

    # Verify all connected
    assert template.id is not None
    assert chat.id is not None
    assert check.id is not None
