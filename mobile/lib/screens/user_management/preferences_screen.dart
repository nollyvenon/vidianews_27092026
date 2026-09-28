import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/user_management_providers.dart';

class PreferencesScreen extends ConsumerStatefulWidget {
  const PreferencesScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<PreferencesScreen> createState() => _PreferencesScreenState();
}

class _PreferencesScreenState extends ConsumerState<PreferencesScreen> {
  late TextEditingController _userIdController;
  String _selectedReadingLevel = 'intermediate';
  Set<String> _selectedCategories = {'technology', 'business'};
  Set<String> _selectedNotificationChannels = {'email', 'push'};
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

  Future<void> _savePreferences() async {
    if (_userIdController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter user ID')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final userId = int.parse(_userIdController.text);
      final service = ref.read(userManagementServiceProvider);

      // Create personalization profile
      await service.createPersonalizationProfile(
        userId: userId,
        readingLevel: _selectedReadingLevel,
        timezone: 'UTC',
      );

      // Update interests
      await service.updateUserInterests(
        userId: userId,
        keywords: _selectedCategories.toList(),
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Preferences saved successfully')),
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
    final personalizationScore = ref.watch(personalizationScoreProvider);

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
                      'User Preferences',
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
                    const Text(
                      'Reading Level',
                      style: TextStyle(fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 8),
                    DropdownButton<String>(
                      value: _selectedReadingLevel,
                      isExpanded: true,
                      items: ['beginner', 'intermediate', 'advanced']
                          .map((level) => DropdownMenuItem(
                            value: level,
                            child: Text(
                              level[0].toUpperCase() + level.substring(1),
                            ),
                          ))
                          .toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => _selectedReadingLevel = value);
                        }
                      },
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Content Categories',
                      style: TextStyle(fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        'technology',
                        'business',
                        'health',
                        'sports',
                        'entertainment'
                      ]
                          .map((category) => FilterChip(
                            label: Text(category),
                            selected: _selectedCategories.contains(category),
                            onSelected: (selected) {
                              setState(() {
                                if (selected) {
                                  _selectedCategories.add(category);
                                } else {
                                  _selectedCategories.remove(category);
                                }
                              });
                            },
                          ))
                          .toList(),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Notification Channels',
                      style: TextStyle(fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      children: ['email', 'push', 'sms', 'in_app']
                          .map((channel) => FilterChip(
                            label: Text(channel),
                            selected: _selectedNotificationChannels.contains(channel),
                            onSelected: (selected) {
                              setState(() {
                                if (selected) {
                                  _selectedNotificationChannels.add(channel);
                                } else {
                                  _selectedNotificationChannels.remove(channel);
                                }
                              });
                            },
                          ))
                          .toList(),
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _savePreferences,
                        child: _isLoading
                            ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                              ),
                            )
                            : const Text('Save Preferences'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            // Personalization Score
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Personalization Score',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Center(
                      child: Column(
                        children: [
                          Text(
                            '${personalizationScore.toStringAsFixed(1)}%',
                            style: const TextStyle(
                              fontSize: 48,
                              fontWeight: FontWeight.bold,
                              color: Colors.blue,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Profile completeness',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value: personalizationScore / 100,
                        minHeight: 8,
                        backgroundColor: Colors.grey[300],
                        valueColor: AlwaysStoppedAnimation<Color>(
                          personalizationScore > 70 ? Colors.green : Colors.orange,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            // Tips
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Personalization Tips',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    ...[
                      'Complete your profile for better recommendations',
                      'Select more categories to get diverse content',
                      'Adjust notification preferences as needed',
                      'Update reading level for optimized content'
                    ]
                        .map((tip) => Padding(
                          padding: const EdgeInsets.only(bottom: 8),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                '• ',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Expanded(
                                child: Text(
                                  tip,
                                  style: const TextStyle(fontSize: 12),
                                ),
                              ),
                            ],
                          ),
                        ))
                        .toList(),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
