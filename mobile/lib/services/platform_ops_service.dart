// Read access to platform operations: cache statistics and policies, data pipelines and API usage.

import 'package:dio/dio.dart';
import '../models/platform_ops_models.dart';

class PlatformOpsService {
  final Dio _dio;

  PlatformOpsService(this._dio);

  Future<CacheStats> fetchCacheStats() async {
    final response = await _dio.get<dynamic>('/cache/stats/summary');
    return CacheStats.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<CachePolicy>> fetchCachePolicies() async {
    final response = await _dio.get<dynamic>('/cache/policies');
    return _rows(response.data).map(CachePolicy.fromJson).toList();
  }

  Future<List<Pipeline>> fetchPipelines() async {
    final response = await _dio.get<dynamic>('/pipelines/');
    return _rows(response.data).map(Pipeline.fromJson).toList();
  }

  Future<List<ApiUsage>> fetchApiUsage() async {
    final response = await _dio.get<dynamic>('/api-docs/usage');
    return _rows(response.data).map(ApiUsage.fromJson).toList();
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
