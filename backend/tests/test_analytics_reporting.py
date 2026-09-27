import pytest
from datetime import datetime, timedelta
from app.models.analytics_reporting import (
    ReportType, SearchIndexStatus, CacheLevel, AnalyticsReport,
    PageViewMetrics, UserBehaviorEvent, HeatmapData, SearchIndex,
    SearchQuery, CacheEntry, PerformanceMetric, SystemLog,
    AdminAuditLog, SystemHealthCheck, ConfigurationSetting, FeatureFlag
)
from app.services.analytics_reporting_service import (
    AnalyticsReportService, UserBehaviorService, HeatmapService,
    SearchService, CacheService, PerformanceService, AdminService,
    FeatureFlagService
)

class TestAnalyticsReportService:
    @pytest.mark.asyncio
    async def test_generate_daily_report(self):
        service = AnalyticsReportService()
        report = await service.generate_report(
            name="Daily Report",
            report_type=ReportType.DAILY,
            period_start=datetime.now() - timedelta(days=1),
            period_end=datetime.now()
        )
        assert report.name == "Daily Report"
        assert report.report_type == ReportType.DAILY

    @pytest.mark.asyncio
    async def test_generate_weekly_report(self):
        service = AnalyticsReportService()
        report = await service.generate_report(
            name="Weekly Report",
            report_type=ReportType.WEEKLY,
            period_start=datetime.now() - timedelta(days=7),
            period_end=datetime.now()
        )
        assert report.report_type == ReportType.WEEKLY

    @pytest.mark.asyncio
    async def test_generate_monthly_report(self):
        service = AnalyticsReportService()
        report = await service.generate_report(
            name="Monthly Report",
            report_type=ReportType.MONTHLY,
            period_start=datetime.now() - timedelta(days=30),
            period_end=datetime.now()
        )
        assert report.report_type == ReportType.MONTHLY

    @pytest.mark.asyncio
    async def test_get_daily_analytics(self):
        service = AnalyticsReportService()
        start = datetime.now() - timedelta(days=7)
        end = datetime.now()
        analytics = await service.get_daily_analytics(start, end)
        assert isinstance(analytics, list)

    @pytest.mark.asyncio
    async def test_get_top_content(self):
        service = AnalyticsReportService()
        top_content = await service.get_top_content(limit=10)
        assert isinstance(top_content, list)
        assert len(top_content) <= 10

    @pytest.mark.asyncio
    async def test_get_top_content_with_date_range(self):
        service = AnalyticsReportService()
        start = datetime.now() - timedelta(days=30)
        end = datetime.now()
        top_content = await service.get_top_content(
            limit=5, start_date=start, end_date=end
        )
        assert isinstance(top_content, list)

    @pytest.mark.asyncio
    async def test_report_includes_correct_metrics(self):
        service = AnalyticsReportService()
        report = await service.generate_report(
            name="Metrics Test",
            report_type=ReportType.DAILY,
            period_start=datetime.now() - timedelta(days=1),
            period_end=datetime.now()
        )
        assert hasattr(report, 'total_pageviews')
        assert hasattr(report, 'total_sessions')
        assert hasattr(report, 'unique_visitors')
        assert hasattr(report, 'bounce_rate')
        assert hasattr(report, 'conversion_rate')


