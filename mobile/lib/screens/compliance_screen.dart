import 'package:flutter/material.dart';
import 'dart:convert';
import '../services/authenticated_http.dart';
import '../services/authenticated_dio.dart';

class ComplianceScreen extends StatefulWidget {
  const ComplianceScreen({Key? key}) : super(key: key);

  @override
  State<ComplianceScreen> createState() => _ComplianceScreenState();
}

class _ComplianceScreenState extends State<ComplianceScreen> {
  Map<String, dynamic>? compliance;
  List<dynamic> auditLogs = [];
  bool loading = false;

  @override
  void initState() {
    super.initState();
    fetchCompliance();
  }

  Future<void> fetchCompliance() async {
    setState(() => loading = true);
    try {
      final res1 = await authenticatedHttp.get(Uri.parse('$kApiBaseUrl/compliance/status'));
      final res2 = await authenticatedHttp.get(Uri.parse('$kApiBaseUrl/audit/logs'));
      if (res1.statusCode == 200 && res2.statusCode == 200) {
        setState(() {
          compliance = jsonDecode(res1.body);
          auditLogs = jsonDecode(res2.body);
        });
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  Widget statusCard(String title, bool compliant) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(
              compliant ? '✓ Compliant' : '✗ Non-compliant',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: compliant ? Colors.green : Colors.red,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Compliance & Legal')),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (compliance != null) ...[
                  GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    children: [
                      statusCard('GDPR', compliance!['gdpr'] ?? false),
                      statusCard('CCPA', compliance!['ccpa'] ?? false),
                    ],
                  ),
                  const SizedBox(height: 24),
                ],
                const Text('Audit Trail', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                ...auditLogs.map((log) => Card(
                  child: ListTile(
                    title: Text(log['action'] ?? 'N/A'),
                    subtitle: Text(log['resource'] ?? 'N/A'),
                  ),
                )),
              ],
            ),
    );
  }
}
