import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/platform_ops_models.dart';
import 'package:aether_cms/screens/advanced_platform/api_docs_screen.dart';
import 'package:aether_cms/screens/advanced_platform/pipelines_screen.dart';
import 'package:aether_cms/screens/api_versions_screen.dart';
import 'package:aether_cms/screens/cache_screen.dart';
import 'package:aether_cms/services/api_versions_service.dart';
import 'package:aether_cms/services/platform_ops_service.dart';

class MockPlatformOpsService extends Mock implements PlatformOpsService {}

class MockApiVersionsService extends Mock implements ApiVersionsService {}

const _stats = CacheStats(
  totalEntries: 12, hotEntries: 3, warmEntries: 4, coldEntries: 5,
  totalHits: 900, avgHitsPerEntry: 75, hitRate: 0.982,
);

const _policy = CachePolicy(
  resourceType: 'content', cacheType: 'redis', ttlSeconds: 3600, maxSizeMb: 512,
  isActive: true, hits: 90, misses: 10, hitRate: 0.9,
);

void main() {
  late MockPlatformOpsService ops;
  late MockApiVersionsService versions;

  setUp(() {
    ops = MockPlatformOpsService();
    versions = MockApiVersionsService();
  });

  testWidgets('cache screen shows real statistics and the policy for each resource', (tester) async {
    when(() => ops.fetchCacheStats()).thenAnswer((_) async => _stats);
    when(() => ops.fetchCachePolicies()).thenAnswer((_) async => [_policy]);

    await tester.pumpWidget(MaterialApp(home: CacheScreen(service: ops)));
    await tester.pumpAndSettle();

    expect(find.text('98.2%'), findsOneWidget);
    expect(find.text('Hot 3 · Warm 4 · Cold 5'), findsOneWidget);
    expect(find.text('content'), findsOneWidget);
    expect(find.text('redis · 3600s TTL · 512 MB'), findsOneWidget);
  });

  testWidgets('cache screen recovers after a failed load', (tester) async {
    var calls = 0;
    when(() => ops.fetchCacheStats()).thenAnswer((_) async {
      calls++;
      if (calls == 1) throw StateError('Sign in again');
      return _stats;
    });
    when(() => ops.fetchCachePolicies()).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: CacheScreen(service: ops)));
    await tester.pumpAndSettle();
    expect(find.textContaining('Sign in again'), findsOneWidget);

    await tester.tap(find.text('Try again'));
    await tester.pumpAndSettle();
    expect(find.text('No cache policies are configured.'), findsOneWidget);
  });

  testWidgets('pipelines screen lists each pipeline with its route and last run', (tester) async {
    when(() => ops.fetchPipelines()).thenAnswer((_) async => [
          Pipeline(
            id: 1, name: 'Nightly', sourceType: 'postgres', destinationType: 's3', status: 'active',
            isActive: true, failureCount: 2, lastRun: DateTime(2026, 10, 10, 2),
          ),
        ]);

    await tester.pumpWidget(MaterialApp(home: PipelinesScreen(service: ops)));
    await tester.pumpAndSettle();

    expect(find.text('Nightly'), findsOneWidget);
    expect(find.textContaining('postgres → s3'), findsOneWidget);
    expect(find.textContaining('Failures: 2'), findsOneWidget);
    expect(find.text('active'), findsOneWidget);
  });

  testWidgets('pipelines screen says when none are configured', (tester) async {
    when(() => ops.fetchPipelines()).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: PipelinesScreen(service: ops)));
    await tester.pumpAndSettle();

    expect(find.text('No data pipelines are configured.'), findsOneWidget);
  });

  testWidgets('API usage shows calls, error rate and average time per endpoint', (tester) async {
    when(() => ops.fetchApiUsage()).thenAnswer((_) async => [
          const ApiUsage(id: 4, endpoint: '/posts', method: 'GET', callCount: 200, errorCount: 5, averageResponseTimeMs: 42.5),
        ]);

    await tester.pumpWidget(MaterialApp(home: APIDocsScreen(service: ops)));
    await tester.pumpAndSettle();

    expect(find.text('GET /posts'), findsOneWidget);
    expect(find.text('200 calls · 2.5% errors · 43 ms average'), findsOneWidget);
  });

  testWidgets('API versions show deprecation with its sunset date and the migrations', (tester) async {
    when(() => versions.fetchVersions()).thenAnswer((_) async => [
          EndpointVersion(id: 1, endpoint: '/content', version: 'v1', deprecated: true, sunsetDate: DateTime(2027, 1, 31)),
        ]);
    when(() => versions.fetchMigrations()).thenAnswer((_) async => [
          const VersionMigration(id: 2, oldVersion: 'v1', newVersion: 'v2', status: 'completed'),
        ]);

    await tester.pumpWidget(MaterialApp(home: APIVersionsScreen(service: versions)));
    await tester.pumpAndSettle();

    expect(find.textContaining('v1 · deprecated, sunsets 2027-01-31'), findsOneWidget);
    expect(find.text('v1 → v2'), findsOneWidget);
    expect(find.text('completed'), findsOneWidget);
  });
}
