import 'package:flutter/material.dart'

class ModerationScreen extends StatelessWidget {
  const ModerationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Moderation')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Pending Reports', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                title: const Text('Inappropriate content'),
                subtitle: const Text('Offensive language'),
                trailing: const Chip(label: Text('PENDING')),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
