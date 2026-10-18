import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/billing_account_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

DioException _status(int code) => DioException(
      requestOptions: RequestOptions(path: ''),
      response: Response<dynamic>(
        statusCode: code,
        data: {'detail': 'No subscription on this account'},
        requestOptions: RequestOptions(path: ''),
      ),
    );

Map<String, dynamic> _subscriptionJson() => {
      'id': 3,
      'tier': 'pro',
      'billing_cycle': 'monthly',
      'amount': 49,
      'is_active': true,
      'started_at': '2026-09-01T00:00:00Z',
      'renews_at': '2026-11-01T00:00:00Z',
      'canceled_at': null,
    };

void main() {
  late MockDio dio;
  late BillingAccountService service;

  setUp(() {
    dio = MockDio();
    service = BillingAccountService(dio);
  });

  test('fetchSubscription parses the active plan', () async {
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response(_subscriptionJson()));

    final subscription = await service.fetchSubscription();

    expect(subscription, isNotNull);
    expect(subscription!.tierLabel, 'Pro');
    expect(subscription.amount, 49.0);
    expect(subscription.renewsAt, DateTime.parse('2026-11-01T00:00:00Z'));
    verify(() => dio.get<dynamic>('/billing/subscription')).called(1);
  });

  test('fetchSubscription returns null when the account has never subscribed', () async {
    when(() => dio.get<dynamic>(any())).thenThrow(_status(404));

    expect(await service.fetchSubscription(), isNull);
  });

  test('fetchSubscription rethrows other failures', () async {
    when(() => dio.get<dynamic>(any())).thenThrow(_status(500));

    await expectLater(service.fetchSubscription(), throwsA(isA<DioException>()));
  });

  test('fetchInvoices parses each invoice and its paid state', () async {
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response([
          {
            'id': 9, 'subscription_id': 3, 'amount': 49, 'status': 'completed',
            'due_date': null, 'paid_date': '2026-10-02T00:00:00Z', 'created_at': '2026-10-01T00:00:00Z',
          },
          {
            'id': 10, 'subscription_id': 3, 'amount': 49, 'status': 'pending',
            'due_date': '2026-10-15T00:00:00Z', 'paid_date': null, 'created_at': '2026-10-10T00:00:00Z',
          },
        ]));

    final invoices = await service.fetchInvoices();

    expect(invoices.map((invoice) => invoice.isPaid), [true, false]);
    expect(invoices.last.dueDate, DateTime.parse('2026-10-15T00:00:00Z'));
    verify(() => dio.get<dynamic>('/billing/invoices')).called(1);
  });

  test('fetchPayments parses the account payments', () async {
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response([
          {'id': 1, 'invoice_id': 9, 'amount': 49, 'status': 'completed', 'payment_method': 'card', 'created_at': null},
        ]));

    final payments = await service.fetchPayments();

    expect(payments.single.paymentMethod, 'card');
    expect(payments.single.createdAt, isNull);
    verify(() => dio.get<dynamic>('/billing/payments')).called(1);
  });
}
