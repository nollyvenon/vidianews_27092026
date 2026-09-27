import 'package:flutter/material.dart'

class PartnershipsScreen extends StatelessWidget {
  const PartnershipsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Partnerships')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        Card(child: ListTile(title: const Text('Brand XYZ'), subtitle: const Text('Brand Deal'))),
      ]),
    );
  }
}
