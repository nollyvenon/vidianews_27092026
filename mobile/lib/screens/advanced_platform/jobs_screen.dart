import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/advanced_platform_models.dart';
import '../../providers/advanced_platform_providers.dart';

class JobsScreen extends ConsumerWidget {
  const JobsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pendingJobs = ref.watch(pendingJobsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Background Jobs'),
        elevation: 0,
      ),
      body: pendingJobs.when(
        data: (jobs) => _buildJobsList(context, jobs),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showCreateJobDialog(context),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildJobsList(BuildContext context, List<BackgroundJob> jobs) {
    if (jobs.isEmpty) {
      return const Center(child: Text('No pending jobs'));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: jobs.length,
      itemBuilder: (context, index) {
        final job = jobs[index];
        return _buildJobCard(job);
      },
    );
  }

  Widget _buildJobCard(BackgroundJob job) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: ListTile(
        title: Text(job.jobType),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Priority: ${job.priority}'),
            Text('Retries: ${job.retryCount}'),
          ],
        ),
        trailing: Chip(
          label: Text(job.status),
          backgroundColor: _getStatusColor(job.status),
        ),
      ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'completed':
        return Colors.green.shade200;
      case 'running':
        return Colors.blue.shade200;
      case 'failed':
        return Colors.red.shade200;
      default:
        return Colors.orange.shade200;
    }
  }

  void _showCreateJobDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Create Job'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const TextField(
              decoration: InputDecoration(labelText: 'Job Type'),
            ),
            const SizedBox(height: 12),
            Slider(
              value: 0,
              min: 0,
              max: 10,
              onChanged: (_) {},
              label: 'Priority',
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
