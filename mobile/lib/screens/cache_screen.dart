// Cache performance and the cache policy for each resource, read from the platform's cache statistics.

import 'package:flutter/material.dart';
import '../models/platform_ops_models.dart';
import '../services/authenticated_dio.dart';
import '../services/platform_ops_service.dart';
import '../widgets/async_view.dart';

class CacheScreen extends StatefulWidget {
  final PlatformOpsService? service;

  const CacheScreen({Key? key, this.service}) : super(key: key);

  @override
  State<CacheScreen> createState() => _CacheScreenState();
}

class _CacheScreenState extends State<CacheScreen> {
  late final PlatformOpsService _service = widget.service ?? PlatformOpsService(createAuthenticatedDio());
  late Future<_CacheData> _data = _load();

  Future<_CacheData> _load() async {
    final stats = await _service.fetchCacheStats();
    final policies = await _service.fetchCachePolicies();
    return _CacheData(stats: stats, policies: policies);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Cache Configuration')),
      body: AsyncView<_CacheData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const Text('Performance', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Row(
              children: [
                _metric('${data.stats.totalEntries}', 'Entries'),
                _metric('${(data.stats.hitRate * 100).toStringAsFixed(1)}%', 'Hit rate', color: Colors.green),
                _metric('${data.stats.totalHits}', 'Hits'),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Hot ${data.stats.hotEntries} · Warm ${data.stats.warmEntries} · Cold ${data.stats.coldEntries}',
              style: const TextStyle(color: Colors.black54),
            ),
            const SizedBox(height: 24),
            const Text('Cache Policies', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            if (data.policies.isEmpty)
              const Text('No cache policies are configured.'),
            for (final policy in data.policies)
              Card(
                child: ListTile(
                  key: Key('policy-${policy.resourceType}'),
                  title: Text(policy.resourceType),
                  subtitle: Text(
                    '${policy.cacheType} · ${policy.ttlSeconds}s TTL · ${policy.maxSizeMb} MB'
                    '${policy.isActive ? '' : ' · inactive'}',
                  ),
                  trailing: Text(
                    '${(policy.hitRate * 100).toStringAsFixed(1)}%',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _metric(String value, String label, {Color? color}) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            children: [
              Text(value, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
              const SizedBox(height: 4),
              Text(label, style: const TextStyle(fontSize: 12)),
            ],
          ),
        ),
      ),
    );
  }
}

class _CacheData {
  final CacheStats stats;
  final List<CachePolicy> policies;

  const _CacheData({required this.stats, required this.policies});
}
