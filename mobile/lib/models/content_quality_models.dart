// Models for Content Quality Analysis (Modules 61-65)

import 'package:freezed_annotation/freezed_annotation.dart';

part 'content_quality_models.freezed.dart';
part 'content_quality_models.g.dart';

// Module 61: Content Calendar
@freezed
class CalendarEvent with _$CalendarEvent {
  const factory CalendarEvent({
    required int id,
    required String eventType,
    required String title,
    required DateTime scheduledFor,
    DateTime? aiRecommendedTime,
    required double aiConfidenceScore,
    int? predictedReach,
    int? predictedEngagement,
  }) = _CalendarEvent;

  factory CalendarEvent.fromJson(Map<String, dynamic> json) =>
      _$CalendarEventFromJson(json);
}

@freezed
class CalendarResponse with _$CalendarResponse {
  const factory CalendarResponse({
    required List<CalendarEvent> events,
    required int totalCount,
    required double averageConfidence,
  }) = _CalendarResponse;

  factory CalendarResponse.fromJson(Map<String, dynamic> json) =>
      _$CalendarResponseFromJson(json);
}

// Module 62: Proofreading
@freezed
class ProofreadingIssue with _$ProofreadingIssue {
  const factory ProofreadingIssue({
    required int id,
    required String issueType,
    required String severity,
    required String text,
    required String suggestion,
    required int position,
    required int length,
  }) = _ProofreadingIssue;

  factory ProofreadingIssue.fromJson(Map<String, dynamic> json) =>
      _$ProofreadingIssueFromJson(json);
}

@freezed
class ProofreadingResult with _$ProofreadingResult {
  const factory ProofreadingResult({
    required int id,
    required double qualityScore,
    required String overallRating,
    required int totalIssues,
    required int grammarIssues,
    required int spellingIssues,
    required int punctuationIssues,
    required int styleIssues,
    List<ProofreadingIssue>? issues,
  }) = _ProofreadingResult;

  factory ProofreadingResult.fromJson(Map<String, dynamic> json) =>
      _$ProofreadingResultFromJson(json);
}

// Module 63: Plagiarism Detection
@freezed
class Source with _$Source {
  const factory Source({
    required String url,
    required double similarityPercent,
    required String matchedText,
  }) = _Source;

  factory Source.fromJson(Map<String, dynamic> json) => _$SourceFromJson(json);
}

@freezed
class PlagiarismResult with _$PlagiarismResult {
  const factory PlagiarismResult({
    required int id,
    required double similarityPercentage,
    required double originalityPercentage,
    required String plagiarismRisk,
    required String status,
    required int totalSourcesFound,
    required double aiContentPercentage,
    required double humanContentPercentage,
    required List<Source> detectedSources,
  }) = _PlagiarismResult;

  factory PlagiarismResult.fromJson(Map<String, dynamic> json) =>
      _$PlagiarismResultFromJson(json);
}

// Module 64: Readability Analysis
@freezed
class ReadabilityResult with _$ReadabilityResult {
  const factory ReadabilityResult({
    required int id,
    required int wordCount,
    required int sentenceCount,
    required int paragraphCount,
    required double fleschReadingEase,
    required double fleschKincaidGrade,
    required double gunningFogIndex,
    required double smogIndex,
    required String readabilityLevel,
    required String targetAudienceGradeLevel,
    required double complexityScore,
    required double avgWordLength,
    required double avgSentenceLength,
  }) = _ReadabilityResult;

  factory ReadabilityResult.fromJson(Map<String, dynamic> json) =>
      _$ReadabilityResultFromJson(json);
}

// Module 65: Brand Voice Consistency
@freezed
class BrandVoiceViolation with _$BrandVoiceViolation {
  const factory BrandVoiceViolation({
    required int id,
    required String violationType,
    required String severity,
    required String description,
    required String suggestedFix,
  }) = _BrandVoiceViolation;

  factory BrandVoiceViolation.fromJson(Map<String, dynamic> json) =>
      _$BrandVoiceViolationFromJson(json);
}

@freezed
class BrandVoiceResult with _$BrandVoiceResult {
  const factory BrandVoiceResult({
    required int id,
    required double consistencyScore,
    required double compliancePercentage,
    required String brandAlignment,
    required int totalViolations,
    required int toneViolations,
    required int styleViolations,
    required int terminologyViolations,
    required List<BrandVoiceViolation> violations,
  }) = _BrandVoiceResult;

  factory BrandVoiceResult.fromJson(Map<String, dynamic> json) =>
      _$BrandVoiceResultFromJson(json);
}
