import 'package:freezed_annotation/freezed_annotation.dart';

part 'analytics_models.freezed.dart';
part 'analytics_models.g.dart';

@freezed
class AnalyticsReport with _$AnalyticsReport {
  const factory AnalyticsReport({
    required int id,
    required String name,
    required String reportType,
    required DateTime periodStart,
    required DateTime periodEnd,
    required int totalPageviews,
    required int totalSessions,
    required int uniqueVisitors,
    required double avgSessionDuration,
    required double bounceRate,
    required double conversionRate,
    required double revenue,
    required DateTime createdAt,
    required DateTime updatedAt,
  }) = _AnalyticsReport;

  factory AnalyticsReport.fromJson(Map<String, dynamic> json) =>
      _$AnalyticsReportFromJson(json);
}

@freezed
class DailyAnalytics with _$DailyAnalytics {
  const factory DailyAnalytics({
    required DateTime date,
    required int pageviews,
    required int sessions,
    required int uniqueVisitors,
    required double bounceRate,
    required double conversionRate,
  }) = _DailyAnalytics;

  factory DailyAnalytics.fromJson(Map<String, dynamic> json) =>
      _$DailyAnalyticsFromJson(json);
}

@freezed
class PageViewMetric with _$PageViewMetric {
  const factory PageViewMetric({
    required int id,
    required int contentId,
    required DateTime date,
    required int pageViews,
    required int uniqueVisitors,
    required double avgTimeOnPage,
    required double bounceRate,
    required double scrollDepth,
    required int conversionCount,
  }) = _PageViewMetric;

  factory PageViewMetric.fromJson(Map<String, dynamic> json) =>
      _$PageViewMetricFromJson(json);
}

@freezed
class TopContent with _$TopContent {
  const factory TopContent({
    required int contentId,
    required int pageviews,
    required int uniqueVisitors,
    required double avgTimeOnPage,
    required int conversionCount,
    required String? title,
  }) = _TopContent;

  factory TopContent.fromJson(Map<String, dynamic> json) =>
      _$TopContentFromJson(json);
}

@freezed
class UserEvent with _$UserEvent {
  const factory UserEvent({
    required int id,
    required int userId,
    required int? contentId,
    required String eventType,
    required Map<String, dynamic> eventData,
    required String? pageUrl,
    required String? referrer,
    required String? deviceType,
    required String? browser,
    required String? os,
    required DateTime timestamp,
  }) = _UserEvent;

  factory UserEvent.fromJson(Map<String, dynamic> json) =>
      _$UserEventFromJson(json);
}

@freezed
class UserBehaviorSummary with _$UserBehaviorSummary {
  const factory UserBehaviorSummary({
    required int userId,
    required int totalEvents,
    required Map<String, int> eventBreakdown,
    required DateTime? lastEvent,
    required String? mostCommonEvent,
    required double? engagementScore,
  }) = _UserBehaviorSummary;

  factory UserBehaviorSummary.fromJson(Map<String, dynamic> json) =>
      _$UserBehaviorSummaryFromJson(json);
}

@freezed
class HeatmapData with _$HeatmapData {
  const factory HeatmapData({
    required int id,
    required int contentId,
    required Map<String, dynamic> heatmapJson,
    required Map<String, dynamic> scrollDepthPercentiles,
    required Map<String, dynamic> clickZones,
    required double exitRate,
    required DateTime lastUpdated,
  }) = _HeatmapData;

  factory HeatmapData.fromJson(Map<String, dynamic> json) =>
      _$HeatmapDataFromJson(json);
}

@freezed
class SearchIndexEntry with _$SearchIndexEntry {
  const factory SearchIndexEntry({
    required int id,
    required int contentId,
    required String title,
    required String? summary,
    required String status,
    required DateTime? indexedAt,
    required DateTime createdAt,
  }) = _SearchIndexEntry;

  factory SearchIndexEntry.fromJson(Map<String, dynamic> json) =>
      _$SearchIndexEntryFromJson(json);
}

@freezed
class SearchResult with _$SearchResult {
  const factory SearchResult({
    required int contentId,
    required String title,
    required String? summary,
    required double relevanceScore,
    required List<String> tags,
    required List<String> categories,
  }) = _SearchResult;

  factory SearchResult.fromJson(Map<String, dynamic> json) =>
      _$SearchResultFromJson(json);
}

@freezed
class TrendingSearch with _$TrendingSearch {
  const factory TrendingSearch({
    required String query,
    required int count,
    required int resultCountAvg,
    required double clickThroughRate,
    required int? lastSearched,
  }) = _TrendingSearch;

  factory TrendingSearch.fromJson(Map<String, dynamic> json) =>
      _$TrendingSearchFromJson(json);
}

@freezed
class CacheEntry with _$CacheEntry {
  const factory CacheEntry({
    required int id,
    required String key,
    required String value,
    required String cacheLevel,
    required int ttlSeconds,
    required int hits,
    required DateTime lastAccessed,
    required DateTime createdAt,
  }) = _CacheEntry;

