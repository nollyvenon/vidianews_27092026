// Admin audit log entries from GET /admin/audit-logs.

class AuditEntry {
  final int id;
  final int adminId;
  final String action;
  final String resourceType;
  final Map<String, dynamic> changes;
  final DateTime timestamp;

  const AuditEntry({
    required this.id,
    required this.adminId,
    required this.action,
    required this.resourceType,
    required this.changes,
    required this.timestamp,
  });

  factory AuditEntry.fromJson(Map<String, dynamic> json) => AuditEntry(
        id: json['id'] as int,
        adminId: json['admin_id'] as int,
        action: json['action'] as String,
        resourceType: json['resource_type'] as String,
        changes: (json['changes'] as Map<String, dynamic>?) ?? const {},
        timestamp: DateTime.parse(json['timestamp'] as String),
      );
}
