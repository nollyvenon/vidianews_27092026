// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'publishing_distribution_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$PublishingJobImpl _$$PublishingJobImplFromJson(Map<String, dynamic> json) =>
    _$PublishingJobImpl(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      status: json['status'] as String,
      scheduledPublishTime:
          DateTime.parse(json['scheduled_publish_time'] as String),
      actualPublishTime: json['actual_publish_time'] == null
          ? null
          : DateTime.parse(json['actual_publish_time'] as String),
      distributionChannels: (json['distribution_channels'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      autoPromote: json['auto_promote'] as bool? ?? false,
    );

Map<String, dynamic> _$$PublishingJobImplToJson(_$PublishingJobImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'status': instance.status,
      'scheduled_publish_time': instance.scheduledPublishTime.toIso8601String(),
      'actual_publish_time': instance.actualPublishTime?.toIso8601String(),
      'distribution_channels': instance.distributionChannels,
      'auto_promote': instance.autoPromote,
    };

_$EngagementMetricImpl _$$EngagementMetricImplFromJson(
        Map<String, dynamic> json) =>
    _$EngagementMetricImpl(
      id: (json['id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      views: (json['views'] as num).toInt(),
      clicks: (json['clicks'] as num).toInt(),
      shares: (json['shares'] as num).toInt(),
      ctr: (json['ctr'] as num).toDouble(),
      engagementRate: (json['engagement_rate'] as num?)?.toDouble() ?? 0,
      shareRate: (json['share_rate'] as num?)?.toDouble() ?? 0,
      conversionRate: (json['conversion_rate'] as num?)?.toDouble() ?? 0,
      engagementScore: (json['engagement_score'] as num?)?.toDouble() ?? 0,
      recordedAt: DateTime.parse(json['recorded_at'] as String),
    );

Map<String, dynamic> _$$EngagementMetricImplToJson(
        _$EngagementMetricImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'content_id': instance.contentId,
      'views': instance.views,
      'clicks': instance.clicks,
      'shares': instance.shares,
      'ctr': instance.ctr,
      'engagement_rate': instance.engagementRate,
      'share_rate': instance.shareRate,
      'conversion_rate': instance.conversionRate,
      'engagement_score': instance.engagementScore,
      'recorded_at': instance.recordedAt.toIso8601String(),
    };

_$ABTestCampaignImpl _$$ABTestCampaignImplFromJson(Map<String, dynamic> json) =>
    _$ABTestCampaignImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      testMetric: json['test_metric'] as String,
      hypothesis: json['hypothesis'] as String,
      status: json['status'] as String,
      startDate: json['start_date'] == null
          ? null
          : DateTime.parse(json['start_date'] as String),
      endDate: json['end_date'] == null
          ? null
          : DateTime.parse(json['end_date'] as String),
      statisticalSignificance:
          (json['statistical_significance'] as num?)?.toDouble() ?? 0,
    );

Map<String, dynamic> _$$ABTestCampaignImplToJson(
        _$ABTestCampaignImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'test_metric': instance.testMetric,
      'hypothesis': instance.hypothesis,
      'status': instance.status,
      'start_date': instance.startDate?.toIso8601String(),
      'end_date': instance.endDate?.toIso8601String(),
      'statistical_significance': instance.statisticalSignificance,
    };

_$ABTestVariantImpl _$$ABTestVariantImplFromJson(Map<String, dynamic> json) =>
    _$ABTestVariantImpl(
      id: (json['id'] as num).toInt(),
      campaignId: (json['campaign_id'] as num).toInt(),
      variantName: json['variant_name'] as String,
      conversions: (json['conversions'] as num?)?.toInt() ?? 0,
      impressions: (json['impressions'] as num?)?.toInt() ?? 0,
      conversionRate: (json['conversion_rate'] as num?)?.toDouble() ?? 0,
      ctr: (json['ctr'] as num?)?.toDouble() ?? 0,
      isWinner: json['is_winner'] as bool?,
    );

Map<String, dynamic> _$$ABTestVariantImplToJson(_$ABTestVariantImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'campaign_id': instance.campaignId,
      'variant_name': instance.variantName,
      'conversions': instance.conversions,
      'impressions': instance.impressions,
      'conversion_rate': instance.conversionRate,
      'ctr': instance.ctr,
      'is_winner': instance.isWinner,
    };

_$RecommendedContentImpl _$$RecommendedContentImplFromJson(
        Map<String, dynamic> json) =>
    _$RecommendedContentImpl(
      contentId: (json['content_id'] as num).toInt(),
      title: json['title'] as String,
      matchScore: (json['match_score'] as num).toDouble(),
      contentType: json['content_type'] as String? ?? 'content',
      tags: (json['tags'] as List<dynamic>?)?.map((e) => e as String).toList(),
      publishedAt: json['published_at'] == null
          ? null
          : DateTime.parse(json['published_at'] as String),
    );

Map<String, dynamic> _$$RecommendedContentImplToJson(
        _$RecommendedContentImpl instance) =>
    <String, dynamic>{
      'content_id': instance.contentId,
      'title': instance.title,
      'match_score': instance.matchScore,
      'content_type': instance.contentType,
      'tags': instance.tags,
      'published_at': instance.publishedAt?.toIso8601String(),
    };

_$UserPreferenceImpl _$$UserPreferenceImplFromJson(Map<String, dynamic> json) =>
    _$UserPreferenceImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      category: json['category'] as String,
      preferenceScore: (json['preference_score'] as num).toDouble(),
      interactionCount: (json['interaction_count'] as num?)?.toInt() ?? 0,
    );

Map<String, dynamic> _$$UserPreferenceImplToJson(
        _$UserPreferenceImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'category': instance.category,
      'preference_score': instance.preferenceScore,
      'interaction_count': instance.interactionCount,
    };

_$DistributionChannelImpl _$$DistributionChannelImplFromJson(
        Map<String, dynamic> json) =>
    _$DistributionChannelImpl(
      id: (json['id'] as num).toInt(),
      channelName: json['channel_name'] as String,
      status: json['status'] as String,
      reach: (json['reach'] as num?)?.toInt() ?? 0,
      engagementRate: (json['engagement_rate'] as num?)?.toDouble() ?? 0,
      impressions: (json['impressions'] as num?)?.toInt() ?? 0,
    );

Map<String, dynamic> _$$DistributionChannelImplToJson(
        _$DistributionChannelImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'channel_name': instance.channelName,
      'status': instance.status,
      'reach': instance.reach,
      'engagement_rate': instance.engagementRate,
      'impressions': instance.impressions,
    };

_$SyndicationPartnerImpl _$$SyndicationPartnerImplFromJson(
        Map<String, dynamic> json) =>
    _$SyndicationPartnerImpl(
      id: (json['id'] as num).toInt(),
      partnerName: json['partner_name'] as String,
      articlesSyndicated: (json['articles_syndicated'] as num?)?.toInt() ?? 0,
      totalReach: (json['total_reach'] as num?)?.toInt() ?? 0,
      lastSyndicationDate: json['last_syndication_date'] == null
          ? null
          : DateTime.parse(json['last_syndication_date'] as String),
      status: json['status'] as String? ?? 'active',
    );

Map<String, dynamic> _$$SyndicationPartnerImplToJson(
        _$SyndicationPartnerImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'partner_name': instance.partnerName,
      'articles_syndicated': instance.articlesSyndicated,
      'total_reach': instance.totalReach,
      'last_syndication_date': instance.lastSyndicationDate?.toIso8601String(),
      'status': instance.status,
    };

_$AnalyticsSnapshotImpl _$$AnalyticsSnapshotImplFromJson(
        Map<String, dynamic> json) =>
    _$AnalyticsSnapshotImpl(
      contentId: (json['content_id'] as num).toInt(),
      views: (json['views'] as num).toInt(),
      clicks: (json['clicks'] as num).toInt(),
      shares: (json['shares'] as num).toInt(),
      engagementScore: (json['engagement_score'] as num).toDouble(),
      trend: (json['trend'] as num?)?.toDouble() ?? 0,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );

Map<String, dynamic> _$$AnalyticsSnapshotImplToJson(
        _$AnalyticsSnapshotImpl instance) =>
    <String, dynamic>{
      'content_id': instance.contentId,
      'views': instance.views,
      'clicks': instance.clicks,
      'shares': instance.shares,
      'engagement_score': instance.engagementScore,
      'trend': instance.trend,
      'timestamp': instance.timestamp.toIso8601String(),
    };

_$RecommendationPerformanceImpl _$$RecommendationPerformanceImplFromJson(
        Map<String, dynamic> json) =>
    _$RecommendationPerformanceImpl(
      totalRecommendations: (json['total_recommendations'] as num).toInt(),
      clicks: (json['clicks'] as num).toInt(),
      conversions: (json['conversions'] as num).toInt(),
      clickThroughRate: (json['click_through_rate'] as num?)?.toDouble() ?? 0,
      conversionRate: (json['conversion_rate'] as num?)?.toDouble() ?? 0,
      avgReadTime: (json['avg_read_time'] as num?)?.toDouble() ?? 0,
    );

Map<String, dynamic> _$$RecommendationPerformanceImplToJson(
        _$RecommendationPerformanceImpl instance) =>
    <String, dynamic>{
      'total_recommendations': instance.totalRecommendations,
      'clicks': instance.clicks,
      'conversions': instance.conversions,
      'click_through_rate': instance.clickThroughRate,
      'conversion_rate': instance.conversionRate,
      'avg_read_time': instance.avgReadTime,
    };