  factory CacheEntry.fromJson(Map<String, dynamic> json) =>
      _$CacheEntryFromJson(json);
}

@freezed
class CacheStats with _$CacheStats {
  const factory CacheStats({
    required int totalEntries,
    required int hotEntries,
    required int warmEntries,
    required int coldEntries,
    required int totalHits,
    required double avgHitsPerEntry,
    required double hitRate,
  }) = _CacheStats;

  factory CacheStats.fromJson(Map<String, dynamic> json) =>
      _$CacheStatsFromJson(json);
}

@freezed
class PerformanceMetric with _$PerformanceMetric {
  const factory PerformanceMetric({
    required int id,
    required String endpoint,
    required String method,
    required int responseTimeMs,
    required int statusCode,
    required int requestSize,
    required int responseSize,
    required DateTime timestamp,
  }) = _PerformanceMetric;

  factory PerformanceMetric.fromJson(Map<String, dynamic> json) =>
      _$PerformanceMetricFromJson(json);
}

@freezed
class EndpointStats with _$EndpointStats {
  const factory EndpointStats({
    required String endpoint,
    required String method,
    required int requestCount,
    required double avgResponseTimeMs,
    required double p95ResponseTimeMs,
    required double p99ResponseTimeMs,
    required double errorRate,
    required Map<String, int> statusBreakdown,
  }) = _EndpointStats;

  factory EndpointStats.fromJson(Map<String, dynamic> json) =>
      _$EndpointStatsFromJson(json);
}

@freezed
class AdminAction with _$AdminAction {
  const factory AdminAction({
    required int id,
    required int adminId,
    required String action,
    required String resourceType,
    required int? resourceId,
    required Map<String, dynamic> changes,
    required String? ipAddress,
    required DateTime timestamp,
  }) = _AdminAction;

  factory AdminAction.fromJson(Map<String, dynamic> json) =>
      _$AdminActionFromJson(json);
}

@freezed
class AuditLog with _$AuditLog {
  const factory AuditLog({
    required int id,
    required int adminId,
    required String action,
    required String resourceType,
    required int? resourceId,
    required Map<String, dynamic> changes,
    required DateTime timestamp,
  }) = _AuditLog;

  factory AuditLog.fromJson(Map<String, dynamic> json) =>
      _$AuditLogFromJson(json);
}

@freezed
class HealthCheckResult with _$HealthCheckResult {
  const factory HealthCheckResult({
    required String serviceName,
    required String status,
    required int? responseTimeMs,
    required double uptimePercentage,
    required int errorCount,
    required DateTime lastCheck,
  }) = _HealthCheckResult;

  factory HealthCheckResult.fromJson(Map<String, dynamic> json) =>
      _$HealthCheckResultFromJson(json);
}

@freezed
class SystemHealth with _$SystemHealth {
  const factory SystemHealth({
    required String overallStatus,
    required DateTime timestamp,
    required List<HealthCheckResult> services,
    required double totalUptime,
  }) = _SystemHealth;

  factory SystemHealth.fromJson(Map<String, dynamic> json) =>
      _$SystemHealthFromJson(json);
}

@freezed
class ConfigurationSetting with _$ConfigurationSetting {
  const factory ConfigurationSetting({
    required int id,
    required String key,
    required String value,
    required String settingType,
    required String? description,
    required DateTime updatedAt,
  }) = _ConfigurationSetting;

  factory ConfigurationSetting.fromJson(Map<String, dynamic> json) =>
      _$ConfigurationSettingFromJson(json);
}

@freezed
class FeatureFlag with _$FeatureFlag {
  const factory FeatureFlag({
    required int id,
    required String name,
    required String? description,
    required bool enabled,
    required int rolloutPercentage,
    required List<String> targetSegments,
    required DateTime createdAt,
    required DateTime updatedAt,
  }) = _FeatureFlag;

  factory FeatureFlag.fromJson(Map<String, dynamic> json) =>
      _$FeatureFlagFromJson(json);
}

@freezed
class PerformanceSummary with _$PerformanceSummary {
  const factory PerformanceSummary({
    required double avgResponseTimeMs,
    required double p95ResponseTimeMs,
    required double p99ResponseTimeMs,
    required int totalRequests,
    required double errorRate,
    required int uptime,
  }) = _PerformanceSummary;

  factory PerformanceSummary.fromJson(Map<String, dynamic> json) =>
      _$PerformanceSummaryFromJson(json);
}

@freezed
class SearchQuery with _$SearchQuery {
  const factory SearchQuery({
    required int id,
    required int? userId,
    required String query,
    required int resultCount,
    required int? clickedResult,
    required int searchTimeMs,
    required DateTime createdAt,
  }) = _SearchQuery;

  factory SearchQuery.fromJson(Map<String, dynamic> json) =>
      _$SearchQueryFromJson(json);
}
