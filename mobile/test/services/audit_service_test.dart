import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/audit_models.dart';
import 'package:aether_cms/services/audit_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late AuditService service;

  setUp(() {
    dio = MockDio();
    service = AuditService(dio);
  });

  test('fetchEntries parses the audit trail and sends paging', () async {
    when(() => dio.get<dynamic>(any(), queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response([
              {
                'id': 2,
                'admin_id': 7,
                'action': 'update',
                'resource_type': 'subscription',
                'changes': {'tier': 'pro'},
                'timestamp': '2026-10-17T09:30:00Z',
              },
            ]));

    final entries = await service.fetchEntries(limit: 20, offset: 40);

    expect(entries.single.action, 'update');
    expect(entries.single.changes, {'tier': 'pro'});
    expect(entries.single.timestamp, DateTime.parse('2026-10-17T09:30:00Z'));
    verify(() => dio.get<dynamic>('/admin/audit-logs', queryParameters: {
          'limit': 20,
          'offset': 40,
        })).called(1);
  });

  test('fetchEntries filters by administrator when asked', () async {
    when(() => dio.get<dynamic>(any(), queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response(<dynamic>[]));

    await service.fetchEntries(adminId: 7);

    verify(() => dio.get<dynamic>('/admin/audit-logs', queryParameters: {
          'limit': 100,
          'offset': 0,
          'admin_id': 7,
        })).called(1);
  });

  test('an entry without changes parses with an empty change set', () {
    final entry = AuditEntry.fromJson({
      'id': 1,
      'admin_id': 1,
      'action': 'login',
      'resource_type': 'session',
      'changes': null,
      'timestamp': '2026-10-17T09:00:00Z',
    });

    expect(entry.changes, isEmpty);
  });
}
