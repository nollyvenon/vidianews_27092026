// All invoices for the account, from GET /billing/invoices.

import 'package:flutter/material.dart';
import '../models/billing_account_models.dart';
import '../services/authenticated_dio.dart';
import '../services/billing_account_service.dart';

class InvoicesScreen extends StatefulWidget {
  final BillingAccountService? service;

  const InvoicesScreen({Key? key, this.service}) : super(key: key);

  @override
  State<InvoicesScreen> createState() => _InvoicesScreenState();
}

class _InvoicesScreenState extends State<InvoicesScreen> {
  late final BillingAccountService _service = widget.service ?? BillingAccountService(createAuthenticatedDio());
  late Future<List<AccountInvoice>> _invoices = _service.fetchInvoices();

  void _reload() {
    setState(() {
      _invoices = _service.fetchInvoices();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Invoices')),
      body: FutureBuilder<List<AccountInvoice>>(
        future: _invoices,
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
          final invoices = snapshot.data!;
          if (invoices.isEmpty) {
            return const Center(child: Text('No invoices yet.'));
          }
          final paidTotal = invoices
              .where((invoice) => invoice.isPaid)
              .fold<double>(0, (sum, invoice) => sum + invoice.amount);
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Column(
                        children: [
                          Text(
                            '\$${paidTotal.toStringAsFixed(2)}',
                            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.green),
                          ),
                          const SizedBox(height: 4),
                          const Text('Paid', style: TextStyle(fontSize: 12)),
                        ],
                      ),
                      Column(
                        children: [
                          Text('${invoices.length}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 4),
                          const Text('Invoices', style: TextStyle(fontSize: 12)),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
              for (final invoice in invoices)
                Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    title: Text('Invoice #${invoice.id}'),
                    subtitle: Text(_dateLabel(invoice.createdAt)),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text('\$${invoice.amount.toStringAsFixed(2)}', style: const TextStyle(fontWeight: FontWeight.bold)),
                        Text(
                          invoice.isPaid ? 'Paid' : (invoice.status ?? 'Unknown'),
                          style: TextStyle(fontSize: 10, color: invoice.isPaid ? Colors.green : Colors.orange),
                        ),
                      ],
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

String _dateLabel(DateTime? value) => value == null ? '—' : value.toLocal().toString().split(' ').first;
