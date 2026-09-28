// Content Quality Providers using Riverpod (Modules 61-65)

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../services/content_quality_service.dart';
import '../models/content_quality_models.dart';

// Service Provider
final contentQualityServiceProvider = Provider((ref) {
  final dio = Dio();
  return ContentQualityService(dio);
});

// Module 61: Calendar Events
final calendarEventsProvider = FutureProvider.family<CalendarResponse, ({DateTime start, DateTime end})>((ref, params) async {
  final service = ref.watch(contentQualityServiceProvider);
  return service.getCalendarEvents(
    startDate: params.start,
    endDate: params.end,
  );
});

// Module 62: Proofreading
final proofreadingProvider = FutureProvider.family<ProofreadingResult, String>((ref, text) async {
  final service = ref.watch(contentQualityServiceProvider);
  return service.checkProofreading(text: text);
});

final proofreadingOptionsProvider = StateProvider<({bool grammar, bool spelling, bool style})>((ref) {
  return (grammar: true, spelling: true, style: true);
});

// Module 63: Plagiarism Detection
final plagiarismProvider = FutureProvider.family<PlagiarismResult, String>((ref, text) async {
  final service = ref.watch(contentQualityServiceProvider);
  return service.checkPlagiarism(text: text);
});

// Module 64: Readability Analysis
final readabilityProvider = FutureProvider.family<ReadabilityResult, String>((ref, text) async {
  final service = ref.watch(contentQualityServiceProvider);
  return service.checkReadability(text: text);
});

// Module 65: Brand Voice Consistency
final brandVoiceProvider = FutureProvider.family<BrandVoiceResult, String>((ref, text) async {
  final service = ref.watch(contentQualityServiceProvider);
  return service.checkBrandVoice(text: text);
});

// UI State Providers
final proofreadingContentProvider = StateProvider<String>((ref) => '');
final plagiarismContentProvider = StateProvider<String>((ref) => '');
final readabilityContentProvider = StateProvider<String>((ref) => '');
final brandVoiceContentProvider = StateProvider<String>((ref) => '');
