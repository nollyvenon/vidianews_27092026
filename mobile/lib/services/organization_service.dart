import 'package:http/http.dart' as http;
import 'dart:convert';

class OrganizationService {
  final String apiUrl;
  final String token;

  OrganizationService({
    required this.apiUrl,
    required this.token,
  });

  Future<List<Organization>> listOrganizations(int tenantId) async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/api/v1/organizations?tenant_id=$tenantId'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return (data['data'] as List)
            .map((o) => Organization.fromJson(o))
            .toList();
      }
      throw Exception('Failed to load organizations');
    } catch (e) {
      rethrow;
    }
  }

  Future<Organization> createOrganization({
    required int tenantId,
    required String name,
    required String slug,
    String orgType = 'department',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/organizations'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'tenant_id': tenantId,
          'name': name,
          'slug': slug,
          'org_type': orgType,
        }),
      );

      if (response.statusCode == 201) {
        return Organization.fromJson(json.decode(response.body));
      }
      throw Exception('Failed to create organization');
    } catch (e) {
      rethrow;
    }
  }

  Future<List<OrganizationMember>> getMembers(int orgId) async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/api/v1/organizations/$orgId/members'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return (json.decode(response.body) as List)
            .map((m) => OrganizationMember.fromJson(m))
            .toList();
      }
      throw Exception('Failed to load members');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> addMember(int orgId, int userId, String role) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/api/v1/organizations/$orgId/members?user_id=$userId&role=$role'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode != 201) {
        throw Exception('Failed to add member');
      }
    } catch (e) {
      rethrow;
    }
  }
}

class Organization {
  final int id;
  final int tenantId;
  final String name;
  final String slug;
  final String orgType;
  final String status;
  final DateTime createdAt;

  Organization({
    required this.id,
    required this.tenantId,
    required this.name,
    required this.slug,
    required this.orgType,
    required this.status,
    required this.createdAt,
  });

  factory Organization.fromJson(Map<String, dynamic> json) {
    return Organization(
      id: json['id'],
      tenantId: json['tenant_id'],
      name: json['name'],
      slug: json['slug'],
      orgType: json['org_type'],
      status: json['status'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class OrganizationMember {
  final int id;
  final int organizationId;
  final int userId;
  final String role;
  final bool isLead;
  final String status;

  OrganizationMember({
    required this.id,
    required this.organizationId,
    required this.userId,
    required this.role,
    required this.isLead,
    required this.status,
  });

  factory OrganizationMember.fromJson(Map<String, dynamic> json) {
    return OrganizationMember(
      id: json['id'],
      organizationId: json['organization_id'],
      userId: json['user_id'],
      role: json['role'],
      isLead: json['is_lead'],
      status: json['status'],
    );
  }
}
