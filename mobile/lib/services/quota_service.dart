// Usage and quota API for the signed-in account.

import 'package:dio/dio.dart';
import '../models/quota_models.dart';

class QuotaService {
  final Dio _dio;

  QuotaService(this._dio);

  Future<QuotaUsage> fetchUsage() async {
    final response = await _dio.get<dynamic>('/quota/usage');
    return QuotaUsage.fromJson(response.data as Map<String, dynamic>);
  }
}
