"""Platform completion endpoints: social graph, messaging, search, devices, notification logs, admin and system (async).

Access rules:
- Acting users are the signed-in caller. The ``user_id`` / ``admin_user_id`` query parameters are still accepted for
  compatibility, but a value that names anyone else is refused.
- Administrative operations (admin users, admin action log, system notifications, statistics recording, search index
  maintenance, delivery status updates) require platform administrator access.
"""

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import AliasChoices, BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_access import require_admin
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.platform_completion import (
    AdminActionType, InteractionType, PushNotificationType, SearchIndexType,
)
from app.models.user import User
from app.services.platform_completion_service import (
    AdminService, PushNotificationService, SearchService, SocialService, SystemService,
)

router = APIRouter(prefix="/platform", tags=["platform"])

require_platform_admin = require_admin("platform")


def _acting_user_id(user_id: Optional[int], current_user: User) -> int:
    """The caller's own id. A different id in the request is refused rather than trusted."""
    if user_id is not None and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only act as yourself")
    return current_user.id


class InteractionRequest(BaseModel):
    content_id: int
    interaction_type: InteractionType
    metadata: Optional[Dict] = None


class InteractionResponse(BaseModel):
    id: int
    user_id: int
    content_id: int
    interaction_type: str
    metadata: Dict = Field(validation_alias=AliasChoices("extra_metadata", "metadata"))
    created_at: datetime

    class Config:
        from_attributes = True


class FollowRequest(BaseModel):
    following_id: int


class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime = Field(validation_alias=AliasChoices("followed_at", "created_at"))
    follower_name: Optional[str] = None

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
    text: str = Field(validation_alias=AliasChoices("body", "text"))
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SearchIndexRequest(BaseModel):
    content_id: int
    index_type: SearchIndexType
    title: str
    content: str
    metadata: Optional[Dict] = None
    embeddings: Optional[List[float]] = None


class SearchIndexResponse(BaseModel):
    id: int
    content_id: int
    index_type: str
    title: str
    content: str = Field(validation_alias=AliasChoices("description", "content"))
    metadata: Dict = Field(validation_alias=AliasChoices("extra_metadata", "metadata"))
    created_at: datetime = Field(validation_alias=AliasChoices("indexed_at", "created_at"))

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
    last_active: datetime = Field(validation_alias=AliasChoices("last_sync", "last_active"))
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationLogRequest(BaseModel):
    notification_type: PushNotificationType
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
    action_type: AdminActionType
    resource_type: str
    resource_id: int
    details: Optional[Dict] = None


class AdminActionLogResponse(BaseModel):
    id: int
    admin_user_id: int = Field(validation_alias=AliasChoices("admin_id", "admin_user_id"))
    action_type: str
    resource_type: str = Field(validation_alias=AliasChoices("target_type", "resource_type"))
    resource_id: Optional[int] = Field(default=None, validation_alias=AliasChoices("target_id", "resource_id"))
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




