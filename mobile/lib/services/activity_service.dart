import 'package:http/http.dart' as http;
import 'dart:convert';

class ActivityService {
  final String baseUrl = 'http://localhost:8000/api/v1';
  final String? token;

  ActivityService({this.token});

  Future<List<dynamic>> getActivities({int limit = 50, int offset = 0}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/activity/me?limit=$limit&offset=$offset'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get activities');
  }

  Future<Map<String, dynamic>> getActivityCount({int days = 7}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/activity/me/count?days=$days'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get activity count');
  }

  Future<Map<String, dynamic>> getActivitySummary({int days = 7}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/activity/me/summary?days=$days'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get summary');
  }

  Future<List<dynamic>> getActivityFeed({int limit = 50, int offset = 0}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/activity/feed?limit=$limit&offset=$offset'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get feed');
  }

  Future<Map<String, dynamic>> getUnreadFeedCount() async {
    final response = await http.get(
      Uri.parse('$baseUrl/activity/feed/unread-count'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get unread count');
  }

  Future<void> markFeedRead(int feedId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/activity/feed/$feedId/read'),
      headers: _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark as read');
    }
  }

  Future<void> markAllFeedRead() async {
    final response = await http.post(
      Uri.parse('$baseUrl/activity/feed/read-all'),
      headers: _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark all as read');
    }
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
