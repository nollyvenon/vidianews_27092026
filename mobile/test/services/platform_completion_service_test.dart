import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/platform_completion_service.dart';

class MockDio extends Mock implements Dio {}

Response<T> _response<T>(T? data, {int statusCode = 200}) => Response<T>(
      data: data,
      statusCode: statusCode,
      requestOptions: RequestOptions(path: ''),
    );

Map<String, dynamic> _interactionJson() => {
      'id': 7,
      'user_id': 1,
      'content_id': 42,
      'interaction_type': 'like',
      'metadata': <String, dynamic>{},
      'created_at': '2026-09-27T10:00:00Z',
    };

void main() {
  late MockDio dio;
  late PlatformCompletionService service;

  setUp(() {
    dio = MockDio();
    service = PlatformCompletionService(dio: dio);
  });

  group('PlatformCompletionService interactions', () {
    test('recordInteraction posts the interaction and returns the parsed model', () async {
      when(() => dio.post<Map<String, dynamic>>(any(), data: any(named: 'data')))
          .thenAnswer((_) async => _response<Map<String, dynamic>>(_interactionJson()));

      final model = await service.recordInteraction(contentId: 42, interactionType: 'like');

      expect(model.id, 7);
      expect(model.contentId, 42);
      expect(model.interactionType, 'like');
      verify(() => dio.post<Map<String, dynamic>>(
            '/api/v1/platform/interactions',
            data: {'content_id': 42, 'interaction_type': 'like'},
          )).called(1);
    });

    test('getContentInteractions decodes every item in the list', () async {
      when(() => dio.get<List<dynamic>>(any()))
          .thenAnswer((_) async => _response<List<dynamic>>([_interactionJson(), _interactionJson()]));

      final items = await service.getContentInteractions(42);

      expect(items, hasLength(2));
      expect(items.first.contentId, 42);
    });

    test('getContentInteractions returns an empty list when the body is null', () async {
      when(() => dio.get<List<dynamic>>(any()))
          .thenAnswer((_) async => _response<List<dynamic>>(null));

      expect(await service.getContentInteractions(42), isEmpty);
    });

    test('removeInteraction deletes the interaction for the content id', () async {
      when(() => dio.delete<void>(any())).thenAnswer((_) async => _response<void>(null, statusCode: 204));

      await service.removeInteraction(42);

      verify(() => dio.delete<void>('/api/v1/platform/interactions/42')).called(1);
    });
  });

  group('PlatformCompletionService follows, comments, and messages', () {
    test('unfollow deletes the follow relationship', () async {
      when(() => dio.delete<void>(any())).thenAnswer((_) async => _response<void>(null, statusCode: 204));

      await service.unfollow(5);

      verify(() => dio.delete<void>('/api/v1/platform/follow/5')).called(1);
    });

    test('addComment posts the comment and includes the parent id when replying', () async {
      when(() => dio.post<Map<String, dynamic>>(any(), data: any(named: 'data'))).thenAnswer(
        (_) async => _response<Map<String, dynamic>>({
          'id': 9,
          'user_id': 1,
          'content_id': 42,
          'text': 'Reply',
          'parent_comment_id': 3,
          'status': 'approved',
          'created_at': '2026-09-27T10:00:00Z',
        }),
      );

      final comment = await service.addComment(contentId: 42, text: 'Reply', parentCommentId: 3);

      expect(comment.parentCommentId, 3);
      verify(() => dio.post<Map<String, dynamic>>(
            '/api/v1/platform/comments',
            data: {'content_id': 42, 'text': 'Reply', 'parent_comment_id': 3},
          )).called(1);
    });

    test('sendMessage posts to the recipient and returns the stored message', () async {
      when(() => dio.post<Map<String, dynamic>>(any(), data: any(named: 'data'))).thenAnswer(
        (_) async => _response<Map<String, dynamic>>({
          'id': 11,
          'sender_id': 1,
          'recipient_id': 2,
          'text': 'Hello',
          'read': false,
          'created_at': '2026-09-27T10:00:00Z',
        }),
      );

      final message = await service.sendMessage(recipientId: 2, text: 'Hello');

      expect(message.recipientId, 2);
      expect(message.read, isFalse);
    });
  });
}
