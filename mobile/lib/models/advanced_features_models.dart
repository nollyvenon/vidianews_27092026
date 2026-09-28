import 'package:freezed_annotation/freezed_annotation.dart';

part 'advanced_features_models.freezed.dart';
part 'advanced_features_models.g.dart';

@freezed
class PersonalizationProfile with _$PersonalizationProfile {
  const factory PersonalizationProfile({
    required int id,
    required int userId,
    required Map<String, double> contentPreferences,
    required Map<String, double> authorPreferences,
    required Map<String, double> categoryWeights,
    String? readingTimePreference,
    required double personalizationScore,
    required DateTime lastUpdated,
  }) = _PersonalizationProfile;

  factory PersonalizationProfile.fromJson(Map<String, dynamic> json) =>
      _$PersonalizationProfileFromJson(json);
}

@freezed
class ContentRecommendation with _$ContentRecommendation {
  const factory ContentRecommendation({
    required int id,
    required int userId,
    required int contentId,
    required String type,
    required double similarityScore,
    required double relevanceScore,
    required bool clicked,
    required bool conversion,
    DateTime? clickTimestamp,
  }) = _ContentRecommendation;

  factory ContentRecommendation.fromJson(Map<String, dynamic> json) =>
      _$ContentRecommendationFromJson(json);
}

@freezed
class RecommendationEffectiveness with _$RecommendationEffectiveness {
  const factory RecommendationEffectiveness({
    required int totalRecommendations,
    required int clicks,
    required int conversions,
    required double clickThroughRate,
    required double conversionRate,
  }) = _RecommendationEffectiveness;

  factory RecommendationEffectiveness.fromJson(Map<String, dynamic> json) =>
      _$RecommendationEffectivenessFromJson(json);
}

@freezed
class RetentionMetric with _$RetentionMetric {
  const factory RetentionMetric({
    required int id,
    required int userId,
    required String status,
    required double churnProbability,
    required int daysSinceActive,
    String? engagementTrend,
    String? retentionSegment,
    String? recommendedAction,
    DateTime? lastEngagement,
  }) = _RetentionMetric;

  factory RetentionMetric.fromJson(Map<String, dynamic> json) =>
      _$RetentionMetricFromJson(json);
}

@freezed
class RetentionCampaign with _$RetentionCampaign {
  const factory RetentionCampaign({
    required int id,
    required String name,
    String? description,
    required String status,
    required String targetSegment,
    String? campaignType,
    required int sentCount,
    required int convertedCount,
    required double roi,
  }) = _RetentionCampaign;

  factory RetentionCampaign.fromJson(Map<String, dynamic> json) =>
      _$RetentionCampaignFromJson(json);
}

@freezed
class ABTest with _$ABTest {
  const factory ABTest({
    required int id,
    required String name,
    String? description,
    String? hypothesis,
    required String status,
    required String metricToOptimize,
    required String variantAName,
    required String variantBName,
    required double metricA,
    required double metricB,
    required double confidence,
    String? winner,
    DateTime? startDate,
    DateTime? endDate,
  }) = _ABTest;

  factory ABTest.fromJson(Map<String, dynamic> json) => _$ABTestFromJson(json);
}

@freezed
class ABTestVariant with _$ABTestVariant {
  const factory ABTestVariant({
    required int id,
    required int abTestId,
    required int userId,
    required String variant,
    required bool conversion,
    required double metricValue,
    required DateTime assignedAt,
  }) = _ABTestVariant;

  factory ABTestVariant.fromJson(Map<String, dynamic> json) =>
      _$ABTestVariantFromJson(json);
}

@freezed
class AnalyticsInsight with _$AnalyticsInsight {
  const factory AnalyticsInsight({
    required int id,
    required String type,
    required String title,
    String? description,
    required Map<String, dynamic> data,
    String? metricName,
    double? metricValue,
    String? trend,
    required double confidenceLevel,
    required bool actionable,
    String? recommendedAction,
    required DateTime createdAt,
  }) = _AnalyticsInsight;

  factory AnalyticsInsight.fromJson(Map<String, dynamic> json) =>
      _$AnalyticsInsightFromJson(json);
}

@freezed
class UserCohort with _$UserCohort {
  const factory UserCohort({
    required int id,
    required String name,
    String? description,
    required String cohortType,
    required Map<String, dynamic> criteria,
    required int userCount,
    required DateTime createdAt,
  }) = _UserCohort;

  factory UserCohort.fromJson(Map<String, dynamic> json) =>
      _$UserCohortFromJson(json);
}

@freezed
class PredictionModel with _$PredictionModel {
  const factory PredictionModel({
    required int id,
    required String name,
    required String modelType,
    required String targetMetric,
    required double accuracy,
    required double precision,
    required double recall,
    required double f1Score,
    required double aucScore,
    required bool deployed,
    DateTime? lastTrained,
  }) = _PredictionModel;

  factory PredictionModel.fromJson(Map<String, dynamic> json) =>
      _$PredictionModelFromJson(json);
}

@freezed
class UserPrediction with _$UserPrediction {
  const factory UserPrediction({
    required int id,
    required int userId,
    required int modelId,
    required double predictionScore,
    required double confidence,
    String? predictedBehavior,
    String? actualBehavior,
    required DateTime createdAt,
  }) = _UserPrediction;

  factory UserPrediction.fromJson(Map<String, dynamic> json) =>
      _$UserPredictionFromJson(json);
}

@freezed
class RecommendationListResponse with _$RecommendationListResponse {
  const factory RecommendationListResponse({
    required List<ContentRecommendation> recommendations,
    required int totalCount,
  }) = _RecommendationListResponse;

  factory RecommendationListResponse.fromJson(Map<String, dynamic> json) =>
      _$RecommendationListResponseFromJson(json);
}

@freezed
class CohortMemberResponse with _$CohortMemberResponse {
  const factory CohortMemberResponse({
    required int cohortId,
    required int memberCount,
    required List<int> members,
  }) = _CohortMemberResponse;

  factory CohortMemberResponse.fromJson(Map<String, dynamic> json) =>
      _$CohortMemberResponseFromJson(json);
}

@freezed
class UserPredictionListResponse with _$UserPredictionListResponse {
  const factory UserPredictionListResponse({
    required int userId,
    required List<UserPrediction> predictions,
  }) = _UserPredictionListResponse;

  factory UserPredictionListResponse.fromJson(Map<String, dynamic> json) =>
      _$UserPredictionListResponseFromJson(json);
}
