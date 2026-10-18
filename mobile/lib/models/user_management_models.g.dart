// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_management_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$SubscriberProfileImpl _$$SubscriberProfileImplFromJson(
        Map<String, dynamic> json) =>
    _$SubscriberProfileImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      subscriptionTier: json['subscription_tier'] as String,
      subscriptionStatus: json['subscription_status'] as String,
      subscriptionStartDate:
          DateTime.parse(json['subscription_start_date'] as String),
      subscriptionEndDate: json['subscription_end_date'] == null
          ? null
          : DateTime.parse(json['subscription_end_date'] as String),
      articlesRead: (json['articles_read'] as num?)?.toInt() ?? 0,
      totalSessionTime: (json['total_session_time'] as num?)?.toDouble() ?? 0.0,
      engagementScore: (json['engagement_score'] as num?)?.toDouble() ?? 0.0,
      churnRiskScore: (json['churn_risk_score'] as num?)?.toDouble() ?? 0.0,
      lastActivityAt: DateTime.parse(json['last_activity_at'] as String),
    );

Map<String, dynamic> _$$SubscriberProfileImplToJson(
        _$SubscriberProfileImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'subscription_tier': instance.subscriptionTier,
      'subscription_status': instance.subscriptionStatus,
      'subscription_start_date':
          instance.subscriptionStartDate.toIso8601String(),
      'subscription_end_date': instance.subscriptionEndDate?.toIso8601String(),
      'articles_read': instance.articlesRead,
      'total_session_time': instance.totalSessionTime,
      'engagement_score': instance.engagementScore,
      'churn_risk_score': instance.churnRiskScore,
      'last_activity_at': instance.lastActivityAt.toIso8601String(),
    };

