// Search the resources indexed for the signed-in user's organization.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';

class SearchScreen extends StatefulWidget {
  final DiscoveryService? service;

  const SearchScreen({Key? key, this.service}) : super(key: key);

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  final _queryController = TextEditingController();
  Future<List<SearchResult>>? _results;

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }

  void _search() {
    final query = _queryController.text.trim();
    if (query.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Enter something to search for.')));
      return;
    }
    setState(() {
      _results = _service.search(query);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Search')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              Expanded(
                child: TextField(
                  key: const Key('search-field'),
                  controller: _queryController,
                  textInputAction: TextInputAction.search,
                  onSubmitted: (_) => _search(),
                  decoration: const InputDecoration(labelText: 'Search'),
                ),
              ),
              const SizedBox(width: 12),
              ElevatedButton(key: const Key('search-button'), onPressed: _search, child: const Text('Search')),
            ],
          ),
          const SizedBox(height: 16),
          if (_results != null)
            FutureBuilder<List<SearchResult>>(
              future: _results,
              builder: (context, snapshot) {
                if (snapshot.connectionState != ConnectionState.done) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return Text(
                    messageFromError(snapshot.error!),
                    style: const TextStyle(color: Colors.red),
                  );
                }
                final results = snapshot.data ?? const <SearchResult>[];
                if (results.isEmpty) return const Text('No results.');
                return Column(
                  children: [
                    for (final result in results)
                      ListTile(
                        key: Key('result-${result.id}'),
                        contentPadding: EdgeInsets.zero,
                        title: Text(result.title),
                        subtitle: Text(result.content ?? result.resourceType),
                        trailing: Text(result.resourceType),
                      ),
                  ],
                );
              },
            ),
        ],
      ),
    );
  }
}
