// Wishlists, shipping addresses, shipments, tracking and returns for the signed-in customer.

class Wishlist {
  final int id;
  final String name;
  final String? description;
  final bool isPublic;
  final String shareToken;

  const Wishlist({
    required this.id,
    required this.name,
    this.description,
    required this.isPublic,
    required this.shareToken,
  });

  factory Wishlist.fromJson(Map<String, dynamic> json) => Wishlist(
        id: json['id'] as int,
        name: json['name'] as String,
        description: json['description'] as String?,
        isPublic: json['is_public'] as bool? ?? false,
        shareToken: json['share_token'] as String,
      );
}

class WishlistItem {
  final int id;
  final int wishlistId;
  final int productId;
  final int priority;
  final String? notes;

  const WishlistItem({
    required this.id,
    required this.wishlistId,
    required this.productId,
    required this.priority,
    this.notes,
  });

  factory WishlistItem.fromJson(Map<String, dynamic> json) => WishlistItem(
        id: json['id'] as int,
        wishlistId: json['wishlist_id'] as int,
        productId: json['product_id'] as int,
        priority: json['priority'] as int? ?? 0,
        notes: json['notes'] as String?,
      );
}

class ShippingAddress {
  final int id;
  final String firstName;
  final String lastName;
  final String streetAddress;
  final String city;
  final String? state;
  final String postalCode;
  final String country;
  final String? phone;
  final bool isDefault;

  const ShippingAddress({
    required this.id,
    required this.firstName,
    required this.lastName,
    required this.streetAddress,
    required this.city,
    this.state,
    required this.postalCode,
    required this.country,
    this.phone,
    required this.isDefault,
  });

  factory ShippingAddress.fromJson(Map<String, dynamic> json) => ShippingAddress(
        id: json['id'] as int,
        firstName: json['first_name'] as String,
        lastName: json['last_name'] as String,
        streetAddress: json['street_address'] as String,
        city: json['city'] as String,
        state: json['state'] as String?,
        postalCode: json['postal_code'] as String,
        country: json['country'] as String,
        phone: json['phone'] as String?,
        isDefault: json['is_default'] as bool? ?? false,
      );
}

class Shipment {
  final int id;
  final int orderId;
  final String carrier;
  final String? trackingNumber;
  final String? status;

  const Shipment({
    required this.id,
    required this.orderId,
    required this.carrier,
    this.trackingNumber,
    this.status,
  });

  factory Shipment.fromJson(Map<String, dynamic> json) => Shipment(
        id: json['id'] as int,
        orderId: json['order_id'] as int,
        carrier: json['carrier'] as String,
        trackingNumber: json['tracking_number'] as String?,
        status: json['status'] as String?,
      );
}

class TrackingEvent {
  final int id;
  final String status;
  final String? description;
  final String? location;
  final DateTime timestamp;

  const TrackingEvent({
    required this.id,
    required this.status,
    this.description,
    this.location,
    required this.timestamp,
  });

  factory TrackingEvent.fromJson(Map<String, dynamic> json) => TrackingEvent(
        id: json['id'] as int,
        status: json['status'] as String,
        description: json['description'] as String?,
        location: json['location'] as String?,
        timestamp: DateTime.parse(json['timestamp'] as String),
      );
}

class ReturnRequest {
  final int id;
  final String? rmaNumber;
  final String reason;
  final String status;
  final int quantityRequested;
  final int? quantityReceived;
  final double? refundAmount;
  final String? refundMethod;

  const ReturnRequest({
    required this.id,
    this.rmaNumber,
    required this.reason,
    required this.status,
    required this.quantityRequested,
    this.quantityReceived,
    this.refundAmount,
    this.refundMethod,
  });

  factory ReturnRequest.fromJson(Map<String, dynamic> json) => ReturnRequest(
        id: json['id'] as int,
        rmaNumber: json['rma_number'] as String?,
        reason: json['reason'] as String,
        status: json['status'] as String,
        quantityRequested: json['quantity_requested'] as int,
        quantityReceived: json['quantity_received'] as int?,
        refundAmount: (json['refund_amount'] as num?)?.toDouble(),
        refundMethod: json['refund_method'] as String?,
      );
}

/// Return reasons offered to customers, with the labels shown on screen.
const List<MapEntry<String, String>> kReturnReasons = [
  MapEntry('damaged', 'Arrived damaged'),
  MapEntry('defective', 'Defective'),
  MapEntry('not_as_described', 'Not as described'),
  MapEntry('wrong_item', 'Wrong item'),
  MapEntry('no_longer_needed', 'No longer needed'),
  MapEntry('size_issue', 'Size does not fit'),
  MapEntry('color_issue', 'Colour is different'),
  MapEntry('other', 'Other'),
];
