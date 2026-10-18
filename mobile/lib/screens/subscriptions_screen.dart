// The account's current subscription, from GET /billing/subscription.

import 'package:flutter/material.dart';
import '../models/billing_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/billing_account_service.dart';

class SubscriptionsScreen extends StatefulWidget {
  final BillingAccountService? service;

  const SubscriptionsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<SubscriptionsScreen> createState() => _SubscriptionsScreenState();
}

class _SubscriptionsScreenState extends State<SubscriptionsScreen> {
  late final BillingAccountService _service = widget.service ?? BillingAccountService(createAuthenticatedDio());
  late Future<AccountSubscription?> _subscription = _service.fetchSubscription();

  void _reload() {
    setState(() {
      _subscription = _service.fetchSubscription();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Subscriptions')),
      body: FutureBuilder<AccountSubscription?>(
        future: _subscription,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return _ErrorView(message: messageFromError(snapshot.error!), onRetry: _reload);
          }
          final subscription = snapshot.data;
          if (subscription == null) {
            return const Center(child: Text('This account has no subscription.'));
          }
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Card(
                child: ListTile(
                  title: Text(subscription.tierLabel),
                  subtitle: Text(_describe(subscription)),
                  trailing: Text(subscription.isActive ? 'Active' : 'Canceled'),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

String _describe(AccountSubscription subscription) {
  final cycle = subscription.billingCycle ?? 'one-time';
  final price = '\$${subscription.amount.toStringAsFixed(2)} · $cycle';
  if (!subscription.isActive) {
    final canceled = subscription.canceledAt;
    return canceled == null ? price : '$price · canceled ${_dateLabel(canceled)}';
  }
  final renews = subscription.renewsAt;
  return renews == null ? price : '$price · renews ${_dateLabel(renews)}';
}

String _dateLabel(DateTime value) => value.toLocal().toString().split(' ').first;

class _ErrorView extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;

  const _ErrorView({required this.message, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 12),
            OutlinedButton(onPressed: onRetry, child: const Text('Try again')),
          ],
        ),
      ),
    );
  }
}