_$SubscriberActivityImpl _$$SubscriberActivityImplFromJson(
        Map<String, dynamic> json) =>
    _$SubscriberActivityImpl(
      id: (json['id'] as num).toInt(),
      subscriberId: (json['subscriber_id'] as num).toInt(),
      activityType: json['activity_type'] as String,
      contentId: (json['content_id'] as num?)?.toInt(),
      metadata: json['metadata'] as Map<String, dynamic>?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$SubscriberActivityImplToJson(
        _$SubscriberActivityImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'subscriber_id': instance.subscriberId,
      'activity_type': instance.activityType,
      'content_id': instance.contentId,
      'metadata': instance.metadata,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$EmailCampaignImpl _$$EmailCampaignImplFromJson(Map<String, dynamic> json) =>
    _$EmailCampaignImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      templateId: (json['template_id'] as num).toInt(),
      subject: json['subject'] as String,
      fromEmail: json['from_email'] as String,
      recipientCount: (json['recipient_count'] as num).toInt(),
      sentCount: (json['sent_count'] as num).toInt(),
      openCount: (json['open_count'] as num).toInt(),
      clickCount: (json['click_count'] as num).toInt(),
      openRate: (json['open_rate'] as num?)?.toDouble() ?? 0,
      clickRate: (json['click_rate'] as num?)?.toDouble() ?? 0,
      status: json['status'] as String,
      scheduledAt: json['scheduled_at'] == null
          ? null
          : DateTime.parse(json['scheduled_at'] as String),
      sentAt: json['sent_at'] == null
          ? null
          : DateTime.parse(json['sent_at'] as String),
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$EmailCampaignImplToJson(_$EmailCampaignImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'template_id': instance.templateId,
      'subject': instance.subject,
      'from_email': instance.fromEmail,
      'recipient_count': instance.recipientCount,
      'sent_count': instance.sentCount,
      'open_count': instance.openCount,
      'click_count': instance.clickCount,
      'open_rate': instance.openRate,
      'click_rate': instance.clickRate,
      'status': instance.status,
      'scheduled_at': instance.scheduledAt?.toIso8601String(),
      'sent_at': instance.sentAt?.toIso8601String(),
      'created_at': instance.createdAt?.toIso8601String(),
    };

_$UserSegmentImpl _$$UserSegmentImplFromJson(Map<String, dynamic> json) =>
    _$UserSegmentImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      segmentType: json['segment_type'] as String,
      description: json['description'] as String?,
      userCount: (json['user_count'] as num?)?.toInt() ?? 0,
      filterCriteria: json['filter_criteria'] as Map<String, dynamic>?,
    );

Map<String, dynamic> _$$UserSegmentImplToJson(_$UserSegmentImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'segment_type': instance.segmentType,
      'description': instance.description,
      'user_count': instance.userCount,
      'filter_criteria': instance.filterCriteria,
    };

_$UserPreferenceProfileImpl _$$UserPreferenceProfileImplFromJson(
        Map<String, dynamic> json) =>
    _$UserPreferenceProfileImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      preferredCategories: (json['preferred_categories'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      preferredLanguages: (json['preferred_languages'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const ['en'],
      notificationChannels: (json['notification_channels'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const ['email'],
      emailFrequency: json['email_frequency'] as String? ?? 'daily',
      digestEnabled: json['digest_enabled'] as bool? ?? true,
      personalizationEnabled: json['personalization_enabled'] as bool? ?? true,
    );

Map<String, dynamic> _$$UserPreferenceProfileImplToJson(
        _$UserPreferenceProfileImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'preferred_categories': instance.preferredCategories,
      'preferred_languages': instance.preferredLanguages,
      'notification_channels': instance.notificationChannels,
      'email_frequency': instance.emailFrequency,
      'digest_enabled': instance.digestEnabled,
      'personalization_enabled': instance.personalizationEnabled,
    };

_$NotificationMessageImpl _$$NotificationMessageImplFromJson(
        Map<String, dynamic> json) =>
    _$NotificationMessageImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      channel: json['channel'] as String,
      title: json['title'] as String,
      message: json['message'] as String,
      status: json['status'] as String? ?? 'pending',
      readAt: json['read_at'] == null
          ? null
          : DateTime.parse(json['read_at'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$NotificationMessageImplToJson(
        _$NotificationMessageImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'channel': instance.channel,
      'title': instance.title,
      'message': instance.message,
      'status': instance.status,
      'read_at': instance.readAt?.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$WebhookEndpointImpl _$$WebhookEndpointImplFromJson(
        Map<String, dynamic> json) =>
    _$WebhookEndpointImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      url: json['url'] as String,
      events:
          (json['events'] as List<dynamic>).map((e) => e as String).toList(),
      isActive: json['is_active'] as bool? ?? true,
      lastTriggeredAt: json['last_triggered_at'] == null
          ? null
          : DateTime.parse(json['last_triggered_at'] as String),
    );

Map<String, dynamic> _$$WebhookEndpointImplToJson(
        _$WebhookEndpointImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'url': instance.url,
      'events': instance.events,
      'is_active': instance.isActive,
      'last_triggered_at': instance.lastTriggeredAt?.toIso8601String(),
    };

_$APIKeyInfoImpl _$$APIKeyInfoImplFromJson(Map<String, dynamic> json) =>
    _$APIKeyInfoImpl(
      keyId: (json['key_id'] as num).toInt(),
      key: json['key'] as String,
      name: json['name'] as String,
      permissions: (json['permissions'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      isActive: json['is_active'] as bool? ?? true,
    );

Map<String, dynamic> _$$APIKeyInfoImplToJson(_$APIKeyInfoImpl instance) =>
    <String, dynamic>{
      'key_id': instance.keyId,
      'key': instance.key,
      'name': instance.name,
      'permissions': instance.permissions,
      'is_active': instance.isActive,
    };

_$PersonalizationProfileImpl _$$PersonalizationProfileImplFromJson(
        Map<String, dynamic> json) =>
    _$PersonalizationProfileImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      readingLevel: json['reading_level'] as String? ?? 'intermediate',
      contentTypePreferences:
          json['content_type_preferences'] as Map<String, dynamic>? ?? const {},
      authorPreferences: (json['author_preferences'] as List<dynamic>?)
              ?.map((e) => (e as num).toInt())
              .toList() ??
          const [],
      keywordInterests: (json['keyword_interests'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      readingTimePref: (json['reading_time_pref'] as num?)?.toInt() ?? 0,
      timezone: json['timezone'] as String? ?? 'UTC',
      personalizationScore:
          (json['personalization_score'] as num?)?.toDouble() ?? 0.0,
    );

Map<String, dynamic> _$$PersonalizationProfileImplToJson(
        _$PersonalizationProfileImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'reading_level': instance.readingLevel,
      'content_type_preferences': instance.contentTypePreferences,
      'author_preferences': instance.authorPreferences,
      'keyword_interests': instance.keywordInterests,
      'reading_time_pref': instance.readingTimePref,
      'timezone': instance.timezone,
      'personalization_score': instance.personalizationScore,
    };

_$SubscriberAnalyticsImpl _$$SubscriberAnalyticsImplFromJson(
        Map<String, dynamic> json) =>
    _$SubscriberAnalyticsImpl(
      subscriberId: (json['subscriber_id'] as num).toInt(),
      date: DateTime.parse(json['date'] as String),
      dailyActive: json['daily_active'] as bool? ?? false,
      articlesRead: (json['articles_read'] as num?)?.toInt() ?? 0,
      sessionCount: (json['session_count'] as num?)?.toInt() ?? 0,
      avgSessionTime: (json['avg_session_time'] as num?)?.toDouble() ?? 0.0,
      engagementScore: (json['engagement_score'] as num?)?.toDouble() ?? 0.0,
      retentionScore: (json['retention_score'] as num?)?.toDouble() ?? 0.0,
    );

Map<String, dynamic> _$$SubscriberAnalyticsImplToJson(
        _$SubscriberAnalyticsImpl instance) =>
    <String, dynamic>{
      'subscriber_id': instance.subscriberId,
      'date': instance.date.toIso8601String(),
      'daily_active': instance.dailyActive,
      'articles_read': instance.articlesRead,
      'session_count': instance.sessionCount,
      'avg_session_time': instance.avgSessionTime,
      'engagement_score': instance.engagementScore,
      'retention_score': instance.retentionScore,
    };

_$CampaignPerformanceImpl _$$CampaignPerformanceImplFromJson(
        Map<String, dynamic> json) =>
    _$CampaignPerformanceImpl(
      campaignId: (json['campaign_id'] as num).toInt(),
      campaignName: json['campaign_name'] as String,
      recipientCount: (json['recipient_count'] as num).toInt(),
      sentCount: (json['sent_count'] as num).toInt(),
      openCount: (json['open_count'] as num).toInt(),
      clickCount: (json['click_count'] as num).toInt(),
      openRate: (json['open_rate'] as num?)?.toDouble() ?? 0,
      clickRate: (json['click_rate'] as num?)?.toDouble() ?? 0,
      sentAt: DateTime.parse(json['sent_at'] as String),
    );

Map<String, dynamic> _$$CampaignPerformanceImplToJson(
        _$CampaignPerformanceImpl instance) =>
    <String, dynamic>{
      'campaign_id': instance.campaignId,
      'campaign_name': instance.campaignName,
      'recipient_count': instance.recipientCount,
      'sent_count': instance.sentCount,
      'open_count': instance.openCount,
      'click_count': instance.clickCount,
      'open_rate': instance.openRate,
      'click_rate': instance.clickRate,
      'sent_at': instance.sentAt.toIso8601String(),
    };

_$SegmentMetricsImpl _$$SegmentMetricsImplFromJson(Map<String, dynamic> json) =>
    _$SegmentMetricsImpl(
      segmentId: (json['segment_id'] as num).toInt(),
      segmentName: json['segment_name'] as String,
      userCount: (json['user_count'] as num).toInt(),
      avgEngagement: (json['avg_engagement'] as num?)?.toDouble() ?? 0,
      churnRisk: (json['churn_risk'] as num?)?.toDouble() ?? 0.0,
      activeUsers: (json['active_users'] as num?)?.toInt() ?? 0,
    );

Map<String, dynamic> _$$SegmentMetricsImplToJson(
        _$SegmentMetricsImpl instance) =>
    <String, dynamic>{
      'segment_id': instance.segmentId,
      'segment_name': instance.segmentName,
      'user_count': instance.userCount,
      'avg_engagement': instance.avgEngagement,
      'churn_risk': instance.churnRisk,
      'active_users': instance.activeUsers,
    };
