// Registered API endpoint versions and the migrations between them.

import 'package:dio/dio.dart';

class EndpointVersion {
  final int id;
  final String endpoint;
  final String version;
  final bool deprecated;
  final DateTime? sunsetDate;

  const EndpointVersion({
    required this.id,
    required this.endpoint,
    required this.version,
    required this.deprecated,
    this.sunsetDate,
  });

  factory EndpointVersion.fromJson(Map<String, dynamic> json) => EndpointVersion(
        id: json['id'] as int,
        endpoint: json['endpoint'] as String,
        version: json['version'] as String,
        deprecated: json['deprecated'] as bool? ?? false,
        sunsetDate: json['sunset_date'] is String ? DateTime.tryParse(json['sunset_date'] as String) : null,
      );
}

class VersionMigration {
  final int id;
  final String oldVersion;
  final String newVersion;
  final String status;
  final DateTime? executedAt;

  const VersionMigration({
    required this.id,
    required this.oldVersion,
    required this.newVersion,
    required this.status,
    this.executedAt,
  });

  factory VersionMigration.fromJson(Map<String, dynamic> json) => VersionMigration(
        id: json['id'] as int,
        oldVersion: json['old_version'] as String,
        newVersion: json['new_version'] as String,
        status: json['status'] as String,
        executedAt: json['executed_at'] is String ? DateTime.tryParse(json['executed_at'] as String) : null,
      );
}

class ApiVersionsService {
  final Dio _dio;

  ApiVersionsService(this._dio);

  Future<List<EndpointVersion>> fetchVersions() async {
    final response = await _dio.get<dynamic>('/versions');
    return _rows(response.data).map(EndpointVersion.fromJson).toList();
  }

  Future<List<VersionMigration>> fetchMigrations() async {
    final response = await _dio.get<dynamic>('/versions/migrations');
    return _rows(response.data).map(VersionMigration.fromJson).toList();
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
