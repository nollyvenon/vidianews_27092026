import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../models/user_management_models.dart';

final userManagementServiceProvider = Provider((ref) {
  final dio = Dio();
  return UserManagementService(dio);
});

class UserManagementService {
  final Dio _dio;
  final String _baseUrl = 'http://localhost:8000/api/v1';

  UserManagementService(this._dio);

  // Subscriber Management
  Future<Map<String, dynamic>> createSubscriber({
    required int userId,
    required String subscriptionTier,
  }) async {
    final response = await _dio.post('$_baseUrl/subscribers', data: {
      'user_id': userId,
      'subscription_tier': subscriptionTier,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> recordActivity({
    required int subscriberId,
    required String activityType,
    int? contentId,
    Map<String, dynamic>? metadata,
  }) async {
    final response = await _dio.post('$_baseUrl/subscribers/activity', data: {
      'subscriber_id': subscriberId,
      'activity_type': activityType,
      'content_id': contentId,
      'metadata': metadata,
    });
    return response.data;
  }

  Future<double> getEngagementScore(int subscriberId) async {
    final response = await _dio.get(
      '$_baseUrl/subscribers/$subscriberId/engagement-score',
    );
    return response.data['engagement_score'].toDouble();
  }

  Future<double> getChurnRisk(int subscriberId) async {
    final response = await _dio.get(
      '$_baseUrl/subscribers/$subscriberId/churn-risk',
    );
    return response.data['churn_risk_score'].toDouble();
  }

  // Email Campaigns
  Future<Map<String, dynamic>> createCampaign({
    required String name,
    required int templateId,
    required String subject,
    required String fromEmail,
    DateTime? scheduledAt,
  }) async {
    final response = await _dio.post('$_baseUrl/emails/campaigns', data: {
      'name': name,
      'template_id': templateId,
      'subject': subject,
      'from_email': fromEmail,
      'scheduled_at': scheduledAt?.toIso8601String(),
    });
    return response.data;
  }

  Future<Map<String, dynamic>> sendCampaign(int campaignId) async {
    final response = await _dio.post(
      '$_baseUrl/emails/campaigns/$campaignId/send',
    );
    return response.data;
  }

  Future<Map<String, dynamic>> getCampaignMetrics(int campaignId) async {
    final response = await _dio.get(
      '$_baseUrl/emails/campaigns/$campaignId/metrics',
    );
    return response.data;
  }

  // User Segments
  Future<Map<String, dynamic>> createSegment({
    required String name,
    required String segmentType,
    String? description,
    Map<String, dynamic>? filterCriteria,
  }) async {
    final response = await _dio.post('$_baseUrl/segments', data: {
      'name': name,
      'segment_type': segmentType,
      'description': description,
      'filter_criteria': filterCriteria,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> addUsersToSegment({
    required int segmentId,
    required List<int> userIds,
  }) async {
    final response = await _dio.post(
      '$_baseUrl/segments/$segmentId/users',
      data: {'user_ids': userIds},
    );
    return response.data;
  }

  Future<List<int>> getSegmentUsers(int segmentId) async {
    final response = await _dio.get('$_baseUrl/segments/$segmentId/users');
    return List<int>.from(response.data['user_ids']);
  }

  // Notifications
  Future<Map<String, dynamic>> sendNotification({
    required int userId,
    required String channel,
    required String title,
    required String message,
  }) async {
    final response = await _dio.post('$_baseUrl/notifications', data: {
      'user_id': userId,
      'channel': channel,
      'title': title,
      'message': message,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> markNotificationRead(int notificationId) async {
    final response = await _dio.patch(
      '$_baseUrl/notifications/$notificationId/read',
    );
    return response.data;
  }

  // Personalization
  Future<Map<String, dynamic>> createPersonalizationProfile({
    required int userId,
    String? readingLevel,
    String? timezone,
  }) async {
    final response =
        await _dio.post('$_baseUrl/personalization/profiles', data: {
      'user_id': userId,
      'reading_level': readingLevel ?? 'intermediate',
      'timezone': timezone ?? 'UTC',
    });
    return response.data;
  }

  Future<Map<String, dynamic>> updateUserInterests({
    required int userId,
    required List<String> keywords,
  }) async {
    final response = await _dio.post('$_baseUrl/personalization/interests', data: {
      'user_id': userId,
      'keywords': keywords,
    });
    return response.data;
  }

  Future<double> getPersonalizationScore(int userId) async {
    final response = await _dio.get(
      '$_baseUrl/personalization/$userId/score',
    );
    return response.data['personalization_score'].toDouble();
  }

  // API Keys
  Future<Map<String, dynamic>> createAPIKey({
    required String name,
    required List<String> permissions,
  }) async {
    final response = await _dio.post('$_baseUrl/api-keys', data: {
      'name': name,
      'permissions': permissions,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> validateAPIKey(String key) async {
    final response = await _dio.get(
      '$_baseUrl/api-keys/validate',
      queryParameters: {'key': key},
    );
    return response.data;
  }

  // Webhooks
  Future<Map<String, dynamic>> createWebhook({
    required String name,
    required String url,
    required List<String> events,
  }) async {
    final response = await _dio.post('$_baseUrl/webhooks/endpoints', data: {
      'name': name,
      'url': url,
      'events': events,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> triggerWebhook({
    required int webhookId,
    required String eventType,
    required Map<String, dynamic> payload,
  }) async {
    final response = await _dio.post(
      '$_baseUrl/webhooks/$webhookId/trigger',
      data: {
        'event_type': eventType,
        'payload': payload,
      },
    );
    return response.data;
  }
}

// State Providers
final subscriberProfileProvider =
    StateProvider<SubscriberProfile?>((ref) => null);

final userSegmentsProvider =
    StateProvider<List<UserSegment>>((ref) => []);

final emailCampaignsProvider =
    StateProvider<List<EmailCampaign>>((ref) => []);

final notificationsProvider =
    StateProvider<List<NotificationMessage>>((ref) => []);

final personalizationProfileProvider =
    StateProvider<PersonalizationProfile?>((ref) => null);

final subscriberAnalyticsProvider =
    StateProvider<SubscriberAnalytics?>((ref) => null);

final engagementScoreProvider = StateProvider<double>((ref) => 0.0);

final churnRiskProvider = StateProvider<double>((ref) => 0.0);

final personalizationScoreProvider = StateProvider<double>((ref) => 0.0);
