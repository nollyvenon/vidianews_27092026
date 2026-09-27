import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import '../models/advanced_platform_models.dart';

const String baseUrl = 'http://localhost:8000/api/v1';

class AdvancedPlatformService {
  final String _baseUrl;
  late WebSocketChannel _webSocketChannel;

  AdvancedPlatformService({String? baseUrl}) : _baseUrl = baseUrl ?? baseUrl;

  // WebSocket Methods
  Future<void> connectWebSocket(int userId, String connectionId) async {
    try {
      _webSocketChannel = WebSocketChannel.connect(
        Uri.parse('ws://localhost:8000/api/v1/websocket/ws/$userId/$connectionId'),
      );
    } catch (e) {
      throw Exception('Failed to connect WebSocket: $e');
    }
  }

  Stream<dynamic> get webSocketStream => _webSocketChannel.stream;

  Future<void> sendWebSocketMessage(Map<String, dynamic> message) async {
    _webSocketChannel.sink.add(jsonEncode(message));
  }

  Future<void> disconnectWebSocket() async {
    await _webSocketChannel.sink.close();
  }

  // Background Job Methods
  Future<BackgroundJob> createJob({
    required String jobType,
    required Map<String, dynamic> payload,
    int? userId,
    int priority = 0,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/jobs/create'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'job_type': jobType,
        'payload': payload,
        'user_id': userId,
        'priority': priority,
      }),
    );

    if (response.statusCode == 200) {
      return BackgroundJob.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to create job');
  }

  Future<List<BackgroundJob>> getPendingJobs({int limit = 50}) async {
    final uri = Uri.parse('$_baseUrl/jobs/pending').replace(
      queryParameters: {'limit': limit.toString()},
    );
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => BackgroundJob.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch pending jobs');
  }

  // Data Pipeline Methods
  Future<DataPipeline> createPipeline({
    required String name,
    required String sourceType,
    required String destinationType,
    required Map<String, dynamic> config,
    Map<String, dynamic>? transformationRules,
    String? schedule,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/pipelines/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'source_type': sourceType,
        'destination_type': destinationType,
        'config': config,
        'transformation_rules': transformationRules,
        'schedule': schedule,
      }),
    );

    if (response.statusCode == 200) {
      return DataPipeline.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to create pipeline');
  }

  Future<PipelineExecution> executePipeline(int pipelineId) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/pipelines/$pipelineId/execute'),
    );

    if (response.statusCode == 200) {
      return PipelineExecution.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to execute pipeline');
  }

  // Cache Methods
  Future<void> setCacheEntry({
    required String cacheKey,
    required Map<String, dynamic> cacheValue,
    int? ttlSeconds,
    String strategy = 'ttl',
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/cache/set'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'cache_key': cacheKey,
        'cache_value': cacheValue,
        'ttl_seconds': ttlSeconds,
        'strategy': strategy,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to set cache entry');
    }
  }

  Future<Map<String, dynamic>?> getCacheEntry(String cacheKey) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/cache/get/$cacheKey'),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else if (response.statusCode == 404) {
      return null;
    }
    throw Exception('Failed to get cache entry');
  }

  Future<CacheMetrics> getCacheMetrics() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/cache/metrics'),
    );

    if (response.statusCode == 200) {
      return CacheMetrics.fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to fetch cache metrics');
  }

  // API Documentation Methods
  Future<APIDocumentation> createDocumentation({
    required String name,
    required String format,
    required Map<String, dynamic> spec,
    String version = '1.0.0',
    String? description,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/api-docs/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'format': format,
        'spec': spec,
        'version': version,
        'description': description,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return APIDocumentation(
        id: data['id'],
        name: data['name'],
        format: data['format'],
        version: data['version'] ?? '1.0.0',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );
    }
    throw Exception('Failed to create documentation');
  }

  Future<List<APIEndpoint>> getDocumentationEndpoints(int docId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/api-docs/$docId/endpoints'),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => APIEndpoint.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch endpoints');
  }

  Future<List<APIUsageMetrics>> getAPIUsageMetrics(String endpoint) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/api-docs/usage/$endpoint'),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => APIUsageMetrics.fromJson(item)).toList();
    }
    throw Exception('Failed to fetch usage metrics');
  }
}

final advancedPlatformServiceProvider = Provider((ref) {
  return AdvancedPlatformService();
});

final pendingJobsProvider = FutureProvider<List<BackgroundJob>>((ref) async {
  final service = ref.watch(advancedPlatformServiceProvider);
  return service.getPendingJobs();
});

final cacheMetricsProvider = FutureProvider<CacheMetrics>((ref) async {
  final service = ref.watch(advancedPlatformServiceProvider);
  return service.getCacheMetrics();
});

final cacheEntryProvider = FutureProvider.family<Map<String, dynamic>?, String>(
  (ref, cacheKey) async {
    final service = ref.watch(advancedPlatformServiceProvider);
    return service.getCacheEntry(cacheKey);
  },
);

final apiUsageMetricsProvider = FutureProvider.family<List<APIUsageMetrics>, String>(
  (ref, endpoint) async {
    final service = ref.watch(advancedPlatformServiceProvider);
    return service.getAPIUsageMetrics(endpoint);
  },
);

final webSocketProvider = StreamProvider<dynamic>((ref) async* {
  final service = ref.watch(advancedPlatformServiceProvider);
  yield* service.webSocketStream;
});
