from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.database import get_db
from app.services.platform_completion_service import (
    SocialService, SearchService, PushNotificationService,
    AdminService, SystemService
)

router = APIRouter(prefix="/api/v1/platform", tags=["platform"])


class InteractionRequest(BaseModel):
    content_id: int
    interaction_type: str
    metadata: Optional[Dict] = None


class InteractionResponse(BaseModel):
    id: int
    user_id: int
    content_id: int
    interaction_type: str
    metadata: Dict
    created_at: datetime

    class Config:
        from_attributes = True


class FollowRequest(BaseModel):
    following_id: int


class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentRequest(BaseModel):
    content_id: int
    text: str
    parent_comment_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    content_id: int
    text: str
    parent_comment_id: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageRequest(BaseModel):
    recipient_id: int
    text: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    text: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SearchIndexRequest(BaseModel):
    content_id: int
    index_type: str
    title: str
    content: str
    metadata: Optional[Dict] = None
    embeddings: Optional[List[float]] = None


class SearchIndexResponse(BaseModel):
    id: int
    content_id: int
    index_type: str
    title: str
    content: str
    metadata: Dict
    created_at: datetime

    class Config:
        from_attributes = True


class SavedSearchRequest(BaseModel):
    query: str
    filters: Optional[Dict] = None


class SavedSearchResponse(BaseModel):
    id: int
    user_id: int
    query: str
    filters: Dict
    result_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceRegistrationRequest(BaseModel):
    device_token: str
    platform: str
    device_name: Optional[str] = None


class DeviceRegistrationResponse(BaseModel):
    id: int
    user_id: int
    device_token: str
    platform: str
    device_name: Optional[str]
    last_active: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationLogRequest(BaseModel):
    notification_type: str
    title: str
    body: str
    device_id: Optional[int] = None


class NotificationLogResponse(BaseModel):
    id: int
    user_id: int
    notification_type: str
    title: str
    body: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUserRequest(BaseModel):
    user_id: int
    role: str
    permissions: Optional[List[str]] = None


class AdminUserResponse(BaseModel):
    id: int
    user_id: int
    role: str
    permissions: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AdminActionLogRequest(BaseModel):
    action_type: str
    resource_type: str
    resource_id: int
    details: Optional[Dict] = None


class AdminActionLogResponse(BaseModel):
    id: int
    admin_user_id: int
    action_type: str
    resource_type: str
    resource_id: int
    details: Dict
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SystemNotificationRequest(BaseModel):
    title: str
    message: str
    notification_type: str
    target_users: Optional[List[int]] = None
    metadata: Optional[Dict] = None


class SystemNotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class PlatformStatisticRequest(BaseModel):
    metric_name: str
    metric_value: float
    metric_type: str = "count"
    breakdown: Optional[Dict] = None


class PlatformStatisticResponse(BaseModel):
    id: int
    metric_name: str
    metric_value: float
    metric_type: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/interactions", response_model=InteractionResponse)
