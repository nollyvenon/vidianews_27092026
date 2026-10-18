import 'package:flutter/material.dart';
import 'package:aether_cms/screens/content/content_list_screen.dart';
import 'package:aether_cms/screens/ai/chat_screen.dart';
import 'package:aether_cms/screens/ai/monitoring_screen.dart';
import 'package:aether_cms/screens/analytics/analytics_main_screen.dart';
import 'package:aether_cms/screens/features_menu_screen.dart';
import 'package:aether_cms/services/authenticated_dio.dart';
import 'package:aether_cms/services/dashboard_service.dart';
import 'package:aether_cms/widgets/async_view.dart';

class HomeScreen extends StatefulWidget {
  final DashboardService? dashboardService;

  const HomeScreen({Key? key, this.dashboardService}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  late final DashboardService _dashboard = widget.dashboardService ?? DashboardService(createAuthenticatedDio());

  @override
  Widget build(BuildContext context) {
    final screens = <Widget>[
      _DashboardScreen(service: _dashboard),
      const ContentListScreen(),
      const ChatScreen(),
      const MonitoringScreen(),
    ];
    return Scaffold(
      appBar: AppBar(
        title: const Text('VidiNews'),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.apps),
            tooltip: 'All features',
            onPressed: () => Navigator.of(context).push(MaterialPageRoute<void>(
              builder: (_) => const FeaturesMenuScreen(),
            )),
          ),
        ],
      ),
      body: screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.video_library), label: 'Content'),
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Chat'),
          BottomNavigationBarItem(icon: Icon(Icons.analytics), label: 'Monitor'),
        ],
      ),
    );
  }
}

class _DashboardScreen extends StatefulWidget {
  final DashboardService service;

  const _DashboardScreen({required this.service});

  @override
  State<_DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<_DashboardScreen> {
  late Future<_DashboardData> _data = _load();

  Future<_DashboardData> _load() async {
    final summary = await widget.service.fetchSummary();
    final activity = await widget.service.fetchRecentActivity();
    return _DashboardData(summary: summary, activity: activity);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  void _open(BuildContext context, Widget screen) {
    Navigator.of(context).push(MaterialPageRoute<void>(builder: (_) => screen));
  }

  @override
  Widget build(BuildContext context) {
    return AsyncView<_DashboardData>(
      future: _data,
      onRetry: _reload,
      builder: (context, data) => SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Welcome Back!',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              children: [
                _StatCard(icon: Icons.video_library, label: '${data.summary.videos} Videos', color: Colors.blue),
                _StatCard(icon: Icons.article, label: '${data.summary.articles} Articles', color: Colors.green),
                _StatCard(icon: Icons.chat, label: '${data.summary.chats} Chats', color: Colors.purple),
                _StatCard(
                  icon: Icons.attach_money,
                  label: '\$${data.summary.monthlySpend.toStringAsFixed(2)} Spent this month',
                  color: Colors.orange,
                ),
              ],
            ),
            const SizedBox(height: 32),
            const Text(
              'Quick Actions',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            _QuickActionTile(
              icon: Icons.video_library,
              title: 'Manage Content',
              subtitle: 'Videos & Articles',
              onTap: () => _open(context, const ContentListScreen()),
            ),
            _QuickActionTile(
              icon: Icons.chat,
              title: 'AI Chat',
              subtitle: 'Ask AI questions',
              onTap: () => _open(context, const ChatScreen()),
            ),
            _QuickActionTile(
              icon: Icons.analytics,
              title: 'Analytics',
              subtitle: 'View metrics',
              onTap: () => _open(context, const AnalyticsMainScreen()),
            ),
            const SizedBox(height: 32),
            const Text(
              'Recent Activity',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            if (data.activity.isEmpty) const Text('No recent activity yet.'),
            for (final entry in data.activity)
              ListTile(
                key: Key('activity-${entry.id}'),
                contentPadding: EdgeInsets.zero,
                title: Text(entry.description ?? entry.action),
                subtitle: Text(entry.createdAt.toLocal().toString()),
              ),
          ],
        ),
      ),
    );
  }
}

class _DashboardData {
  final DashboardSummary summary;
  final List<ActivityEntry> activity;

  const _DashboardData({required this.summary, required this.activity});
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;

  const _StatCard({
    required this.icon,
    required this.label,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          color: color.withValues(alpha: 0.1),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(label, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}

class _QuickActionTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _QuickActionTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.arrow_forward),
        onTap: onTap,
      ),
    );
  }
}
