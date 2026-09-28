import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/enterprise_features_models.dart';
import '../../providers/enterprise_features_providers.dart';

class SecurityScreen extends ConsumerWidget {
  final int userId;

  const SecurityScreen({
    Key? key,
    required this.userId,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auditLogs = ref.watch(auditLogsProvider(userId));
    final userRole = ref.watch(userRoleProvider(userId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Security & Access Control'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            userRole.when(
              data: (role) => _buildRoleCard(role),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, stack) => ErrorWidget(error: err.toString()),
            ),
            const SizedBox(height: 24),
            Text(
              'Recent Activity',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            auditLogs.when(
              data: (logs) => _buildAuditLogsList(logs),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, stack) => ErrorWidget(error: err.toString()),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRoleCard(RoleAssignment role) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Role: ${role.role}',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                if (role.canEditContent)
                  const Chip(label: Text('Edit Content')),
                if (role.canDeleteContent)
                  const Chip(label: Text('Delete Content')),
                if (role.canManageUsers)
                  const Chip(label: Text('Manage Users')),
                if (role.canAccessAnalytics)
                  const Chip(label: Text('View Analytics')),
                if (role.canAccessAdmin)
                  const Chip(label: Text('Admin Access')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAuditLogsList(List<AuditLog> logs) {
    return Column(
      children: logs.take(10).map((log) {
        return ListTile(
          title: Text(log.action),
          subtitle: Text(log.resourceType ?? 'System'),
          trailing: Chip(
            label: Text(log.severity ?? 'info'),
            backgroundColor: _getSeverityColor(log.severity),
          ),
          dense: true,
        );
      }).toList(),
    );
  }

  Color _getSeverityColor(String? severity) {
    switch (severity) {
      case 'high':
        return Colors.red.shade200;
      case 'medium':
        return Colors.orange.shade200;
      default:
        return Colors.green.shade200;
    }
  }
}

final userRoleProvider = FutureProvider.family<RoleAssignment, int>(
  (ref, userId) async {
    final service = ref.watch(enterpriseServiceProvider);
    return service.getUserRole(userId);
  },
);
