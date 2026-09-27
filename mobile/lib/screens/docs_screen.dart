import 'package:flutter/material.dart'

class DocsScreen extends StatelessWidget {
  const DocsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final docs = [
      {'title': 'Getting Started', 'type': 'guide', 'views': '1.2K'},
      {'title': 'API Reference', 'type': 'reference', 'views': '3.4K'},
      {'title': 'Authentication', 'type': 'guide', 'views': '890'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Documentation')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Published Docs', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: docs.length,
              itemBuilder: (context, index) {
                final doc = docs[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(doc['title']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                        const SizedBox(height: 4),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(doc['type']!, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                            Text('${doc['views']} views', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                          ],
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
