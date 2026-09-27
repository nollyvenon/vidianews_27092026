import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/platform_completion_providers.dart';


class AdminDashboardScreen extends ConsumerWidget {
  final int userId;

  const AdminDashboardScreen({Key? key, required this.userId}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Admin Dashboard'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSummaryCard(context, ref),
            const SizedBox(height: 24),
            _buildStatisticsSection(context, ref),
            const SizedBox(height: 24),
            _buildAdminActionsSection(context, ref),
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryCard(BuildContext context, WidgetRef ref) {
    final summary = ref.watch(dashboardSummaryProvider);

    return summary.when(
      data: (data) {
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Platform Summary',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 16),
                _buildSummaryRow('Total Interactions', data['total_interactions'].toString()),
                _buildSummaryRow('Total Follows', data['total_follows'].toString()),
                _buildSummaryRow('Total Comments', data['total_comments'].toString()),
                _buildSummaryRow('Total Messages', data['total_messages'].toString()),
                _buildSummaryRow('Total Notifications', data['total_notifications'].toString()),
              ],
            ),
          ),
        );
      },
      loading: () => const Card(
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: CircularProgressIndicator(),
        ),
      ),
      error: (err, stack) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text('Error loading summary: $err'),
        ),
      ),
    );
  }

  Widget _buildSummaryRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          ),
        ],
      ),
    );
  }

  Widget _buildStatisticsSection(BuildContext context, WidgetRef ref) {
    final stats = ref.watch(
      platformStatisticsProvider({
        'days': 7,
        'limit': 100,
      }),
    );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Platform Statistics (Last 7 Days)',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 16),
        stats.when(
          data: (data) {
            if (data.isEmpty) {
              return const Card(
                child: Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Text('No statistics available'),
                ),
              );
            }

            return Column(
              children: [
                ...data.take(5).map((stat) {
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    child: ListTile(
                      title: Text(stat.metricName),
                      subtitle: Text('${stat.metricType} • ${stat.createdAt}'),
                      trailing: Text(
                        stat.metricValue.toStringAsFixed(2),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  );
                }).toList(),
              ],
            );
          },
          loading: () => const Card(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: CircularProgressIndicator(),
            ),
          ),
          error: (err, stack) => Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text('Error: $err'),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAdminActionsSection(BuildContext context, WidgetRef ref) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Admin Actions',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.person_add),
                  title: const Text('Manage Users'),
                  trailing: const Icon(Icons.arrow_forward),
                  onTap: () {
                    // Navigate to user management
                  },
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.block),
                  title: const Text('Moderation Queue'),
                  trailing: const Icon(Icons.arrow_forward),
                  onTap: () {
                    // Navigate to moderation
                  },
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.history),
                  title: const Text('Audit Logs'),
                  trailing: const Icon(Icons.arrow_forward),
                  onTap: () {
                    // Navigate to audit logs
                  },
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.settings),
                  title: const Text('System Configuration'),
                  trailing: const Icon(Icons.arrow_forward),
                  onTap: () {
                    // Navigate to system config
                  },
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
