import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/advanced_features_providers.dart';

class RecommendationsScreen extends ConsumerWidget {
  const RecommendationsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userId = 1;
    final recommendations = ref.watch(recommendationsProvider(userId));
    final effectiveness = ref.watch(recommendationEffectivenessProvider(userId));

    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Personalized Recommendations',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            effectiveness.when(
              data: (stats) => Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Performance Metrics',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 16),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${stats.totalRecommendations}',
                                style: const TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blue,
                                ),
                              ),
                              const Text(
                                'Total',
                                style: TextStyle(fontSize: 12, color: Colors.grey),
                              ),
                            ],
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${(stats.clickThroughRate * 100).toStringAsFixed(1)}%',
                                style: const TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.green,
                                ),
                              ),
                              const Text(
                                'CTR',
                                style: TextStyle(fontSize: 12, color: Colors.grey),
                              ),
                            ],
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${(stats.conversionRate * 100).toStringAsFixed(1)}%',
                                style: const TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.orange,
                                ),
                              ),
                              const Text(
                                'Conversion',
                                style: TextStyle(fontSize: 12, color: Colors.grey),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Text('Error: $err'),
            ),
            const SizedBox(height: 24),
            const Text(
              'Recommended Content',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            recommendations.when(
              data: (recs) => recs.isEmpty
                  ? const Card(
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Text('No recommendations available'),
                      ),
                    )
                  : ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: recs.length,
                      itemBuilder: (context, index) {
                        final rec = recs[index];
                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: Padding(
                            padding: const EdgeInsets.all(12.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      'Content #${rec.contentId}',
                                      style: const TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 14,
                                      ),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 8,
                                        vertical: 4,
                                      ),
                                      decoration: BoxDecoration(
                                        color: Colors.blue.withOpacity(0.2),
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                      child: Text(
                                        rec.type,
                                        style: const TextStyle(
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.blue,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      'Relevance: ${(rec.relevanceScore * 100).toStringAsFixed(0)}%',
                                      style: const TextStyle(fontSize: 12),
                                    ),
                                    Text(
                                      'Similarity: ${(rec.similarityScore * 100).toStringAsFixed(0)}%',
                                      style: const TextStyle(fontSize: 12),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Chip(
                                      label: Text(rec.clicked ? 'Clicked' : 'Not clicked'),
                                      backgroundColor: rec.clicked ? Colors.green.withOpacity(0.2) : Colors.grey.withOpacity(0.2),
                                    ),
                                    Chip(
                                      label: Text(rec.conversion ? 'Converted' : 'No conversion'),
                                      backgroundColor: rec.conversion ? Colors.orange.withOpacity(0.2) : Colors.grey.withOpacity(0.2),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Text('Error: $err'),
            ),
          ],
        ),
      ),
    );
  }
}
