import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/community_models.dart';
import 'package:aether_cms/models/content_quality_models.dart';
import 'package:aether_cms/screens/comments_screen.dart';
import 'package:aether_cms/screens/content_quality/content_quality_screen.dart';
import 'package:aether_cms/screens/logs_screen.dart';
import 'package:aether_cms/screens/push_notifications_screen.dart';
import 'package:aether_cms/screens/webhooks_screen.dart';
import 'package:aether_cms/services/community_service.dart';
import 'package:aether_cms/services/content_quality_service.dart';

class MockCommunityService extends Mock implements CommunityService {}

class MockContentQualityService extends Mock implements ContentQualityService {}

const _comment = ContentComment(id: 1, userId: 2, contentId: 4, text: 'Great video', status: 'published');

void main() {
  late MockCommunityService community;

  setUp(() {
    community = MockCommunityService();
    registerFallbackValue(<String>[]);
  });

  testWidgets('comments show the thread and post a new comment', (tester) async {
    when(() => community.fetchComments(4)).thenAnswer((_) async => [_comment]);
    when(() => community.postComment(contentId: 4, text: 'Thanks')).thenAnswer((_) async => _comment);

    await tester.pumpWidget(MaterialApp(
      home: CommentsScreen(resourceId: 4, resourceType: 'content', service: community),
    ));
    await tester.pumpAndSettle();
    expect(find.text('Great video'), findsOneWidget);

    await tester.enterText(find.byKey(const Key('comment-field')), 'Thanks');
    await tester.tap(find.byKey(const Key('post-comment')));
    await tester.pumpAndSettle();

    verify(() => community.postComment(contentId: 4, text: 'Thanks')).called(1);
  });

  testWidgets('comments say when there are none', (tester) async {
    when(() => community.fetchComments(4)).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(
      home: CommentsScreen(resourceId: 4, resourceType: 'content', service: community),
    ));
    await tester.pumpAndSettle();

    expect(find.text('No comments yet.'), findsOneWidget);
  });

  testWidgets('push notifications list devices and the recent notifications', (tester) async {
    when(() => community.fetchDevices()).thenAnswer((_) async => [
          const PushDevice(id: 3, deviceToken: 'tok', platform: 'ios', deviceName: 'Phone'),
        ]);
    when(() => community.fetchNotificationLogs()).thenAnswer((_) async => [
          const NotificationLog(id: 5, notificationType: 'system', title: 'Hi', body: 'Body', status: 'delivered'),
        ]);
    when(() => community.registerDevice(token: 'new-token', platform: 'android', name: null)).thenAnswer(
      (_) async => const PushDevice(id: 4, deviceToken: 'new-token', platform: 'android'),
    );

    await tester.pumpWidget(MaterialApp(home: PushNotificationsScreen(service: community)));
    await tester.pumpAndSettle();
    expect(find.text('Phone'), findsOneWidget);
    expect(find.text('delivered'), findsOneWidget);

    await tester.enterText(find.byKey(const Key('push-token-field')), 'new-token');
    await tester.tap(find.byKey(const Key('register-device')));
    await tester.pumpAndSettle();
    verify(() => community.registerDevice(token: 'new-token', platform: 'android', name: null)).called(1);
  });

  testWidgets('webhooks create an endpoint for the chosen events and run a test delivery', (tester) async {
    when(() => community.fetchWebhooks()).thenAnswer((_) async => [
          const OutboundWebhook(id: 6, url: 'https://hooks.example.com/x', events: ['content.published'], isActive: true),
        ]);
    when(() => community.fetchWebhookEvents()).thenAnswer((_) async => [
          const WebhookEventType(event: 'content.published', description: 'Published'),
          const WebhookEventType(event: 'user.created', description: 'New user'),
        ]);
    when(() => community.createWebhook(url: 'https://hooks.example.com/y', events: ['user.created'], description: null))
        .thenAnswer((_) async => const OutboundWebhook(id: 7, url: 'https://hooks.example.com/y', events: ['user.created'], isActive: true));
    when(() => community.testWebhook(6)).thenAnswer((_) async => {'status': 'delivered'});

    await tester.pumpWidget(MaterialApp(home: WebhooksScreen(service: community)));
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(const Key('webhook-url-field')), 'https://hooks.example.com/y');
    await tester.tap(find.byKey(const Key('event-user.created')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('create-webhook')));
    await tester.pumpAndSettle();
    verify(() => community.createWebhook(url: 'https://hooks.example.com/y', events: ['user.created'], description: null)).called(1);

    // The 'Webhook created.' snackbar is queued ahead of the test result; let it expire first.
    await tester.pump(const Duration(seconds: 6));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Test'));
    await tester.pumpAndSettle();
    verify(() => community.testWebhook(6)).called(1);
    expect(find.text('Test delivery: delivered'), findsOneWidget);
  });

  testWidgets('content quality shows each tool\'s checks and average', (tester) async {
    final quality = MockContentQualityService();
    when(() => quality.fetchOverview()).thenAnswer((_) async => const ContentQualityOverview(
          proofreadingChecks: 2,
          averageProofreadingScore: 88.5,
          readabilityChecks: 0,
          brandVoiceChecks: 1,
          averageBrandVoiceCompliance: 70,
          plagiarismChecks: 3,
          averagePlagiarismSimilarity: 4.25,
        ));

    await tester.pumpWidget(MaterialApp(home: ContentQualityScreen(service: quality)));
    await tester.pumpAndSettle();

    expect(find.text('88.5 average score'), findsOneWidget);
    expect(find.text('No checks yet'), findsOneWidget);
    expect(find.text('70.0% compliance'), findsOneWidget);
    expect(find.text('4.3% similarity'), findsOneWidget);
  });

  testWidgets('administration tools say they are used from the web dashboard', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: LogsScreen()));

    expect(find.byKey(const Key('web-only-notice')), findsOneWidget);
    expect(find.textContaining('Use it from the web dashboard'), findsOneWidget);
  });
}
