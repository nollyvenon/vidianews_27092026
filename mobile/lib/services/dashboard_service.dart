// The signed-in user's dashboard totals and recent activity.

import 'package:dio/dio.dart';

class DashboardSummary {
  final int videos;
  final int articles;
  final int chats;
  final double monthlySpend;

  const DashboardSummary({
    required this.videos,
    required this.articles,
    required this.chats,
    required this.monthlySpend,
  });

  factory DashboardSummary.fromJson(Map<String, dynamic> json) => DashboardSummary(
        videos: json['videos'] as int,
        articles: json['articles'] as int,
        chats: json['chats'] as int,
        monthlySpend: (json['monthly_spend'] as num).toDouble(),
      );
}

class ActivityEntry {
  final int id;
  final String action;
  final String? description;
  final DateTime createdAt;

  const ActivityEntry({
    required this.id,
    required this.action,
    this.description,
    required this.createdAt,
  });

  factory ActivityEntry.fromJson(Map<String, dynamic> json) => ActivityEntry(
        id: json['id'] as int,
        action: json['action'] as String,
        description: json['description'] as String?,
        createdAt: DateTime.parse(json['created_at'] as String),
      );
}

class DashboardService {
  final Dio _dio;

  DashboardService(this._dio);

  Future<DashboardSummary> fetchSummary() async {
    final response = await _dio.get<dynamic>('/dashboard/summary');
    return DashboardSummary.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<ActivityEntry>> fetchRecentActivity({int limit = 5}) async {
    final response = await _dio.get<dynamic>('/activity/me', queryParameters: {'limit': limit});
    final data = response.data;
    if (data is! List) {
      throw const FormatException('Expected a list of activity from the server');
    }
    return data.cast<Map<String, dynamic>>().map(ActivityEntry.fromJson).toList();
  }
}
