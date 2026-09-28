import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/user_management_providers.dart';

class SubscriberScreen extends ConsumerStatefulWidget {
  const SubscriberScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<SubscriberScreen> createState() => _SubscriberScreenState();
}

class _SubscriberScreenState extends ConsumerState<SubscriberScreen> {
  late TextEditingController _userIdController;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _userIdController = TextEditingController();
  }

  @override
  void dispose() {
    _userIdController.dispose();
    super.dispose();
  }

  Future<void> _loadSubscriber() async {
    setState(() => _isLoading = true);

    try {
      final userId = int.parse(_userIdController.text);
      final service = ref.read(userManagementServiceProvider);

      final subscriber = await service.createSubscriber(
        userId: userId,
        subscriptionTier: 'premium',
      );

      final engagement = await service.getEngagementScore(subscriber['id']);
      final churnRisk = await service.getChurnRisk(subscriber['id']);

      ref.read(engagementScoreProvider.notifier).state = engagement;
      ref.read(churnRiskProvider.notifier).state = churnRisk;

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Subscriber loaded successfully')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final engagement = ref.watch(engagementScoreProvider);
    final churnRisk = ref.watch(churnRiskProvider);

    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Subscriber Information',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _userIdController,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: 'User ID',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _loadSubscriber,
                        child: _isLoading
                            ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                              ),
                            )
                            : const Text('Load Subscriber'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            // Metrics Cards
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 1.2,
              children: [
                _buildMetricCard(
                  'Engagement Score',
                  '${engagement.toStringAsFixed(1)}%',
                  Colors.green,
                ),
                _buildMetricCard(
                  'Churn Risk',
                  '${(churnRisk * 100).toStringAsFixed(1)}%',
                  Colors.red,
                ),
              ],
            ),
            const SizedBox(height: 24),
            // Activity Log
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Recent Activities',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: 5,
                      itemBuilder: (context, index) {
                        final activities = [
                          'Article Read',
                          'Content Shared',
                          'Comment Posted',
                          'Page Visited',
                          'Newsletter Opened'
                        ];
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 8),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                activities[index],
                                style: const TextStyle(fontSize: 12),
                              ),
                              Text(
                                '${index + 1} day ago',
                                style: TextStyle(
                                  fontSize: 11,
                                  color: Colors.grey[600],
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricCard(String label, String value, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              label,
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
            Text(
              value,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
