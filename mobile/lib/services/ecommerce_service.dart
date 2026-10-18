// Shop API for the signed-in customer: catalogue, wishlists, shipping addresses, shipments and returns.

import 'package:dio/dio.dart';
import '../models/ecommerce_extended_models.dart';

class EcommerceService {
  final Dio _dio;

  EcommerceService(this._dio);

  Future<List<Map<String, dynamic>>> fetchProducts({String query = ''}) async {
    final response = query.trim().isEmpty
        ? await _dio.get<dynamic>('/products')
        : await _dio.get<dynamic>('/products/search', queryParameters: {'q': query.trim()});
    return _rows(response.data);
  }

  Future<List<Wishlist>> fetchWishlists() async {
    final response = await _dio.get<dynamic>('/wishlists');
    return _rows(response.data).map(Wishlist.fromJson).toList();
  }

  Future<Wishlist> createWishlist({required String name, String? description, bool isPublic = false}) async {
    final response = await _dio.post<dynamic>('/wishlists', data: {
      'name': name,
      'description': description,
      'is_public': isPublic,
    });
    return Wishlist.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<WishlistItem>> fetchWishlistItems(int wishlistId) async {
    final response = await _dio.get<dynamic>('/wishlists/$wishlistId/items');
    return _rows(response.data).map(WishlistItem.fromJson).toList();
  }

  Future<void> addWishlistItem(int wishlistId, int productId) async {
    await _dio.post<dynamic>('/wishlists/$wishlistId/items/$productId');
  }

  Future<void> removeWishlistItem(int itemId) async {
    await _dio.delete<dynamic>('/wishlist-items/$itemId');
  }

  Future<List<ShippingAddress>> fetchAddresses() async {
    final response = await _dio.get<dynamic>('/shipping-addresses');
    return _rows(response.data).map(ShippingAddress.fromJson).toList();
  }

  Future<ShippingAddress> createAddress(Map<String, dynamic> address) async {
    final response = await _dio.post<dynamic>('/shipping-addresses', data: address);
    return ShippingAddress.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<Shipment>> fetchOrderShipments(int orderId) async {
    final response = await _dio.get<dynamic>('/orders/$orderId/shipments');
    return _rows(response.data).map(Shipment.fromJson).toList();
  }

  Future<List<TrackingEvent>> fetchTracking(int shipmentId) async {
    final response = await _dio.get<dynamic>('/shipments/$shipmentId/tracking');
    return _rows(response.data).map(TrackingEvent.fromJson).toList();
  }

  Future<List<ReturnRequest>> fetchOrderReturns(int orderId) async {
    final response = await _dio.get<dynamic>('/orders/$orderId/returns');
    return _rows(response.data).map(ReturnRequest.fromJson).toList();
  }

  Future<ReturnRequest> requestReturn(
    int orderId, {
    required String reason,
    required int quantity,
    String? details,
  }) async {
    final response = await _dio.post<dynamic>('/orders/$orderId/return', data: {
      'reason': reason,
      'quantity_requested': quantity,
      'reason_details': details,
    });
    return ReturnRequest.fromJson(response.data as Map<String, dynamic>);
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
