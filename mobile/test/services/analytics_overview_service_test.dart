import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/analytics_overview_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late AnalyticsOverviewService service;

  setUp(() {
    dio = MockDio();
    service = AnalyticsOverviewService(dio);
  });

  test('fetchSummary requests the window and parses the headline figures', () async {
    when(() => dio.get<dynamic>('/analytics/summary', queryParameters: {'days': 30})).thenAnswer((_) async => _response({
          'days': 30, 'views': 1200, 'watch_hours': 45.5, 'subscribers': 80,
        }));

    final summary = await service.fetchSummary(days: 30);

    expect(summary.views, 1200);
    expect(summary.watchHours, 45.5);
    expect(summary.subscribers, 80);
  });

  test('fetchEngagement parses each day', () async {
    when(() => dio.get<dynamic>('/analytics/engagement', queryParameters: {'days': 30})).thenAnswer((_) async => _response([
          {'date': '2026-10-10', 'active_users': 40, 'new_users': 5},
        ]));

    final rows = await service.fetchEngagement(days: 30);

    expect(rows.single.activeUsers, 40);
    expect(rows.single.newUsers, 5);
  });

  test('fetchRevenue sends the start and end of the window and parses each day', () async {
    when(() => dio.get<dynamic>('/analytics/revenue', queryParameters: any(named: 'queryParameters'))).thenAnswer((_) async =>
        _response([
          {'date': '2026-10-10', 'total_revenue': 19.99, 'transaction_count': 2},
        ]));

    final rows = await service.fetchRevenue(days: 30);

    expect(rows.single.totalRevenue, 19.99);
    expect(rows.single.transactionCount, 2);
    final query = verify(() => dio.get<dynamic>('/analytics/revenue', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single as Map<String, dynamic>;
    final start = DateTime.parse(query['start_date'] as String);
    final end = DateTime.parse(query['end_date'] as String);
    expect(end.difference(start), const Duration(days: 30));
  });

  test('a non-list engagement response is rejected', () async {
    when(() => dio.get<dynamic>('/analytics/engagement', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({'detail': 'nope'}));

    expect(service.fetchEngagement(), throwsA(isA<FormatException>()));
  });
}
