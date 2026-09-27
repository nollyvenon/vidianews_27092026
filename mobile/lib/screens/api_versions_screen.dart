import 'package:flutter/material.dart'

class APIVersionsScreen extends StatelessWidget {
  const APIVersionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final versions = [
      {'endpoint': '/api/users', 'version': 'v3', 'usage': '8.5K'},
      {'endpoint': '/api/posts', 'version': 'v2', 'usage': '3.2K'},
      {'endpoint': '/api/content', 'version': 'v1 (deprecated)', 'usage': '120'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('API Versions')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Active Versions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: versions.length,
              itemBuilder: (context, index) {
                final v = versions[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(v['endpoint']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                        const SizedBox(height: 4),
                        Text(v['version']!, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                        const SizedBox(height: 4),
                        Text('Usage: ${v['usage']} calls/day', style: const TextStyle(fontSize: 11)),
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
