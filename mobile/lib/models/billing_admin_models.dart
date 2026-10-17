// Admin models for subscriptions and transactions.

class SubscriptionAdmin {
  final int id;
  final int userId;
  final String? userEmail;
  final String? tier;
  final String? billingCycle;
  final double amount;
  final bool isActive;
  final DateTime? renewsAt;
  final DateTime? canceledAt;

  const SubscriptionAdmin({
    required this.id,
    required this.userId,
    required this.userEmail,
    required this.tier,
    required this.billingCycle,
    required this.amount,
    required this.isActive,
    required this.renewsAt,
    required this.canceledAt,
  });

  factory SubscriptionAdmin.fromJson(Map<String, dynamic> json) => SubscriptionAdmin(
        id: json['id'] as int,
        userId: json['user_id'] as int,
        userEmail: json['user_email'] as String?,
        tier: json['tier'] as String?,
        billingCycle: json['billing_cycle'] as String?,
        amount: (json['amount'] as num).toDouble(),
        isActive: json['is_active'] as bool,
        renewsAt: _parseDate(json['renews_at']),
        canceledAt: _parseDate(json['canceled_at']),
      );
}

class TransactionAdmin {
  final String source;
  final int id;
  final String? userEmail;
  final double amount;
  final String currency;
  final String? status;
  final String? paymentMethod;
  final String? reference;
  final DateTime? createdAt;

  const TransactionAdmin({
    required this.source,
    required this.id,
    required this.userEmail,
    required this.amount,
    required this.currency,
    required this.status,
    required this.paymentMethod,
    required this.reference,
    required this.createdAt,
  });

  factory TransactionAdmin.fromJson(Map<String, dynamic> json) => TransactionAdmin(
        source: json['source'] as String,
        id: json['id'] as int,
        userEmail: json['user_email'] as String?,
        amount: (json['amount'] as num).toDouble(),
        currency: (json['currency'] as String?) ?? 'USD',
        status: json['status'] as String?,
        paymentMethod: json['payment_method'] as String?,
        reference: json['reference'] as String?,
        createdAt: _parseDate(json['created_at']),
      );
}

class AdminPage<T> {
  final List<T> items;
  final int total;

  const AdminPage({required this.items, required this.total});

  factory AdminPage.fromJson(Map<String, dynamic> json, T Function(Map<String, dynamic>) parseItem) => AdminPage(
        items: (json['items'] as List<dynamic>)
            .map((item) => parseItem(item as Map<String, dynamic>))
            .toList(),
        total: json['total'] as int,
      );
}

DateTime? _parseDate(Object? value) => value == null ? null : DateTime.parse(value as String);
