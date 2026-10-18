// Push notifications: the devices this account receives them on, and the recent deliveries.

import 'package:flutter/material.dart';
import '../models/community_models.dart';
import '../services/authenticated_dio.dart';
import '../services/community_service.dart';
import '../widgets/async_view.dart';

class _PushData {
  final List<PushDevice> devices;
  final List<NotificationLog> logs;

  const _PushData({required this.devices, required this.logs});
}

class PushNotificationsScreen extends StatefulWidget {
  final CommunityService? service;

  const PushNotificationsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<PushNotificationsScreen> createState() => _PushNotificationsScreenState();
}

class _PushNotificationsScreenState extends State<PushNotificationsScreen> {
  late final CommunityService _service = widget.service ?? CommunityService(createAuthenticatedDio());
  final _tokenController = TextEditingController();
  final _nameController = TextEditingController();
  String _platform = 'android';
  late Future<_PushData> _data = _load();

  @override
  void dispose() {
    _tokenController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  Future<_PushData> _load() async {
    final devices = await _service.fetchDevices();
    final logs = await _service.fetchNotificationLogs();
    return _PushData(devices: devices, logs: logs);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  void _notify(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> _register() async {
    final token = _tokenController.text.trim();
    if (token.isEmpty) {
      _notify('Enter this device\'s push token.');
      return;
    }
    try {
      await _service.registerDevice(token: token, platform: _platform, name: _nameController.text.trim().isEmpty ? null : _nameController.text.trim());
      _tokenController.clear();
      _nameController.clear();
      _notify('Device registered for push notifications.');
      _reload();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _remove(PushDevice device) async {
    try {
      await _service.removeDevice(device.id);
      _reload();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Push notifications')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            key: const Key('push-token-field'),
            controller: _tokenController,
            decoration: const InputDecoration(labelText: 'Device push token'),
          ),
          TextField(
            key: const Key('device-name-field'),
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'Device name (optional)'),
          ),
          DropdownButtonFormField<String>(
            key: const Key('device-platform'),
            initialValue: _platform,
            decoration: const InputDecoration(labelText: 'Platform'),
            items: const [
              DropdownMenuItem(value: 'android', child: Text('Android')),
              DropdownMenuItem(value: 'ios', child: Text('iOS')),
              DropdownMenuItem(value: 'web', child: Text('Web')),
            ],
            onChanged: (value) => setState(() => _platform = value ?? _platform),
          ),
          ElevatedButton(key: const Key('register-device'), onPressed: _register, child: const Text('Register this device')),
          const Divider(height: 32),
          AsyncView<_PushData>(
            future: _data,
            onRetry: _reload,
            builder: (context, data) => Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Registered devices', style: TextStyle(fontWeight: FontWeight.bold)),
                if (data.devices.isEmpty) const Text('No devices registered.'),
                for (final device in data.devices)
                  ListTile(
                    key: Key('device-${device.id}'),
                    contentPadding: EdgeInsets.zero,
                    title: Text(device.deviceName ?? device.platform),
                    subtitle: Text(device.platform),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline),
                      tooltip: 'Remove device',
                      onPressed: () => _remove(device),
                    ),
                  ),
                const Divider(height: 32),
                const Text('Recent notifications', style: TextStyle(fontWeight: FontWeight.bold)),
                if (data.logs.isEmpty) const Text('No notifications sent yet.'),
                for (final log in data.logs)
                  ListTile(
                    key: Key('log-${log.id}'),
                    contentPadding: EdgeInsets.zero,
                    title: Text(log.title),
                    subtitle: Text(log.body),
                    trailing: Text(log.status),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
