// Encoding progress for the signed-in creator's videos.

import 'package:flutter/material.dart';
import '../models/discovery_models.dart';
import '../services/authenticated_dio.dart';
import '../services/discovery_service.dart';
import '../widgets/async_view.dart';

class VideoProcessingScreen extends StatefulWidget {
  final DiscoveryService? service;

  const VideoProcessingScreen({Key? key, this.service}) : super(key: key);

  @override
  State<VideoProcessingScreen> createState() => _VideoProcessingScreenState();
}

class _VideoProcessingScreenState extends State<VideoProcessingScreen> {
  late final DiscoveryService _service = widget.service ?? DiscoveryService(createAuthenticatedDio());
  late Future<List<VideoJob>> _jobs = _service.fetchVideoJobs();

  void _reload() {
    setState(() {
      _jobs = _service.fetchVideoJobs();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Video processing')),
      body: AsyncView<List<VideoJob>>(
        future: _jobs,
        onRetry: _reload,
        builder: (context, jobs) {
          if (jobs.isEmpty) {
            return const Center(child: Text('No videos are being processed.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: jobs.length,
            itemBuilder: (context, index) {
              final job = jobs[index];
              return Card(
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(job.title, key: Key('job-${job.contentId}')),
                      const SizedBox(height: 4),
                      Text('${job.status} · ${job.progress}%'),
                      const SizedBox(height: 6),
                      LinearProgressIndicator(value: job.progress / 100),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
