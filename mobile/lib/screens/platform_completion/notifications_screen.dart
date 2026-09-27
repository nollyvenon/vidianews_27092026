import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/platform_completion_models.dart';
import '../../providers/platform_completion_providers.dart';


class NotificationsScreen extends ConsumerWidget {
  final int userId;

  const NotificationsScreen({Key? key, required this.userId}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Notifications'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Push Notifications'),
              Tab(text: 'System'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _buildPushNotifications(context, ref),
            _buildSystemNotifications(context, ref),
          ],
        ),
      ),
    );
  }

  Widget _buildPushNotifications(BuildContext context, WidgetRef ref) {
    final logs = ref.watch(
      notificationLogsProvider({
        'user_id': userId,
        'limit': 50,
        'offset': 0,
      }),
    );

    final devices = ref.watch(userDevicesProvider(userId));

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Registered Devices',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  devices.when(
                    data: (data) => Text('${data.length} device(s) registered'),
                    loading: () => const SizedBox.shrink(),
                    error: (err, stack) => const Text('Error loading devices'),
                  ),
                ],
              ),
            ),
          ),
        ),
        Expanded(
          child: logs.when(
            data: (data) {
              if (data.isEmpty) {
                return Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.notifications_none, size: 64, color: Colors.grey),
                      const SizedBox(height: 16),
                      const Text('No notifications'),
                    ],
                  ),
                );
              }

              return ListView.builder(
                itemCount: data.length,
                itemBuilder: (context, index) {
                  final log = data[index];
                  return ListTile(
                    leading: _getNotificationIcon(log.notificationType),
                    title: Text(log.title),
                    subtitle: Text(log.body),
                    trailing: _getStatusBadge(log.status),
                  );
                },
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (err, stack) => Center(child: Text('Error: $err')),
          ),
        ),
      ],
    );
  }

  Widget _buildSystemNotifications(BuildContext context, WidgetRef ref) {
    final notifications = ref.watch(
      systemNotificationsProvider({
        'limit': 50,
        'offset': 0,
      }),
    );

    return notifications.when(
      data: (data) {
        if (data.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.info_outline, size: 64, color: Colors.grey),
                const SizedBox(height: 16),
                const Text('No system notifications'),
              ],
            ),
          );
        }

        return ListView.builder(
          itemCount: data.length,
          itemBuilder: (context, index) {
            final notification = data[index];
            return Card(
              margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: ListTile(
                leading: _getSystemNotificationIcon(notification.notificationType),
                title: Text(notification.title),
                subtitle: Text(notification.message),
                trailing: Text(notification.createdAt.toString()),
              ),
            );
          },
        );
      },
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }

  IconData _getNotificationIcon(String type) {
    switch (type) {
      case 'engagement':
        return Icons.favorite;
      case 'content':
        return Icons.article;
      case 'social':
        return Icons.people;
      case 'system':
        return Icons.settings;
      case 'promotional':
        return Icons.local_offer;
      default:
        return Icons.notifications;
    }
  }

  IconData _getSystemNotificationIcon(String type) {
    switch (type) {
      case 'alert':
        return Icons.warning;
      case 'info':
        return Icons.info;
      case 'success':
        return Icons.check_circle;
      case 'error':
        return Icons.error;
      default:
        return Icons.notifications;
    }
  }

  Widget _getStatusBadge(String status) {
    Color color;
    switch (status) {
      case 'delivered':
        color = Colors.green;
        break;
      case 'opened':
        color = Colors.blue;
        break;
      case 'pending':
        color = Colors.orange;
        break;
      default:
        color = Colors.grey;
    }

    return Chip(
      label: Text(status),
      backgroundColor: color.withOpacity(0.3),
      labelStyle: TextStyle(color: color),
    );
  }
}
