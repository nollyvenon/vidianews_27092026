from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.analytics_reporting import (
    ReportType, SearchIndexStatus, CacheLevel
)
from app.services.analytics_reporting_service import (
    AnalyticsReportService,
    UserBehaviorService,
    HeatmapService,
    SearchService,
    CacheService,
    PerformanceService,
    AdminService,
    FeatureFlagService
)

# Request/Response Schemas

class AnalyticsReportRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    report_type: ReportType
    period_start: datetime
    period_end: datetime

class AnalyticsReportResponse(BaseModel):
    id: int
    name: str
    report_type: ReportType
    period_start: datetime
    period_end: datetime
    total_pageviews: int
    total_sessions: int
    unique_visitors: int
    avg_session_duration: float
    bounce_rate: float
    conversion_rate: float
    revenue: float
    created_at: datetime
    updated_at: datetime

class DailyAnalyticsResponse(BaseModel):
    date: datetime
    pageviews: int
    sessions: int
    unique_visitors: int
    bounce_rate: float

class TopContentResponse(BaseModel):
    content_id: int
    pageviews: int
    unique_visitors: int
    avg_time_on_page: float
    conversion_count: int

class UserEventRequest(BaseModel):
    user_id: int
    content_id: Optional[int] = None
    event_type: str = Field(..., min_length=1, max_length=50)
    event_data: dict = {}
    page_url: Optional[str] = None
    referrer: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None

class UserEventResponse(BaseModel):
    id: int
    user_id: int
    content_id: Optional[int]
    event_type: str
    event_data: dict
    page_url: Optional[str]
    timestamp: datetime

class UserBehaviorSummaryResponse(BaseModel):
    user_id: int
    total_events: int
    event_breakdown: dict
    last_event: Optional[datetime]
    most_common_event: Optional[str]

class HeatmapRequest(BaseModel):
    content_id: int
    heatmap_json: dict
    scroll_depth_percentiles: dict = {}
    click_zones: dict = {}
    exit_rate: float = 0.0

class HeatmapResponse(BaseModel):
    id: int
    content_id: int
    heatmap_json: dict
    scroll_depth_percentiles: dict
    click_zones: dict
    exit_rate: float
    last_updated: datetime

class SearchIndexRequest(BaseModel):
    content_id: int
    title: str = Field(..., min_length=1, max_length=255)
    summary: Optional[str] = None
    full_text: Optional[str] = None
    tags: List[str] = []
    categories: List[str] = []
    keywords: List[str] = []

class SearchIndexResponse(BaseModel):
    id: int
    content_id: int
    title: str
    summary: Optional[str]
    status: SearchIndexStatus
    indexed_at: Optional[datetime]
    created_at: datetime

class SearchResultResponse(BaseModel):
    content_id: int
    title: str
    summary: Optional[str]
    relevance_score: float
    tags: List[str]

class TrendingSearchResponse(BaseModel):
    query: str
    count: int
    result_count_avg: int
    click_through_rate: float

class CacheEntryRequest(BaseModel):
    key: str = Field(..., min_length=1, max_length=512)
    value: str
    cache_level: CacheLevel = CacheLevel.WARM
    ttl_seconds: int = 3600

class CacheEntryResponse(BaseModel):
    id: int
    key: str
    cache_level: CacheLevel
    ttl_seconds: int
    hits: int
    last_accessed: datetime
    created_at: datetime

class CacheStatsResponse(BaseModel):
    total_entries: int
    hot_entries: int
    warm_entries: int
    cold_entries: int
    total_hits: int
    avg_hits_per_entry: float
    hit_rate: float

class PerformanceMetricRequest(BaseModel):
    endpoint: str = Field(..., min_length=1, max_length=255)
    method: str = Field(..., min_length=3, max_length=10)
    response_time_ms: int
    status_code: int
    request_size: int = 0
    response_size: int = 0

class PerformanceMetricResponse(BaseModel):
    id: int
    endpoint: str
    method: str
    response_time_ms: int
    status_code: int
    timestamp: datetime

class EndpointStatsResponse(BaseModel):
    endpoint: str
    method: str
    request_count: int
    avg_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    error_rate: float
    status_breakdown: dict

class AdminActionRequest(BaseModel):
    admin_id: int
    action: str = Field(..., min_length=1, max_length=100)
    resource_type: str = Field(..., min_length=1, max_length=50)
    resource_id: Optional[int] = None
    changes: dict = {}
    ip_address: Optional[str] = None

class AdminActionResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    resource_type: str
    resource_id: Optional[int]
    changes: dict
    ip_address: Optional[str]
    timestamp: datetime

class AuditLogResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    resource_type: str
    changes: dict
    timestamp: datetime

class HealthCheckResponse(BaseModel):
    service_name: str
    status: str
    response_time_ms: Optional[int]
    uptime_percentage: float
    error_count: int
    last_check: datetime

class SystemHealthResponse(BaseModel):
    overall_status: str
    timestamp: datetime
    services: List[HealthCheckResponse]
    total_uptime: float

class ConfigurationSettingRequest(BaseModel):
    key: str = Field(..., min_length=1, max_length=255)
    value: str
    setting_type: str = "string"
    description: Optional[str] = None

class ConfigurationSettingResponse(BaseModel):
    id: int
    key: str
    value: str
    setting_type: str
    description: Optional[str]
    updated_at: datetime

class FeatureFlagRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    enabled: bool = False
    rollout_percentage: int = Field(0, ge=0, le=100)
    target_segments: List[str] = []

class FeatureFlagResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    enabled: bool
    rollout_percentage: int
    target_segments: List[str]
    created_at: datetime
    updated_at: datetime

# Initialize routers

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])
behavior_router = APIRouter(prefix="/behavior", tags=["behavior"])
heatmap_router = APIRouter(prefix="/heatmaps", tags=["heatmaps"])
search_router = APIRouter(prefix="/search", tags=["search"])
cache_router = APIRouter(prefix="/cache", tags=["cache"])
performance_router = APIRouter(prefix="/performance", tags=["performance"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])
featureflag_router = APIRouter(prefix="/feature-flags", tags=["feature-flags"])

# Analytics Endpoints

@analytics_router.post("/reports", response_model=AnalyticsReportResponse)
async def create_analytics_report(
    request: AnalyticsReportRequest,
    service: AnalyticsReportService = Depends()
):
    """Create analytics report for period"""
    return await service.generate_report(
        name=request.name,
        report_type=request.report_type,
        period_start=request.period_start,
        period_end=request.period_end
    )

@analytics_router.get("/reports/{report_id}", response_model=AnalyticsReportResponse)
async def get_analytics_report(
    report_id: int,
    service: AnalyticsReportService = Depends()
):
    """Get analytics report by ID"""
    report = await service.get_analytics_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@analytics_router.get("/daily", response_model=List[DailyAnalyticsResponse])
async def get_daily_analytics(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    service: AnalyticsReportService = Depends()
):
    """Get daily analytics for date range"""
    return await service.get_daily_analytics(start_date, end_date)

@analytics_router.get("/top-content", response_model=List[TopContentResponse])
async def get_top_content(
    limit: int = Query(10, ge=1, le=100),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    service: AnalyticsReportService = Depends()
):
    """Get top content by pageviews"""
    return await service.get_top_content(
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )

# User Behavior Endpoints

@behavior_router.post("/events", response_model=UserEventResponse)
async def record_user_event(
    request: UserEventRequest,
    service: UserBehaviorService = Depends()
):
    """Record user behavior event"""
    return await service.record_event(
        user_id=request.user_id,
        content_id=request.content_id,
        event_type=request.event_type,
        event_data=request.event_data,
        page_url=request.page_url,
        referrer=request.referrer,
        device_type=request.device_type,
        browser=request.browser,
        os=request.os
    )

@behavior_router.get("/users/{user_id}/summary", response_model=UserBehaviorSummaryResponse)
async def get_user_behavior_summary(
    user_id: int,
    service: UserBehaviorService = Depends()
):
    """Get user behavior summary"""
    summary = await service.get_user_behavior_summary(user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="User behavior not found")
    return summary

@behavior_router.get("/users/{user_id}/events", response_model=List[UserEventResponse])
async def get_user_events(
    user_id: int,
    limit: int = Query(100, ge=1, le=1000),
    service: UserBehaviorService = Depends()
):
    """Get user events"""
    return await service.get_user_events(user_id, limit)

# Heatmap Endpoints

@heatmap_router.post("", response_model=HeatmapResponse)
async def create_heatmap(
    request: HeatmapRequest,
    service: HeatmapService = Depends()
):
    """Create or update heatmap for content"""
    return await service.create_heatmap(
        content_id=request.content_id,
        heatmap_json=request.heatmap_json,
        scroll_depth_percentiles=request.scroll_depth_percentiles,
        click_zones=request.click_zones,
        exit_rate=request.exit_rate
    )

