import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/enterprise_features_models.dart';
import '../../providers/enterprise_features_providers.dart';

class ReportsScreen extends ConsumerWidget {
  final int userId;

  const ReportsScreen({
    Key? key,
    required this.userId,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final reports = ref.watch(userReportsProvider(userId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Reports & Exports'),
        elevation: 0,
      ),
      body: reports.when(
        data: (items) => _buildReportsList(context, items),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showCreateReportDialog(context),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildReportsList(BuildContext context, List<AdvancedReport> items) {
    if (items.isEmpty) {
      return const Center(child: Text('No reports generated yet'));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: items.length,
      itemBuilder: (context, index) {
        final report = items[index];
        return _buildReportCard(report);
      },
    );
  }

  Widget _buildReportCard(AdvancedReport report) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: ListTile(
        leading: _getReportIcon(report.reportType),
        title: Text(report.name),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Type: ${report.reportType}'),
            Text('Status: ${report.status}'),
            if (report.generatedAt != null)
              Text('Generated: ${report.generatedAt}'),
          ],
        ),
        trailing: PopupMenuButton(
          itemBuilder: (context) => [
            const PopupMenuItem(
              child: Text('Download'),
            ),
            const PopupMenuItem(
              child: Text('Share'),
            ),
            const PopupMenuItem(
              child: Text('Delete'),
            ),
          ],
        ),
      ),
    );
  }

  Icon _getReportIcon(String type) {
    switch (type) {
      case 'analytics':
        return const Icon(Icons.analytics);
      case 'performance':
        return const Icon(Icons.speed);
      case 'compliance':
        return const Icon(Icons.verified);
      default:
        return const Icon(Icons.description);
    }
  }

  void _showCreateReportDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Create Report'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: const InputDecoration(labelText: 'Report Name'),
            ),
            const SizedBox(height: 12),
            DropdownButton<String>(
              isExpanded: true,
              hint: const Text('Select Type'),
              items: ['analytics', 'performance', 'compliance']
                  .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                  .toList(),
              onChanged: (_) {},
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }
}
