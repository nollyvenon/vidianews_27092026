import 'package:freezed_annotation/freezed_annotation.dart';

part 'platform_completion_models.freezed.dart';
part 'platform_completion_models.g.dart';


@freezed
class UserInteractionModel with _$UserInteractionModel {
  const factory UserInteractionModel({
    required int id,
    required int userId,
    required int contentId,
    required String interactionType,
    required Map<String, dynamic> metadata,
    required DateTime createdAt,
  }) = _UserInteractionModel;

  factory UserInteractionModel.fromJson(Map<String, dynamic> json) =>
      _$UserInteractionModelFromJson(json);
}


@freezed
class UserFollowModel with _$UserFollowModel {
  const factory UserFollowModel({
    required int id,
    required int followerId,
    required int followingId,
    required DateTime createdAt,
  }) = _UserFollowModel;

  factory UserFollowModel.fromJson(Map<String, dynamic> json) =>
      _$UserFollowModelFromJson(json);
}


@freezed
class ContentCommentModel with _$ContentCommentModel {
  const factory ContentCommentModel({
    required int id,
    required int userId,
    required int contentId,
    required String text,
    int? parentCommentId,
    required String status,
    required DateTime createdAt,
  }) = _ContentCommentModel;

  factory ContentCommentModel.fromJson(Map<String, dynamic> json) =>
      _$ContentCommentModelFromJson(json);
}


@freezed
class UserMessageModel with _$UserMessageModel {
  const factory UserMessageModel({
    required int id,
    required int senderId,
    required int recipientId,
    required String text,
    required bool read,
    required DateTime createdAt,
  }) = _UserMessageModel;

  factory UserMessageModel.fromJson(Map<String, dynamic> json) =>
      _$UserMessageModelFromJson(json);
}


@freezed
class SearchIndexModel with _$SearchIndexModel {
  const factory SearchIndexModel({
    required int id,
    required int contentId,
    required String indexType,
    required String title,
    required String content,
    required Map<String, dynamic> metadata,
    required DateTime createdAt,
  }) = _SearchIndexModel;

  factory SearchIndexModel.fromJson(Map<String, dynamic> json) =>
      _$SearchIndexModelFromJson(json);
}


@freezed
class SavedSearchModel with _$SavedSearchModel {
  const factory SavedSearchModel({
    required int id,
    required int userId,
    required String query,
    required Map<String, dynamic> filters,
    required int resultCount,
    required DateTime createdAt,
  }) = _SavedSearchModel;

  factory SavedSearchModel.fromJson(Map<String, dynamic> json) =>
      _$SavedSearchModelFromJson(json);
}


@freezed
class PushNotificationConfigModel with _$PushNotificationConfigModel {
  const factory PushNotificationConfigModel({
    required int id,
    required int userId,
    required String deviceToken,
    required String platform,
    String? deviceName,
    required DateTime lastActive,
    required DateTime createdAt,
  }) = _PushNotificationConfigModel;

  factory PushNotificationConfigModel.fromJson(Map<String, dynamic> json) =>
      _$PushNotificationConfigModelFromJson(json);
}


@freezed
class PushNotificationLogModel with _$PushNotificationLogModel {
  const factory PushNotificationLogModel({
    required int id,
    required int userId,
    required String notificationType,
    required String title,
    required String body,
    required String status,
    required DateTime createdAt,
  }) = _PushNotificationLogModel;

  factory PushNotificationLogModel.fromJson(Map<String, dynamic> json) =>
      _$PushNotificationLogModelFromJson(json);
}


@freezed
class AdminUserModel with _$AdminUserModel {
  const factory AdminUserModel({
    required int id,
    required int userId,
    required String role,
    required List<String> permissions,
    required DateTime createdAt,
  }) = _AdminUserModel;

  factory AdminUserModel.fromJson(Map<String, dynamic> json) =>
      _$AdminUserModelFromJson(json);
}


@freezed
class SystemNotificationModel with _$SystemNotificationModel {
  const factory SystemNotificationModel({
    required int id,
    required String title,
    required String message,
    required String notificationType,
    required DateTime createdAt,
  }) = _SystemNotificationModel;

  factory SystemNotificationModel.fromJson(Map<String, dynamic> json) =>
      _$SystemNotificationModelFromJson(json);
}


@freezed
class PlatformStatisticModel with _$PlatformStatisticModel {
  const factory PlatformStatisticModel({
    required int id,
    required String metricName,
    required double metricValue,
    required String metricType,
    required DateTime createdAt,
  }) = _PlatformStatisticModel;

  factory PlatformStatisticModel.fromJson(Map<String, dynamic> json) =>
      _$PlatformStatisticModelFromJson(json);
}
