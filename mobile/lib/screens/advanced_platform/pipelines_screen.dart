import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class PipelinesScreen extends ConsumerWidget {
  const PipelinesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pipelines = [
      {'name': 'User Sync', 'status': 'active', 'source': 'database', 'dest': 'warehouse'},
      {'name': 'Event Pipeline', 'status': 'active', 'source': 'events', 'dest': 'analytics'},
      {'name': 'ETL Process', 'status': 'inactive', 'source': 'api', 'dest': 'storage'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Data Pipelines'),
        elevation: 0,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(8),
        itemCount: pipelines.length,
        itemBuilder: (context, index) {
          final pipeline = pipelines[index];
          return Card(
            margin: const EdgeInsets.all(8),
            child: ListTile(
              title: Text(pipeline['name'] as String),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${pipeline['source']} → ${pipeline['dest']}'),
                  Text('Status: ${pipeline['status']}'),
                ],
              ),
              trailing: Chip(
                label: Text(pipeline['status'] as String),
                backgroundColor: pipeline['status'] == 'active'
                    ? Colors.green.shade200
                    : Colors.gray.shade200,
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}
