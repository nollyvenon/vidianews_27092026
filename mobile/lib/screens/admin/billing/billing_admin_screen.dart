// Admin screen: subscriptions (change tier, cancel) and transaction history.

import 'package:flutter/material.dart';
import '../../../models/billing_admin_models.dart';
import '../../../services/authenticated_dio.dart';
import '../../../services/billing_admin_service.dart';

const List<String> kSubscriptionTiers = ['free', 'starter', 'pro', 'enterprise'];

class BillingAdminScreen extends StatefulWidget {
  final BillingAdminService service;

  const BillingAdminScreen({Key? key, required this.service}) : super(key: key);

  @override
  State<BillingAdminScreen> createState() => _BillingAdminScreenState();
}

class _BillingAdminScreenState extends State<BillingAdminScreen> {
  late Future<AdminPage<SubscriptionAdmin>> _subscriptions;
  late Future<AdminPage<TransactionAdmin>> _transactions;
  String _source = 'all';

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    _subscriptions = widget.service.listSubscriptions();
    _transactions = widget.service.listTransactions(source: _source);
  }

  void _refresh() => setState(_load);

  Future<void> _changeTier(SubscriptionAdmin sub, String tier) async {
    final messenger = ScaffoldMessenger.of(context);
    try {
      await widget.service.changeTier(sub.id, tier);
      messenger.showSnackBar(SnackBar(content: Text('Tier changed to $tier')));
      _refresh();
    } catch (error) {
      messenger.showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  Future<void> _cancel(SubscriptionAdmin sub) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Cancel subscription?'),
        content: Text('Cancel the subscription for ${sub.userEmail ?? 'this customer'}?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Keep')),
          TextButton(onPressed: () => Navigator.pop(context, true), child: const Text('Cancel subscription')),
        ],
      ),
    );
    if (confirmed != true) return;
    final messenger = ScaffoldMessenger.of(context);
    try {
      await widget.service.cancelSubscription(sub.id);
      messenger.showSnackBar(const SnackBar(content: Text('Subscription canceled')));
      _refresh();
    } catch (error) {
      messenger.showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  void _setSource(String value) {
    setState(() {
      _source = value;
      _transactions = widget.service.listTransactions(source: value);
    });
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Subscriptions & transactions'),
          bottom: const TabBar(tabs: [Tab(text: 'Subscriptions'), Tab(text: 'Transactions')]),
        ),
        body: TabBarView(
          children: [
            _SubscriptionsTab(future: _subscriptions, onChangeTier: _changeTier, onCancel: _cancel),
            Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(12),
                  child: DropdownButton<String>(
                    value: _source,
                    items: const [
                      DropdownMenuItem(value: 'all', child: Text('All sources')),
                      DropdownMenuItem(value: 'subscription', child: Text('Subscriptions')),
                      DropdownMenuItem(value: 'checkout', child: Text('Checkout')),
                    ],
                    onChanged: (value) {
                      if (value != null) _setSource(value);
                    },
                  ),
                ),
                Expanded(child: _TransactionsTab(future: _transactions)),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _SubscriptionsTab extends StatelessWidget {
  final Future<AdminPage<SubscriptionAdmin>> future;
  final Future<void> Function(SubscriptionAdmin, String) onChangeTier;
  final Future<void> Function(SubscriptionAdmin) onCancel;

  const _SubscriptionsTab({required this.future, required this.onChangeTier, required this.onCancel});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<AdminPage<SubscriptionAdmin>>(
      future: future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(child: Text(messageFromError(snapshot.error!)));
        }
        final items = snapshot.data!.items;
        if (items.isEmpty) return const Center(child: Text('No subscriptions found.'));
        return ListView.separated(
          itemCount: items.length,
          separatorBuilder: (_, __) => const Divider(height: 1),
          itemBuilder: (context, index) {
            final sub = items[index];
            return ListTile(
              title: Text(sub.userEmail ?? 'User #${sub.userId}'),
              subtitle: Text(
                '${sub.isActive ? 'Active' : 'Canceled'} · \$${sub.amount.toStringAsFixed(2)} · ${sub.billingCycle ?? ''}',
              ),
              trailing: Wrap(
                spacing: 8,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  DropdownButton<String>(
                    value: kSubscriptionTiers.contains(sub.tier) ? sub.tier : null,
                    hint: const Text('Tier'),
                    items: [
                      for (final tier in kSubscriptionTiers) DropdownMenuItem(value: tier, child: Text(tier)),
                    ],
                    onChanged: (tier) {
                      if (tier != null && tier != sub.tier) onChangeTier(sub, tier);
                    },
                  ),
                  if (sub.isActive)
                    IconButton(
                      tooltip: 'Cancel subscription',
                      icon: const Icon(Icons.cancel_outlined),
                      onPressed: () => onCancel(sub),
                    ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}

class _TransactionsTab extends StatelessWidget {
  final Future<AdminPage<TransactionAdmin>> future;

  const _TransactionsTab({required this.future});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<AdminPage<TransactionAdmin>>(
      future: future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(child: Text(messageFromError(snapshot.error!)));
        }
        final items = snapshot.data!.items;
        if (items.isEmpty) return const Center(child: Text('No transactions found.'));
        return ListView.separated(
          itemCount: items.length,
          separatorBuilder: (_, __) => const Divider(height: 1),
          itemBuilder: (context, index) {
            final tx = items[index];
            return ListTile(
              title: Text('${tx.source} · ${tx.userEmail ?? '—'}'),
              subtitle: Text('${tx.status ?? '—'} · ${tx.reference ?? '—'}'),
              trailing: Text('${tx.currency} ${tx.amount.toStringAsFixed(2)}'),
            );
          },
        );
      },
    );
  }
}
