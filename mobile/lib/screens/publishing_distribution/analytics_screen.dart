import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/publishing_distribution_providers.dart';

class AnalyticsScreen extends ConsumerStatefulWidget {
  const AnalyticsScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends ConsumerState<AnalyticsScreen> {
  int _selectedContentId = 1;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadMetrics();
    });
  }

  Future<void> _loadMetrics() async {
    try {
      final service = ref.read(publishingServiceProvider);
      final metrics = await service.getEngagementMetrics(_selectedContentId);
      ref.read(analyticsDataProvider.notifier).state = metrics;
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading metrics: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final analytics = ref.watch(analyticsDataProvider);

    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Metrics Cards
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 1.2,
              children: [
                _buildMetricCard(
                  'Views',
                  '${analytics['views'] ?? 0}',
                  Icons.visibility,
                ),
                _buildMetricCard(
                  'Clicks',
                  '${analytics['clicks'] ?? 0}',
                  Icons.touch_app,
                ),
                _buildMetricCard(
                  'Shares',
                  '${analytics['shares'] ?? 0}',
                  Icons.share,
                ),
                _buildMetricCard(
                  'CTR',
                  '${analytics['ctr'] != null ? (analytics['ctr'] as num).toStringAsFixed(1) : '0'}%',
                  Icons.trending_up,
                ),
              ],
            ),
            const SizedBox(height: 24),
            // Performance Trends
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Performance Trends',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    _buildMetricRow('Total Views', analytics['views'] ?? 0, 100),
                    const SizedBox(height: 12),
                    _buildMetricRow(
                      'Engagement Rate',
                      analytics['engagement_rate'] ?? 0,
                      100,
                    ),
                    const SizedBox(height: 12),
                    _buildMetricRow('Share Rate', analytics['share_rate'] ?? 0, 100),
                    const SizedBox(height: 12),
                    _buildMetricRow(
                      'Conversion Rate',
                      analytics['conversion_rate'] ?? 0,
                      100,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            // Top Performing Content
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Engagement Score',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Center(
                      child: Column(
                        children: [
                          Text(
                            '${analytics['engagement_score'] != null ? (analytics['engagement_score'] as num).toStringAsFixed(1) : '0'}%',
                            style: const TextStyle(
                              fontSize: 48,
                              fontWeight: FontWeight.bold,
                              color: Colors.blue,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 12,
                              vertical: 6,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.green[100],
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: const Text(
                              'Up 12%',
                              style: TextStyle(
                                color: Colors.green,
                                fontWeight: FontWeight.w600,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            Center(
              child: ElevatedButton(
                onPressed: _loadMetrics,
                child: const Text('Refresh Metrics'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricCard(String label, String value, IconData icon) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: Colors.blue, size: 24),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricRow(String label, dynamic value, int maxValue) {
    final numValue = (value is num ? value : 0).toDouble();
    final percentage = (numValue / maxValue * 100).clamp(0, 100);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(fontSize: 12)),
            Text(
              '${percentage.toStringAsFixed(1)}%',
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: percentage / 100,
            minHeight: 8,
            backgroundColor: Colors.grey[300],
            valueColor: AlwaysStoppedAnimation<Color>(
              percentage > 70 ? Colors.green : Colors.orange,
            ),
          ),
        ),
      ],
    );
  }
}
