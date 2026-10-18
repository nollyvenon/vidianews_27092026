import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/discovery_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late DiscoveryService service;

  setUp(() {
    dio = MockDio();
    service = DiscoveryService(dio);
  });

  test('the creator profile is read and the bio is saved as a query value', () async {
    when(() => dio.get<dynamic>('/monetization/creator-profile')).thenAnswer((_) async => _response({
          'id': 1, 'user_id': 2, 'bio': 'Hello', 'followers': 10, 'is_verified': true,
        }));
    when(() => dio.post<dynamic>('/monetization/creator-profile', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({'id': 1, 'user_id': 2, 'bio': 'New bio', 'followers': 10, 'is_verified': true}));

    final profile = await service.fetchCreatorProfile();
    final saved = await service.saveCreatorBio('New bio');

    expect(profile.isVerified, isTrue);
    expect(saved.bio, 'New bio');
    final query = verify(() => dio.post<dynamic>('/monetization/creator-profile', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single as Map<String, dynamic>;
    expect(query, {'bio': 'New bio'});
  });

  test('the creator directory can be limited to verified creators', () async {
    when(() => dio.get<dynamic>('/monetization/creators', queryParameters: {'verified_only': true}))
        .thenAnswer((_) async => _response([
              {'id': 1, 'user_id': 2, 'bio': null, 'followers': 3, 'is_verified': true},
            ]));

    final creators = await service.fetchCreators(verifiedOnly: true);

    expect(creators.single.followers, 3);
  });

  test('recommendations, trending topics and search read their lists', () async {
    when(() => dio.get<dynamic>('/recommendations', queryParameters: {'limit': 10})).thenAnswer((_) async => _response([
          {'id': 1, 'content_id': 9, 'title': 'Launch', 'creator': 'Ada', 'views': 4, 'reason': 'Popular'},
        ]));
    when(() => dio.get<dynamic>('/trending', queryParameters: {'limit': 10})).thenAnswer((_) async => _response([
          {'id': 2, 'topic': 'Flutter', 'score': 1.5, 'mention_count': 12},
        ]));
    when(() => dio.get<dynamic>('/system/search', queryParameters: {'q': 'launch'})).thenAnswer((_) async => _response([
          {'id': 3, 'resource_type': 'video', 'resource_id': 9, 'title': 'Launch', 'content': null},
        ]));

    expect((await service.fetchRecommendations()).single.reason, 'Popular');
    expect((await service.fetchTrending()).single.mentionCount, 12);
    expect((await service.search('launch')).single.resourceType, 'video');
  });

  test('video jobs round the progress to a whole percentage', () async {
    when(() => dio.get<dynamic>('/content/videos/processing')).thenAnswer((_) async => _response([
          {'video_id': 1, 'content_id': 4, 'title': 'Intro', 'status': 'encoding', 'progress': 42.6, 'qualities': []},
        ]));

    final jobs = await service.fetchVideoJobs();

    expect(jobs.single.progress, 43);
  });

  test('starting a stream sends its title and description and returns the stream key', () async {
    when(() => dio.post<dynamic>('/livestream', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({'id': 5, 'stream_key': 'key-123', 'status': 'created'}));

    final created = await service.startLiveStream(title: 'Q&A', description: 'Ask anything');

    expect(created['stream_key'], 'key-123');
    final query = verify(() => dio.post<dynamic>('/livestream', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single as Map<String, dynamic>;
    expect(query, {'title': 'Q&A', 'description': 'Ask anything'});
  });

  test('a partnership proposal sends the partner and type', () async {
    when(() => dio.post<dynamic>('/partnerships', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({}));

    await service.proposePartnership(partnerId: '7', partnershipType: 'affiliate');

    final query = verify(() => dio.post<dynamic>('/partnerships', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single as Map<String, dynamic>;
    expect(query, {'partner_id': '7', 'partnership_type': 'affiliate'});
  });

  test('documentation and the API reference are read as lists', () async {
    when(() => dio.get<dynamic>('/docs')).thenAnswer((_) async => _response([
          {'id': 1, 'title': 'Start', 'slug': 'start', 'doc_type': 'guide', 'views': 9, 'version': '1.0'},
        ]));
    when(() => dio.get<dynamic>('/docs/api/all')).thenAnswer((_) async => _response([
          {'id': 2, 'method': 'GET', 'endpoint': '/posts'},
        ]));

    expect((await service.fetchDocs()).single.docType, 'guide');
    expect((await service.fetchApiReference()).single.endpoint, '/posts');
  });

  test('a non-list response is rejected', () async {
    when(() => dio.get<dynamic>('/trending', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response({'detail': 'nope'}));

    expect(service.fetchTrending(), throwsA(isA<FormatException>()));
  });
}
