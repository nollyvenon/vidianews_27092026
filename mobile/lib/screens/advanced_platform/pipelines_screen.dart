// Data pipelines and their latest runs. Creating, activating and running pipelines is an administrator task on the web.

import 'package:flutter/material.dart';
import '../../models/platform_ops_models.dart';
import '../../services/authenticated_dio.dart';
import '../../services/platform_ops_service.dart';
import '../../widgets/async_view.dart';

class PipelinesScreen extends StatefulWidget {
  final PlatformOpsService? service;

  const PipelinesScreen({Key? key, this.service}) : super(key: key);

  @override
  State<PipelinesScreen> createState() => _PipelinesScreenState();
}

class _PipelinesScreenState extends State<PipelinesScreen> {
  late final PlatformOpsService _service = widget.service ?? PlatformOpsService(createAuthenticatedDio());
  late Future<List<Pipeline>> _pipelines = _service.fetchPipelines();

  void _reload() {
    setState(() {
      _pipelines = _service.fetchPipelines();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Data Pipelines'), elevation: 0),
      body: AsyncView<List<Pipeline>>(
        future: _pipelines,
        onRetry: _reload,
        builder: (context, pipelines) {
          if (pipelines.isEmpty) {
            return const Center(child: Text('No data pipelines are configured.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(8),
            itemCount: pipelines.length,
            itemBuilder: (context, index) {
              final pipeline = pipelines[index];
              return Card(
                margin: const EdgeInsets.all(8),
                child: ListTile(
                  key: Key('pipeline-${pipeline.id}'),
                  title: Text(pipeline.name),
                  subtitle: Text(
                    '${pipeline.sourceType} → ${pipeline.destinationType}'
                    '${pipeline.lastRun != null ? '\nLast run: ${pipeline.lastRun!.toLocal()}' : ''}'
                    '${pipeline.failureCount > 0 ? '\nFailures: ${pipeline.failureCount}' : ''}',
                  ),
                  isThreeLine: pipeline.lastRun != null,
                  trailing: Chip(
                    label: Text(pipeline.isActive ? 'active' : pipeline.status),
                    backgroundColor: pipeline.isActive ? Colors.green.shade200 : Colors.grey.shade200,
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
