// Direct messages with one member: the unread count, the conversation, sending and reading.

import 'package:flutter/material.dart';
import '../models/social_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_account_service.dart';

class MessagesScreen extends StatefulWidget {
  final SocialAccountService? service;
  final int currentUserId;

  const MessagesScreen({Key? key, this.service, required this.currentUserId}) : super(key: key);

  @override
  State<MessagesScreen> createState() => _MessagesScreenState();
}

class _MessagesScreenState extends State<MessagesScreen> {
  late final SocialAccountService _service = widget.service ?? SocialAccountService(createAuthenticatedDio());
  final _otherController = TextEditingController();
  final _draftController = TextEditingController();

  late Future<int> _unread = _service.fetchUnreadMessageCount();
  int? _otherId;
  Future<List<DirectMessage>>? _conversation;

  @override
  void dispose() {
    _otherController.dispose();
    _draftController.dispose();
    super.dispose();
  }

  void _notify(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  void _open() {
    final id = int.tryParse(_otherController.text.trim());
    if (id == null || id <= 0) {
      _notify('Enter the member number you want to message.');
      return;
    }
    setState(() {
      _otherId = id;
      _conversation = _service.fetchConversation(id);
    });
  }

  void _reloadConversation() {
    final id = _otherId;
    if (id == null) return;
    setState(() {
      _conversation = _service.fetchConversation(id);
      _unread = _service.fetchUnreadMessageCount();
    });
  }

  Future<void> _send() async {
    final id = _otherId;
    final text = _draftController.text.trim();
    if (id == null) return;
    if (text.isEmpty) {
      _notify('Write a message first.');
      return;
    }
    try {
      await _service.sendMessage(recipientId: id, content: text);
      _draftController.clear();
      _reloadConversation();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _markRead(DirectMessage message) async {
    try {
      await _service.markMessageRead(message.id);
      _reloadConversation();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Messages')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          FutureBuilder<int>(
            future: _unread,
            builder: (context, snapshot) => Text(
              snapshot.hasData ? '${snapshot.data} unread' : 'Loading unread count...',
              key: const Key('unread-count'),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: TextField(
                  key: const Key('other-member-field'),
                  controller: _otherController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(labelText: 'Member number'),
                ),
              ),
              const SizedBox(width: 12),
              ElevatedButton(key: const Key('open-conversation'), onPressed: _open, child: const Text('Open')),
            ],
          ),
          const Divider(height: 24),
          if (_conversation != null)
            FutureBuilder<List<DirectMessage>>(
              future: _conversation,
              builder: (context, snapshot) {
                if (snapshot.connectionState != ConnectionState.done) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return Text(messageFromError(snapshot.error!), style: const TextStyle(color: Colors.red));
                }
                final messages = snapshot.data ?? const <DirectMessage>[];
                if (messages.isEmpty) return const Text('No messages yet.');
                return Column(
                  children: [
                    for (final message in messages)
                      ListTile(
                        key: Key('message-${message.id}'),
                        contentPadding: EdgeInsets.zero,
                        leading: Icon(
                          message.senderId == widget.currentUserId ? Icons.north_east : Icons.south_west,
                        ),
                        title: Text(message.content),
                        subtitle: Text(message.senderId == widget.currentUserId ? 'Sent' : 'Received'),
                        trailing: !message.isRead && message.senderId != widget.currentUserId
                            ? TextButton(onPressed: () => _markRead(message), child: const Text('Mark read'))
                            : null,
                      ),
                  ],
                );
              },
            ),
          if (_otherId != null) ...[
            TextField(
              key: const Key('message-draft-field'),
              controller: _draftController,
              decoration: const InputDecoration(labelText: 'Message'),
            ),
            ElevatedButton(key: const Key('send-message'), onPressed: _send, child: const Text('Send')),
          ],
        ],
      ),
    );
  }
}
