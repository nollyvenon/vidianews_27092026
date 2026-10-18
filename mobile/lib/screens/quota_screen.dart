// Usage & quotas for the signed-in account, from GET /quota/usage.

import 'package:flutter/material.dart';
import '../models/quota_models.dart';
import '../services/authenticated_dio.dart';
import '../services/quota_service.dart';

class QuotaScreen extends StatefulWidget {
  final QuotaService? service;

  const QuotaScreen({Key? key, this.service}) : super(key: key);

  @override
  State<QuotaScreen> createState() => _QuotaScreenState();
}

class _QuotaScreenState extends State<QuotaScreen> {
  late final QuotaService _service = widget.service ?? QuotaService(createAuthenticatedDio());
  late Future<QuotaUsage> _usage = _service.fetchUsage();

  void _reload() {
    setState(() {
      _usage = _service.fetchUsage();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Usage & Quotas')),
      body: FutureBuilder<QuotaUsage>(
        future: _usage,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(messageFromError(snapshot.error!), textAlign: TextAlign.center),
                    const SizedBox(height: 12),
                    OutlinedButton(onPressed: _reload, child: const Text('Try again')),
                  ],
                ),
              ),
            );
          }
          final usage = snapshot.data!;
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _UsageCard(
                title: 'API calls this month',
                valueLabel: '${usage.apiCalls} / ${usage.apiCallLimit}',
                ratio: usage.apiCallRatio,
                color: Colors.blue,
              ),
              const SizedBox(height: 12),
              _FactCard(title: 'Stored media', value: '${usage.storageGb.toStringAsFixed(2)} GB'),
              const SizedBox(height: 12),
              _FactCard(title: 'Bandwidth used', value: '${usage.bandwidthGb.toStringAsFixed(2)} GB'),
            ],
          );
        },
      ),
    );
  }
}

class _UsageCard extends StatelessWidget {
  final String title;
  final String valueLabel;
  final double ratio;
  final Color color;

  const _UsageCard({required this.title, required this.valueLabel, required this.ratio, required this.color});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(valueLabel),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: ratio,
                minHeight: 8,
                backgroundColor: Colors.grey.shade300,
                valueColor: AlwaysStoppedAnimation(color),
              ),
            ),
            const SizedBox(height: 4),
            Text('${(ratio * 100).round()}% used', style: const TextStyle(fontSize: 12, color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}

class _FactCard extends StatelessWidget {
  final String title;
  final String value;

  const _FactCard({required this.title, required this.value});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(title),
        trailing: Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
      ),
    );
  }
}
