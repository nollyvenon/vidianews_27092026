import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/advanced_platform_providers.dart';

class PerformanceScreen extends ConsumerWidget {
  const PerformanceScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cacheMetrics = ref.watch(cacheMetricsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Performance & Caching'),
        elevation: 0,
      ),
      body: cacheMetrics.when(
        data: (metrics) => _buildMetricsView(context, metrics),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }

  Widget _buildMetricsView(BuildContext context, dynamic metrics) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Cache Statistics',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          _buildMetricCard(
            'Total Requests',
            metrics.totalRequests.toString(),
            Colors.blue,
          ),
          _buildMetricCard(
            'Cache Hit Rate',
            '${((metrics.totalHits / (metrics.totalRequests + 1)) * 100).toStringAsFixed(1)}%',
            Colors.green,
          ),
          _buildMetricCard(
            'Avg Response Time',
            '${metrics.averageResponseTimeMs.toStringAsFixed(2)}ms',
            Colors.orange,
          ),
          _buildMetricCard(
            'Memory Usage',
            '${metrics.memoryUsageMb.toStringAsFixed(2)}MB',
            Colors.red,
          ),
          const SizedBox(height: 24),
          Text(
            'Cache Strategies',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          _buildStrategyTile('LRU (Least Recently Used)', 'Removes least accessed entries'),
          _buildStrategyTile('LFU (Least Frequently Used)', 'Removes least used entries'),
          _buildStrategyTile('TTL (Time To Live)', 'Removes expired entries'),
          _buildStrategyTile('FIFO (First In First Out)', 'Removes oldest entries'),
        ],
      ),
    );
  }

  Widget _buildMetricCard(String label, String value, Color color) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              width: 60,
              height: 60,
              decoration: BoxDecoration(
                color: color.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Center(
                child: Text(
                  value.substring(0, (value.length / 2).toInt()),
                  style: TextStyle(color: color, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            const SizedBox(width: 16),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: const TextStyle(fontSize: 12)),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStrategyTile(String title, String description) {
    return ListTile(
      title: Text(title),
      subtitle: Text(description),
      leading: const Icon(Icons.storage),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }
}
