import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/billing_admin_models.dart';
import 'package:aether_cms/models/social_auth_models.dart';
import 'package:aether_cms/screens/admin/billing/billing_admin_screen.dart';
import 'package:aether_cms/screens/admin/social_login/social_login_admin_screen.dart';
import 'package:aether_cms/services/billing_admin_service.dart';
import 'package:aether_cms/services/social_auth_service.dart';

class MockSocialAuthService extends Mock implements SocialAuthService {}

class MockBillingAdminService extends Mock implements BillingAdminService {}

class _FakeSocialUpdate extends Fake implements SocialProviderUpdate {}

const _google = SocialProviderAdmin(
  provider: 'google',
  displayName: 'Google',
  enabled: true,
  clientId: 'g-id',
  clientSecretSet: true,
  redirectUri: 'https://app.test/auth/social/google/callback',
  scopes: 'openid email profile',
);

SubscriptionAdmin _sub() => const SubscriptionAdmin(
      id: 7,
      userId: 3,
      userEmail: 'subscriber@example.com',
      tier: 'pro',
      billingCycle: 'monthly',
      amount: 49,
      isActive: true,
      renewsAt: null,
      canceledAt: null,
    );

Future<void> _pump(WidgetTester tester, Widget screen) => tester.pumpWidget(MaterialApp(home: screen));

void main() {
  setUpAll(() {
    registerFallbackValue(_FakeSocialUpdate());
  });

  group('SocialLoginAdminScreen', () {
    late MockSocialAuthService service;

    setUp(() {
      service = MockSocialAuthService();
    });

    testWidgets('shows each provider with its stored client ID and no secret', (tester) async {
      when(() => service.listProviders()).thenAnswer((_) async => [_google]);

      await _pump(tester, SocialLoginAdminScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('Google'), findsOneWidget);
      expect(find.text('g-id'), findsOneWidget);
      expect(find.text('Stored. Enter a value to replace it.'), findsOneWidget);
    });

    testWidgets('saves the edited provider and shows confirmation', (tester) async {
      when(() => service.listProviders()).thenAnswer((_) async => [_google]);
      when(() => service.updateProvider(any(), any())).thenAnswer((_) async => _google);

      await _pump(tester, SocialLoginAdminScreen(service: service));
      await tester.pumpAndSettle();

      await tester.enterText(find.byKey(const Key('google-client-secret')), 'new-secret');
      await tester.tap(find.widgetWithText(ElevatedButton, 'Save'));
      await tester.pumpAndSettle();

      final captured = verify(() => service.updateProvider('google', captureAny())).captured.single
          as SocialProviderUpdate;
      expect(captured.clientSecret, 'new-secret');
      expect(captured.clientId, 'g-id');
      expect(find.text('Google saved'), findsOneWidget);
    });

    testWidgets('shows the server message when the save is refused', (tester) async {
      when(() => service.listProviders()).thenAnswer((_) async => [_google]);
      when(() => service.updateProvider(any(), any())).thenThrow(StateError('Cannot enable Google: missing client_secret'));

      await _pump(tester, SocialLoginAdminScreen(service: service));
      await tester.pumpAndSettle();
      await tester.tap(find.widgetWithText(ElevatedButton, 'Save'));
      await tester.pumpAndSettle();

      expect(find.textContaining('Cannot enable Google'), findsOneWidget);
    });

    testWidgets('shows the load error instead of the list', (tester) async {
      when(() => service.listProviders()).thenAnswer((_) async => throw StateError('Admin access required'));

      await _pump(tester, SocialLoginAdminScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.textContaining('Admin access required'), findsOneWidget);
    });
  });

  group('BillingAdminScreen', () {
    late MockBillingAdminService service;

    setUp(() {
      service = MockBillingAdminService();
      when(() => service.listSubscriptions()).thenAnswer(
        (_) async => AdminPage<SubscriptionAdmin>(items: [_sub()], total: 1),
      );
      when(() => service.listTransactions(source: any(named: 'source'))).thenAnswer(
        (_) async => const AdminPage<TransactionAdmin>(items: [], total: 0),
      );
    });

    testWidgets('lists subscriptions with the customer email and amount', (tester) async {
      await _pump(tester, BillingAdminScreen(service: service));
      await tester.pumpAndSettle();

      expect(find.text('subscriber@example.com'), findsOneWidget);
      expect(find.textContaining('49.00'), findsOneWidget);
    });

    testWidgets('cancels a subscription only after confirmation', (tester) async {
      when(() => service.cancelSubscription(7)).thenAnswer((_) async => _sub());

      await _pump(tester, BillingAdminScreen(service: service));
      await tester.pumpAndSettle();
      await tester.tap(find.byTooltip('Cancel subscription'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Keep'));
      await tester.pumpAndSettle();
      verifyNever(() => service.cancelSubscription(any()));

      await tester.tap(find.byTooltip('Cancel subscription'));
      await tester.pumpAndSettle();
      await tester.tap(find.widgetWithText(TextButton, 'Cancel subscription'));
      await tester.pumpAndSettle();

      verify(() => service.cancelSubscription(7)).called(1);
    });

    testWidgets('shows an empty state when there are no transactions', (tester) async {
      await _pump(tester, BillingAdminScreen(service: service));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Transactions'));
      await tester.pumpAndSettle();

      expect(find.text('No transactions found.'), findsOneWidget);
    });
  });
}
