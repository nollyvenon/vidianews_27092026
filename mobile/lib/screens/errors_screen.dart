import 'package:flutter/material.dart'

class ErrorsScreen extends StatelessWidget {
  const ErrorsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final errors = [
      {'type': 'ValueError', 'count': '12', 'severity': 'HIGH'},
      {'type': 'DatabaseError', 'count': '8', 'severity': 'CRITICAL'},
      {'type': 'TypeError', 'count': '3', 'severity': 'MEDIUM'}
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Error Tracking')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Unresolved Errors', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: errors.length,
              itemBuilder: (context, index) {
                final err = errors[index];
                final bgColor = err['severity'] == 'CRITICAL' ? Colors.red : err['severity'] == 'HIGH' ? Colors.orange : Colors.yellow;
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(err['type']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(color: bgColor.withOpacity(0.3), borderRadius: BorderRadius.circular(4)),
                              child: Text(err['severity']!, style: TextStyle(fontSize: 10, color: bgColor, fontWeight: FontWeight.bold)),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text('${err['count']} occurrences', style: const TextStyle(fontSize: 12, color: Colors.grey)),
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
}
