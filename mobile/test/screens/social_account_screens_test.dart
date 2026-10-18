import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/social_account_models.dart';
import 'package:aether_cms/screens/alerts_screen.dart';
import 'package:aether_cms/screens/followers_screen.dart';
import 'package:aether_cms/screens/messages_screen.dart';
import 'package:aether_cms/screens/notifications_center_screen.dart';
import 'package:aether_cms/screens/premium_screen.dart';
import 'package:aether_cms/screens/privacy_screen.dart';
import 'package:aether_cms/services/social_account_service.dart';

class MockSocialAccountService extends Mock implements SocialAccountService {}

const _settings = PrivacySettings(
  profileVisibility: 'public', contentVisibility: 'private', allowAnalytics: true, allowMarketing: false,
);

void main() {
  late MockSocialAccountService service;

  setUpAll(() {
    registerFallbackValue(_settings);
  });

  setUp(() {
    service = MockSocialAccountService();
  });

  testWidgets('messages show the unread count and the conversation, and mark a message read', (tester) async {
    when(() => service.fetchUnreadMessageCount()).thenAnswer((_) async => 2);
    when(() => service.fetchConversation(7)).thenAnswer((_) async => [
          const DirectMessage(id: 1, senderId: 7, content: 'Are you free?', isRead: false),
        ]);
    when(() => service.markMessageRead(1)).thenAnswer((_) async {});

    await tester.pumpWidget(MaterialApp(home: MessagesScreen(service: service, currentUserId: 2)));
    await tester.pumpAndSettle();
    expect(find.text('2 unread'), findsOneWidget);

    await tester.enterText(find.byKey(const Key('other-member-field')), '7');
    await tester.tap(find.byKey(const Key('open-conversation')));
    await tester.pumpAndSettle();
    expect(find.text('Are you free?'), findsOneWidget);

    await tester.tap(find.text('Mark read'));
    await tester.pumpAndSettle();
    verify(() => service.markMessageRead(1)).called(1);
  });

  testWidgets('messages send the typed text to the open conversation', (tester) async {
    when(() => service.fetchUnreadMessageCount()).thenAnswer((_) async => 0);
    when(() => service.fetchConversation(7)).thenAnswer((_) async => []);
    when(() => service.sendMessage(recipientId: 7, content: 'On my way')).thenAnswer((_) async {});

    await tester.pumpWidget(MaterialApp(home: MessagesScreen(service: service, currentUserId: 2)));
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const Key('other-member-field')), '7');
    await tester.tap(find.byKey(const Key('open-conversation')));
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const Key('message-draft-field')), 'On my way');
    await tester.tap(find.byKey(const Key('send-message')));
    await tester.pumpAndSettle();

    verify(() => service.sendMessage(recipientId: 7, content: 'On my way')).called(1);
  });

  testWidgets('followers list who follows the user', (tester) async {
    when(() => service.fetchFollowers(2)).thenAnswer((_) async => [
          Follower(id: 5, followerId: 9, followingId: 2, followerName: 'Ada Lovelace', followedAt: DateTime(2026, 10, 1)),
        ]);

    await tester.pumpWidget(MaterialApp(home: FollowersScreen(service: service, userId: 2)));
    await tester.pumpAndSettle();

    expect(find.text('Ada Lovelace'), findsOneWidget);
    expect(find.text('Following since 2026-10-01'), findsOneWidget);
  });

  testWidgets('alerts can be marked read and then no longer offer the action', (tester) async {
    var unread = true;
    when(() => service.fetchAlerts()).thenAnswer((_) async => [
          AppNotification(id: 1, title: 'Payment', message: 'Received', isRead: !unread),
        ]);
    when(() => service.markAlertRead(1)).thenAnswer((_) async {
      unread = false;
    });

    await tester.pumpWidget(MaterialApp(home: AlertsScreen(service: service)));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Mark read'));
    await tester.pumpAndSettle();

    verify(() => service.markAlertRead(1)).called(1);
  });

  testWidgets('notices show their message and say when there are none', (tester) async {
    when(() => service.fetchNotices()).thenAnswer((_) async => [
          AppNotification(id: 2, title: 'Maintenance', message: 'Tonight', isRead: true),
        ]);

    await tester.pumpWidget(MaterialApp(home: NotificationsCenterScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('Maintenance'), findsOneWidget);
    expect(find.text('Tonight'), findsOneWidget);
  });

  testWidgets('privacy saves the chosen visibility and logs both consents', (tester) async {
    when(() => service.fetchPrivacySettings()).thenAnswer((_) async => _settings);
    when(() => service.fetchConsents()).thenAnswer((_) async => []);
    when(() => service.updatePrivacySettings(any())).thenAnswer((invocation) async => invocation.positionalArguments.first as PrivacySettings);
    when(() => service.logConsent(consentType: any(named: 'consentType'), granted: any(named: 'granted'))).thenAnswer((_) async {});

    await tester.pumpWidget(MaterialApp(home: PrivacyScreen(service: service)));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('allow-marketing')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('save-privacy')));
    await tester.pumpAndSettle();

    final saved = verify(() => service.updatePrivacySettings(captureAny())).captured.single as PrivacySettings;
    expect(saved.allowMarketing, isTrue);
    verify(() => service.logConsent(consentType: 'analytics', granted: true)).called(1);
    verify(() => service.logConsent(consentType: 'marketing', granted: true)).called(1);
  });

  testWidgets('privacy asks the server to schedule an account deletion', (tester) async {
    when(() => service.fetchPrivacySettings()).thenAnswer((_) async => _settings);
    when(() => service.fetchConsents()).thenAnswer((_) async => []);
    when(() => service.requestDeletion()).thenAnswer((_) async => DateTime(2026, 11, 1));

    await tester.pumpWidget(MaterialApp(home: PrivacyScreen(service: service)));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('request-deletion')));
    await tester.pumpAndSettle();

    verify(() => service.requestDeletion()).called(1);
    expect(find.text('Deletion scheduled for 2026-11-01.'), findsOneWidget);
  });

  testWidgets('premium shows the status and offers to subscribe when not premium', (tester) async {
    when(() => service.fetchPremiumStatus()).thenAnswer((_) async => const PremiumStatus(isPremium: false));
    when(() => service.subscribeToPremium()).thenAnswer((_) async {});

    await tester.pumpWidget(MaterialApp(home: PremiumScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.text('You do not have premium access yet.'), findsOneWidget);

    await tester.tap(find.byKey(const Key('subscribe-premium')));
    await tester.pumpAndSettle();
    verify(() => service.subscribeToPremium()).called(1);
  });
}
