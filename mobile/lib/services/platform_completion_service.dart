import 'package:dio/dio.dart';

import '../models/platform_completion_models.dart';

/// Client for the social features of the platform completion API:
/// content interactions, follows, comments, and direct messages.
///
/// Paths are relative to the base URL configured on the injected [Dio].
class PlatformCompletionService {
  static const String _basePath = '/api/v1/platform';

  final Dio _dio;

  PlatformCompletionService({required Dio dio}) : _dio = dio;

  // ---------------------------------------------------------------- interactions

  Future<UserInteractionModel> recordInteraction({
    required int contentId,
    required String interactionType,
    Map<String, dynamic>? metadata,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '$_basePath/interactions',
      data: {
        'content_id': contentId,
        'interaction_type': interactionType,
        if (metadata != null) 'metadata': metadata,
      },
    );
    return UserInteractionModel.fromJson(response.data!);
  }

  Future<List<UserInteractionModel>> getContentInteractions(int contentId) async {
    final response = await _dio.get<List<dynamic>>('$_basePath/interactions/$contentId');
    return _decodeList(response.data, UserInteractionModel.fromJson);
  }

  Future<List<UserInteractionModel>> getMyInteractions() async {
    final response = await _dio.get<List<dynamic>>('$_basePath/my-interactions');
    return _decodeList(response.data, UserInteractionModel.fromJson);
  }

  Future<void> removeInteraction(int contentId) async {
    await _dio.delete<void>('$_basePath/interactions/$contentId');
  }

  // ---------------------------------------------------------------- follows

  Future<UserFollowModel> follow(int followingId) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '$_basePath/follow',
      data: {'following_id': followingId},
    );
    return UserFollowModel.fromJson(response.data!);
  }

  Future<void> unfollow(int followingId) async {
    await _dio.delete<void>('$_basePath/follow/$followingId');
  }

  Future<List<UserFollowModel>> getFollowers(int userId) async {
    final response = await _dio.get<List<dynamic>>('$_basePath/followers/$userId');
    return _decodeList(response.data, UserFollowModel.fromJson);
  }

  Future<List<UserFollowModel>> getFollowing(int userId) async {
    final response = await _dio.get<List<dynamic>>('$_basePath/following/$userId');
    return _decodeList(response.data, UserFollowModel.fromJson);
  }

  // ---------------------------------------------------------------- comments

  Future<ContentCommentModel> addComment({
    required int contentId,
    required String text,
    int? parentCommentId,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '$_basePath/comments',
      data: {
        'content_id': contentId,
        'text': text,
        if (parentCommentId != null) 'parent_comment_id': parentCommentId,
      },
    );
    return ContentCommentModel.fromJson(response.data!);
  }

  Future<List<ContentCommentModel>> getComments(int contentId) async {
    final response = await _dio.get<List<dynamic>>('$_basePath/comments/$contentId');
    return _decodeList(response.data, ContentCommentModel.fromJson);
  }

  Future<void> deleteComment(int commentId) async {
    await _dio.delete<void>('$_basePath/comments/$commentId');
  }

  // ---------------------------------------------------------------- messages

  Future<UserMessageModel> sendMessage({required int recipientId, required String text}) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '$_basePath/messages',
      data: {'recipient_id': recipientId, 'text': text},
    );
    return UserMessageModel.fromJson(response.data!);
  }

  Future<List<UserMessageModel>> getConversation(int otherUserId) async {
    final response = await _dio.get<List<dynamic>>('$_basePath/conversations/$otherUserId');
    return _decodeList(response.data, UserMessageModel.fromJson);
  }

  Future<void> markMessageRead(int messageId) async {
    await _dio.post<void>('$_basePath/messages/$messageId/read');
  }

  static List<T> _decodeList<T>(List<dynamic>? raw, T Function(Map<String, dynamic>) fromJson) {
    if (raw == null) return <T>[];
    return raw.map((item) => fromJson(item as Map<String, dynamic>)).toList();
  }
}
