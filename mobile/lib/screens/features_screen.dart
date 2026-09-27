import 'package:flutter/material.dart'

class FeaturesScreen extends StatelessWidget {
  const FeaturesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final flags = [
      {'name': 'dark_mode', 'status': 'enabled', 'rollout': '100%'},
      {'name': 'new_ui', 'status': 'rollout', 'rollout': '50%'},
      {'name': 'beta_search', 'status': 'disabled', 'rollout': '0%'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Feature Flags')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Active Flags', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: flags.length,
              itemBuilder: (context, index) {
                final flag = flags[index];
                final statusColor = flag['status'] == 'enabled' ? Colors.green : flag['status'] == 'rollout' ? Colors.blue : Colors.grey;
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(flag['name']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                            Chip(label: Text(flag['status']!))
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text('Rollout: ${flag['rollout']}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
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
