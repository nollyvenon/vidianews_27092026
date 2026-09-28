// Readability Analysis Screen (Module 64)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/content_quality_providers.dart';

class ReadabilityScreen extends ConsumerWidget {
  const ReadabilityScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = ref.watch(readabilityContentProvider);

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
                    'Analyze Readability',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Check readability metrics and complexity of your content',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    onChanged: (value) {
                      ref.read(readabilityContentProvider.notifier).state = value;
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
                        ref.refresh(readabilityProvider(content));
                      },
                      child: const Padding(
                        padding: EdgeInsets.symmetric(vertical: 12),
                        child: Text('Check Readability'),
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
    final result = ref.watch(readabilityProvider(content));

    return result.when(
      data: (data) => Column(
        children: [
          // Readability Level Card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Readability Level',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              data.readabilityLevel,
                              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              data.targetAudienceGradeLevel,
                              style: const TextStyle(fontSize: 12, color: Colors.grey),
                            ),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              data.complexityScore.toStringAsFixed(0),
                              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                            ),
                            const SizedBox(height: 4),
                            const Text(
                              'Complexity Score',
                              style: TextStyle(fontSize: 12, color: Colors.grey),
                            ),
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
          // Readability Metrics
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Readability Metrics',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  _buildMetricCard('Flesch Reading Ease', data.fleschReadingEase.toStringAsFixed(1), '0-100'),
                  const SizedBox(height: 12),
                  _buildMetricCard('Flesch-Kincaid Grade', data.fleschKincaidGrade.toStringAsFixed(1), 'Grade Level'),
                  const SizedBox(height: 12),
                  _buildMetricCard('Gunning Fog Index', data.gunningFogIndex.toStringAsFixed(1), 'Grade Level'),
                  const SizedBox(height: 12),
                  _buildMetricCard('SMOG Index', data.smogIndex.toStringAsFixed(1), 'Grade Level'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Content Statistics
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Content Statistics',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildStatBox('Words', data.wordCount.toString()),
                      _buildStatBox('Sentences', data.sentenceCount.toString()),
                      _buildStatBox('Paragraphs', data.paragraphCount.toString()),
                    ],
                  ),
                  const SizedBox(height: 16),
                  ListTile(
                    title: const Text('Average Word Length'),
                    subtitle: Text('${data.avgWordLength.toStringAsFixed(1)} characters per word'),
                    contentPadding: EdgeInsets.zero,
                  ),
                  ListTile(
                    title: const Text('Average Sentence Length'),
                    subtitle: Text('${data.avgSentenceLength.toStringAsFixed(1)} words per sentence'),
                    contentPadding: EdgeInsets.zero,
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

  Widget _buildMetricCard(String title, String value, String unit) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey[300]!),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(fontSize: 12, color: Colors.grey)),
              const SizedBox(height: 4),
              Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
          Text(unit, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        ],
      ),
    );
  }

  Widget _buildStatBox(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      ],
    );
  }
}
