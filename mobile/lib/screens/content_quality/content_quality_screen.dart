// Content quality: how the organization's checks score overall, and the tools to run each check.

import 'package:flutter/material.dart';
import '../../models/content_quality_models.dart';
import '../../services/authenticated_dio.dart';
import '../../services/content_quality_service.dart';
import '../../widgets/async_view.dart';
import 'brand_voice_screen.dart';
import 'calendar_screen.dart';
import 'plagiarism_screen.dart';
import 'proofreading_screen.dart';
import 'readability_screen.dart';

class ContentQualityScreen extends StatefulWidget {
  final ContentQualityService? service;

  const ContentQualityScreen({Key? key, this.service}) : super(key: key);

  @override
  State<ContentQualityScreen> createState() => _ContentQualityScreenState();
}

class _ContentQualityScreenState extends State<ContentQualityScreen> {
  late final ContentQualityService _service = widget.service ?? ContentQualityService(createAuthenticatedDio());
  late Future<ContentQualityOverview> _overview = _service.fetchOverview();

  void _reload() {
    setState(() {
      _overview = _service.fetchOverview();
    });
  }

  String _score(double? value, {String suffix = ''}) => value == null ? 'No checks yet' : '${value.toStringAsFixed(1)}$suffix';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Content Quality')),
      body: AsyncView<ContentQualityOverview>(
        future: _overview,
        onRetry: _reload,
        builder: (context, overview) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _row('Proofreading', '${overview.proofreadingChecks} checks',
                _score(overview.averageProofreadingScore, suffix: ' average score')),
            _row('Readability', '${overview.readabilityChecks} checks',
                _score(overview.averageReadabilityGrade, suffix: ' average grade')),
            _row('Brand voice', '${overview.brandVoiceChecks} checks',
                _score(overview.averageBrandVoiceCompliance, suffix: '% compliance')),
            _row('Plagiarism', '${overview.plagiarismChecks} checks',
                _score(overview.averagePlagiarismSimilarity, suffix: '% similarity')),
            const Divider(height: 32),
            _tool(context, 'Proofreading', const ProofreadingScreen()),
            _tool(context, 'Readability', const ReadabilityScreen()),
            _tool(context, 'Brand voice', const BrandVoiceScreen()),
            _tool(context, 'Plagiarism', const PlagiarismScreen()),
            _tool(context, 'Content calendar', const ContentCalendarScreen()),
          ],
        ),
      ),
    );
  }

  Widget _row(String title, String checks, String score) {
    return Card(
      child: ListTile(
        title: Text(title),
        subtitle: Text(checks),
        trailing: Text(score),
      ),
    );
  }

  Widget _tool(BuildContext context, String title, Widget screen) {
    return ListTile(
      title: Text(title),
      trailing: const Icon(Icons.chevron_right),
      onTap: () => Navigator.of(context).push(MaterialPageRoute<void>(builder: (_) => screen)),
    );
  }
}
