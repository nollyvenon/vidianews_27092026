// The people who follow the signed-in user.

import 'package:flutter/material.dart';
import '../models/social_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_account_service.dart';
import '../widgets/async_view.dart';

class FollowersScreen extends StatefulWidget {
  final SocialAccountService? service;
  final int userId;

  const FollowersScreen({Key? key, this.service, required this.userId}) : super(key: key);

  @override
  State<FollowersScreen> createState() => _FollowersScreenState();
}

class _FollowersScreenState extends State<FollowersScreen> {
  late final SocialAccountService _service = widget.service ?? SocialAccountService(createAuthenticatedDio());
  late Future<List<Follower>> _followers = _service.fetchFollowers(widget.userId);

  void _reload() {
    setState(() {
      _followers = _service.fetchFollowers(widget.userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Followers')),
      body: AsyncView<List<Follower>>(
        future: _followers,
        onRetry: _reload,
        builder: (context, followers) {
          if (followers.isEmpty) {
            return const Center(child: Text('No followers yet.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: followers.length,
            itemBuilder: (context, index) {
              final follower = followers[index];
              return ListTile(
                key: Key('follower-${follower.id}'),
                leading: const CircleAvatar(child: Icon(Icons.person)),
                title: Text(follower.followerName ?? 'Member #${follower.followerId}'),
                subtitle: follower.followedAt != null
                    ? Text('Following since ${follower.followedAt!.toLocal().toString().split(' ').first}')
                    : null,
              );
            },
          );
        },
      ),
    );
  }
}
