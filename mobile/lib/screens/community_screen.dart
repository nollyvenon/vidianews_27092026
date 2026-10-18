import 'package:flutter/material.dart';
import 'dart:convert';
import '../services/authenticated_http.dart';
import '../services/authenticated_dio.dart';

class CommunityScreen extends StatefulWidget {
  const CommunityScreen({Key? key}) : super(key: key);

  @override
  State<CommunityScreen> createState() => _CommunityScreenState();
}

class _CommunityScreenState extends State<CommunityScreen> {
  List<dynamic> threads = [];
  bool loading = false;

  @override
  void initState() {
    super.initState();
    fetchThreads();
  }

  Future<void> fetchThreads() async {
    setState(() => loading = true);
    try {
      final res = await authenticatedHttp.get(Uri.parse('$kApiBaseUrl/forum/threads'));
      if (res.statusCode == 200) {
        setState(() => threads = jsonDecode(res.body));
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Community Forums')),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: threads.length,
              itemBuilder: (context, index) {
                final thread = threads[index];
                return Card(
                  margin: const EdgeInsets.all(8),
                  child: ListTile(
                    title: Text(thread['title'] ?? 'Untitled'),
                    subtitle: Text('Replies: ${thread['replies'] ?? 0}'),
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: fetchThreads,
        child: const Icon(Icons.refresh),
      ),
    );
  }
}
