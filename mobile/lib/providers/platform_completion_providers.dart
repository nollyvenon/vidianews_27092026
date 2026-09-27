import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../models/platform_completion_models.dart';


final dioProvider = Provider((ref) => Dio(BaseOptions(
  baseUrl: 'http://localhost:8000',
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 10),
)));


// Social Service Providers
final createInteractionProvider = FutureProvider.family<UserInteractionModel, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.post(
    '/api/v1/platform/interactions',
    data: {
      'content_id': params['content_id'],
      'interaction_type': params['interaction_type'],
      'metadata': params['metadata'] ?? {},
    },
    queryParameters: {'user_id': userId},
  );

  return UserInteractionModel.fromJson(response.data);
});


final userInteractionsProvider = FutureProvider.family<List<UserInteractionModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/my-interactions',
    queryParameters: {
      'user_id': userId,
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => UserInteractionModel.fromJson(e as Map<String, dynamic>)).toList();
});


final contentInteractionsProvider = FutureProvider.family<List<UserInteractionModel>, int>((ref, contentId) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get('/api/v1/platform/interactions/$contentId');

  return (response.data as List).map((e) => UserInteractionModel.fromJson(e as Map<String, dynamic>)).toList();
});


final followUserProvider = FutureProvider.family<UserFollowModel, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;
  final followingId = params['following_id'] as int;

  final response = await dio.post(
    '/api/v1/platform/follow',
    data: {'following_id': followingId},
    queryParameters: {'user_id': userId},
  );

  return UserFollowModel.fromJson(response.data);
});


final followersProvider = FutureProvider.family<List<UserFollowModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/followers/$userId',
    queryParameters: {
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => UserFollowModel.fromJson(e as Map<String, dynamic>)).toList();
});


final followingProvider = FutureProvider.family<List<UserFollowModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/following/$userId',
    queryParameters: {
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => UserFollowModel.fromJson(e as Map<String, dynamic>)).toList();
});


final createCommentProvider = FutureProvider.family<ContentCommentModel, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.post(
    '/api/v1/platform/comments',
    data: {
      'content_id': params['content_id'],
      'text': params['text'],
      'parent_comment_id': params['parent_comment_id'],
    },
    queryParameters: {'user_id': userId},
  );

  return ContentCommentModel.fromJson(response.data);
});


final contentCommentsProvider = FutureProvider.family<List<ContentCommentModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final contentId = params['content_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/comments/$contentId',
    queryParameters: {
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
      'parent_comment_id': params['parent_comment_id'],
    },
  );

  return (response.data as List).map((e) => ContentCommentModel.fromJson(e as Map<String, dynamic>)).toList();
});


final sendMessageProvider = FutureProvider.family<UserMessageModel, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.post(
    '/api/v1/platform/messages',
    data: {
      'recipient_id': params['recipient_id'],
      'text': params['text'],
    },
    queryParameters: {'user_id': userId},
  );

  return UserMessageModel.fromJson(response.data);
});


final conversationProvider = FutureProvider.family<List<UserMessageModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;
  final otherUserId = params['other_user_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/conversations/$otherUserId',
    queryParameters: {
      'user_id': userId,
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => UserMessageModel.fromJson(e as Map<String, dynamic>)).toList();
});


// Search Service Providers
final searchContentProvider = FutureProvider.family<List<SearchIndexModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get(
    '/api/v1/platform/search',
    queryParameters: {
      'query': params['query'],
      'index_type': params['index_type'],
      'limit': params['limit'] ?? 20,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => SearchIndexModel.fromJson(e as Map<String, dynamic>)).toList();
});


final savedSearchesProvider = FutureProvider.family<List<SavedSearchModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/saved-searches',
    queryParameters: {
      'user_id': userId,
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => SavedSearchModel.fromJson(e as Map<String, dynamic>)).toList();
});


// Push Notification Service Providers
final registerDeviceProvider = FutureProvider.family<PushNotificationConfigModel, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.post(
    '/api/v1/platform/devices/register',
    data: {
      'device_token': params['device_token'],
      'platform': params['platform'],
      'device_name': params['device_name'],
    },
    queryParameters: {'user_id': userId},
  );

  return PushNotificationConfigModel.fromJson(response.data);
});


final userDevicesProvider = FutureProvider.family<List<PushNotificationConfigModel>, int>((ref, userId) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get(
    '/api/v1/platform/devices',
    queryParameters: {'user_id': userId},
  );

  return (response.data as List).map((e) => PushNotificationConfigModel.fromJson(e as Map<String, dynamic>)).toList();
});


final notificationLogsProvider = FutureProvider.family<List<PushNotificationLogModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);
  final userId = params['user_id'] as int;

  final response = await dio.get(
    '/api/v1/platform/notifications/logs',
    queryParameters: {
      'user_id': userId,
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => PushNotificationLogModel.fromJson(e as Map<String, dynamic>)).toList();
});


// Admin Service Providers
final adminLogsProvider = FutureProvider.family<List<dynamic>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get(
    '/api/v1/platform/admin/logs',
    queryParameters: {
      'admin_user_id': params['admin_user_id'],
      'action_type': params['action_type'],
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return response.data as List;
});


// System Service Providers
final systemNotificationsProvider = FutureProvider.family<List<SystemNotificationModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get(
    '/api/v1/platform/system/notifications',
    queryParameters: {
      'limit': params['limit'] ?? 50,
      'offset': params['offset'] ?? 0,
    },
  );

  return (response.data as List).map((e) => SystemNotificationModel.fromJson(e as Map<String, dynamic>)).toList();
});


final platformStatisticsProvider = FutureProvider.family<List<PlatformStatisticModel>, Map<String, dynamic>>((ref, params) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get(
    '/api/v1/platform/statistics',
    queryParameters: {
      'metric_name': params['metric_name'],
      'days': params['days'] ?? 7,
      'limit': params['limit'] ?? 100,
    },
  );

  return (response.data as List).map((e) => PlatformStatisticModel.fromJson(e as Map<String, dynamic>)).toList();
});


final dashboardSummaryProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final dio = ref.watch(dioProvider);

  final response = await dio.get('/api/v1/platform/dashboard-summary');

  return response.data as Map<String, dynamic>;
});
