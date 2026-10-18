import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/quota_models.dart';
import 'package:aether_cms/services/quota_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late QuotaService service;

  setUp(() {
    dio = MockDio();
    service = QuotaService(dio);
  });

  test('fetchUsage parses the usage document', () async {
    when(() => dio.get<dynamic>(any())).thenAnswer((_) async => _response({
          'api_calls': 8500,
          'api_call_limit': 10000,
          'storage_gb': 0.45,
          'bandwidth_gb': 2,
        }));

    final usage = await service.fetchUsage();

    expect(usage.apiCalls, 8500);
    expect(usage.apiCallLimit, 10000);
    expect(usage.storageGb, 0.45);
    expect(usage.bandwidthGb, 2.0);
    expect(usage.apiCallRatio, closeTo(0.85, 1e-9));
    verify(() => dio.get<dynamic>('/quota/usage')).called(1);
  });

  test('the API-call ratio is capped at 1 and is 0 without a limit', () {
    const over = QuotaUsage(apiCalls: 12000, apiCallLimit: 10000, storageGb: 0, bandwidthGb: 0);
    const none = QuotaUsage(apiCalls: 5, apiCallLimit: 0, storageGb: 0, bandwidthGb: 0);

    expect(over.apiCallRatio, 1.0);
    expect(none.apiCallRatio, 0.0);
  });
}
