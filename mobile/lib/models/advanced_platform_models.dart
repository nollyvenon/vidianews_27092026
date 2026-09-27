import 'package:freezed_annotation/freezed_annotation.dart';

part 'advanced_platform_models.freezed.dart';
part 'advanced_platform_models.g.dart';

@freezed
class WebSocketConnection with _$WebSocketConnection {
  const factory WebSocketConnection({
    required int id,
    required int userId,
    required String connectionId,
    required String status,
    required List<String> eventSubscriptions,
    String? ipAddress,
    required DateTime connectedAt,
    DateTime? disconnectedAt,
  }) = _WebSocketConnection;

  factory WebSocketConnection.fromJson(Map<String, dynamic> json) => _$WebSocketConnectionFromJson(json);
}

@freezed
class RealtimeEvent with _$RealtimeEvent {
  const factory RealtimeEvent({
    required int id,
    required String eventType,
    required String eventSource,
    required List<int> userIds,
    required Map<String, dynamic> payload,
    required int priority,
    required String status,
    required DateTime createdAt,
    DateTime? publishedAt,
  }) = _RealtimeEvent;

  factory RealtimeEvent.fromJson(Map<String, dynamic> json) => _$RealtimeEventFromJson(json);
}

@freezed
class BackgroundJob with _$BackgroundJob {
  const factory BackgroundJob({
    required int id,
    required String jobType,
    required String status,
    int? userId,
    required int priority,
    required Map<String, dynamic> payload,
    Map<String, dynamic>? result,
    String? errorMessage,
    required int retryCount,
    required DateTime createdAt,
    DateTime? startedAt,
    DateTime? completedAt,
  }) = _BackgroundJob;

  factory BackgroundJob.fromJson(Map<String, dynamic> json) => _$BackgroundJobFromJson(json);
}

@freezed
class JobSchedule with _$JobSchedule {
  const factory JobSchedule({
    required int id,
    required String jobType,
    required String cronExpression,
    required bool enabled,
    String? description,
    DateTime? lastRun,
    DateTime? nextRun,
    required DateTime createdAt,
  }) = _JobSchedule;

  factory JobSchedule.fromJson(Map<String, dynamic> json) => _$JobScheduleFromJson(json);
}

@freezed
class DataPipeline with _$DataPipeline {
  const factory DataPipeline({
    required int id,
    required String name,
    required String sourceType,
    required String destinationType,
    required String status,
    required bool isActive,
    String? description,
    String? schedule,
    required DateTime createdAt,
    DateTime? lastRun,
    DateTime? lastSuccess,
  }) = _DataPipeline;

  factory DataPipeline.fromJson(Map<String, dynamic> json) => _$DataPipelineFromJson(json);
}

@freezed
class PipelineExecution with _$PipelineExecution {
  const factory PipelineExecution({
    required int id,
    required int pipelineId,
    required String status,
    required int recordsProcessed,
    required int recordsFailed,
    int? executionTimeMs,
    required DateTime startedAt,
    DateTime? completedAt,
    String? errorMessage,
  }) = _PipelineExecution;

  factory PipelineExecution.fromJson(Map<String, dynamic> json) => _$PipelineExecutionFromJson(json);
}

@freezed
class PipelineStage with _$PipelineStage {
  const factory PipelineStage({
    required int id,
    required int pipelineId,
    required String stageName,
    required int stageOrder,
    required String stageType,
    required Map<String, dynamic> config,
    required String status,
    required DateTime createdAt,
  }) = _PipelineStage;

  factory PipelineStage.fromJson(Map<String, dynamic> json) => _$PipelineStageFromJson(json);
}

@freezed
class CacheEntry with _$CacheEntry {
  const factory CacheEntry({
    required String cacheKey,
    required Map<String, dynamic> cacheValue,
    required String strategy,
    int? ttlSeconds,
    required int hitCount,
    int? sizeBytes,
    required DateTime createdAt,
    DateTime? expiresAt,
  }) = _CacheEntry;

  factory CacheEntry.fromJson(Map<String, dynamic> json) => _$CacheEntryFromJson(json);
}

@freezed
class CacheMetrics with _$CacheMetrics {
  const factory CacheMetrics({
    required int totalRequests,
    required int totalHits,
    required int totalMisses,
    required double averageResponseTimeMs,
    required double memoryUsageMb,
    required int evictionCount,
    required DateTime measuredAt,
  }) = _CacheMetrics;

  factory CacheMetrics.fromJson(Map<String, dynamic> json) => _$CacheMetricsFromJson(json);
}

@freezed
class APIDocumentation with _$APIDocumentation {
  const factory APIDocumentation({
    required int id,
    required String name,
    required String format,
    required String version,
    String? description,
    String? basePath,
    required List<String> servers,
    required DateTime createdAt,
    required DateTime updatedAt,
  }) = _APIDocumentation;

  factory APIDocumentation.fromJson(Map<String, dynamic> json) => _$APIDocumentationFromJson(json);
}

@freezed
class APIEndpoint with _$APIEndpoint {
  const factory APIEndpoint({
    required int id,
    required String path,
    required String method,
    String? summary,
    String? description,
    Map<String, dynamic>? parameters,
    Map<String, dynamic>? requestSchema,
    Map<String, dynamic>? responseSchema,
    required DateTime createdAt,
  }) = _APIEndpoint;

  factory APIEndpoint.fromJson(Map<String, dynamic> json) => _$APIEndpointFromJson(json);
}

@freezed
class APIUsageMetrics with _$APIUsageMetrics {
  const factory APIUsageMetrics({
    required String endpoint,
    required String method,
    required int callCount,
    required int errorCount,
    required double averageResponseTimeMs,
    required double maxResponseTimeMs,
    required double minResponseTimeMs,
    required DateTime measuredAt,
  }) = _APIUsageMetrics;

  factory APIUsageMetrics.fromJson(Map<String, dynamic> json) => _$APIUsageMetricsFromJson(json);
}

@freezed
class PlatformMetrics with _$PlatformMetrics {
  const factory PlatformMetrics({
    required int activeWebSocketConnections,
    required int pendingBackgroundJobs,
    required int runningPipelines,
    required int totalCacheSize,
    required double cacheHitRate,
    required double apiAverageResponseTime,
  }) = _PlatformMetrics;

  factory PlatformMetrics.fromJson(Map<String, dynamic> json) => _$PlatformMetricsFromJson(json);
}
