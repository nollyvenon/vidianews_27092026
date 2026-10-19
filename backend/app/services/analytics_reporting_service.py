"""Analytics, behaviour, search, cache, performance, admin and feature-flag services.

Every service receives the database session in its constructor. Methods return ORM
rows (so callers can read columns as attributes) or small dataclasses for computed
results. Routers wire the session in through ``Depends(get_db)``.
"""

import hashlib
import math
import statistics
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, delete, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics_reporting import (
    AdminAuditLog,
    AnalyticsReport,
    CacheEntry,
    CacheLevel,
    ConfigurationSetting,
    FeatureFlag,
    HeatmapData,
    PageViewMetrics,
    PerformanceMetric,
    ReportType,
    SearchIndex,
    SearchIndexStatus,
    SearchQuery,
    SystemHealthCheck,
    UserBehaviorEvent,
)

HEALTH_STATUSES = ("healthy", "degraded", "unhealthy")


def _utcnow() -> datetime:
    """Naive UTC timestamp, matching how the analytics columns are written."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _check_period(start: datetime, end: datetime) -> None:
    if start > end:
        raise ValueError("period_start must be before or equal to period_end")


def _percentile(values: List[float], pct: float) -> float:
    """Nearest-rank percentile (pct in 0-100). Returns 0.0 for an empty list."""
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(1, math.ceil(pct / 100 * len(ordered)))
    return float(ordered[rank - 1])


# ---------------------------------------------------------------- result types


@dataclass
class UserBehaviorSummary:
    user_id: int
    total_events: int
    event_breakdown: Dict[str, int]
    device_types: List[str]
    last_event: Optional[datetime]
    most_common_event: Optional[str]


@dataclass
class SearchResult:
    content_id: int
    title: str
    summary: Optional[str]
    relevance_score: float
    tags: List[str]


@dataclass
class TrendingSearch:
    query: str
    count: int
    result_count_avg: int
    click_through_rate: float


@dataclass
class CacheStats:
    total_entries: int
    hot_entries: int
    warm_entries: int
    cold_entries: int
    total_hits: int
    avg_hits_per_entry: float
    hit_rate: float


@dataclass
class EndpointStats:
    endpoint: str
    method: str
    request_count: int
    avg_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    error_rate: float
    status_breakdown: Dict[str, int]


@dataclass
class SystemHealth:
    overall_status: str
    timestamp: datetime
    services: List[SystemHealthCheck]
    total_uptime: float


# ---------------------------------------------------------------- analytics


class AnalyticsReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_report(
        self,
        name: str,
        report_type: ReportType,
        period_start: datetime,
        period_end: datetime,
    ) -> AnalyticsReport:
        _check_period(period_start, period_end)
        result = await self.db.execute(
            select(PageViewMetrics).where(
                and_(
                    PageViewMetrics.date >= period_start,
                    PageViewMetrics.date <= period_end,
                )
            )
        )
        metrics = result.scalars().all()

        total_pageviews = sum(m.page_views or 0 for m in metrics)
        total_visitors = sum(m.unique_visitors or 0 for m in metrics)
        total_conversions = sum(m.conversion_count or 0 for m in metrics)
        bounce_rates = [m.bounce_rate for m in metrics if m.bounce_rate is not None]
        durations = [m.avg_time_on_page for m in metrics if m.avg_time_on_page is not None]

        report = AnalyticsReport(
            name=name,
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            total_pageviews=total_pageviews,
            total_sessions=len(metrics),
            unique_visitors=total_visitors,
            avg_session_duration=statistics.mean(durations) if durations else 0.0,
            bounce_rate=statistics.mean(bounce_rates) if bounce_rates else 0.0,
            conversion_rate=(total_conversions / total_pageviews * 100) if total_pageviews else 0.0,
            revenue=0,
        )
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def get_analytics_report(self, report_id: int) -> Optional[AnalyticsReport]:
        result = await self.db.execute(select(AnalyticsReport).where(AnalyticsReport.id == report_id))
        return result.scalar_one_or_none()

    async def get_daily_analytics(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        _check_period(start_date, end_date)
        result = await self.db.execute(
            select(PageViewMetrics).where(
                and_(PageViewMetrics.date >= start_date, PageViewMetrics.date <= end_date)
            )
        )
        by_day: Dict[datetime, List[PageViewMetrics]] = {}
        for metric in result.scalars().all():
            day = metric.date.replace(hour=0, minute=0, second=0, microsecond=0)
            by_day.setdefault(day, []).append(metric)

        rows = []
        for day in sorted(by_day):
            metrics = by_day[day]
            bounce_rates = [m.bounce_rate for m in metrics if m.bounce_rate is not None]
            rows.append(
                {
                    "date": day,
                    "pageviews": sum(m.page_views or 0 for m in metrics),
                    "sessions": len(metrics),
                    "unique_visitors": sum(m.unique_visitors or 0 for m in metrics),
                    "bounce_rate": statistics.mean(bounce_rates) if bounce_rates else 0.0,
                }
            )
        return rows

    async def get_top_content(
        self,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        query = select(PageViewMetrics)
        if start_date is not None or end_date is not None:
            if start_date is not None and end_date is not None:
                _check_period(start_date, end_date)
            if start_date is not None:
                query = query.where(PageViewMetrics.date >= start_date)
            if end_date is not None:
                query = query.where(PageViewMetrics.date <= end_date)
        else:
            query = query.where(PageViewMetrics.date >= _utcnow() - timedelta(days=days))

        result = await self.db.execute(query.order_by(desc(PageViewMetrics.page_views)).limit(limit))
        return [
            {
                "content_id": m.content_id,
                "pageviews": m.page_views or 0,
                "unique_visitors": m.unique_visitors or 0,
                "avg_time_on_page": m.avg_time_on_page or 0.0,
                "conversion_count": m.conversion_count or 0,
                "conversion_rate": (m.conversion_count or 0) / max(m.page_views or 0, 1) * 100,
            }
            for m in result.scalars().all()
        ]


# ---------------------------------------------------------------- behaviour


class UserBehaviorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_event(
        self,
        user_id: int,
        content_id: Optional[int] = None,
        event_type: Optional[str] = None,
        event_data: Optional[Dict[str, Any]] = None,
        page_url: Optional[str] = None,
        referrer: Optional[str] = None,
        device_type: Optional[str] = None,
        browser: Optional[str] = None,
        os: Optional[str] = None,
    ) -> UserBehaviorEvent:
        if not event_type:
            raise ValueError("event_type is required")
        event = UserBehaviorEvent(
            user_id=user_id,
            content_id=content_id,
            event_type=event_type,
            event_data=event_data or {},
            page_url=page_url,
            referrer=referrer,
            device_type=device_type,
            browser=browser,
            os=os,
            timestamp=_utcnow(),
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_user_events(self, user_id: int, limit: int = 100) -> List[UserBehaviorEvent]:
        result = await self.db.execute(
            select(UserBehaviorEvent)
            .where(UserBehaviorEvent.user_id == user_id)
            .order_by(desc(UserBehaviorEvent.timestamp))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_user_behavior_summary(self, user_id: int) -> UserBehaviorSummary:
        result = await self.db.execute(
            select(UserBehaviorEvent).where(UserBehaviorEvent.user_id == user_id)
        )
        events = result.scalars().all()

        breakdown: Dict[str, int] = {}
        for event in events:
            breakdown[event.event_type] = breakdown.get(event.event_type, 0) + 1

        most_common = max(breakdown, key=breakdown.get) if breakdown else None
        last = max((e.timestamp for e in events if e.timestamp), default=None)

        return UserBehaviorSummary(
            user_id=user_id,
            total_events=len(events),
            event_breakdown=breakdown,
            device_types=sorted({e.device_type for e in events if e.device_type}),
            last_event=last,
            most_common_event=most_common,
        )


# ---------------------------------------------------------------- heatmaps


class HeatmapService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_heatmap(
        self,
        content_id: int,
        heatmap_json: Dict[str, Any],
        scroll_depth_percentiles: Optional[Dict[str, Any]] = None,
        click_zones: Optional[Dict[str, Any]] = None,
        exit_rate: Optional[float] = None,
    ) -> HeatmapData:
        result = await self.db.execute(select(HeatmapData).where(HeatmapData.content_id == content_id))
        heatmap = result.scalar_one_or_none()

        if heatmap is None:
            heatmap = HeatmapData(content_id=content_id)
            self.db.add(heatmap)

        heatmap.heatmap_json = heatmap_json
        heatmap.scroll_depth_percentiles = scroll_depth_percentiles or {}
        heatmap.click_zones = click_zones or {}
        heatmap.exit_rate = exit_rate if exit_rate is not None else (heatmap.exit_rate or 0.0)
        heatmap.last_updated = _utcnow()

        await self.db.commit()
        await self.db.refresh(heatmap)
        return heatmap

    async def get_heatmap(self, content_id: int) -> Optional[HeatmapData]:
        result = await self.db.execute(select(HeatmapData).where(HeatmapData.content_id == content_id))
        return result.scalar_one_or_none()


# ---------------------------------------------------------------- search


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def index_content(
        self,
        content_id: int,
        title: str,
        summary: Optional[str] = None,
        full_text: Optional[str] = None,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
    ) -> SearchIndex:
        result = await self.db.execute(select(SearchIndex).where(SearchIndex.content_id == content_id))
        entry = result.scalar_one_or_none()

        if entry is None:
            entry = SearchIndex(content_id=content_id, created_at=_utcnow())
            self.db.add(entry)

        entry.title = title
        entry.summary = summary
        entry.full_text = full_text
        entry.tags = tags or []
        entry.categories = categories or []
        entry.keywords = keywords or []
        entry.status = SearchIndexStatus.INDEXED
        entry.indexed_at = _utcnow()

        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def search(self, query: str, limit: int = 20, user_id: Optional[int] = None) -> List[SearchResult]:
        term = f"%{query}%"
        result = await self.db.execute(
            select(SearchIndex).where(
                or_(
                    SearchIndex.title.ilike(term),
                    SearchIndex.full_text.ilike(term),
                    SearchIndex.summary.ilike(term),
                    SearchIndex.tags.contains([query]),
                    SearchIndex.keywords.contains([query]),
                )
            )
        )
        matches = result.scalars().all()

        ranked = sorted(
            (
                SearchResult(
                    content_id=entry.content_id,
                    title=entry.title,
                    summary=entry.summary,
                    relevance_score=self._relevance(query, entry),
                    tags=list(entry.tags or []),
                )
                for entry in matches
            ),
            key=lambda item: item.relevance_score,
            reverse=True,
        )[:limit]

        self.db.add(SearchQuery(user_id=user_id, query=query, result_count=len(matches), created_at=_utcnow()))
        await self.db.commit()
        return ranked

    @staticmethod
    def _relevance(query: str, entry: SearchIndex) -> float:
        """Weighted match score in [0, 1]: title 0.6, summary/body 0.3, tags/keywords 0.1."""
        needle = query.lower()
        score = 0.0
        if needle in (entry.title or "").lower():
            score += 0.6
        if needle in (entry.summary or "").lower() or needle in (entry.full_text or "").lower():
            score += 0.3
        terms = [t.lower() for t in (entry.tags or []) + (entry.keywords or [])]
        if needle in terms:
            score += 0.1
        return min(score, 1.0)

    async def get_search_query(self, query_id: int) -> Optional[SearchQuery]:
        result = await self.db.execute(select(SearchQuery).where(SearchQuery.id == query_id))
        return result.scalar_one_or_none()

    async def get_indexed_content(self, content_id: int) -> Optional[SearchIndex]:
        result = await self.db.execute(select(SearchIndex).where(SearchIndex.content_id == content_id))
        return result.scalar_one_or_none()

    async def get_trending_searches(self, days: int = 7, limit: int = 10) -> List[TrendingSearch]:
        cutoff = _utcnow() - timedelta(days=days)
        count_col = func.count(SearchQuery.id).label("count")
        result = await self.db.execute(
            select(
                SearchQuery.query,
                count_col,
                func.avg(SearchQuery.result_count),
                func.count(SearchQuery.clicked_result),
            )
            .where(SearchQuery.created_at >= cutoff)
            .group_by(SearchQuery.query)
            .order_by(desc(count_col))
            .limit(limit)
        )
        trending = []
        for query, count, avg_results, clicks in result.all():
            trending.append(
                TrendingSearch(
                    query=query,
                    count=int(count),
                    result_count_avg=int(round(avg_results or 0)),
                    click_through_rate=(clicks / count) if count else 0.0,
                )
            )
        return trending


# ---------------------------------------------------------------- cache


class CacheService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def set_cache(
        self,
        key: str,
        value: str,
        ttl_seconds: int = 3600,
        cache_level: CacheLevel = CacheLevel.WARM,
    ) -> CacheEntry:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        result = await self.db.execute(select(CacheEntry).where(CacheEntry.key == key))
        entry = result.scalar_one_or_none()

        now = _utcnow()
        if entry is None:
            entry = CacheEntry(key=key, created_at=now, last_accessed=now, hits=0)
            self.db.add(entry)
        entry.value = value
        entry.ttl_seconds = ttl_seconds
        entry.cache_level = cache_level

        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def get_cache(self, key: str) -> Optional[CacheEntry]:
        result = await self.db.execute(select(CacheEntry).where(CacheEntry.key == key))
        entry = result.scalar_one_or_none()
        if entry is None:
            return None
        entry.hits = (entry.hits or 0) + 1
        entry.last_accessed = _utcnow()
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def delete_cache(self, key: str) -> bool:
        result = await self.db.execute(select(CacheEntry).where(CacheEntry.key == key))
        entry = result.scalar_one_or_none()
        if entry is None:
            return False
        await self.db.delete(entry)
        await self.db.commit()
        return True

    async def clear_cache(self) -> int:
        result = await self.db.execute(select(CacheEntry))
        entries = result.scalars().all()
        for entry in entries:
            await self.db.delete(entry)
        await self.db.commit()
        return len(entries)

    async def get_cache_stats(self) -> CacheStats:
        result = await self.db.execute(select(CacheEntry))
        entries = result.scalars().all()

        total_hits = sum(e.hits or 0 for e in entries)
        levels = [e.cache_level for e in entries]
        return CacheStats(
            total_entries=len(entries),
            hot_entries=levels.count(CacheLevel.HOT),
            warm_entries=levels.count(CacheLevel.WARM),
            cold_entries=levels.count(CacheLevel.COLD),
            total_hits=total_hits,
            avg_hits_per_entry=total_hits / len(entries) if entries else 0.0,
            hit_rate=(len([e for e in entries if (e.hits or 0) > 0]) / len(entries)) if entries else 0.0,
        )


    async def flush(self) -> int:
        """Remove every cache entry; returns how many were removed."""
        result = await self.db.execute(delete(CacheEntry))
        await self.db.commit()
        return result.rowcount or 0

    async def optimize(self) -> Dict[str, int]:
        """Remove entries whose time-to-live has passed; returns the removed and remaining counts."""
        entries = (await self.db.execute(select(CacheEntry))).scalars().all()
        now = _utcnow()
        expired = [e.id for e in entries if e.created_at and e.created_at + timedelta(seconds=e.ttl_seconds) <= now]
        if expired:
            await self.db.execute(delete(CacheEntry).where(CacheEntry.id.in_(expired)))
            await self.db.commit()
        return {"removed": len(expired), "remaining": len(entries) - len(expired)}


# ---------------------------------------------------------------- performance


class PerformanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_metric(
        self,
        endpoint: str,
        method: str,
        response_time_ms: int,
        status_code: int,
        request_size: int = 0,
        response_size: int = 0,
    ) -> PerformanceMetric:
        if response_time_ms < 0:
            raise ValueError("response_time_ms cannot be negative")
        metric = PerformanceMetric(
            endpoint=endpoint,
            method=method.upper(),
            response_time_ms=response_time_ms,
            status_code=status_code,
            request_size=request_size,
            response_size=response_size,
            timestamp=_utcnow(),
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_endpoint_stats(self, endpoint: str, method: str, hours: int = 24) -> EndpointStats:
        cutoff = _utcnow() - timedelta(hours=hours)
        result = await self.db.execute(
            select(PerformanceMetric).where(
                and_(
                    PerformanceMetric.endpoint == endpoint,
                    PerformanceMetric.method == method.upper(),
                    PerformanceMetric.timestamp >= cutoff,
                )
            )
        )
        metrics = result.scalars().all()

        times = [float(m.response_time_ms or 0) for m in metrics]
        breakdown: Dict[str, int] = {}
        for m in metrics:
            key = str(m.status_code)
            breakdown[key] = breakdown.get(key, 0) + 1
        errors = len([m for m in metrics if (m.status_code or 0) >= 400])

        return EndpointStats(
            endpoint=endpoint,
            method=method.upper(),
            request_count=len(metrics),
            avg_response_time_ms=statistics.mean(times) if times else 0.0,
            p95_response_time_ms=_percentile(times, 95),
            p99_response_time_ms=_percentile(times, 99),
            error_rate=(errors / len(metrics)) if metrics else 0.0,
            status_breakdown=breakdown,
        )

    async def get_performance_summary(self) -> Dict[str, Any]:
        cutoff = _utcnow() - timedelta(hours=24)
        result = await self.db.execute(select(PerformanceMetric).where(PerformanceMetric.timestamp >= cutoff))
        metrics = result.scalars().all()
        times = [float(m.response_time_ms or 0) for m in metrics]
        errors = len([m for m in metrics if (m.status_code or 0) >= 400])
        return {
            "window_hours": 24,
            "total_requests": len(metrics),
            "avg_response_time_ms": statistics.mean(times) if times else 0.0,
            "p95_response_time_ms": _percentile(times, 95),
            "error_rate": (errors / len(metrics)) if metrics else 0.0,
        }


# ---------------------------------------------------------------- admin


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_admin_action(
        self,
        admin_id: int,
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        changes: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
    ) -> AdminAuditLog:
        log = AdminAuditLog(
            admin_id=admin_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes or {},
            ip_address=ip_address,
            timestamp=_utcnow(),
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def get_audit_logs(
        self,
        limit: int = 100,
        offset: int = 0,
        admin_id: Optional[int] = None,
        days: Optional[int] = None,
    ) -> List[AdminAuditLog]:
        query = select(AdminAuditLog)
        if admin_id is not None:
            query = query.where(AdminAuditLog.admin_id == admin_id)
        if days is not None:
            query = query.where(AdminAuditLog.timestamp >= _utcnow() - timedelta(days=days))
        result = await self.db.execute(query.order_by(desc(AdminAuditLog.timestamp)).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def get_audit_log(self, log_id: int) -> Optional[AdminAuditLog]:
        result = await self.db.execute(select(AdminAuditLog).where(AdminAuditLog.id == log_id))
        return result.scalar_one_or_none()

    async def update_service_health(
        self,
        service_name: str,
        status: str,
        response_time_ms: Optional[int] = None,
        error_count: int = 0,
    ) -> SystemHealthCheck:
        if status not in HEALTH_STATUSES:
            raise ValueError(f"status must be one of {HEALTH_STATUSES}")
        result = await self.db.execute(
            select(SystemHealthCheck).where(SystemHealthCheck.service_name == service_name)
        )
        check = result.scalar_one_or_none()
        if check is None:
            check = SystemHealthCheck(service_name=service_name, uptime_percentage=100.0, error_count=0)
            self.db.add(check)
        check.status = status
        check.response_time_ms = response_time_ms
        check.error_count = (check.error_count or 0) + error_count
        check.last_check = _utcnow()

        await self.db.commit()
        await self.db.refresh(check)
        return check

    async def get_service_health(self, service_name: str) -> Optional[SystemHealthCheck]:
        result = await self.db.execute(
            select(SystemHealthCheck).where(SystemHealthCheck.service_name == service_name)
        )
        return result.scalar_one_or_none()

    async def check_system_health(self) -> SystemHealth:
        result = await self.db.execute(select(SystemHealthCheck).order_by(SystemHealthCheck.service_name))
        services = list(result.scalars().all())
        statuses = {s.status for s in services}
        if "unhealthy" in statuses:
            overall = "unhealthy"
        elif "degraded" in statuses:
            overall = "degraded"
        else:
            overall = "healthy"
        uptimes = [s.uptime_percentage for s in services if s.uptime_percentage is not None]
        return SystemHealth(
            overall_status=overall,
            timestamp=_utcnow(),
            services=services,
            total_uptime=statistics.mean(uptimes) if uptimes else 0.0,
        )

    async def get_system_health(self) -> Dict[str, Any]:
        result = await self.db.execute(select(SystemHealthCheck))
        checks = result.scalars().all()
        return {
            "total_services": len(checks),
            "healthy": len([c for c in checks if c.status == "healthy"]),
            "degraded": len([c for c in checks if c.status == "degraded"]),
            "unhealthy": len([c for c in checks if c.status == "unhealthy"]),
            "overall_status": (
                "unhealthy"
                if any(c.status == "unhealthy" for c in checks)
                else "degraded"
                if any(c.status == "degraded" for c in checks)
                else "healthy"
            ),
        }

    async def set_configuration(
        self,
        key: str,
        value: str,
        setting_type: str = "string",
        description: Optional[str] = None,
        updated_by: Optional[int] = None,
    ) -> ConfigurationSetting:
        result = await self.db.execute(select(ConfigurationSetting).where(ConfigurationSetting.key == key))
        setting = result.scalar_one_or_none()
        if setting is None:
            setting = ConfigurationSetting(key=key)
            self.db.add(setting)
        setting.value = value
        setting.setting_type = setting_type
        setting.description = description
        setting.updated_by = updated_by
        setting.updated_at = _utcnow()
        await self.db.commit()
        await self.db.refresh(setting)
        return setting

    async def get_configuration(self, key: str) -> Optional[ConfigurationSetting]:
        result = await self.db.execute(select(ConfigurationSetting).where(ConfigurationSetting.key == key))
        return result.scalar_one_or_none()

    async def list_configurations(self) -> List[ConfigurationSetting]:
        result = await self.db.execute(select(ConfigurationSetting).order_by(ConfigurationSetting.key))
        return list(result.scalars().all())

    async def delete_configuration(self, key: str) -> bool:
        setting = await self.get_configuration(key)
        if setting is None:
            return False
        await self.db.delete(setting)
        await self.db.commit()
        return True


# ---------------------------------------------------------------- feature flags


def _check_rollout(rollout_percentage: int) -> None:
    if not 0 <= rollout_percentage <= 100:
        raise ValueError("rollout_percentage must be between 0 and 100")


class FeatureFlagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_feature_flag(
        self,
        name: str,
        description: Optional[str] = None,
        enabled: bool = False,
        rollout_percentage: int = 0,
        target_segments: Optional[List[str]] = None,
    ) -> FeatureFlag:
        _check_rollout(rollout_percentage)
        if await self.get_feature_flag(name) is not None:
            raise ValueError(f"Feature flag '{name}' already exists")
        flag = FeatureFlag(
            name=name,
            description=description,
            enabled=enabled,
            rollout_percentage=rollout_percentage,
            target_segments=target_segments or [],
            created_at=_utcnow(),
            updated_at=_utcnow(),
        )
        self.db.add(flag)
        await self.db.commit()
        await self.db.refresh(flag)
        return flag

    async def get_feature_flag(self, name: str) -> Optional[FeatureFlag]:
        result = await self.db.execute(select(FeatureFlag).where(FeatureFlag.name == name))
        return result.scalar_one_or_none()

    async def list_feature_flags(self) -> List[FeatureFlag]:
        result = await self.db.execute(select(FeatureFlag).order_by(FeatureFlag.name))
        return list(result.scalars().all())

    async def is_feature_enabled(self, feature_name: str, user_id: Optional[int] = None) -> bool:
        flag = await self.get_feature_flag(feature_name)
        if flag is None or not flag.enabled:
            return False
        if flag.rollout_percentage < 100 and user_id is not None:
            # Deterministic bucket per (user, feature) so a user always gets the same answer.
            digest = hashlib.md5(f"{user_id}{feature_name}".encode(), usedforsecurity=False).hexdigest()
            return (int(digest, 16) % 100) < flag.rollout_percentage
        return True

    async def update_feature_flag(
        self,
        flag_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
        rollout_percentage: Optional[int] = None,
        target_segments: Optional[List[str]] = None,
    ) -> FeatureFlag:
        result = await self.db.execute(select(FeatureFlag).where(FeatureFlag.id == flag_id))
        flag = result.scalar_one_or_none()
        if flag is None:
            raise ValueError(f"Feature flag {flag_id} not found")
        if rollout_percentage is not None:
            _check_rollout(rollout_percentage)
            flag.rollout_percentage = rollout_percentage
        if name is not None:
            flag.name = name
        if description is not None:
            flag.description = description
        if enabled is not None:
            flag.enabled = enabled
        if target_segments is not None:
            flag.target_segments = target_segments
        flag.updated_at = _utcnow()
        await self.db.commit()
        await self.db.refresh(flag)
        return flag

    async def delete_feature_flag(self, flag_id: int) -> bool:
        result = await self.db.execute(select(FeatureFlag).where(FeatureFlag.id == flag_id))
        flag = result.scalar_one_or_none()
        if flag is None:
            return False
        await self.db.delete(flag)
        await self.db.commit()
        return True
