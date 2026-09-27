import 'package:flutter/material.dart'

class RealtimeScreen extends StatefulWidget {
  const RealtimeScreen({Key? key}) : super(key: key);

  @override
  State<RealtimeScreen> createState() => _RealtimeScreenState();
}

class _RealtimeScreenState extends State<RealtimeScreen> {
  final TextEditingController messageController = TextEditingController();
  List<Map<String, String>> messages = [
    {'user': 'John', 'text': 'Just uploaded a new video!', 'time': 'now'},
    {'user': 'Jane', 'text': 'Great content', 'time': '2m ago'},
  ];

  void sendMessage() {
    if (messageController.text.isNotEmpty) {
      setState(() {
        messages.insert(0, {'user': 'You', 'text': messageController.text, 'time': 'now'});
      });
      messageController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Live Feed'),
        actions: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Center(
              child: Row(
                children: const [
                  Icon(Icons.circle, color: Colors.green, size: 8),
                  SizedBox(width: 4),
                  Text('Live', style: TextStyle(fontSize: 12)),
                ],
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: true,
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final msg = messages[index];
                return Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(msg['user']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                          Text(msg['time']!, style: const TextStyle(fontSize: 10, color: Colors.grey)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(msg['text']!, style: const TextStyle(fontSize: 14)),
                      const SizedBox(height: 8),
                      Container(height: 1, color: Colors.grey.shade300),
                    ],
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: messageController,
                    decoration: InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(onPressed: sendMessage, child: const Text('Send')),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
