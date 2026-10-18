// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'platform_completion_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$UserInteractionModelImpl _$$UserInteractionModelImplFromJson(
        Map<String, dynamic> json) =>
    _$UserInteractionModelImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      interactionType: json['interaction_type'] as String,
      metadata: json['metadata'] as Map<String, dynamic>,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$UserInteractionModelImplToJson(
        _$UserInteractionModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'content_id': instance.contentId,
      'interaction_type': instance.interactionType,
      'metadata': instance.metadata,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$UserFollowModelImpl _$$UserFollowModelImplFromJson(
        Map<String, dynamic> json) =>
    _$UserFollowModelImpl(
      id: (json['id'] as num).toInt(),
      followerId: (json['follower_id'] as num).toInt(),
      followingId: (json['following_id'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$UserFollowModelImplToJson(
        _$UserFollowModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'follower_id': instance.followerId,
      'following_id': instance.followingId,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$ContentCommentModelImpl _$$ContentCommentModelImplFromJson(
        Map<String, dynamic> json) =>
    _$ContentCommentModelImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      text: json['text'] as String,
      parentCommentId: (json['parent_comment_id'] as num?)?.toInt(),
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$ContentCommentModelImplToJson(
        _$ContentCommentModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'content_id': instance.contentId,
      'text': instance.text,
      'parent_comment_id': instance.parentCommentId,
      'status': instance.status,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$UserMessageModelImpl _$$UserMessageModelImplFromJson(
        Map<String, dynamic> json) =>
    _$UserMessageModelImpl(
      id: (json['id'] as num).toInt(),
      senderId: (json['sender_id'] as num).toInt(),
      recipientId: (json['recipient_id'] as num).toInt(),
      text: json['text'] as String,
      read: json['read'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$UserMessageModelImplToJson(
        _$UserMessageModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'sender_id': instance.senderId,
      'recipient_id': instance.recipientId,
      'text': instance.text,
      'read': instance.read,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$SearchIndexModelImpl _$$SearchIndexModelImplFromJson(
        Map<String, dynamic> json) =>
    _$SearchIndexModelImpl(
      id: (json['id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      indexType: json['index_type'] as String,
      title: json['title'] as String,
      content: json['content'] as String,
      metadata: json['metadata'] as Map<String, dynamic>,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$SearchIndexModelImplToJson(
        _$SearchIndexModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'content_id': instance.contentId,
      'index_type': instance.indexType,
      'title': instance.title,
      'content': instance.content,
      'metadata': instance.metadata,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$SavedSearchModelImpl _$$SavedSearchModelImplFromJson(
        Map<String, dynamic> json) =>
    _$SavedSearchModelImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      query: json['query'] as String,
      filters: json['filters'] as Map<String, dynamic>,
      resultCount: (json['result_count'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$SavedSearchModelImplToJson(
        _$SavedSearchModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'query': instance.query,
      'filters': instance.filters,
      'result_count': instance.resultCount,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$PushNotificationConfigModelImpl _$$PushNotificationConfigModelImplFromJson(
        Map<String, dynamic> json) =>
    _$PushNotificationConfigModelImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      deviceToken: json['device_token'] as String,
      platform: json['platform'] as String,
      deviceName: json['device_name'] as String?,
      lastActive: DateTime.parse(json['last_active'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$PushNotificationConfigModelImplToJson(
        _$PushNotificationConfigModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'device_token': instance.deviceToken,
      'platform': instance.platform,
      'device_name': instance.deviceName,
      'last_active': instance.lastActive.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$PushNotificationLogModelImpl _$$PushNotificationLogModelImplFromJson(
        Map<String, dynamic> json) =>
    _$PushNotificationLogModelImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      notificationType: json['notification_type'] as String,
      title: json['title'] as String,
      body: json['body'] as String,
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$PushNotificationLogModelImplToJson(
        _$PushNotificationLogModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'notification_type': instance.notificationType,
      'title': instance.title,
      'body': instance.body,
      'status': instance.status,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$AdminUserModelImpl _$$AdminUserModelImplFromJson(Map<String, dynamic> json) =>
    _$AdminUserModelImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      role: json['role'] as String,
      permissions: (json['permissions'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$AdminUserModelImplToJson(
        _$AdminUserModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'role': instance.role,
      'permissions': instance.permissions,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$SystemNotificationModelImpl _$$SystemNotificationModelImplFromJson(
        Map<String, dynamic> json) =>
    _$SystemNotificationModelImpl(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      message: json['message'] as String,
      notificationType: json['notification_type'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$SystemNotificationModelImplToJson(
        _$SystemNotificationModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'message': instance.message,
      'notification_type': instance.notificationType,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$PlatformStatisticModelImpl _$$PlatformStatisticModelImplFromJson(
        Map<String, dynamic> json) =>
    _$PlatformStatisticModelImpl(
      id: (json['id'] as num).toInt(),
      metricName: json['metric_name'] as String,
      metricValue: (json['metric_value'] as num).toDouble(),
      metricType: json['metric_type'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$PlatformStatisticModelImplToJson(
        _$PlatformStatisticModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'metric_name': instance.metricName,
      'metric_value': instance.metricValue,
      'metric_type': instance.metricType,
      'created_at': instance.createdAt.toIso8601String(),
    };
