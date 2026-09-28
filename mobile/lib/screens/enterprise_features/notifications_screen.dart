import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/enterprise_features_models.dart';
import '../../providers/enterprise_features_providers.dart';

class NotificationsScreen extends ConsumerWidget {
  final int userId;

  const NotificationsScreen({
    Key? key,
    required this.userId,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notifications = ref.watch(userNotificationsProvider(userId));
    final preferences = ref.watch(notificationPreferencesProvider(userId));

    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Notifications'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Notifications'),
              Tab(text: 'Preferences'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _buildNotificationsTab(notifications),
            _buildPreferencesTab(context, ref, preferences, userId),
          ],
        ),
      ),
    );
  }

  Widget _buildNotificationsTab(AsyncValue<List<Notification>> notifs) {
    return notifs.when(
      data: (items) => _buildNotificationsList(items),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }

  Widget _buildNotificationsList(List<Notification> items) {
    if (items.isEmpty) {
      return const Center(child: Text('No notifications'));
    }

    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        final notif = items[index];
        return ListTile(
          leading: _getNotificationIcon(notif.notificationType),
          title: Text(notif.title),
          subtitle: Text(notif.message),
          trailing: notif.read
              ? null
              : Container(
                  width: 12,
                  height: 12,
                  decoration: const BoxDecoration(
                    color: Colors.blue,
                    shape: BoxShape.circle,
                  ),
                ),
        );
      },
    );
  }

  Widget _buildPreferencesTab(
    BuildContext context,
    WidgetRef ref,
    AsyncValue<NotificationPreference> prefs,
    int userId,
  ) {
    return prefs.when(
      data: (pref) => _buildPreferencesForm(pref),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Error: $err')),
    );
  }

  Widget _buildPreferencesForm(NotificationPreference pref) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        SwitchListTile(
          title: const Text('Email Notifications'),
          value: pref.emailEnabled,
          onChanged: (_) {},
        ),
        SwitchListTile(
          title: const Text('Push Notifications'),
          value: pref.pushEnabled,
          onChanged: (_) {},
        ),
        SwitchListTile(
          title: const Text('SMS Notifications'),
          value: pref.smsEnabled,
          onChanged: (_) {},
        ),
        SwitchListTile(
          title: const Text('In-App Notifications'),
          value: pref.inAppEnabled,
          onChanged: (_) {},
        ),
        const SizedBox(height: 16),
        DropdownButton<String>(
          isExpanded: true,
          value: pref.frequency,
          items: ['immediate', 'hourly', 'daily', 'weekly']
              .map((e) => DropdownMenuItem(value: e, child: Text(e)))
              .toList(),
          onChanged: (_) {},
        ),
      ],
    );
  }

  Icon _getNotificationIcon(String type) {
    switch (type) {
      case 'alert':
        return const Icon(Icons.warning, color: Colors.red);
      case 'success':
        return const Icon(Icons.check_circle, color: Colors.green);
      case 'error':
        return const Icon(Icons.error, color: Colors.red);
      case 'warning':
        return const Icon(Icons.warning_amber, color: Colors.orange);
      default:
        return const Icon(Icons.info, color: Colors.blue);
    }
  }
}
