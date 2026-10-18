// Shared `package:http` client for the screens and services that use it.
// Attaches the signed-in user's bearer token (stored by the login flow) to every request,
// the same way the Dio client does.

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import 'authenticated_dio.dart';

class AuthenticatedHttpClient extends http.BaseClient {
  final http.Client _inner;

  AuthenticatedHttpClient({http.Client? inner}) : _inner = inner ?? http.Client();

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(kAuthTokenKey);
    if (token != null && token.isNotEmpty) {
      request.headers['Authorization'] = 'Bearer $token';
    }
    return _inner.send(request);
  }

  @override
  void close() {
    _inner.close();
    super.close();
  }
}

/// The one HTTP client used by the screens and services built on `package:http`.
final http.Client authenticatedHttp = AuthenticatedHttpClient();
