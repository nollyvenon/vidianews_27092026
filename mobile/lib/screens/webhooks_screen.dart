import 'package:flutter/material.dart'

class WebhooksScreen extends StatelessWidget {
  const WebhooksScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final webhooks = [
      {'url': 'example.com/hook', 'event': 'user.created', 'status': 'active'},
      {'url': 'api.service.com/events', 'event': 'content.uploaded', 'status': 'active'},
      {'url': 'old-service.com/hook', 'event': 'payment.received', 'status': 'failed'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Webhooks')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Active Webhooks', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: webhooks.length,
              itemBuilder: (context, index) {
                final w = webhooks[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(w['url']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                        const SizedBox(height: 4),
                        Text(w['event']!, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                        const SizedBox(height: 8),
                        Text(
                          w['status']!.toUpperCase(),
                          style: TextStyle(
                            fontSize: 10,
                            color: w['status'] == 'active' ? Colors.green : Colors.red,
                            fontWeight: FontWeight.bold
                          ),
                        ),
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
