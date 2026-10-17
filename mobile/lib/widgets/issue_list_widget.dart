import 'package:flutter/material.dart';

import '../models/content_quality_models.dart';

/// Lists proofreading issues with their type, severity, the flagged text, and the suggested fix.
class IssueListWidget extends StatelessWidget {
  final List<ProofreadingIssue> issues;

  const IssueListWidget({super.key, required this.issues});

  @override
  Widget build(BuildContext context) {
    if (issues.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(16),
        child: Text('No issues found'),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (final issue in issues)
          Card(
            child: ListTile(
              leading: Icon(
                issue.severity == 'high' ? Icons.error : Icons.warning_amber,
                color: issue.severity == 'high' ? Colors.red : Colors.orange,
              ),
              title: Text('${issue.issueType}: "${issue.text}"'),
              subtitle: Text('Suggestion: ${issue.suggestion}'),
            ),
          ),
      ],
    );
  }
}
