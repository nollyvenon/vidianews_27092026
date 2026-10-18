// Messages, followers, notifications, privacy and premium access for the signed-in user.

import 'package:dio/dio.dart';
import '../models/social_account_models.dart';

class SocialAccountService {
  final Dio _dio;

  SocialAccountService(this._dio);

  Future<int> fetchUnreadMessageCount() async {
    final response = await _dio.get<dynamic>('/messages/unread/count');
    return (response.data as Map<String, dynamic>)['unread_count'] as int;
  }

  Future<List<DirectMessage>> fetchConversation(int otherUserId) async {
    final response = await _dio.get<dynamic>('/messages/$otherUserId');
    return _rows(response.data).map(DirectMessage.fromJson).toList();
  }

  Future<void> sendMessage({required int recipientId, required String content}) async {
    await _dio.post<dynamic>('/messages/send', queryParameters: {'recipient_id': recipientId, 'content': content});
  }

  Future<void> markMessageRead(int messageId) async {
    await _dio.put<dynamic>('/messages/$messageId/read');
  }

  Future<List<Follower>> fetchFollowers(int userId) async {
    final response = await _dio.get<dynamic>('/platform/followers/$userId');
    return _rows(response.data).map(Follower.fromJson).toList();
  }

  Future<List<AppNotification>> fetchAlerts() async {
    final response = await _dio.get<dynamic>('/notifications/me');
    return _rows(response.data).map(AppNotification.fromJson).toList();
  }

  Future<void> markAlertRead(int notificationId) async {
    await _dio.post<dynamic>('/notifications/me/$notificationId/read');
  }

  Future<List<AppNotification>> fetchNotices() async {
    final response = await _dio.get<dynamic>('/system/notifications');
    return _rows(response.data).map(AppNotification.fromJson).toList();
  }

  Future<void> markNoticeRead(int noticeId) async {
    await _dio.post<dynamic>('/system/notifications/$noticeId/read');
  }

  Future<PrivacySettings> fetchPrivacySettings() async {
    final response = await _dio.get<dynamic>('/privacy/settings');
    return PrivacySettings.fromJson(response.data as Map<String, dynamic>);
  }

  Future<PrivacySettings> updatePrivacySettings(PrivacySettings settings) async {
    final response = await _dio.put<dynamic>('/privacy/settings', queryParameters: {
      'profile_visibility': settings.profileVisibility,
      'content_visibility': settings.contentVisibility,
      'allow_analytics': settings.allowAnalytics,
      'allow_marketing': settings.allowMarketing,
    });
    return PrivacySettings.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<ConsentEntry>> fetchConsents() async {
    final response = await _dio.get<dynamic>('/privacy/consents');
    return _rows(response.data).map(ConsentEntry.fromJson).toList();
  }

  Future<void> logConsent({required String consentType, required bool granted}) async {
    await _dio.post<dynamic>('/privacy/consent-log', queryParameters: {
      'consent_type': consentType,
      'granted': granted,
    });
  }

  Future<Map<String, dynamic>> exportData() async {
    final response = await _dio.get<dynamic>('/privacy/export');
    return response.data as Map<String, dynamic>;
  }

  Future<DateTime> requestDeletion() async {
    final response = await _dio.post<dynamic>('/privacy/request-deletion');
    return DateTime.parse((response.data as Map<String, dynamic>)['scheduled_for'] as String);
  }

  Future<PremiumStatus> fetchPremiumStatus() async {
    final response = await _dio.get<dynamic>('/premium/status');
    return PremiumStatus.fromJson(response.data as Map<String, dynamic>);
  }

  Future<void> subscribeToPremium() async {
    await _dio.post<dynamic>('/premium/subscribe');
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
