import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Webhook payload signing that matches the backend's `WebhookService`:
/// HMAC-SHA256 over the UTF-8 payload, keyed with the UTF-8 secret, encoded as lowercase hex.
class WebhookSignature {
  const WebhookSignature._();

  /// Returns the lowercase hex HMAC-SHA256 signature for [payload].
  static String generate(String payload, String secretKey) {
    final hmac = Hmac(sha256, utf8.encode(secretKey));
    return hmac.convert(utf8.encode(payload)).toString();
  }

  /// Returns true only when [signature] is the valid signature for [payload].
  ///
  /// The comparison is constant-time over the full length, so timing does not reveal
  /// how many leading characters matched.
  static bool verify(String payload, String signature, String secretKey) {
    final expected = generate(payload, secretKey);
    if (signature.length != expected.length) {
      return false;
    }
    var difference = 0;
    for (var i = 0; i < expected.length; i++) {
      difference |= signature.codeUnitAt(i) ^ expected.codeUnitAt(i);
    }
    return difference == 0;
  }
}
