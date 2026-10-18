// Headline analytics for the last 30 days: views, watch hours and subscribers.

import 'package:flutter/material.dart';
import '../services/analytics_overview_service.dart';
import '../services/authenticated_dio.dart';
import '../widgets/async_view.dart';

class AnalyticsScreen extends StatefulWidget {
  final AnalyticsOverviewService? service;

  const AnalyticsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  late final AnalyticsOverviewService _service = widget.service ?? AnalyticsOverviewService(createAuthenticatedDio());
  late Future<AnalyticsSummary> _summary = _service.fetchSummary();

  void _reload() {
    setState(() {
      _summary = _service.fetchSummary();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analytics Summary')),
      body: AsyncView<AnalyticsSummary>(
        future: _summary,
        onRetry: _reload,
        builder: (context, summary) => GridView.count(
          crossAxisCount: 3,
          padding: const EdgeInsets.all(16),
          mainAxisSpacing: 12,
          crossAxisSpacing: 12,
          children: [
            _figure('${summary.views}', 'Views'),
            _figure(summary.watchHours.toStringAsFixed(1), 'Watch hours'),
            _figure('${summary.subscribers}', 'Subscribers'),
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
            Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontSize: 11)),
          ],
        ),
      ),
    );
  }
}