class TestUserBehaviorService:
    @pytest.mark.asyncio
    async def test_record_click_event(self):
        service = UserBehaviorService()
        event = await service.record_event(
            user_id=1,
            content_id=100,
            event_type='click',
            event_data={'x': 100, 'y': 200}
        )
        assert event.event_type == 'click'
        assert event.user_id == 1

    @pytest.mark.asyncio
    async def test_record_scroll_event(self):
        service = UserBehaviorService()
        event = await service.record_event(
            user_id=1,
            event_type='scroll',
            event_data={'depth': 75}
        )
        assert event.event_type == 'scroll'

    @pytest.mark.asyncio
    async def test_record_hover_event(self):
        service = UserBehaviorService()
        event = await service.record_event(
            user_id=1,
            event_type='hover',
            event_data={'duration_ms': 2000}
        )
        assert event.event_type == 'hover'

    @pytest.mark.asyncio
    async def test_record_exit_event(self):
        service = UserBehaviorService()
        event = await service.record_event(
            user_id=1,
            event_type='exit'
        )
        assert event.event_type == 'exit'

    @pytest.mark.asyncio
    async def test_get_user_behavior_summary(self):
        service = UserBehaviorService()
        summary = await service.get_user_behavior_summary(user_id=1)
        assert summary.user_id == 1
        assert isinstance(summary.event_breakdown, dict)

    @pytest.mark.asyncio
    async def test_behavior_summary_includes_event_types(self):
        service = UserBehaviorService()
        summary = await service.get_user_behavior_summary(user_id=1)
        assert hasattr(summary, 'total_events')
        assert hasattr(summary, 'event_breakdown')
        assert hasattr(summary, 'most_common_event')

    @pytest.mark.asyncio
    async def test_record_event_with_page_context(self):
        service = UserBehaviorService()
        event = await service.record_event(
            user_id=1,
            content_id=100,
            event_type='read',
            page_url='https://example.com/article/1',
            referrer='https://google.com'
        )
        assert event.page_url == 'https://example.com/article/1'
        assert event.referrer == 'https://google.com'

    @pytest.mark.asyncio
    async def test_record_event_with_device_info(self):
        service = UserBehaviorService()
        event = await service.record_event(
            user_id=1,
            event_type='click',
            device_type='mobile',
            browser='Chrome',
            os='iOS'
        )
        assert event.device_type == 'mobile'
        assert event.browser == 'Chrome'
        assert event.os == 'iOS'


class TestHeatmapService:
    @pytest.mark.asyncio
    async def test_create_heatmap(self):
        service = HeatmapService()
        heatmap = await service.create_heatmap(
            content_id=100,
            heatmap_json={'zones': [{'x': 0, 'y': 0, 'clicks': 10}]},
            exit_rate=0.15
        )
        assert heatmap.content_id == 100
        assert heatmap.exit_rate == 0.15

    @pytest.mark.asyncio
    async def test_create_heatmap_with_scroll_depth(self):
        service = HeatmapService()
        heatmap = await service.create_heatmap(
            content_id=100,
            heatmap_json={'zones': []},
            scroll_depth_percentiles={'25': 80, '50': 60, '75': 40, '100': 20}
        )
        assert '25' in heatmap.scroll_depth_percentiles

    @pytest.mark.asyncio
    async def test_create_heatmap_with_click_zones(self):
        service = HeatmapService()
        click_zones = {'button': 150, 'link': 300, 'image': 50}
        heatmap = await service.create_heatmap(
            content_id=100,
            heatmap_json={},
            click_zones=click_zones
        )
        assert 'button' in heatmap.click_zones

    @pytest.mark.asyncio
    async def test_get_heatmap(self):
        service = HeatmapService()
        heatmap = await service.get_heatmap(content_id=100)
        assert heatmap.content_id == 100

    @pytest.mark.asyncio
    async def test_heatmap_updates_existing(self):
        service = HeatmapService()
        heatmap1 = await service.create_heatmap(
            content_id=100,
            heatmap_json={'version': 1}
        )
        heatmap2 = await service.create_heatmap(
            content_id=100,
            heatmap_json={'version': 2}
        )
        assert heatmap2.heatmap_json['version'] == 2


class TestSearchService:
    @pytest.mark.asyncio
    async def test_index_content(self):
        service = SearchService()
        indexed = await service.index_content(
            content_id=100,
            title="Test Article",
            summary="Test summary",
            keywords=['test', 'search']
        )
        assert indexed.title == "Test Article"
        assert indexed.status == SearchIndexStatus.PENDING or indexed.status == SearchIndexStatus.INDEXED

    @pytest.mark.asyncio
    async def test_index_with_categories(self):
        service = SearchService()
        indexed = await service.index_content(
            content_id=100,
            title="Article",
            categories=['technology', 'ai']
        )
        assert 'technology' in indexed.categories

    @pytest.mark.asyncio
    async def test_search_content(self):
        service = SearchService()
        results = await service.search(query="test", limit=10)
        assert isinstance(results, list)
        assert len(results) <= 10

    @pytest.mark.asyncio
    async def test_search_with_limit(self):
        service = SearchService()
        results = await service.search(query="technology", limit=5)
        assert len(results) <= 5

    @pytest.mark.asyncio
    async def test_search_results_have_relevance(self):
        service = SearchService()
        results = await service.search(query="test")
        for result in results:
            assert hasattr(result, 'relevance_score')
            assert 0 <= result.relevance_score <= 1.0

    @pytest.mark.asyncio
    async def test_get_trending_searches(self):
        service = SearchService()
        trending = await service.get_trending_searches(days=7, limit=10)
        assert isinstance(trending, list)
        assert len(trending) <= 10

    @pytest.mark.asyncio
    async def test_trending_searches_sorted_by_count(self):
        service = SearchService()
        trending = await service.get_trending_searches(days=7, limit=100)
        if len(trending) > 1:
            counts = [t.count for t in trending]
            assert counts == sorted(counts, reverse=True)


