// Premium streaming access: the signed-in user's status and the option to subscribe.

import 'package:flutter/material.dart';
import '../models/social_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/social_account_service.dart';
import '../widgets/async_view.dart';

class PremiumScreen extends StatefulWidget {
  final SocialAccountService? service;

  const PremiumScreen({Key? key, this.service}) : super(key: key);

  @override
  State<PremiumScreen> createState() => _PremiumScreenState();
}

class _PremiumScreenState extends State<PremiumScreen> {
  late final SocialAccountService _service = widget.service ?? SocialAccountService(createAuthenticatedDio());
  late Future<PremiumStatus> _status = _service.fetchPremiumStatus();

  void _reload() {
    setState(() {
      _status = _service.fetchPremiumStatus();
    });
  }

  Future<void> _subscribe() async {
    try {
      await _service.subscribeToPremium();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Premium subscription started.')));
      _reload();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Premium')),
      body: AsyncView<PremiumStatus>(
        future: _status,
        onRetry: _reload,
        builder: (context, status) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              status.isPremium ? 'You have premium access.' : 'You do not have premium access yet.',
              key: const Key('premium-status'),
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            for (final feature in status.features)
              ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.check), title: Text(feature)),
            if (!status.isPremium) ...[
              const SizedBox(height: 16),
              ElevatedButton(key: const Key('subscribe-premium'), onPressed: _subscribe, child: const Text('Subscribe to premium')),
            ],
          ],
        ),
      ),
    );
  }
}
