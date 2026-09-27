import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/advanced_features_providers.dart';

class RetentionScreen extends ConsumerWidget {
  const RetentionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final atRiskUsers = ref.watch(atRiskUsersProvider);

    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'User Retention & Churn',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            const Text(
              'At-Risk Users',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            atRiskUsers.when(
              data: (users) => users.isEmpty
                  ? const Card(
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Text('No at-risk users'),
                      ),
                    )
                  : ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: users.length,
                      itemBuilder: (context, index) {
                        final user = users[index];
                        final churnColor = user.churnProbability > 0.8
                            ? Colors.red
                            : user.churnProbability > 0.6
                                ? Colors.orange
                                : Colors.yellow;

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
                                      'User #${user.userId}',
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
                                        color: churnColor.withOpacity(0.2),
                                        border: Border.all(color: churnColor),
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                      child: Text(
                                        user.status,
                                        style: TextStyle(
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                          color: churnColor,
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
                                      'Churn Risk: ${(user.churnProbability * 100).toStringAsFixed(1)}%',
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: churnColor,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    Text(
                                      'Inactive: ${user.daysSinceActive} days',
                                      style: const TextStyle(fontSize: 12),
                                    ),
                                  ],
                                ),
                                if (user.engagementTrend != null)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 8.0),
                                    child: Text(
                                      'Trend: ${user.engagementTrend}',
                                      style: const TextStyle(fontSize: 12),
                                    ),
                                  ),
                                if (user.recommendedAction != null)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 8.0),
                                    child: Chip(
                                      label: Text(user.recommendedAction!),
                                      backgroundColor: Colors.blue.withOpacity(0.2),
                                    ),
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
