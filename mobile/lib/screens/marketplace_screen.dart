import 'package:flutter/material.dart'

class MarketplaceScreen extends StatelessWidget {
  const MarketplaceScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final creators = [
      {'name': 'Tech Reviews', 'earnings': '\$5.2K', 'followers': '12.4K', 'rating': '4.8'},
      {'name': 'Lifestyle Vlog', 'earnings': '\$3.8K', 'followers': '8.9K', 'rating': '4.6'},
      {'name': 'Gaming Pro', 'earnings': '\$7.1K', 'followers': '25.6K', 'rating': '4.9'},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Creator Marketplace')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Top Creators', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: creators.length,
              itemBuilder: (context, index) {
                final creator = creators[index];
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
                            Text(creator['name']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                            Text(creator['earnings']!, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text('👥 ${creator['followers']}', style: const TextStyle(fontSize: 12)),
                            Text('⭐ ${creator['rating']}/5', style: const TextStyle(fontSize: 12)),
                          ],
                        ),
                        const SizedBox(height: 12),
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton(
                            onPressed: () {},
                            child: const Text('View Profile'),
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
