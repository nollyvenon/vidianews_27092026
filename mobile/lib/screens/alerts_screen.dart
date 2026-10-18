// Alerts addressed to the signed-in user, with mark-as-read.

import 'package:flutter/material.dart';
import '../models/social_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_account_service.dart';
import '../widgets/async_view.dart';

class AlertsScreen extends StatefulWidget {
  final SocialAccountService? service;

  const AlertsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<AlertsScreen> createState() => _AlertsScreenState();
}

class _AlertsScreenState extends State<AlertsScreen> {
  late final SocialAccountService _service = widget.service ?? SocialAccountService(createAuthenticatedDio());
  late Future<List<AppNotification>> _alerts = _service.fetchAlerts();

  void _reload() {
    setState(() {
      _alerts = _service.fetchAlerts();
    });
  }

  Future<void> _markRead(AppNotification alert) async {
    try {
      await _service.markAlertRead(alert.id);
      _reload();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Alerts')),
      body: AsyncView<List<AppNotification>>(
        future: _alerts,
        onRetry: _reload,
        builder: (context, alerts) {
          if (alerts.isEmpty) {
            return const Center(child: Text('No alerts.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: alerts.length,
            itemBuilder: (context, index) {
              final alert = alerts[index];
              return Card(
                child: ListTile(
                  key: Key('alert-${alert.id}'),
                  leading: Icon(alert.isRead ? Icons.notifications_none : Icons.notifications_active),
                  title: Text(alert.title),
                  subtitle: Text(alert.message),
                  trailing: alert.isRead
                      ? null
                      : TextButton(onPressed: () => _markRead(alert), child: const Text('Mark read')),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
