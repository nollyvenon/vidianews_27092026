import 'package:flutter/material.dart'

class AuditScreen extends StatefulWidget {
  const AuditScreen({Key? key}) : super(key: key);

  @override
  State<AuditScreen> createState() => _AuditScreenState();
}

class _AuditScreenState extends State<AuditScreen> {
  final List<Map<String, String>> logs = [
    {'action': 'CREATE', 'resource': 'Video', 'date': '2026-09-27'},
    {'action': 'UPDATE', 'resource': 'Content', 'date': '2026-09-26'},
    {'action': 'DELETE', 'resource': 'Draft', 'date': '2026-09-25'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Audit Logs')),
      body: ListView.builder(
        itemCount: logs.length,
        itemBuilder: (context, index) {
          final log = logs[index];
          return Card(
            margin: const EdgeInsets.all(8),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.blue[100],
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(log['action']!, style: const TextStyle(fontSize: 12)),
                      ),
                      const SizedBox(height: 8),
                      Text(log['resource']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                  Text(log['date']!, style: const TextStyle(color: Colors.grey, fontSize: 12)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
