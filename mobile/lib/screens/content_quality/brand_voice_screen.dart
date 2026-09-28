// Brand Voice Consistency Screen (Module 65)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/content_quality_providers.dart';

class BrandVoiceScreen extends ConsumerWidget {
  const BrandVoiceScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = ref.watch(brandVoiceContentProvider);

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
                    'Check Brand Voice',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Verify your content aligns with brand guidelines and tone',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    onChanged: (value) {
                      ref.read(brandVoiceContentProvider.notifier).state = value;
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
                        ref.refresh(brandVoiceProvider(content));
                      },
                      child: const Padding(
                        padding: EdgeInsets.symmetric(vertical: 12),
                        child: Text('Check Brand Voice'),
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
    final result = ref.watch(brandVoiceProvider(content));

    return result.when(
      data: (data) => Column(
        children: [
          // Alignment Overview
          Card(
            color: _getAlignmentColor(data.brandAlignment),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Brand Voice Alignment',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              data.consistencyScore.toStringAsFixed(1),
                              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                            ),
                            const Text('Consistency Score'),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              data.brandAlignment,
                              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                            ),
                            Text('${data.compliancePercentage.toStringAsFixed(1)}% compliant'),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: data.compliancePercentage / 100,
                      minHeight: 8,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Violation Summary
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Violation Summary',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildViolationBox('Tone', data.toneViolations, Colors.orange),
                      _buildViolationBox('Style', data.styleViolations, Colors.blue),
                      _buildViolationBox('Terminology', data.terminologyViolations, Colors.red),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          // Issues Found
          if (data.violations.isNotEmpty)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Issues Found (${data.violations.length})',
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    ListView.separated(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: data.violations.length,
                      separatorBuilder: (_, __) => const Divider(),
                      itemBuilder: (context, index) {
                        final violation = data.violations[index];
                        return Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(
                                  _getSeverityIcon(violation.severity),
                                  color: _getSeverityColor(violation.severity),
                                  size: 18,
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    violation.violationType,
                                    style: const TextStyle(fontWeight: FontWeight.bold),
                                  ),
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: _getSeverityColor(violation.severity),
                                    borderRadius: BorderRadius.circular(3),
                                  ),
                                  child: Text(
                                    violation.severity,
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
                            Text(
                              violation.description,
                              style: const TextStyle(fontSize: 12, color: Colors.grey),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Suggestion: ${violation.suggestedFix}',
                              style: const TextStyle(
                                fontSize: 12,
                                color: Colors.blue,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ],
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

  Color _getAlignmentColor(String alignment) {
    switch (alignment) {
      case 'Excellent':
        return Colors.green[700] ?? Colors.green;
      case 'Good':
        return Colors.blue[700] ?? Colors.blue;
      case 'Fair':
        return Colors.orange[700] ?? Colors.orange;
      default:
        return Colors.red[700] ?? Colors.red;
    }
  }

  Widget _buildViolationBox(String label, int count, Color color) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            count.toString(),
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color),
          ),
        ),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }

  Color _getSeverityColor(String severity) {
    switch (severity) {
      case 'critical':
        return Colors.red;
      case 'high':
        return Colors.orange;
      case 'medium':
        return Colors.yellow[700] ?? Colors.yellow;
      default:
        return Colors.blue;
    }
  }

  IconData _getSeverityIcon(String severity) {
    switch (severity) {
      case 'critical':
      case 'high':
        return Icons.error;
      case 'medium':
        return Icons.warning;
      default:
        return Icons.info;
    }
  }
}
