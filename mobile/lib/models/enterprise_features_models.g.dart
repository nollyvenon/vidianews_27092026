// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'enterprise_features_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$AuditLogImpl _$$AuditLogImplFromJson(Map<String, dynamic> json) =>
    _$AuditLogImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      action: json['action'] as String,
      resourceType: json['resource_type'] as String?,
      resourceId: (json['resource_id'] as num?)?.toInt(),
      status: json['status'] as String?,
      ipAddress: json['ip_address'] as String?,
      severity: json['severity'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$AuditLogImplToJson(_$AuditLogImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'action': instance.action,
      'resource_type': instance.resourceType,
      'resource_id': instance.resourceId,
      'status': instance.status,
      'ip_address': instance.ipAddress,
      'severity': instance.severity,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$AccessControlImpl _$$AccessControlImplFromJson(Map<String, dynamic> json) =>
    _$AccessControlImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      resourceType: json['resource_type'] as String,
      resourceId: (json['resource_id'] as num).toInt(),
      accessLevel: json['access_level'] as String,
      permissions: (json['permissions'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      grantedBy: (json['granted_by'] as num?)?.toInt(),
      grantedAt: DateTime.parse(json['granted_at'] as String),
      expiresAt: json['expires_at'] == null
          ? null
          : DateTime.parse(json['expires_at'] as String),
    );

Map<String, dynamic> _$$AccessControlImplToJson(_$AccessControlImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'resource_type': instance.resourceType,
      'resource_id': instance.resourceId,
      'access_level': instance.accessLevel,
      'permissions': instance.permissions,
      'granted_by': instance.grantedBy,
      'granted_at': instance.grantedAt.toIso8601String(),
      'expires_at': instance.expiresAt?.toIso8601String(),
    };

_$RoleAssignmentImpl _$$RoleAssignmentImplFromJson(Map<String, dynamic> json) =>
    _$RoleAssignmentImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      role: json['role'] as String,
      permissions: (json['permissions'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      canEditContent: json['can_edit_content'] as bool,
      canDeleteContent: json['can_delete_content'] as bool,
      canManageUsers: json['can_manage_users'] as bool,
      canAccessAnalytics: json['can_access_analytics'] as bool,
      canAccessAdmin: json['can_access_admin'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$RoleAssignmentImplToJson(
        _$RoleAssignmentImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'role': instance.role,
      'permissions': instance.permissions,
      'can_edit_content': instance.canEditContent,
      'can_delete_content': instance.canDeleteContent,
      'can_manage_users': instance.canManageUsers,
      'can_access_analytics': instance.canAccessAnalytics,
      'can_access_admin': instance.canAccessAdmin,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$ModerationItemImpl _$$ModerationItemImplFromJson(Map<String, dynamic> json) =>
    _$ModerationItemImpl(
      id: (json['id'] as num).toInt(),
      contentId: (json['content_id'] as num).toInt(),
      contentType: json['content_type'] as String,
      status: json['status'] as String,
      reason: json['reason'] as String?,
      flags: (json['flags'] as List<dynamic>).map((e) => e as String).toList(),
      confidenceScore: (json['confidence_score'] as num).toDouble(),
      assignedTo: (json['assigned_to'] as num?)?.toInt(),
      reviewedBy: (json['reviewed_by'] as num?)?.toInt(),
      reviewedAt: json['reviewed_at'] == null
          ? null
          : DateTime.parse(json['reviewed_at'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$ModerationItemImplToJson(
        _$ModerationItemImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'content_id': instance.contentId,
      'content_type': instance.contentType,
      'status': instance.status,
      'reason': instance.reason,
      'flags': instance.flags,
      'confidence_score': instance.confidenceScore,
      'assigned_to': instance.assignedTo,
      'reviewed_by': instance.reviewedBy,
      'reviewed_at': instance.reviewedAt?.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$ComplianceCheckResultImpl _$$ComplianceCheckResultImplFromJson(
        Map<String, dynamic> json) =>
    _$ComplianceCheckResultImpl(
      isCompliant: json['is_compliant'] as bool,
      violations: (json['violations'] as List<dynamic>)
          .map((e) => e as Map<String, dynamic>)
          .toList(),
      violationCount: (json['violation_count'] as num).toInt(),
    );

Map<String, dynamic> _$$ComplianceCheckResultImplToJson(
        _$ComplianceCheckResultImpl instance) =>
    <String, dynamic>{
      'is_compliant': instance.isCompliant,
      'violations': instance.violations,
      'violation_count': instance.violationCount,
    };

_$RateLimitStatusImpl _$$RateLimitStatusImplFromJson(
        Map<String, dynamic> json) =>
    _$RateLimitStatusImpl(
      limited: json['limited'] as bool,
      minuteRemaining: (json['minute_remaining'] as num?)?.toInt(),
      hourRemaining: (json['hour_remaining'] as num?)?.toInt(),
      dayRemaining: (json['day_remaining'] as num?)?.toInt(),
    );

Map<String, dynamic> _$$RateLimitStatusImplToJson(
        _$RateLimitStatusImpl instance) =>
    <String, dynamic>{
      'limited': instance.limited,
      'minute_remaining': instance.minuteRemaining,
      'hour_remaining': instance.hourRemaining,
      'day_remaining': instance.dayRemaining,
    };

_$NotificationPreferenceImpl _$$NotificationPreferenceImplFromJson(
        Map<String, dynamic> json) =>
    _$NotificationPreferenceImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      emailEnabled: json['email_enabled'] as bool,
      pushEnabled: json['push_enabled'] as bool,
      smsEnabled: json['sms_enabled'] as bool,
      inAppEnabled: json['in_app_enabled'] as bool,
      frequency: json['frequency'] as String,
      doNotDisturbStart: json['do_not_disturb_start'] as String?,
      doNotDisturbEnd: json['do_not_disturb_end'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$NotificationPreferenceImplToJson(
        _$NotificationPreferenceImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'email_enabled': instance.emailEnabled,
      'push_enabled': instance.pushEnabled,
      'sms_enabled': instance.smsEnabled,
      'in_app_enabled': instance.inAppEnabled,
      'frequency': instance.frequency,
      'do_not_disturb_start': instance.doNotDisturbStart,
      'do_not_disturb_end': instance.doNotDisturbEnd,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$NotificationImpl _$$NotificationImplFromJson(Map<String, dynamic> json) =>
    _$NotificationImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      notificationType: json['notification_type'] as String,
      title: json['title'] as String,
      message: json['message'] as String,
      read: json['read'] as bool,
      readAt: json['read_at'] == null
          ? null
          : DateTime.parse(json['read_at'] as String),
      actionUrl: json['action_url'] as String?,
      source: json['source'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$NotificationImplToJson(_$NotificationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'notification_type': instance.notificationType,
      'title': instance.title,
      'message': instance.message,
      'read': instance.read,
      'read_at': instance.readAt?.toIso8601String(),
      'action_url': instance.actionUrl,
      'source': instance.source,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$AlertConfigurationImpl _$$AlertConfigurationImplFromJson(
        Map<String, dynamic> json) =>
    _$AlertConfigurationImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      alertType: json['alert_type'] as String,
      condition: json['condition'] as String,
      threshold: (json['threshold'] as num?)?.toDouble(),
      enabled: json['enabled'] as bool,
      notificationChannels: (json['notification_channels'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$AlertConfigurationImplToJson(
        _$AlertConfigurationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'alert_type': instance.alertType,
      'condition': instance.condition,
      'threshold': instance.threshold,
      'enabled': instance.enabled,
      'notification_channels': instance.notificationChannels,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$AdvancedReportImpl _$$AdvancedReportImplFromJson(Map<String, dynamic> json) =>
    _$AdvancedReportImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      name: json['name'] as String,
      reportType: json['report_type'] as String,
      format: json['format'] as String,
      status: json['status'] as String,
      generatedAt: json['generated_at'] == null
          ? null
          : DateTime.parse(json['generated_at'] as String),
      expiresAt: json['expires_at'] == null
          ? null
          : DateTime.parse(json['expires_at'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$AdvancedReportImplToJson(
        _$AdvancedReportImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'name': instance.name,
      'report_type': instance.reportType,
      'format': instance.format,
      'status': instance.status,
      'generated_at': instance.generatedAt?.toIso8601String(),
      'expires_at': instance.expiresAt?.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$ReportTemplateImpl _$$ReportTemplateImplFromJson(Map<String, dynamic> json) =>
    _$ReportTemplateImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      reportType: json['report_type'] as String,
      sections:
          (json['sections'] as List<dynamic>).map((e) => e as String).toList(),
      format: json['format'] as String,
      description: json['description'] as String?,
      schedule: json['schedule'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$ReportTemplateImplToJson(
        _$ReportTemplateImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'report_type': instance.reportType,
      'sections': instance.sections,
      'format': instance.format,
      'description': instance.description,
      'schedule': instance.schedule,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$ScheduledReportImpl _$$ScheduledReportImplFromJson(
        Map<String, dynamic> json) =>
    _$ScheduledReportImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      name: json['name'] as String,
      cronExpression: json['cron_expression'] as String,
      enabled: json['enabled'] as bool,
      lastRun: json['last_run'] == null
          ? null
          : DateTime.parse(json['last_run'] as String),
      nextRun: json['next_run'] == null
          ? null
          : DateTime.parse(json['next_run'] as String),
      recipientEmails: (json['recipient_emails'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$ScheduledReportImplToJson(
        _$ScheduledReportImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'name': instance.name,
      'cron_expression': instance.cronExpression,
      'enabled': instance.enabled,
      'last_run': instance.lastRun?.toIso8601String(),
      'next_run': instance.nextRun?.toIso8601String(),
      'recipient_emails': instance.recipientEmails,
      'created_at': instance.createdAt.toIso8601String(),
    };

_$ExportJobImpl _$$ExportJobImplFromJson(Map<String, dynamic> json) =>
    _$ExportJobImpl(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      exportType: json['export_type'] as String,
      format: json['format'] as String,
      status: json['status'] as String,
      progress: (json['progress'] as num).toInt(),
      recordCount: (json['record_count'] as num).toInt(),
      startedAt: json['started_at'] == null
          ? null
          : DateTime.parse(json['started_at'] as String),
      completedAt: json['completed_at'] == null
          ? null
          : DateTime.parse(json['completed_at'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$$ExportJobImplToJson(_$ExportJobImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'export_type': instance.exportType,
      'format': instance.format,
      'status': instance.status,
      'progress': instance.progress,
      'record_count': instance.recordCount,
      'started_at': instance.startedAt?.toIso8601String(),
      'completed_at': instance.completedAt?.toIso8601String(),
      'created_at': instance.createdAt.toIso8601String(),
    };

_$SecurityStatsImpl _$$SecurityStatsImplFromJson(Map<String, dynamic> json) =>
    _$SecurityStatsImpl(
      totalAuditLogs: (json['total_audit_logs'] as num).toInt(),
      moderationItemsPending: (json['moderation_items_pending'] as num).toInt(),
      recentThrottles: (json['recent_throttles'] as num).toInt(),
      unreadNotifications: (json['unread_notifications'] as num).toInt(),
      activeAlerts: (json['active_alerts'] as num).toInt(),
    );

Map<String, dynamic> _$$SecurityStatsImplToJson(_$SecurityStatsImpl instance) =>
    <String, dynamic>{
      'total_audit_logs': instance.totalAuditLogs,
      'moderation_items_pending': instance.moderationItemsPending,
      'recent_throttles': instance.recentThrottles,
      'unread_notifications': instance.unreadNotifications,
      'active_alerts': instance.activeAlerts,
    };
