// Social login API: public provider list and token exchange, plus admin credential management.

import 'package:dio/dio.dart';
import '../models/social_auth_models.dart';

class SocialAuthService {
  final Dio _dio;

  SocialAuthService(this._dio);

  Future<List<SocialProvider>> listEnabledProviders() async {
    final response = await _dio.get<dynamic>('/auth/social/providers');
    return (response.data as List<dynamic>)
        .map((item) => SocialProvider.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  /// Consent URL for [provider]. Pass the app's [ticket] to hand the tokens back through [claimHandoff].
  Future<Uri> authorizationUrl(String provider, {String? ticket}) async {
    final response = await _dio.get<dynamic>(
      '/auth/social/$provider/authorize',
      queryParameters: ticket == null ? null : {'ticket': ticket},
    );
    return Uri.parse((response.data as Map<String, dynamic>)['authorization_url'] as String);
  }

  /// Tokens for a mobile sign-in, or null while the browser step is still pending.
  /// Throws a DioException (404) when the ticket is unknown or has expired.
  Future<Map<String, dynamic>?> claimHandoff(String ticket) async {
    final response = await _dio.get<dynamic>('/auth/social/handoff/$ticket');
    if (response.statusCode == 202) return null;
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> exchangeCode({
    required String provider,
    required String code,
    required String state,
  }) async {
    final response = await _dio.post<dynamic>(
      '/auth/social/$provider/exchange',
      data: {'code': code, 'state': state},
    );
    return response.data as Map<String, dynamic>;
  }

  Future<List<SocialProviderAdmin>> listProviders() async {
    final response = await _dio.get<dynamic>('/admin/social-providers');
    return (response.data as List<dynamic>)
        .map((item) => SocialProviderAdmin.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<SocialProviderAdmin> updateProvider(String provider, SocialProviderUpdate update) async {
    final response = await _dio.put<dynamic>(
      '/admin/social-providers/$provider',
      data: update.toJson(),
    );
    return SocialProviderAdmin.fromJson(response.data as Map<String, dynamic>);
  }
}
