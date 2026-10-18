import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/quota_models.dart';
import 'package:aether_cms/screens/quota_screen.dart';
import 'package:aether_cms/services/quota_service.dart';

class MockQuotaService extends Mock implements QuotaService {}

void main() {
  late MockQuotaService service;

  setUp(() {
    service = MockQuotaService();
  });

  testWidgets('shows real usage against the stored API-call limit', (tester) async {
    when(() => service.fetchUsage()).thenAnswer((_) async => const QuotaUsage(
          apiCalls: 8500, apiCallLimit: 10000, storageGb: 0.45, bandwidthGb: 2.5,
        ));

    await tester.pumpWidget(MaterialApp(home: QuotaScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('8500 / 10000'), findsOneWidget);
    expect(find.text('85% used'), findsOneWidget);
    expect(find.text('0.45 GB'), findsOneWidget);
    expect(find.text('2.50 GB'), findsOneWidget);
    expect(find.text('Upgrade Plan'), findsNothing);
  });

  testWidgets('shows the failure and retries on request', (tester) async {
    var calls = 0;
    when(() => service.fetchUsage()).thenAnswer((_) async {
      calls++;
      if (calls == 1) throw StateError('Not authenticated');
      return const QuotaUsage(apiCalls: 0, apiCallLimit: 10000, storageGb: 0, bandwidthGb: 0);
    });

    await tester.pumpWidget(MaterialApp(home: QuotaScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.textContaining('Not authenticated'), findsOneWidget);

    await tester.tap(find.text('Try again'));
    await tester.pumpAndSettle();
    expect(find.text('0 / 10000'), findsOneWidget);
  });
}
