// Usage and quota models for the signed-in account.

class QuotaUsage {
  final int apiCalls;
  final int apiCallLimit;
  final double storageGb;
  final double bandwidthGb;

  const QuotaUsage({
    required this.apiCalls,
    required this.apiCallLimit,
    required this.storageGb,
    required this.bandwidthGb,
  });

  /// Share of the monthly API-call allowance used, between 0 and 1.
  double get apiCallRatio => apiCallLimit <= 0 ? 0 : (apiCalls / apiCallLimit).clamp(0.0, 1.0).toDouble();

  factory QuotaUsage.fromJson(Map<String, dynamic> json) => QuotaUsage(
        apiCalls: json['api_calls'] as int,
        apiCallLimit: json['api_call_limit'] as int,
        storageGb: (json['storage_gb'] as num).toDouble(),
        bandwidthGb: (json['bandwidth_gb'] as num).toDouble(),
      );
}
