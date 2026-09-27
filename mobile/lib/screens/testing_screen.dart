import 'package:flutter/material.dart'

class TestingScreen extends StatelessWidget {
  const TestingScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final suites = [
      {'name': 'Unit Tests', 'tests': '250', 'passed': '245', 'coverage': '94.5%'},
      {'name': 'Integration', 'tests': '85', 'passed': '83', 'coverage': '89.2%'},
      {'name': 'E2E Tests', 'tests': '42', 'passed': '41', 'coverage': '92.1%'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Test Suites')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            GridView.count(
              crossAxisCount: 3,
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
                        Text('377', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text('Total Tests', style: TextStyle(fontSize: 10)),
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
                        Text('98.7%', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green)),
                        SizedBox(height: 4),
                        Text('Pass Rate', style: TextStyle(fontSize: 10)),
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
                        Text('91.9%', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.purple)),
                        SizedBox(height: 4),
                        Text('Coverage', style: TextStyle(fontSize: 10)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            const Text('Test Suites', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: suites.length,
              itemBuilder: (context, index) {
                final s = suites[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    title: Text(s['name']!),
                    subtitle: Text('${s['passed']}/${s['tests']} • ${s['coverage']}'),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
