import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AnalyticsScreen extends StatefulWidget {
  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  late Future<Map<String, dynamic>> futureStats;

  @override
  void initState() {
    super.initState();
    futureStats = fetchAnalytics();
  }

  Future<Map<String, dynamic>> fetchAnalytics() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/system/health'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('Error: $e');
      return {};
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Analytics'),
        elevation: 0,
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: futureStats,
        builder: (context, snapshot) {
          if (snapshot.hasData && snapshot.data!.isNotEmpty) {
            final data = snapshot.data!;
            return SingleChildScrollView(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('System Health', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  SizedBox(height: 16),
                  _HealthMetricCard('CPU Usage', '${data['cpu_usage'] ?? 0}%'),
                  _HealthMetricCard('Memory Usage', '${data['memory_usage'] ?? 0}%'),
                  _HealthMetricCard('Disk Usage', '${data['disk_usage'] ?? 0}%'),
                  _HealthMetricCard('API Response Time', '${data['api_response_time'] ?? 0}ms'),
                  _HealthMetricCard('Uptime', '${data['uptime_percentage'] ?? 0}%'),
                ],
              ),
            );
          } else if (snapshot.hasError) {
            return Center(child: Text('Error loading analytics'));
          }
          return Center(child: CircularProgressIndicator());
        },
      ),
    );
  }
}

class _HealthMetricCard extends StatelessWidget {
  final String label;
  final String value;

  _HealthMetricCard(this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: TextStyle(fontSize: 16)),
            Text(value, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
