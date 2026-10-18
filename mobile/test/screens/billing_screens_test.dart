import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/billing_account_models.dart';
import 'package:aether_cms/screens/billing_screen.dart';
import 'package:aether_cms/screens/invoices_screen.dart';
import 'package:aether_cms/screens/subscriptions_screen.dart';
import 'package:aether_cms/services/billing_account_service.dart';

class MockBillingAccountService extends Mock implements BillingAccountService {}

const _plan = AccountSubscription(
  id: 3,
  tier: 'pro',
  billingCycle: 'monthly',
  amount: 49,
  isActive: true,
  renewsAt: null,
  canceledAt: null,
);

final _paid = AccountInvoice(
  id: 9, subscriptionId: 3, amount: 49, status: 'completed',
  dueDate: null, paidDate: null, createdAt: DateTime.utc(2026, 10, 1),
);

final _pending = AccountInvoice(
  id: 10, subscriptionId: 3, amount: 19, status: 'pending',
  dueDate: null, paidDate: null, createdAt: DateTime.utc(2026, 10, 10),
);

Future<void> _pump(WidgetTester tester, Widget screen) => tester.pumpWidget(MaterialApp(home: screen));

void main() {
  late MockBillingAccountService service;

  setUp(() {
    service = MockBillingAccountService();
  });

  group('SubscriptionsScreen', () {
    testWidgets('shows the account plan with its price', (tester) async {
      when(() => service.fetchSubscription()).thenAnswer((_) async => _plan);

      await _pump(tester, SubscriptionsScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('Pro'), findsOneWidget);
      expect(find.textContaining('\$49.00 · monthly'), findsOneWidget);
      expect(find.text('Active'), findsOneWidget);
    });

    testWidgets('says so when the account has no subscription', (tester) async {
      when(() => service.fetchSubscription()).thenAnswer((_) async => null);

      await _pump(tester, SubscriptionsScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('This account has no subscription.'), findsOneWidget);
    });

    testWidgets('shows a failure with a retry', (tester) async {
      var calls = 0;
      when(() => service.fetchSubscription()).thenAnswer((_) async {
        calls++;
        if (calls == 1) throw StateError('Service unavailable');
        return _plan;
      });

      await _pump(tester, SubscriptionsScreen(service: service));
      await tester.pumpAndSettle();
      expect(find.textContaining('Service unavailable'), findsOneWidget);

      await tester.tap(find.text('Try again'));
      await tester.pumpAndSettle();
      expect(find.text('Pro'), findsOneWidget);
    });
  });

  group('BillingScreen', () {
    testWidgets('shows the plan and the latest invoices with their state', (tester) async {
      when(() => service.fetchSubscription()).thenAnswer((_) async => _plan);
      when(() => service.fetchInvoices()).thenAnswer((_) async => [_paid, _pending]);

      await _pump(tester, BillingScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('Current plan'), findsOneWidget);
      expect(find.text('Invoice #9'), findsOneWidget);
      expect(find.text('Paid'), findsOneWidget);
      expect(find.text('pending'), findsOneWidget);
      expect(find.text('Manage Plan'), findsNothing);
    });

    testWidgets('shows No plan for an account that has never subscribed', (tester) async {
      when(() => service.fetchSubscription()).thenAnswer((_) async => null);
      when(() => service.fetchInvoices()).thenAnswer((_) async => []);

      await _pump(tester, BillingScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('No plan'), findsOneWidget);
      expect(find.text('No invoices yet.'), findsOneWidget);
    });
  });

  group('InvoicesScreen', () {
    testWidgets('totals only the paid invoices', (tester) async {
      when(() => service.fetchInvoices()).thenAnswer((_) async => [_paid, _pending]);

      await _pump(tester, InvoicesScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('\$49.00'), findsWidgets);
      expect(find.text('2'), findsOneWidget);
      expect(find.text('Invoice #10'), findsOneWidget);
    });

    testWidgets('says so when there are no invoices', (tester) async {
      when(() => service.fetchInvoices()).thenAnswer((_) async => []);

      await _pump(tester, InvoicesScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('No invoices yet.'), findsOneWidget);
    });
  });
}
