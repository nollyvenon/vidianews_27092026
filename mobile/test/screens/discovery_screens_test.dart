import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/discovery_models.dart';
import 'package:aether_cms/screens/creator_screen.dart';
import 'package:aether_cms/screens/discover_screen.dart';
import 'package:aether_cms/screens/docs_screen.dart';
import 'package:aether_cms/screens/livestream_screen.dart';
import 'package:aether_cms/screens/partnerships_screen.dart';
import 'package:aether_cms/screens/recommendations_screen.dart';
import 'package:aether_cms/screens/search_screen.dart';
import 'package:aether_cms/screens/video_processing_screen.dart';
import 'package:aether_cms/services/discovery_service.dart';

class MockDiscoveryService extends Mock implements DiscoveryService {}

const _recommendation = Recommendation(id: 1, contentId: 9, title: 'Launch recap', creator: 'Ada', views: 4, reason: 'Popular');

void main() {
  late MockDiscoveryService service;

  setUp(() {
    service = MockDiscoveryService();
  });

  testWidgets('discover shows recommendations and trending topics', (tester) async {
    when(() => service.fetchRecommendations()).thenAnswer((_) async => [_recommendation]);
    when(() => service.fetchTrending()).thenAnswer((_) async => [
          const TrendingTopic(id: 2, topic: 'Flutter', mentionCount: 12),
        ]);

    await tester.pumpWidget(MaterialApp(home: DiscoverScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('Launch recap'), findsOneWidget);
    expect(find.text('Popular'), findsOneWidget);
    expect(find.text('Flutter'), findsOneWidget);
    expect(find.text('12 mentions'), findsOneWidget);
  });

  testWidgets('recommendations list the content with its views', (tester) async {
    when(() => service.fetchRecommendations(limit: 20)).thenAnswer((_) async => [_recommendation]);

    await tester.pumpWidget(MaterialApp(home: RecommendationsScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('Launch recap'), findsOneWidget);
    expect(find.text('4 views'), findsOneWidget);
  });

  testWidgets('creator shows the profile, saves the bio and lists creators', (tester) async {
    when(() => service.fetchCreatorProfile()).thenAnswer((_) async => const CreatorProfile(
          id: 1, userId: 2, bio: 'Hello', followers: 10, isVerified: true,
        ));
    when(() => service.fetchCreators(verifiedOnly: false)).thenAnswer((_) async => [
          const CreatorProfile(id: 1, userId: 2, bio: 'Hello', followers: 10, isVerified: true),
        ]);
    when(() => service.saveCreatorBio('Updated bio')).thenAnswer((_) async => const CreatorProfile(
          id: 1, userId: 2, bio: 'Updated bio', followers: 10, isVerified: true,
        ));

    await tester.pumpWidget(MaterialApp(home: CreatorScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.text('10 followers · verified'), findsOneWidget);

    await tester.enterText(find.byKey(const Key('bio-field')), 'Updated bio');
    await tester.tap(find.byKey(const Key('save-bio')));
    await tester.pumpAndSettle();
    verify(() => service.saveCreatorBio('Updated bio')).called(1);
  });

  testWidgets('creator without a profile is told so', (tester) async {
    when(() => service.fetchCreatorProfile()).thenThrow(_httpError(404, 'Not found'));
    when(() => service.fetchCreators(verifiedOnly: false)).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: CreatorScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('You do not have a creator profile yet.'), findsOneWidget);
  });

  testWidgets('a server failure while loading the creator profile is shown, not hidden', (tester) async {
    when(() => service.fetchCreatorProfile()).thenThrow(_httpError(500, 'Profile service is down'));
    when(() => service.fetchCreators(verifiedOnly: false)).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: CreatorScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('Profile service is down'), findsOneWidget);
    expect(find.text('You do not have a creator profile yet.'), findsNothing);
  });

  testWidgets('search runs the query and lists the matches', (tester) async {
    when(() => service.search('launch')).thenAnswer((_) async => [
          const SearchResult(id: 3, resourceType: 'video', resourceId: 9, title: 'Launch', content: null),
        ]);

    await tester.pumpWidget(MaterialApp(home: SearchScreen(service: service)));
    await tester.enterText(find.byKey(const Key('search-field')), 'launch');
    await tester.tap(find.byKey(const Key('search-button')));
    await tester.pumpAndSettle();

    expect(find.text('Launch'), findsOneWidget);
    expect(find.text('video'), findsNWidgets(2));
  });

  testWidgets('video processing shows each job with its status and progress', (tester) async {
    when(() => service.fetchVideoJobs()).thenAnswer((_) async => [
          const VideoJob(contentId: 4, title: 'Intro', status: 'encoding', progress: 43),
        ]);

    await tester.pumpWidget(MaterialApp(home: VideoProcessingScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('Intro'), findsOneWidget);
    expect(find.text('encoding · 43%'), findsOneWidget);
  });

  testWidgets('livestream lists who is live and shows the key of a new stream', (tester) async {
    when(() => service.fetchActiveStreams()).thenAnswer((_) async => [
          const ActiveStream(id: 5, title: 'Q&A', viewers: 12),
        ]);
    when(() => service.startLiveStream(title: 'Next', description: '')).thenAnswer((_) async => {
          'id': 6, 'stream_key': 'key-123', 'status': 'created',
        });

    await tester.pumpWidget(MaterialApp(home: LivestreamScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.text('12 watching'), findsOneWidget);

    await tester.enterText(find.byKey(const Key('stream-title-field')), 'Next');
    await tester.tap(find.byKey(const Key('start-stream')));
    await tester.pumpAndSettle();
    expect(find.text('Stream key: key-123'), findsOneWidget);
  });

  testWidgets('partnerships list existing partners and propose a new one', (tester) async {
    when(() => service.fetchPartnerships()).thenAnswer((_) async => [
          const Partnership(id: 1, type: 'sponsorship', status: 'active'),
        ]);
    when(() => service.proposePartnership(partnerId: '7', partnershipType: 'sponsorship')).thenAnswer((_) async {});

    await tester.pumpWidget(MaterialApp(home: PartnershipsScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.text('active'), findsOneWidget);

    await tester.enterText(find.byKey(const Key('partner-field')), '7');
    await tester.tap(find.byKey(const Key('propose-partnership')));
    await tester.pumpAndSettle();
    verify(() => service.proposePartnership(partnerId: '7', partnershipType: 'sponsorship')).called(1);
  });

  testWidgets('docs show the guides and the API reference', (tester) async {
    when(() => service.fetchDocs()).thenAnswer((_) async => [
          const Doc(id: 1, title: 'Start here', slug: 'start', docType: 'guide', views: 9, version: '1.0'),
        ]);
    when(() => service.fetchApiReference()).thenAnswer((_) async => [
          const ApiReference(id: 2, method: 'GET', endpoint: '/posts'),
        ]);

    await tester.pumpWidget(MaterialApp(home: DocsScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('Start here'), findsOneWidget);
    expect(find.text('GET /posts'), findsOneWidget);
  });
}

/// An HTTP failure as Dio reports it, carrying the status and the server's detail.
DioException _httpError(int status, String detail) {
  final options = RequestOptions(path: '/monetization/creator-profile');
  return DioException(
    requestOptions: options,
    response: Response<dynamic>(
      requestOptions: options,
      statusCode: status,
      data: {'detail': detail},
    ),
    type: DioExceptionType.badResponse,
  );
}
