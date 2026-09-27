import 'package:flutter/material.dart'

class PremiumScreen extends StatelessWidget {
  const PremiumScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Premium')),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(children: const [
          Text('VidiNews Premium'),
          SizedBox(height: 8),
          Text('Active'),
        ]))),
      ])),
    );
  }
}
