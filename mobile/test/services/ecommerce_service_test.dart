import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/services/ecommerce_service.dart';

class MockDio extends Mock implements Dio {}

Response<dynamic> _response(dynamic data) => Response<dynamic>(
      data: data,
      statusCode: 200,
      requestOptions: RequestOptions(path: ''),
    );

void main() {
  late MockDio dio;
  late EcommerceService service;

  setUp(() {
    dio = MockDio();
    service = EcommerceService(dio);
  });

  test('fetchWishlists parses the customer wishlists', () async {
    when(() => dio.get<dynamic>('/wishlists')).thenAnswer((_) async => _response([
          {'id': 3, 'name': 'Gifts', 'description': null, 'is_public': true, 'share_token': 'tok'},
        ]));

    final lists = await service.fetchWishlists();

    expect(lists.single.name, 'Gifts');
    expect(lists.single.isPublic, isTrue);
    expect(lists.single.shareToken, 'tok');
  });

  test('createWishlist sends the name, description and visibility', () async {
    when(() => dio.post<dynamic>('/wishlists', data: any(named: 'data'))).thenAnswer((_) async => _response({
          'id': 4, 'name': 'Later', 'description': 'Someday', 'is_public': false, 'share_token': 't4',
        }));

    final created = await service.createWishlist(name: 'Later', description: 'Someday');

    expect(created.id, 4);
    final sent = verify(() => dio.post<dynamic>('/wishlists', data: captureAny(named: 'data'))).captured.single;
    expect(sent, {'name': 'Later', 'description': 'Someday', 'is_public': false});
  });

  test('addWishlistItem and removeWishlistItem call the item routes', () async {
    when(() => dio.post<dynamic>('/wishlists/3/items/42')).thenAnswer((_) async => _response({}));
    when(() => dio.delete<dynamic>('/wishlist-items/11')).thenAnswer((_) async => _response({}));

    await service.addWishlistItem(3, 42);
    await service.removeWishlistItem(11);

    verify(() => dio.post<dynamic>('/wishlists/3/items/42')).called(1);
    verify(() => dio.delete<dynamic>('/wishlist-items/11')).called(1);
  });

  test('fetchAddresses parses shipping addresses', () async {
    when(() => dio.get<dynamic>('/shipping-addresses')).thenAnswer((_) async => _response([
          {
            'id': 1, 'first_name': 'Ada', 'last_name': 'Lovelace', 'street_address': '1 Main St', 'city': 'London',
            'state': null, 'postal_code': 'W1', 'country': 'UK', 'phone': null, 'is_default': true,
          },
        ]));

    final addresses = await service.fetchAddresses();

    expect(addresses.single.city, 'London');
    expect(addresses.single.isDefault, isTrue);
    expect(addresses.single.state, isNull);
  });

  test('fetchProducts searches only when a query is given', () async {
    when(() => dio.get<dynamic>('/products')).thenAnswer((_) async => _response([{'id': 1}]));
    when(() => dio.get<dynamic>('/products/search', queryParameters: any(named: 'queryParameters')))
        .thenAnswer((_) async => _response([{'id': 2}]));

    expect(await service.fetchProducts(), [{'id': 1}]);
    expect(await service.fetchProducts(query: ' lamp '), [{'id': 2}]);
    final query = verify(() => dio.get<dynamic>('/products/search', queryParameters: captureAny(named: 'queryParameters')))
        .captured
        .single;
    expect(query, {'q': 'lamp'});
  });

  test('fetchOrderShipments and fetchTracking parse the shipment history', () async {
    when(() => dio.get<dynamic>('/orders/9/shipments')).thenAnswer((_) async => _response([
          {'id': 5, 'order_id': 9, 'carrier': 'ups', 'tracking_number': '1Z', 'status': 'in_transit'},
        ]));
    when(() => dio.get<dynamic>('/shipments/5/tracking')).thenAnswer((_) async => _response([
          {'id': 1, 'shipment_id': 5, 'status': 'picked_up', 'description': null, 'location': 'Dallas',
           'timestamp': '2026-10-10T10:00:00Z'},
        ]));

    final shipments = await service.fetchOrderShipments(9);
    final events = await service.fetchTracking(shipments.single.id);

    expect(shipments.single.carrier, 'ups');
    expect(events.single.location, 'Dallas');
    expect(events.single.timestamp.toUtc(), DateTime.utc(2026, 10, 10, 10));
  });

  test('requestReturn posts the reason, quantity and details', () async {
    when(() => dio.post<dynamic>('/orders/9/return', data: any(named: 'data'))).thenAnswer((_) async => _response({
          'id': 8, 'rma_number': 'RMA-1', 'reason': 'defective', 'status': 'initiated',
          'quantity_requested': 2, 'quantity_received': null, 'refund_amount': null, 'refund_method': null,
        }));

    final request = await service.requestReturn(9, reason: 'defective', quantity: 2, details: 'Cracked');

    expect(request.rmaNumber, 'RMA-1');
    final sent = verify(() => dio.post<dynamic>('/orders/9/return', data: captureAny(named: 'data'))).captured.single;
    expect(sent, {'reason': 'defective', 'quantity_requested': 2, 'reason_details': 'Cracked'});
  });

  test('a response that is not a list is rejected', () async {
    when(() => dio.get<dynamic>('/wishlists')).thenAnswer((_) async => _response({'detail': 'oops'}));

    expect(service.fetchWishlists(), throwsA(isA<FormatException>()));
  });
}
