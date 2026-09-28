import 'package:freezed_annotation/freezed_annotation.dart';

part 'publishing_distribution_models.freezed.dart';
part 'publishing_distribution_models.g.dart';

@freezed
class PublishingJob with _$PublishingJob {
  const factory PublishingJob({
    required int id,
    required String title,
    required String status,
    required DateTime scheduledPublishTime,
    DateTime? actualPublishTime,
    required List<String> distributionChannels,
    @Default(false) bool autoPromote,
  }) = _PublishingJob;

  factory PublishingJob.fromJson(Map<String, dynamic> json) =>
      _$PublishingJobFromJson(json);
}

@freezed
class EngagementMetric with _$EngagementMetric {
  const factory EngagementMetric({
    required int id,
    required int contentId,
    required int views,
    required int clicks,
    required int shares,
    required double ctr,
    @Default(0) double engagementRate,
    @Default(0) double shareRate,
    @Default(0) double conversionRate,
    @Default(0) double engagementScore,
    required DateTime recordedAt,
  }) = _EngagementMetric;

  factory EngagementMetric.fromJson(Map<String, dynamic> json) =>
      _$EngagementMetricFromJson(json);
}

@freezed
class ABTestCampaign with _$ABTestCampaign {
  const factory ABTestCampaign({
    required int id,
    required String name,
    required String testMetric,
    required String hypothesis,
    required String status,
    DateTime? startDate,
    DateTime? endDate,
    @Default(0) double statisticalSignificance,
  }) = _ABTestCampaign;

  factory ABTestCampaign.fromJson(Map<String, dynamic> json) =>
      _$ABTestCampaignFromJson(json);
}

@freezed
class ABTestVariant with _$ABTestVariant {
  const factory ABTestVariant({
    required int id,
    required int campaignId,
    required String variantName,
    @Default(0) int conversions,
    @Default(0) int impressions,
    @Default(0) double conversionRate,
    @Default(0) double ctr,
    bool? isWinner,
  }) = _ABTestVariant;

  factory ABTestVariant.fromJson(Map<String, dynamic> json) =>
      _$ABTestVariantFromJson(json);
}

@freezed
class RecommendedContent with _$RecommendedContent {
  const factory RecommendedContent({
    required int contentId,
    required String title,
    required double matchScore,
    @Default('content') String contentType,
    List<String>? tags,
    DateTime? publishedAt,
  }) = _RecommendedContent;

  factory RecommendedContent.fromJson(Map<String, dynamic> json) =>
      _$RecommendedContentFromJson(json);
}

@freezed
class UserPreference with _$UserPreference {
  const factory UserPreference({
    required int id,
    required int userId,
    required String category,
    required double preferenceScore,
    @Default(0) int interactionCount,
  }) = _UserPreference;

  factory UserPreference.fromJson(Map<String, dynamic> json) =>
      _$UserPreferenceFromJson(json);
}

@freezed
class DistributionChannel with _$DistributionChannel {
  const factory DistributionChannel({
    required int id,
    required String channelName,
    required String status,
    @Default(0) int reach,
    @Default(0) double engagementRate,
    @Default(0) int impressions,
  }) = _DistributionChannel;

  factory DistributionChannel.fromJson(Map<String, dynamic> json) =>
      _$DistributionChannelFromJson(json);
}

@freezed
class SyndicationPartner with _$SyndicationPartner {
  const factory SyndicationPartner({
    required int id,
    required String partnerName,
    @Default(0) int articlesSyndicated,
    @Default(0) int totalReach,
    DateTime? lastSyndicationDate,
    @Default('active') String status,
  }) = _SyndicationPartner;

  factory SyndicationPartner.fromJson(Map<String, dynamic> json) =>
      _$SyndicationPartnerFromJson(json);
}

@freezed
class AnalyticsSnapshot with _$AnalyticsSnapshot {
  const factory AnalyticsSnapshot({
    required int contentId,
    required int views,
    required int clicks,
    required int shares,
    required double engagementScore,
    @Default(0) double trend,
    required DateTime timestamp,
  }) = _AnalyticsSnapshot;

  factory AnalyticsSnapshot.fromJson(Map<String, dynamic> json) =>
      _$AnalyticsSnapshotFromJson(json);
}

@freezed
class RecommendationPerformance with _$RecommendationPerformance {
  const factory RecommendationPerformance({
    required int totalRecommendations,
    required int clicks,
    required int conversions,
    @Default(0) double clickThroughRate,
    @Default(0) double conversionRate,
    @Default(0) double avgReadTime,
  }) = _RecommendationPerformance;

  factory RecommendationPerformance.fromJson(Map<String, dynamic> json) =>
      _$RecommendationPerformanceFromJson(json);
}
