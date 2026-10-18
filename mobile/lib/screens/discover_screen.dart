// Content recommended for the signed-in user, and the topics trending across the platform.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

class _DiscoverData {
  final List<Recommendation> recommendations;
  final List<TrendingTopic> trending;

  const _DiscoverData({required this.recommendations, required this.trending});
}

class DiscoverScreen extends StatefulWidget {
  final DiscoveryService? service;

  const DiscoverScreen({Key? key, this.service}) : super(key: key);

  @override
  State<DiscoverScreen> createState() => _DiscoverScreenState();
}

class _DiscoverScreenState extends State<DiscoverScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  late Future<_DiscoverData> _data = _load();

  Future<_DiscoverData> _load() async {
    final recommendations = await _service.fetchRecommendations();
    final trending = await _service.fetchTrending();
    return _DiscoverData(recommendations: recommendations, trending: trending);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Discover')),
      body: AsyncView<_DiscoverData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text('Recommended for you', style: Theme.of(context).textTheme.titleMedium),
            if (data.recommendations.isEmpty) const Text('Nothing recommended yet.'),
            for (final item in data.recommendations)
              ListTile(
                key: Key('recommendation-${item.id}'),
                contentPadding: EdgeInsets.zero,
                title: Text(item.title),
                subtitle: Text(item.reason ?? item.creator ?? 'Content #${item.contentId}'),
                trailing: Text('${item.views} views'),
              ),
            const Divider(height: 32),
            Text('Trending topics', style: Theme.of(context).textTheme.titleMedium),
            if (data.trending.isEmpty) const Text('No trending topics right now.'),
            for (final topic in data.trending)
              ListTile(
                key: Key('topic-${topic.id}'),
                contentPadding: EdgeInsets.zero,
                title: Text(topic.topic),
                trailing: Text('${topic.mentionCount} mentions'),
              ),
          ],
        ),
      ),
    );
  }
}
