import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/api_versions_service.dart';
import 'package:aether_cms/services/platform_ops_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;

  setUp(() {
    dio = MockDio();
  });

  group('PlatformOpsService', () {
    late PlatformOpsService service;

    setUp(() {
      service = PlatformOpsService(dio);
    });

    test('fetchCacheStats parses the summary document', () async {
      when(() => dio.get<dynamic>('/cache/stats/summary')).thenAnswer((_) async => _response({
            'total_entries': 12, 'hot_entries': 3, 'warm_entries': 4, 'cold_entries': 5,
            'total_hits': 900, 'avg_hits_per_entry': 75.0, 'hit_rate': 0.982,
          }));

      final stats = await service.fetchCacheStats();

      expect(stats.totalEntries, 12);
      expect(stats.hitRate, closeTo(0.982, 1e-9));
    });

    test('fetchCachePolicies parses each policy', () async {
      when(() => dio.get<dynamic>('/cache/policies')).thenAnswer((_) async => _response([
            {
              'resource_type': 'content', 'cache_type': 'redis', 'ttl_seconds': 3600, 'max_size_mb': 512,
              'is_active': true, 'hits': 90, 'misses': 10, 'hit_rate': 0.9,
            },
          ]));

      final policies = await service.fetchCachePolicies();

      expect(policies.single.resourceType, 'content');
      expect(policies.single.ttlSeconds, 3600);
    });

    test('fetchPipelines parses run dates and failure counts', () async {
      when(() => dio.get<dynamic>('/pipelines/')).thenAnswer((_) async => _response([
            {
              'id': 1, 'name': 'Nightly', 'source_type': 'postgres', 'destination_type': 's3', 'status': 'active',
              'is_active': true, 'failure_count': 2, 'last_run': '2026-10-10T02:00:00', 'last_success': null,
            },
          ]));

      final pipelines = await service.fetchPipelines();

      expect(pipelines.single.name, 'Nightly');
      expect(pipelines.single.failureCount, 2);
      expect(pipelines.single.lastRun, DateTime(2026, 10, 10, 2));
      expect(pipelines.single.lastSuccess, isNull);
    });

    test('fetchApiUsage computes the error rate', () async {
      when(() => dio.get<dynamic>('/api-docs/usage')).thenAnswer((_) async => _response([
            {'id': 4, 'endpoint': '/posts', 'method': 'GET', 'call_count': 200, 'error_count': 5, 'average_response_time_ms': 42.5},
          ]));

      final usage = await service.fetchApiUsage();

      expect(usage.single.errorRate, closeTo(0.025, 1e-9));
    });

    test('a response that is not a list is rejected', () async {
      when(() => dio.get<dynamic>('/pipelines/')).thenAnswer((_) async => _response({'detail': 'nope'}));

      expect(service.fetchPipelines(), throwsA(isA<FormatException>()));
    });
  });

  group('ApiVersionsService', () {
    late ApiVersionsService service;

    setUp(() {
      service = ApiVersionsService(dio);
    });

    test('fetchVersions parses deprecation and sunset dates', () async {
      when(() => dio.get<dynamic>('/versions')).thenAnswer((_) async => _response([
            {'id': 1, 'endpoint': '/content', 'version': 'v1', 'deprecated': true, 'sunset_date': '2027-01-31T00:00:00'},
          ]));

      final versions = await service.fetchVersions();

      expect(versions.single.deprecated, isTrue);
      expect(versions.single.sunsetDate, DateTime(2027, 1, 31));
    });

    test('fetchMigrations parses the migration list', () async {
      when(() => dio.get<dynamic>('/versions/migrations')).thenAnswer((_) async => _response([
            {'id': 2, 'old_version': 'v1', 'new_version': 'v2', 'status': 'completed', 'executed_at': null},
          ]));

      final migrations = await service.fetchMigrations();

      expect(migrations.single.newVersion, 'v2');
      expect(migrations.single.executedAt, isNull);
    });
  });
}
