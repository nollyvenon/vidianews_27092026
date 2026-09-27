"""Advanced AI services: Memory, Templates, Chat, Research, Monitoring, Safety"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.models.ai_advanced import (
    Memory, ConversationMemory, AITemplate, Chat, ChatMessage,
    Document, ResearchQuery, UsageMetric, CostAlert,
    SafetyCheck, ComplianceLog
)


class MemoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def store_memory(self, agent_id: int, memory_type: str, key: str, value: Dict) -> Memory:
        memory = Memory(agent_id=agent_id, memory_type=memory_type, key=key, value=value)
        self.session.add(memory)
        await self.session.commit()
        await self.session.refresh(memory)
        return memory

    async def get_memory(self, key: str) -> Optional[Memory]:
        stmt = select(Memory).where(Memory.key == key)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def search_memories(self, agent_id: int, memory_type: str) -> List[Memory]:
        stmt = select(Memory).where(
            and_(Memory.agent_id == agent_id, Memory.memory_type == memory_type)
        ).order_by(desc(Memory.relevance_score))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_expired_memories(self) -> int:
        now = datetime.now(timezone.utc)
        stmt = delete(Memory).where(Memory.expires_at <= now)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount


class TemplateService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_template(self, name: str, slug: str, definition: Dict, creator_user_id: int, **kwargs) -> AITemplate:
        template = AITemplate(name=name, slug=slug, definition=definition, creator_user_id=creator_user_id, **kwargs)
        self.session.add(template)
        await self.session.commit()
        await self.session.refresh(template)
        return template

    async def get_template(self, template_id: int) -> Optional[AITemplate]:
        stmt = select(AITemplate).where(AITemplate.id == template_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_templates(self, category: Optional[str] = None) -> List[AITemplate]:
        stmt = select(AITemplate).where(AITemplate.is_public == True)
        if category:
            stmt = stmt.where(AITemplate.category == category)
        stmt = stmt.order_by(desc(AITemplate.usage_count))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def use_template(self, template_id: int) -> bool:
        stmt = update(AITemplate).where(AITemplate.id == template_id).values(
            usage_count=AITemplate.usage_count + 1
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return True


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, user_id: int, title: Optional[str] = None) -> Chat:
        chat = Chat(user_id=user_id, title=title or f"Chat {datetime.now(timezone.utc).isoformat()}")
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def add_message(self, chat_id: int, role: str, content: str, tokens: int = 0) -> ChatMessage:
        message = ChatMessage(chat_id=chat_id, role=role, content=content, tokens=tokens)
        self.session.add(message)

        chat = await self.session.get(Chat, chat_id)
        if chat:
            chat.total_tokens += tokens

        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_chat(self, chat_id: int) -> Optional[Chat]:
        stmt = select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.messages))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_chats(self, user_id: int) -> List[Chat]:
        stmt = select(Chat).where(Chat.user_id == user_id).order_by(desc(Chat.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()


class ResearchService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_document(self, user_id: int, title: str, content: str, doc_type: str) -> Document:
        doc = Document(user_id=user_id, title=title, content=content, document_type=doc_type)
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def index_documents(self, user_id: int) -> int:
        stmt = update(Document).where(
            and_(Document.user_id == user_id, Document.is_indexed == False)
        ).values(is_indexed=True)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    async def search_documents(self, user_id: int, query: str) -> List[Document]:
        stmt = select(Document).where(
            and_(Document.user_id == user_id, Document.is_indexed == True)
        ).order_by(desc(Document.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_research_query(self, user_id: int, query: str) -> ResearchQuery:
        research = ResearchQuery(user_id=user_id, query=query)
        self.session.add(research)
        await self.session.commit()
        await self.session.refresh(research)
        return research


class MonitoringService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_metric(self, user_id: int, metric_type: str, value: float, **kwargs) -> UsageMetric:
        metric = UsageMetric(user_id=user_id, metric_type=metric_type, value=value, **kwargs)
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def get_usage_stats(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = select(
            func.sum(UsageMetric.value).label("total"),
            func.avg(UsageMetric.value).label("avg"),
            func.count(UsageMetric.id).label("count")
        ).where(
            and_(UsageMetric.user_id == user_id, UsageMetric.created_at >= cutoff)
        )
        result = await self.session.execute(stmt)
        row = result.one()
        return {
            "period_days": days,
            "total": row.total or 0,
            "average": row.avg or 0,
            "count": row.count or 0
        }

    async def create_cost_alert(self, user_id: int, threshold: float, period: str) -> CostAlert:
        alert = CostAlert(user_id=user_id, threshold=threshold, period=period)
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def check_alerts(self, user_id: int) -> List[CostAlert]:
        stmt = select(CostAlert).where(
            and_(CostAlert.user_id == user_id, CostAlert.is_active == True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


class SafetyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_content(self, content: str) -> SafetyCheck:
        check = SafetyCheck(content=content)
        self.session.add(check)
        await self.session.commit()
        await self.session.refresh(check)
        return check

    async def get_safety_check(self, check_id: int) -> Optional[SafetyCheck]:
        stmt = select(SafetyCheck).where(SafetyCheck.id == check_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def approve_content(self, check_id: int) -> bool:
        stmt = update(SafetyCheck).where(SafetyCheck.id == check_id).values(is_approved=True)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def log_compliance_action(self, user_id: int, action: str, resource: Optional[str] = None) -> ComplianceLog:
        log = ComplianceLog(user_id=user_id, action=action, resource=resource)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_compliance_logs(self, user_id: int, limit: int = 100) -> List[ComplianceLog]:
        stmt = select(ComplianceLog).where(ComplianceLog.user_id == user_id).order_by(
            desc(ComplianceLog.created_at)
        ).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
