import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'subscriber_screen.dart';
import 'segments_screen.dart';
import 'campaigns_screen.dart';
import 'preferences_screen.dart';

class UserManagementScreen extends ConsumerWidget {
  const UserManagementScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('User Management'),
          elevation: 0,
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Subscribers'),
              Tab(text: 'Segments'),
              Tab(text: 'Campaigns'),
              Tab(text: 'Preferences'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            SubscriberScreen(),
            SegmentsScreen(),
            CampaignsScreen(),
            PreferencesScreen(),
          ],
        ),
      ),
    );
  }
}
