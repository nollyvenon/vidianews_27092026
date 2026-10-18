// Published documentation with view counts, and the API reference.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

class _DocsData {
  final List<Doc> docs;
  final List<ApiReference> api;

  const _DocsData({required this.docs, required this.api});
}

class DocsScreen extends StatefulWidget {
  final DiscoveryService? service;

  const DocsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<DocsScreen> createState() => _DocsScreenState();
}

class _DocsScreenState extends State<DocsScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  late Future<_DocsData> _data = _load();

  Future<_DocsData> _load() async {
    final docs = await _service.fetchDocs();
    final api = await _service.fetchApiReference();
    return _DocsData(docs: docs, api: api);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Documentation')),
      body: AsyncView<_DocsData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text('Guides', style: Theme.of(context).textTheme.titleMedium),
            if (data.docs.isEmpty) const Text('No documents published yet.'),
            for (final doc in data.docs)
              ListTile(
                key: Key('doc-${doc.id}'),
                contentPadding: EdgeInsets.zero,
                title: Text(doc.title),
                subtitle: Text('${doc.docType} · version ${doc.version}'),
                trailing: Text('${doc.views} views'),
              ),
            const Divider(height: 32),
            Text('API reference', style: Theme.of(context).textTheme.titleMedium),
            if (data.api.isEmpty) const Text('No endpoints documented yet.'),
            for (final entry in data.api)
              ListTile(
                key: Key('api-${entry.id}'),
                contentPadding: EdgeInsets.zero,
                title: Text('${entry.method} ${entry.endpoint}'),
              ),
          ],
        ),
      ),
    );
  }
}
