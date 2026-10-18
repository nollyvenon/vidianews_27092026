// The comment thread for one piece of content, and posting a new comment.

import 'package:flutter/material.dart';
import '../models/community_models.dart';
import '../services/authenticated_dio.dart';
import '../services/community_service.dart';
import '../widgets/async_view.dart';

class CommentsScreen extends StatefulWidget {
  final int resourceId;
  final String resourceType;
  final CommunityService? service;

  const CommentsScreen({
    Key? key,
    required this.resourceId,
    required this.resourceType,
    this.service,
  }) : super(key: key);

  @override
  State<CommentsScreen> createState() => _CommentsScreenState();
}

class _CommentsScreenState extends State<CommentsScreen> {
  late final CommunityService _service = widget.service ?? CommunityService(createAuthenticatedDio());
  final TextEditingController _controller = TextEditingController();
  late Future<List<ContentComment>> _comments = _service.fetchComments(widget.resourceId);

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() {
      _comments = _service.fetchComments(widget.resourceId);
    });
  }

  Future<void> _post() async {
    final text = _controller.text.trim();
    if (text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Write a comment first.')));
      return;
    }
    try {
      await _service.postComment(contentId: widget.resourceId, text: text);
      _controller.clear();
      _reload();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Comments')),
      body: Column(
        children: [
          Expanded(
            child: AsyncView<List<ContentComment>>(
              future: _comments,
              onRetry: _reload,
              builder: (context, comments) {
                if (comments.isEmpty) {
                  return const Center(child: Text('No comments yet.'));
                }
                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: comments.length,
                  itemBuilder: (context, index) {
                    final comment = comments[index];
                    return ListTile(
                      key: Key('comment-${comment.id}'),
                      title: Text(comment.text),
                      subtitle: Text(comment.status == 'edited' ? 'Edited' : 'Member #${comment.userId}'),
                    );
                  },
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    key: const Key('comment-field'),
                    controller: _controller,
                    decoration: const InputDecoration(hintText: 'Write a comment...'),
                  ),
                ),
                IconButton(key: const Key('post-comment'), icon: const Icon(Icons.send), onPressed: _post),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// Asks for the content number whose comments to open.
class CommentsLookupScreen extends StatefulWidget {
  const CommentsLookupScreen({Key? key}) : super(key: key);

  @override
  State<CommentsLookupScreen> createState() => _CommentsLookupScreenState();
}

class _CommentsLookupScreenState extends State<CommentsLookupScreen> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _open() {
    final id = int.tryParse(_controller.text.trim());
    if (id == null || id <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Enter a valid content number.')));
      return;
    }
    Navigator.of(context).push(MaterialPageRoute<void>(
      builder: (_) => CommentsScreen(resourceId: id, resourceType: 'content'),
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Comments')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              key: const Key('content-number-field'),
              controller: _controller,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Content number'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(key: const Key('open-comments'), onPressed: _open, child: const Text('Open comments')),
          ],
        ),
      ),
    );
  }
}
