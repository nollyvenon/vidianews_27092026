import 'package:flutter/material.dart'

class PushNotificationsScreen extends StatefulWidget {
  const PushNotificationsScreen({Key? key}) : super(key: key);

  @override
  State<PushNotificationsScreen> createState() => _PushNotificationsScreenState();
}

class _PushNotificationsScreenState extends State<PushNotificationsScreen> {
  bool commentsEnabled = true;
  bool likesEnabled = true;
  bool followersEnabled = false;
  bool systemEnabled = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notifications')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Notification Preferences', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: Column(
                children: [
                  CheckboxListTile(
                    title: const Text('Comments'),
                    value: commentsEnabled,
                    onChanged: (v) => setState(() => commentsEnabled = v!),
                  ),
                  CheckboxListTile(
                    title: const Text('Likes'),
                    value: likesEnabled,
                    onChanged: (v) => setState(() => likesEnabled = v!),
                  ),
                  CheckboxListTile(
                    title: const Text('New Followers'),
                    value: followersEnabled,
                    onChanged: (v) => setState(() => followersEnabled = v!),
                  ),
                  CheckboxListTile(
                    title: const Text('System Alerts'),
                    value: systemEnabled,
                    onChanged: (v) => setState(() => systemEnabled = v!),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text('Registered Devices', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('iPhone 14 Pro', style: TextStyle(fontWeight: FontWeight.bold)),
                    SizedBox(height: 4),
                    Text('iOS • Active', style: TextStyle(fontSize: 12, color: Colors.green)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 8),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Android Phone', style: TextStyle(fontWeight: FontWeight.bold)),
                    SizedBox(height: 4),
                    Text('Android • Active', style: TextStyle(fontSize: 12, color: Colors.green)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Recent Notifications', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                title: const Text('New Comment'),
                subtitle: const Text('Someone commented on your video • 2h ago'),
                trailing: const Dot(),
              ),
            ),
            const SizedBox(height: 8),
            Card(
              child: ListTile(
                title: const Text('Upload Complete'),
                subtitle: const Text('Your video has been processed • 1d ago'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class Dot extends StatelessWidget {
  const Dot({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 8,
      height: 8,
      decoration: const BoxDecoration(color: Colors.blue, shape: BoxShape.circle),
    );
  }
}
