import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart';
import '../lib/models/platform_completion_models.dart';
import '../lib/services/platform_completion_service.dart';


class MockDio extends Mock implements Dio {}


void main() {
  group('Platform Completion Models', () {
    test('UserInteractionModel.fromJson', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'content_id': 1,
        'interaction_type': 'like',
        'metadata': {'sentiment': 'positive'},
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = UserInteractionModel.fromJson(json);

      expect(model.id, 1);
      expect(model.userId, 1);
      expect(model.contentId, 1);
      expect(model.interactionType, 'like');
    });

    test('UserFollowModel.fromJson', () {
      final json = {
        'id': 1,
        'follower_id': 1,
        'following_id': 2,
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = UserFollowModel.fromJson(json);

      expect(model.id, 1);
      expect(model.followerId, 1);
      expect(model.followingId, 2);
    });

    test('ContentCommentModel.fromJson', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'content_id': 1,
        'text': 'Great content!',
        'parent_comment_id': null,
        'status': 'approved',
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = ContentCommentModel.fromJson(json);

      expect(model.id, 1);
      expect(model.text, 'Great content!');
      expect(model.status, 'approved');
    });

    test('UserMessageModel.fromJson', () {
      final json = {
        'id': 1,
        'sender_id': 1,
        'recipient_id': 2,
        'text': 'Hello!',
        'read': false,
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = UserMessageModel.fromJson(json);

      expect(model.id, 1);
      expect(model.senderId, 1);
      expect(model.recipientId, 2);
      expect(model.read, false);
    });

    test('SearchIndexModel.fromJson', () {
      final json = {
        'id': 1,
        'content_id': 1,
        'index_type': 'content',
        'title': 'Test Title',
        'content': 'Test content',
        'metadata': {},
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = SearchIndexModel.fromJson(json);

      expect(model.id, 1);
      expect(model.title, 'Test Title');
      expect(model.indexType, 'content');
    });

    test('SavedSearchModel.fromJson', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'query': 'flutter',
        'filters': {},
        'result_count': 100,
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = SavedSearchModel.fromJson(json);

      expect(model.id, 1);
      expect(model.query, 'flutter');
      expect(model.resultCount, 100);
    });

    test('PushNotificationConfigModel.fromJson', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'device_token': 'token123',
        'platform': 'ios',
        'device_name': 'iPhone 12',
        'last_active': '2026-09-27T10:00:00Z',
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = PushNotificationConfigModel.fromJson(json);

      expect(model.id, 1);
      expect(model.deviceToken, 'token123');
      expect(model.platform, 'ios');
    });

    test('PushNotificationLogModel.fromJson', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'notification_type': 'engagement',
        'title': 'New Like',
        'body': 'Someone liked your post',
        'status': 'delivered',
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = PushNotificationLogModel.fromJson(json);

      expect(model.id, 1);
      expect(model.notificationType, 'engagement');
      expect(model.status, 'delivered');
    });

    test('AdminUserModel.fromJson', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'role': 'moderator',
        'permissions': ['delete_content', 'block_user'],
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = AdminUserModel.fromJson(json);

      expect(model.id, 1);
      expect(model.role, 'moderator');
      expect(model.permissions.length, 2);
    });

    test('SystemNotificationModel.fromJson', () {
      final json = {
        'id': 1,
        'title': 'Maintenance',
        'message': 'System will be down',
        'notification_type': 'system',
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = SystemNotificationModel.fromJson(json);

      expect(model.id, 1);
      expect(model.title, 'Maintenance');
    });

    test('PlatformStatisticModel.fromJson', () {
      final json = {
        'id': 1,
        'metric_name': 'active_users',
        'metric_value': 1500.0,
        'metric_type': 'count',
        'created_at': '2026-09-27T10:00:00Z',
      };

      final model = PlatformStatisticModel.fromJson(json);

      expect(model.id, 1);
      expect(model.metricName, 'active_users');
      expect(model.metricValue, 1500.0);
    });
  });

  group('Platform Completion Serialization', () {
    test('UserInteractionModel serializes to JSON', () {
      final now = DateTime.now();
      final model = UserInteractionModel(
        id: 1,
        userId: 1,
        contentId: 1,
        interactionType: 'like',
        metadata: {'sentiment': 'positive'},
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['user_id'], 1);
      expect(json['interaction_type'], 'like');
    });

    test('UserFollowModel serializes to JSON', () {
      final now = DateTime.now();
      final model = UserFollowModel(
        id: 1,
        followerId: 1,
        followingId: 2,
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['follower_id'], 1);
      expect(json['following_id'], 2);
    });

    test('ContentCommentModel serializes to JSON', () {
      final now = DateTime.now();
      final model = ContentCommentModel(
        id: 1,
        userId: 1,
        contentId: 1,
        text: 'Great!',
        status: 'approved',
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['text'], 'Great!');
      expect(json['status'], 'approved');
    });

    test('UserMessageModel serializes to JSON', () {
      final now = DateTime.now();
      final model = UserMessageModel(
        id: 1,
        senderId: 1,
        recipientId: 2,
        text: 'Hello!',
        read: false,
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['sender_id'], 1);
      expect(json['text'], 'Hello!');
    });

    test('SearchIndexModel serializes to JSON', () {
      final now = DateTime.now();
      final model = SearchIndexModel(
        id: 1,
        contentId: 1,
        indexType: 'content',
        title: 'Test',
        content: 'Content',
        metadata: {},
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['title'], 'Test');
    });

    test('SavedSearchModel serializes to JSON', () {
      final now = DateTime.now();
      final model = SavedSearchModel(
        id: 1,
        userId: 1,
        query: 'test',
        filters: {},
        resultCount: 50,
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['query'], 'test');
    });

    test('PushNotificationConfigModel serializes to JSON', () {
      final now = DateTime.now();
      final model = PushNotificationConfigModel(
        id: 1,
        userId: 1,
        deviceToken: 'token',
        platform: 'ios',
        lastActive: now,
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['device_token'], 'token');
    });

    test('AdminUserModel serializes to JSON', () {
      final now = DateTime.now();
      final model = AdminUserModel(
        id: 1,
        userId: 1,
        role: 'admin',
        permissions: ['all'],
        createdAt: now,
      );

      final json = model.toJson();

      expect(json['id'], 1);
      expect(json['role'], 'admin');
    });
  });

  group('Platform Completion Equality', () {
    test('UserInteractionModel equality', () {
      final now = DateTime.now();
      final model1 = UserInteractionModel(
        id: 1,
        userId: 1,
        contentId: 1,
        interactionType: 'like',
        metadata: {},
        createdAt: now,
      );
      final model2 = UserInteractionModel(
        id: 1,
        userId: 1,
        contentId: 1,
        interactionType: 'like',
        metadata: {},
        createdAt: now,
      );

      expect(model1, model2);
    });

    test('UserFollowModel equality', () {
      final now = DateTime.now();
      final model1 = UserFollowModel(
        id: 1,
        followerId: 1,
        followingId: 2,
        createdAt: now,
      );
      final model2 = UserFollowModel(
        id: 1,
        followerId: 1,
        followingId: 2,
        createdAt: now,
      );

      expect(model1, model2);
    });
  });

  group('Platform Completion Copying', () {
    test('UserInteractionModel copyWith', () {
      final now = DateTime.now();
      final model = UserInteractionModel(
        id: 1,
        userId: 1,
        contentId: 1,
        interactionType: 'like',
        metadata: {},
        createdAt: now,
      );

      final copied = model.copyWith(interactionType: 'share');

      expect(copied.id, model.id);
      expect(copied.interactionType, 'share');
    });

    test('ContentCommentModel copyWith', () {
      final now = DateTime.now();
      final model = ContentCommentModel(
        id: 1,
        userId: 1,
        contentId: 1,
        text: 'Original',
        status: 'approved',
        createdAt: now,
      );

      final copied = model.copyWith(text: 'Updated');

      expect(copied.id, model.id);
      expect(copied.text, 'Updated');
    });

    test('SearchIndexModel copyWith', () {
      final now = DateTime.now();
      final model = SearchIndexModel(
        id: 1,
        contentId: 1,
        indexType: 'content',
        title: 'Original',
        content: 'Content',
        metadata: {},
        createdAt: now,
      );

      final copied = model.copyWith(title: 'Updated');

      expect(copied.title, 'Updated');
    });
  });
}
