import 'package:http/http.dart' as http;
import 'dart:convert';

class ProfileService {
  final String apiUrl;
  final String token;

  ProfileService({required this.apiUrl, required this.token});

  Future<UserProfile> getMyProfile() async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/api/v1/profiles/me'),
        headers: {'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        return UserProfile.fromJson(json.decode(response.body));
      }
      throw Exception('Failed to load profile');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> updateProfile(Map<String, dynamic> updates) async {
    try {
      final response = await http.put(
        Uri.parse('$apiUrl/api/v1/profiles/me'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode(updates),
      );
      if (response.statusCode != 200) throw Exception('Failed to update');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> addSkill(String name, {String? category}) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/profiles/me/skills'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode({'name': name, 'category': category}),
      );
      if (response.statusCode != 201) throw Exception('Failed to add skill');
    } catch (e) {
      rethrow;
    }
  }
}

class UserProfile {
  final int id;
  final int userId;
  final String? title;
  final String? bio;
  final String? avatarUrl;
  final String? location;
  final String timezone;
  final bool isPublic;

  UserProfile({
    required this.id,
    required this.userId,
    this.title,
    this.bio,
    this.avatarUrl,
    this.location,
    required this.timezone,
    required this.isPublic,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'],
      userId: json['user_id'],
      title: json['title'],
      bio: json['bio'],
      avatarUrl: json['avatar_url'],
      location: json['location'],
      timezone: json['timezone'],
      isPublic: json['is_public'],
    );
  }
}
