// Shared HTTP client for administrative and account-scoped API calls.
// Attaches the signed-in user's bearer token (stored by the login flow) to every request.

import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// API base URL. Build for another environment with --dart-define=API_BASE_URL=https://...
const String kApiBaseUrl = String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000/api/v1');
const String kAuthTokenKey = 'auth_token';

/// Scheme and host of the API, for callers whose paths already include /api/v1.
final String kApiOrigin = kApiBaseUrl.replaceFirst('/api/v1', '');

/// The API's WebSocket base, derived from [kApiBaseUrl].
final String kApiWsBaseUrl = kApiBaseUrl.replaceFirst(RegExp(r'^http'), 'ws');

Dio createAuthenticatedDio({String baseUrl = kApiBaseUrl, Dio? dio}) {
  final client = dio ??
      Dio(BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 15),
      ));
  client.interceptors.add(InterceptorsWrapper(
    onRequest: (options, handler) async {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString(kAuthTokenKey);
      if (token != null && token.isNotEmpty) {
        options.headers['Authorization'] = 'Bearer $token';
      }
      handler.next(options);
    },
  ));
  return client;
}

/// Human-readable message from an API error. Uses the server's ``detail`` when present.
String messageFromError(Object error) {
  if (error is DioException) {
    final data = error.response?.data;
    if (data is Map<String, dynamic> && data['detail'] is String) {
      return data['detail'] as String;
    }
    if (error.response?.statusCode == 403) {
      return 'You do not have permission to do this.';
    }
    return error.message ?? 'Request failed';
  }
  return error.toString();
}
