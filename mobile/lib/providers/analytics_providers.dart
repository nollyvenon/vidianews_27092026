import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/analytics_models.dart';

class AnalyticsService {
  final Dio dio;
  final String baseUrl = 'https://api.vidianews.com/api/v1';

  AnalyticsService({required this.dio});

  // Analytics Report Methods
  Future<AnalyticsReport> createAnalyticsReport({
    required String name,
    required String reportType,
    required DateTime periodStart,
    required DateTime periodEnd,
  }) async {
    final response = await dio.post(
      '$baseUrl/analytics/reports',
      data: {
        'name': name,
        'report_type': reportType,
        'period_start': periodStart.toIso8601String(),
        'period_end': periodEnd.toIso8601String(),
      },
    );
    return AnalyticsReport.fromJson(response.data);
  }

  Future<AnalyticsReport?> getAnalyticsReport(int reportId) async {
    try {
      final response = await dio.get('$baseUrl/analytics/reports/$reportId');
      return AnalyticsReport.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  Future<List<DailyAnalytics>> getDailyAnalytics({
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    final response = await dio.get(
      '$baseUrl/analytics/daily',
      queryParameters: {
        'start_date': startDate.toIso8601String(),
        'end_date': endDate.toIso8601String(),
      },
    );
    return (response.data as List)
        .map((item) => DailyAnalytics.fromJson(item))
        .toList();
  }

  Future<List<TopContent>> getTopContent({
    int limit = 10,
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    final response = await dio.get(
      '$baseUrl/analytics/top-content',
      queryParameters: {
        'limit': limit,
        if (startDate != null) 'start_date': startDate.toIso8601String(),
        if (endDate != null) 'end_date': endDate.toIso8601String(),
      },
    );
    return (response.data as List)
        .map((item) => TopContent.fromJson(item))
        .toList();
  }

  // User Behavior Methods
  Future<UserEvent> recordUserEvent({
    required int userId,
    int? contentId,
    required String eventType,
    Map<String, dynamic> eventData = const {},
    String? pageUrl,
    String? referrer,
    String? deviceType,
    String? browser,
    String? os,
  }) async {
    final response = await dio.post(
      '$baseUrl/behavior/events',
      data: {
        'user_id': userId,
        if (contentId != null) 'content_id': contentId,
        'event_type': eventType,
        'event_data': eventData,
        if (pageUrl != null) 'page_url': pageUrl,
        if (referrer != null) 'referrer': referrer,
        if (deviceType != null) 'device_type': deviceType,
        if (browser != null) 'browser': browser,
        if (os != null) 'os': os,
      },
    );
    return UserEvent.fromJson(response.data);
  }

  Future<UserBehaviorSummary?> getUserBehaviorSummary(int userId) async {
    try {
      final response = await dio.get('$baseUrl/behavior/users/$userId/summary');
      return UserBehaviorSummary.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  Future<List<UserEvent>> getUserEvents(int userId, {int limit = 100}) async {
    final response = await dio.get(
      '$baseUrl/behavior/users/$userId/events',
      queryParameters: {'limit': limit},
    );
    return (response.data as List)
        .map((item) => UserEvent.fromJson(item))
        .toList();
  }

  // Heatmap Methods
  Future<HeatmapData> createHeatmap({
    required int contentId,
    required Map<String, dynamic> heatmapJson,
    Map<String, dynamic> scrollDepthPercentiles = const {},
    Map<String, dynamic> clickZones = const {},
    double exitRate = 0.0,
  }) async {
    final response = await dio.post(
      '$baseUrl/heatmaps',
      data: {
        'content_id': contentId,
        'heatmap_json': heatmapJson,
        'scroll_depth_percentiles': scrollDepthPercentiles,
        'click_zones': clickZones,
        'exit_rate': exitRate,
      },
    );
    return HeatmapData.fromJson(response.data);
  }

  Future<HeatmapData?> getHeatmap(int contentId) async {
    try {
      final response = await dio.get('$baseUrl/heatmaps/$contentId');
      return HeatmapData.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  // Search Methods
  Future<SearchIndexEntry> indexContent({
    required int contentId,
    required String title,
    String? summary,
    String? fullText,
    List<String> tags = const [],
    List<String> categories = const [],
    List<String> keywords = const [],
  }) async {
    final response = await dio.post(
      '$baseUrl/search/index',
      data: {
        'content_id': contentId,
        'title': title,
        if (summary != null) 'summary': summary,
        if (fullText != null) 'full_text': fullText,
        'tags': tags,
        'categories': categories,
        'keywords': keywords,
      },
    );
    return SearchIndexEntry.fromJson(response.data);
  }

  Future<List<SearchResult>> search(String query, {int limit = 20}) async {
    final response = await dio.get(
      '$baseUrl/search/results',
      queryParameters: {
        'query': query,
        'limit': limit,
      },
    );
    return (response.data as List)
        .map((item) => SearchResult.fromJson(item))
        .toList();
  }

  Future<List<TrendingSearch>> getTrendingSearches({
    int days = 7,
    int limit = 10,
  }) async {
    final response = await dio.get(
      '$baseUrl/search/trending',
      queryParameters: {
        'days': days,
        'limit': limit,
      },
    );
    return (response.data as List)
        .map((item) => TrendingSearch.fromJson(item))
        .toList();
  }

  Future<SearchIndexEntry?> getIndexedContent(int contentId) async {
    try {
      final response = await dio.get('$baseUrl/search/indexed/$contentId');
      return SearchIndexEntry.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  // Cache Methods
  Future<CacheEntry> setCache({
    required String key,
    required String value,
    String cacheLevel = 'warm',
    int ttlSeconds = 3600,
  }) async {
    final response = await dio.post(
      '$baseUrl/cache',
      data: {
        'key': key,
        'value': value,
        'cache_level': cacheLevel,
        'ttl_seconds': ttlSeconds,
      },
    );
    return CacheEntry.fromJson(response.data);
  }

  Future<CacheEntry?> getCache(String key) async {
    try {
      final response = await dio.get('$baseUrl/cache/$key');
      return CacheEntry.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  Future<void> deleteCache(String key) async {
    await dio.delete('$baseUrl/cache/$key');
  }

  Future<void> clearAllCache() async {
    await dio.post('$baseUrl/cache/clear-all');
  }

  Future<CacheStats> getCacheStats() async {
    final response = await dio.get('$baseUrl/cache/stats/summary');
    return CacheStats.fromJson(response.data);
  }

  // Performance Methods
  Future<PerformanceMetric> recordPerformanceMetric({
    required String endpoint,
    required String method,
    required int responseTimeMs,
    required int statusCode,
    int requestSize = 0,
    int responseSize = 0,
  }) async {
    final response = await dio.post(
      '$baseUrl/performance/metrics',
      data: {
        'endpoint': endpoint,
        'method': method,
        'response_time_ms': responseTimeMs,
        'status_code': statusCode,
        'request_size': requestSize,
        'response_size': responseSize,
      },
    );
    return PerformanceMetric.fromJson(response.data);
  }

  Future<EndpointStats?> getEndpointStats(String endpoint, String method) async {
    try {
      final response = await dio.get(
        '$baseUrl/performance/endpoints/$endpoint',
        queryParameters: {'method': method},
      );
      return EndpointStats.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  Future<PerformanceSummary> getPerformanceSummary() async {
    final response = await dio.get('$baseUrl/performance/summary');
    return PerformanceSummary.fromJson(response.data);
  }

  // Admin Methods
  Future<AdminAction> logAdminAction({
    required int adminId,
    required String action,
    required String resourceType,
    int? resourceId,
    Map<String, dynamic> changes = const {},
    String? ipAddress,
  }) async {
    final response = await dio.post(
      '$baseUrl/admin/actions',
      data: {
        'admin_id': adminId,
        'action': action,
        'resource_type': resourceType,
        if (resourceId != null) 'resource_id': resourceId,
        'changes': changes,
        if (ipAddress != null) 'ip_address': ipAddress,
      },
    );
    return AdminAction.fromJson(response.data);
  }

  Future<List<AuditLog>> getAuditLogs({
    int limit = 100,
    int offset = 0,
    int? adminId,
  }) async {
    final response = await dio.get(
      '$baseUrl/admin/audit-logs',
      queryParameters: {
        'limit': limit,
        'offset': offset,
        if (adminId != null) 'admin_id': adminId,
      },
    );
    return (response.data as List)
        .map((item) => AuditLog.fromJson(item))
        .toList();
  }

  Future<SystemHealth> checkSystemHealth() async {
    final response = await dio.get('$baseUrl/admin/health');
    return SystemHealth.fromJson(response.data);
  }

  Future<HealthCheckResult?> getServiceHealth(String serviceName) async {
    try {
      final response = await dio.get('$baseUrl/admin/health/$serviceName');
      return HealthCheckResult.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  // Feature Flag Methods
  Future<FeatureFlag> createFeatureFlag({
    required String name,
    String? description,
    bool enabled = false,
    int rolloutPercentage = 0,
    List<String> targetSegments = const [],
  }) async {
    final response = await dio.post(
      '$baseUrl/feature-flags',
      data: {
        'name': name,
        if (description != null) 'description': description,
        'enabled': enabled,
        'rollout_percentage': rolloutPercentage,
        'target_segments': targetSegments,
      },
    );
    return FeatureFlag.fromJson(response.data);
  }

  Future<FeatureFlag?> getFeatureFlag(String flagName) async {
    try {
      final response = await dio.get('$baseUrl/feature-flags/$flagName');
      return FeatureFlag.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  Future<bool> isFeatureEnabled(String flagName, {int? userId}) async {
    final response = await dio.get(
      '$baseUrl/feature-flags/$flagName/enabled',
      queryParameters: {
        if (userId != null) 'user_id': userId,
      },
    );
    return response.data['enabled'] as bool;
  }

  Future<List<FeatureFlag>> listFeatureFlags() async {
    final response = await dio.get('$baseUrl/feature-flags');
    return (response.data as List)
        .map((item) => FeatureFlag.fromJson(item))
        .toList();
  }
}

// Riverpod Providers

final dioProvider = Provider((ref) {
  return Dio();
});

final analyticsServiceProvider = Provider((ref) {
  final dio = ref.watch(dioProvider);
  return AnalyticsService(dio: dio);
});

final analyticsReportProvider = FutureProvider<AnalyticsReport?>((ref) async {
  return null;
});

final dailyAnalyticsProvider =
    FutureProvider.family<List<DailyAnalytics>, (DateTime, DateTime)>(
  (ref, dates) async {
    final service = ref.watch(analyticsServiceProvider);
    return service.getDailyAnalytics(
      startDate: dates.$1,
      endDate: dates.$2,
    );
  },
);

final topContentProvider =
    FutureProvider.family<List<TopContent>, int>((ref, limit) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getTopContent(limit: limit);
});

final userEventProvider = FutureProvider<UserEvent?>((ref) async {
  return null;
});

final userBehaviorSummaryProvider =
    FutureProvider.family<UserBehaviorSummary?, int>((ref, userId) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getUserBehaviorSummary(userId);
});

final userEventsProvider =
    FutureProvider.family<List<UserEvent>, int>((ref, userId) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getUserEvents(userId);
});

final heatmapProvider =
    FutureProvider.family<HeatmapData?, int>((ref, contentId) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getHeatmap(contentId);
});

final searchResultsProvider =
    FutureProvider.family<List<SearchResult>, String>((ref, query) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.search(query);
});

final trendingSearchesProvider =
    FutureProvider.family<List<TrendingSearch>, int>((ref, days) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getTrendingSearches(days: days);
});

final cacheStatsProvider = FutureProvider<CacheStats>((ref) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getCacheStats();
});

final endpointStatsProvider =
    FutureProvider.family<EndpointStats?, (String, String)>(
  (ref, params) async {
    final service = ref.watch(analyticsServiceProvider);
    return service.getEndpointStats(params.$1, params.$2);
  },
);

final performanceSummaryProvider =
    FutureProvider<PerformanceSummary>((ref) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getPerformanceSummary();
});

final auditLogsProvider =
    FutureProvider.family<List<AuditLog>, int>((ref, limit) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getAuditLogs(limit: limit);
});

final systemHealthProvider = FutureProvider<SystemHealth>((ref) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.checkSystemHealth();
});

final serviceHealthProvider =
    FutureProvider.family<HealthCheckResult?, String>((ref, serviceName) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getServiceHealth(serviceName);
});

final featureFlagsProvider = FutureProvider<List<FeatureFlag>>((ref) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.listFeatureFlags();
});

final featureFlagProvider =
    FutureProvider.family<FeatureFlag?, String>((ref, flagName) async {
  final service = ref.watch(analyticsServiceProvider);
  return service.getFeatureFlag(flagName);
});

final isFeatureEnabledProvider = FutureProvider.family<bool, (String, int?)>(
  (ref, params) async {
    final service = ref.watch(analyticsServiceProvider);
    return service.isFeatureEnabled(params.$1, userId: params.$2);
  },
);
