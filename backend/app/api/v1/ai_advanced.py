"""Advanced AI APIs: Memory (M15), Templates (M16), Chat (M17), Research (M18), Monitoring (M19), Safety (M20)"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.ai_advanced_service import (
    MemoryService, TemplateService, ChatService,
    ResearchService, MonitoringService, SafetyService
)
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai-advanced"])

# ==================== MODULE 15: MEMORY ====================

class MemoryCreate(BaseModel):
    memory_type: str
    key: str
    value: Dict[str, Any]
    expires_at: Optional[datetime] = None

class MemoryResponse(BaseModel):
    id: int
    key: str
    value: Dict
    memory_type: str
    relevance_score: float
    access_count: int
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/memory", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def store_memory(req: MemoryCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Store memory for agent"""
    service = MemoryService(session)
    return await service.store_memory(current_user.id, req.memory_type, req.key, req.value)

@router.get("/memory/{key}", response_model=Optional[MemoryResponse])
async def get_memory(key: str, session: AsyncSession = Depends(get_db)):
    """Retrieve memory by key"""
    service = MemoryService(session)
    return await service.get_memory(key)

@router.post("/memory/cleanup", response_model=Dict[str, int])
async def cleanup_expired(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Clean up expired memories"""
    service = MemoryService(session)
    deleted = await service.delete_expired_memories()
    return {"deleted": deleted}

# ==================== MODULE 16: TEMPLATES ====================

class TemplateCreate(BaseModel):
    name: str
    slug: str
    definition: Dict[str, Any]
    category: Optional[str] = None
    description: Optional[str] = None

class TemplateResponse(BaseModel):
    id: int
    name: str
    slug: str
    category: Optional[str]
    usage_count: int
    rating: float
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/templates", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(req: TemplateCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create AI template"""
    service = TemplateService(session)
    return await service.create_template(req.name, req.slug, req.definition, current_user.id, category=req.category, description=req.description)

@router.get("/templates", response_model=List[TemplateResponse])
async def list_templates(category: Optional[str] = None, session: AsyncSession = Depends(get_db)):
    """List templates"""
    service = TemplateService(session)
    return await service.list_templates(category)

@router.get("/templates/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: int, session: AsyncSession = Depends(get_db)):
    """Get template"""
    service = TemplateService(session)
    template = await service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return template

@router.post("/templates/{template_id}/use", response_model=Dict[str, str])
async def use_template(template_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Record template usage"""
    service = TemplateService(session)
    success = await service.use_template(template_id)
    return {"status": "success" if success else "failed"}

# ==================== MODULE 17: CHAT ====================

class ChatCreate(BaseModel):
    title: Optional[str] = None
    system_prompt: Optional[str] = None

class ChatMessageCreate(BaseModel):
    role: str
    content: str
    tokens: int = 0

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    tokens: int
    created_at: datetime
    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    id: int
    title: str
    status: str
    total_tokens: int
    total_cost: float
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/chats", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(req: ChatCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create chat"""
    service = ChatService(session)
    return await service.create_chat(current_user.id, req.title)

@router.get("/chats", response_model=List[ChatResponse])
async def list_chats(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """List user chats"""
    service = ChatService(session)
    return await service.list_chats(current_user.id)

@router.get("/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get chat"""
    service = ChatService(session)
    chat = await service.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return chat

@router.post("/chats/{chat_id}/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def add_message(chat_id: int, req: ChatMessageCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Add message to chat"""
    service = ChatService(session)
    return await service.add_message(chat_id, req.role, req.content, req.tokens)

# ==================== MODULE 18: RESEARCH ====================

class DocumentCreate(BaseModel):
    title: str
    content: str
    document_type: str
    source_url: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    document_type: str
    is_indexed: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ResearchQueryCreate(BaseModel):
    query: str

class ResearchQueryResponse(BaseModel):
    id: int
    query: str
    summary: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def add_document(req: DocumentCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Add research document"""
    service = ResearchService(session)
    return await service.add_document(current_user.id, req.title, req.content, req.document_type)

@router.post("/documents/index", response_model=Dict[str, int])
async def index_documents(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Index documents for search"""
    service = ResearchService(session)
    indexed = await service.index_documents(current_user.id)
    return {"indexed": indexed}

@router.get("/documents/search", response_model=List[DocumentResponse])
async def search_documents(query: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Search documents"""
    service = ResearchService(session)
    return await service.search_documents(current_user.id, query)

@router.post("/research", response_model=ResearchQueryResponse, status_code=status.HTTP_201_CREATED)
async def create_research_query(req: ResearchQueryCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create research query"""
    service = ResearchService(session)
    return await service.create_research_query(current_user.id, req.query)

# ==================== MODULE 19: MONITORING ====================

class MetricCreate(BaseModel):
    metric_type: str
    value: float
    tags: Optional[Dict] = None

class MetricResponse(BaseModel):
    id: int
    metric_type: str
    value: float
    created_at: datetime
    class Config:
        from_attributes = True

class CostAlertCreate(BaseModel):
    threshold: float
    period: str

class CostAlertResponse(BaseModel):
    id: int
    threshold: float
    period: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/metrics", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def record_metric(req: MetricCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Record usage metric"""
    service = MonitoringService(session)
    return await service.record_metric(current_user.id, req.metric_type, req.value, tags=req.tags)

@router.get("/metrics/usage", response_model=Dict[str, Any])
async def get_usage_stats(days: int = Query(30, ge=1, le=365), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get usage statistics"""
    service = MonitoringService(session)
    return await service.get_usage_stats(current_user.id, days)

@router.post("/alerts/cost", response_model=CostAlertResponse, status_code=status.HTTP_201_CREATED)
async def create_cost_alert(req: CostAlertCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Create cost alert"""
    service = MonitoringService(session)
    return await service.create_cost_alert(current_user.id, req.threshold, req.period)

@router.get("/alerts", response_model=List[CostAlertResponse])
async def get_alerts(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get active alerts"""
    service = MonitoringService(session)
    return await service.check_alerts(current_user.id)

# ==================== MODULE 20: SAFETY ====================

class SafetyCheckCreate(BaseModel):
    content: str

class SafetyCheckResponse(BaseModel):
    id: int
    severity: str
    flags: list
    is_approved: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ComplianceLogResponse(BaseModel):
    id: int
    action: str
    resource: Optional[str]
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/safety/check", response_model=SafetyCheckResponse, status_code=status.HTTP_201_CREATED)
async def check_content(req: SafetyCheckCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Check content safety"""
    service = SafetyService(session)
    return await service.check_content(req.content)

@router.get("/safety/check/{check_id}", response_model=SafetyCheckResponse)
async def get_safety_check(check_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get safety check result"""
    service = SafetyService(session)
    check = await service.get_safety_check(check_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return check

@router.post("/safety/check/{check_id}/approve", response_model=Dict[str, str])
async def approve_content(check_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Approve content"""
    service = SafetyService(session)
    success = await service.approve_content(check_id)
    return {"status": "approved" if success else "failed"}

@router.get("/compliance/logs", response_model=List[ComplianceLogResponse])
async def get_compliance_logs(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Get compliance logs"""
    service = SafetyService(session)
    return await service.get_compliance_logs(current_user.id)

@router.post("/compliance/log", response_model=ComplianceLogResponse, status_code=status.HTTP_201_CREATED)
async def log_action(action: str, resource: Optional[str] = None, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    """Log compliance action"""
    service = SafetyService(session)
    return await service.log_compliance_action(current_user.id, action, resource)
