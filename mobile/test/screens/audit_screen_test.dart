import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/audit_models.dart';
import 'package:aether_cms/screens/audit_screen.dart';
import 'package:aether_cms/services/audit_service.dart';

class MockAuditService extends Mock implements AuditService {}

void main() {
  late MockAuditService service;

  setUp(() {
    service = MockAuditService();
  });

  testWidgets('lists each entry with its action, resource and administrator', (tester) async {
    when(() => service.fetchEntries()).thenAnswer((_) async => [
          AuditEntry(
            id: 1,
            adminId: 7,
            action: 'delete',
            resourceType: 'user',
            changes: const {},
            timestamp: DateTime.utc(2026, 10, 17),
          ),
        ]);

    await tester.pumpWidget(MaterialApp(home: AuditScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('delete · user'), findsOneWidget);
    expect(find.textContaining('Admin #7'), findsOneWidget);
  });

  testWidgets('says so when the trail is empty', (tester) async {
    when(() => service.fetchEntries()).thenAnswer((_) async => []);

    await tester.pumpWidget(MaterialApp(home: AuditScreen(service: service)));
    await tester.pumpAndSettle();

    expect(find.text('No audit entries yet.'), findsOneWidget);
  });

  testWidgets('shows the refusal for non-administrators and retries', (tester) async {
    var calls = 0;
    when(() => service.fetchEntries()).thenAnswer((_) async {
      calls++;
      if (calls == 1) throw StateError('Admin access required');
      return [];
    });

    await tester.pumpWidget(MaterialApp(home: AuditScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.textContaining('Admin access required'), findsOneWidget);

    await tester.tap(find.text('Try again'));
    await tester.pumpAndSettle();
    expect(find.text('No audit entries yet.'), findsOneWidget);
  });
}
