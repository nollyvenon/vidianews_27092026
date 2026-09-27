import 'package:flutter_test/flutter_test.dart';
import '../lib/models/advanced_platform_models.dart';

void main() {
  group('Advanced Platform Models', () {
    test('WebSocketConnection model creation', () {
      final now = DateTime.now();
      final connection = WebSocketConnection(
        id: 1,
        userId: 123,
        connectionId: 'conn123',
        status: 'connected',
        eventSubscriptions: ['all'],
        connectedAt: now,
      );

      expect(connection.id, 1);
      expect(connection.userId, 123);
      expect(connection.status, 'connected');
    });

    test('RealtimeEvent model creation', () {
      final now = DateTime.now();
      final event = RealtimeEvent(
        id: 1,
        eventType: 'update',
        eventSource: 'system',
        userIds: [123, 456],
        payload: {'data': 'test'},
        priority: 0,
        status: 'published',
        createdAt: now,
      );

      expect(event.eventType, 'update');
      expect(event.userIds.length, 2);
    });

    test('BackgroundJob model creation', () {
      final now = DateTime.now();
      final job = BackgroundJob(
        id: 1,
        jobType: 'email',
        status: 'pending',
        payload: {'email': 'test@example.com'},
        priority: 0,
        retryCount: 0,
        createdAt: now,
      );

      expect(job.jobType, 'email');
      expect(job.status, 'pending');
    });

    test('DataPipeline model creation', () {
      final now = DateTime.now();
      final pipeline = DataPipeline(
        id: 1,
        name: 'user_sync',
        sourceType: 'database',
        destinationType: 'warehouse',
        status: 'active',
        isActive: true,
        createdAt: now,
      );

      expect(pipeline.name, 'user_sync');
      expect(pipeline.isActive, true);
    });

    test('PipelineExecution model creation', () {
      final now = DateTime.now();
      final execution = PipelineExecution(
        id: 1,
        pipelineId: 1,
        status: 'success',
        recordsProcessed: 1000,
        recordsFailed: 0,
        startedAt: now,
      );

      expect(execution.recordsProcessed, 1000);
      expect(execution.status, 'success');
    });

    test('CacheEntry model creation', () {
      final now = DateTime.now();
      final entry = CacheEntry(
        cacheKey: 'user:123',
        cacheValue: {'id': 123, 'name': 'John'},
        strategy: 'ttl',
        hitCount: 5,
        createdAt: now,
      );

      expect(entry.cacheKey, 'user:123');
      expect(entry.hitCount, 5);
    });

    test('CacheMetrics model creation', () {
      final now = DateTime.now();
      final metrics = CacheMetrics(
        totalRequests: 100,
        totalHits: 85,
        totalMisses: 15,
        averageResponseTimeMs: 12.5,
        memoryUsageMb: 256.0,
        evictionCount: 0,
        measuredAt: now,
      );

      expect(metrics.totalRequests, 100);
      expect(metrics.averageResponseTimeMs, 12.5);
    });

    test('APIDocumentation model creation', () {
      final now = DateTime.now();
      final doc = APIDocumentation(
        id: 1,
        name: 'Vidi API',
        format: 'openapi3',
        version: '1.0.0',
        servers: ['https://api.example.com'],
        createdAt: now,
        updatedAt: now,
      );

      expect(doc.name, 'Vidi API');
      expect(doc.format, 'openapi3');
    });

    test('APIEndpoint model creation', () {
      final now = DateTime.now();
      final endpoint = APIEndpoint(
        id: 1,
        path: '/users/{id}',
        method: 'GET',
        summary: 'Get user by ID',
        createdAt: now,
      );

      expect(endpoint.path, '/users/{id}');
      expect(endpoint.method, 'GET');
    });

    test('APIUsageMetrics model creation', () {
      final now = DateTime.now();
      final metrics = APIUsageMetrics(
        endpoint: '/users',
        method: 'GET',
        callCount: 1234,
        errorCount: 12,
        averageResponseTimeMs: 45.2,
        maxResponseTimeMs: 234.5,
        minResponseTimeMs: 12.3,
        measuredAt: now,
      );

      expect(metrics.endpoint, '/users');
      expect(metrics.callCount, 1234);
    });

    test('PlatformMetrics model creation', () {
      final metrics = PlatformMetrics(
        activeWebSocketConnections: 50,
        pendingBackgroundJobs: 12,
        runningPipelines: 3,
        totalCacheSize: 512,
        cacheHitRate: 0.85,
        apiAverageResponseTime: 45.2,
      );

      expect(metrics.activeWebSocketConnections, 50);
      expect(metrics.cacheHitRate, 0.85);
    });
  });

  group('Advanced Platform Model Serialization', () {
    test('WebSocketConnection JSON serialization', () {
      final now = DateTime.now();
      final connection = WebSocketConnection(
        id: 1,
        userId: 123,
        connectionId: 'conn123',
        status: 'connected',
        eventSubscriptions: ['all'],
        connectedAt: now,
      );

      final json = connection.toJson();
      expect(json['id'], 1);
      expect(json['user_id'], 123);
      expect(json['connection_id'], 'conn123');
    });

    test('BackgroundJob JSON deserialization', () {
      final now = DateTime.now();
      final json = {
        'id': 1,
        'job_type': 'email',
        'status': 'pending',
        'payload': {'email': 'test@example.com'},
        'priority': 0,
        'retry_count': 0,
        'created_at': now.toIso8601String(),
      };

      final job = BackgroundJob.fromJson(json);
      expect(job.jobType, 'email');
      expect(job.status, 'pending');
    });

    test('DataPipeline JSON serialization', () {
      final now = DateTime.now();
      final pipeline = DataPipeline(
        id: 1,
        name: 'user_sync',
        sourceType: 'database',
        destinationType: 'warehouse',
        status: 'active',
        isActive: true,
        createdAt: now,
      );

      final json = pipeline.toJson();
      expect(json['name'], 'user_sync');
      expect(json['is_active'], true);
    });
  });
}
