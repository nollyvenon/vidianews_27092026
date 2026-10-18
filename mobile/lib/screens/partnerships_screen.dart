// Partnerships the signed-in creator has with other members, and proposing a new one.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

const List<String> _partnershipTypes = ['sponsorship', 'revenue_share', 'collaboration', 'affiliate'];

class PartnershipsScreen extends StatefulWidget {
  final DiscoveryService? service;

  const PartnershipsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<PartnershipsScreen> createState() => _PartnershipsScreenState();
}

class _PartnershipsScreenState extends State<PartnershipsScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  final _partnerController = TextEditingController();
  String _type = _partnershipTypes.first;
  late Future<List<Partnership>> _partnerships = _service.fetchPartnerships();

  @override
  void dispose() {
    _partnerController.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() {
      _partnerships = _service.fetchPartnerships();
    });
  }

  Future<void> _propose() async {
    final partner = _partnerController.text.trim();
    if (partner.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Enter the partner\'s member number.')));
      return;
    }
    try {
      await _service.proposePartnership(partnerId: partner, partnershipType: _type);
      _partnerController.clear();
      _reload();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Partnerships')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            key: const Key('partner-field'),
            controller: _partnerController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: 'Partner member number'),
          ),
          DropdownButtonFormField<String>(
            key: const Key('partnership-type'),
            initialValue: _type,
            decoration: const InputDecoration(labelText: 'Type'),
            items: [for (final type in _partnershipTypes) DropdownMenuItem(value: type, child: Text(type))],
            onChanged: (value) => setState(() => _type = value ?? _type),
          ),
          ElevatedButton(key: const Key('propose-partnership'), onPressed: _propose, child: const Text('Propose partnership')),
          const Divider(height: 32),
          AsyncView<List<Partnership>>(
            future: _partnerships,
            onRetry: _reload,
            builder: (context, partnerships) {
              if (partnerships.isEmpty) return const Text('No partnerships yet.');
              return Column(
                children: [
                  for (final partnership in partnerships)
                    ListTile(
                      key: Key('partnership-${partnership.id}'),
                      contentPadding: EdgeInsets.zero,
                      title: Text(partnership.type),
                      subtitle: Text(partnership.status),
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
