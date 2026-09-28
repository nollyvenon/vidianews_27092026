import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import '../models/enterprise_features_models.dart';

const String baseUrl = 'http://localhost:8000/api/v1';

class EnterpriseService {
  final String _baseUrl;

  EnterpriseService({String? baseUrl}) : _baseUrl = baseUrl ?? baseUrl;

  // Security endpoints
  Future<List<AuditLog>> getAuditLogs({
    int? userId,
    String? action,
    String? severity,
    int days = 30,
    int limit = 100,
  }) async {
    final params = <String, String>{
      'days': days.toString(),
      'limit': limit.toString(),
    };
    if (userId != null) params['user_id'] = userId.toString();
    if (action != null) params['action'] = action;
    if (severity != null) params['severity'] = severity;

    final uri = Uri.parse('$_baseUrl/security/audit-logs').replace(queryParameters: params);
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => AuditLog.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch audit logs');
  }

  Future<AccessControl> grantAccess({
    required int userId,
    required String resourceType,
    required int resourceId,
    required String accessLevel,
    required List<String> permissions,
    required int grantedBy,
    DateTime? expiresAt,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/security/access-control/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'resource_type': resourceType,
        'resource_id': resourceId,
        'access_level': accessLevel,
        'permissions': permissions,
        'granted_by': grantedBy,
        'expires_at': expiresAt?.toIso8601String(),
      }),
    );

    if (response.statusCode == 200) {
      return AccessControl.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to grant access');
  }

  Future<RoleAssignment> assignRole({
    required int userId,
    required String role,
    required List<String> permissions,
    bool canEditContent = false,
    bool canDeleteContent = false,
    bool canManageUsers = false,
    bool canAccessAnalytics = false,
    bool canAccessAdmin = false,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/security/roles/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'role': role,
        'permissions': permissions,
        'can_edit_content': canEditContent,
        'can_delete_content': canDeleteContent,
        'can_manage_users': canManageUsers,
        'can_access_analytics': canAccessAnalytics,
        'can_access_admin': canAccessAdmin,
      }),
    );

    if (response.statusCode == 200) {
      return RoleAssignment.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to assign role');
  }

  Future<RoleAssignment> getUserRole(int userId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/security/roles/$userId'),
    );

    if (response.statusCode == 200) {
      return RoleAssignment.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to fetch user role');
  }

  // Moderation endpoints
  Future<ModerationItem> submitForModeration({
    required int contentId,
    required String contentType,
    required String reason,
    List<String>? flags,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/moderation/queue'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'content_id': contentId,
        'content_type': contentType,
        'reason': reason,
        'flags': flags ?? [],
      }),
    );

    if (response.statusCode == 200) {
      return ModerationItem.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to submit for moderation');
  }

  Future<List<ModerationItem>> getPendingModerationItems({int limit = 50}) async {
    final uri = Uri.parse('$_baseUrl/moderation/queue/pending').replace(
      queryParameters: {'limit': limit.toString()},
    );
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => ModerationItem.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch pending moderation items');
  }

  Future<ComplianceCheckResult> checkCompliance(String text) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/moderation/check-compliance'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'text': text}),
    );

    if (response.statusCode == 200) {
      return ComplianceCheckResult.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to check compliance');
  }

  // Rate limiting endpoints
  Future<RateLimitStatus> checkRateLimit({
    int? userId,
    String? ipAddress,
    String endpoint = '*',
  }) async {
    final params = <String, String>{
      'endpoint': endpoint,
    };
    if (userId != null) params['user_id'] = userId.toString();
    if (ipAddress != null) params['ip_address'] = ipAddress;

    final uri = Uri.parse('$_baseUrl/rate-limits/check').replace(queryParameters: params);
    final response = await http.post(uri);

    if (response.statusCode == 200) {
      return RateLimitStatus.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to check rate limit');
  }

  // Notification endpoints
  Future<NotificationPreference> getNotificationPreferences(int userId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/notifications/preferences/$userId'),
    );

    if (response.statusCode == 200) {
      return NotificationPreference.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to fetch notification preferences');
  }

  Future<NotificationPreference> updateNotificationPreferences({
    required int userId,
    bool? emailEnabled,
    bool? pushEnabled,
    bool? smsEnabled,
    bool? inAppEnabled,
    String? frequency,
  }) async {
    final response = await http.put(
      Uri.parse('$_baseUrl/notifications/preferences/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email_enabled': emailEnabled,
        'push_enabled': pushEnabled,
        'sms_enabled': smsEnabled,
        'in_app_enabled': inAppEnabled,
        'frequency': frequency,
      }),
    );

    if (response.statusCode == 200) {
      return NotificationPreference.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to update notification preferences');
  }

  Future<List<Notification>> getNotifications({
    required int userId,
    bool unreadOnly = false,
    int limit = 50,
  }) async {
    final uri = Uri.parse('$_baseUrl/notifications/').replace(queryParameters: {
      'user_id': userId.toString(),
      'unread_only': unreadOnly.toString(),
      'limit': limit.toString(),
    });
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => Notification.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch notifications');
  }

  Future<void> markNotificationAsRead(int notificationId) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/notifications/$notificationId/mark-read'),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to mark notification as read');
    }
  }

  // Reporting endpoints
  Future<AdvancedReport> createReport({
    required int userId,
    required String name,
    required String reportType,
    required String format,
    Map<String, dynamic>? query,
    Map<String, dynamic>? filters,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/reports/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'name': name,
        'report_type': reportType,
        'format': format,
        'query': query,
        'filters': filters,
      }),
    );

    if (response.statusCode == 200) {
      return AdvancedReport.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to create report');
  }

  Future<List<AdvancedReport>> getUserReports({
    required int userId,
    int limit = 50,
  }) async {
    final uri = Uri.parse('$_baseUrl/reports/').replace(queryParameters: {
      'user_id': userId.toString(),
      'limit': limit.toString(),
    });
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => AdvancedReport.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch reports');
  }

  Future<ExportJob> createExportJob({
    required int userId,
    required String exportType,
    required String format,
    Map<String, dynamic>? filters,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/reports/exports'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'export_type': exportType,
        'format': format,
        'filters': filters,
      }),
    );

    if (response.statusCode == 200) {
      return ExportJob.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to create export job');
  }

  Future<ExportJob> getExportJob(int jobId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/reports/exports/$jobId'),
    );

    if (response.statusCode == 200) {
      return ExportJob.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to fetch export job');
  }
}

