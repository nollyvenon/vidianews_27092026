import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:aether_cms/models/ecommerce_extended_models.dart';
import 'package:aether_cms/screens/ecommerce/addresses_screen.dart';
import 'package:aether_cms/screens/ecommerce/order_tracking_screen.dart';
import 'package:aether_cms/screens/ecommerce/wishlists_screen.dart';
import 'package:aether_cms/services/ecommerce_service.dart';

class MockEcommerceService extends Mock implements EcommerceService {}

const _gifts = Wishlist(id: 3, name: 'Gifts', isPublic: false, shareToken: 'tok');
const _item = WishlistItem(id: 11, wishlistId: 3, productId: 42, priority: 0);

const _home = ShippingAddress(
  id: 1,
  firstName: 'Ada',
  lastName: 'Lovelace',
  streetAddress: '1 Main St',
  city: 'London',
  postalCode: 'W1',
  country: 'UK',
  isDefault: true,
);

void main() {
  late MockEcommerceService service;

  setUp(() {
    service = MockEcommerceService();
    registerFallbackValue(<String, dynamic>{});
  });

  group('WishlistsScreen', () {
    testWidgets('shows the lists and the products of the selected list', (tester) async {
      when(() => service.fetchWishlists()).thenAnswer((_) async => [_gifts]);
      when(() => service.fetchWishlistItems(3)).thenAnswer((_) async => [_item]);

      await tester.pumpWidget(MaterialApp(home: WishlistsScreen(service: service)));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const Key('wishlist-3')));
      await tester.pumpAndSettle();

      expect(find.text('Share token: tok'), findsNothing);
      expect(find.text('Product #42'), findsOneWidget);
    });

    testWidgets('shows the empty state', (tester) async {
      when(() => service.fetchWishlists()).thenAnswer((_) async => []);

      await tester.pumpWidget(MaterialApp(home: WishlistsScreen(service: service)));
      await tester.pumpAndSettle();

      expect(find.text('You have no wishlists yet.'), findsOneWidget);
    });

    testWidgets('creates a list and selects it', (tester) async {
      when(() => service.fetchWishlists()).thenAnswer((_) async => []);
      when(() => service.createWishlist(name: 'Later', isPublic: false))
          .thenAnswer((_) async => const Wishlist(id: 4, name: 'Later', isPublic: false, shareToken: 't4'));
      when(() => service.fetchWishlistItems(4)).thenAnswer((_) async => []);

      await tester.pumpWidget(MaterialApp(home: WishlistsScreen(service: service)));
      await tester.pumpAndSettle();
      await tester.enterText(find.byKey(const Key('wishlist-name-field')), 'Later');
      await tester.tap(find.byKey(const Key('create-wishlist')));
      await tester.pumpAndSettle();

      verify(() => service.createWishlist(name: 'Later', isPublic: false)).called(1);
      expect(find.text('Wishlist "Later" created.'), findsOneWidget);
    });

    testWidgets('refuses an empty product number', (tester) async {
      when(() => service.fetchWishlists()).thenAnswer((_) async => [_gifts]);
      when(() => service.fetchWishlistItems(3)).thenAnswer((_) async => []);

      await tester.pumpWidget(MaterialApp(home: WishlistsScreen(service: service)));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const Key('wishlist-3')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const Key('add-wishlist-product')));
      await tester.pumpAndSettle();

      expect(find.text('Enter a valid product number.'), findsOneWidget);
      verifyNever(() => service.addWishlistItem(any(), any()));
    });

    testWidgets('removes an item from the list', (tester) async {
      when(() => service.fetchWishlists()).thenAnswer((_) async => [_gifts]);
      when(() => service.fetchWishlistItems(3)).thenAnswer((_) async => [_item]);
      when(() => service.removeWishlistItem(11)).thenAnswer((_) async {});

      await tester.pumpWidget(MaterialApp(home: WishlistsScreen(service: service)));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const Key('wishlist-3')));
      await tester.pumpAndSettle();
      await tester.tap(find.byTooltip('Remove'));
      await tester.pumpAndSettle();

      verify(() => service.removeWishlistItem(11)).called(1);
    });
  });

  group('AddressesScreen', () {
    testWidgets('lists saved addresses with the default marked', (tester) async {
      when(() => service.fetchAddresses()).thenAnswer((_) async => [_home]);

      await tester.pumpWidget(MaterialApp(home: AddressesScreen(service: service)));
      await tester.pumpAndSettle();

      expect(find.text('Ada Lovelace (default)'), findsOneWidget);
      expect(find.text('1 Main St, London W1, UK'), findsOneWidget);
    });

    testWidgets('requires the mandatory fields before saving', (tester) async {
      tester.view.devicePixelRatio = 1.0;
      tester.view.physicalSize = const Size(800, 1800);
      addTearDown(tester.view.reset);
      when(() => service.fetchAddresses()).thenAnswer((_) async => []);

      await tester.pumpWidget(MaterialApp(home: AddressesScreen(service: service)));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const Key('save-address')));
      await tester.pumpAndSettle();

      expect(find.text('First name is required'), findsOneWidget);
      verifyNever(() => service.createAddress(any()));
    });

    testWidgets('saves a complete address', (tester) async {
      tester.view.devicePixelRatio = 1.0;
      tester.view.physicalSize = const Size(800, 1800);
      addTearDown(tester.view.reset);
      when(() => service.fetchAddresses()).thenAnswer((_) async => []);
      when(() => service.createAddress(any())).thenAnswer((_) async => _home);

      await tester.pumpWidget(MaterialApp(home: AddressesScreen(service: service)));
      await tester.pumpAndSettle();
      const fields = {
        'first_name': 'Ada',
        'last_name': 'Lovelace',
        'street_address': '1 Main St',
        'city': 'London',
        'postal_code': 'W1',
        'country': 'UK',
      };
      for (final entry in fields.entries) {
        await tester.enterText(find.byKey(Key('address-field-${entry.key}')), entry.value);
      }
      await tester.tap(find.byKey(const Key('save-address')));
      await tester.pumpAndSettle();

      final sent = verify(() => service.createAddress(captureAny())).captured.single as Map<String, dynamic>;
      expect(sent['city'], 'London');
      expect(sent['state'], isNull);
      expect(sent['is_default'], isFalse);
      expect(find.text('Address saved.'), findsOneWidget);
    });
  });

  group('OrderTrackingScreen', () {
    testWidgets('shows shipments, tracking history and returns for an order', (tester) async {
      when(() => service.fetchOrderShipments(9)).thenAnswer((_) async => [
            const Shipment(id: 5, orderId: 9, carrier: 'ups', trackingNumber: '1Z-9', status: 'in_transit'),
          ]);
      when(() => service.fetchTracking(5)).thenAnswer((_) async => [
            TrackingEvent(id: 1, status: 'picked_up', location: 'Dallas', timestamp: DateTime.utc(2026, 10, 10)),
          ]);
      when(() => service.fetchOrderReturns(9)).thenAnswer((_) async => [
            const ReturnRequest(id: 7, rmaNumber: 'RMA-7', reason: 'damaged', status: 'refunded', quantityRequested: 1, refundAmount: 20),
          ]);

      await tester.pumpWidget(MaterialApp(home: OrderTrackingScreen(service: service, initialOrderId: 9)));
      await tester.pumpAndSettle();

      expect(find.text('UPS 1Z-9'), findsOneWidget);
      expect(find.textContaining('picked_up · Dallas'), findsOneWidget);
      expect(find.text('RMA-7'), findsOneWidget);
      expect(find.text('refunded · 1 item(s) · refund 20.0'), findsOneWidget);
    });

    testWidgets('says when an order has not shipped', (tester) async {
      when(() => service.fetchOrderShipments(4)).thenAnswer((_) async => []);
      when(() => service.fetchOrderReturns(4)).thenAnswer((_) async => []);

      await tester.pumpWidget(MaterialApp(home: OrderTrackingScreen(service: service)));
      await tester.enterText(find.byKey(const Key('order-number-field')), '4');
      await tester.tap(find.byKey(const Key('open-order')));
      await tester.pumpAndSettle();

      expect(find.text('This order has not shipped yet.'), findsOneWidget);
      expect(find.text('No return requests for this order.'), findsOneWidget);
    });

    testWidgets('submits a return with the chosen reason and quantity', (tester) async {
      when(() => service.fetchOrderShipments(9)).thenAnswer((_) async => []);
      when(() => service.fetchOrderReturns(9)).thenAnswer((_) async => []);
      when(() => service.requestReturn(9, reason: 'wrong_item', quantity: 2, details: null))
          .thenAnswer((_) async => const ReturnRequest(id: 8, reason: 'wrong_item', status: 'initiated', quantityRequested: 2));

      await tester.pumpWidget(MaterialApp(home: OrderTrackingScreen(service: service, initialOrderId: 9)));
      await tester.pumpAndSettle();

      await tester.tap(find.byKey(const Key('return-reason')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Wrong item').last);
      await tester.pumpAndSettle();
      await tester.enterText(find.byKey(const Key('return-quantity')), '2');
      await tester.tap(find.byKey(const Key('request-return')));
      await tester.pumpAndSettle();

      verify(() => service.requestReturn(9, reason: 'wrong_item', quantity: 2, details: null)).called(1);
      expect(find.text('Your return request has been submitted.'), findsOneWidget);
    });

    testWidgets('refuses an order number that is not positive', (tester) async {
      await tester.pumpWidget(MaterialApp(home: OrderTrackingScreen(service: service)));
      await tester.enterText(find.byKey(const Key('order-number-field')), '0');
      await tester.tap(find.byKey(const Key('open-order')));
      await tester.pump();

      expect(find.text('Enter a valid order number.'), findsOneWidget);
      verifyNever(() => service.fetchOrderShipments(any()));
    });
  });
}
