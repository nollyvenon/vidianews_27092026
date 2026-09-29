import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AdminScreen extends StatefulWidget {
  @override
  State<AdminScreen> createState() => _AdminScreenState();
}

class _AdminScreenState extends State<AdminScreen> {
  late Future<List<dynamic>> futureAlerts;
  late Future<List<dynamic>> futureLogs;

  @override
  void initState() {
    super.initState();
    futureAlerts = fetchAlerts();
    futureLogs = fetchLogs();
  }

  Future<List<dynamic>> fetchAlerts() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/system/alerts'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  Future<List<dynamic>> fetchLogs() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/admin/logs'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Admin Panel'),
        elevation: 0,
      ),
      body: ListView(
        padding: EdgeInsets.all(16),
        children: [
          Text('System Alerts', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          SizedBox(height: 12),
          FutureBuilder<List<dynamic>>(
            future: futureAlerts,
            builder: (context, snapshot) {
              if (snapshot.hasData && snapshot.data!.isNotEmpty) {
                return Column(
                  children: snapshot.data!.take(5).map((alert) {
                    return Card(
                      margin: EdgeInsets.only(bottom: 12),
                      color: alert['severity'] == 'critical' ? Colors.red[50] : Colors.yellow[50],
                      child: Padding(
                        padding: EdgeInsets.all(12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              alert['alert_type'],
                              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                            ),
                            SizedBox(height: 4),
                            Text(
                              alert['message'],
                              style: TextStyle(fontSize: 12, color: Colors.grey),
                            ),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                );
              }
              return Text('No active alerts');
            },
          ),
          SizedBox(height: 24),
          Text('Recent Activity', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          SizedBox(height: 12),
          FutureBuilder<List<dynamic>>(
            future: futureLogs,
            builder: (context, snapshot) {
              if (snapshot.hasData && snapshot.data!.isNotEmpty) {
                return Column(
                  children: snapshot.data!.take(10).map((log) {
                    return ListTile(
                      title: Text('${log['action']} ${log['resource_type']}'),
                      subtitle: Text(DateTime.parse(log['created_at']).toString()),
                      trailing: Icon(Icons.arrow_forward),
                    );
                  }).toList(),
                );
              }
              return Text('No activity logs');
            },
          ),
        ],
      ),
    );
  }
}
