// The customer's wishlists: create lists, add products by number, remove items.

import 'package:flutter/material.dart';
import '../../models/ecommerce_extended_models.dart';
import '../../services/authenticated_dio.dart';
import '../../services/ecommerce_service.dart';

class WishlistsScreen extends StatefulWidget {
  final EcommerceService? service;

  const WishlistsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<WishlistsScreen> createState() => _WishlistsScreenState();
}

class _WishlistsScreenState extends State<WishlistsScreen> {
  late final EcommerceService _service = widget.service ?? EcommerceService(createAuthenticatedDio());
  final _nameController = TextEditingController();
  final _productController = TextEditingController();

  late Future<List<Wishlist>> _wishlists = _service.fetchWishlists();
  Wishlist? _selected;
  Future<List<WishlistItem>>? _items;
  bool _makePublic = false;

  @override
  void dispose() {
    _nameController.dispose();
    _productController.dispose();
    super.dispose();
  }

  void _reloadWishlists() {
    setState(() {
      _wishlists = _service.fetchWishlists();
    });
  }

  void _select(Wishlist wishlist) {
    setState(() {
      _selected = wishlist;
      _items = _service.fetchWishlistItems(wishlist.id);
    });
  }

  void _reloadItems() {
    final wishlist = _selected;
    if (wishlist == null) return;
    setState(() {
      _items = _service.fetchWishlistItems(wishlist.id);
    });
  }

  void _notify(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> _createWishlist() async {
    final name = _nameController.text.trim();
    if (name.isEmpty) {
      _notify('Give the wishlist a name.');
      return;
    }
    try {
      final created = await _service.createWishlist(name: name, isPublic: _makePublic);
      _nameController.clear();
      setState(() => _makePublic = false);
      _reloadWishlists();
      _select(created);
      _notify('Wishlist "${created.name}" created.');
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _addProduct() async {
    final wishlist = _selected;
    final productId = int.tryParse(_productController.text.trim());
    if (wishlist == null) return;
    if (productId == null || productId <= 0) {
      _notify('Enter a valid product number.');
      return;
    }
    try {
      await _service.addWishlistItem(wishlist.id, productId);
      _productController.clear();
      _reloadItems();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  Future<void> _removeItem(WishlistItem item) async {
    try {
      await _service.removeWishlistItem(item.id);
      _reloadItems();
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Wishlists')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            key: const Key('wishlist-name-field'),
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'New wishlist name'),
          ),
          SwitchListTile(
            key: const Key('wishlist-public-switch'),
            contentPadding: EdgeInsets.zero,
            title: const Text('Share publicly'),
            value: _makePublic,
            onChanged: (value) => setState(() => _makePublic = value),
          ),
          ElevatedButton(
            key: const Key('create-wishlist'),
            onPressed: _createWishlist,
            child: const Text('Create wishlist'),
          ),
          const Divider(height: 32),
          FutureBuilder<List<Wishlist>>(
            future: _wishlists,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return _ErrorBlock(message: messageFromError(snapshot.error!), onRetry: _reloadWishlists);
              }
              final lists = snapshot.data ?? const <Wishlist>[];
              if (lists.isEmpty) {
                return const Text('You have no wishlists yet.');
              }
              return Column(
                children: [
                  for (final wishlist in lists)
                    ListTile(
                      key: Key('wishlist-${wishlist.id}'),
                      selected: _selected?.id == wishlist.id,
                      title: Text(wishlist.name),
                      subtitle: wishlist.isPublic ? const Text('Public') : null,
                      onTap: () => _select(wishlist),
                    ),
                ],
              );
            },
          ),
          if (_selected != null) ...[
            const Divider(height: 32),
            if (_selected!.isPublic) Text('Share token: ${_selected!.shareToken}'),
            TextField(
              key: const Key('wishlist-product-field'),
              controller: _productController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Product number'),
            ),
            ElevatedButton(
              key: const Key('add-wishlist-product'),
              onPressed: _addProduct,
              child: const Text('Add product'),
            ),
            FutureBuilder<List<WishlistItem>>(
              future: _items,
              builder: (context, snapshot) {
                if (snapshot.connectionState != ConnectionState.done) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return _ErrorBlock(message: messageFromError(snapshot.error!), onRetry: _reloadItems);
                }
                final items = snapshot.data ?? const <WishlistItem>[];
                if (items.isEmpty) {
                  return const Padding(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    child: Text('No products in this wishlist yet.'),
                  );
                }
                return Column(
                  children: [
                    for (final item in items)
                      ListTile(
                        key: Key('wishlist-item-${item.id}'),
                        title: Text('Product #${item.productId}'),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete_outline),
                          tooltip: 'Remove',
                          onPressed: () => _removeItem(item),
                        ),
                      ),
                  ],
                );
              },
            ),
          ],
        ],
      ),
    );
  }
}

class _ErrorBlock extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;

  const _ErrorBlock({required this.message, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(message, style: const TextStyle(color: Colors.red)),
        TextButton(onPressed: onRetry, child: const Text('Try again')),
      ],
    );
  }
}
