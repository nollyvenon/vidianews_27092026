// The signed-in member's creator profile, with the bio editor, and the directory of creators.

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

class _CreatorData {
  final CreatorProfile? profile;
  final List<CreatorProfile> creators;

  const _CreatorData({required this.profile, required this.creators});
}

class CreatorScreen extends StatefulWidget {
  final DiscoveryService? service;

  const CreatorScreen({Key? key, this.service}) : super(key: key);

  @override
  State<CreatorScreen> createState() => _CreatorScreenState();
}

class _CreatorScreenState extends State<CreatorScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  final _bioController = TextEditingController();
  bool _verifiedOnly = false;
  late Future<_CreatorData> _data = _load();

  @override
  void dispose() {
    _bioController.dispose();
    super.dispose();
  }

  Future<_CreatorData> _load() async {
    final profile = await _loadProfile();
    final creators = await _service.fetchCreators(verifiedOnly: _verifiedOnly);
    return _CreatorData(profile: profile, creators: creators);
  }

  Future<CreatorProfile?> _loadProfile() async {
    try {
      final profile = await _service.fetchCreatorProfile();
      _bioController.text = profile.bio ?? '';
      return profile;
    } on DioException catch (error) {
      // 404 means no creator profile yet: the member can create one by saving a bio.
      if (error.response?.statusCode == 404) return null;
      rethrow;
    }
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  Future<void> _saveBio() async {
    final bio = _bioController.text.trim();
    if (bio.isEmpty) {
      _notify('Write a short bio first.');
      return;
    }
    try {
      await _service.saveCreatorBio(bio);
      _notify('Creator profile saved.');
      _reload();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  void _notify(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Creator')),
      body: AsyncView<_CreatorData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (data.profile != null)
              Text(
                '${data.profile!.followers} followers${data.profile!.isVerified ? ' · verified' : ''}',
                key: const Key('creator-summary'),
              )
            else
              const Text('You do not have a creator profile yet.'),
            const SizedBox(height: 12),
            TextField(
              key: const Key('bio-field'),
              controller: _bioController,
              maxLines: 3,
              decoration: const InputDecoration(labelText: 'Bio'),
            ),
            ElevatedButton(key: const Key('save-bio'), onPressed: _saveBio, child: const Text('Save bio')),
            const Divider(height: 32),
            SwitchListTile(
              key: const Key('verified-only'),
              contentPadding: EdgeInsets.zero,
              title: const Text('Verified creators only'),
              value: _verifiedOnly,
              onChanged: (value) {
                setState(() => _verifiedOnly = value);
                _reload();
              },
            ),
            if (data.creators.isEmpty) const Text('No creators to show.'),
            for (final creator in data.creators)
              ListTile(
                key: Key('creator-${creator.id}'),
                contentPadding: EdgeInsets.zero,
                leading: const CircleAvatar(child: Icon(Icons.person)),
                title: Text('Creator #${creator.userId}${creator.isVerified ? ' ✓' : ''}'),
                subtitle: Text(creator.bio ?? 'No bio yet'),
                trailing: Text('${creator.followers}'),
              ),
          ],
        ),
      ),
    );
  }
}
