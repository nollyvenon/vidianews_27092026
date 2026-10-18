// Notices from the platform, with mark-as-read.

import 'package:flutter/material.dart';
import '../models/social_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_account_service.dart';
import '../widgets/async_view.dart';

class NotificationsCenterScreen extends StatefulWidget {
  final SocialAccountService? service;

  const NotificationsCenterScreen({Key? key, this.service}) : super(key: key);

  @override
  State<NotificationsCenterScreen> createState() => _NotificationsCenterScreenState();
}

class _NotificationsCenterScreenState extends State<NotificationsCenterScreen> {
  late final SocialAccountService _service = widget.service ?? SocialAccountService(createAuthenticatedDio());
  late Future<List<AppNotification>> _notices = _service.fetchNotices();

  void _reload() {
    setState(() {
      _notices = _service.fetchNotices();
    });
  }

  Future<void> _markRead(AppNotification notice) async {
    try {
      await _service.markNoticeRead(notice.id);
      _reload();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notifications')),
      body: AsyncView<List<AppNotification>>(
        future: _notices,
        onRetry: _reload,
        builder: (context, notices) {
          if (notices.isEmpty) {
            return const Center(child: Text('No notifications.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: notices.length,
            itemBuilder: (context, index) {
              final notice = notices[index];
              return Card(
                child: ListTile(
                  key: Key('notice-${notice.id}'),
                  title: Text(notice.title),
                  subtitle: Text(notice.message),
                  trailing: notice.isRead
                      ? null
                      : TextButton(onPressed: () => _markRead(notice), child: const Text('Mark read')),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
