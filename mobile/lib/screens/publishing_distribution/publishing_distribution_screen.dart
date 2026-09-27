// Publishing & Distribution Screen (Modules 66-70)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'publishing_screen.dart';
import 'analytics_screen.dart';
import 'ab_testing_screen.dart';
import 'recommendations_screen.dart';

class PublishingDistributionScreen extends ConsumerWidget {
  const PublishingDistributionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Publishing & Distribution'),
          elevation: 0,
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Publishing'),
              Tab(text: 'Analytics'),
              Tab(text: 'A/B Tests'),
              Tab(text: 'Recommendations'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            PublishingScreen(),
            AnalyticsScreen(),
            ABTestingScreen(),
            RecommendationsScreen(),
          ],
        ),
      ),
    );
  }
}
