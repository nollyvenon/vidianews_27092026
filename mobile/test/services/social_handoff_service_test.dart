import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/social_auth_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data, {int statusCode = 200}) => Response<dynamic>(
      data: data,
      statusCode: statusCode,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late SocialAuthService service;

  setUp(() {
    dio = MockDio();
    service = SocialAuthService(dio);
  });

  test('authorizationUrl sends the app ticket as a query parameter', () async {
    when(() => dio.get<dynamic>(any(), queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({'authorization_url': 'https://accounts.google.com/auth?state=s'}));

    final uri = await service.authorizationUrl('google', ticket: 'abc123');

    expect(uri.host, 'accounts.google.com');
    verify(() => dio.get<dynamic>(
          '/auth/social/google/authorize',
          queryParameters: {'ticket': 'abc123'},
        )).called(1);
  });

  test('claimHandoff returns null while the browser step is pending (202)', () async {
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response({'status': 'pending'}, statusCode: 202));

    expect(await service.claimHandoff('ticket-value'), isNull);
  });

  test('claimHandoff returns the tokens once they are ready (200)', () async {
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response({
          'access_token': 'a',
          'refresh_token': 'r',
          'token_type': 'bearer',
        }));

    final tokens = await service.claimHandoff('ticket-value');

    expect(tokens?['access_token'], 'a');
    verify(() => dio.get<dynamic>('/auth/social/handoff/ticket-value')).called(1);
  });

  test('claimHandoff propagates a not-found error for unknown tickets', () async {
    when(() => dio.get<dynamic>(any())).thenThrow(DioException(
      requestOptions: RequestOptions(path: ''),
      response: _response({'detail': 'Unknown or expired sign-in'}, statusCode: 404),
    ));

    await expectLater(service.claimHandoff('ticket-value'), throwsA(isA<DioException>()));
  });
}
