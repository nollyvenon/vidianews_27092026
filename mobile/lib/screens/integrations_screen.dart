import 'package:flutter/material.dart'

class IntegrationsScreen extends StatefulWidget {
  const IntegrationsScreen({Key? key}) : super(key: key);

  @override
  State<IntegrationsScreen> createState() => _IntegrationsScreenState();
}

class _IntegrationsScreenState extends State<IntegrationsScreen> {
  final List<Map<String, String>> availableIntegrations = [
    {'name': 'Slack', 'icon': '💬', 'desc': 'Send notifications'},
    {'name': 'Zapier', 'icon': '⚡', 'desc': 'Automate workflows'},
    {'name': 'Stripe', 'icon': '💳', 'desc': 'Process payments'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Integrations')),
      body: ListView.builder(
        itemCount: availableIntegrations.length,
        itemBuilder: (context, index) {
          final integ = availableIntegrations[index];
          return Card(
            margin: const EdgeInsets.all(8),
            child: ListTile(
              leading: Text(integ['icon']!, style: const TextStyle(fontSize: 24)),
              title: Text(integ['name']!),
              subtitle: Text(integ['desc']!),
              trailing: const Icon(Icons.arrow_forward),
              onTap: () {},
            ),
          );
        },
      ),
    );
  }
}
