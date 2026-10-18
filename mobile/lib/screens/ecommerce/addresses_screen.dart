// The customer's shipping addresses: list them and add new ones.

import 'package:flutter/material.dart';
import '../../models/ecommerce_extended_models.dart';
import '../../services/authenticated_dio.dart';
import '../../services/ecommerce_service.dart';

class AddressesScreen extends StatefulWidget {
  final EcommerceService? service;

  const AddressesScreen({Key? key, this.service}) : super(key: key);

  @override
  State<AddressesScreen> createState() => _AddressesScreenState();
}

class _AddressesScreenState extends State<AddressesScreen> {
  late final EcommerceService _service = widget.service ?? EcommerceService(createAuthenticatedDio());
  final _formKey = GlobalKey<FormState>();
  final Map<String, TextEditingController> _controllers = {
    for (final key in _requiredFields.keys) key: TextEditingController(),
    for (final key in _optionalFields) key: TextEditingController(),
  };
  bool _isDefault = false;

  late Future<List<ShippingAddress>> _addresses = _service.fetchAddresses();

  static const Map<String, String> _requiredFields = {
    'first_name': 'First name',
    'last_name': 'Last name',
    'street_address': 'Street address',
    'city': 'City',
    'postal_code': 'Postal code',
    'country': 'Country',
  };
  static const List<String> _optionalFields = ['state', 'phone'];

  @override
  void dispose() {
    for (final controller in _controllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  void _reload() {
    setState(() {
      _addresses = _service.fetchAddresses();
    });
  }

  String? _optional(String key) {
    final value = _controllers[key]!.text.trim();
    return value.isEmpty ? null : value;
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    try {
      await _service.createAddress({
        for (final key in _requiredFields.keys) key: _controllers[key]!.text.trim(),
        'state': _optional('state'),
        'phone': _optional('phone'),
        'is_default': _isDefault,
      });
      for (final controller in _controllers.values) {
        controller.clear();
      }
      setState(() => _isDefault = false);
      _reload();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Address saved.')));
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(messageFromError(error))));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Shipping addresses')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          FutureBuilder<List<ShippingAddress>>(
            future: _addresses,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return Text(messageFromError(snapshot.error!), style: const TextStyle(color: Colors.red));
              }
              final addresses = snapshot.data ?? const <ShippingAddress>[];
              if (addresses.isEmpty) {
                return const Text('You have no saved addresses.');
              }
              return Column(
                children: [
                  for (final address in addresses)
                    Card(
                      child: ListTile(
                        key: Key('address-${address.id}'),
                        title: Text('${address.firstName} ${address.lastName}${address.isDefault ? ' (default)' : ''}'),
                        subtitle: Text(
                          '${address.streetAddress}, ${address.city}'
                          '${address.state != null ? ', ${address.state}' : ''} ${address.postalCode}, ${address.country}',
                        ),
                      ),
                    ),
                ],
              );
            },
          ),
          const Divider(height: 32),
          Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                for (final entry in _requiredFields.entries)
                  TextFormField(
                    key: Key('address-field-${entry.key}'),
                    controller: _controllers[entry.key],
                    decoration: InputDecoration(labelText: entry.value),
                    validator: (value) =>
                        (value == null || value.trim().isEmpty) ? '${entry.value} is required' : null,
                  ),
                for (final key in _optionalFields)
                  TextFormField(
                    key: Key('address-field-$key'),
                    controller: _controllers[key],
                    decoration: InputDecoration(labelText: key == 'state' ? 'State / region' : 'Phone'),
                  ),
                SwitchListTile(
                  contentPadding: EdgeInsets.zero,
                  title: const Text('Use as my default address'),
                  value: _isDefault,
                  onChanged: (value) => setState(() => _isDefault = value),
                ),
                ElevatedButton(
                  key: const Key('save-address'),
                  onPressed: _save,
                  child: const Text('Save address'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
