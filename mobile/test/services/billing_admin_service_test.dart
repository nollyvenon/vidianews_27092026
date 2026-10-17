import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/billing_admin_models.dart';
import 'package:aether_cms/services/billing_admin_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

Map<String, dynamic> _subscription({bool active = true, String tier = 'pro'}) => {
      'id': 7,
      'user_id': 3,
      'user_email': 'subscriber@example.com',
      'organization_id': 1,
      'tier': tier,
      'billing_cycle': 'monthly',
      'amount': 49,
      'is_active': active,
      'started_at': '2026-09-01T00:00:00Z',
      'renews_at': '2026-11-01T00:00:00Z',
      'canceled_at': active ? null : '2026-10-17T00:00:00Z',
    };

void main() {
  late MockDio dio;
  late BillingAdminService service;

  setUp(() {
    dio = MockDio();
    service = BillingAdminService(dio);
  });

  group('listSubscriptions', () {
    test('sends the filters and parses the page', () async {
      when(() => dio.get<dynamic>(any(), queryParameters: any(named: 'queryParameters')))
          .thenAnswer((_) async => _response({
                'items': [_subscription()],
                'total': 1,
                'skip': 0,
                'limit': 50,
              }));

      final page = await service.listSubscriptions(isActive: true, tier: 'pro');

      expect(page.total, 1);
      expect(page.items.single.userEmail, 'subscriber@example.com');
      expect(page.items.single.amount, 49.0);
      verify(() => dio.get<dynamic>('/admin/subscriptions', queryParameters: {
            'is_active': true,
            'tier': 'pro',
            'skip': 0,
            'limit': 50,
          })).called(1);
    });

    test('omits filters that were not set', () async {
      when(() => dio.get<dynamic>(any(), queryParameters: any(named: 'queryParameters')))
          .thenAnswer((_) async => _response({'items': [], 'total': 0, 'skip': 0, 'limit': 50}));

      await service.listSubscriptions();

      verify(() => dio.get<dynamic>('/admin/subscriptions', queryParameters: {
            'skip': 0,
            'limit': 50,
          })).called(1);
    });
  });

  test('changeTier patches the subscription and returns the updated record', () async {
    when(() => dio.patch<dynamic>(any(), data: any(named: 'data')))
        .thenAnswer((_) async => _response(_subscription(tier: 'enterprise')));

    final sub = await service.changeTier(7, 'enterprise');

    expect(sub.tier, 'enterprise');
    verify(() => dio.patch<dynamic>('/admin/subscriptions/7', data: {'tier': 'enterprise'})).called(1);
  });

  test('cancelSubscription posts to the cancel endpoint', () async {
    when(() => dio.post<dynamic>(any())).thenAnswer((_) async => _response(_subscription(active: false)));

    final sub = await service.cancelSubscription(7);

    expect(sub.isActive, isFalse);
    expect(sub.canceledAt, isNotNull);
    verify(() => dio.post<dynamic>('/admin/subscriptions/7/cancel')).called(1);
  });

  test('listTransactions passes the source and status and parses both sources', () async {
    when(() => dio.get<dynamic>(any(), queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({
              'items': [
                {
                  'source': 'checkout',
                  'id': 2,
                  'user_email': 'buyer@example.com',
                  'amount': 20,
                  'currency': 'USD',
                  'status': 'failed',
                  'payment_method': 'credit_card',
                  'reference': 'txn-9',
                  'created_at': '2026-10-02T10:00:00Z',
                },
              ],
              'total': 1,
              'skip': 0,
              'limit': 50,
            }));

    final page = await service.listTransactions(source: 'checkout', status: 'failed');

    final tx = page.items.single;
    expect(tx.source, 'checkout');
    expect(tx.reference, 'txn-9');
    expect(tx.createdAt, DateTime.parse('2026-10-02T10:00:00Z'));
    verify(() => dio.get<dynamic>('/admin/transactions', queryParameters: {
          'source': 'checkout',
          'status': 'failed',
          'skip': 0,
          'limit': 50,
        })).called(1);
  });

  test('TransactionAdmin defaults the currency to USD when the server omits it', () {
    final tx = TransactionAdmin.fromJson({
      'source': 'subscription',
      'id': 1,
      'user_email': null,
      'amount': 5,
      'currency': null,
      'status': 'completed',
      'payment_method': 'card',
      'reference': null,
      'created_at': null,
    });

    expect(tx.currency, 'USD');
    expect(tx.createdAt, isNull);
  });
}