final enterpriseServiceProvider = Provider((ref) {
  return EnterpriseService();
});

final auditLogsProvider = FutureProvider.family<List<AuditLog>, int>((ref, userId) async {
  final service = ref.watch(enterpriseServiceProvider);
  return service.getAuditLogs(userId: userId);
});

final pendingModerationProvider = FutureProvider<List<ModerationItem>>((ref) async {
  final service = ref.watch(enterpriseServiceProvider);
  return service.getPendingModerationItems();
});

final notificationPreferencesProvider = FutureProvider.family<NotificationPreference, int>(
  (ref, userId) async {
    final service = ref.watch(enterpriseServiceProvider);
    return service.getNotificationPreferences(userId);
  },
);

final userNotificationsProvider = FutureProvider.family<List<Notification>, int>(
  (ref, userId) async {
    final service = ref.watch(enterpriseServiceProvider);
    return service.getNotifications(userId: userId);
  },
);

final userReportsProvider = FutureProvider.family<List<AdvancedReport>, int>(
  (ref, userId) async {
    final service = ref.watch(enterpriseServiceProvider);
    return service.getUserReports(userId: userId);
  },
);

final rateLimitStatusProvider = FutureProvider.family<RateLimitStatus, int>(
  (ref, userId) async {
    final service = ref.watch(enterpriseServiceProvider);
    return service.checkRateLimit(userId: userId);
  },
);
