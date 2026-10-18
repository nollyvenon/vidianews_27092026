// Cache statistics and policies, data pipelines and API usage for the platform operations screens.

class CacheStats {
  final int totalEntries;
  final int hotEntries;
  final int warmEntries;
  final int coldEntries;
  final int totalHits;
  final double avgHitsPerEntry;
  final double hitRate;

  const CacheStats({
    required this.totalEntries,
    required this.hotEntries,
    required this.warmEntries,
    required this.coldEntries,
    required this.totalHits,
    required this.avgHitsPerEntry,
    required this.hitRate,
  });

  factory CacheStats.fromJson(Map<String, dynamic> json) => CacheStats(
        totalEntries: json['total_entries'] as int,
        hotEntries: json['hot_entries'] as int,
        warmEntries: json['warm_entries'] as int,
        coldEntries: json['cold_entries'] as int,
        totalHits: json['total_hits'] as int,
        avgHitsPerEntry: (json['avg_hits_per_entry'] as num).toDouble(),
        hitRate: (json['hit_rate'] as num).toDouble(),
      );
}

class CachePolicy {
  final String resourceType;
  final String cacheType;
  final int ttlSeconds;
  final int maxSizeMb;
  final bool isActive;
  final int hits;
  final int misses;
  final double hitRate;

  const CachePolicy({
    required this.resourceType,
    required this.cacheType,
    required this.ttlSeconds,
    required this.maxSizeMb,
    required this.isActive,
    required this.hits,
    required this.misses,
    required this.hitRate,
  });

  factory CachePolicy.fromJson(Map<String, dynamic> json) => CachePolicy(
        resourceType: json['resource_type'] as String,
        cacheType: json['cache_type'] as String,
        ttlSeconds: json['ttl_seconds'] as int,
        maxSizeMb: json['max_size_mb'] as int,
        isActive: json['is_active'] as bool,
        hits: json['hits'] as int,
        misses: json['misses'] as int,
        hitRate: (json['hit_rate'] as num).toDouble(),
      );
}

class Pipeline {
  final int id;
  final String name;
  final String sourceType;
  final String destinationType;
  final String status;
  final bool isActive;
  final int failureCount;
  final DateTime? lastRun;
  final DateTime? lastSuccess;

  const Pipeline({
    required this.id,
    required this.name,
    required this.sourceType,
    required this.destinationType,
    required this.status,
    required this.isActive,
    required this.failureCount,
    this.lastRun,
    this.lastSuccess,
  });

  factory Pipeline.fromJson(Map<String, dynamic> json) => Pipeline(
        id: json['id'] as int,
        name: json['name'] as String,
        sourceType: json['source_type'] as String,
        destinationType: json['destination_type'] as String,
        status: json['status'] as String,
        isActive: json['is_active'] as bool,
        failureCount: json['failure_count'] as int? ?? 0,
        lastRun: _date(json['last_run']),
        lastSuccess: _date(json['last_success']),
      );
}

class ApiUsage {
  final int id;
  final String endpoint;
  final String method;
  final int callCount;
  final int errorCount;
  final double averageResponseTimeMs;

  const ApiUsage({
    required this.id,
    required this.endpoint,
    required this.method,
    required this.callCount,
    required this.errorCount,
    required this.averageResponseTimeMs,
  });

  /// Share of calls that failed, between 0 and 1.
  double get errorRate => callCount <= 0 ? 0 : (errorCount / callCount).clamp(0.0, 1.0).toDouble();

  factory ApiUsage.fromJson(Map<String, dynamic> json) => ApiUsage(
        id: json['id'] as int,
        endpoint: json['endpoint'] as String,
        method: json['method'] as String,
        callCount: json['call_count'] as int,
        errorCount: json['error_count'] as int,
        averageResponseTimeMs: (json['average_response_time_ms'] as num).toDouble(),
      );
}

DateTime? _date(Object? value) => value is String ? DateTime.tryParse(value) : null;
