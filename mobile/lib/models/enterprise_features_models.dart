import 'package:freezed_annotation/freezed_annotation.dart';

part 'enterprise_features_models.freezed.dart';
part 'enterprise_features_models.g.dart';

@freezed
class AuditLog with _$AuditLog {
  const factory AuditLog({
    required int id,
    required int userId,
    required String action,
    String? resourceType,
    int? resourceId,
    String? status,
    String? ipAddress,
    String? severity,
    required DateTime createdAt,
  }) = _AuditLog;

  factory AuditLog.fromJson(Map<String, dynamic> json) => _$AuditLogFromJson(json);
}

@freezed
class AccessControl with _$AccessControl {
  const factory AccessControl({
    required int id,
    required int userId,
    required String resourceType,
    required int resourceId,
    required String accessLevel,
    required List<String> permissions,
    int? grantedBy,
    required DateTime grantedAt,
    DateTime? expiresAt,
  }) = _AccessControl;

  factory AccessControl.fromJson(Map<String, dynamic> json) => _$AccessControlFromJson(json);
}

@freezed
class RoleAssignment with _$RoleAssignment {
  const factory RoleAssignment({
    required int id,
    required int userId,
    required String role,
    required List<String> permissions,
    required bool canEditContent,
    required bool canDeleteContent,
    required bool canManageUsers,
    required bool canAccessAnalytics,
    required bool canAccessAdmin,
    required DateTime createdAt,
  }) = _RoleAssignment;

  factory RoleAssignment.fromJson(Map<String, dynamic> json) => _$RoleAssignmentFromJson(json);
}

@freezed
class ModerationItem with _$ModerationItem {
  const factory ModerationItem({
    required int id,
    required int contentId,
    required String contentType,
    required String status,
    String? reason,
    required List<String> flags,
    required double confidenceScore,
    int? assignedTo,
    int? reviewedBy,
    DateTime? reviewedAt,
    required DateTime createdAt,
  }) = _ModerationItem;

  factory ModerationItem.fromJson(Map<String, dynamic> json) => _$ModerationItemFromJson(json);
}

@freezed
class ComplianceCheckResult with _$ComplianceCheckResult {
  const factory ComplianceCheckResult({
    required bool isCompliant,
    required List<Map<String, dynamic>> violations,
    required int violationCount,
  }) = _ComplianceCheckResult;

  factory ComplianceCheckResult.fromJson(Map<String, dynamic> json) => _$ComplianceCheckResultFromJson(json);
}

@freezed
class RateLimitStatus with _$RateLimitStatus {
  const factory RateLimitStatus({
    required bool limited,
    int? minuteRemaining,
    int? hourRemaining,
    int? dayRemaining,
  }) = _RateLimitStatus;

  factory RateLimitStatus.fromJson(Map<String, dynamic> json) => _$RateLimitStatusFromJson(json);
}

@freezed
class NotificationPreference with _$NotificationPreference {
  const factory NotificationPreference({
    required int id,
    required int userId,
    required bool emailEnabled,
    required bool pushEnabled,
    required bool smsEnabled,
    required bool inAppEnabled,
    required String frequency,
    String? doNotDisturbStart,
    String? doNotDisturbEnd,
    required DateTime createdAt,
  }) = _NotificationPreference;

  factory NotificationPreference.fromJson(Map<String, dynamic> json) => _$NotificationPreferenceFromJson(json);
}

@freezed
class Notification with _$Notification {
  const factory Notification({
    required int id,
    required int userId,
    required String notificationType,
    required String title,
    required String message,
    required bool read,
    DateTime? readAt,
    String? actionUrl,
    String? source,
    required DateTime createdAt,
  }) = _Notification;

  factory Notification.fromJson(Map<String, dynamic> json) => _$NotificationFromJson(json);
}

@freezed
class AlertConfiguration with _$AlertConfiguration {
  const factory AlertConfiguration({
    required int id,
    required int userId,
    required String alertType,
    required String condition,
    double? threshold,
    required bool enabled,
    required List<String> notificationChannels,
    required DateTime createdAt,
  }) = _AlertConfiguration;

  factory AlertConfiguration.fromJson(Map<String, dynamic> json) => _$AlertConfigurationFromJson(json);
}

@freezed
class AdvancedReport with _$AdvancedReport {
  const factory AdvancedReport({
    required int id,
    required int userId,
    required String name,
    required String reportType,
    required String format,
    required String status,
    DateTime? generatedAt,
    DateTime? expiresAt,
    required DateTime createdAt,
  }) = _AdvancedReport;

  factory AdvancedReport.fromJson(Map<String, dynamic> json) => _$AdvancedReportFromJson(json);
}

@freezed
class ReportTemplate with _$ReportTemplate {
  const factory ReportTemplate({
    required int id,
    required String name,
    required String reportType,
    required List<String> sections,
    required String format,
    String? description,
    String? schedule,
    required DateTime createdAt,
  }) = _ReportTemplate;

  factory ReportTemplate.fromJson(Map<String, dynamic> json) => _$ReportTemplateFromJson(json);
}

@freezed
class ScheduledReport with _$ScheduledReport {
  const factory ScheduledReport({
    required int id,
    required int userId,
    required String name,
    required String cronExpression,
    required bool enabled,
    DateTime? lastRun,
    DateTime? nextRun,
    required List<String> recipientEmails,
    required DateTime createdAt,
  }) = _ScheduledReport;

  factory ScheduledReport.fromJson(Map<String, dynamic> json) => _$ScheduledReportFromJson(json);
}

@freezed
class ExportJob with _$ExportJob {
  const factory ExportJob({
    required int id,
    required int userId,
    required String exportType,
    required String format,
    required String status,
    required int progress,
    required int recordCount,
    DateTime? startedAt,
    DateTime? completedAt,
    required DateTime createdAt,
  }) = _ExportJob;

  factory ExportJob.fromJson(Map<String, dynamic> json) => _$ExportJobFromJson(json);
}

@freezed
class SecurityStats with _$SecurityStats {
  const factory SecurityStats({
    required int totalAuditLogs,
    required int moderationItemsPending,
    required int recentThrottles,
    required int unreadNotifications,
    required int activeAlerts,
  }) = _SecurityStats;

  factory SecurityStats.fromJson(Map<String, dynamic> json) => _$SecurityStatsFromJson(json);
}
