import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/platform_completion_models.dart';
import '../../providers/platform_completion_providers.dart';


class SocialScreen extends ConsumerWidget {
  final int userId;

  const SocialScreen({Key? key, required this.userId}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Social Hub'),
          bottom: const TabBar(
            tabs: [
              Tab(icon: Icon(Icons.favorite), text: 'Interactions'),
              Tab(icon: Icon(Icons.people), text: 'Follows'),
              Tab(icon: Icon(Icons.message), text: 'Messages'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _buildInteractionsTab(context, ref),
            _buildFollowsTab(context, ref),
            _buildMessagesTab(context, ref),
          ],
        ),
      ),
    );
  }

  Widget _buildInteractionsTab(BuildContext context, WidgetRef ref) {
    final interactions = ref.watch(
      userInteractionsProvider({
        'user_id': userId,
        'limit': 50,
        'offset': 0,
      }),
    );

    return interactions.when(
      data: (data) => ListView.builder(
        itemCount: data.length,
        itemBuilder: (context, index) {
          final interaction = data[index];
          return ListTile(
            leading: _getInteractionIcon(interaction.interactionType),
            title: Text('${interaction.interactionType.toUpperCase()} - Content #${interaction.contentId}'),
            subtitle: Text(interaction.createdAt.toString()),
            trailing: IconButton(
              icon: const Icon(Icons.delete),
              onPressed: () {
                // Delete interaction
              },
            ),
          );
        },
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }

  Widget _buildFollowsTab(BuildContext context, WidgetRef ref) {
    final followers = ref.watch(
      followersProvider({
        'user_id': userId,
        'limit': 50,
        'offset': 0,
      }),
    );

    final following = ref.watch(
      followingProvider({
        'user_id': userId,
        'limit': 50,
        'offset': 0,
      }),
    );

    return SingleChildScrollView(
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              'Followers & Following',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
          ),
          followers.when(
            data: (data) => Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text('Followers: ${data.length}'),
            ),
            loading: () => const SizedBox.shrink(),
            error: (err, stack) => SizedBox.shrink(),
          ),
          following.when(
            data: (data) => Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text('Following: ${data.length}'),
            ),
            loading: () => const SizedBox.shrink(),
            error: (err, stack) => const SizedBox.shrink(),
          ),
        ],
      ),
    );
  }

  Widget _buildMessagesTab(BuildContext context, WidgetRef ref) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.message, size: 64, color: Colors.grey),
          const SizedBox(height: 16),
          const Text('Direct Messages'),
          const SizedBox(height: 8),
          const Text('Your conversations will appear here'),
          const SizedBox(height: 32),
          ElevatedButton(
            onPressed: () {
              // Open new message dialog
            },
            child: const Text('Start Conversation'),
          ),
        ],
      ),
    );
  }

  IconData _getInteractionIcon(String type) {
    switch (type) {
      case 'like':
        return Icons.favorite;
      case 'comment':
        return Icons.comment;
      case 'share':
        return Icons.share;
      case 'follow':
        return Icons.person_add;
      case 'bookmark':
        return Icons.bookmark;
      default:
        return Icons.star;
    }
  }
}
