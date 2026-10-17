import 'package:flutter/material.dart';

/// Summary card for a content-quality check: overall score, rating, and issue counts by category.
class QualityScoreWidget extends StatelessWidget {
  final double score;
  final String rating;
  final int totalIssues;
  final int grammarIssues;
  final int spellingIssues;
  final int styleIssues;

  const QualityScoreWidget({
    super.key,
    required this.score,
    required this.rating,
    required this.totalIssues,
    required this.grammarIssues,
    required this.spellingIssues,
    required this.styleIssues,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Quality score: ${score.toStringAsFixed(1)}',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 4),
            Text('Rating: $rating'),
            const SizedBox(height: 8),
            Text(
              'Issues: $totalIssues '
              '(grammar $grammarIssues, spelling $spellingIssues, style $styleIssues)',
            ),
          ],
        ),
      ),
    );
  }
}
