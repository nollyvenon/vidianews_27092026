import 'package:flutter/material.dart'

class SecurityScreen extends StatefulWidget {
  const SecurityScreen({Key? key}) : super(key: key);

  @override
  State<SecurityScreen> createState() => _SecurityScreenState();
}

class _SecurityScreenState extends State<SecurityScreen> {
  bool mfaEnabled = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Security Settings')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Rate Limiting', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('API Requests: 850/1000'),
                    SizedBox(height: 8),
                    LinearProgressIndicator(value: 0.85),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Two-Factor Authentication', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('MFA Status'),
                    Switch(
                      value: mfaEnabled,
                      onChanged: (value) => setState(() => mfaEnabled = value),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Connected Accounts', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ListTile(
              title: const Text('Google'),
              trailing: const Text('Connected', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
              tileColor: Colors.green.shade50,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ],
        ),
      ),
    );
  }
}
