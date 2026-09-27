import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/platform_completion_models.dart';
import '../../providers/platform_completion_providers.dart';


final searchQueryProvider = StateProvider<String>((ref) => '');


class SearchScreen extends ConsumerWidget {
  final int userId;

  const SearchScreen({Key? key, required this.userId}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final query = ref.watch(searchQueryProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Search'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              onChanged: (value) {
                ref.read(searchQueryProvider.notifier).state = value;
              },
              decoration: InputDecoration(
                hintText: 'Search content...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
          ),
          if (query.isNotEmpty)
            Expanded(
              child: _buildSearchResults(context, ref, query),
            )
          else
            Expanded(
              child: _buildSavedSearches(context, ref),
            ),
        ],
      ),
    );
  }

  Widget _buildSearchResults(BuildContext context, WidgetRef ref, String query) {
    final results = ref.watch(
      searchContentProvider({
        'query': query,
        'limit': 20,
        'offset': 0,
      }),
    );

    return results.when(
      data: (data) {
        if (data.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.search_off, size: 64, color: Colors.grey),
                const SizedBox(height: 16),
                const Text('No results found'),
              ],
            ),
          );
        }

        return ListView.builder(
          itemCount: data.length,
          itemBuilder: (context, index) {
            final result = data[index];
            return ListTile(
              title: Text(result.title),
              subtitle: Text(result.content.length > 100
                  ? '${result.content.substring(0, 100)}...'
                  : result.content),
              trailing: IconButton(
                icon: const Icon(Icons.bookmark_border),
                onPressed: () {
                  // Save search
                },
              ),
            );
          },
        );
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }

  Widget _buildSavedSearches(BuildContext context, WidgetRef ref) {
    final saved = ref.watch(
      savedSearchesProvider({
        'user_id': userId,
        'limit': 50,
        'offset': 0,
      }),
    );

    return saved.when(
      data: (data) {
        if (data.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.bookmark_outline, size: 64, color: Colors.grey),
                const SizedBox(height: 16),
                const Text('No saved searches yet'),
                const SizedBox(height: 8),
                const Text('Your searches will be saved here'),
              ],
            ),
          );
        }

        return ListView.builder(
          itemCount: data.length,
          itemBuilder: (context, index) {
            final search = data[index];
            return ListTile(
              leading: const Icon(Icons.bookmark),
              title: Text(search.query),
              subtitle: Text('${search.resultCount} results'),
              trailing: IconButton(
                icon: const Icon(Icons.delete),
                onPressed: () {
                  // Delete saved search
                },
              ),
              onTap: () {
                ref.read(searchQueryProvider.notifier).state = search.query;
              },
            );
          },
        );
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }
}
