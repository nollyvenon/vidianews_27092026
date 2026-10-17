// Admin API for subscriptions and transactions.

import 'package:dio/dio.dart';
import '../models/billing_admin_models.dart';

class BillingAdminService {
  final Dio _dio;

  BillingAdminService(this._dio);

  Future<AdminPage<SubscriptionAdmin>> listSubscriptions({
    bool? isActive,
    String? tier,
    int skip = 0,
    int limit = 50,
  }) async {
    final response = await _dio.get<dynamic>(
      '/admin/subscriptions',
      queryParameters: {
        if (isActive != null) 'is_active': isActive,
        if (tier != null) 'tier': tier,
        'skip': skip,
        'limit': limit,
      },
    );
    return AdminPage.fromJson(response.data as Map<String, dynamic>, SubscriptionAdmin.fromJson);
  }

  Future<SubscriptionAdmin> changeTier(int subscriptionId, String tier) async {
    final response = await _dio.patch<dynamic>(
      '/admin/subscriptions/$subscriptionId',
      data: {'tier': tier},
    );
    return SubscriptionAdmin.fromJson(response.data as Map<String, dynamic>);
  }

  Future<SubscriptionAdmin> cancelSubscription(int subscriptionId) async {
    final response = await _dio.post<dynamic>('/admin/subscriptions/$subscriptionId/cancel');
    return SubscriptionAdmin.fromJson(response.data as Map<String, dynamic>);
  }

  Future<AdminPage<TransactionAdmin>> listTransactions({
    String source = 'all',
    String? status,
    int skip = 0,
    int limit = 50,
  }) async {
    final response = await _dio.get<dynamic>(
      '/admin/transactions',
      queryParameters: {
        'source': source,
        if (status != null) 'status': status,
        'skip': skip,
        'limit': limit,
      },
    );
    return AdminPage.fromJson(response.data as Map<String, dynamic>, TransactionAdmin.fromJson);
  }
}
