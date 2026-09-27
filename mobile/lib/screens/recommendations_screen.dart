import 'package:flutter/material.dart'

class RecommendationsScreen extends StatefulWidget {
  const RecommendationsScreen({Key? key}) : super(key: key);

  @override
  State<RecommendationsScreen> createState() => _RecommendationsScreenState();
}

class _RecommendationsScreenState extends State<RecommendationsScreen> {
  final List<Map<String, String>> recommendations = [
    {'title': 'Advanced Flutter Tips', 'reason': 'Based on your interests', 'score': '0.95'},
    {'title': 'React Performance Guide', 'reason': 'Similar to watched videos', 'score': '0.88'},
    {'title': 'Web Security Basics', 'reason': 'Trending in your category', 'score': '0.85'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Recommendations')),
      body: ListView.builder(
        itemCount: recommendations.length,
        itemBuilder: (context, index) {
          final rec = recommendations[index];
          return Card(
            margin: const EdgeInsets.all(8),
            child: ListTile(
              leading: CircleAvatar(
                child: Text(rec['score']!),
              ),
              title: Text(rec['title']!),
              subtitle: Text(rec['reason']!),
              trailing: const Icon(Icons.arrow_forward),
              onTap: () {},
            ),
          );
        },
      ),
    );
  }
}
