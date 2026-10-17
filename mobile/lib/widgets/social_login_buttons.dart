// Sign-in buttons for the providers an administrator has enabled.

import 'package:flutter/material.dart';
import '../models/social_auth_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_auth_service.dart';
import '../services/social_sign_in_flow.dart';

class SocialLoginButtons extends StatefulWidget {
  final SocialAuthService service;
  final SocialSignInFlow flow;
  final VoidCallback onSignedIn;

  const SocialLoginButtons({
    Key? key,
    required this.service,
    required this.flow,
    required this.onSignedIn,
  }) : super(key: key);

  @override
  State<SocialLoginButtons> createState() => _SocialLoginButtonsState();
}

class _SocialLoginButtonsState extends State<SocialLoginButtons> {
  late Future<List<SocialProvider>> _providers;
  String? _busyProvider;

  @override
  void initState() {
    super.initState();
    _providers = widget.service.listEnabledProviders();
  }

  Future<void> _signIn(SocialProvider provider) async {
    setState(() => _busyProvider = provider.provider);
    final messenger = ScaffoldMessenger.of(context);
    try {
      await widget.flow.signIn(provider.provider);
      if (mounted) widget.onSignedIn();
    } catch (error) {
      messenger.showSnackBar(SnackBar(content: Text(messageFromError(error))));
    } finally {
      if (mounted) setState(() => _busyProvider = null);
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<SocialProvider>>(
      future: _providers,
      builder: (context, snapshot) {
        // Sign-in is optional: show nothing while loading, on failure, or when no provider is enabled.
        final providers = snapshot.data ?? const <SocialProvider>[];
        if (snapshot.connectionState != ConnectionState.done || providers.isEmpty) {
          return const SizedBox.shrink();
        }
        return Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 24),
            const Row(
              children: [
                Expanded(child: Divider()),
                Padding(padding: EdgeInsets.symmetric(horizontal: 8), child: Text('Or continue with')),
                Expanded(child: Divider()),
              ],
            ),
            const SizedBox(height: 16),
            for (final provider in providers)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: OutlinedButton(
                  key: Key('social-${provider.provider}'),
                  style: OutlinedButton.styleFrom(minimumSize: const Size(double.infinity, 48)),
                  onPressed: _busyProvider != null ? null : () => _signIn(provider),
                  child: Text(
                    _busyProvider == provider.provider
                        ? 'Waiting for browser sign-in...'
                        : 'Continue with ${provider.displayName}',
                  ),
                ),
              ),
          ],
        );
      },
    );
  }
}
