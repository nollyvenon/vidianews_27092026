import 'package:flutter/material.dart'
import 'package:vidianews/services/chat_service.dart'

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ChatService _chatService = ChatService();
  final TextEditingController _messageController = TextEditingController();
  List<Map<String, String>> messages = [];
  bool isLoading = false;
  int? activeChatId;

  @override
  void initState() {
    super.initState();
    _loadChats();
  }

  Future<void> _loadChats() async {
    try {
      setState(() => isLoading = true);
      final chats = await _chatService.listChats(1);
      if (chats.isNotEmpty) {
        setState(() => activeChatId = chats[0]['id']);
        _loadChatMessages(chats[0]['id']);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading chats: $e')),
      );
    } finally {
      setState(() => isLoading = false);
    }
  }

  Future<void> _loadChatMessages(int chatId) async {
    try {
      final chat = await _chatService.getChat(chatId);
      setState(() {
        messages = (chat['messages'] as List?)?.map<Map<String, String>>((m) {
          return {
            'role': m['role'].toString(),
            'content': m['content'].toString(),
          };
        }).toList() ?? [];
      });
    } catch (e) {
      print('Error loading messages: $e');
    }
  }

  Future<void> _sendMessage() async {
    if (_messageController.text.isEmpty || activeChatId == null) return;

    final message = _messageController.text;
    _messageController.clear();

    setState(() {
      messages.add({'role': 'user', 'content': message});
    });

    try {
      await _chatService.addMessage(
        activeChatId!,
        'user',
        message,
        (message.length ~/ 4) + 1,
      );

      // Simulate AI response
      await Future.delayed(Duration(seconds: 1));
      setState(() {
        messages.add({
          'role': 'assistant',
          'content': 'Thanks for your message! How can I help?'
        });
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error sending message: $e')),
      );
    }
  }

  Future<void> _createNewChat() async {
    try {
      final chat = await _chatService.createChat(1, 'New Chat');
      setState(() {
        activeChatId = chat['id'];
        messages = [];
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error creating chat: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Chat'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _createNewChat,
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: messages.length,
                    itemBuilder: (context, index) {
                      final msg = messages[index];
                      final isUser = msg['role'] == 'user';
                      return Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Align(
                          alignment: isUser
                              ? Alignment.centerRight
                              : Alignment.centerLeft,
                          child: Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: isUser
                                  ? Colors.blue[600]
                                  : Colors.grey[300],
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              msg['content'] ?? '',
                              style: TextStyle(
                                color: isUser ? Colors.white : Colors.black,
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _messageController,
                          decoration: InputDecoration(
                            hintText: 'Ask anything...',
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(24),
                            ),
                          ),
                        ),
                      ),
                      SizedBox(width: 8),
                      FloatingActionButton(
                        mini: true,
                        onPressed: _sendMessage,
                        child: const Icon(Icons.send),
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }
}
