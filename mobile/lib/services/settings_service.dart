import 'package:http/http.dart' as http;
import 'dart:convert';

class SettingsService {
  final String baseUrl = 'http://localhost:8000/api/v1';
  final String? token;

  SettingsService({this.token});

  Future<Map<String, dynamic>> getAllSettings() async {
    final response = await http.get(
      Uri.parse('$baseUrl/settings/me'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get settings');
  }

  Future<Map<String, dynamic>> updateSettings(Map<String, dynamic> updates) async {
    final response = await http.put(
      Uri.parse('$baseUrl/settings/me'),
      headers: _getHeaders(),
      body: jsonEncode(updates),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to update settings');
  }

  Future<Map<String, dynamic>> getNotificationSettings() async {
    final response = await http.get(
      Uri.parse('$baseUrl/settings/me/notifications'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get notification settings');
  }

  Future<Map<String, dynamic>> updateNotificationSettings(
    Map<String, dynamic> updates,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/settings/me/notifications'),
      headers: _getHeaders(),
      body: jsonEncode(updates),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to update notification settings');
  }

  Future<Map<String, dynamic>> getPrivacySettings() async {
    final response = await http.get(
      Uri.parse('$baseUrl/settings/me/privacy'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get privacy settings');
  }

  Future<Map<String, dynamic>> updatePrivacySettings(
    Map<String, dynamic> updates,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/settings/me/privacy'),
      headers: _getHeaders(),
      body: jsonEncode(updates),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to update privacy settings');
  }

  Future<Map<String, dynamic>> getDisplaySettings() async {
    final response = await http.get(
      Uri.parse('$baseUrl/settings/me/display'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to get display settings');
  }

  Future<Map<String, dynamic>> updateDisplaySettings(
    Map<String, dynamic> updates,
  ) async {
    final response = await http.put(
      Uri.parse('$baseUrl/settings/me/display'),
      headers: _getHeaders(),
      body: jsonEncode(updates),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to update display settings');
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
