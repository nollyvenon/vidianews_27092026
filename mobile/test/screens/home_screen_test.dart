import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/screens/features_menu_screen.dart';
import 'package:aether_cms/screens/home_screen.dart';
import 'package:aether_cms/services/dashboard_service.dart';

class MockDashboardService extends Mock implements DashboardService {}

void main() {
  late MockDashboardService service;

  setUp(() {
    service = MockDashboardService();
  });

  testWidgets('home shows the signed-in user totals and recent activity', (tester) async {
    when(() => service.fetchSummary()).thenAnswer((_) async => const DashboardSummary(
          videos: 3, articles: 2, chats: 7, monthlySpend: 15.5,
        ));
    when(() => service.fetchRecentActivity()).thenAnswer((_) async => [
          ActivityEntry(id: 1, action: 'create', description: 'Published a video', createdAt: DateTime(2026, 10, 10)),
        ]);

    await tester.pumpWidget(MaterialApp(home: HomeScreen(dashboardService: service)));
    await tester.pumpAndSettle();

    expect(find.text('3 Videos'), findsOneWidget);
    expect(find.text('2 Articles'), findsOneWidget);
    expect(find.text('7 Chats'), findsOneWidget);
    expect(find.text('\$15.50 Spent this month'), findsOneWidget);
    expect(find.text('Published a video'), findsOneWidget);
  });

  testWidgets('home says when there is no activity yet', (tester) async {
    when(() => service.fetchSummary()).thenAnswer((_) async => const DashboardSummary(
          videos: 0, articles: 0, chats: 0, monthlySpend: 0,
        ));
    when(() => service.fetchRecentActivity()).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: HomeScreen(dashboardService: service)));
    await tester.pumpAndSettle();

    expect(find.text('No recent activity yet.'), findsOneWidget);
  });

  testWidgets('home recovers from a failed load', (tester) async {
    var calls = 0;
    when(() => service.fetchSummary()).thenAnswer((_) async {
      calls++;
      if (calls == 1) throw StateError('Network down');
      return const DashboardSummary(videos: 1, articles: 0, chats: 0, monthlySpend: 0);
    });
    when(() => service.fetchRecentActivity()).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: HomeScreen(dashboardService: service)));
    await tester.pumpAndSettle();
    expect(find.textContaining('Network down'), findsOneWidget);

    await tester.tap(find.text('Try again'));
    await tester.pumpAndSettle();
    expect(find.text('1 Videos'), findsOneWidget);
  });

  testWidgets('the app bar opens the list of every feature', (tester) async {
    when(() => service.fetchSummary()).thenAnswer((_) async => const DashboardSummary(
          videos: 0, articles: 0, chats: 0, monthlySpend: 0,
        ));
    when(() => service.fetchRecentActivity()).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: HomeScreen(dashboardService: service)));
    await tester.pumpAndSettle();
    await tester.tap(find.byTooltip('All features'));
    await tester.pumpAndSettle();

    expect(find.byType(FeaturesMenuScreen), findsOneWidget);
    expect(find.text('Account & social'), findsOneWidget);
    expect(find.byKey(const Key('feature-Activity')), findsOneWidget);
  });
}
