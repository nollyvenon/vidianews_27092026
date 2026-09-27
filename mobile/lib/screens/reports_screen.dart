import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({Key? key}) : super(key: key);

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  List<dynamic> reports = [];
  String reportType = 'views';
  bool loading = false;

  @override
  void initState() {
    super.initState();
    fetchReports();
  }

  Future<void> fetchReports() async {
    setState(() => loading = true);
    try {
      final res = await http.get(Uri.parse('http://localhost:8000/api/v1/reports'));
      if (res.statusCode == 200) {
        setState(() => reports = jsonDecode(res.body));
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  Future<void> generateReport() async {
    setState(() => loading = true);
    try {
      final res = await http.post(
        Uri.parse('http://localhost:8000/api/v1/reports'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'report_type': reportType}),
      );
      if (res.statusCode == 200) {
        fetchReports();
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Reports & Analytics')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                DropdownButton<String>(
                  value: reportType,
                  items: ['views', 'engagement', 'revenue', 'growth']
                      .map((t) => DropdownMenuItem(value: t, child: Text(t)))
                      .toList(),
                  onChanged: (v) => setState(() => reportType = v ?? 'views'),
                ),
                const SizedBox(height: 12),
                ElevatedButton.icon(
                  onPressed: loading ? null : generateReport,
                  icon: const Icon(Icons.bar_chart),
                  label: const Text('Generate Report'),
                ),
              ],
            ),
          ),
          Expanded(
            child: loading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: reports.length,
                    itemBuilder: (context, index) {
                      final report = reports[index];
                      return Card(
                        margin: const EdgeInsets.all(8),
                        child: ListTile(
                          title: Text('${report['type']} Report'),
                          subtitle: Text(report['generated'] ?? 'N/A'),
                          trailing: const Icon(Icons.download),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