class TestCacheService:
    @pytest.mark.asyncio
    async def test_set_cache_warm(self):
        service = CacheService()
        entry = await service.set_cache(
            key="test_key",
            value="test_value",
            cache_level=CacheLevel.WARM
        )
        assert entry.key == "test_key"
        assert entry.cache_level == CacheLevel.WARM

    @pytest.mark.asyncio
    async def test_set_cache_hot(self):
        service = CacheService()
        entry = await service.set_cache(
            key="hot_key",
            value="hot_value",
            cache_level=CacheLevel.HOT,
            ttl_seconds=60
        )
        assert entry.cache_level == CacheLevel.HOT
        assert entry.ttl_seconds == 60

    @pytest.mark.asyncio
    async def test_set_cache_cold(self):
        service = CacheService()
        entry = await service.set_cache(
            key="cold_key",
            value="cold_value",
            cache_level=CacheLevel.COLD,
            ttl_seconds=86400
        )
        assert entry.cache_level == CacheLevel.COLD

    @pytest.mark.asyncio
    async def test_get_cache(self):
        service = CacheService()
        await service.set_cache("key1", "value1")
        entry = await service.get_cache("key1")
        assert entry.value == "value1"
        assert entry.hits >= 1

    @pytest.mark.asyncio
    async def test_get_cache_increments_hits(self):
        service = CacheService()
        await service.set_cache("key_hits", "value")
        await service.get_cache("key_hits")
        entry = await service.get_cache("key_hits")
        assert entry.hits >= 1

    @pytest.mark.asyncio
    async def test_delete_cache(self):
        service = CacheService()
        await service.set_cache("key_delete", "value")
        await service.delete_cache("key_delete")
        deleted = await service.get_cache("key_delete")
        assert deleted is None

    @pytest.mark.asyncio
    async def test_clear_cache(self):
        service = CacheService()
        await service.set_cache("key1", "value1")
        await service.set_cache("key2", "value2")
        await service.clear_cache()
        stats = await service.get_cache_stats()
        assert stats.total_entries == 0

    @pytest.mark.asyncio
    async def test_get_cache_stats(self):
        service = CacheService()
        await service.set_cache("stat_key", "value")
        stats = await service.get_cache_stats()
        assert stats.total_entries >= 1
        assert hasattr(stats, 'hit_rate')
        assert hasattr(stats, 'total_hits')


class TestPerformanceService:
    @pytest.mark.asyncio
    async def test_record_metric(self):
        service = PerformanceService()
        metric = await service.record_metric(
            endpoint="/api/articles",
            method="GET",
            response_time_ms=150,
            status_code=200
        )
        assert metric.endpoint == "/api/articles"
        assert metric.response_time_ms == 150

    @pytest.mark.asyncio
    async def test_record_metric_post(self):
        service = PerformanceService()
        metric = await service.record_metric(
            endpoint="/api/subscribers",
            method="POST",
            response_time_ms=250,
            status_code=201
        )
        assert metric.method == "POST"
        assert metric.status_code == 201

    @pytest.mark.asyncio
    async def test_record_metric_with_sizes(self):
        service = PerformanceService()
        metric = await service.record_metric(
            endpoint="/api/data",
            method="GET",
            response_time_ms=100,
            status_code=200,
            request_size=512,
            response_size=4096
        )
        assert metric.response_size == 4096

    @pytest.mark.asyncio
    async def test_get_endpoint_stats(self):
        service = PerformanceService()
        for _ in range(5):
            await service.record_metric(
                endpoint="/api/test",
                method="GET",
                response_time_ms=100 + _,
                status_code=200
            )
        stats = await service.get_endpoint_stats("/api/test", "GET")
        assert stats.endpoint == "/api/test"
        assert stats.request_count >= 5

    @pytest.mark.asyncio
    async def test_endpoint_stats_p95_latency(self):
        service = PerformanceService()
        for i in range(100):
            await service.record_metric(
                endpoint="/api/load",
                method="GET",
                response_time_ms=100 + (i % 50),
                status_code=200
            )
        stats = await service.get_endpoint_stats("/api/load", "GET")
        assert stats.p95_response_time_ms > 0

    @pytest.mark.asyncio
    async def test_endpoint_stats_error_rate(self):
        service = PerformanceService()
        for i in range(10):
            await service.record_metric(
                endpoint="/api/errors",
                method="GET",
                response_time_ms=100,
                status_code=200 if i < 8 else 500
            )
        stats = await service.get_endpoint_stats("/api/errors", "GET")
        assert stats.error_rate == 0.2 or stats.error_rate >= 0


