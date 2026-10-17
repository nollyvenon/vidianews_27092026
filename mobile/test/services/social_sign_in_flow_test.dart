import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/social_auth_service.dart';
import 'package:aether_cms/services/social_sign_in_flow.dart';

class MockSocialAuthService extends Mock implements SocialAuthService {}

void main() {
  late MockSocialAuthService service;
  late List<Uri> launched;
  late List<String> savedTokens;
  late int delays;

  setUp(() {
    service = MockSocialAuthService();
    launched = [];
    savedTokens = [];
    delays = 0;
  });

  SocialSignInFlow buildFlow({Duration timeout = const Duration(seconds: 10)}) => SocialSignInFlow(
        service: service,
        launch: (url) async => launched.add(url),
        saveSession: (token) async => savedTokens.add(token),
        newTicket: () => 'ticket-' + 'x' * 40,
        delay: (_) async => delays++,
        pollInterval: const Duration(seconds: 2),
        timeout: timeout,
      );

  group('generateHandoffTicket', () {
    test('is URL-safe, unpadded and long enough to be unguessable', () {
      final ticket = generateHandoffTicket(random: Random(7));

      expect(ticket.length, greaterThanOrEqualTo(40));
      expect(RegExp(r'^[A-Za-z0-9_-]+$').hasMatch(ticket), isTrue);
    });

    test('differs between calls with a secure source', () {
      expect(generateHandoffTicket(), isNot(generateHandoffTicket()));
    });
  });

  test('signIn opens the consent page with the ticket and stores the tokens once claimed', () async {
    final ticket = 'ticket-' + 'x' * 40;
    when(() => service.authorizationUrl('google', ticket: ticket))
        .thenAnswer((_) async => Uri.parse('https://accounts.google.com/auth'));
    var claims = 0;
    when(() => service.claimHandoff(ticket)).thenAnswer((_) async {
      claims++;
      return claims < 3 ? null : {'access_token': 'app-token', 'refresh_token': 'r'};
    });

    await buildFlow().signIn('google');

    expect(launched.single, Uri.parse('https://accounts.google.com/auth'));
    expect(claims, 3);
    expect(delays, 3);
    expect(savedTokens, ['app-token']);
  });

  test('signIn times out when the browser step never completes', () async {
    when(() => service.authorizationUrl(any(), ticket: any(named: 'ticket')))
        .thenAnswer((_) async => Uri.parse('https://accounts.google.com/auth'));
    when(() => service.claimHandoff(any())).thenAnswer((_) async => null);

    await expectLater(
      buildFlow(timeout: const Duration(seconds: 6)).signIn('google'),
      throwsA(isA<SocialSignInTimeout>()),
    );
    expect(delays, 3);
    expect(savedTokens, isEmpty);
  });

  test('signIn surfaces an expired or unknown ticket without storing anything', () async {
    when(() => service.authorizationUrl(any(), ticket: any(named: 'ticket')))
        .thenAnswer((_) async => Uri.parse('https://accounts.google.com/auth'));
    when(() => service.claimHandoff(any())).thenThrow(StateError('Unknown or expired sign-in'));

    await expectLater(buildFlow().signIn('google'), throwsA(isA<StateError>()));
    expect(savedTokens, isEmpty);
  });

  test('signIn does not open the browser when the consent URL cannot be created', () async {
    when(() => service.authorizationUrl(any(), ticket: any(named: 'ticket')))
        .thenThrow(StateError('GitHub login is not enabled'));

    await expectLater(buildFlow().signIn('github'), throwsA(isA<StateError>()));
    expect(launched, isEmpty);
  });
}
