import 'package:flutter/material.dart'

class InvoicesScreen extends StatelessWidget {
  const InvoicesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final invoices = [
      {'id': 'INV-001', 'date': '2026-09-27', 'amount': '\$99.00', 'status': 'Paid'},
      {'id': 'INV-002', 'date': '2026-08-27', 'amount': '\$99.00', 'status': 'Paid'},
      {'id': 'INV-003', 'date': '2026-07-27', 'amount': '\$99.00', 'status': 'Paid'},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Invoices')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Column(
                      children: const [
                        Text('\$297', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.green)),
                        SizedBox(height: 4),
                        Text('Total Revenue', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                    Column(
                      children: const [
                        Text('3', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Invoices', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Recent Invoices', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: invoices.length,
              itemBuilder: (context, index) {
                final inv = invoices[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    title: Text(inv['id']!),
                    subtitle: Text(inv['date']!),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(inv['amount']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                        Text(inv['status']!, style: const TextStyle(fontSize: 10, color: Colors.green)),
                      ],
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
