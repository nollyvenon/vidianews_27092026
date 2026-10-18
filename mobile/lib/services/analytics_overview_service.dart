// Analytics overview for the signed-in creator: headline figures, daily engagement and daily revenue.

import 'package:dio/dio.dart';

class AnalyticsSummary {
  final int days;
  final int views;
  final double watchHours;
  final int subscribers;

  const AnalyticsSummary({
    required this.days,
    required this.views,
    required this.watchHours,
    required this.subscribers,
  });

  factory AnalyticsSummary.fromJson(Map<String, dynamic> json) => AnalyticsSummary(
        days: json['days'] as int,
        views: json['views'] as int,
        watchHours: (json['watch_hours'] as num).toDouble(),
        subscribers: json['subscribers'] as int,
      );
}

class EngagementRow {
  final String date;
  final int activeUsers;
  final int newUsers;

  const EngagementRow({required this.date, required this.activeUsers, required this.newUsers});

  factory EngagementRow.fromJson(Map<String, dynamic> json) => EngagementRow(
        date: json['date'] as String,
        activeUsers: json['active_users'] as int,
        newUsers: json['new_users'] as int,
      );
}

class RevenueRow {
  final String date;
  final double totalRevenue;
  final int transactionCount;

  const RevenueRow({required this.date, required this.totalRevenue, required this.transactionCount});

  factory RevenueRow.fromJson(Map<String, dynamic> json) => RevenueRow(
        date: json['date'] as String,
        totalRevenue: (json['total_revenue'] as num).toDouble(),
        transactionCount: json['transaction_count'] as int,
      );
}

class AnalyticsOverviewService {
  final Dio _dio;

  AnalyticsOverviewService(this._dio);

  Future<AnalyticsSummary> fetchSummary({int days = 30}) async {
    final response = await _dio.get<dynamic>('/analytics/summary', queryParameters: {'days': days});
    return AnalyticsSummary.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<EngagementRow>> fetchEngagement({int days = 30}) async {
    final response = await _dio.get<dynamic>('/analytics/engagement', queryParameters: {'days': days});
    return _rows(response.data).map(EngagementRow.fromJson).toList();
  }

  Future<List<RevenueRow>> fetchRevenue({int days = 30}) async {
    final end = DateTime.now().toUtc();
    final start = end.subtract(Duration(days: days));
    final response = await _dio.get<dynamic>('/analytics/revenue', queryParameters: {
      'start_date': start.toIso8601String(),
      'end_date': end.toIso8601String(),
    });
    return _rows(response.data).map(RevenueRow.fromJson).toList();
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
