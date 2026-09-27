import 'package:flutter/material.dart'

class NotificationsCenterScreen extends StatefulWidget {
  const NotificationsCenterScreen({Key? key}) : super(key: key);

  @override
  State<NotificationsCenterScreen> createState() => _NotificationsCenterScreenState();
}

class _NotificationsCenterScreenState extends State<NotificationsCenterScreen> {
  final List<Map<String, String>> notifications = [
    {'title': 'Content Approved', 'msg': 'Your video was approved', 'type': 'info'},
    {'title': 'Payment Received', 'msg': '\$150 received', 'type': 'success'},
    {'title': 'New Comment', 'msg': 'Someone commented on your video', 'type': 'info'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notifications')),
      body: ListView.builder(
        itemCount: notifications.length,
        itemBuilder: (context, index) {
          final notif = notifications[index];
          return Card(
            margin: const EdgeInsets.all(8),
            child: ListTile(
              leading: Icon(
                notif['type'] == 'success' ? Icons.check_circle : Icons.info,
                color: notif['type'] == 'success' ? Colors.green : Colors.blue,
              ),
              title: Text(notif['title']!),
              subtitle: Text(notif['msg']!),
              trailing: const Icon(Icons.close),
            ),
          );
        },
      ),
    );
  }
}
