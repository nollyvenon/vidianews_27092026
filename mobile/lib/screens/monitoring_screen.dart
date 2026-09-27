import 'package:flutter/material.dart'

class MonitoringScreen extends StatelessWidget {
  const MonitoringScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('System Monitoring')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Key Metrics', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              children: [
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Text('45ms', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Response Time', style: TextStyle(fontSize: 11)),
                        SizedBox(height: 8),
                        Chip(label: Text('Good', style: TextStyle(fontSize: 10)))
                      ],
                    ),
                  ),
                ),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Text('0.2%', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Error Rate', style: TextStyle(fontSize: 11)),
                        SizedBox(height: 8),
                        Chip(label: Text('Good', style: TextStyle(fontSize: 10)))
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            const Text('Health Checks', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListTile(
              title: const Text('Database'),
              trailing: const Text('✓ Healthy', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
            ),
            ListTile(
              title: const Text('API Gateway'),
              trailing: const Text('✓ Healthy', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
            ),
            ListTile(
              title: const Text('Cache Service'),
              trailing: const Text('✓ Healthy', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
            ),
            ListTile(
              title: const Text('Message Queue'),
              trailing: const Text('⚠ Degraded', style: TextStyle(color: Colors.orange, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}
