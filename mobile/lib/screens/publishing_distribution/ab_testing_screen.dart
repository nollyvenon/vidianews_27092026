import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/publishing_distribution_providers.dart';

class ABTestingScreen extends ConsumerStatefulWidget {
  const ABTestingScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<ABTestingScreen> createState() => _ABTestingScreenState();
}

class _ABTestingScreenState extends ConsumerState<ABTestingScreen> {
  late TextEditingController _nameController;
  late TextEditingController _metricController;
  late TextEditingController _hypothesisController;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _metricController = TextEditingController();
    _hypothesisController = TextEditingController();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _metricController.dispose();
    _hypothesisController.dispose();
    super.dispose();
  }

  Future<void> _createABTest() async {
    if (_nameController.text.isEmpty ||
        _metricController.text.isEmpty ||
        _hypothesisController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill in all fields')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final service = ref.read(publishingServiceProvider);
      final result = await service.createABTest(
        name: _nameController.text,
        testMetric: _metricController.text,
        hypothesis: _hypothesisController.text,
      );

      ref.read(abTestsProvider.notifier).update((state) => [
        ...state,
        {
          'id': result['id'],
          'name': _nameController.text,
          'status': 'active',
        }
      ]);

      _nameController.clear();
      _metricController.clear();
      _hypothesisController.clear();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('A/B test created successfully')),
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
    final tests = ref.watch(abTestsProvider);

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
                      'Create A/B Test Campaign',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _nameController,
                      decoration: InputDecoration(
                        labelText: 'Test Name',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _metricController,
                      decoration: InputDecoration(
                        labelText: 'Test Metric (e.g., CTR, Engagement)',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _hypothesisController,
                      decoration: InputDecoration(
                        labelText: 'Hypothesis',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      maxLines: 3,
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _createABTest,
                        child: _isLoading
                            ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                              ),
                            )
                            : const Text('Create Test'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Active Tests (${tests.length})',
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            tests.isEmpty
                ? Center(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 32),
                    child: Text(
                      'No active A/B tests',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ),
                )
                : ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: tests.length,
                  itemBuilder: (context, index) {
                    final test = tests[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    test['name'] ?? 'Unnamed Test',
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w600,
                                      fontSize: 14,
                                    ),
                                  ),
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 8,
                                    vertical: 4,
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.blue[100],
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(
                                    test['status'] ?? 'active',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: Colors.blue[900],
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),
                            // Variant Comparison
                            _buildVariantComparison('Control', 4.2, 2.1),
                            const SizedBox(height: 8),
                            _buildVariantComparison('Variant A', 4.8, 2.5),
                            const SizedBox(height: 12),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 12,
                                vertical: 8,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.green[100],
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  const Text(
                                    'Variant A is winning',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  Text(
                                    '+14.3%',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w600,
                                      color: Colors.green[800],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
          ],
        ),
      ),
    );
  }

  Widget _buildVariantComparison(String label, double ctr, double conversion) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Text(
            label,
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
          ),
        ),
        Text(
          'CTR: ${ctr.toStringAsFixed(1)}%',
          style: const TextStyle(fontSize: 11),
        ),
        const SizedBox(width: 12),
        Text(
          'Conv: ${conversion.toStringAsFixed(1)}%',
          style: const TextStyle(fontSize: 11),
        ),
      ],
    );
  }
}
