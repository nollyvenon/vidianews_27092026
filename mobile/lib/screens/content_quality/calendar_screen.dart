// Content Calendar Screen (Module 61)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../providers/content_quality_providers.dart';

class ContentCalendarScreen extends ConsumerWidget {
  const ContentCalendarScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final now = DateTime.now();
    final endDate = now.add(const Duration(days: 30));
    final params = (start: now, end: endDate);

    final calendarEvents = ref.watch(calendarEventsProvider(params));

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: calendarEvents.when(
        data: (data) => Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Overview Cards
            _buildOverviewSection(data),
            const SizedBox(height: 20),
            // Events List
            _buildEventsList(data),
            const SizedBox(height: 20),
            // AI Insights
            _buildAIInsights(),
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
      ),
    );
  }

  Widget _buildOverviewSection(dynamic data) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      const Text('Scheduled Events', style: TextStyle(fontSize: 12, color: Colors.grey)),
                      const SizedBox(height: 8),
                      Text(
                        data.totalCount.toString(),
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                      const Text('Next 30 days', style: TextStyle(fontSize: 10)),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      const Text('Avg Confidence', style: TextStyle(fontSize: 12, color: Colors.grey)),
                      const SizedBox(height: 8),
                      Text(
                        '${(data.averageConfidence * 100).toStringAsFixed(0)}%',
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                      const Text('AI quality', style: TextStyle(fontSize: 10)),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildEventsList(dynamic data) {
    if (data.events.isEmpty) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            children: [
              Icon(Icons.calendar_today, size: 48, color: Colors.grey[300]),
              const SizedBox(height: 16),
              const Text(
                'No events scheduled',
                style: TextStyle(color: Colors.grey, fontSize: 14),
              ),
              const Text(
                'Create your first event to get started!',
                style: TextStyle(color: Colors.grey, fontSize: 12),
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
            const Text('Upcoming Events', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: data.events.length,
              separatorBuilder: (_, __) => const Divider(),
              itemBuilder: (context, index) {
                final event = data.events[index];
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Text(
                              event.title,
                              style: const TextStyle(fontWeight: FontWeight.bold),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: _getConfidenceColor(event.aiConfidenceScore),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              '${(event.aiConfidenceScore * 100).toStringAsFixed(0)}%',
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
                      Row(
                        children: [
                          Icon(Icons.calendar_today, size: 14, color: Colors.grey),
                          const SizedBox(width: 4),
                          Text(
                            DateFormat('MMM d, HH:mm').format(event.scheduledFor),
                            style: const TextStyle(fontSize: 12, color: Colors.grey),
                          ),
                        ],
                      ),
                      if (event.predictedReach != null) ...[
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            Icon(Icons.trending_up, size: 14, color: Colors.green),
                            const SizedBox(width: 4),
                            Text(
                              'Est. Reach: ${(event.predictedReach! / 1000).toStringAsFixed(1)}K',
                              style: const TextStyle(fontSize: 12, color: Colors.green),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAIInsights() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('AI Insights', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildInsightItem(
              title: 'Best Publishing Time',
              description: 'Based on audience behavior, Tuesday 2-4 PM has the highest engagement rates',
              color: Colors.blue,
            ),
            const SizedBox(height: 12),
            _buildInsightItem(
              title: 'Content Gap',
              description: 'You have 3 days without scheduled content next week',
              color: Colors.green,
            ),
            const SizedBox(height: 12),
            _buildInsightItem(
              title: 'Engagement Opportunity',
              description: 'Trending topics in your niche could boost reach by 35%',
              color: Colors.orange,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInsightItem({
    required String title,
    required String description,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        border: Border(left: BorderSide(color: color, width: 4)),
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
          const SizedBox(height: 4),
          Text(
            description,
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Color _getConfidenceColor(double confidence) {
    if (confidence >= 0.8) return Colors.green;
    if (confidence >= 0.6) return Colors.blue;
    if (confidence >= 0.4) return Colors.orange;
    return Colors.grey;
  }
}
