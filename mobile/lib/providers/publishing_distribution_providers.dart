// Publishing & Distribution Providers (Modules 66-70)

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';

final publishingServiceProvider = Provider((ref) {
  final dio = Dio();
  return PublishingDistributionService(dio);
});

class PublishingDistributionService {
  final Dio _dio;
  final String _baseUrl = 'http://localhost:8000/api/v1';

  PublishingDistributionService(this._dio);

  Future<Map<String, dynamic>> createPublishingJob({
    required String title,
    required DateTime scheduledTime,
    required List<String> channels,
  }) async {
    final response = await _dio.post('$_baseUrl/publishing/jobs', data: {
      'content_id': 1,
      'title': title,
      'scheduled_publish_time': scheduledTime.toIso8601String(),
      'distribution_channels': channels,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> recordEngagement({
    required int contentId,
    required String actionType,
    required String deviceType,
  }) async {
    final response = await _dio.post('$_baseUrl/analytics/engagement', data: {
      'content_id': contentId,
      'action_type': actionType,
      'device_type': deviceType,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> getEngagementMetrics(int contentId) async {
    final response = await _dio.get('$_baseUrl/analytics/metrics/$contentId');
    return response.data;
  }

  Future<Map<String, dynamic>> createABTest({
    required String name,
    required String testMetric,
    required String hypothesis,
  }) async {
    final response = await _dio.post('$_baseUrl/ab-testing/campaigns', data: {
      'content_id': 1,
      'name': name,
      'test_metric': testMetric,
      'hypothesis': hypothesis,
    });
    return response.data;
  }

  Future<List<Map<String, dynamic>>> generateRecommendations({
    required int userId,
    required List<int> contentPool,
  }) async {
    final response = await _dio.post('$_baseUrl/recommendations/generate', data: {
      'user_id': userId,
      'content_pool': contentPool,
    });
    return List<Map<String, dynamic>>.from(response.data['recommended_content_ids']);
  }
}

// State Providers
final publishingJobsProvider = StateProvider<List<Map<String, dynamic>>>((ref) => []);
final analyticsDataProvider = StateProvider<Map<String, dynamic>>((ref) => {});
final abTestsProvider = StateProvider<List<Map<String, dynamic>>>((ref) => []);
final recommendationsProvider = StateProvider<List<int>>((ref) => []);
