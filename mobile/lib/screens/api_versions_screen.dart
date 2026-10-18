// Registered API endpoint versions, their deprecation state, and the migrations between versions.

import 'package:flutter/material.dart';
import '../services/api_versions_service.dart';
import '../services/authenticated_dio.dart';
import '../widgets/async_view.dart';

class APIVersionsScreen extends StatefulWidget {
  final ApiVersionsService? service;

  const APIVersionsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<APIVersionsScreen> createState() => _APIVersionsScreenState();
}

class _APIVersionsScreenState extends State<APIVersionsScreen> {
  late final ApiVersionsService _service = widget.service ?? ApiVersionsService(createAuthenticatedDio());
  late Future<_VersionData> _data = _load();

  Future<_VersionData> _load() async {
    final versions = await _service.fetchVersions();
    final migrations = await _service.fetchMigrations();
    return _VersionData(versions: versions, migrations: migrations);
  }

  void _reload() {
    setState(() {
      _data = _load();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('API Versions')),
      body: AsyncView<_VersionData>(
        future: _data,
        onRetry: _reload,
        builder: (context, data) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const Text('Endpoint versions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            if (data.versions.isEmpty) const Text('No endpoint versions are registered.'),
            for (final version in data.versions)
              Card(
                child: ListTile(
                  key: Key('version-${version.id}'),
                  title: Text(version.endpoint),
                  subtitle: Text(
                    version.deprecated
                        ? '${version.version} · deprecated'
                            '${version.sunsetDate != null ? ', sunsets ${version.sunsetDate!.toLocal().toString().split(' ').first}' : ''}'
                        : version.version,
                  ),
                ),
              ),
            const SizedBox(height: 24),
            const Text('Migrations', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            if (data.migrations.isEmpty) const Text('No migrations between versions.'),
            for (final migration in data.migrations)
              ListTile(
                key: Key('migration-${migration.id}'),
                contentPadding: EdgeInsets.zero,
                title: Text('${migration.oldVersion} → ${migration.newVersion}'),
                subtitle: Text(migration.status),
              ),
          ],
        ),
      ),
    );
  }
}

class _VersionData {
  final List<EndpointVersion> versions;
  final List<VersionMigration> migrations;

  const _VersionData({required this.versions, required this.migrations});
}
