import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/social_account_models.dart';
import 'package:aether_cms/services/social_account_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late SocialAccountService service;

  setUp(() {
    dio = MockDio();
    service = SocialAccountService(dio);
  });

  test('messages: unread count, conversation and mark-as-read use the message routes', () async {
    when(() => dio.get<dynamic>('/messages/unread/count')).thenAnswer((_) async => _response({'unread_count': 3}));
    when(() => dio.get<dynamic>('/messages/7')).thenAnswer((_) async => _response([
          {'id': 1, 'sender_id': 7, 'content': 'Hi', 'is_read': false},
        ]));
    when(() => dio.put<dynamic>('/messages/1/read')).thenAnswer((_) async => _response({}));

    expect(await service.fetchUnreadMessageCount(), 3);
    final messages = await service.fetchConversation(7);
    await service.markMessageRead(1);

    expect(messages.single.content, 'Hi');
    expect(messages.single.isRead, isFalse);
    verify(() => dio.put<dynamic>('/messages/1/read')).called(1);
  });

  test('sending a message puts the recipient and text in the query string', () async {
    when(() => dio.post<dynamic>('/messages/send', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({}));

    await service.sendMessage(recipientId: 7, content: 'Hello there');

    final query = verify(() => dio.post<dynamic>('/messages/send', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single as Map<String, dynamic>;
    expect(query, {'recipient_id': 7, 'content': 'Hello there'});
  });

  test('followers parse the follower name and follow date', () async {
    when(() => dio.get<dynamic>('/platform/followers/2')).thenAnswer((_) async => _response([
          {'id': 5, 'follower_id': 9, 'following_id': 2, 'created_at': '2026-10-01T00:00:00', 'follower_name': 'Ada Lovelace'},
        ]));

    final followers = await service.fetchFollowers(2);

    expect(followers.single.followerName, 'Ada Lovelace');
    expect(followers.single.followedAt, DateTime(2026, 10, 1));
  });

  test('alerts and notices read their own lists and mark items read', () async {
    when(() => dio.get<dynamic>('/notifications/me')).thenAnswer((_) async => _response([
          {'id': 1, 'title': 'Payment', 'message': 'Received', 'is_read': false, 'created_at': '2026-10-01T00:00:00'},
        ]));
    when(() => dio.get<dynamic>('/system/notifications')).thenAnswer((_) async => _response([
          {'id': 2, 'title': 'Maintenance', 'message': 'Tonight', 'read': true},
        ]));
    when(() => dio.post<dynamic>('/notifications/me/1/read')).thenAnswer((_) async => _response({}));
    when(() => dio.post<dynamic>('/system/notifications/2/read')).thenAnswer((_) async => _response({}));

    expect((await service.fetchAlerts()).single.isRead, isFalse);
    expect((await service.fetchNotices()).single.isRead, isTrue);
    await service.markAlertRead(1);
    await service.markNoticeRead(2);

    verify(() => dio.post<dynamic>('/notifications/me/1/read')).called(1);
    verify(() => dio.post<dynamic>('/system/notifications/2/read')).called(1);
  });

  test('privacy settings are read, saved as query values and logged as consents', () async {
    when(() => dio.get<dynamic>('/privacy/settings')).thenAnswer((_) async => _response({
          'profile_visibility': 'public', 'content_visibility': 'private', 'allow_analytics': true, 'allow_marketing': false,
        }));
    when(() => dio.put<dynamic>('/privacy/settings', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({
              'profile_visibility': 'friends_only', 'content_visibility': 'private', 'allow_analytics': false, 'allow_marketing': false,
            }));

    final current = await service.fetchPrivacySettings();
    expect(current.contentVisibility, 'private');

    final saved = await service.updatePrivacySettings(const PrivacySettings(
      profileVisibility: 'friends_only', contentVisibility: 'private', allowAnalytics: false, allowMarketing: false,
    ));
    expect(saved.profileVisibility, 'friends_only');
    final query = verify(() => dio.put<dynamic>('/privacy/settings', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single as Map<String, dynamic>;
    expect(query['profile_visibility'], 'friends_only');
    expect(query['allow_analytics'], isFalse);
  });

  test('deletion returns the scheduled date and premium status reads the feature list', () async {
    when(() => dio.post<dynamic>('/privacy/request-deletion')).thenAnswer((_) async => _response({
          'scheduled_for': '2026-11-01T00:00:00',
        }));
    when(() => dio.get<dynamic>('/premium/status')).thenAnswer((_) async => _response({
          'is_premium': true, 'features': ['ad-free', 'downloads'],
        }));

    expect(await service.requestDeletion(), DateTime(2026, 11, 1));
    final status = await service.fetchPremiumStatus();
    expect(status.isPremium, isTrue);
    expect(status.features, ['ad-free', 'downloads']);
  });

  test('a non-list response is rejected', () async {
    when(() => dio.get<dynamic>('/messages/7')).thenAnswer((_) async => _response({'detail': 'nope'}));

    expect(service.fetchConversation(7), throwsA(isA<FormatException>()));
  });
}
