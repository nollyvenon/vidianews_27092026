import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static String? token;

  static void setToken(String? newToken) => token = newToken;

  Future<List<dynamic>> listChats(int userId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/ai/chats'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load chats');
  }

  Future<Map<String, dynamic>> getChat(int chatId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/ai/chats/$chatId'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load chat');
  }

  Future<Map<String, dynamic>> createChat(int userId, String title) async {
    final response = await http.post(
      Uri.parse('$baseUrl/ai/chats'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'title': title}),
    );
    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to create chat');
  }

  Future<Map<String, dynamic>> addMessage(
    int chatId,
    String role,
    String content,
    int tokens,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/ai/chats/$chatId/messages'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'role': role,
        'content': content,
        'tokens': tokens,
      }),
    );
    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to add message');
  }
}
