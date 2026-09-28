// Proofreading Analysis Screen (Module 62)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/content_quality_providers.dart';
import 'widgets/quality_score_widget.dart';
import 'widgets/issue_list_widget.dart';

class ProofreadingScreen extends ConsumerWidget {
  const ProofreadingScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = ref.watch(proofreadingContentProvider);
    final options = ref.watch(proofreadingOptionsProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Input Section
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Check Content',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Paste your content to check for grammar, spelling, and style issues',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    onChanged: (value) {
                      ref.read(proofreadingContentProvider.notifier).state = value;
                    },
                    maxLines: 6,
                    decoration: InputDecoration(
                      hintText: 'Paste your content here...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  _buildCheckOptions(ref, options),
                  const SizedBox(height: 16),
                  _buildCheckButton(ref, content),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          // Results Section
          if (content.isNotEmpty)
            _buildResultsSection(ref, content),
        ],
      ),
    );
  }

  Widget _buildCheckOptions(WidgetRef ref, dynamic options) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Check Options', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        CheckboxListTile(
          value: options.grammar,
          onChanged: (value) {
            ref.read(proofreadingOptionsProvider.notifier).state = (
              grammar: value ?? true,
              spelling: options.spelling,
              style: options.style,
            );
          },
          title: const Text('Grammar'),
          contentPadding: EdgeInsets.zero,
          dense: true,
        ),
        CheckboxListTile(
          value: options.spelling,
          onChanged: (value) {
            ref.read(proofreadingOptionsProvider.notifier).state = (
              grammar: options.grammar,
              spelling: value ?? true,
              style: options.style,
            );
          },
          title: const Text('Spelling'),
          contentPadding: EdgeInsets.zero,
          dense: true,
        ),
        CheckboxListTile(
          value: options.style,
          onChanged: (value) {
            ref.read(proofreadingOptionsProvider.notifier).state = (
              grammar: options.grammar,
              spelling: options.spelling,
              style: value ?? true,
            );
          },
          title: const Text('Style'),
          contentPadding: EdgeInsets.zero,
          dense: true,
        ),
      ],
    );
  }

  Widget _buildCheckButton(WidgetRef ref, String content) {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: content.trim().isEmpty ? null : () {
          ref.refresh(proofreadingProvider(content));
        },
        child: const Padding(
          padding: EdgeInsets.symmetric(vertical: 12),
          child: Text('Check Proofreading'),
        ),
      ),
    );
  }

  Widget _buildResultsSection(WidgetRef ref, String content) {
    final result = ref.watch(proofreadingProvider(content));

    return result.when(
      data: (data) => Column(
        children: [
          QualityScoreWidget(
            score: data.qualityScore,
            rating: data.overallRating,
            totalIssues: data.totalIssues,
            grammarIssues: data.grammarIssues,
            spellingIssues: data.spellingIssues,
            styleIssues: data.styleIssues,
          ),
          const SizedBox(height: 16),
          IssueListWidget(issues: data.issues ?? []),
        ],
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Card(
        color: Colors.red[50],
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Error', style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text(err.toString(), style: const TextStyle(color: Colors.red)),
            ],
          ),
        ),
      ),
    );
  }
}
