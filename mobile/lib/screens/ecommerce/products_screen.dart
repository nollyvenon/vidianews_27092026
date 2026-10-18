import 'package:flutter/material.dart';
import '../../services/authenticated_dio.dart';
import '../../services/ecommerce_service.dart';
import 'wishlists_screen.dart';
import 'addresses_screen.dart';
import 'order_tracking_screen.dart';

class Product {
  final int id;
  final String sku;
  final String name;
  final double price;
  final String category;
  final int stockQuantity;
  final double averageRating;
  final int reviewCount;

  Product({
    required this.id,
    required this.sku,
    required this.name,
    required this.price,
    required this.category,
    required this.stockQuantity,
    required this.averageRating,
    required this.reviewCount,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      sku: json['sku'],
      name: json['name'],
      price: (json['price'] as num).toDouble(),
      category: json['category'],
      stockQuantity: json['stock_quantity'],
      averageRating: (json['average_rating'] as num).toDouble(),
      reviewCount: json['review_count'],
    );
  }
}

class ProductsScreen extends StatefulWidget {
  final EcommerceService? service;

  const ProductsScreen({Key? key, this.service}) : super(key: key);

  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  late final EcommerceService _service = widget.service ?? EcommerceService(createAuthenticatedDio());
  late Future<List<Product>> futureProducts;
  String selectedCategory = '';
  String searchQuery = '';

  @override
  void initState() {
    super.initState();
    futureProducts = fetchProducts();
  }

  Future<List<Product>> fetchProducts({String query = ''}) async {
    final rows = await _service.fetchProducts(query: query);
    return rows.map(Product.fromJson).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Products'),
        backgroundColor: Colors.blue,
        actions: [
          IconButton(
            icon: const Icon(Icons.favorite_border),
            tooltip: 'Wishlists',
            onPressed: () => Navigator.of(context).push(MaterialPageRoute<void>(
              builder: (_) => WishlistsScreen(service: _service),
            )),
          ),
          IconButton(
            icon: const Icon(Icons.location_on_outlined),
            tooltip: 'Shipping addresses',
            onPressed: () => Navigator.of(context).push(MaterialPageRoute<void>(
              builder: (_) => AddressesScreen(service: _service),
            )),
          ),
          IconButton(
            icon: const Icon(Icons.local_shipping_outlined),
            tooltip: 'Order tracking',
            onPressed: () => Navigator.of(context).push(MaterialPageRoute<void>(
              builder: (_) => OrderTrackingScreen(service: _service),
            )),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                TextField(
                  onChanged: (value) {
                    setState(() {
                      searchQuery = value;
                      if (value.isNotEmpty) {
                        futureProducts = fetchProducts(query: value);
                      } else {
                        futureProducts = fetchProducts();
                      }
                    });
                  },
                  decoration: InputDecoration(
                    hintText: 'Search products...',
                    prefixIcon: const Icon(Icons.search),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  height: 40,
                  child: ListView(
                    scrollDirection: Axis.horizontal,
                    children: [
                      _buildCategoryChip('', 'All'),
                      _buildCategoryChip('electronics', 'Electronics'),
                      _buildCategoryChip('clothing', 'Clothing'),
                      _buildCategoryChip('books', 'Books'),
                      _buildCategoryChip('food', 'Food'),
                      _buildCategoryChip('home', 'Home'),
                      _buildCategoryChip('sports', 'Sports'),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: FutureBuilder<List<Product>>(
              future: futureProducts,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                } else if (snapshot.hasError) {
                  return Center(child: Text('Error: ${snapshot.error}'));
                } else if (snapshot.data!.isEmpty) {
                  return const Center(child: Text('No products found'));
                } else {
                  return GridView.builder(
                    padding: const EdgeInsets.all(16),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      childAspectRatio: 0.75,
                      crossAxisSpacing: 16,
                      mainAxisSpacing: 16,
                    ),
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      Product product = snapshot.data![index];
                      return Card(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Expanded(
                              child: Container(
                                color: Colors.grey[200],
                                child: const Icon(Icons.image, size: 80),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    product.name,
                                    maxLines: 2,
                                    overflow: TextOverflow.ellipsis,
                                    style: const TextStyle(
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  Text(
                                    '\$${product.price}',
                                    style: const TextStyle(
                                      color: Colors.blue,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 16,
                                    ),
                                  ),
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.star,
                                        size: 16,
                                        color: Colors.amber,
                                      ),
                                      Text(
                                        '${product.averageRating}',
                                        style: const TextStyle(fontSize: 12),
                                      ),
                                    ],
                                  ),
                                  SizedBox(
                                    width: double.infinity,
                                    child: ElevatedButton(
                                      onPressed: () {},
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor: Colors.green,
                                        padding: const EdgeInsets.symmetric(
                                          vertical: 4,
                                        ),
                                      ),
                                      child: const Text(
                                        'Add to Cart',
                                        style: TextStyle(fontSize: 12),
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      );
                    },
                  );
                }
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryChip(String category, String label) {
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: FilterChip(
        label: Text(label),
        selected: selectedCategory == category,
        onSelected: (selected) {
          setState(() {
            selectedCategory = category;
          });
        },
      ),
    );
  }
}
