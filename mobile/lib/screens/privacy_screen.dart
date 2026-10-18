// Privacy: who sees the profile and content, consent choices, a copy of the data, and account deletion.

import 'package:flutter/material.dart';
import '../models/social_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_account_service.dart';
import '../widgets/async_view.dart';

const List<MapEntry<String, String>> _visibilityOptions = [
  MapEntry('public', 'Public'),
  MapEntry('friends_only', 'Friends only'),
  MapEntry('private', 'Private'),
];

class _PrivacyData {
  final PrivacySettings settings;
  final List<ConsentEntry> consents;

  const _PrivacyData({required this.settings, required this.consents});
}

class PrivacyScreen extends StatefulWidget {
  final SocialAccountService? service;

  const PrivacyScreen({Key? key, this.service}) : super(key: key);

  @override
  State<PrivacyScreen> createState() => _PrivacyScreenState();
}

class _PrivacyScreenState extends State<PrivacyScreen> {
  late final SocialAccountService _service = widget.service ?? SocialAccountService(createAuthenticatedDio());
  late Future<_PrivacyData> _data = _load();
  PrivacySettings? _editing;

  Future<_PrivacyData> _load() async {
    final settings = await _service.fetchPrivacySettings();
    final consents = await _service.fetchConsents();
    _editing = settings;
    return _PrivacyData(settings: settings, consents: consents);
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

  Future<void> _save() async {
    final draft = _editing;
    if (draft == null) return;
    try {
      final saved = await _service.updatePrivacySettings(draft);
      await _service.logConsent(consentType: 'analytics', granted: saved.allowAnalytics);
      await _service.logConsent(consentType: 'marketing', granted: saved.allowMarketing);
      _notify('Privacy preferences saved.');
      _reload();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _export() async {
    try {
      final data = await _service.exportData();
      _notify('Your data export is ready: ${data.length} sections.');
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _requestDeletion() async {
    try {
      final scheduledFor = await _service.requestDeletion();
      _notify('Deletion scheduled for ${scheduledFor.toLocal().toString().split(' ').first}.');
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Privacy')),
      body: AsyncView<_PrivacyData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) {
          final draft = _editing ?? data.settings;
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              const Text('Visibility', style: TextStyle(fontWeight: FontWeight.bold)),
              DropdownButtonFormField<String>(
                key: const Key('profile-visibility'),
                initialValue: draft.profileVisibility,
                decoration: const InputDecoration(labelText: 'Profile visible to'),
                items: [for (final option in _visibilityOptions) DropdownMenuItem(value: option.key, child: Text(option.value))],
                onChanged: (value) => setState(() {
                  _editing = _copy(draft, profileVisibility: value);
                }),
              ),
              DropdownButtonFormField<String>(
                key: const Key('content-visibility'),
                initialValue: draft.contentVisibility,
                decoration: const InputDecoration(labelText: 'Content visible to'),
                items: [for (final option in _visibilityOptions) DropdownMenuItem(value: option.key, child: Text(option.value))],
                onChanged: (value) => setState(() {
                  _editing = _copy(draft, contentVisibility: value);
                }),
              ),
              SwitchListTile(
                key: const Key('allow-analytics'),
                title: const Text('Allow analytics'),
                value: draft.allowAnalytics,
                onChanged: (value) => setState(() {
                  _editing = _copy(draft, allowAnalytics: value);
                }),
              ),
              SwitchListTile(
                key: const Key('allow-marketing'),
                title: const Text('Allow marketing'),
                value: draft.allowMarketing,
                onChanged: (value) => setState(() {
                  _editing = _copy(draft, allowMarketing: value);
                }),
              ),
              ElevatedButton(key: const Key('save-privacy'), onPressed: _save, child: const Text('Save preferences')),
              const Divider(height: 32),
              const Text('Consent history', style: TextStyle(fontWeight: FontWeight.bold)),
              if (data.consents.isEmpty) const Text('No consent changes recorded.'),
              for (final entry in data.consents)
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(entry.consentType),
                  subtitle: Text(entry.granted ? 'Granted' : 'Withdrawn'),
                ),
              const Divider(height: 32),
              OutlinedButton(key: const Key('export-data'), onPressed: _export, child: const Text('Export my data')),
              const SizedBox(height: 8),
              OutlinedButton(
                key: const Key('request-deletion'),
                onPressed: _requestDeletion,
                child: const Text('Request account deletion'),
              ),
            ],
          );
        },
      ),
    );
  }

  PrivacySettings _copy(
    PrivacySettings base, {
    String? profileVisibility,
    String? contentVisibility,
    bool? allowAnalytics,
    bool? allowMarketing,
  }) {
    return PrivacySettings(
      profileVisibility: profileVisibility ?? base.profileVisibility,
      contentVisibility: contentVisibility ?? base.contentVisibility,
      allowAnalytics: allowAnalytics ?? base.allowAnalytics,
      allowMarketing: allowMarketing ?? base.allowMarketing,
    );
  }
}
