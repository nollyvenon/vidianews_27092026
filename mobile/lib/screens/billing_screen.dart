// Billing overview: the current plan and the most recent invoices, from GET /billing/*.

import 'package:flutter/material.dart';
import '../models/billing_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/billing_account_service.dart';

class BillingScreen extends StatefulWidget {
  final BillingAccountService? service;

  const BillingScreen({Key? key, this.service}) : super(key: key);

  @override
  State<BillingScreen> createState() => _BillingScreenState();
}

class _BillingScreenState extends State<BillingScreen> {
  late final BillingAccountService _service = widget.service ?? BillingAccountService(createAuthenticatedDio());
  late Future<_BillingOverview> _overview = _load();

  Future<_BillingOverview> _load() async {
    final subscription = await _service.fetchSubscription();
    final invoices = await _service.fetchInvoices();
    return _BillingOverview(subscription: subscription, invoices: invoices.take(5).toList());
  }

  void _reload() {
    setState(() {
      _overview = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Billing')),
      body: FutureBuilder<_BillingOverview>(
        future: _overview,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(messageFromError(snapshot.error!), textAlign: TextAlign.center),
                    const SizedBox(height: 12),
                    OutlinedButton(onPressed: _reload, child: const Text('Try again')),
                  ],
                ),
              ),
            );
          }
          final overview = snapshot.data!;
          final subscription = overview.subscription;
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Current plan', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Text(
                        subscription == null ? 'No plan' : subscription.tierLabel,
                        style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.blue),
                      ),
                      if (subscription != null) ...[
                        const SizedBox(height: 4),
                        Text('\$${subscription.amount.toStringAsFixed(2)} · ${subscription.billingCycle ?? 'one-time'}'),
                      ],
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const Text('Recent invoices', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              if (overview.invoices.isEmpty)
                const Text('No invoices yet.')
              else
                for (final invoice in overview.invoices)
                  Card(
                    child: ListTile(
                      title: Text('Invoice #${invoice.id}'),
                      subtitle: Text('\$${invoice.amount.toStringAsFixed(2)}'),
                      trailing: Text(
                        invoice.isPaid ? 'Paid' : (invoice.status ?? 'Unknown'),
                        style: TextStyle(color: invoice.isPaid ? Colors.green : Colors.orange),
                      ),
                    ),
                  ),
            ],
          );
        },
      ),
    );
  }
}

class _BillingOverview {
  final AccountSubscription? subscription;
  final List<AccountInvoice> invoices;

  const _BillingOverview({required this.subscription, required this.invoices});
}