async def create_interaction(
    request: InteractionRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SocialService.create_interaction(
        db, user_id, request.content_id, request.interaction_type, request.metadata
    )


@router.get("/interactions/{content_id}", response_model=List[InteractionResponse])
async def get_content_interactions(
    content_id: int,
    interaction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return await SocialService.get_content_interactions(db, content_id, interaction_type)


@router.get("/my-interactions", response_model=List[InteractionResponse])
async def get_my_interactions(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SocialService.get_user_interactions(db, user_id, limit, offset)


@router.delete("/interactions/{content_id}")
async def remove_interaction(
    content_id: int,
    interaction_type: str = Query(...),
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    success = await SocialService.remove_interaction(db, user_id, content_id, interaction_type)
    return {"success": success}


@router.post("/follow", response_model=FollowResponse)
async def follow_user(
    request: FollowRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SocialService.follow_user(db, user_id, request.following_id)


@router.delete("/follow/{following_id}")
async def unfollow_user(
    following_id: int,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    success = await SocialService.unfollow_user(db, user_id, following_id)
    return {"success": success}


@router.get("/followers/{user_id}", response_model=List[FollowResponse])
async def get_followers(
    user_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await SocialService.get_followers(db, user_id, limit, offset)


@router.get("/following/{user_id}", response_model=List[FollowResponse])
async def get_following(
    user_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await SocialService.get_following(db, user_id, limit, offset)


@router.post("/comments", response_model=CommentResponse)
async def create_comment(
    request: CommentRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SocialService.create_comment(
        db, user_id, request.content_id, request.text, request.parent_comment_id
    )


@router.get("/comments/{content_id}", response_model=List[CommentResponse])
async def get_comments(
    content_id: int,
    parent_comment_id: Optional[int] = None,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await SocialService.get_comments(db, content_id, parent_comment_id, limit, offset)


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    success = await SocialService.delete_comment(db, comment_id, user_id)
    return {"success": success}


@router.post("/messages", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SocialService.send_message(db, user_id, request.recipient_id, request.text)


@router.get("/conversations/{other_user_id}", response_model=List[MessageResponse])
async def get_conversation(
    other_user_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SocialService.get_conversation(db, user_id, other_user_id, limit, offset)


@router.post("/messages/{message_id}/read")
async def mark_message_read(
    message_id: int,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    success = await SocialService.mark_message_read(db, message_id, user_id)
    return {"success": success}


@router.post("/search-index", response_model=SearchIndexResponse)
async def create_search_index(
    request: SearchIndexRequest,
    db: Session = Depends(get_db)
):
    return await SearchService.create_search_index(
        db, request.content_id, request.index_type, request.title,
        request.content, request.metadata, request.embeddings
    )


@router.get("/search", response_model=List[SearchIndexResponse])
async def search_content(
    query: str = Query(...),
    index_type: Optional[str] = None,
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await SearchService.search_content(db, query, index_type, limit, offset)


@router.post("/saved-searches", response_model=SavedSearchResponse)
async def save_search(
    request: SavedSearchRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SearchService.save_search(
        db, user_id, request.query, request.filters
    )


@router.get("/saved-searches", response_model=List[SavedSearchResponse])
async def get_saved_searches(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await SearchService.get_saved_searches(db, user_id, limit, offset)


@router.delete("/saved-searches/{search_id}")
async def delete_saved_search(
    search_id: int,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    success = await SearchService.delete_saved_search(db, search_id, user_id)
    return {"success": success}


@router.post("/devices/register", response_model=DeviceRegistrationResponse)
async def register_device(
    request: DeviceRegistrationRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await PushNotificationService.register_device(
        db, user_id, request.device_token, request.platform, request.device_name
    )


@router.delete("/devices/{device_id}")
async def unregister_device(
    device_id: int,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    success = await PushNotificationService.unregister_device(db, device_id, user_id)
    return {"success": success}


@router.get("/devices", response_model=List[DeviceRegistrationResponse])
async def get_my_devices(
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await PushNotificationService.get_user_devices(db, user_id)


@router.post("/notifications/log", response_model=NotificationLogResponse)
async def log_notification(
    request: NotificationLogRequest,
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await PushNotificationService.log_notification(
        db, user_id, request.notification_type, request.title, request.body, request.device_id
    )


@router.put("/notifications/{log_id}/status")
async def update_notification_status(
    log_id: int,
    status: str = Query(...),
    db: Session = Depends(get_db)
):
    result = await PushNotificationService.update_notification_status(
        db, log_id, status
    )
    return result


@router.get("/notifications/logs", response_model=List[NotificationLogResponse])
async def get_notification_logs(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user_id: int = Query(..., description="Current user ID")
):
    return await PushNotificationService.get_notification_logs(db, user_id, limit, offset)


@router.post("/admin/users", response_model=AdminUserResponse)
async def create_admin_user(
    request: AdminUserRequest,
    db: Session = Depends(get_db)
):
    return await AdminService.create_admin_user(db, request.user_id, request.role, request.permissions)


@router.delete("/admin/users/{user_id}")
async def remove_admin_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    success = await AdminService.remove_admin_user(db, user_id)
    return {"success": success}


@router.get("/admin/users/{user_id}", response_model=AdminUserResponse)
async def get_admin_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    admin = await AdminService.get_admin_user(db, user_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return admin


@router.post("/admin/logs", response_model=AdminActionLogResponse)
async def log_admin_action(
    request: AdminActionLogRequest,
    db: Session = Depends(get_db),
    admin_user_id: int = Query(..., description="Admin user ID")
):
    return await AdminService.log_admin_action(
        db, admin_user_id, request.action_type, request.resource_type,
        request.resource_id, request.details
    )


@router.get("/admin/logs", response_model=List[AdminActionLogResponse])
async def get_admin_logs(
    admin_user_id: Optional[int] = None,
    action_type: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await AdminService.get_admin_logs(db, admin_user_id, action_type, limit, offset)


@router.put("/admin/users/{user_id}/permissions")
async def update_admin_permissions(
    user_id: int,
    permissions: List[str],
    db: Session = Depends(get_db)
):
    result = await AdminService.update_admin_permissions(db, user_id, permissions)
    return result


@router.post("/system/notifications", response_model=SystemNotificationResponse)
async def create_system_notification(
    request: SystemNotificationRequest,
    db: Session = Depends(get_db)
):
    return await SystemService.create_system_notification(
        db, request.title, request.message, request.notification_type,
        request.target_users, request.metadata
    )


@router.get("/system/notifications", response_model=List[SystemNotificationResponse])
async def get_system_notifications(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return await SystemService.get_system_notifications(db, limit, offset)


@router.post("/statistics", response_model=PlatformStatisticResponse)
async def record_statistic(
    request: PlatformStatisticRequest,
    db: Session = Depends(get_db)
):
    return await SystemService.record_platform_statistic(
        db, request.metric_name, request.metric_value, request.metric_type, request.breakdown
    )


@router.get("/statistics", response_model=List[PlatformStatisticResponse])
async def get_statistics(
    metric_name: Optional[str] = None,
    days: int = Query(7, ge=1),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    return await SystemService.get_platform_statistics(db, metric_name, days, limit)


@router.get("/statistics/aggregated")
async def get_aggregated_statistics(
    metric_name: str = Query(...),
    days: int = Query(30, ge=1),
    db: Session = Depends(get_db)
):
    return await SystemService.get_aggregated_statistics(db, metric_name, days)


@router.get("/dashboard-summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db)
):
    return await SystemService.get_dashboard_summary(db)
