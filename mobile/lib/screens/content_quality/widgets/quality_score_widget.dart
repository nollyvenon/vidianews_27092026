// Quality Score Widget

import 'package:flutter/material.dart';

class QualityScoreWidget extends StatelessWidget {
  final double score;
  final String rating;
  final int totalIssues;
  final int grammarIssues;
  final int spellingIssues;
  final int styleIssues;
  final int? punctuationIssues;

  const QualityScoreWidget({
    Key? key,
    required this.score,
    required this.rating,
    required this.totalIssues,
    required this.grammarIssues,
    required this.spellingIssues,
    required this.styleIssues,
    this.punctuationIssues,
  }) : super(key: key);

  Color _getRatingColor() {
    switch (rating) {
      case 'Excellent':
        return Colors.green;
      case 'Good':
        return Colors.blue;
      case 'Fair':
        return Colors.orange;
      default:
        return Colors.red;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Quality Score',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Column(
                    children: [
                      Text(
                        score.toStringAsFixed(1),
                        style: TextStyle(
                          fontSize: 40,
                          fontWeight: FontWeight.bold,
                          color: _getRatingColor(),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        rating,
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: _getRatingColor(),
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    children: [
                      _buildIssueBadge('Grammar', grammarIssues),
                      const SizedBox(height: 8),
                      _buildIssueBadge('Spelling', spellingIssues),
                      const SizedBox(height: 8),
                      _buildIssueBadge('Style', styleIssues),
                      if (punctuationIssues != null) ...[
                        const SizedBox(height: 8),
                        _buildIssueBadge('Punctuation', punctuationIssues!),
                      ]
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      children: [
                        const Text(
                          'Total Issues',
                          style: TextStyle(fontSize: 12, color: Colors.grey),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          totalIssues.toString(),
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIssueBadge(String label, int count) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(6),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 12)),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: count > 0 ? Colors.orange : Colors.green,
              borderRadius: BorderRadius.circular(4),
            ),
            child: Text(
              count.toString(),
              style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }
}
