// The signed-in account's subscription, invoices and payments (GET /billing/*).

import 'package:dio/dio.dart';
import '../models/billing_account_models.dart';

class BillingAccountService {
  final Dio _dio;

  BillingAccountService(this._dio);

  /// The active subscription, or the most recent one. Null when the account has never subscribed.
  Future<AccountSubscription?> fetchSubscription() async {
    try {
      final response = await _dio.get<dynamic>('/billing/subscription');
      return AccountSubscription.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (error) {
      if (error.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  Future<List<AccountInvoice>> fetchInvoices() async {
    final response = await _dio.get<dynamic>('/billing/invoices');
    return (response.data as List<dynamic>)
        .map((item) => AccountInvoice.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<List<AccountPayment>> fetchPayments() async {
    final response = await _dio.get<dynamic>('/billing/payments');
    return (response.data as List<dynamic>)
        .map((item) => AccountPayment.fromJson(item as Map<String, dynamic>))
        .toList();
  }
}
