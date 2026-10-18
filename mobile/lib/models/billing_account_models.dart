// The signed-in account's subscription, invoices and payments.

String _capitalize(String value) => value.isEmpty ? value : '${value[0].toUpperCase()}${value.substring(1)}';

DateTime? _parseDate(Object? value) => value == null ? null : DateTime.parse(value as String);

class AccountSubscription {
  final int id;
  final String tier;
  final String? billingCycle;
  final double amount;
  final bool isActive;
  final DateTime? renewsAt;
  final DateTime? canceledAt;

  const AccountSubscription({
    required this.id,
    required this.tier,
    required this.billingCycle,
    required this.amount,
    required this.isActive,
    required this.renewsAt,
    required this.canceledAt,
  });

  String get tierLabel => _capitalize(tier);

  factory AccountSubscription.fromJson(Map<String, dynamic> json) => AccountSubscription(
        id: json['id'] as int,
        tier: (json['tier'] as String?) ?? 'free',
        billingCycle: json['billing_cycle'] as String?,
        amount: (json['amount'] as num).toDouble(),
        isActive: json['is_active'] as bool,
        renewsAt: _parseDate(json['renews_at']),
        canceledAt: _parseDate(json['canceled_at']),
      );
}

class AccountInvoice {
  final int id;
  final int subscriptionId;
  final double amount;
  final String? status;
  final DateTime? dueDate;
  final DateTime? paidDate;
  final DateTime? createdAt;

  const AccountInvoice({
    required this.id,
    required this.subscriptionId,
    required this.amount,
    required this.status,
    required this.dueDate,
    required this.paidDate,
    required this.createdAt,
  });

  bool get isPaid => status == 'completed';

  factory AccountInvoice.fromJson(Map<String, dynamic> json) => AccountInvoice(
        id: json['id'] as int,
        subscriptionId: json['subscription_id'] as int,
        amount: (json['amount'] as num).toDouble(),
        status: json['status'] as String?,
        dueDate: _parseDate(json['due_date']),
        paidDate: _parseDate(json['paid_date']),
        createdAt: _parseDate(json['created_at']),
      );
}

class AccountPayment {
  final int id;
  final int invoiceId;
  final double amount;
  final String? status;
  final String? paymentMethod;
  final DateTime? createdAt;

  const AccountPayment({
    required this.id,
    required this.invoiceId,
    required this.amount,
    required this.status,
    required this.paymentMethod,
    required this.createdAt,
  });

  factory AccountPayment.fromJson(Map<String, dynamic> json) => AccountPayment(
        id: json['id'] as int,
        invoiceId: json['invoice_id'] as int,
        amount: (json['amount'] as num).toDouble(),
        status: json['status'] as String?,
        paymentMethod: json['payment_method'] as String?,
        createdAt: _parseDate(json['created_at']),
      );
}
