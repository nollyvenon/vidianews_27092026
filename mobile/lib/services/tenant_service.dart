import 'package:http/http.dart' as http;
import 'dart:convert';

class TenantService {
  final String apiUrl;
  final String token;

  TenantService({
    required this.apiUrl,
    required this.token,
  });

  Future<List<Tenant>> listTenants({int skip = 0, int limit = 20}) async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/api/v1/tenants?skip=$skip&limit=$limit'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return (data['data'] as List)
            .map((t) => Tenant.fromJson(t))
            .toList();
      }
      throw Exception('Failed to load tenants');
    } catch (e) {
      rethrow;
    }
  }

  Future<Tenant> getTenant(int id) async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/api/v1/tenants/$id'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return Tenant.fromJson(json.decode(response.body));
      }
      throw Exception('Failed to load tenant');
    } catch (e) {
      rethrow;
    }
  }

  Future<Tenant> createTenant({
    required String name,
    required String slug,
    String? description,
    String plan = 'free',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/tenants'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'name': name,
          'slug': slug,
          'description': description,
          'plan': plan,
        }),
      );

      if (response.statusCode == 201) {
        return Tenant.fromJson(json.decode(response.body));
      }
      throw Exception('Failed to create tenant');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> updateTenant(
    int id, {
    String? name,
    String? description,
    String? plan,
  }) async {
    try {
      final body = <String, dynamic>{};
      if (name != null) body['name'] = name;
      if (description != null) body['description'] = description;
      if (plan != null) body['plan'] = plan;

      final response = await http.put(
        Uri.parse('$apiUrl/api/v1/tenants/$id'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode(body),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to update tenant');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> deleteTenant(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$apiUrl/api/v1/tenants/$id'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode != 204) {
        throw Exception('Failed to delete tenant');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<List<TenantMember>> getTenantMembers(int tenantId) async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/api/v1/tenants/$tenantId/members'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return (json.decode(response.body) as List)
            .map((m) => TenantMember.fromJson(m))
            .toList();
      }
      throw Exception('Failed to load members');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> addMember(
    int tenantId,
    int userId, {
    String role = 'member',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/tenants/$tenantId/members'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'user_id': userId,
          'role': role,
        }),
      );

      if (response.statusCode != 201) {
        throw Exception('Failed to add member');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> removeMember(int tenantId, int userId) async {
    try {
      final response = await http.delete(
        Uri.parse('$apiUrl/api/v1/tenants/$tenantId/members/$userId'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode != 204) {
        throw Exception('Failed to remove member');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> inviteUser(
    int tenantId,
    String email, {
    String role = 'member',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/tenants/$tenantId/invite'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'email': email,
          'role': role,
        }),
      );

      if (response.statusCode != 201) {
        throw Exception('Failed to invite user');
      }
    } catch (e) {
      rethrow;
    }
  }
}

// Models
class Tenant {
  final int id;
  final String name;
  final String slug;
  final String? description;
  final String? logoUrl;
  final String? website;
  final String status;
  final String plan;
  final int maxUsers;
  final int maxStorageGb;
  final DateTime createdAt;
  final DateTime updatedAt;

  Tenant({
    required this.id,
    required this.name,
    required this.slug,
    this.description,
    this.logoUrl,
    this.website,
    required this.status,
    required this.plan,
    required this.maxUsers,
    required this.maxStorageGb,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Tenant.fromJson(Map<String, dynamic> json) {
    return Tenant(
      id: json['id'],
      name: json['name'],
      slug: json['slug'],
      description: json['description'],
      logoUrl: json['logo_url'],
      website: json['website'],
      status: json['status'],
      plan: json['plan'],
      maxUsers: json['max_users'],
      maxStorageGb: json['max_storage_gb'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }
}

class TenantMember {
  final int id;
  final int tenantId;
  final int userId;
  final String role;
  final bool isOwner;
  final String status;
  final DateTime joinedAt;

  TenantMember({
    required this.id,
    required this.tenantId,
    required this.userId,
    required this.role,
    required this.isOwner,
    required this.status,
    required this.joinedAt,
  });

  factory TenantMember.fromJson(Map<String, dynamic> json) {
    return TenantMember(
      id: json['id'],
      tenantId: json['tenant_id'],
      userId: json['user_id'],
      role: json['role'],
      isOwner: json['is_owner'],
      status: json['status'],
      joinedAt: DateTime.parse(json['joined_at']),
    );
  }
}
