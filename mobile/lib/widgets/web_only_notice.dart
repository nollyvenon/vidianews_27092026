// Shown by administration tools that are used from the web dashboard rather than the mobile app.

import 'package:flutter/material.dart';

class WebOnlyNotice extends StatelessWidget {
  final String title;

  const WebOnlyNotice({Key? key, required this.title}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.desktop_windows_outlined, size: 48),
              const SizedBox(height: 16),
              Text(
                '$title is an administration tool. Use it from the web dashboard.',
                key: const Key('web-only-notice'),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
