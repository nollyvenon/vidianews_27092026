// Outbound webhooks: the endpoints that receive platform events, creating one, and a test delivery.

import 'package:flutter/material.dart';
import '../models/community_models.dart';
import '../services/authenticated_dio.dart';
import '../services/community_service.dart';
import '../widgets/async_view.dart';

class _WebhookData {
  final List<OutboundWebhook> webhooks;
  final List<WebhookEventType> events;

  const _WebhookData({required this.webhooks, required this.events});
}

class WebhooksScreen extends StatefulWidget {
  final CommunityService? service;

  const WebhooksScreen({Key? key, this.service}) : super(key: key);

  @override
  State<WebhooksScreen> createState() => _WebhooksScreenState();
}

class _WebhooksScreenState extends State<WebhooksScreen> {
  late final CommunityService _service = widget.service ?? CommunityService(createAuthenticatedDio());
  final _urlController = TextEditingController();
  final _descriptionController = TextEditingController();
  final Set<String> _selectedEvents = {};
  late Future<_WebhookData> _data = _load();

  @override
  void dispose() {
    _urlController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<_WebhookData> _load() async {
    final webhooks = await _service.fetchWebhooks();
    final events = await _service.fetchWebhookEvents();
    return _WebhookData(webhooks: webhooks, events: events);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  void _notify(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> _create() async {
    final url = _urlController.text.trim();
    if (url.isEmpty) {
      _notify('Enter the URL that should receive events.');
      return;
    }
    if (_selectedEvents.isEmpty) {
      _notify('Choose at least one event.');
      return;
    }
    try {
      await _service.createWebhook(
        url: url,
        events: _selectedEvents.toList(),
        description: _descriptionController.text.trim().isEmpty ? null : _descriptionController.text.trim(),
      );
      _urlController.clear();
      _descriptionController.clear();
      setState(_selectedEvents.clear);
      _notify('Webhook created.');
      _reload();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _test(OutboundWebhook webhook) async {
    try {
      final result = await _service.testWebhook(webhook.id);
      _notify('Test delivery: ${result['status'] ?? 'sent'}');
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Webhooks')),
      body: AsyncView<_WebhookData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextField(
              key: const Key('webhook-url-field'),
              controller: _urlController,
              keyboardType: TextInputType.url,
              decoration: const InputDecoration(labelText: 'Endpoint URL'),
            ),
            TextField(
              key: const Key('webhook-description-field'),
              controller: _descriptionController,
              decoration: const InputDecoration(labelText: 'Description (optional)'),
            ),
            const SizedBox(height: 8),
            const Text('Events', style: TextStyle(fontWeight: FontWeight.bold)),
            for (final event in data.events)
              CheckboxListTile(
                key: Key('event-${event.event}'),
                contentPadding: EdgeInsets.zero,
                title: Text(event.event),
                subtitle: Text(event.description),
                value: _selectedEvents.contains(event.event),
                onChanged: (checked) => setState(() {
                  if (checked ?? false) {
                    _selectedEvents.add(event.event);
                  } else {
                    _selectedEvents.remove(event.event);
                  }
                }),
              ),
            ElevatedButton(key: const Key('create-webhook'), onPressed: _create, child: const Text('Create webhook')),
            const Divider(height: 32),
            if (data.webhooks.isEmpty) const Text('No webhooks yet.'),
            for (final webhook in data.webhooks)
              Card(
                child: ListTile(
                  key: Key('webhook-${webhook.id}'),
                  title: Text(webhook.url),
                  subtitle: Text('${webhook.events.join(', ')}${webhook.isActive ? '' : ' · paused'}'),
                  trailing: TextButton(onPressed: () => _test(webhook), child: const Text('Test')),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
