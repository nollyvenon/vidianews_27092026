// Admin audit log API.

import 'package:dio/dio.dart';
import '../models/audit_models.dart';

class AuditService {
  final Dio _dio;

  AuditService(this._dio);

  Future<List<AuditEntry>> fetchEntries({int limit = 100, int offset = 0, int? adminId}) async {
    final response = await _dio.get<dynamic>(
      '/admin/audit-logs',
      queryParameters: {
        'limit': limit,
        'offset': offset,
        if (adminId != null) 'admin_id': adminId,
      },
    );
    return (response.data as List<dynamic>)
        .map((item) => AuditEntry.fromJson(item as Map<String, dynamic>))
        .toList();
  }
}
