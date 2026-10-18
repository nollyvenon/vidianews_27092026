// Comments, push device registration and notification logs, and outbound webhooks for the signed-in user.

import 'package:dio/dio.dart';
import '../models/community_models.dart';

class CommunityService {
  final Dio _dio;

  CommunityService(this._dio);

  Future<List<ContentComment>> fetchComments(int contentId) async {
    final response = await _dio.get<dynamic>('/platform/comments/$contentId');
    return _rows(response.data).map(ContentComment.fromJson).toList();
  }

  Future<ContentComment> postComment({required int contentId, required String text}) async {
    final response = await _dio.post<dynamic>('/platform/comments', data: {'content_id': contentId, 'text': text});
    return ContentComment.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<PushDevice>> fetchDevices() async {
    final response = await _dio.get<dynamic>('/platform/devices');
    return _rows(response.data).map(PushDevice.fromJson).toList();
  }

  Future<PushDevice> registerDevice({required String token, required String platform, String? name}) async {
    final response = await _dio.post<dynamic>('/platform/devices/register', data: {
      'device_token': token,
      'platform': platform,
      'device_name': name,
    });
    return PushDevice.fromJson(response.data as Map<String, dynamic>);
  }

  Future<void> removeDevice(int deviceId) async {
    await _dio.delete<dynamic>('/platform/devices/$deviceId');
  }

  Future<List<NotificationLog>> fetchNotificationLogs() async {
    final response = await _dio.get<dynamic>('/platform/notifications/logs');
    return _rows(response.data).map(NotificationLog.fromJson).toList();
  }

  Future<List<OutboundWebhook>> fetchWebhooks() async {
    final response = await _dio.get<dynamic>('/outbound-webhooks');
    return _rows(response.data).map(OutboundWebhook.fromJson).toList();
  }

  Future<List<WebhookEventType>> fetchWebhookEvents() async {
    final response = await _dio.get<dynamic>('/outbound-webhooks/events');
    return _rows(response.data).map(WebhookEventType.fromJson).toList();
  }

  Future<OutboundWebhook> createWebhook({required String url, required List<String> events, String? description}) async {
    final response = await _dio.post<dynamic>('/outbound-webhooks', data: {
      'url': url,
      'events': events,
      'description': description,
    });
    return OutboundWebhook.fromJson(response.data as Map<String, dynamic>);
  }

  Future<Map<String, dynamic>> testWebhook(int webhookId) async {
    final response = await _dio.post<dynamic>('/outbound-webhooks/$webhookId/test');
    return response.data as Map<String, dynamic>;
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
