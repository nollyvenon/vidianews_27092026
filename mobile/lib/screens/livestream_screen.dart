// Live streams: see who is live now, and start a new stream with its key.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

class LivestreamScreen extends StatefulWidget {
  final DiscoveryService? service;

  const LivestreamScreen({Key? key, this.service}) : super(key: key);

  @override
  State<LivestreamScreen> createState() => _LivestreamScreenState();
}

class _LivestreamScreenState extends State<LivestreamScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  late Future<List<ActiveStream>> _active = _service.fetchActiveStreams();
  String? _streamKey;

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() {
      _active = _service.fetchActiveStreams();
    });
  }

  Future<void> _start() async {
    final title = _titleController.text.trim();
    if (title.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Give the stream a title.')));
      return;
    }
    try {
      final created = await _service.startLiveStream(title: title, description: _descriptionController.text.trim());
      _titleController.clear();
      _descriptionController.clear();
      setState(() => _streamKey = created['stream_key'] as String?);
      _reload();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Live')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            key: const Key('stream-title-field'),
            controller: _titleController,
            decoration: const InputDecoration(labelText: 'Stream title'),
          ),
          TextField(
            key: const Key('stream-description-field'),
            controller: _descriptionController,
            decoration: const InputDecoration(labelText: 'Description (optional)'),
          ),
          ElevatedButton(key: const Key('start-stream'), onPressed: _start, child: const Text('Start a stream')),
          if (_streamKey != null) ...[
            const SizedBox(height: 8),
            SelectableText('Stream key: $_streamKey', key: const Key('stream-key')),
          ],
          const Divider(height: 32),
          const Text('Live now', style: TextStyle(fontWeight: FontWeight.bold)),
          AsyncView<List<ActiveStream>>(
            future: _active,
            onRetry: _reload,
            builder: (context, streams) {
              if (streams.isEmpty) return const Text('Nobody is live right now.');
              return Column(
                children: [
                  for (final stream in streams)
                    ListTile(
                      key: Key('stream-${stream.id}'),
                      contentPadding: EdgeInsets.zero,
                      title: Text(stream.title),
                      trailing: Text('${stream.viewers} watching'),
                    ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}