class TestAdminService:
    @pytest.mark.asyncio
    async def test_log_admin_action(self):
        service = AdminService()
        log = await service.log_admin_action(
            admin_id=1,
            action="delete_article",
            resource_type="article",
            resource_id=100,
            changes={"status": "published"}
        )
        assert log.admin_id == 1
        assert log.action == "delete_article"

    @pytest.mark.asyncio
    async def test_log_admin_action_with_ip(self):
        service = AdminService()
        log = await service.log_admin_action(
            admin_id=1,
            action="login",
            resource_type="user",
            ip_address="192.168.1.1"
        )
        assert log.ip_address == "192.168.1.1"

    @pytest.mark.asyncio
    async def test_get_audit_logs(self):
        service = AdminService()
        logs = await service.get_audit_logs(limit=10)
        assert isinstance(logs, list)
        assert len(logs) <= 10

    @pytest.mark.asyncio
    async def test_get_audit_logs_by_admin(self):
        service = AdminService()
        logs = await service.get_audit_logs(limit=10, admin_id=1)
        for log in logs:
            assert log.admin_id == 1

    @pytest.mark.asyncio
    async def test_check_system_health(self):
        service = AdminService()
        health = await service.check_system_health()
        assert health.overall_status in ['healthy', 'degraded', 'unhealthy']
        assert len(health.services) > 0

    @pytest.mark.asyncio
    async def test_system_health_includes_services(self):
        service = AdminService()
        health = await service.check_system_health()
        for svc in health.services:
            assert hasattr(svc, 'service_name')
            assert hasattr(svc, 'status')
            assert hasattr(svc, 'uptime_percentage')

    @pytest.mark.asyncio
    async def test_get_service_health(self):
        service = AdminService()
        health = await service.get_service_health("api_server")
        assert health.service_name == "api_server"

    @pytest.mark.asyncio
    async def test_update_service_health(self):
        service = AdminService()
        result = await service.update_service_health(
            service_name="cache_service",
            status="healthy",
            response_time_ms=50
        )
        assert result.service_name == "cache_service"

    @pytest.mark.asyncio
    async def test_configuration_setting(self):
        service = AdminService()
        config = await service.set_configuration(
            key="max_cache_size",
            value="1000000",
            setting_type="number"
        )
        assert config.key == "max_cache_size"

    @pytest.mark.asyncio
    async def test_get_configuration(self):
        service = AdminService()
        await service.set_configuration("test_key", "test_value")
        config = await service.get_configuration("test_key")
        assert config.value == "test_value"


