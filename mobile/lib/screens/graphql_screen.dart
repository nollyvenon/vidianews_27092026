import 'package:flutter/material.dart'

class GraphQLScreen extends StatelessWidget {
  const GraphQLScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final queries = [
      {'name': 'GetUser', 'executions': '12.5K', 'time': '25ms'},
      {'name': 'GetPosts', 'executions': '8.4K', 'time': '45ms'},
      {'name': 'GetComments', 'executions': '5.2K', 'time': '18ms'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('GraphQL')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Popular Queries', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: queries.length,
              itemBuilder: (context, index) {
                final q = queries[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    title: Text(q['name']!),
                    subtitle: Text('${q['executions']} executions • ${q['time']} avg'),
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
