"""AI Core API endpoints for Prompts (M12), Workflows (M13), and Agents (M14)"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.ai_core import PromptStatus, WorkflowStatus, AgentStatus
from app.services.ai_core_service import PromptService, WorkflowService, AgentService
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai-core"])

# ==================== PROMPTS (Module 12) ====================

class PromptCreate(BaseModel):
    name: str
    slug: str
    template: str
    description: Optional[str] = None
    category: Optional[str] = None
    system_message: Optional[str] = None
    variables: Optional[Dict] = None
    parameters: Optional[Dict] = None

class PromptResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    category: Optional[str]
    status: str
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/prompts", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(req: PromptCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create prompt template"""
    service = PromptService(session)
    return await service.create_prompt(
        name=req.name,
        slug=req.slug,
        template=req.template,
        creator_user_id=current_user.id,
        **{k: v for k, v in req.model_dump().items() if k not in ["name", "slug", "template"]}
    )

@router.get("/prompts", response_model=List[PromptResponse])
async def list_prompts(status_filter: Optional[str] = Query(None, alias="status"), limit: int = Query(50, le=100), session: AsyncSession = Depends(get_db)):
    """List prompts"""
    service = PromptService(session)
    status_enum = PromptStatus(status_filter) if status_filter else None
    return await service.list_prompts(status=status_enum, limit=limit)

@router.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: int, session: AsyncSession = Depends(get_db)):
    """Get prompt"""
    service = PromptService(session)
    prompt = await service.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return prompt

@router.get("/prompts/category/{category}", response_model=List[PromptResponse])
async def get_prompts_by_category(category: str, session: AsyncSession = Depends(get_db)):
    """Get prompts by category"""
    service = PromptService(session)
    return await service.get_prompts_by_category(category)

@router.get("/prompts/search", response_model=List[PromptResponse])
async def search_prompts(query: str = Query(..., min_length=1), session: AsyncSession = Depends(get_db)):
    """Search prompts"""
    service = PromptService(session)
    return await service.search_prompts(query)

@router.post("/prompts/{prompt_id}/publish", response_model=PromptResponse)
async def publish_prompt(prompt_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Publish prompt"""
    service = PromptService(session)
    prompt = await service.publish_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return prompt

@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(prompt_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Delete prompt"""
    service = PromptService(session)
    if not await service.delete_prompt(prompt_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# ==================== WORKFLOWS (Module 13) ====================

class WorkflowCreate(BaseModel):
    name: str
    slug: str
    steps: Dict[str, Any]
    description: Optional[str] = None
    prompt_ids: Optional[List[int]] = None
    model_ids: Optional[List[int]] = None

class WorkflowResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    status: str
    execution_count: int
    success_rate: int
    created_at: datetime

    class Config:
        from_attributes = True

class WorkflowExecutionResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    execution_time_ms: Optional[int]
    tokens_used: int
    cost: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(req: WorkflowCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create workflow"""
    service = WorkflowService(session)
    return await service.create_workflow(
        name=req.name,
        slug=req.slug,
        steps=req.steps,
        creator_user_id=current_user.id,
        description=req.description,
        prompt_ids=req.prompt_ids or [],
        model_ids=req.model_ids or []
    )

@router.get("/workflows", response_model=List[WorkflowResponse])
async def list_workflows(session: AsyncSession = Depends(get_db)):
    """List workflows"""
    service = WorkflowService(session)
    return await service.list_workflows()

@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: int, session: AsyncSession = Depends(get_db)):
    """Get workflow"""
    service = WorkflowService(session)
    workflow = await service.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return workflow

@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(workflow_id: int, input_data: Dict[str, Any], current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Execute workflow"""
    service = WorkflowService(session)
    workflow = await service.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await service.execute_workflow(workflow_id, current_user.id, input_data)

@router.get("/workflows/{workflow_id}/executions", response_model=List[WorkflowExecutionResponse])
async def get_execution_history(workflow_id: int, session: AsyncSession = Depends(get_db)):
    """Get execution history"""
    service = WorkflowService(session)
    return await service.get_execution_history(workflow_id)

@router.delete("/workflows/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(workflow_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Delete workflow"""
    service = WorkflowService(session)
    if not await service.delete_workflow(workflow_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# ==================== AGENTS (Module 14) ====================

class AgentCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    model_id: Optional[int] = None
    tools: Optional[List[str]] = None
    constraints: Optional[Dict] = None

class AgentResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    status: str
    execution_count: int
    success_rate: int
    created_at: datetime

    class Config:
        from_attributes = True

class AgentConversationResponse(BaseModel):
    id: int
    agent_id: int
    title: str
    status: str
    total_tokens: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/agents", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(req: AgentCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create agent"""
    service = AgentService(session)
    return await service.create_agent(
        name=req.name,
        slug=req.slug,
        creator_user_id=current_user.id,
        description=req.description,
        system_prompt=req.system_prompt,
        model_id=req.model_id,
        tools=req.tools or [],
        constraints=req.constraints or {}
    )

@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(session: AsyncSession = Depends(get_db)):
    """List agents"""
    service = AgentService(session)
    return await service.list_agents()

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, session: AsyncSession = Depends(get_db)):
    """Get agent"""
    service = AgentService(session)
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return agent

@router.get("/agents/{agent_id}/stats", response_model=Dict[str, Any])
async def get_agent_stats(agent_id: int, session: AsyncSession = Depends(get_db)):
    """Get agent statistics"""
    service = AgentService(session)
    stats = await service.get_agent_stats(agent_id)
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return stats

@router.post("/agents/{agent_id}/activate", response_model=AgentResponse)
async def activate_agent(agent_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Activate agent"""
    service = AgentService(session)
    agent = await service.activate_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return agent

@router.post("/agents/{agent_id}/pause", response_model=AgentResponse)
async def pause_agent(agent_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Pause agent"""
    service = AgentService(session)
    agent = await service.pause_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return agent

@router.post("/agents/{agent_id}/conversations", response_model=AgentConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(agent_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Start agent conversation"""
    service = AgentService(session)
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await service.create_conversation(agent_id, current_user.id)

@router.get("/agents/{agent_id}/conversations", response_model=List[AgentConversationResponse])
async def get_conversations(agent_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get agent conversations"""
    service = AgentService(session)
    return await service.get_conversations(agent_id, current_user.id)

@router.post("/agents/conversations/{conversation_id}/message", response_model=AgentConversationResponse)
async def add_message(conversation_id: int, role: str, content: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Add message to conversation"""
    service = AgentService(session)
    conversation = await service.add_message(conversation_id, role, content)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return conversation

@router.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Delete agent"""
    service = AgentService(session)
    if not await service.delete_agent(agent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
