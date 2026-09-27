import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/enterprise_features_models.dart';
import '../../providers/enterprise_features_providers.dart';

class ModerationScreen extends ConsumerWidget {
  const ModerationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pendingItems = ref.watch(pendingModerationProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Content Moderation'),
        elevation: 0,
      ),
      body: pendingItems.when(
        data: (items) => _buildModerationList(context, items),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(
          child: Text('Error: $err'),
        ),
      ),
    );
  }

  Widget _buildModerationList(BuildContext context, List<ModerationItem> items) {
    if (items.isEmpty) {
      return const Center(
        child: Text('No pending items for moderation'),
      );
    }

    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        return _buildModerationCard(context, item);
      },
    );
  }

  Widget _buildModerationCard(BuildContext context, ModerationItem item) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: ExpansionTile(
        title: Text('Content ID: ${item.contentId}'),
        subtitle: Text(item.contentType),
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Status: ${item.status}',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text('Reason: ${item.reason ?? "N/A"}'),
                const SizedBox(height: 8),
                Text('Confidence: ${(item.confidenceScore * 100).toStringAsFixed(1)}%'),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  children: item.flags.map((flag) {
                    return Chip(label: Text(flag));
                  }).toList(),
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.check),
                      label: const Text('Approve'),
                    ),
                    ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.close),
                      label: const Text('Reject'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
