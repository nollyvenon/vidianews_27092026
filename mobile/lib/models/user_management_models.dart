import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_management_models.freezed.dart';
part 'user_management_models.g.dart';

@freezed
class SubscriberProfile with _$SubscriberProfile {
  const factory SubscriberProfile({
    required int id,
    required int userId,
    required String subscriptionTier,
    required String subscriptionStatus,
    required DateTime subscriptionStartDate,
    DateTime? subscriptionEndDate,
    @Default(0) int articlesRead,
    @Default(0.0) double totalSessionTime,
    @Default(0.0) double engagementScore,
    @Default(0.0) double churnRiskScore,
    required DateTime lastActivityAt,
  }) = _SubscriberProfile;

  factory SubscriberProfile.fromJson(Map<String, dynamic> json) =>
      _$SubscriberProfileFromJson(json);
}

@freezed
class SubscriberActivity with _$SubscriberActivity {
  const factory SubscriberActivity({
    required int id,
    required int subscriberId,
    required String activityType,
    int? contentId,
    Map<String, dynamic>? metadata,
    required DateTime createdAt,
  }) = _SubscriberActivity;

  factory SubscriberActivity.fromJson(Map<String, dynamic> json) =>
      _$SubscriberActivityFromJson(json);
}

@freezed
class EmailCampaign with _$EmailCampaign {
  const factory EmailCampaign({
    required int id,
    required String name,
    required int templateId,
    required String subject,
    required String fromEmail,
    required int recipientCount,
    required int sentCount,
    required int openCount,
    required int clickCount,
    @Default(0) double openRate,
    @Default(0) double clickRate,
    required String status,
    DateTime? scheduledAt,
    DateTime? sentAt,
  }) = _EmailCampaign;

  factory EmailCampaign.fromJson(Map<String, dynamic> json) =>
      _$EmailCampaignFromJson(json);
}

@freezed
class UserSegment with _$UserSegment {
  const factory UserSegment({
    required int id,
    required String name,
    required String segmentType,
    String? description,
    @Default(0) int userCount,
    Map<String, dynamic>? filterCriteria,
  }) = _UserSegment;

  factory UserSegment.fromJson(Map<String, dynamic> json) =>
      _$UserSegmentFromJson(json);
}

@freezed
class UserPreferenceProfile with _$UserPreferenceProfile {
  const factory UserPreferenceProfile({
    required int id,
    required int userId,
    required List<String> preferredCategories,
    @Default(['en']) List<String> preferredLanguages,
    @Default(['email']) List<String> notificationChannels,
    @Default('daily') String emailFrequency,
    @Default(true) bool digestEnabled,
    @Default(true) bool personalizationEnabled,
  }) = _UserPreferenceProfile;

  factory UserPreferenceProfile.fromJson(Map<String, dynamic> json) =>
      _$UserPreferenceProfileFromJson(json);
}

@freezed
class NotificationMessage with _$NotificationMessage {
  const factory NotificationMessage({
    required int id,
    required int userId,
    required String channel,
    required String title,
    required String message,
    @Default('pending') String status,
    DateTime? readAt,
    required DateTime createdAt,
  }) = _NotificationMessage;

  factory NotificationMessage.fromJson(Map<String, dynamic> json) =>
      _$NotificationMessageFromJson(json);
}

@freezed
class WebhookEndpoint with _$WebhookEndpoint {
  const factory WebhookEndpoint({
    required int id,
    required String name,
    required String url,
    required List<String> events,
    @Default(true) bool isActive,
    DateTime? lastTriggeredAt,
  }) = _WebhookEndpoint;

  factory WebhookEndpoint.fromJson(Map<String, dynamic> json) =>
      _$WebhookEndpointFromJson(json);
}

@freezed
class APIKeyInfo with _$APIKeyInfo {
  const factory APIKeyInfo({
    required int keyId,
    required String key,
    required String name,
    required List<String> permissions,
    @Default(true) bool isActive,
  }) = _APIKeyInfo;

  factory APIKeyInfo.fromJson(Map<String, dynamic> json) =>
      _$APIKeyInfoFromJson(json);
}

@freezed
class PersonalizationProfile with _$PersonalizationProfile {
  const factory PersonalizationProfile({
    required int id,
    required int userId,
    @Default('intermediate') String readingLevel,
    @Default({}) Map<String, dynamic> contentTypePreferences,
    @Default([]) List<int> authorPreferences,
    @Default([]) List<String> keywordInterests,
    @Default(0) int readingTimePref,
    @Default('UTC') String timezone,
    @Default(0.0) double personalizationScore,
  }) = _PersonalizationProfile;

  factory PersonalizationProfile.fromJson(Map<String, dynamic> json) =>
      _$PersonalizationProfileFromJson(json);
}

@freezed
class SubscriberAnalytics with _$SubscriberAnalytics {
  const factory SubscriberAnalytics({
    required int subscriberId,
    required DateTime date,
    @Default(false) bool dailyActive,
    @Default(0) int articlesRead,
    @Default(0) int sessionCount,
    @Default(0.0) double avgSessionTime,
    @Default(0.0) double engagementScore,
    @Default(0.0) double retentionScore,
  }) = _SubscriberAnalytics;

  factory SubscriberAnalytics.fromJson(Map<String, dynamic> json) =>
      _$SubscriberAnalyticsFromJson(json);
}

@freezed
class CampaignPerformance with _$CampaignPerformance {
  const factory CampaignPerformance({
    required int campaignId,
    required String campaignName,
    required int recipientCount,
    required int sentCount,
    required int openCount,
    required int clickCount,
    @Default(0) double openRate,
    @Default(0) double clickRate,
    required DateTime sentAt,
  }) = _CampaignPerformance;

  factory CampaignPerformance.fromJson(Map<String, dynamic> json) =>
      _$CampaignPerformanceFromJson(json);
}

@freezed
class SegmentMetrics with _$SegmentMetrics {
  const factory SegmentMetrics({
    required int segmentId,
    required String segmentName,
    required int userCount,
    @Default(0) double avgEngagement,
    @Default(0.0) double churnRisk,
    @Default(0) int activeUsers,
  }) = _SegmentMetrics;

  factory SegmentMetrics.fromJson(Map<String, dynamic> json) =>
      _$SegmentMetricsFromJson(json);
}
