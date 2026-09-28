import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class APIDocsScreen extends ConsumerWidget {
  const APIDocsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final endpoints = [
      {'path': '/users', 'method': 'GET', 'calls': 1234},
      {'path': '/users/{id}', 'method': 'GET', 'calls': 567},
      {'path': '/users', 'method': 'POST', 'calls': 89},
      {'path': '/content', 'method': 'GET', 'calls': 4567},
      {'path': '/recommendations', 'method': 'GET', 'calls': 2345},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('API Documentation'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'API Endpoints',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Version 1.0.0',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              padding: const EdgeInsets.symmetric(horizontal: 8),
              itemCount: endpoints.length,
              itemBuilder: (context, index) {
                final endpoint = endpoints[index];
                return _buildEndpointCard(
                  endpoint['path'] as String,
                  endpoint['method'] as String,
                  endpoint['calls'] as int,
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEndpointCard(String path, String method, int calls) {
    Color methodColor;
    switch (method) {
      case 'GET':
        methodColor = Colors.blue;
        break;
      case 'POST':
        methodColor = Colors.green;
        break;
      case 'PUT':
        methodColor = Colors.orange;
        break;
      case 'DELETE':
        methodColor = Colors.red;
        break;
      default:
        methodColor = Colors.gray;
    }

    return Card(
      margin: const EdgeInsets.all(8),
      child: ListTile(
        leading: Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            color: methodColor.withOpacity(0.2),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Center(
            child: Text(
              method,
              style: TextStyle(
                color: methodColor,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
        ),
        title: Text(path),
        subtitle: Text('$calls calls'),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      ),
    );
  }
}
