import 'package:flutter/material.dart'

class MessagesScreen extends StatelessWidget {
  const MessagesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Messages')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Conversations', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                title: const Text('Sarah Johnson'),
                subtitle: const Text('Thanks for the update'),
                trailing: const Text('2m ago', style: TextStyle(fontSize: 10)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
