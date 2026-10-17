// Mobile social sign-in without native deep links.
//
// 1. The app creates a random ticket and keeps it.
// 2. The backend returns a provider consent URL that carries only a hash of the ticket.
// 3. The user signs in in the browser; the web callback completes the exchange and parks the tokens.
// 4. The app polls with its ticket until the tokens are handed over (once).

import 'dart:convert';
import 'dart:math';

import '../services/social_auth_service.dart';

class SocialSignInTimeout implements Exception {
  const SocialSignInTimeout();

  @override
  String toString() => 'Sign-in took too long. Please try again.';
}

/// A 256-bit random ticket, URL-safe and without padding.
String generateHandoffTicket({Random? random}) {
  final source = random ?? Random.secure();
  final bytes = List<int>.generate(32, (_) => source.nextInt(256));
  return base64UrlEncode(bytes).replaceAll('=', '');
}

class SocialSignInFlow {
  final SocialAuthService _service;
  final Future<void> Function(Uri url) _launch;
  final Future<void> Function(String accessToken) _saveSession;
  final String Function() _newTicket;
  final Future<void> Function(Duration) _delay;
  final Duration _pollInterval;
  final Duration _timeout;

  SocialSignInFlow({
    required SocialAuthService service,
    required Future<void> Function(Uri url) launch,
    required Future<void> Function(String accessToken) saveSession,
    String Function()? newTicket,
    Future<void> Function(Duration)? delay,
    Duration pollInterval = const Duration(seconds: 2),
    Duration timeout = const Duration(minutes: 3),
  })  : _service = service,
        _launch = launch,
        _saveSession = saveSession,
        _newTicket = newTicket ?? generateHandoffTicket,
        _delay = delay ?? Future<void>.delayed,
        _pollInterval = pollInterval,
        _timeout = timeout;

  /// Runs the whole sign-in for [provider] and stores the session when it completes.
  Future<void> signIn(String provider) async {
    final ticket = _newTicket();
    final url = await _service.authorizationUrl(provider, ticket: ticket);
    await _launch(url);

    final maxPolls = _timeout.inMilliseconds ~/ _pollInterval.inMilliseconds;
    for (var attempt = 0; attempt < maxPolls; attempt++) {
      await _delay(_pollInterval);
      final tokens = await _service.claimHandoff(ticket);
      if (tokens != null) {
        await _saveSession(tokens['access_token'] as String);
        return;
      }
    }
    throw const SocialSignInTimeout();
  }
}
