import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/community_service.dart';
import 'package:aether_cms/services/content_quality_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late CommunityService service;

  setUp(() {
    dio = MockDio();
    service = CommunityService(dio);
  });

  test('comments are read for a content item and posted with its id', () async {
    when(() => dio.get<dynamic>('/platform/comments/4')).thenAnswer((_) async => _response([
          {'id': 1, 'user_id': 2, 'content_id': 4, 'text': 'Nice', 'status': 'published', 'created_at': '2026-10-01T00:00:00'},
        ]));
    when(() => dio.post<dynamic>('/platform/comments', data: any(named: 'data'))).thenAnswer((_) async => _response(
          {'id': 2, 'user_id': 2, 'content_id': 4, 'text': 'Thanks', 'status': 'published'},
        ));

    final comments = await service.fetchComments(4);
    final posted = await service.postComment(contentId: 4, text: 'Thanks');

    expect(comments.single.text, 'Nice');
    expect(posted.id, 2);
    final sent = verify(() => dio.post<dynamic>('/platform/comments', data: captureAny(named: 'data'))).captured.single;
    expect(sent, {'content_id': 4, 'text': 'Thanks'});
  });

  test('devices are listed, registered and removed', () async {
    when(() => dio.get<dynamic>('/platform/devices')).thenAnswer((_) async => _response([
          {'id': 3, 'device_token': 'tok', 'platform': 'ios', 'device_name': 'Phone', 'last_active': '2026-10-01T00:00:00'},
        ]));
    when(() => dio.post<dynamic>('/platform/devices/register', data: any(named: 'data'))).thenAnswer((_) async => _response(
          {'id': 4, 'device_token': 'tok2', 'platform': 'android', 'device_name': null, 'last_active': '2026-10-01T00:00:00'},
        ));
    when(() => dio.delete<dynamic>('/platform/devices/3')).thenAnswer((_) async => _response({}));

    expect((await service.fetchDevices()).single.deviceName, 'Phone');
    final registered = await service.registerDevice(token: 'tok2', platform: 'android');
    await service.removeDevice(3);

    expect(registered.platform, 'android');
    verify(() => dio.delete<dynamic>('/platform/devices/3')).called(1);
  });

  test('notification logs are read', () async {
    when(() => dio.get<dynamic>('/platform/notifications/logs')).thenAnswer((_) async => _response([
          {'id': 5, 'notification_type': 'system', 'title': 'Hi', 'body': 'Body', 'status': 'delivered'},
        ]));

    expect((await service.fetchNotificationLogs()).single.status, 'delivered');
  });

  test('webhooks are listed, created with their events and tested', () async {
    when(() => dio.get<dynamic>('/outbound-webhooks')).thenAnswer((_) async => _response([
          {'id': 6, 'url': 'https://hooks.example.com/x', 'description': null, 'events': ['content.published'], 'is_active': true},
        ]));
    when(() => dio.get<dynamic>('/outbound-webhooks/events')).thenAnswer((_) async => _response([
          {'event': 'content.published', 'description': 'Published'},
        ]));
    when(() => dio.post<dynamic>('/outbound-webhooks', data: any(named: 'data'))).thenAnswer((_) async => _response(
          {'id': 7, 'url': 'https://hooks.example.com/y', 'description': 'Mine', 'events': ['content.published'], 'is_active': true},
        ));
    when(() => dio.post<dynamic>('/outbound-webhooks/6/test')).thenAnswer((_) async => _response({'status': 'delivered'}));

    expect((await service.fetchWebhooks()).single.events, ['content.published']);
    expect((await service.fetchWebhookEvents()).single.event, 'content.published');
    final created = await service.createWebhook(url: 'https://hooks.example.com/y', events: ['content.published'], description: 'Mine');
    final result = await service.testWebhook(6);

    expect(created.id, 7);
    expect(result['status'], 'delivered');
    final sent = verify(() => dio.post<dynamic>('/outbound-webhooks', data: captureAny(named: 'data'))).captured.single as Map<String, dynamic>;
    expect(sent['events'], ['content.published']);
  });

  test('a non-list response is rejected', () async {
    when(() => dio.get<dynamic>('/platform/devices')).thenAnswer((_) async => _response({'detail': 'nope'}));

    expect(service.fetchDevices(), throwsA(isA<FormatException>()));
  });

  test('the content quality overview reads each tool\'s checks and averages', () async {
    final dio = MockDio();
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response({
          'proofreading': {'checks': 2, 'average_score': 88.5},
          'readability': {'checks': 0, 'average_grade': null},
          'brand_voice': {'checks': 1, 'average_compliance': 70.0},
          'plagiarism': {'checks': 3, 'average_similarity': 4.25},
        }));

    final overview = await ContentQualityService(dio).fetchOverview();

    expect(overview.proofreadingChecks, 2);
    expect(overview.averageProofreadingScore, 88.5);
    expect(overview.averageReadabilityGrade, isNull);
    expect(overview.averagePlagiarismSimilarity, 4.25);
  });
}
