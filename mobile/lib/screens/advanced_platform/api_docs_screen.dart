// API usage: how often each endpoint is called, how often it fails and how long it takes.

import 'package:flutter/material.dart';
import '../../models/platform_ops_models.dart';
import '../../services/authenticated_dio.dart';
import '../../services/platform_ops_service.dart';
import '../../widgets/async_view.dart';

class APIDocsScreen extends StatefulWidget {
  final PlatformOpsService? service;

  const APIDocsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<APIDocsScreen> createState() => _APIDocsScreenState();
}

class _APIDocsScreenState extends State<APIDocsScreen> {
  late final PlatformOpsService _service = widget.service ?? PlatformOpsService(createAuthenticatedDio());
  late Future<List<ApiUsage>> _usage = _service.fetchApiUsage();

  void _reload() {
    setState(() {
      _usage = _service.fetchApiUsage();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('API Usage')),
      body: AsyncView<List<ApiUsage>>(
        future: _usage,
        onRetry: _reload,
        builder: (context, rows) {
          if (rows.isEmpty) {
            return const Center(child: Text('No API calls have been measured yet.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: rows.length,
            itemBuilder: (context, index) {
              final row = rows[index];
              return Card(
                child: ListTile(
                  key: Key('usage-${row.id}'),
                  title: Text('${row.method} ${row.endpoint}'),
                  subtitle: Text(
                    '${row.callCount} calls · ${(row.errorRate * 100).toStringAsFixed(1)}% errors · '
                    '${row.averageResponseTimeMs.toStringAsFixed(0)} ms average',
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
