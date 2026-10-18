import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/account_service.dart';
import 'package:aether_cms/services/dashboard_service.dart';

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

  group('DashboardService', () {
    late DashboardService service;

    setUp(() {
      service = DashboardService(dio);
    });

    test('fetchSummary parses the signed-in user totals', () async {
      when(() => dio.get<dynamic>('/dashboard/summary')).thenAnswer((_) async => _response({
            'videos': 3, 'articles': 2, 'chats': 7, 'monthly_spend': 15.5,
          }));

      final summary = await service.fetchSummary();

      expect(summary.videos, 3);
      expect(summary.articles, 2);
      expect(summary.chats, 7);
      expect(summary.monthlySpend, 15.5);
    });

    test('fetchRecentActivity asks for five entries by default and parses them', () async {
      when(() => dio.get<dynamic>('/activity/me', queryParameters: any(named: 'queryParameters')))
          .thenAnswer((_) async => _response([
                {'id': 1, 'action': 'create', 'entity_type': 'content', 'description': 'Published a video', 'created_at': '2026-10-10T10:00:00'},
              ]));

      final entries = await service.fetchRecentActivity();

      expect(entries.single.description, 'Published a video');
      final query = verify(() => dio.get<dynamic>('/activity/me', queryParameters: captureAny(named: 'queryParameters')))
          .captured
          .single as Map<String, dynamic>;
      expect(query, {'limit': 5});
    });

    test('a non-list activity response is rejected', () async {
      when(() => dio.get<dynamic>('/activity/me', queryParameters: any(named: 'queryParameters')))
          .thenAnswer((_) async => _response({'detail': 'nope'}));

      expect(service.fetchRecentActivity(), throwsA(isA<FormatException>()));
    });
  });

  group('AccountService', () {
    test('fetchCurrentUserId reads the id of the signed-in user', () async {
      when(() => dio.get<dynamic>('/auth/me')).thenAnswer((_) async => _response({'id': 42, 'email': 'a@example.com'}));

      expect(await AccountService(dio).fetchCurrentUserId(), 42);
    });

    test('a response without a user id is rejected', () async {
      when(() => dio.get<dynamic>('/auth/me')).thenAnswer((_) async => _response({'email': 'a@example.com'}));

      expect(AccountService(dio).fetchCurrentUserId(), throwsA(isA<FormatException>()));
    });
  });
}
