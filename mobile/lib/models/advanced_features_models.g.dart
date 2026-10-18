// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'advanced_features_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$PersonalizationProfileImpl _$$PersonalizationProfileImplFromJson(
        Map<String, dynamic> json) =>
    _$PersonalizationProfileImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      contentPreferences:
          (json['content_preferences'] as Map<String, dynamic>).map(
        (k, e) => MapEntry(k, (e as num).toDouble()),
      ),
      authorPreferences:
          (json['author_preferences'] as Map<String, dynamic>).map(
        (k, e) => MapEntry(k, (e as num).toDouble()),
      ),
      categoryWeights: (json['category_weights'] as Map<String, dynamic>).map(
        (k, e) => MapEntry(k, (e as num).toDouble()),
      ),
      readingTimePreference: json['reading_time_preference'] as String?,
      personalizationScore: (json['personalization_score'] as num).toDouble(),
      lastUpdated: DateTime.parse(json['last_updated'] as String),
    );

Map<String, dynamic> _$$PersonalizationProfileImplToJson(
        _$PersonalizationProfileImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'content_preferences': instance.contentPreferences,
      'author_preferences': instance.authorPreferences,
      'category_weights': instance.categoryWeights,
      'reading_time_preference': instance.readingTimePreference,
      'personalization_score': instance.personalizationScore,
      'last_updated': instance.lastUpdated.toIso8601String(),
    };

_$ContentRecommendationImpl _$$ContentRecommendationImplFromJson(
        Map<String, dynamic> json) =>
    _$ContentRecommendationImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      type: json['type'] as String,
      similarityScore: (json['similarity_score'] as num).toDouble(),
      relevanceScore: (json['relevance_score'] as num).toDouble(),
      clicked: json['clicked'] as bool,
      conversion: json['conversion'] as bool,
      clickTimestamp: json['click_timestamp'] == null
          ? null
          : DateTime.parse(json['click_timestamp'] as String),
    );

Map<String, dynamic> _$$ContentRecommendationImplToJson(
        _$ContentRecommendationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'content_id': instance.contentId,
      'type': instance.type,
      'similarity_score': instance.similarityScore,
      'relevance_score': instance.relevanceScore,
      'clicked': instance.clicked,
      'conversion': instance.conversion,
      'click_timestamp': instance.clickTimestamp?.toIso8601String(),
    };

_$RecommendationEffectivenessImpl _$$RecommendationEffectivenessImplFromJson(
        Map<String, dynamic> json) =>
    _$RecommendationEffectivenessImpl(
      totalRecommendations: (json['total_recommendations'] as num).toInt(),
      clicks: (json['clicks'] as num).toInt(),
      conversions: (json['conversions'] as num).toInt(),
      clickThroughRate: (json['click_through_rate'] as num).toDouble(),
      conversionRate: (json['conversion_rate'] as num).toDouble(),
    );

Map<String, dynamic> _$$RecommendationEffectivenessImplToJson(
        _$RecommendationEffectivenessImpl instance) =>
    <String, dynamic>{
      'total_recommendations': instance.totalRecommendations,
      'clicks': instance.clicks,
      'conversions': instance.conversions,
      'click_through_rate': instance.clickThroughRate,
      'conversion_rate': instance.conversionRate,
    };

_$RetentionMetricImpl _$$RetentionMetricImplFromJson(
        Map<String, dynamic> json) =>
    _$RetentionMetricImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      status: json['status'] as String,
      churnProbability: (json['churn_probability'] as num).toDouble(),
      daysSinceActive: (json['days_since_active'] as num).toInt(),
      engagementTrend: json['engagement_trend'] as String?,
      retentionSegment: json['retention_segment'] as String?,
      recommendedAction: json['recommended_action'] as String?,
      lastEngagement: json['last_engagement'] == null
          ? null
          : DateTime.parse(json['last_engagement'] as String),
    );

Map<String, dynamic> _$$RetentionMetricImplToJson(
        _$RetentionMetricImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'status': instance.status,
      'churn_probability': instance.churnProbability,
      'days_since_active': instance.daysSinceActive,
      'engagement_trend': instance.engagementTrend,
      'retention_segment': instance.retentionSegment,
      'recommended_action': instance.recommendedAction,
      'last_engagement': instance.lastEngagement?.toIso8601String(),
    };