@heatmap_router.get("/{content_id}", response_model=HeatmapResponse)
async def get_heatmap(
    content_id: int,
    service: HeatmapService = Depends()
):
    """Get heatmap for content"""
    heatmap = await service.get_heatmap(content_id)
    if not heatmap:
        raise HTTPException(status_code=404, detail="Heatmap not found")
    return heatmap

# Search Endpoints

@search_router.post("/index", response_model=SearchIndexResponse)
async def index_content(
    request: SearchIndexRequest,
    service: SearchService = Depends()
):
    """Index content for search"""
    return await service.index_content(
        content_id=request.content_id,
        title=request.title,
        summary=request.summary,
        full_text=request.full_text,
        tags=request.tags,
        categories=request.categories,
        keywords=request.keywords
    )

@search_router.get("/results", response_model=List[SearchResultResponse])
async def search_content(
    query: str = Query(..., min_length=1, max_length=255),
    limit: int = Query(20, ge=1, le=100),
    service: SearchService = Depends()
):
    """Search indexed content"""
    return await service.search(query, limit)

@search_router.get("/queries/{query_id}", response_model=dict)
async def get_search_query(
    query_id: int,
    service: SearchService = Depends()
):
    """Get search query details"""
    query = await service.get_search_query(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Search query not found")
    return query

@search_router.get("/trending", response_model=List[TrendingSearchResponse])
async def get_trending_searches(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(10, ge=1, le=100),
    service: SearchService = Depends()
):
    """Get trending searches"""
    return await service.get_trending_searches(days, limit)

@search_router.get("/indexed/{content_id}", response_model=SearchIndexResponse)
async def get_indexed_content(
    content_id: int,
    service: SearchService = Depends()
):
    """Get indexed content status"""
    indexed = await service.get_indexed_content(content_id)
    if not indexed:
        raise HTTPException(status_code=404, detail="Content not indexed")
    return indexed

# Cache Endpoints

@cache_router.post("", response_model=CacheEntryResponse)
async def set_cache(
    request: CacheEntryRequest,
    service: CacheService = Depends()
):
    """Set cache entry"""
    return await service.set_cache(
        key=request.key,
        value=request.value,
        cache_level=request.cache_level,
        ttl_seconds=request.ttl_seconds
    )

@cache_router.get("/{cache_key}", response_model=CacheEntryResponse)
async def get_cache(
    cache_key: str,
    service: CacheService = Depends()
):
    """Get cache entry"""
    entry = await service.get_cache(cache_key)
    if not entry:
        raise HTTPException(status_code=404, detail="Cache entry not found")
    return entry

@cache_router.delete("/{cache_key}")
async def delete_cache(
    cache_key: str,
    service: CacheService = Depends()
):
    """Clear cache entry"""
    await service.delete_cache(cache_key)
    return {"status": "deleted"}

@cache_router.post("/clear-all")
async def clear_all_cache(
    service: CacheService = Depends()
):
    """Clear all cache"""
    await service.clear_cache()
    return {"status": "all_cache_cleared"}

@cache_router.get("/stats/summary", response_model=CacheStatsResponse)
async def get_cache_stats(
    service: CacheService = Depends()
):
    """Get cache statistics"""
    return await service.get_cache_stats()

# Performance Endpoints

@performance_router.post("/metrics", response_model=PerformanceMetricResponse)
async def record_performance_metric(
    request: PerformanceMetricRequest,
    service: PerformanceService = Depends()
):
    """Record endpoint performance metric"""
    return await service.record_metric(
        endpoint=request.endpoint,
        method=request.method,
        response_time_ms=request.response_time_ms,
        status_code=request.status_code,
        request_size=request.request_size,
        response_size=request.response_size
    )

@performance_router.get("/endpoints/{endpoint_path}", response_model=EndpointStatsResponse)
async def get_endpoint_stats(
    endpoint_path: str,
    method: str = Query(..., min_length=3, max_length=10),
    service: PerformanceService = Depends()
):
    """Get endpoint performance statistics"""
    stats = await service.get_endpoint_stats(endpoint_path, method)
    if not stats:
        raise HTTPException(status_code=404, detail="Endpoint stats not found")
    return stats

@performance_router.get("/summary", response_model=dict)
async def get_performance_summary(
    service: PerformanceService = Depends()
):
    """Get overall performance summary"""
    return await service.get_performance_summary()

# Admin Endpoints

@admin_router.post("/actions", response_model=AdminActionResponse)
async def log_admin_action(
    request: AdminActionRequest,
    service: AdminService = Depends()
):
    """Log admin action"""
    return await service.log_admin_action(
        admin_id=request.admin_id,
        action=request.action,
        resource_type=request.resource_type,
        resource_id=request.resource_id,
        changes=request.changes,
        ip_address=request.ip_address
    )

@admin_router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    admin_id: Optional[int] = None,
    service: AdminService = Depends()
):
    """Get audit logs"""
    return await service.get_audit_logs(limit, offset, admin_id)

