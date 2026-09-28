import 'package:flutter_test/flutter_test.dart';
import '../lib/models/enterprise_features_models.dart';
import '../lib/providers/enterprise_features_providers.dart';

void main() {
  group('Enterprise Features Models', () {
    test('AuditLog model creation', () {
      final now = DateTime.now();
      final log = AuditLog(
        id: 1,
        userId: 123,
        action: 'login',
        severity: 'info',
        createdAt: now,
      );

      expect(log.id, 1);
      expect(log.userId, 123);
      expect(log.action, 'login');
      expect(log.severity, 'info');
    });

    test('AccessControl model creation', () {
      final now = DateTime.now();
      final access = AccessControl(
        id: 1,
        userId: 123,
        resourceType: 'content',
        resourceId: 456,
        accessLevel: 'protected',
        permissions: ['read', 'write'],
        grantedAt: now,
      );

      expect(access.id, 1);
      expect(access.userId, 123);
      expect(access.resourceType, 'content');
      expect(access.permissions.length, 2);
    });

    test('RoleAssignment model creation', () {
      final now = DateTime.now();
      final role = RoleAssignment(
        id: 1,
        userId: 123,
        role: 'admin',
        permissions: ['read', 'write', 'delete'],
        canEditContent: true,
        canDeleteContent: true,
        canManageUsers: true,
        canAccessAnalytics: true,
        canAccessAdmin: true,
        createdAt: now,
      );

      expect(role.role, 'admin');
      expect(role.canEditContent, true);
      expect(role.canAccessAdmin, true);
    });

    test('ModerationItem model creation', () {
      final now = DateTime.now();
      final item = ModerationItem(
        id: 1,
        contentId: 123,
        contentType: 'article',
        status: 'pending',
        reason: 'Contains inappropriate content',
        flags: ['spam', 'violence'],
        confidenceScore: 0.85,
        createdAt: now,
      );

      expect(item.contentId, 123);
      expect(item.status, 'pending');
      expect(item.flags.length, 2);
      expect(item.confidenceScore, 0.85);
    });

    test('ComplianceCheckResult model creation', () {
      final result = ComplianceCheckResult(
        isCompliant: false,
        violations: [
          {'rule_id': 1, 'severity': 'high'},
        ],
        violationCount: 1,
      );

      expect(result.isCompliant, false);
      expect(result.violationCount, 1);
    });

    test('RateLimitStatus model creation', () {
      final status = RateLimitStatus(
        limited: false,
        minuteRemaining: 50,
        hourRemaining: 900,
        dayRemaining: 9000,
      );

      expect(status.limited, false);
      expect(status.minuteRemaining, 50);
    });

    test('NotificationPreference model creation', () {
      final now = DateTime.now();
      final pref = NotificationPreference(
        id: 1,
        userId: 123,
        emailEnabled: true,
        pushEnabled: true,
        smsEnabled: false,
        inAppEnabled: true,
        frequency: 'immediate',
        createdAt: now,
      );

      expect(pref.emailEnabled, true);
      expect(pref.smsEnabled, false);
      expect(pref.frequency, 'immediate');
    });

    test('Notification model creation', () {
      final now = DateTime.now();
      final notif = Notification(
        id: 1,
        userId: 123,
        notificationType: 'alert',
        title: 'Test Alert',
        message: 'This is a test notification',
        read: false,
        createdAt: now,
      );

      expect(notif.notificationType, 'alert');
      expect(notif.read, false);
    });

    test('AlertConfiguration model creation', () {
      final now = DateTime.now();
      final config = AlertConfiguration(
        id: 1,
        userId: 123,
        alertType: 'high_cpu',
        condition: 'cpu > 80',
        threshold: 80.0,
        enabled: true,
        notificationChannels: ['email', 'push'],
        createdAt: now,
      );

      expect(config.alertType, 'high_cpu');
      expect(config.threshold, 80.0);
    });

    test('AdvancedReport model creation', () {
      final now = DateTime.now();
      final report = AdvancedReport(
        id: 1,
        userId: 123,
        name: 'Monthly Report',
        reportType: 'analytics',
        format: 'pdf',
        status: 'completed',
        generatedAt: now,
        createdAt: now,
      );

      expect(report.reportType, 'analytics');
      expect(report.status, 'completed');
    });

    test('ReportTemplate model creation', () {
      final now = DateTime.now();
      final template = ReportTemplate(
        id: 1,
        name: 'Standard Analytics',
        reportType: 'analytics',
        sections: ['overview', 'details', 'trends'],
        format: 'pdf',
        createdAt: now,
      );

      expect(template.name, 'Standard Analytics');
      expect(template.sections.length, 3);
    });

    test('ScheduledReport model creation', () {
      final now = DateTime.now();
      final scheduled = ScheduledReport(
        id: 1,
        userId: 123,
        name: 'Daily Report',
        cronExpression: '0 9 * * *',
        enabled: true,
        recipientEmails: ['user@example.com'],
        createdAt: now,
      );

      expect(scheduled.name, 'Daily Report');
      expect(scheduled.enabled, true);
    });

    test('ExportJob model creation', () {
      final now = DateTime.now();
      final job = ExportJob(
        id: 1,
        userId: 123,
        exportType: 'user_data',
        format: 'csv',
        status: 'processing',
        progress: 50,
        recordCount: 5000,
        createdAt: now,
      );

      expect(job.exportType, 'user_data');
      expect(job.progress, 50);
    });

    test('SecurityStats model creation', () {
      final stats = SecurityStats(
        totalAuditLogs: 1000,
        moderationItemsPending: 5,
        recentThrottles: 2,
        unreadNotifications: 3,
        activeAlerts: 1,
      );

      expect(stats.totalAuditLogs, 1000);
      expect(stats.moderationItemsPending, 5);
    });
  });

  group('Enterprise Features Model Serialization', () {
    test('AuditLog JSON serialization', () {
      final now = DateTime.now();
      final log = AuditLog(
        id: 1,
        userId: 123,
        action: 'login',
        severity: 'info',
        createdAt: now,
      );

      final json = log.toJson();
      expect(json['id'], 1);
      expect(json['user_id'], 123);
      expect(json['action'], 'login');
    });

    test('RoleAssignment JSON deserialization', () {
      final now = DateTime.now();
      final json = {
        'id': 1,
        'user_id': 123,
        'role': 'admin',
        'permissions': ['read', 'write'],
        'can_edit_content': true,
        'can_delete_content': true,
        'can_manage_users': true,
        'can_access_analytics': true,
        'can_access_admin': true,
        'created_at': now.toIso8601String(),
      };

      final role = RoleAssignment.fromJson(json);
      expect(role.role, 'admin');
      expect(role.permissions.length, 2);
    });
  });
}
