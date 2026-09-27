import 'package:flutter/material.dart'

class CreatorScreen extends StatelessWidget {
  const CreatorScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Creator Dashboard')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
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
                        Text('5.2K', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.blue)),
                        SizedBox(height: 4),
                        Text('Followers', style: TextStyle(fontSize: 12)),
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
                        Text('\$2.4K', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.green)),
                        SizedBox(height: 4),
                        Text('Earnings', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Recent Activity', style: TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 12),
                    ListTile(contentPadding: EdgeInsets.zero, title: const Text('3 new comments'), subtitle: Text('2 hours ago')),
                    ListTile(contentPadding: EdgeInsets.zero, title: const Text('Video published'), subtitle: Text('Today')),
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
