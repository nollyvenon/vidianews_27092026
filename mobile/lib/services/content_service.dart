import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ContentService {
  static const String baseUrl = 'https://api.vidianews.app/api/v1/content';

  Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('auth_token');
  }

  Future<Map<String, String>> _getHeaders() async {
    final token = await _getToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // Content CRUD
  Future<Map<String, dynamic>> createContent(Map<String, dynamic> data) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: headers,
      body: jsonEncode(data),
    );

    if (response.statusCode != 201) {
      throw Exception('Failed to create content');
    }
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> getContent(int id) async {
    final response = await http.get(
      Uri.parse('$baseUrl/$id'),
      headers: await _getHeaders(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to fetch content');
    }
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> updateContent(int id, Map<String, dynamic> data) async {
    final headers = await _getHeaders();
    final response = await http.put(
      Uri.parse('$baseUrl/$id'),
      headers: headers,
      body: jsonEncode(data),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update content');
    }
    return jsonDecode(response.body);
  }

  Future<void> deleteContent(int id) async {
    final headers = await _getHeaders();
    final response = await http.delete(
      Uri.parse('$baseUrl/$id'),
      headers: headers,
    );

    if (response.statusCode != 204) {
      throw Exception('Failed to delete content');
    }
  }

  // List content
  Future<Map<String, dynamic>> listContent({
    int page = 1,
    int pageSize = 20,
    String? status,
    String? contentType,
  }) async {
    final params = {
      'page': page.toString(),
      'page_size': pageSize.toString(),
      if (status != null) 'status': status,
      if (contentType != null) 'content_type': contentType,
    };

    final uri = Uri.parse(baseUrl).replace(queryParameters: params);
    final response = await http.get(uri);

    if (response.statusCode != 200) {
      throw Exception('Failed to fetch content list');
    }
    return jsonDecode(response.body);
  }

  // Search
  Future<List<dynamic>> searchContent(String query, {int limit = 50}) async {
    final params = {
      'query': query,
      'limit': limit.toString(),
    };

    final uri = Uri.parse('$baseUrl/search').replace(queryParameters: params);
    final response = await http.get(uri);

    if (response.statusCode != 200) {
      throw Exception('Failed to search content');
    }
    return jsonDecode(response.body);
  }

  // Get featured content
  Future<List<dynamic>> getFeaturedContent({int limit = 10}) async {
    final params = {'limit': limit.toString()};
    final uri = Uri.parse('$baseUrl/featured').replace(queryParameters: params);
    final response = await http.get(uri);

    if (response.statusCode != 200) {
      throw Exception('Failed to fetch featured content');
    }
    return jsonDecode(response.body);
  }

  // Get trending content
  Future<List<dynamic>> getTrendingContent({int days = 7, int limit = 10}) async {
    final params = {
      'days': days.toString(),
      'limit': limit.toString(),
    };
    final uri = Uri.parse('$baseUrl/trending').replace(queryParameters: params);
    final response = await http.get(uri);

    if (response.statusCode != 200) {
      throw Exception('Failed to fetch trending content');
    }
    return jsonDecode(response.body);
  }

  // Publishing workflow
  Future<Map<String, dynamic>> publishContent(int id) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse('$baseUrl/$id/publish'),
      headers: headers,
      body: jsonEncode({'access_level': 'public'}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to publish content');
    }
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> scheduleContent(int id, DateTime scheduledAt) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse('$baseUrl/$id/schedule'),
      headers: headers,
      body: jsonEncode({'scheduled_at': scheduledAt.toIso8601String()}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to schedule content');
    }
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> archiveContent(int id) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse('$baseUrl/$id/archive'),
      headers: headers,
      body: jsonEncode({}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to archive content');
    }
    return jsonDecode(response.body);
  }

  // Engagement
  Future<void> recordEngagement(int contentId, String engagementType) async {
    final response = await http.post(
      Uri.parse('$baseUrl/$contentId/engage'),
      headers: await _getHeaders(),
      body: jsonEncode({'engagement_type': engagementType}),
    );

    if (response.statusCode != 201) {
      print('Failed to record engagement');
    }
  }

  // Stats
  Future<Map<String, dynamic>> getContentStats(int id) async {
    final response = await http.get(
      Uri.parse('$baseUrl/$id/stats'),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to fetch stats');
    }
    return jsonDecode(response.body);
  }
}
