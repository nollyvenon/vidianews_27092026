import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/social_auth_models.dart';
import 'package:aether_cms/services/authenticated_dio.dart';
import 'package:aether_cms/services/social_auth_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data, {int statusCode = 200}) => Response<dynamic>(
      data: data,
      statusCode: statusCode,
      requestOptions: RequestOptions(path: ''),
    );

Map<String, dynamic> _adminProvider({
  String provider = 'google',
  bool enabled = true,
  String? clientId = 'g-id',
  bool secretSet = true,
}) =>
    {
      'provider': provider,
      'display_name': 'Google',
      'enabled': enabled,
      'client_id': clientId,
      'client_secret_set': secretSet,
      'redirect_uri': 'https://app.test/auth/social/google/callback',
      'scopes': 'openid email profile',
      'updated_at': null,
    };

void main() {
  late MockDio dio;
  late SocialAuthService service;

  setUp(() {
    dio = MockDio();
    service = SocialAuthService(dio);
  });

  group('public login calls', () {
    test('listEnabledProviders parses the enabled providers', () async {
      when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response([
            {'provider': 'github', 'display_name': 'GitHub'},
          ]));

      final providers = await service.listEnabledProviders();

      expect(providers.single.provider, 'github');
      expect(providers.single.displayName, 'GitHub');
      verify(() => dio.get<dynamic>('/auth/social/providers')).called(1);
    });

    test('authorizationUrl returns the provider consent URL', () async {
      when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response({
            'authorization_url': 'https://accounts.google.com/o/oauth2/v2/auth?state=s',
          }));

      final uri = await service.authorizationUrl('google');

      expect(uri.host, 'accounts.google.com');
      expect(uri.queryParameters['state'], 's');
      verify(() => dio.get<dynamic>('/auth/social/google/authorize')).called(1);
    });

    test('exchangeCode posts the code and state and returns the token body', () async {
      when(() => dio.post<dynamic>(any(), data: any(named: 'data'))).thenAnswer((_) async => _response({
            'access_token': 'a',
            'refresh_token': 'r',
            'token_type': 'bearer',
          }));

      final tokens = await service.exchangeCode(provider: 'github', code: 'c1', state: 's1');

      expect(tokens['access_token'], 'a');
      verify(() => dio.post<dynamic>(
            '/auth/social/github/exchange',
            data: {'code': 'c1', 'state': 's1'},
          )).called(1);
    });
  });

  group('admin credential calls', () {
    test('listProviders parses configuration without secrets', () async {
      when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response([_adminProvider()]));

      final providers = await service.listProviders();

      expect(providers.single.clientSecretSet, isTrue);
      expect(providers.single.clientId, 'g-id');
    });

    test('updateProvider sends the update body and parses the saved provider', () async {
      when(() => dio.put<dynamic>(any(), data: any(named: 'data')))
          .thenAnswer((_) async => _response(_adminProvider(clientId: 'new-id')));

      final saved = await service.updateProvider(
        'google',
        const SocialProviderUpdate(
          enabled: true,
          clientId: 'new-id',
          redirectUri: 'https://app.test/auth/social/google/callback',
          scopes: 'openid email profile',
        ),
      );

      expect(saved.clientId, 'new-id');
      verify(() => dio.put<dynamic>(
            '/admin/social-providers/google',
            data: {
              'enabled': true,
              'client_id': 'new-id',
              'redirect_uri': 'https://app.test/auth/social/google/callback',
              'scopes': 'openid email profile',
            },
          )).called(1);
    });
  });

  group('SocialProviderUpdate', () {
    test('includes the secret only when one is entered', () {
      const withSecret = SocialProviderUpdate(
        enabled: false,
        clientId: 'id',
        clientSecret: 'shh',
        redirectUri: 'u',
        scopes: 's',
      );
      const withoutSecret = SocialProviderUpdate(enabled: false, clientId: 'id', redirectUri: 'u', scopes: 's');
      const emptySecret = SocialProviderUpdate(
        enabled: false,
        clientId: 'id',
        clientSecret: '',
        redirectUri: 'u',
        scopes: 's',
      );

      expect(withSecret.toJson()['client_secret'], 'shh');
      expect(withoutSecret.toJson().containsKey('client_secret'), isFalse);
      expect(emptySecret.toJson().containsKey('client_secret'), isFalse);
    });
  });

  group('messageFromError', () {
    test('prefers the server detail message', () {
      final error = DioException(
        requestOptions: RequestOptions(path: ''),
        response: _response({'detail': 'Cannot enable Google: missing client_id'}, statusCode: 422),
      );

      expect(messageFromError(error), 'Cannot enable Google: missing client_id');
    });

    test('explains a forbidden response that has no detail message', () {
      final error = DioException(
        requestOptions: RequestOptions(path: ''),
        response: _response(null, statusCode: 403),
      );

      expect(messageFromError(error), 'You do not have permission to do this.');
    });

    test('falls back to the transport message and to plain errors', () {
      final error = DioException(requestOptions: RequestOptions(path: ''), message: 'Connection timed out');

      expect(messageFromError(error), 'Connection timed out');
      expect(messageFromError(StateError('boom')), contains('boom'));
    });
  });
}
