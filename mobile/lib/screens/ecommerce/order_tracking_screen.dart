// Shipments, tracking history and return requests for one of the customer's orders.

import 'package:flutter/material.dart';
import '../../models/ecommerce_extended_models.dart';
import '../../services/authenticated_dio.dart';
import '../../services/ecommerce_service.dart';

class OrderTrackingScreen extends StatefulWidget {
  final EcommerceService? service;
  final int? initialOrderId;

  const OrderTrackingScreen({Key? key, this.service, this.initialOrderId}) : super(key: key);

  @override
  State<OrderTrackingScreen> createState() => _OrderTrackingScreenState();
}

class _OrderTrackingScreenState extends State<OrderTrackingScreen> {
  late final EcommerceService _service = widget.service ?? EcommerceService(createAuthenticatedDio());
  final _orderController = TextEditingController();
  final _quantityController = TextEditingController(text: '1');
  final _detailsController = TextEditingController();

  int? _orderId;
  String _reason = kReturnReasons.first.key;
  Future<_OrderView>? _view;

  @override
  void initState() {
    super.initState();
    if (widget.initialOrderId != null) {
      _orderController.text = '${widget.initialOrderId}';
      _open(widget.initialOrderId!);
    }
  }

  @override
  void dispose() {
    _orderController.dispose();
    _quantityController.dispose();
    _detailsController.dispose();
    super.dispose();
  }

  void _openFromField() {
    final id = int.tryParse(_orderController.text.trim());
    if (id == null || id <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Enter a valid order number.')));
      return;
    }
    _open(id);
  }

  void _open(int orderId) {
    setState(() {
      _orderId = orderId;
      _view = _load(orderId);
    });
  }

  Future<_OrderView> _load(int orderId) async {
    final shipments = await _service.fetchOrderShipments(orderId);
    final tracking = <int, List<TrackingEvent>>{};
    for (final shipment in shipments) {
      tracking[shipment.id] = await _service.fetchTracking(shipment.id);
    }
    final returns = await _service.fetchOrderReturns(orderId);
    return _OrderView(shipments: shipments, tracking: tracking, returns: returns);
  }

  Future<void> _requestReturn() async {
    final orderId = _orderId;
    if (orderId == null) return;
    final quantity = int.tryParse(_quantityController.text.trim());
    if (quantity == null || quantity < 1) {
      _notify('Enter how many items you are returning.');
      return;
    }
    try {
      await _service.requestReturn(
        orderId,
        reason: _reason,
        quantity: quantity,
        details: _detailsController.text.trim().isEmpty ? null : _detailsController.text.trim(),
      );
      _detailsController.clear();
      _notify('Your return request has been submitted.');
      _open(orderId);
    } catch (error) {
      _notify(messageFromError(error));
    }
  }

  void _notify(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Order tracking')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              Expanded(
                child: TextField(
                  key: const Key('order-number-field'),
                  controller: _orderController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(labelText: 'Order number'),
                ),
              ),
              const SizedBox(width: 12),
              ElevatedButton(
                key: const Key('open-order'),
                onPressed: _openFromField,
                child: const Text('Open'),
              ),
            ],
          ),
          const SizedBox(height: 16),
          if (_view != null)
            FutureBuilder<_OrderView>(
              future: _view,
              builder: (context, snapshot) {
                if (snapshot.connectionState != ConnectionState.done) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return Text(messageFromError(snapshot.error!), style: const TextStyle(color: Colors.red));
                }
                return _details(snapshot.data!);
              },
            ),
        ],
      ),
    );
  }

  Widget _details(_OrderView view) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text('Shipping', style: Theme.of(context).textTheme.titleMedium),
        if (view.shipments.isEmpty)
          const Text('This order has not shipped yet.'),
        for (final shipment in view.shipments) ...[
          ListTile(
            key: Key('shipment-${shipment.id}'),
            contentPadding: EdgeInsets.zero,
            title: Text('${shipment.carrier.toUpperCase()} ${shipment.trackingNumber ?? ''}'),
            subtitle: Text('Status: ${shipment.status ?? 'unknown'}'),
          ),
          if ((view.tracking[shipment.id] ?? const []).isEmpty)
            const Padding(
              padding: EdgeInsets.only(left: 16, bottom: 8),
              child: Text('No tracking updates yet.'),
            ),
          for (final event in view.tracking[shipment.id] ?? const <TrackingEvent>[])
            Padding(
              padding: const EdgeInsets.only(left: 16, bottom: 8),
              child: Text(
                '${event.status}${event.location != null ? ' · ${event.location}' : ''}'
                '${event.description != null ? ' — ${event.description}' : ''}\n'
                '${event.timestamp.toLocal()}',
              ),
            ),
        ],
        const Divider(height: 32),
        Text('Returns', style: Theme.of(context).textTheme.titleMedium),
        if (view.returns.isEmpty) const Text('No return requests for this order.'),
        for (final item in view.returns)
          ListTile(
            contentPadding: EdgeInsets.zero,
            title: Text(item.rmaNumber ?? 'Return #${item.id}'),
            subtitle: Text(
              '${item.status} · ${item.quantityRequested} item(s)'
              '${item.refundAmount != null ? ' · refund ${item.refundAmount}' : ''}',
            ),
          ),
        const SizedBox(height: 12),
        DropdownButtonFormField<String>(
          key: const Key('return-reason'),
          initialValue: _reason,
          decoration: const InputDecoration(labelText: 'Reason'),
          items: [
            for (final reason in kReturnReasons) DropdownMenuItem(value: reason.key, child: Text(reason.value)),
          ],
          onChanged: (value) => setState(() => _reason = value ?? _reason),
        ),
        TextField(
          key: const Key('return-quantity'),
          controller: _quantityController,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'Items to return'),
        ),
        TextField(
          key: const Key('return-details'),
          controller: _detailsController,
          maxLines: 3,
          decoration: const InputDecoration(labelText: 'Details'),
        ),
        ElevatedButton(
          key: const Key('request-return'),
          onPressed: _requestReturn,
          child: const Text('Request a return'),
        ),
      ],
    );
  }
}

class _OrderView {
  final List<Shipment> shipments;
  final Map<int, List<TrackingEvent>> tracking;
  final List<ReturnRequest> returns;

  const _OrderView({required this.shipments, required this.tracking, required this.returns});
}
