"""AI Core services for Prompts, Workflows, and Agents"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from app.models.ai_core import (
    Prompt, Workflow, WorkflowExecution, Agent, AgentConversation,
    PromptStatus, WorkflowStatus, AgentStatus
)


class PromptService:
    """Prompt template management"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_prompt(self, name: str, slug: str, template: str, creator_user_id: int, **kwargs) -> Prompt:
        prompt = Prompt(name=name, slug=slug, template=template, creator_user_id=creator_user_id, **kwargs)
        self.session.add(prompt)
        await self.session.commit()
        await self.session.refresh(prompt)
        return prompt

    async def get_prompt(self, prompt_id: int) -> Optional[Prompt]:
        stmt = select(Prompt).where(Prompt.id == prompt_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_prompts(self, status: Optional[PromptStatus] = None, limit: int = 50) -> List[Prompt]:
        stmt = select(Prompt)
        if status:
            stmt = stmt.where(Prompt.status == status)
        stmt = stmt.order_by(desc(Prompt.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_prompt(self, prompt_id: int, **kwargs) -> Optional[Prompt]:
        stmt = update(Prompt).where(Prompt.id == prompt_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_prompt(prompt_id)

    async def publish_prompt(self, prompt_id: int) -> Optional[Prompt]:
        return await self.update_prompt(prompt_id, status=PromptStatus.PUBLISHED)

    async def delete_prompt(self, prompt_id: int) -> bool:
        stmt = delete(Prompt).where(Prompt.id == prompt_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_prompts_by_category(self, category: str) -> List[Prompt]:
        stmt = select(Prompt).where(
            and_(Prompt.category == category, Prompt.status == PromptStatus.PUBLISHED)
        ).order_by(desc(Prompt.usage_count))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search_prompts(self, query: str) -> List[Prompt]:
        stmt = select(Prompt).where(
            Prompt.name.ilike(f"%{query}%")
        ).order_by(desc(Prompt.usage_count))
        result = await self.session.execute(stmt)
        return result.scalars().all()


class WorkflowService:
    """Workflow management"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_workflow(self, name: str, slug: str, steps: Dict, creator_user_id: int, **kwargs) -> Workflow:
        workflow = Workflow(name=name, slug=slug, steps=steps, creator_user_id=creator_user_id, **kwargs)
        self.session.add(workflow)
        await self.session.commit()
        await self.session.refresh(workflow)
        return workflow

    async def get_workflow(self, workflow_id: int) -> Optional[Workflow]:
        stmt = select(Workflow).where(Workflow.id == workflow_id).options(selectinload(Workflow.executions))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_workflows(self, status: Optional[WorkflowStatus] = None, limit: int = 50) -> List[Workflow]:
        stmt = select(Workflow)
        if status:
            stmt = stmt.where(Workflow.status == status)
        stmt = stmt.order_by(desc(Workflow.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_workflow(self, workflow_id: int, **kwargs) -> Optional[Workflow]:
        stmt = update(Workflow).where(Workflow.id == workflow_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_workflow(workflow_id)

    async def execute_workflow(self, workflow_id: int, user_id: int, input_data: Dict) -> WorkflowExecution:
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            user_id=user_id,
            input_data=input_data,
            status="running"
        )
        self.session.add(execution)
        await self.session.commit()
        await self.session.refresh(execution)
        return execution

    async def update_execution(self, execution_id: int, **kwargs) -> Optional[WorkflowExecution]:
        stmt = update(WorkflowExecution).where(WorkflowExecution.id == execution_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.session.execute(select(WorkflowExecution).where(WorkflowExecution.id == execution_id))

    async def get_execution_history(self, workflow_id: int, limit: int = 50) -> List[WorkflowExecution]:
        stmt = select(WorkflowExecution).where(
            WorkflowExecution.workflow_id == workflow_id
        ).order_by(desc(WorkflowExecution.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_workflow(self, workflow_id: int) -> bool:
        stmt = delete(Workflow).where(Workflow.id == workflow_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0


class AgentService:
    """Agent management"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_agent(self, name: str, slug: str, creator_user_id: int, **kwargs) -> Agent:
        agent = Agent(name=name, slug=slug, creator_user_id=creator_user_id, **kwargs)
        self.session.add(agent)
        await self.session.commit()
        await self.session.refresh(agent)
        return agent

    async def get_agent(self, agent_id: int) -> Optional[Agent]:
        stmt = select(Agent).where(Agent.id == agent_id).options(selectinload(Agent.conversations))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_agents(self, status: Optional[AgentStatus] = None, limit: int = 50) -> List[Agent]:
        stmt = select(Agent)
        if status:
            stmt = stmt.where(Agent.status == status)
        stmt = stmt.order_by(desc(Agent.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_agent(self, agent_id: int, **kwargs) -> Optional[Agent]:
        stmt = update(Agent).where(Agent.id == agent_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_agent(agent_id)

    async def activate_agent(self, agent_id: int) -> Optional[Agent]:
        return await self.update_agent(agent_id, status=AgentStatus.ACTIVE)

    async def pause_agent(self, agent_id: int) -> Optional[Agent]:
        return await self.update_agent(agent_id, status=AgentStatus.PAUSED)

    async def delete_agent(self, agent_id: int) -> bool:
        stmt = delete(Agent).where(Agent.id == agent_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def create_conversation(self, agent_id: int, user_id: int, title: Optional[str] = None) -> AgentConversation:
        conversation = AgentConversation(
            agent_id=agent_id,
            user_id=user_id,
            title=title or f"Conversation with {agent_id}",
            messages=[]
        )
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: int) -> Optional[AgentConversation]:
        stmt = select(AgentConversation).where(AgentConversation.id == conversation_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_message(self, conversation_id: int, role: str, content: str) -> Optional[AgentConversation]:
        conversation = await self.get_conversation(conversation_id)
        if conversation:
            messages = conversation.messages or []
            messages.append({"role": role, "content": content, "timestamp": datetime.now(timezone.utc).isoformat()})
            return await self.update_conversation(conversation_id, messages=messages)
        return None

    async def update_conversation(self, conversation_id: int, **kwargs) -> Optional[AgentConversation]:
        stmt = update(AgentConversation).where(AgentConversation.id == conversation_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_conversation(conversation_id)

    async def get_conversations(self, agent_id: int, user_id: int) -> List[AgentConversation]:
        stmt = select(AgentConversation).where(
            and_(AgentConversation.agent_id == agent_id, AgentConversation.user_id == user_id)
        ).order_by(desc(AgentConversation.created_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_agent_stats(self, agent_id: int) -> Dict[str, Any]:
        agent = await self.get_agent(agent_id)
        if not agent:
            return {}

        conv_stmt = select(func.count(AgentConversation.id)).where(AgentConversation.agent_id == agent_id)
        conv_count = await self.session.scalar(conv_stmt)

        return {
            "agent_id": agent.id,
            "name": agent.name,
            "status": agent.status.value,
            "conversations": conv_count,
            "execution_count": agent.execution_count,
            "success_rate": agent.success_rate
        }