@admin_router.get("/audit-logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    service: AdminService = Depends()
):
    """Get specific audit log"""
    log = await service.get_audit_log(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log

@admin_router.get("/health", response_model=SystemHealthResponse)
async def check_system_health(
    service: AdminService = Depends()
):
    """Check overall system health"""
    return await service.check_system_health()

@admin_router.get("/health/{service_name}", response_model=HealthCheckResponse)
async def check_service_health(
    service_name: str,
    service: AdminService = Depends()
):
    """Check specific service health"""
    health = await service.get_service_health(service_name)
    if not health:
        raise HTTPException(status_code=404, detail="Service not found")
    return health

@admin_router.post("/health/{service_name}")
async def update_service_health(
    service_name: str,
    status: str = Query(..., regex="^(healthy|degraded|unhealthy)$"),
    response_time_ms: Optional[int] = None,
    error_count: int = 0,
    service: AdminService = Depends()
):
    """Update service health status"""
    return await service.update_service_health(
        service_name, status, response_time_ms, error_count
    )

# Configuration Endpoints

@admin_router.post("/config", response_model=ConfigurationSettingResponse)
async def set_configuration(
    request: ConfigurationSettingRequest,
    service: AdminService = Depends()
):
    """Set configuration setting"""
    return await service.set_configuration(
        key=request.key,
        value=request.value,
        setting_type=request.setting_type,
        description=request.description
    )

@admin_router.get("/config/{config_key}", response_model=ConfigurationSettingResponse)
async def get_configuration(
    config_key: str,
    service: AdminService = Depends()
):
    """Get configuration setting"""
    config = await service.get_configuration(config_key)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@admin_router.get("/config", response_model=List[ConfigurationSettingResponse])
async def list_configurations(
    service: AdminService = Depends()
):
    """List all configurations"""
    return await service.list_configurations()

@admin_router.delete("/config/{config_key}")
async def delete_configuration(
    config_key: str,
    service: AdminService = Depends()
):
    """Delete configuration setting"""
    await service.delete_configuration(config_key)
    return {"status": "deleted"}

# Feature Flag Endpoints

@featureflag_router.post("", response_model=FeatureFlagResponse)
async def create_feature_flag(
    request: FeatureFlagRequest,
    service: FeatureFlagService = Depends()
):
    """Create feature flag"""
    return await service.create_feature_flag(
        name=request.name,
        description=request.description,
        enabled=request.enabled,
        rollout_percentage=request.rollout_percentage,
        target_segments=request.target_segments
    )

@featureflag_router.get("/{flag_name}", response_model=FeatureFlagResponse)
async def get_feature_flag(
    flag_name: str,
    service: FeatureFlagService = Depends()
):
    """Get feature flag"""
    flag = await service.get_feature_flag(flag_name)
    if not flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    return flag

@featureflag_router.get("/{flag_name}/enabled", response_model=dict)
async def is_feature_enabled(
    flag_name: str,
    user_id: Optional[int] = None,
    service: FeatureFlagService = Depends()
):
    """Check if feature is enabled for user"""
    enabled = await service.is_feature_enabled(flag_name, user_id)
    return {"flag_name": flag_name, "enabled": enabled}

@featureflag_router.patch("/{flag_id}", response_model=FeatureFlagResponse)
async def update_feature_flag(
    flag_id: int,
    request: FeatureFlagRequest,
    service: FeatureFlagService = Depends()
):
    """Update feature flag"""
    return await service.update_feature_flag(
        flag_id,
        name=request.name,
        description=request.description,
        enabled=request.enabled,
        rollout_percentage=request.rollout_percentage,
        target_segments=request.target_segments
    )

@featureflag_router.delete("/{flag_id}")
async def delete_feature_flag(
    flag_id: int,
    service: FeatureFlagService = Depends()
):
    """Delete feature flag"""
    await service.delete_feature_flag(flag_id)
    return {"status": "deleted"}

@featureflag_router.get("", response_model=List[FeatureFlagResponse])
async def list_feature_flags(
    service: FeatureFlagService = Depends()
):
    """List all feature flags"""
    return await service.list_feature_flags()
