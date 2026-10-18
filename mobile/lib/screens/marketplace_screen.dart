// The marketplace: products with their price, rating and stock, searchable by name.

import 'package:flutter/material.dart';
import '../services/authenticated_dio.dart';
import '../services/ecommerce_service.dart';
import '../widgets/async_view.dart';

class MarketplaceScreen extends StatefulWidget {
  final EcommerceService? service;

  const MarketplaceScreen({Key? key, this.service}) : super(key: key);

  @override
  State<MarketplaceScreen> createState() => _MarketplaceScreenState();
}

class _MarketplaceScreenState extends State<MarketplaceScreen> {
  late final EcommerceService _service = widget.service ?? EcommerceService(createAuthenticatedDio());
  final _queryController = TextEditingController();
  late Future<List<Map<String, dynamic>>> _products = _service.fetchProducts();

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() {
      _products = _service.fetchProducts(query: _queryController.text);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Marketplace')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            key: const Key('marketplace-search'),
            controller: _queryController,
            textInputAction: TextInputAction.search,
            onSubmitted: (_) => _reload(),
            decoration: const InputDecoration(labelText: 'Search products'),
          ),
          const SizedBox(height: 12),
          AsyncView<List<Map<String, dynamic>>>(
            future: _products,
            onRetry: _reload,
            builder: (context, products) {
              if (products.isEmpty) return const Text('No products found.');
              return Column(
                children: [
                  for (final product in products)
                    Card(
                      child: ListTile(
                        key: Key('product-${product['id']}'),
                        title: Text(product['name'] as String),
                        subtitle: Text(
                          '${(product['average_rating'] as num? ?? 0).toStringAsFixed(1)} rating · '
                          '${product['stock_quantity'] as int? ?? 0} in stock',
                        ),
                        trailing: Text('\$${(product['price'] as num).toStringAsFixed(2)}'),
                      ),
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
