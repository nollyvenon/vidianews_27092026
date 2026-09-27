import 'package:flutter/material.dart'

class VideoProcessingScreen extends StatelessWidget {
  const VideoProcessingScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final videos = [
      {'name': 'Tutorial.mp4', 'status': 'completed', 'progress': 1.0},
      {'name': 'Guide.mp4', 'status': 'processing', 'progress': 0.65},
      {'name': 'Demo.mp4', 'status': 'pending', 'progress': 0.0},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Video Processing')),
      body: ListView.builder(
        itemCount: videos.length,
        itemBuilder: (context, index) {
          final video = videos[index];
          return Card(
            margin: const EdgeInsets.all(8),
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(video['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                      Chip(label: Text(video['status']), backgroundColor: Colors.blue[100]),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: video['progress'] as double,
                      minHeight: 8,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text('${((video['progress'] as double) * 100).toStringAsFixed(0)}% complete', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
