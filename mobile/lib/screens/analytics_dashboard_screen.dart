// Analytics dashboard: headline figures for the last 30 days, with daily engagement and revenue.

import 'package:flutter/material.dart';
import '../services/analytics_overview_service.dart';
import '../services/authenticated_dio.dart';
import '../widgets/async_view.dart';

const int _windowDays = 30;

class AnalyticsDashboardScreen extends StatefulWidget {
  final AnalyticsOverviewService? service;

  const AnalyticsDashboardScreen({Key? key, this.service}) : super(key: key);

  @override
  State<AnalyticsDashboardScreen> createState() => _AnalyticsDashboardScreenState();
}

class _AnalyticsDashboardScreenState extends State<AnalyticsDashboardScreen> {
  late final AnalyticsOverviewService _service = widget.service ?? AnalyticsOverviewService(createAuthenticatedDio());
  late Future<_DashboardData> _data = _load();

  Future<_DashboardData> _load() async {
    final summary = await _service.fetchSummary(days: _windowDays);
    final engagement = await _service.fetchEngagement(days: _windowDays);
    final revenue = await _service.fetchRevenue(days: _windowDays);
    return _DashboardData(summary: summary, engagement: engagement, revenue: revenue);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analytics')),
      body: AsyncView<_DashboardData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text('Last $_windowDays days', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              children: [
                _figure('${data.summary.views}', 'Views'),
                _figure(data.summary.watchHours.toStringAsFixed(1), 'Watch hours'),
                _figure('${data.summary.subscribers}', 'Subscribers'),
                _figure(
                  '\$${data.revenue.fold<double>(0, (total, row) => total + row.totalRevenue).toStringAsFixed(2)}',
                  'Revenue',
                ),
              ],
            ),
            const SizedBox(height: 24),
            Text('Engagement by day', style: Theme.of(context).textTheme.titleMedium),
            if (data.engagement.isEmpty) const Text('No engagement recorded yet.'),
            for (final row in data.engagement)
              ListTile(
                contentPadding: EdgeInsets.zero,
                title: Text(row.date),
                subtitle: Text('${row.activeUsers} active · ${row.newUsers} new'),
              ),
            const SizedBox(height: 24),
            Text('Revenue by day', style: Theme.of(context).textTheme.titleMedium),
            if (data.revenue.isEmpty) const Text('No revenue recorded yet.'),
            for (final row in data.revenue)
              ListTile(
                contentPadding: EdgeInsets.zero,
                title: Text(row.date),
                subtitle: Text('${row.transactionCount} transactions'),
                trailing: Text('\$${row.totalRevenue.toStringAsFixed(2)}'),
              ),
          ],
        ),
      ),
    );
  }

  Widget _figure(String value, String label) {
    return Card(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(value, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(label),
          ],
        ),
      ),
    );
  }
}

class _DashboardData {
  final AnalyticsSummary summary;
  final List<EngagementRow> engagement;
  final List<RevenueRow> revenue;

  const _DashboardData({required this.summary, required this.engagement, required this.revenue});
}
