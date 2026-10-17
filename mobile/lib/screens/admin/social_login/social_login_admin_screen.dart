// Admin screen: manage OAuth client credentials for social sign-in.

import 'package:flutter/material.dart';
import '../../../models/social_auth_models.dart';
import '../../../services/authenticated_dio.dart';
import '../../../services/social_auth_service.dart';

class SocialLoginAdminScreen extends StatefulWidget {
  final SocialAuthService service;

  const SocialLoginAdminScreen({Key? key, required this.service}) : super(key: key);

  @override
  State<SocialLoginAdminScreen> createState() => _SocialLoginAdminScreenState();
}

class _SocialLoginAdminScreenState extends State<SocialLoginAdminScreen> {
  late Future<List<SocialProviderAdmin>> _providers;

  @override
  void initState() {
    super.initState();
    _providers = widget.service.listProviders();
  }

  void _reload() => setState(() => _providers = widget.service.listProviders());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Social login')),
      body: FutureBuilder<List<SocialProviderAdmin>>(
        future: _providers,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Text(messageFromError(snapshot.error!), textAlign: TextAlign.center),
              ),
            );
          }
          final providers = snapshot.data ?? const <SocialProviderAdmin>[];
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              for (final provider in providers)
                _ProviderCard(
                  key: ValueKey(provider.provider),
                  provider: provider,
                  service: widget.service,
                  onSaved: _reload,
                ),
            ],
          );
        },
      ),
    );
  }
}

class _ProviderCard extends StatefulWidget {
  final SocialProviderAdmin provider;
  final SocialAuthService service;
  final VoidCallback onSaved;

  const _ProviderCard({Key? key, required this.provider, required this.service, required this.onSaved})
      : super(key: key);

  @override
  State<_ProviderCard> createState() => _ProviderCardState();
}

class _ProviderCardState extends State<_ProviderCard> {
  late bool _enabled;
  late final TextEditingController _clientId;
  late final TextEditingController _clientSecret;
  late final TextEditingController _redirectUri;
  late final TextEditingController _scopes;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    final p = widget.provider;
    _enabled = p.enabled;
    _clientId = TextEditingController(text: p.clientId ?? '');
    _clientSecret = TextEditingController();
    _redirectUri = TextEditingController(text: p.redirectUri ?? '');
    _scopes = TextEditingController(text: p.scopes);
  }

  @override
  void dispose() {
    _clientId.dispose();
    _clientSecret.dispose();
    _redirectUri.dispose();
    _scopes.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    final messenger = ScaffoldMessenger.of(context);
    try {
      await widget.service.updateProvider(
        widget.provider.provider,
        SocialProviderUpdate(
          enabled: _enabled,
          clientId: _clientId.text.trim(),
          clientSecret: _clientSecret.text,
          redirectUri: _redirectUri.text.trim(),
          scopes: _scopes.text.trim(),
        ),
      );
      _clientSecret.clear();
      messenger.showSnackBar(SnackBar(content: Text('${widget.provider.displayName} saved')));
      widget.onSaved();
    } catch (error) {
      messenger.showSnackBar(SnackBar(content: Text(messageFromError(error))));
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final p = widget.provider;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(child: Text(p.displayName, style: Theme.of(context).textTheme.titleMedium)),
                Switch(
                  value: _enabled,
                  onChanged: _saving ? null : (value) => setState(() => _enabled = value),
                ),
              ],
            ),
            TextField(
              key: Key('${p.provider}-client-id'),
              controller: _clientId,
              decoration: const InputDecoration(labelText: 'Client ID'),
            ),
            TextField(
              key: Key('${p.provider}-client-secret'),
              controller: _clientSecret,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'Client secret',
                hintText: p.clientSecretSet ? 'Stored. Enter a value to replace it.' : 'Not set',
              ),
            ),
            TextField(
              controller: _redirectUri,
              decoration: const InputDecoration(labelText: 'Redirect URI'),
            ),
            TextField(
              controller: _scopes,
              decoration: const InputDecoration(labelText: 'Scopes'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _saving ? null : _save,
              child: Text(_saving ? 'Saving...' : 'Save'),
            ),
          ],
        ),
      ),
    );
  }
}
