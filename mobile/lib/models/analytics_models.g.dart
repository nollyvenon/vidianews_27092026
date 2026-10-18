// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'analytics_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$AnalyticsReportImpl _$$AnalyticsReportImplFromJson(
        Map<String, dynamic> json) =>
    _$AnalyticsReportImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      reportType: json['report_type'] as String,
      periodStart: DateTime.parse(json['period_start'] as String),
      periodEnd: DateTime.parse(json['period_end'] as String),
      totalPageviews: (json['total_pageviews'] as num).toInt(),
      totalSessions: (json['total_sessions'] as num).toInt(),
      uniqueVisitors: (json['unique_visitors'] as num).toInt(),
      avgSessionDuration: (json['avg_session_duration'] as num).toDouble(),
      bounceRate: (json['bounce_rate'] as num).toDouble(),
      conversionRate: (json['conversion_rate'] as num).toDouble(),
      revenue: (json['revenue'] as num).toDouble(),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$AnalyticsReportImplToJson(
        _$AnalyticsReportImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'report_type': instance.reportType,
      'period_start': instance.periodStart.toIso8601String(),
      'period_end': instance.periodEnd.toIso8601String(),
      'total_pageviews': instance.totalPageviews,
      'total_sessions': instance.totalSessions,
      'unique_visitors': instance.uniqueVisitors,
      'avg_session_duration': instance.avgSessionDuration,
      'bounce_rate': instance.bounceRate,
      'conversion_rate': instance.conversionRate,
      'revenue': instance.revenue,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

_$DailyAnalyticsImpl _$$DailyAnalyticsImplFromJson(Map<String, dynamic> json) =>
    _$DailyAnalyticsImpl(
      date: DateTime.parse(json['date'] as String),
      pageviews: (json['pageviews'] as num).toInt(),
      sessions: (json['sessions'] as num).toInt(),
      uniqueVisitors: (json['unique_visitors'] as num).toInt(),
      bounceRate: (json['bounce_rate'] as num).toDouble(),
      conversionRate: (json['conversion_rate'] as num).toDouble(),
    );

Map<String, dynamic> _$$DailyAnalyticsImplToJson(
        _$DailyAnalyticsImpl instance) =>
    <String, dynamic>{
      'date': instance.date.toIso8601String(),
      'pageviews': instance.pageviews,
      'sessions': instance.sessions,
      'unique_visitors': instance.uniqueVisitors,
      'bounce_rate': instance.bounceRate,
      'conversion_rate': instance.conversionRate,
    };

_$PageViewMetricImpl _$$PageViewMetricImplFromJson(Map<String, dynamic> json) =>
    _$PageViewMetricImpl(
      id: (json['id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      date: DateTime.parse(json['date'] as String),
      pageViews: (json['page_views'] as num).toInt(),
      uniqueVisitors: (json['unique_visitors'] as num).toInt(),
      avgTimeOnPage: (json['avg_time_on_page'] as num).toDouble(),
      bounceRate: (json['bounce_rate'] as num).toDouble(),
      scrollDepth: (json['scroll_depth'] as num).toDouble(),
      conversionCount: (json['conversion_count'] as num).toInt(),
    );

Map<String, dynamic> _$$PageViewMetricImplToJson(
        _$PageViewMetricImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'content_id': instance.contentId,
      'date': instance.date.toIso8601String(),
      'page_views': instance.pageViews,
      'unique_visitors': instance.uniqueVisitors,
      'avg_time_on_page': instance.avgTimeOnPage,
      'bounce_rate': instance.bounceRate,
      'scroll_depth': instance.scrollDepth,
      'conversion_count': instance.conversionCount,
    };

_$TopContentImpl _$$TopContentImplFromJson(Map<String, dynamic> json) =>
    _$TopContentImpl(
      contentId: (json['content_id'] as num).toInt(),
      pageviews: (json['pageviews'] as num).toInt(),
      uniqueVisitors: (json['unique_visitors'] as num).toInt(),
      avgTimeOnPage: (json['avg_time_on_page'] as num).toDouble(),
      conversionCount: (json['conversion_count'] as num).toInt(),
      title: json['title'] as String?,
    );

Map<String, dynamic> _$$TopContentImplToJson(_$TopContentImpl instance) =>
    <String, dynamic>{
      'content_id': instance.contentId,
      'pageviews': instance.pageviews,
      'unique_visitors': instance.uniqueVisitors,
      'avg_time_on_page': instance.avgTimeOnPage,
      'conversion_count': instance.conversionCount,
      'title': instance.title,
    };

_$UserEventImpl _$$UserEventImplFromJson(Map<String, dynamic> json) =>
    _$UserEventImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      contentId: (json['content_id'] as num?)?.toInt(),
      eventType: json['event_type'] as String,
      eventData: json['event_data'] as Map<String, dynamic>,
      pageUrl: json['page_url'] as String?,
      referrer: json['referrer'] as String?,
      deviceType: json['device_type'] as String?,
      browser: json['browser'] as String?,
      os: json['os'] as String?,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );

Map<String, dynamic> _$$UserEventImplToJson(_$UserEventImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'content_id': instance.contentId,
      'event_type': instance.eventType,
      'event_data': instance.eventData,
      'page_url': instance.pageUrl,
      'referrer': instance.referrer,
      'device_type': instance.deviceType,
      'browser': instance.browser,
      'os': instance.os,
      'timestamp': instance.timestamp.toIso8601String(),
    };

_$UserBehaviorSummaryImpl _$$UserBehaviorSummaryImplFromJson(
        Map<String, dynamic> json) =>
    _$UserBehaviorSummaryImpl(
      userId: (json['user_id'] as num).toInt(),
      totalEvents: (json['total_events'] as num).toInt(),
      eventBreakdown: Map<String, int>.from(json['event_breakdown'] as Map),
      lastEvent: json['last_event'] == null
          ? null
          : DateTime.parse(json['last_event'] as String),
      mostCommonEvent: json['most_common_event'] as String?,
      engagementScore: (json['engagement_score'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$$UserBehaviorSummaryImplToJson(
        _$UserBehaviorSummaryImpl instance) =>
    <String, dynamic>{
      'user_id': instance.userId,
      'total_events': instance.totalEvents,
      'event_breakdown': instance.eventBreakdown,
      'last_event': instance.lastEvent?.toIso8601String(),
      'most_common_event': instance.mostCommonEvent,
      'engagement_score': instance.engagementScore,
    };

_$HeatmapDataImpl _$$HeatmapDataImplFromJson(Map<String, dynamic> json) =>
    _$HeatmapDataImpl(
      id: (json['id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      heatmapJson: json['heatmap_json'] as Map<String, dynamic>,
      scrollDepthPercentiles:
          json['scroll_depth_percentiles'] as Map<String, dynamic>,
      clickZones: json['click_zones'] as Map<String, dynamic>,
      exitRate: (json['exit_rate'] as num).toDouble(),
      lastUpdated: DateTime.parse(json['last_updated'] as String),
    );

Map<String, dynamic> _$$HeatmapDataImplToJson(_$HeatmapDataImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'content_id': instance.contentId,
      'heatmap_json': instance.heatmapJson,
      'scroll_depth_percentiles': instance.scrollDepthPercentiles,
      'click_zones': instance.clickZones,
      'exit_rate': instance.exitRate,
      'last_updated': instance.lastUpdated.toIso8601String(),
    };

_$SearchIndexEntryImpl _$$SearchIndexEntryImplFromJson(
        Map<String, dynamic> json) =>
    _$SearchIndexEntryImpl(
      id: (json['id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      title: json['title'] as String,
      summary: json['summary'] as String?,
      status: json['status'] as String,
      indexedAt: json['indexed_at'] == null
          ? null
          : DateTime.parse(json['indexed_at'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$SearchIndexEntryImplToJson(
        _$SearchIndexEntryImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'content_id': instance.contentId,
      'title': instance.title,
      'summary': instance.summary,
      'status': instance.status,
      'indexed_at': instance.indexedAt?.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$SearchResultImpl _$$SearchResultImplFromJson(Map<String, dynamic> json) =>
    _$SearchResultImpl(
      contentId: (json['content_id'] as num).toInt(),
      title: json['title'] as String,
      summary: json['summary'] as String?,
      relevanceScore: (json['relevance_score'] as num).toDouble(),
      tags: (json['tags'] as List<dynamic>).map((e) => e as String).toList(),
      categories: (json['categories'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
    );

Map<String, dynamic> _$$SearchResultImplToJson(_$SearchResultImpl instance) =>
    <String, dynamic>{
      'content_id': instance.contentId,
      'title': instance.title,
      'summary': instance.summary,
      'relevance_score': instance.relevanceScore,
      'tags': instance.tags,
      'categories': instance.categories,
    };

_$TrendingSearchImpl _$$TrendingSearchImplFromJson(Map<String, dynamic> json) =>
    _$TrendingSearchImpl(
      query: json['query'] as String,
      count: (json['count'] as num).toInt(),
      resultCountAvg: (json['result_count_avg'] as num).toInt(),
      clickThroughRate: (json['click_through_rate'] as num).toDouble(),
      lastSearched: (json['last_searched'] as num?)?.toInt(),
    );

Map<String, dynamic> _$$TrendingSearchImplToJson(
        _$TrendingSearchImpl instance) =>
    <String, dynamic>{
      'query': instance.query,
      'count': instance.count,
      'result_count_avg': instance.resultCountAvg,
      'click_through_rate': instance.clickThroughRate,
      'last_searched': instance.lastSearched,
    };

_$CacheEntryImpl _$$CacheEntryImplFromJson(Map<String, dynamic> json) =>
    _$CacheEntryImpl(
      id: (json['id'] as num).toInt(),
      key: json['key'] as String,
      value: json['value'] as String,
      cacheLevel: json['cache_level'] as String,
      ttlSeconds: (json['ttl_seconds'] as num).toInt(),
      hits: (json['hits'] as num).toInt(),
      lastAccessed: DateTime.parse(json['last_accessed'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$CacheEntryImplToJson(_$CacheEntryImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'key': instance.key,
      'value': instance.value,
      'cache_level': instance.cacheLevel,
      'ttl_seconds': instance.ttlSeconds,
      'hits': instance.hits,
      'last_accessed': instance.lastAccessed.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$CacheStatsImpl _$$CacheStatsImplFromJson(Map<String, dynamic> json) =>
    _$CacheStatsImpl(
      totalEntries: (json['total_entries'] as num).toInt(),
      hotEntries: (json['hot_entries'] as num).toInt(),
      warmEntries: (json['warm_entries'] as num).toInt(),
      coldEntries: (json['cold_entries'] as num).toInt(),
      totalHits: (json['total_hits'] as num).toInt(),
      avgHitsPerEntry: (json['avg_hits_per_entry'] as num).toDouble(),
      hitRate: (json['hit_rate'] as num).toDouble(),
    );

Map<String, dynamic> _$$CacheStatsImplToJson(_$CacheStatsImpl instance) =>
    <String, dynamic>{
      'total_entries': instance.totalEntries,
      'hot_entries': instance.hotEntries,
      'warm_entries': instance.warmEntries,
      'cold_entries': instance.coldEntries,
      'total_hits': instance.totalHits,
      'avg_hits_per_entry': instance.avgHitsPerEntry,
      'hit_rate': instance.hitRate,
    };

_$PerformanceMetricImpl _$$PerformanceMetricImplFromJson(
        Map<String, dynamic> json) =>
    _$PerformanceMetricImpl(
      id: (json['id'] as num).toInt(),
      endpoint: json['endpoint'] as String,
      method: json['method'] as String,
      responseTimeMs: (json['response_time_ms'] as num).toInt(),
      statusCode: (json['status_code'] as num).toInt(),
      requestSize: (json['request_size'] as num).toInt(),
      responseSize: (json['response_size'] as num).toInt(),
      timestamp: DateTime.parse(json['timestamp'] as String),
    );

Map<String, dynamic> _$$PerformanceMetricImplToJson(
        _$PerformanceMetricImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'endpoint': instance.endpoint,
      'method': instance.method,
      'response_time_ms': instance.responseTimeMs,
      'status_code': instance.statusCode,
      'request_size': instance.requestSize,
      'response_size': instance.responseSize,
      'timestamp': instance.timestamp.toIso8601String(),
    };

_$EndpointStatsImpl _$$EndpointStatsImplFromJson(Map<String, dynamic> json) =>
    _$EndpointStatsImpl(
      endpoint: json['endpoint'] as String,
      method: json['method'] as String,
      requestCount: (json['request_count'] as num).toInt(),
      avgResponseTimeMs: (json['avg_response_time_ms'] as num).toDouble(),
      p95ResponseTimeMs: (json['p95_response_time_ms'] as num).toDouble(),
      p99ResponseTimeMs: (json['p99_response_time_ms'] as num).toDouble(),
      errorRate: (json['error_rate'] as num).toDouble(),
      statusBreakdown: Map<String, int>.from(json['status_breakdown'] as Map),
    );

Map<String, dynamic> _$$EndpointStatsImplToJson(_$EndpointStatsImpl instance) =>
    <String, dynamic>{
      'endpoint': instance.endpoint,
      'method': instance.method,
      'request_count': instance.requestCount,
      'avg_response_time_ms': instance.avgResponseTimeMs,
      'p95_response_time_ms': instance.p95ResponseTimeMs,
      'p99_response_time_ms': instance.p99ResponseTimeMs,
      'error_rate': instance.errorRate,
      'status_breakdown': instance.statusBreakdown,
    };

_$AdminActionImpl _$$AdminActionImplFromJson(Map<String, dynamic> json) =>
    _$AdminActionImpl(
      id: (json['id'] as num).toInt(),
      adminId: (json['admin_id'] as num).toInt(),
      action: json['action'] as String,
      resourceType: json['resource_type'] as String,
      resourceId: (json['resource_id'] as num?)?.toInt(),
      changes: json['changes'] as Map<String, dynamic>,
      ipAddress: json['ip_address'] as String?,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );

Map<String, dynamic> _$$AdminActionImplToJson(_$AdminActionImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'admin_id': instance.adminId,
      'action': instance.action,
      'resource_type': instance.resourceType,
      'resource_id': instance.resourceId,
      'changes': instance.changes,
      'ip_address': instance.ipAddress,
      'timestamp': instance.timestamp.toIso8601String(),
    };

_$AuditLogImpl _$$AuditLogImplFromJson(Map<String, dynamic> json) =>
    _$AuditLogImpl(
      id: (json['id'] as num).toInt(),
      adminId: (json['admin_id'] as num).toInt(),
      action: json['action'] as String,
      resourceType: json['resource_type'] as String,
      resourceId: (json['resource_id'] as num?)?.toInt(),
      changes: json['changes'] as Map<String, dynamic>,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );

Map<String, dynamic> _$$AuditLogImplToJson(_$AuditLogImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'admin_id': instance.adminId,
      'action': instance.action,
      'resource_type': instance.resourceType,
      'resource_id': instance.resourceId,
      'changes': instance.changes,
      'timestamp': instance.timestamp.toIso8601String(),
    };

_$HealthCheckResultImpl _$$HealthCheckResultImplFromJson(
        Map<String, dynamic> json) =>
    _$HealthCheckResultImpl(
      serviceName: json['service_name'] as String,
      status: json['status'] as String,
      responseTimeMs: (json['response_time_ms'] as num?)?.toInt(),
      uptimePercentage: (json['uptime_percentage'] as num).toDouble(),
      errorCount: (json['error_count'] as num).toInt(),
      lastCheck: DateTime.parse(json['last_check'] as String),
    );

Map<String, dynamic> _$$HealthCheckResultImplToJson(
        _$HealthCheckResultImpl instance) =>
    <String, dynamic>{
      'service_name': instance.serviceName,
      'status': instance.status,
      'response_time_ms': instance.responseTimeMs,
      'uptime_percentage': instance.uptimePercentage,
      'error_count': instance.errorCount,
      'last_check': instance.lastCheck.toIso8601String(),
    };

_$SystemHealthImpl _$$SystemHealthImplFromJson(Map<String, dynamic> json) =>
    _$SystemHealthImpl(
      overallStatus: json['overall_status'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      services: (json['services'] as List<dynamic>)
          .map((e) => HealthCheckResult.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalUptime: (json['total_uptime'] as num).toDouble(),
    );

Map<String, dynamic> _$$SystemHealthImplToJson(_$SystemHealthImpl instance) =>
    <String, dynamic>{
      'overall_status': instance.overallStatus,
      'timestamp': instance.timestamp.toIso8601String(),
      'services': instance.services,
      'total_uptime': instance.totalUptime,
    };

_$ConfigurationSettingImpl _$$ConfigurationSettingImplFromJson(
        Map<String, dynamic> json) =>
    _$ConfigurationSettingImpl(
      id: (json['id'] as num).toInt(),
      key: json['key'] as String,
      value: json['value'] as String,
      settingType: json['setting_type'] as String,
      description: json['description'] as String?,
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$ConfigurationSettingImplToJson(
        _$ConfigurationSettingImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'key': instance.key,
      'value': instance.value,
      'setting_type': instance.settingType,
      'description': instance.description,
      'updated_at': instance.updatedAt.toIso8601String(),
    };

_$FeatureFlagImpl _$$FeatureFlagImplFromJson(Map<String, dynamic> json) =>
    _$FeatureFlagImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      enabled: json['enabled'] as bool,
      rolloutPercentage: (json['rollout_percentage'] as num).toInt(),
      targetSegments: (json['target_segments'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$FeatureFlagImplToJson(_$FeatureFlagImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'enabled': instance.enabled,
      'rollout_percentage': instance.rolloutPercentage,
      'target_segments': instance.targetSegments,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

_$PerformanceSummaryImpl _$$PerformanceSummaryImplFromJson(
        Map<String, dynamic> json) =>
    _$PerformanceSummaryImpl(
      avgResponseTimeMs: (json['avg_response_time_ms'] as num).toDouble(),
      p95ResponseTimeMs: (json['p95_response_time_ms'] as num).toDouble(),
      p99ResponseTimeMs: (json['p99_response_time_ms'] as num).toDouble(),
      totalRequests: (json['total_requests'] as num).toInt(),
      errorRate: (json['error_rate'] as num).toDouble(),
      uptime: (json['uptime'] as num).toInt(),
    );

Map<String, dynamic> _$$PerformanceSummaryImplToJson(
        _$PerformanceSummaryImpl instance) =>
    <String, dynamic>{
      'avg_response_time_ms': instance.avgResponseTimeMs,
      'p95_response_time_ms': instance.p95ResponseTimeMs,
      'p99_response_time_ms': instance.p99ResponseTimeMs,
      'total_requests': instance.totalRequests,
      'error_rate': instance.errorRate,
      'uptime': instance.uptime,
    };

_$SearchQueryImpl _$$SearchQueryImplFromJson(Map<String, dynamic> json) =>
    _$SearchQueryImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num?)?.toInt(),
      query: json['query'] as String,
      resultCount: (json['result_count'] as num).toInt(),
      clickedResult: (json['clicked_result'] as num?)?.toInt(),
      searchTimeMs: (json['search_time_ms'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$SearchQueryImplToJson(_$SearchQueryImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'query': instance.query,
      'result_count': instance.resultCount,
      'clicked_result': instance.clickedResult,
      'search_time_ms': instance.searchTimeMs,
      'created_at': instance.createdAt.toIso8601String(),
    };