@router.post("/interactions", response_model=InteractionResponse, status_code=201)
async def create_interaction(
    request: InteractionRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.create_interaction(
        db, _acting_user_id(user_id, current_user), request.content_id, request.interaction_type, request.metadata
    )


@router.get("/interactions/{content_id}", response_model=List[InteractionResponse])
async def get_content_interactions(
    content_id: int,
    interaction_type: Optional[InteractionType] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.get_content_interactions(db, content_id, interaction_type)


@router.get("/my-interactions", response_model=List[InteractionResponse])
async def get_my_interactions(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.get_user_interactions(db, _acting_user_id(user_id, current_user), limit, offset)


@router.delete("/interactions/{content_id}")
async def remove_interaction(
    content_id: int,
    interaction_type: InteractionType = Query(...),
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await SocialService.remove_interaction(db, _acting_user_id(user_id, current_user), content_id, interaction_type)
    return {"success": success}


@router.post("/follow", response_model=FollowResponse, status_code=201)
async def follow_user(
    request: FollowRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.follow_user(db, _acting_user_id(user_id, current_user), request.following_id)


@router.delete("/follow/{following_id}")
async def unfollow_user(
    following_id: int,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await SocialService.unfollow_user(db, _acting_user_id(user_id, current_user), following_id)
    return {"success": success}


@router.get("/followers/{user_id}", response_model=List[FollowResponse])
async def get_followers(
    user_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    follows = await SocialService.get_followers(db, user_id, limit, offset)
    names = {}
    if follows:
        rows = await db.execute(
            select(User.id, func.concat(User.first_name, " ", User.last_name))
            .where(User.id.in_([follow.follower_id for follow in follows]))
        )
        names = dict(rows.all())
    return [
        FollowResponse(
            id=follow.id,
            follower_id=follow.follower_id,
            following_id=follow.following_id,
            followed_at=follow.followed_at,
            follower_name=(names.get(follow.follower_id) or "").strip() or None,
        )
        for follow in follows
    ]


@router.get("/following/{user_id}", response_model=List[FollowResponse])
async def get_following(
    user_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.get_following(db, user_id, limit, offset)


@router.post("/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    request: CommentRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.create_comment(
        db, _acting_user_id(user_id, current_user), request.content_id, request.text, request.parent_comment_id
    )


@router.get("/comments/{content_id}", response_model=List[CommentResponse])
async def get_comments(
    content_id: int,
    parent_comment_id: Optional[int] = None,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.get_comments(db, content_id, parent_comment_id, limit, offset)


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await SocialService.delete_comment(db, comment_id, _acting_user_id(user_id, current_user))
    return {"success": success}


@router.post("/messages", response_model=MessageResponse, status_code=201)
async def send_message(
    request: MessageRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.send_message(db, _acting_user_id(user_id, current_user), request.recipient_id, request.text)


@router.get("/conversations/{other_user_id}", response_model=List[MessageResponse])
async def get_conversation(
    other_user_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SocialService.get_conversation(db, _acting_user_id(user_id, current_user), other_user_id, limit, offset)


@router.post("/messages/{message_id}/read")
async def mark_message_read(
    message_id: int,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await SocialService.mark_message_read(db, message_id, _acting_user_id(user_id, current_user))
    return {"success": success}


@router.post("/search-index", response_model=SearchIndexResponse, status_code=201)
async def create_search_index(
    request: SearchIndexRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Add a record to the shared search index (platform administrators only)"""
    return await SearchService.create_search_index(
        db, request.content_id, request.index_type, request.title,
        request.content, request.metadata, request.embeddings
    )


@router.get("/search", response_model=List[SearchIndexResponse])
async def search_content(
    query: str = Query(...),
    index_type: Optional[SearchIndexType] = None,
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SearchService.search_content(db, query, index_type, limit, offset)


@router.post("/saved-searches", response_model=SavedSearchResponse, status_code=201)
async def save_search(
    request: SavedSearchRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SearchService.save_search(db, _acting_user_id(user_id, current_user), request.query, request.filters)


@router.get("/saved-searches", response_model=List[SavedSearchResponse])
async def get_saved_searches(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SearchService.get_saved_searches(db, _acting_user_id(user_id, current_user), limit, offset)


@router.delete("/saved-searches/{search_id}")
async def delete_saved_search(
    search_id: int,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await SearchService.delete_saved_search(db, search_id, _acting_user_id(user_id, current_user))
    return {"success": success}


@router.post("/devices/register", response_model=DeviceRegistrationResponse, status_code=201)
async def register_device(
    request: DeviceRegistrationRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await PushNotificationService.register_device(
        db, _acting_user_id(user_id, current_user), request.device_token, request.platform, request.device_name
    )


@router.delete("/devices/{device_id}")
async def unregister_device(
    device_id: int,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await PushNotificationService.unregister_device(db, device_id, _acting_user_id(user_id, current_user))
    return {"success": success}


@router.get("/devices", response_model=List[DeviceRegistrationResponse])
async def get_my_devices(
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await PushNotificationService.get_user_devices(db, _acting_user_id(user_id, current_user))


@router.post("/notifications/log", response_model=NotificationLogResponse, status_code=201)
async def log_notification(
    request: NotificationLogRequest,
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await PushNotificationService.log_notification(
        db, _acting_user_id(user_id, current_user), request.notification_type, request.title, request.body, request.device_id
    )


@router.put("/notifications/{log_id}/status", response_model=NotificationLogResponse)
async def update_notification_status(
    log_id: int,
    status: str = Query(...),
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record delivery status from the push provider (platform administrators only)"""
    return await PushNotificationService.update_notification_status(db, log_id, status)


@router.get("/notifications/logs", response_model=List[NotificationLogResponse])
async def get_notification_logs(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    user_id: Optional[int] = Query(None, description="Acting user ID; must be the caller"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await PushNotificationService.get_notification_logs(db, _acting_user_id(user_id, current_user), limit, offset)


@router.post("/admin/users", response_model=AdminUserResponse, status_code=201)
async def create_admin_user(
    request: AdminUserRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Make a user a platform administrator (platform administrators only)"""
    return await AdminService.create_admin_user(db, request.user_id, request.role, request.permissions)


@router.delete("/admin/users/{user_id}")
async def remove_admin_user(
    user_id: int,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    success = await AdminService.remove_admin_user(db, user_id)
    return {"success": success}


@router.get("/admin/users/{user_id}", response_model=AdminUserResponse)
async def get_admin_user(
    user_id: int,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    admin = await AdminService.get_admin_user(db, user_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return admin


@router.post("/admin/logs", response_model=AdminActionLogResponse, status_code=201)
async def log_admin_action(
    request: AdminActionLogRequest,
    admin_user_id: Optional[int] = Query(None, description="Acting admin user ID; must be the caller"),
    admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record an administrative action performed by the caller"""
    return await AdminService.log_admin_action(
        db, _acting_user_id(admin_user_id, admin), request.action_type, request.resource_type,
        request.resource_id, request.details
    )


@router.get("/admin/logs", response_model=List[AdminActionLogResponse])
async def get_admin_logs(
    admin_user_id: Optional[int] = None,
    action_type: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """The administrative action trail (platform administrators only)"""
    return await AdminService.get_admin_logs(db, admin_user_id, action_type, limit, offset)


@router.put("/admin/users/{user_id}/permissions", response_model=AdminUserResponse)
async def update_admin_permissions(
    user_id: int,
    permissions: List[str],
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    return await AdminService.update_admin_permissions(db, user_id, permissions)


@router.post("/system/notifications", response_model=SystemNotificationResponse, status_code=201)
async def create_system_notification(
    request: SystemNotificationRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Publish a system notification (platform administrators only)"""
    return await SystemService.create_system_notification(
        db, request.title, request.message, request.notification_type,
        request.target_users, request.metadata
    )


@router.get("/system/notifications", response_model=List[SystemNotificationResponse])
async def get_system_notifications(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SystemService.get_system_notifications(db, limit, offset)


@router.post("/statistics", response_model=PlatformStatisticResponse, status_code=201)
async def record_statistic(
    request: PlatformStatisticRequest,
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Record a platform metric (platform administrators only)"""
    return await SystemService.record_platform_statistic(
        db, request.metric_name, request.metric_value, request.metric_type, request.breakdown
    )


@router.get("/statistics", response_model=List[PlatformStatisticResponse])
async def get_statistics(
    metric_name: Optional[str] = None,
    days: int = Query(7, ge=1),
    limit: int = Query(100, le=1000),
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Recorded platform metrics (platform administrators only)"""
    return await SystemService.get_platform_statistics(db, metric_name, days, limit)


@router.get("/statistics/aggregated")
async def get_aggregated_statistics(
    metric_name: str = Query(...),
    days: int = Query(30, ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await SystemService.get_aggregated_statistics(db, metric_name, days)


@router.get("/dashboard-summary")
async def get_dashboard_summary(
    _admin: User = Depends(require_platform_admin),
    db: AsyncSession = Depends(get_db),
):
    """Platform-wide totals for the admin dashboard (platform administrators only)"""
    return await SystemService.get_dashboard_summary(db)
