// Admin audit trail, newest first. Only administrators can open it; others see the server's refusal.

import 'package:flutter/material.dart';
import '../models/audit_models.dart';
import '../services/audit_service.dart';
import '../services/authenticated_dio.dart';

class AuditScreen extends StatefulWidget {
  final AuditService? service;

  const AuditScreen({Key? key, this.service}) : super(key: key);

  @override
  State<AuditScreen> createState() => _AuditScreenState();
}

class _AuditScreenState extends State<AuditScreen> {
  late final AuditService _service = widget.service ?? AuditService(createAuthenticatedDio());
  late Future<List<AuditEntry>> _entries = _service.fetchEntries();

  void _reload() {
    setState(() {
      _entries = _service.fetchEntries();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Audit Logs')),
      body: FutureBuilder<List<AuditEntry>>(
        future: _entries,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(messageFromError(snapshot.error!), textAlign: TextAlign.center),
                    const SizedBox(height: 12),
                    OutlinedButton(onPressed: _reload, child: const Text('Try again')),
                  ],
                ),
              ),
            );
          }
          final entries = snapshot.data!;
          if (entries.isEmpty) {
            return const Center(child: Text('No audit entries yet.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: entries.length,
            itemBuilder: (context, index) {
              final entry = entries[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  title: Text('${entry.action} · ${entry.resourceType}'),
                  subtitle: Text('Admin #${entry.adminId} · ${entry.timestamp.toLocal()}'),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
