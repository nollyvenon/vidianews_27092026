import 'package:flutter/material.dart';
import 'analytics_screen.dart';
import 'behavior_tracking_screen.dart';
import 'search_analytics_screen.dart';
import 'system_health_screen.dart';

class AnalyticsMainScreen extends StatefulWidget {
  const AnalyticsMainScreen({Key? key}) : super(key: key);

  @override
  State<AnalyticsMainScreen> createState() => _AnalyticsMainScreenState();
}

class _AnalyticsMainScreenState extends State<AnalyticsMainScreen> {
  int _currentTabIndex = 0;

  final List<Widget> _screens = [
    const AnalyticsScreen(),
    const BehaviorTrackingScreen(),
    const SearchAnalyticsScreen(),
    const SystemHealthScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analytics & Reporting'),
        elevation: 0,
      ),
      body: _screens[_currentTabIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentTabIndex,
        onTap: (index) {
          setState(() {
            _currentTabIndex = index;
          });
        },
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.analytics),
            label: 'Overview',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.track_changes),
            label: 'Behavior',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.search),
            label: 'Search',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.health_and_safety),
            label: 'Health',
          ),
        ],
      ),
    );
  }
}
