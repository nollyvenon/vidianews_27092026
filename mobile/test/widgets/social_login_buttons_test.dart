import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/social_auth_models.dart';
import 'package:aether_cms/services/social_auth_service.dart';
import 'package:aether_cms/services/social_sign_in_flow.dart';
import 'package:aether_cms/widgets/social_login_buttons.dart';

class MockSocialAuthService extends Mock implements SocialAuthService {}

class MockSocialSignInFlow extends Mock implements SocialSignInFlow {}

const _google = SocialProvider(provider: 'google', displayName: 'Google');
const _github = SocialProvider(provider: 'github', displayName: 'GitHub');

Future<void> _pump(
  WidgetTester tester, {
  required SocialAuthService service,
  required SocialSignInFlow flow,
  required VoidCallback onSignedIn,
}) {
  return tester.pumpWidget(MaterialApp(
    home: Scaffold(
      body: SingleChildScrollView(
        child: SocialLoginButtons(service: service, flow: flow, onSignedIn: onSignedIn),
      ),
    ),
  ));
}

void main() {
  late MockSocialAuthService service;
  late MockSocialSignInFlow flow;

  setUp(() {
    service = MockSocialAuthService();
    flow = MockSocialSignInFlow();
  });

  testWidgets('shows nothing when no provider is enabled', (tester) async {
    when(() => service.listEnabledProviders()).thenAnswer((_) async => []);

    await _pump(tester, service: service, flow: flow, onSignedIn: () {});
    await tester.pumpAndSettle();

    expect(find.text('Or continue with'), findsNothing);
    expect(find.byType(OutlinedButton), findsNothing);
  });

  testWidgets('shows nothing when the provider list cannot be loaded', (tester) async {
    when(() => service.listEnabledProviders()).thenAnswer((_) async => throw StateError('offline'));

    await _pump(tester, service: service, flow: flow, onSignedIn: () {});
    await tester.pumpAndSettle();

    expect(find.byType(OutlinedButton), findsNothing);
  });

  testWidgets('shows one button per enabled provider', (tester) async {
    when(() => service.listEnabledProviders()).thenAnswer((_) async => [_google, _github]);

    await _pump(tester, service: service, flow: flow, onSignedIn: () {});
    await tester.pumpAndSettle();

    expect(find.text('Continue with Google'), findsOneWidget);
    expect(find.text('Continue with GitHub'), findsOneWidget);
  });

  testWidgets('a successful sign-in runs the flow and reports it', (tester) async {
    var signedIn = 0;
    when(() => service.listEnabledProviders()).thenAnswer((_) async => [_google]);
    when(() => flow.signIn('google')).thenAnswer((_) async {});

    await _pump(tester, service: service, flow: flow, onSignedIn: () => signedIn++);
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('social-google')));
    await tester.pumpAndSettle();

    verify(() => flow.signIn('google')).called(1);
    expect(signedIn, 1);
  });

  testWidgets('shows the wait state and disables every button while the browser step runs', (tester) async {
    final browserStep = Completer<void>();
    when(() => service.listEnabledProviders()).thenAnswer((_) async => [_google, _github]);
    when(() => flow.signIn('google')).thenAnswer((_) => browserStep.future);

    await _pump(tester, service: service, flow: flow, onSignedIn: () {});
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('social-google')));
    await tester.pump();

    expect(find.text('Waiting for browser sign-in...'), findsOneWidget);
    expect(tester.widget<OutlinedButton>(find.byKey(const Key('social-github'))).onPressed, isNull);

    browserStep.complete();
    await tester.pumpAndSettle();
  });

  testWidgets('a failed sign-in shows the message and does not report success', (tester) async {
    var signedIn = 0;
    when(() => service.listEnabledProviders()).thenAnswer((_) async => [_google]);
    when(() => flow.signIn('google')).thenThrow(const SocialSignInTimeout());

    await _pump(tester, service: service, flow: flow, onSignedIn: () => signedIn++);
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('social-google')));
    await tester.pumpAndSettle();

    expect(find.text('Sign-in took too long. Please try again.'), findsOneWidget);
    expect(signedIn, 0);
    expect(find.text('Continue with Google'), findsOneWidget);
  });
}
