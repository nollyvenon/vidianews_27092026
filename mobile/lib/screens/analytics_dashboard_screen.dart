import 'package:flutter/material.dart'

class AnalyticsDashboardScreen extends StatelessWidget {
  const AnalyticsDashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analytics')),
      body: GridView.count(
        crossAxisCount: 2,
        padding: const EdgeInsets.all(16),
        mainAxisSpacing: 12,
        crossAxisSpacing: 12,
        children: [
          Card(child: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: const [Text('125K'), Text('Views')]))),
          Card(child: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: const [Text('3.4K'), Text('Subs')]))),
        ],
      ),
    );
  }
}
