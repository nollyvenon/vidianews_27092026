import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/screens/analytics_dashboard_screen.dart';
import 'package:aether_cms/screens/analytics_screen.dart';
import 'package:aether_cms/services/analytics_overview_service.dart';

class MockAnalyticsOverviewService extends Mock implements AnalyticsOverviewService {}

const _summary = AnalyticsSummary(days: 30, views: 1200, watchHours: 45.5, subscribers: 80);

void main() {
  late MockAnalyticsOverviewService service;

  setUp(() {
    service = MockAnalyticsOverviewService();
  });

  // The dashboard is a long list; a taller surface keeps every section built during the test.
  void useTallSurface(WidgetTester tester) {
    tester.view.devicePixelRatio = 1.0;
    tester.view.physicalSize = const Size(800, 3000);
    addTearDown(tester.view.reset);
  }

  testWidgets('dashboard shows the headline figures, daily engagement and revenue', (tester) async {
    useTallSurface(tester);
    when(() => service.fetchSummary(days: 30)).thenAnswer((_) async => _summary);
    when(() => service.fetchEngagement(days: 30)).thenAnswer((_) async => [
          const EngagementRow(date: '2026-10-10', activeUsers: 40, newUsers: 5),
        ]);
    when(() => service.fetchRevenue(days: 30)).thenAnswer((_) async => [
          const RevenueRow(date: '2026-10-10', totalRevenue: 19.99, transactionCount: 2),
        ]);

    await tester.pumpWidget(MaterialApp(home: AnalyticsDashboardScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('1200'), findsOneWidget);
    expect(find.text('45.5'), findsOneWidget);
    expect(find.text('80'), findsOneWidget);
    expect(find.text('\$19.99'), findsNWidgets(2));
    expect(find.text('40 active · 5 new'), findsOneWidget);
    expect(find.text('2 transactions'), findsOneWidget);
  });

  testWidgets('dashboard says when there is no engagement or revenue yet', (tester) async {
    useTallSurface(tester);
    when(() => service.fetchSummary(days: 30)).thenAnswer((_) async => _summary);
    when(() => service.fetchEngagement(days: 30)).thenAnswer((_) async => []);
    when(() => service.fetchRevenue(days: 30)).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: AnalyticsDashboardScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('No engagement recorded yet.'), findsOneWidget);
    expect(find.text('No revenue recorded yet.'), findsOneWidget);
  });

  testWidgets('summary screen shows the headline figures and recovers from a failure', (tester) async {
    var calls = 0;
    when(() => service.fetchSummary()).thenAnswer((_) async {
      calls++;
      if (calls == 1) throw StateError('Offline');
      return _summary;
    });

    await tester.pumpWidget(MaterialApp(home: AnalyticsScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.textContaining('Offline'), findsOneWidget);

    await tester.tap(find.text('Try again'));
    await tester.pumpAndSettle();
    expect(find.text('1200'), findsOneWidget);
    expect(find.text('Watch hours'), findsOneWidget);
  });
}
