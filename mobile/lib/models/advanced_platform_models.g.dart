// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'advanced_platform_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$WebSocketConnectionImpl _$$WebSocketConnectionImplFromJson(
        Map<String, dynamic> json) =>
    _$WebSocketConnectionImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      connectionId: json['connection_id'] as String,
      status: json['status'] as String,
      eventSubscriptions: (json['event_subscriptions'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      ipAddress: json['ip_address'] as String?,
      connectedAt: DateTime.parse(json['connected_at'] as String),
      disconnectedAt: json['disconnected_at'] == null
          ? null
          : DateTime.parse(json['disconnected_at'] as String),
    );

Map<String, dynamic> _$$WebSocketConnectionImplToJson(
        _$WebSocketConnectionImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'connection_id': instance.connectionId,
      'status': instance.status,
      'event_subscriptions': instance.eventSubscriptions,
      'ip_address': instance.ipAddress,
      'connected_at': instance.connectedAt.toIso8601String(),
      'disconnected_at': instance.disconnectedAt?.toIso8601String(),
    };

_$RealtimeEventImpl _$$RealtimeEventImplFromJson(Map<String, dynamic> json) =>
    _$RealtimeEventImpl(
      id: (json['id'] as num).toInt(),
      eventType: json['event_type'] as String,
      eventSource: json['event_source'] as String,
      userIds: (json['user_ids'] as List<dynamic>)
          .map((e) => (e as num).toInt())
          .toList(),
      payload: json['payload'] as Map<String, dynamic>,
      priority: (json['priority'] as num).toInt(),
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      publishedAt: json['published_at'] == null
          ? null
          : DateTime.parse(json['published_at'] as String),
    );

Map<String, dynamic> _$$RealtimeEventImplToJson(_$RealtimeEventImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'event_type': instance.eventType,
      'event_source': instance.eventSource,
      'user_ids': instance.userIds,
      'payload': instance.payload,
      'priority': instance.priority,
      'status': instance.status,
      'created_at': instance.createdAt.toIso8601String(),
      'published_at': instance.publishedAt?.toIso8601String(),
    };

_$BackgroundJobImpl _$$BackgroundJobImplFromJson(Map<String, dynamic> json) =>
    _$BackgroundJobImpl(
      id: (json['id'] as num).toInt(),
      jobType: json['job_type'] as String,
      status: json['status'] as String,
      userId: (json['user_id'] as num?)?.toInt(),
      priority: (json['priority'] as num).toInt(),
      payload: json['payload'] as Map<String, dynamic>,
      result: json['result'] as Map<String, dynamic>?,
      errorMessage: json['error_message'] as String?,
      retryCount: (json['retry_count'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
      startedAt: json['started_at'] == null
          ? null
          : DateTime.parse(json['started_at'] as String),
      completedAt: json['completed_at'] == null
          ? null
          : DateTime.parse(json['completed_at'] as String),
    );

Map<String, dynamic> _$$BackgroundJobImplToJson(_$BackgroundJobImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'job_type': instance.jobType,
      'status': instance.status,
      'user_id': instance.userId,
      'priority': instance.priority,
      'payload': instance.payload,
      'result': instance.result,
      'error_message': instance.errorMessage,
      'retry_count': instance.retryCount,
      'created_at': instance.createdAt.toIso8601String(),
      'started_at': instance.startedAt?.toIso8601String(),
      'completed_at': instance.completedAt?.toIso8601String(),
    };

_$JobScheduleImpl _$$JobScheduleImplFromJson(Map<String, dynamic> json) =>
    _$JobScheduleImpl(
      id: (json['id'] as num).toInt(),
      jobType: json['job_type'] as String,
      cronExpression: json['cron_expression'] as String,
      enabled: json['enabled'] as bool,
      description: json['description'] as String?,
      lastRun: json['last_run'] == null
          ? null
          : DateTime.parse(json['last_run'] as String),
      nextRun: json['next_run'] == null
          ? null
          : DateTime.parse(json['next_run'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$JobScheduleImplToJson(_$JobScheduleImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'job_type': instance.jobType,
      'cron_expression': instance.cronExpression,
      'enabled': instance.enabled,
      'description': instance.description,
      'last_run': instance.lastRun?.toIso8601String(),
      'next_run': instance.nextRun?.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$DataPipelineImpl _$$DataPipelineImplFromJson(Map<String, dynamic> json) =>
    _$DataPipelineImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      sourceType: json['source_type'] as String,
      destinationType: json['destination_type'] as String,
      status: json['status'] as String,
      isActive: json['is_active'] as bool,
      description: json['description'] as String?,
      schedule: json['schedule'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      lastRun: json['last_run'] == null
          ? null
          : DateTime.parse(json['last_run'] as String),
      lastSuccess: json['last_success'] == null
          ? null
          : DateTime.parse(json['last_success'] as String),
    );

Map<String, dynamic> _$$DataPipelineImplToJson(_$DataPipelineImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'source_type': instance.sourceType,
      'destination_type': instance.destinationType,
      'status': instance.status,
      'is_active': instance.isActive,
      'description': instance.description,
      'schedule': instance.schedule,
      'created_at': instance.createdAt.toIso8601String(),
      'last_run': instance.lastRun?.toIso8601String(),
      'last_success': instance.lastSuccess?.toIso8601String(),
    };

_$PipelineExecutionImpl _$$PipelineExecutionImplFromJson(
        Map<String, dynamic> json) =>
    _$PipelineExecutionImpl(
      id: (json['id'] as num).toInt(),
      pipelineId: (json['pipeline_id'] as num).toInt(),
      status: json['status'] as String,
      recordsProcessed: (json['records_processed'] as num).toInt(),
      recordsFailed: (json['records_failed'] as num).toInt(),
      executionTimeMs: (json['execution_time_ms'] as num?)?.toInt(),
      startedAt: DateTime.parse(json['started_at'] as String),
      completedAt: json['completed_at'] == null
          ? null
          : DateTime.parse(json['completed_at'] as String),
      errorMessage: json['error_message'] as String?,
    );

Map<String, dynamic> _$$PipelineExecutionImplToJson(
        _$PipelineExecutionImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'pipeline_id': instance.pipelineId,
      'status': instance.status,
      'records_processed': instance.recordsProcessed,
      'records_failed': instance.recordsFailed,
      'execution_time_ms': instance.executionTimeMs,
      'started_at': instance.startedAt.toIso8601String(),
      'completed_at': instance.completedAt?.toIso8601String(),
      'error_message': instance.errorMessage,
    };

_$PipelineStageImpl _$$PipelineStageImplFromJson(Map<String, dynamic> json) =>
    _$PipelineStageImpl(
      id: (json['id'] as num).toInt(),
      pipelineId: (json['pipeline_id'] as num).toInt(),
      stageName: json['stage_name'] as String,
      stageOrder: (json['stage_order'] as num).toInt(),
      stageType: json['stage_type'] as String,
      config: json['config'] as Map<String, dynamic>,
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$PipelineStageImplToJson(_$PipelineStageImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'pipeline_id': instance.pipelineId,
      'stage_name': instance.stageName,
      'stage_order': instance.stageOrder,
      'stage_type': instance.stageType,
      'config': instance.config,
      'status': instance.status,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$CacheEntryImpl _$$CacheEntryImplFromJson(Map<String, dynamic> json) =>
    _$CacheEntryImpl(
      cacheKey: json['cache_key'] as String,
      cacheValue: json['cache_value'] as Map<String, dynamic>,
      strategy: json['strategy'] as String,
      ttlSeconds: (json['ttl_seconds'] as num?)?.toInt(),
      hitCount: (json['hit_count'] as num).toInt(),
      sizeBytes: (json['size_bytes'] as num?)?.toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
      expiresAt: json['expires_at'] == null
          ? null
          : DateTime.parse(json['expires_at'] as String),
    );

Map<String, dynamic> _$$CacheEntryImplToJson(_$CacheEntryImpl instance) =>
    <String, dynamic>{
      'cache_key': instance.cacheKey,
      'cache_value': instance.cacheValue,
      'strategy': instance.strategy,
      'ttl_seconds': instance.ttlSeconds,
      'hit_count': instance.hitCount,
      'size_bytes': instance.sizeBytes,
      'created_at': instance.createdAt.toIso8601String(),
      'expires_at': instance.expiresAt?.toIso8601String(),
    };

_$CacheMetricsImpl _$$CacheMetricsImplFromJson(Map<String, dynamic> json) =>
    _$CacheMetricsImpl(
      totalRequests: (json['total_requests'] as num).toInt(),
      totalHits: (json['total_hits'] as num).toInt(),
      totalMisses: (json['total_misses'] as num).toInt(),
      averageResponseTimeMs:
          (json['average_response_time_ms'] as num).toDouble(),
      memoryUsageMb: (json['memory_usage_mb'] as num).toDouble(),
      evictionCount: (json['eviction_count'] as num).toInt(),
      measuredAt: DateTime.parse(json['measured_at'] as String),
    );

Map<String, dynamic> _$$CacheMetricsImplToJson(_$CacheMetricsImpl instance) =>
    <String, dynamic>{
      'total_requests': instance.totalRequests,
      'total_hits': instance.totalHits,
      'total_misses': instance.totalMisses,
      'average_response_time_ms': instance.averageResponseTimeMs,
      'memory_usage_mb': instance.memoryUsageMb,
      'eviction_count': instance.evictionCount,
      'measured_at': instance.measuredAt.toIso8601String(),
    };

_$APIDocumentationImpl _$$APIDocumentationImplFromJson(
        Map<String, dynamic> json) =>
    _$APIDocumentationImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      format: json['format'] as String,
      version: json['version'] as String,
      description: json['description'] as String?,
      basePath: json['base_path'] as String?,
      servers:
          (json['servers'] as List<dynamic>).map((e) => e as String).toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$$APIDocumentationImplToJson(
        _$APIDocumentationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'format': instance.format,
      'version': instance.version,
      'description': instance.description,
      'base_path': instance.basePath,
      'servers': instance.servers,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

_$APIEndpointImpl _$$APIEndpointImplFromJson(Map<String, dynamic> json) =>
    _$APIEndpointImpl(
      id: (json['id'] as num).toInt(),
      path: json['path'] as String,
      method: json['method'] as String,
      summary: json['summary'] as String?,
      description: json['description'] as String?,
      parameters: json['parameters'] as Map<String, dynamic>?,
      requestSchema: json['request_schema'] as Map<String, dynamic>?,
      responseSchema: json['response_schema'] as Map<String, dynamic>?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$APIEndpointImplToJson(_$APIEndpointImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'path': instance.path,
      'method': instance.method,
      'summary': instance.summary,
      'description': instance.description,
      'parameters': instance.parameters,
      'request_schema': instance.requestSchema,
      'response_schema': instance.responseSchema,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$APIUsageMetricsImpl _$$APIUsageMetricsImplFromJson(
        Map<String, dynamic> json) =>
    _$APIUsageMetricsImpl(
      endpoint: json['endpoint'] as String,
      method: json['method'] as String,
      callCount: (json['call_count'] as num).toInt(),
      errorCount: (json['error_count'] as num).toInt(),
      averageResponseTimeMs:
          (json['average_response_time_ms'] as num).toDouble(),
      maxResponseTimeMs: (json['max_response_time_ms'] as num).toDouble(),
      minResponseTimeMs: (json['min_response_time_ms'] as num).toDouble(),
      measuredAt: DateTime.parse(json['measured_at'] as String),
    );

Map<String, dynamic> _$$APIUsageMetricsImplToJson(
        _$APIUsageMetricsImpl instance) =>
    <String, dynamic>{
      'endpoint': instance.endpoint,
      'method': instance.method,
      'call_count': instance.callCount,
      'error_count': instance.errorCount,
      'average_response_time_ms': instance.averageResponseTimeMs,
      'max_response_time_ms': instance.maxResponseTimeMs,
      'min_response_time_ms': instance.minResponseTimeMs,
      'measured_at': instance.measuredAt.toIso8601String(),
    };

_$PlatformMetricsImpl _$$PlatformMetricsImplFromJson(
        Map<String, dynamic> json) =>
    _$PlatformMetricsImpl(
      activeWebSocketConnections:
          (json['active_web_socket_connections'] as num).toInt(),
      pendingBackgroundJobs: (json['pending_background_jobs'] as num).toInt(),
      runningPipelines: (json['running_pipelines'] as num).toInt(),
      totalCacheSize: (json['total_cache_size'] as num).toInt(),
      cacheHitRate: (json['cache_hit_rate'] as num).toDouble(),
      apiAverageResponseTime:
          (json['api_average_response_time'] as num).toDouble(),
    );

Map<String, dynamic> _$$PlatformMetricsImplToJson(
        _$PlatformMetricsImpl instance) =>
    <String, dynamic>{
      'active_web_socket_connections': instance.activeWebSocketConnections,
      'pending_background_jobs': instance.pendingBackgroundJobs,
      'running_pipelines': instance.runningPipelines,
      'total_cache_size': instance.totalCacheSize,
      'cache_hit_rate': instance.cacheHitRate,
      'api_average_response_time': instance.apiAverageResponseTime,
    };
