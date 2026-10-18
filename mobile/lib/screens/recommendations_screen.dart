// Content recommended for the signed-in user, most relevant first.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

class RecommendationsScreen extends StatefulWidget {
  final DiscoveryService? service;

  const RecommendationsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<RecommendationsScreen> createState() => _RecommendationsScreenState();
}

class _RecommendationsScreenState extends State<RecommendationsScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  late Future<List<Recommendation>> _items = _service.fetchRecommendations(limit: 20);

  void _reload() {
    setState(() {
      _items = _service.fetchRecommendations(limit: 20);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Recommendations')),
      body: AsyncView<List<Recommendation>>(
        future: _items,
        onRetry: _reload,
        builder: (context, items) {
          if (items.isEmpty) {
            return const Center(child: Text('Nothing recommended yet.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: items.length,
            itemBuilder: (context, index) {
              final item = items[index];
              return Card(
                child: ListTile(
                  key: Key('recommendation-${item.id}'),
                  title: Text(item.title),
                  subtitle: Text(item.reason ?? item.creator ?? 'Content #${item.contentId}'),
                  trailing: Text('${item.views} views'),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
