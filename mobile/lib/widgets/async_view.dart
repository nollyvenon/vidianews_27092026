// Shared loading, error and retry state for screens that load one future.

import 'package:flutter/material.dart';
import '../services/authenticated_dio.dart';

/// Shows a spinner while [future] runs, the server's message with a retry button when it fails,
/// and otherwise [builder] applied to the loaded value.
class AsyncView<T> extends StatelessWidget {
  final Future<T> future;
  final Widget Function(BuildContext context, T data) builder;
  final VoidCallback onRetry;

  const AsyncView({
    Key? key,
    required this.future,
    required this.builder,
    required this.onRetry,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<T>(
      future: future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(
            child: Padding(padding: EdgeInsets.all(24), child: CircularProgressIndicator()),
          );
        }
        if (snapshot.hasError) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    messageFromError(snapshot.error!),
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(height: 8),
                  TextButton(onPressed: onRetry, child: const Text('Try again')),
                ],
              ),
            ),
          );
        }
        return builder(context, snapshot.requireData);
      },
    );
  }
}