_$RetentionCampaignImpl _$$RetentionCampaignImplFromJson(
        Map<String, dynamic> json) =>
    _$RetentionCampaignImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      status: json['status'] as String,
      targetSegment: json['target_segment'] as String,
      campaignType: json['campaign_type'] as String?,
      sentCount: (json['sent_count'] as num).toInt(),
      convertedCount: (json['converted_count'] as num).toInt(),
      roi: (json['roi'] as num).toDouble(),
    );

Map<String, dynamic> _$$RetentionCampaignImplToJson(
        _$RetentionCampaignImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'status': instance.status,
      'target_segment': instance.targetSegment,
      'campaign_type': instance.campaignType,
      'sent_count': instance.sentCount,
      'converted_count': instance.convertedCount,
      'roi': instance.roi,
    };

_$ABTestImpl _$$ABTestImplFromJson(Map<String, dynamic> json) => _$ABTestImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      hypothesis: json['hypothesis'] as String?,
      status: json['status'] as String,
      metricToOptimize: json['metric_to_optimize'] as String,
      variantAName: json['variant_a_name'] as String,
      variantBName: json['variant_b_name'] as String,
      metricA: (json['metric_a'] as num).toDouble(),
      metricB: (json['metric_b'] as num).toDouble(),
      confidence: (json['confidence'] as num).toDouble(),
      winner: json['winner'] as String?,
      startDate: json['start_date'] == null
          ? null
          : DateTime.parse(json['start_date'] as String),
      endDate: json['end_date'] == null
          ? null
          : DateTime.parse(json['end_date'] as String),
    );

Map<String, dynamic> _$$ABTestImplToJson(_$ABTestImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'hypothesis': instance.hypothesis,
      'status': instance.status,
      'metric_to_optimize': instance.metricToOptimize,
      'variant_a_name': instance.variantAName,
      'variant_b_name': instance.variantBName,
      'metric_a': instance.metricA,
      'metric_b': instance.metricB,
      'confidence': instance.confidence,
      'winner': instance.winner,
      'start_date': instance.startDate?.toIso8601String(),
      'end_date': instance.endDate?.toIso8601String(),
    };

