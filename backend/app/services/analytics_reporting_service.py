from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import statistics
import hashlib
from app.models.analytics_reporting import (
    AnalyticsReport, PageViewMetrics, UserBehaviorEvent, HeatmapData,
    SearchIndex, SearchQuery, CacheEntry, PerformanceMetric, SystemLog,
    AdminAuditLog, SystemHealthCheck, ConfigurationSetting, FeatureFlag,
    ReportType, SearchIndexStatus, CacheLevel
)


class AnalyticsReportService:
    async def generate_report(
        self,
        db: AsyncSession,
        name: str,
        report_type: ReportType,
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(PageViewMetrics).where(
                and_(
                    PageViewMetrics.date >= period_start,
                    PageViewMetrics.date <= period_end,
                )
            )
        )
        metrics = result.scalars().all()

        total_pageviews = sum(m.page_views for m in metrics)
        total_visitors = sum(m.unique_visitors for m in metrics)
        avg_bounce_rate = (
            statistics.mean([m.bounce_rate for m in metrics]) if metrics else 0.0
        )
        avg_session_duration = (
            statistics.mean([m.avg_time_on_page for m in metrics]) if metrics else 0.0
        )

        report = AnalyticsReport(
            name=name,
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            total_pageviews=total_pageviews,
            total_sessions=len(metrics),
            unique_visitors=total_visitors,
            avg_session_duration=avg_session_duration,
            bounce_rate=avg_bounce_rate,
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)

        return {
            "id": report.id,
            "name": report.name,
            "report_type": report.report_type.value,
            "total_pageviews": total_pageviews,
            "unique_visitors": total_visitors,
            "avg_session_duration": avg_session_duration,
        }

    async def get_daily_analytics(
        self,
        db: AsyncSession,
        date: datetime,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(PageViewMetrics).where(
                func.date(PageViewMetrics.date) == date.date()
            )
        )
        metrics = result.scalars().all()

        return {
            "date": date,
            "total_pageviews": sum(m.page_views for m in metrics),
            "unique_visitors": sum(m.unique_visitors for m in metrics),
            "avg_bounce_rate": (
                statistics.mean([m.bounce_rate for m in metrics]) if metrics else 0.0
            ),
        }

    async def get_top_content(
        self,
        db: AsyncSession,
        limit: int = 10,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        result = await db.execute(
            select(PageViewMetrics)
            .where(PageViewMetrics.date >= cutoff_date)
            .order_by(desc(PageViewMetrics.page_views))
            .limit(limit)
        )
        metrics = result.scalars().all()

        return [
            {
                "content_id": m.content_id,
                "page_views": m.page_views,
                "unique_visitors": m.unique_visitors,
                "conversion_rate": m.conversion_count / max(m.page_views, 1) * 100,
            }
            for m in metrics
        ]


class UserBehaviorService:
    async def record_event(
        self,
        db: AsyncSession,
        user_id: int,
        event_type: str,
        content_id: Optional[int] = None,
        event_data: Optional[Dict] = None,
        device_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        event = UserBehaviorEvent(
            user_id=user_id,
            content_id=content_id,
            event_type=event_type,
            event_data=event_data or {},
            device_type=device_type,
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)

        return {
            "event_id": event.id,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
        }

    async def get_user_behavior_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(UserBehaviorEvent).where(UserBehaviorEvent.user_id == user_id)
        )
        events = result.scalars().all()

        event_types = {}
        for event in events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1

        return {
            "user_id": user_id,
            "total_events": len(events),
            "event_breakdown": event_types,
            "device_types": list(set(e.device_type for e in events if e.device_type)),
        }


class HeatmapService:
    async def create_heatmap(
        self,
        db: AsyncSession,
        content_id: int,
        heatmap_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(HeatmapData).where(HeatmapData.content_id == content_id)
        )
        heatmap = result.scalar_one_or_none()

        if heatmap:
            heatmap.heatmap_json = heatmap_data
            heatmap.last_updated = datetime.utcnow()
        else:
            heatmap = HeatmapData(
                content_id=content_id,
                heatmap_json=heatmap_data,
            )
            db.add(heatmap)

        await db.commit()

        return {
            "content_id": content_id,
            "heatmap_data": heatmap_data,
        }

    async def get_heatmap(self, db: AsyncSession, content_id: int) -> Dict[str, Any]:
        result = await db.execute(
            select(HeatmapData).where(HeatmapData.content_id == content_id)
        )
        heatmap = result.scalar_one_or_none()

        if not heatmap:
            raise ValueError(f"Heatmap for content {content_id} not found")

        return {
            "content_id": content_id,
            "heatmap_data": heatmap.heatmap_json,
            "exit_rate": heatmap.exit_rate,
        }


class SearchService:
    async def index_content(
        self,
        db: AsyncSession,
        content_id: int,
        title: str,
        full_text: str,
        tags: List[str],
        keywords: List[str],
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(SearchIndex).where(SearchIndex.content_id == content_id)
        )
        index_entry = result.scalar_one_or_none()

        if index_entry:
            index_entry.title = title
            index_entry.full_text = full_text
            index_entry.tags = tags
            index_entry.keywords = keywords
            index_entry.status = SearchIndexStatus.INDEXED
        else:
            index_entry = SearchIndex(
                content_id=content_id,
                title=title,
                full_text=full_text,
                tags=tags,
                keywords=keywords,
                status=SearchIndexStatus.INDEXED,
                indexed_at=datetime.utcnow(),
            )
            db.add(index_entry)

        await db.commit()

        return {
            "content_id": content_id,
            "status": index_entry.status.value,
            "indexed_at": index_entry.indexed_at,
        }

    async def search(
        self,
        db: AsyncSession,
        query: str,
        user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(SearchIndex).where(
                or_(
                    SearchIndex.title.ilike(f"%{query}%"),
                    SearchIndex.full_text.ilike(f"%{query}%"),
                    SearchIndex.tags.contains([query]),
                )
            )
        )
        results = result.scalars().all()

        # Log search query
        search_log = SearchQuery(
            user_id=user_id,
            query=query,
            result_count=len(results),
        )
        db.add(search_log)
        await db.commit()

        return {
            "query": query,
            "result_count": len(results),
            "results": [
                {
                    "content_id": r.content_id,
                    "title": r.title,
                    "relevance_score": 0.95,
                }
                for r in results[:20]
            ],
        }

    async def get_trending_searches(
        self,
        db: AsyncSession,
        limit: int = 10,
        days: int = 7,
    ) -> List[Dict[str, Any]]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        result = await db.execute(
            select(SearchQuery.query, func.count().label("count"))
            .where(SearchQuery.created_at >= cutoff_date)
            .group_by(SearchQuery.query)
            .order_by(desc("count"))
            .limit(limit)
        )
        rows = result.all()

        return [{"query": row[0], "count": row[1]} for row in rows]


class CacheService:
    async def set_cache(
        self,
        db: AsyncSession,
        key: str,
        value: str,
        ttl_seconds: int = 3600,
        cache_level: CacheLevel = CacheLevel.WARM,
    ) -> Dict[str, Any]:
        result = await db.execute(select(CacheEntry).where(CacheEntry.key == key))
        entry = result.scalar_one_or_none()

        if entry:
            entry.value = value
            entry.ttl_seconds = ttl_seconds
            entry.cache_level = cache_level
        else:
            entry = CacheEntry(
                key=key,
                value=value,
                ttl_seconds=ttl_seconds,
                cache_level=cache_level,
            )
            db.add(entry)

        await db.commit()

        return {
            "key": key,
            "ttl_seconds": ttl_seconds,
            "cache_level": cache_level.value,
        }

    async def get_cache(self, db: AsyncSession, key: str) -> Optional[str]:
        result = await db.execute(select(CacheEntry).where(CacheEntry.key == key))
        entry = result.scalar_one_or_none()

        if entry:
            entry.hits += 1
            entry.last_accessed = datetime.utcnow()
            await db.commit()
            return entry.value

        return None

    async def clear_cache(self, db: AsyncSession, key: str) -> Dict[str, Any]:
        result = await db.execute(select(CacheEntry).where(CacheEntry.key == key))
        entry = result.scalar_one_or_none()

        if entry:
            await db.delete(entry)
            await db.commit()

        return {"key": key, "status": "cleared"}

    async def get_cache_stats(self, db: AsyncSession) -> Dict[str, Any]:
        result = await db.execute(select(CacheEntry))
        entries = result.scalars().all()

        total_hits = sum(e.hits for e in entries)

        return {
            "total_entries": len(entries),
            "total_hits": total_hits,
            "avg_hits": total_hits / max(len(entries), 1),
            "hot_entries": len([e for e in entries if e.cache_level == CacheLevel.HOT]),
        }


class PerformanceService:
    async def record_metric(
        self,
        db: AsyncSession,
        endpoint: str,
        method: str,
        response_time_ms: int,
        status_code: int,
    ) -> Dict[str, Any]:
        metric = PerformanceMetric(
            endpoint=endpoint,
            method=method,
            response_time_ms=response_time_ms,
            status_code=status_code,
        )
        db.add(metric)
        await db.commit()

        return {
            "endpoint": endpoint,
            "response_time_ms": response_time_ms,
            "status_code": status_code,
        }

    async def get_endpoint_stats(
        self,
        db: AsyncSession,
        endpoint: str,
        hours: int = 24,
    ) -> Dict[str, Any]:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        result = await db.execute(
            select(PerformanceMetric).where(
                and_(
                    PerformanceMetric.endpoint == endpoint,
                    PerformanceMetric.timestamp >= cutoff_time,
                )
            )
        )
        metrics = result.scalars().all()

        if not metrics:
            return {"endpoint": endpoint, "data": None}

        response_times = [m.response_time_ms for m in metrics]

        return {
            "endpoint": endpoint,
            "request_count": len(metrics),
            "avg_response_time": statistics.mean(response_times),
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "p95_response_time": sorted(response_times)[int(len(response_times) * 0.95)],
            "error_rate": (
                len([m for m in metrics if m.status_code >= 400]) / len(metrics) * 100
            ),
        }


class AdminService:
    async def log_admin_action(
        self,
        db: AsyncSession,
        admin_id: int,
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        changes: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        audit_log = AdminAuditLog(
            admin_id=admin_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes or {},
        )
        db.add(audit_log)
        await db.commit()
        await db.refresh(audit_log)

        return {
            "log_id": audit_log.id,
            "action": action,
            "timestamp": audit_log.timestamp,
        }

    async def get_audit_logs(
        self,
        db: AsyncSession,
        admin_id: Optional[int] = None,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = select(AdminAuditLog).where(
            AdminAuditLog.timestamp >= cutoff_date
        )

        if admin_id:
            query = query.where(AdminAuditLog.admin_id == admin_id)

        result = await db.execute(query)
        logs = result.scalars().all()

        return [
            {
                "log_id": log.id,
                "admin_id": log.admin_id,
                "action": log.action,
                "resource_type": log.resource_type,
                "timestamp": log.timestamp,
            }
            for log in logs
        ]

    async def check_system_health(
        self,
        db: AsyncSession,
        service_name: str,
        status: str,
        response_time_ms: int,
    ) -> Dict[str, Any]:
        result = await db.execute(
            select(SystemHealthCheck).where(
                SystemHealthCheck.service_name == service_name
            )
        )
        health_check = result.scalar_one_or_none()

        if health_check:
            health_check.status = status
            health_check.response_time_ms = response_time_ms
            health_check.last_check = datetime.utcnow()
        else:
            health_check = SystemHealthCheck(
                service_name=service_name,
                status=status,
                response_time_ms=response_time_ms,
            )
            db.add(health_check)

        await db.commit()

        return {
            "service_name": service_name,
            "status": status,
            "response_time_ms": response_time_ms,
        }

    async def get_system_health(self, db: AsyncSession) -> Dict[str, Any]:
        result = await db.execute(select(SystemHealthCheck))
        health_checks = result.scalars().all()

        healthy = len([h for h in health_checks if h.status == "healthy"])
        degraded = len([h for h in health_checks if h.status == "degraded"])
        unhealthy = len([h for h in health_checks if h.status == "unhealthy"])

        return {
            "total_services": len(health_checks),
            "healthy": healthy,
            "degraded": degraded,
            "unhealthy": unhealthy,
            "overall_status": (
                "healthy" if unhealthy == 0 else "degraded" if degraded > 0 else "unhealthy"
            ),
        }


class FeatureFlagService:
    async def create_feature_flag(
        self,
        db: AsyncSession,
        name: str,
        enabled: bool,
        rollout_percentage: int = 0,
        target_segments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        flag = FeatureFlag(
            name=name,
            enabled=enabled,
            rollout_percentage=rollout_percentage,
            target_segments=target_segments or [],
        )
        db.add(flag)
        await db.commit()
        await db.refresh(flag)

        return {
            "flag_id": flag.id,
            "name": flag.name,
            "enabled": flag.enabled,
        }

    async def is_feature_enabled(
        self,
        db: AsyncSession,
        feature_name: str,
        user_id: Optional[int] = None,
    ) -> bool:
        result = await db.execute(
            select(FeatureFlag).where(FeatureFlag.name == feature_name)
        )
        flag = result.scalar_one_or_none()

        if not flag or not flag.enabled:
            return False

        # Implement rollout logic if needed
        if flag.rollout_percentage < 100 and user_id:
            hash_value = int(
                hashlib.md5(f"{user_id}{feature_name}".encode()).hexdigest(), 16
            )
            return (hash_value % 100) < flag.rollout_percentage

        return True

    async def update_feature_flag(
        self,
        db: AsyncSession,
        flag_id: int,
        enabled: Optional[bool] = None,
        rollout_percentage: Optional[int] = None,
    ) -> Dict[str, Any]:
        result = await db.execute(select(FeatureFlag).where(FeatureFlag.id == flag_id))
        flag = result.scalar_one_or_none()

        if not flag:
            raise ValueError(f"Feature flag {flag_id} not found")

        if enabled is not None:
            flag.enabled = enabled
        if rollout_percentage is not None:
            flag.rollout_percentage = rollout_percentage

        await db.commit()

        return {
            "flag_id": flag.id,
            "enabled": flag.enabled,
            "rollout_percentage": flag.rollout_percentage,
        }
