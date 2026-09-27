import 'package:flutter/material.dart';
import '../../services/notification_service.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({Key? key}) : super(key: key);

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  late NotificationService _notificationService;
  List<dynamic> _notifications = [];
  int _unreadCount = 0;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _notificationService = NotificationService();
    _loadNotifications();
  }

  Future<void> _loadNotifications() async {
    try {
      final notifs = await _notificationService.getMyNotifications();
      final unread = await _notificationService.getUnreadCount();

      setState(() {
        _notifications = notifs;
        _unreadCount = unread['unread_count'] ?? 0;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading notifications: $e')),
        );
      }
    }
  }

  Future<void> _markAsRead(int id) async {
    try {
      await _notificationService.markAsRead(id);
      _loadNotifications();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  Future<void> _markAllAsRead() async {
    try {
      await _notificationService.markAllAsRead();
      _loadNotifications();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  Future<void> _archiveNotification(int id) async {
    try {
      await _notificationService.archiveNotification(id);
      _loadNotifications();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  Future<void> _deleteNotification(int id) async {
    try {
      await _notificationService.deleteNotification(id);
      _loadNotifications();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Scaffold(
        appBar: AppBar(title: const Text('Notifications')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
        actions: [
          if (_unreadCount > 0)
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Center(
                child: GestureDetector(
                  onTap: _markAllAsRead,
                  child: Text(
                    'Mark all read',
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              ),
            ),
        ],
      ),
      body: _notifications.isEmpty
          ? Center(
              child: Text(
                'No notifications',
                style: TextStyle(color: Colors.grey),
              ),
            )
          : ListView.builder(
              itemCount: _notifications.length,
              itemBuilder: (context, index) {
                final notif = _notifications[index];
                return Card(
                  margin: EdgeInsets.all(8),
                  child: ListTile(
                    title: Text(notif['title'] ?? ''),
                    subtitle: Text(notif['message'] ?? ''),
                    trailing: PopupMenuButton(
                      itemBuilder: (context) => [
                        if (!(notif['is_read'] ?? false))
                          PopupMenuItem(
                            child: Text('Mark as read'),
                            onTap: () => _markAsRead(notif['id']),
                          ),
                        PopupMenuItem(
                          child: Text('Archive'),
                          onTap: () => _archiveNotification(notif['id']),
                        ),
                        PopupMenuItem(
                          child: Text('Delete'),
                          onTap: () => _deleteNotification(notif['id']),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