_$ABTestVariantImpl _$$ABTestVariantImplFromJson(Map<String, dynamic> json) =>
    _$ABTestVariantImpl(
      id: (json['id'] as num).toInt(),
      abTestId: (json['ab_test_id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      variant: json['variant'] as String,
      conversion: json['conversion'] as bool,
      metricValue: (json['metric_value'] as num).toDouble(),
      assignedAt: DateTime.parse(json['assigned_at'] as String),
    );

Map<String, dynamic> _$$ABTestVariantImplToJson(_$ABTestVariantImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'ab_test_id': instance.abTestId,
      'user_id': instance.userId,
      'variant': instance.variant,
      'conversion': instance.conversion,
      'metric_value': instance.metricValue,
      'assigned_at': instance.assignedAt.toIso8601String(),
    };

_$AnalyticsInsightImpl _$$AnalyticsInsightImplFromJson(
        Map<String, dynamic> json) =>
    _$AnalyticsInsightImpl(
      id: (json['id'] as num).toInt(),
      type: json['type'] as String,
      title: json['title'] as String,
      description: json['description'] as String?,
      data: json['data'] as Map<String, dynamic>,
      metricName: json['metric_name'] as String?,
      metricValue: (json['metric_value'] as num?)?.toDouble(),
      trend: json['trend'] as String?,
      confidenceLevel: (json['confidence_level'] as num).toDouble(),
      actionable: json['actionable'] as bool,
      recommendedAction: json['recommended_action'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$AnalyticsInsightImplToJson(
        _$AnalyticsInsightImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'type': instance.type,
      'title': instance.title,
      'description': instance.description,
      'data': instance.data,
      'metric_name': instance.metricName,
      'metric_value': instance.metricValue,
      'trend': instance.trend,
      'confidence_level': instance.confidenceLevel,
      'actionable': instance.actionable,
      'recommended_action': instance.recommendedAction,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$UserCohortImpl _$$UserCohortImplFromJson(Map<String, dynamic> json) =>
    _$UserCohortImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      cohortType: json['cohort_type'] as String,
      criteria: json['criteria'] as Map<String, dynamic>,
      userCount: (json['user_count'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$UserCohortImplToJson(_$UserCohortImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'cohort_type': instance.cohortType,
      'criteria': instance.criteria,
      'user_count': instance.userCount,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$PredictionModelImpl _$$PredictionModelImplFromJson(
        Map<String, dynamic> json) =>
    _$PredictionModelImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      modelType: json['model_type'] as String,
      targetMetric: json['target_metric'] as String,
      accuracy: (json['accuracy'] as num).toDouble(),
      precision: (json['precision'] as num).toDouble(),
      recall: (json['recall'] as num).toDouble(),
      f1Score: (json['f1_score'] as num).toDouble(),
      aucScore: (json['auc_score'] as num).toDouble(),
      deployed: json['deployed'] as bool,
      lastTrained: json['last_trained'] == null
          ? null
          : DateTime.parse(json['last_trained'] as String),
    );

Map<String, dynamic> _$$PredictionModelImplToJson(
        _$PredictionModelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'model_type': instance.modelType,
      'target_metric': instance.targetMetric,
      'accuracy': instance.accuracy,
      'precision': instance.precision,
      'recall': instance.recall,
      'f1_score': instance.f1Score,
      'auc_score': instance.aucScore,
      'deployed': instance.deployed,
      'last_trained': instance.lastTrained?.toIso8601String(),
    };

_$UserPredictionImpl _$$UserPredictionImplFromJson(Map<String, dynamic> json) =>
    _$UserPredictionImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      modelId: (json['model_id'] as num).toInt(),
      predictionScore: (json['prediction_score'] as num).toDouble(),
      confidence: (json['confidence'] as num).toDouble(),
      predictedBehavior: json['predicted_behavior'] as String?,
      actualBehavior: json['actual_behavior'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$UserPredictionImplToJson(
        _$UserPredictionImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'model_id': instance.modelId,
      'prediction_score': instance.predictionScore,
      'confidence': instance.confidence,
      'predicted_behavior': instance.predictedBehavior,
      'actual_behavior': instance.actualBehavior,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$RecommendationListResponseImpl _$$RecommendationListResponseImplFromJson(
        Map<String, dynamic> json) =>
    _$RecommendationListResponseImpl(
      recommendations: (json['recommendations'] as List<dynamic>)
          .map((e) => ContentRecommendation.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalCount: (json['total_count'] as num).toInt(),
    );

Map<String, dynamic> _$$RecommendationListResponseImplToJson(
        _$RecommendationListResponseImpl instance) =>
    <String, dynamic>{
      'recommendations': instance.recommendations,
      'total_count': instance.totalCount,
    };

_$CohortMemberResponseImpl _$$CohortMemberResponseImplFromJson(
        Map<String, dynamic> json) =>
    _$CohortMemberResponseImpl(
      cohortId: (json['cohort_id'] as num).toInt(),
      memberCount: (json['member_count'] as num).toInt(),
      members: (json['members'] as List<dynamic>)
          .map((e) => (e as num).toInt())
          .toList(),
    );

Map<String, dynamic> _$$CohortMemberResponseImplToJson(
        _$CohortMemberResponseImpl instance) =>
    <String, dynamic>{
      'cohort_id': instance.cohortId,
      'member_count': instance.memberCount,
      'members': instance.members,
    };

_$UserPredictionListResponseImpl _$$UserPredictionListResponseImplFromJson(
        Map<String, dynamic> json) =>
    _$UserPredictionListResponseImpl(
      userId: (json['user_id'] as num).toInt(),
      predictions: (json['predictions'] as List<dynamic>)
          .map((e) => UserPrediction.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$UserPredictionListResponseImplToJson(
        _$UserPredictionListResponseImpl instance) =>
    <String, dynamic>{
      'user_id': instance.userId,
      'predictions': instance.predictions,
    };