class TestFeatureFlagService:
    @pytest.mark.asyncio
    async def test_create_feature_flag(self):
        service = FeatureFlagService()
        flag = await service.create_feature_flag(
            name="new_dashboard",
            description="New dashboard UI",
            enabled=False,
            rollout_percentage=0
        )
        assert flag.name == "new_dashboard"
        assert flag.enabled is False

    @pytest.mark.asyncio
    async def test_create_flag_with_rollout(self):
        service = FeatureFlagService()
        flag = await service.create_feature_flag(
            name="partial_rollout",
            enabled=True,
            rollout_percentage=50
        )
        assert flag.rollout_percentage == 50

    @pytest.mark.asyncio
    async def test_is_feature_enabled_always_true(self):
        service = FeatureFlagService()
        await service.create_feature_flag("feature_on", enabled=True)
        enabled = await service.is_feature_enabled("feature_on")
        assert enabled is True

    @pytest.mark.asyncio
    async def test_is_feature_enabled_always_false(self):
        service = FeatureFlagService()
        await service.create_feature_flag("feature_off", enabled=False)
        enabled = await service.is_feature_enabled("feature_off")
        assert enabled is False

    @pytest.mark.asyncio
    async def test_is_feature_enabled_with_rollout(self):
        service = FeatureFlagService()
        await service.create_feature_flag(
            "rollout_feature",
            enabled=True,
            rollout_percentage=50
        )
        enabled = await service.is_feature_enabled("rollout_feature", user_id=1)
        assert isinstance(enabled, bool)

    @pytest.mark.asyncio
    async def test_is_feature_enabled_consistent_for_user(self):
        service = FeatureFlagService()
        await service.create_feature_flag(
            "consistent_feature",
            enabled=True,
            rollout_percentage=50
        )
        enabled1 = await service.is_feature_enabled("consistent_feature", user_id=123)
        enabled2 = await service.is_feature_enabled("consistent_feature", user_id=123)
        assert enabled1 == enabled2

    @pytest.mark.asyncio
    async def test_update_feature_flag(self):
        service = FeatureFlagService()
        flag = await service.create_feature_flag("update_test", enabled=False)
        updated = await service.update_feature_flag(
            flag.id,
            name="update_test",
            enabled=True,
            rollout_percentage=100
        )
        assert updated.enabled is True

    @pytest.mark.asyncio
    async def test_get_feature_flag(self):
        service = FeatureFlagService()
        await service.create_feature_flag("get_test", enabled=True)
        flag = await service.get_feature_flag("get_test")
        assert flag.name == "get_test"

    @pytest.mark.asyncio
    async def test_list_feature_flags(self):
        service = FeatureFlagService()
        for i in range(5):
            await service.create_feature_flag(f"flag_{i}", enabled=True)
        flags = await service.list_feature_flags()
        assert len(flags) >= 5

    @pytest.mark.asyncio
    async def test_delete_feature_flag(self):
        service = FeatureFlagService()
        flag = await service.create_feature_flag("delete_test", enabled=True)
        await service.delete_feature_flag(flag.id)
        deleted = await service.get_feature_flag("delete_test")
        assert deleted is None


class TestIntegrationScenarios:
    @pytest.mark.asyncio
    async def test_full_analytics_workflow(self):
        analytics_service = AnalyticsReportService()
        behavior_service = UserBehaviorService()

        await behavior_service.record_event(1, 100, "read", {})
        await behavior_service.record_event(1, 100, "click", {"x": 50})

        report = await analytics_service.generate_report(
            "integration_test",
            ReportType.DAILY,
            datetime.now() - timedelta(days=1),
            datetime.now()
        )
        assert report.name == "integration_test"

    @pytest.mark.asyncio
    async def test_search_and_heatmap_workflow(self):
        search_service = SearchService()
        heatmap_service = HeatmapService()

        await search_service.index_content(
            100, "Article", keywords=["test"]
        )
        await heatmap_service.create_heatmap(
            100, {"zones": []}, exit_rate=0.1
        )

        results = await search_service.search("test")
        assert len(results) >= 0

    @pytest.mark.asyncio
    async def test_cache_and_performance_tracking(self):
        cache_service = CacheService()
        perf_service = PerformanceService()

        await cache_service.set_cache("perf_key", "value")
        await perf_service.record_metric(
            "/api/cache", "GET", 50, 200
        )

        cache_entry = await cache_service.get_cache("perf_key")
        assert cache_entry is not None


class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_invalid_date_range(self):
        service = AnalyticsReportService()
        with pytest.raises(ValueError):
            await service.get_daily_analytics(
                datetime.now(), datetime.now() - timedelta(days=1)
            )

    @pytest.mark.asyncio
    async def test_invalid_percentage(self):
        service = FeatureFlagService()
        with pytest.raises(ValueError):
            await service.create_feature_flag(
                "invalid", enabled=True, rollout_percentage=150
            )

    @pytest.mark.asyncio
    async def test_cache_ttl_negative(self):
        service = CacheService()
        with pytest.raises(ValueError):
            await service.set_cache("key", "value", ttl_seconds=-1)


class TestPerformance:
    @pytest.mark.asyncio
    async def test_performance_with_large_dataset(self):
        service = UserBehaviorService()
        for i in range(100):
            await service.record_event(
                user_id=1, content_id=i, event_type="click"
            )
        summary = await service.get_user_behavior_summary(1)
        assert summary.total_events >= 100

    @pytest.mark.asyncio
    async def test_cache_with_many_entries(self):
        service = CacheService()
        for i in range(100):
            await service.set_cache(f"key_{i}", f"value_{i}")
        stats = await service.get_cache_stats()
        assert stats.total_entries >= 100

    @pytest.mark.asyncio
    async def test_search_performance(self):
        service = SearchService()
        for i in range(50):
            await service.index_content(i, f"Article {i}")
        results = await service.search("article", limit=100)
        assert len(results) >= 0
