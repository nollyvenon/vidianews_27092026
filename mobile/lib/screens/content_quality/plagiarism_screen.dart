// Plagiarism Detection Screen (Module 63)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../providers/content_quality_providers.dart';

class PlagiarismScreen extends ConsumerWidget {
  const PlagiarismScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = ref.watch(plagiarismContentProvider);

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
                    'Check Plagiarism',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Analyze your content for plagiarism and originality',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    onChanged: (value) {
                      ref.read(plagiarismContentProvider.notifier).state = value;
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
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: content.trim().isEmpty ? null : () {
                        ref.refresh(plagiarismProvider(content));
                      },
                      child: const Padding(
                        padding: EdgeInsets.symmetric(vertical: 12),
                        child: Text('Check Plagiarism'),
                      ),
                    ),
                  ),
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

  Widget _buildResultsSection(WidgetRef ref, String content) {
    final result = ref.watch(plagiarismProvider(content));

    return result.when(
      data: (data) => Column(
        children: [
          // Risk Assessment
          Card(
            color: _getRiskColor(data.plagiarismRisk),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Plagiarism Assessment',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      Icon(
                        _getRiskIcon(data.plagiarismRisk),
                        color: Colors.white70,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              '${data.similarityPercentage.toStringAsFixed(1)}%',
                              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                            ),
                            const Text('Similarity'),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              '${data.originalityPercentage.toStringAsFixed(1)}%',
                              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                            ),
                            const Text('Originality'),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: Colors.white12,
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(data.plagiarismRisk),
                            ),
                            const Text('Risk Level'),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: data.similarityPercentage / 100,
                      minHeight: 8,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          children: [
                            Text('${data.humanContentPercentage.toStringAsFixed(1)}%'),
                            const Text('Human', style: TextStyle(fontSize: 12)),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          children: [
                            Text('${data.aiContentPercentage.toStringAsFixed(1)}%'),
                            const Text('AI Content', style: TextStyle(fontSize: 12)),
                          ],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Matched Sources
          if (data.totalSourcesFound > 0)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Matched Sources (${data.totalSourcesFound})',
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    ListView.separated(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: data.detectedSources.length,
                      separatorBuilder: (_, __) => const Divider(),
                      itemBuilder: (context, index) {
                        final source = data.detectedSources[index];
                        return ListTile(
                          title: Text(
                            source.url,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(fontSize: 12),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              LinearProgressIndicator(
                                value: source.similarityPercent / 100,
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Similarity: ${source.similarityPercent.toStringAsFixed(1)}%',
                                style: const TextStyle(fontSize: 11),
                              ),
                            ],
                          ),
                          trailing: IconButton(
                            icon: const Icon(Icons.open_in_browser),
                            onPressed: () => _launchUrl(source.url),
                          ),
                          contentPadding: EdgeInsets.zero,
                        );
                      },
                    ),
                  ],
                ),
              ),
            ),
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
              Text(err.toString(), style: const TextStyle(color: Colors.red, fontSize: 12)),
            ],
          ),
        ),
      ),
    );
  }

  Color _getRiskColor(String risk) {
    switch (risk) {
      case 'Low':
        return Colors.green;
      case 'Medium':
        return Colors.yellow[700] ?? Colors.yellow;
      case 'High':
        return Colors.orange;
      case 'Critical':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  IconData _getRiskIcon(String risk) {
    switch (risk) {
      case 'Low':
        return Icons.check_circle;
      case 'Medium':
        return Icons.warning;
      case 'High':
      case 'Critical':
        return Icons.error;
      default:
        return Icons.info;
    }
  }

  Future<void> _launchUrl(String url) async {
    if (await canLaunchUrl(Uri.parse(url))) {
      await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
    }
  }
}
