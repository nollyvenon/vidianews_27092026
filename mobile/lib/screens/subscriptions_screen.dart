import 'package:flutter/material.dart'

class SubscriptionsScreen extends StatelessWidget {
  const SubscriptionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Subscriptions')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Card(child: ListTile(title: const Text('Silver'), subtitle: const Text('4.99 per month'))),
            const SizedBox(height: 8),
            Card(child: ListTile(title: const Text('Gold'), subtitle: const Text('9.99 per month'))),
          ],
        ),
      ),
    );
  }
}
