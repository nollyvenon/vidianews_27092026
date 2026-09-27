import 'package:flutter/material.dart';
import '../../services/settings_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late SettingsService _settingsService;
  Map<String, dynamic>? _settings;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _settingsService = SettingsService();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    try {
      final settings = await _settingsService.getAllSettings();
      setState(() {
        _settings = settings;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading settings: $e')),
        );
      }
    }
  }

  Future<void> _updateNotificationSettings(Map<String, dynamic> updates) async {
    try {
      final result = await _settingsService.updateNotificationSettings(updates);
      setState(() {
        _settings?['notifications'] = result;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Notification settings updated')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  Future<void> _updatePrivacySettings(Map<String, dynamic> updates) async {
    try {
      final result = await _settingsService.updatePrivacySettings(updates);
      setState(() {
        _settings?['privacy'] = result;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Privacy settings updated')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  Future<void> _updateDisplaySettings(Map<String, dynamic> updates) async {
    try {
      final result = await _settingsService.updateDisplaySettings(updates);
      setState(() {
        _settings?['display'] = result;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Display settings updated')),
        );
      }
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
        appBar: AppBar(title: const Text('Settings')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Settings'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Notifications'),
              Tab(text: 'Privacy'),
              Tab(text: 'Display'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _buildNotificationSettings(),
            _buildPrivacySettings(),
            _buildDisplaySettings(),
          ],
        ),
      ),
    );
  }

  Widget _buildNotificationSettings() {
    final notif = _settings?['notifications'] ?? {};

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        SwitchListTile(
          title: const Text('Activity Notifications'),
          value: notif['email_on_activity'] ?? true,
          onChanged: (value) {
            _updateNotificationSettings({'email_on_activity': value});
          },
        ),
        SwitchListTile(
          title: const Text('Push Notifications'),
          value: notif['push_enabled'] ?? true,
          onChanged: (value) {
            _updateNotificationSettings({'push_enabled': value});
          },
        ),
        SwitchListTile(
          title: const Text('In-App Notifications'),
          value: notif['inapp_enabled'] ?? true,
          onChanged: (value) {
            _updateNotificationSettings({'inapp_enabled': value});
          },
        ),
      ],
    );
  }

  Widget _buildPrivacySettings() {
    final privacy = _settings?['privacy'] ?? {};

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ListTile(
          title: const Text('Profile Visibility'),
          trailing: DropdownButton<String>(
            value: privacy['profile_visibility'] ?? 'private',
            onChanged: (value) {
              if (value != null) {
                _updatePrivacySettings({'profile_visibility': value});
              }
            },
            items: const [
              DropdownMenuItem(value: 'private', child: Text('Private')),
              DropdownMenuItem(value: 'public', child: Text('Public')),
            ],
          ),
        ),
        SwitchListTile(
          title: const Text('Allow Messages'),
          value: privacy['allow_messages'] == 'everyone',
          onChanged: (value) {
            _updatePrivacySettings({'allow_messages': value ? 'everyone' : 'nobody'});
          },
        ),
        SwitchListTile(
          title: const Text('Show Email'),
          value: privacy['show_email'] ?? false,
          onChanged: (value) {
            _updatePrivacySettings({'show_email': value});
          },
        ),
      ],
    );
  }

  Widget _buildDisplaySettings() {
    final display = _settings?['display'] ?? {};

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        ListTile(
          title: const Text('Theme'),
          trailing: DropdownButton<String>(
            value: display['theme'] ?? 'light',
            onChanged: (value) {
              if (value != null) {
                _updateDisplaySettings({'theme': value});
              }
            },
            items: const [
              DropdownMenuItem(value: 'light', child: Text('Light')),
              DropdownMenuItem(value: 'dark', child: Text('Dark')),
              DropdownMenuItem(value: 'auto', child: Text('Auto')),
            ],
          ),
        ),
        ListTile(
          title: const Text('Language'),
          trailing: DropdownButton<String>(
            value: display['language'] ?? 'en',
            onChanged: (value) {
              if (value != null) {
                _updateDisplaySettings({'language': value});
              }
            },
            items: const [
              DropdownMenuItem(value: 'en', child: Text('English')),
              DropdownMenuItem(value: 'es', child: Text('Español')),
              DropdownMenuItem(value: 'fr', child: Text('Français')),
            ],
          ),
        ),
      ],
    );
  }
}
