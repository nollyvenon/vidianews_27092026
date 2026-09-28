// Issue List Widget

import 'package:flutter/material.dart';
import '../../../models/content_quality_models.dart';

class IssueListWidget extends StatelessWidget {
  final List<ProofreadingIssue> issues;

  const IssueListWidget({
    Key? key,
    required this.issues,
  }) : super(key: key);

  Color _getSeverityColor(String severity) {
    switch (severity) {
      case 'error':
        return Colors.red;
      case 'warning':
        return Colors.orange;
      case 'info':
        return Colors.blue;
      default:
        return Colors.grey;
    }
  }

  IconData _getSeverityIcon(String severity) {
    switch (severity) {
      case 'error':
        return Icons.error;
      case 'warning':
        return Icons.warning;
      case 'info':
        return Icons.info;
      default:
        return Icons.check_circle;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (issues.isEmpty) {
      return Card(
        color: Colors.green[50],
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(Icons.check_circle, color: Colors.green[700]),
              const SizedBox(width: 12),
              const Text(
                'No issues found!',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),
      );
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Issues Found (${issues.length})',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: issues.length,
              separatorBuilder: (_, __) => const Divider(),
              itemBuilder: (context, index) {
                final issue = issues[index];
                return _buildIssueItem(issue);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIssueItem(ProofreadingIssue issue) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                _getSeverityIcon(issue.severity),
                color: _getSeverityColor(issue.severity),
                size: 20,
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  issue.issueType.replaceAll('_', ' ').toUpperCase(),
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: _getSeverityColor(issue.severity),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  issue.severity,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.grey[100],
              borderRadius: BorderRadius.circular(4),
            ),
            child: Text(
              '"${issue.text}"',
              style: const TextStyle(fontStyle: FontStyle.italic),
            ),
          ),
          const SizedBox(height: 8),
          RichText(
            text: TextSpan(
              children: [
                const TextSpan(
                  text: 'Suggested: ',
                  style: TextStyle(color: Colors.grey, fontSize: 12),
                ),
                TextSpan(
                  text: issue.suggestion,
                  style: const TextStyle(
                    color: Colors.blue,
                    fontWeight: FontWeight.bold,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
