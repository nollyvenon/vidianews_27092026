import 'dart:convert';
import './authenticated_http.dart';
import './authenticated_dio.dart';

class NotificationService {
  final String baseUrl = '$kApiBaseUrl';
  final String? token;

  NotificationService({this.token});

  Future<List<dynamic>> getMyNotifications({int limit = 50, int offset = 0}) async {
    final response = await authenticatedHttp.get(
      Uri.parse('$baseUrl/notifications/me?limit=$limit&offset=$offset'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get notifications');
  }

  Future<Map<String, dynamic>> getUnreadCount() async {
    final response = await authenticatedHttp.get(
      Uri.parse('$baseUrl/notifications/me/unread-count'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get unread count');
  }

  Future<void> markAsRead(int notificationId) async {
    final response = await authenticatedHttp.post(
      Uri.parse('$baseUrl/notifications/me/$notificationId/read'),
      headers: _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark as read');
    }
  }

  Future<void> markAllAsRead() async {
    final response = await authenticatedHttp.post(
      Uri.parse('$baseUrl/notifications/me/read-all'),
      headers: _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark all as read');
    }
  }

  Future<void> archiveNotification(int notificationId) async {
    final response = await authenticatedHttp.post(
      Uri.parse('$baseUrl/notifications/me/$notificationId/archive'),
      headers: _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to archive notification');
    }
  }

  Future<void> deleteNotification(int notificationId) async {
    final response = await authenticatedHttp.delete(
      Uri.parse('$baseUrl/notifications/me/$notificationId'),
      headers: _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to delete notification');
    }
  }

  Future<Map<String, dynamic>> getNotificationLogs({int limit = 100, int offset = 0}) async {
    final response = await authenticatedHttp.get(
      Uri.parse('$baseUrl/notifications/me/logs?limit=$limit&offset=$offset'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get notification logs');
  }

  Map<String, String> _getHeaders() {
    final headers = {
      'Content-Type': 'application/json',
    };
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }
}
