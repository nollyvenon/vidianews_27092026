// Content Quality Dashboard (Modules 61-65)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'proofreading_screen.dart';
import 'plagiarism_screen.dart';
import 'readability_screen.dart';
import 'brand_voice_screen.dart';
import 'calendar_screen.dart';

class ContentQualityScreen extends ConsumerWidget {
  const ContentQualityScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return DefaultTabController(
      length: 5,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Content Quality'),
          elevation: 0,
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Calendar'),
              Tab(text: 'Proofreading'),
              Tab(text: 'Plagiarism'),
              Tab(text: 'Readability'),
              Tab(text: 'Brand Voice'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            ContentCalendarScreen(),
            ProofreadingScreen(),
            PlagiarismScreen(),
            ReadabilityScreen(),
            BrandVoiceScreen(),
          ],
        ),
      ),
    );
  }
}
