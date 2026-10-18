// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'content_quality_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$CalendarEventImpl _$$CalendarEventImplFromJson(Map<String, dynamic> json) =>
    _$CalendarEventImpl(
      id: (json['id'] as num).toInt(),
      eventType: json['event_type'] as String,
      title: json['title'] as String,
      scheduledFor: DateTime.parse(json['scheduled_for'] as String),
      aiRecommendedTime: json['ai_recommended_time'] == null
          ? null
          : DateTime.parse(json['ai_recommended_time'] as String),
      aiConfidenceScore: (json['ai_confidence_score'] as num).toDouble(),
      predictedReach: (json['predicted_reach'] as num?)?.toInt(),
      predictedEngagement: (json['predicted_engagement'] as num?)?.toInt(),
    );

Map<String, dynamic> _$$CalendarEventImplToJson(_$CalendarEventImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'event_type': instance.eventType,
      'title': instance.title,
      'scheduled_for': instance.scheduledFor.toIso8601String(),
      'ai_recommended_time': instance.aiRecommendedTime?.toIso8601String(),
      'ai_confidence_score': instance.aiConfidenceScore,
      'predicted_reach': instance.predictedReach,
      'predicted_engagement': instance.predictedEngagement,
    };

_$CalendarResponseImpl _$$CalendarResponseImplFromJson(
        Map<String, dynamic> json) =>
    _$CalendarResponseImpl(
      events: (json['events'] as List<dynamic>)
          .map((e) => CalendarEvent.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalCount: (json['total_count'] as num).toInt(),
      averageConfidence: (json['average_confidence'] as num).toDouble(),
    );

Map<String, dynamic> _$$CalendarResponseImplToJson(
        _$CalendarResponseImpl instance) =>
    <String, dynamic>{
      'events': instance.events,
      'total_count': instance.totalCount,
      'average_confidence': instance.averageConfidence,
    };

_$ProofreadingIssueImpl _$$ProofreadingIssueImplFromJson(
        Map<String, dynamic> json) =>
    _$ProofreadingIssueImpl(
      id: (json['id'] as num).toInt(),
      issueType: json['issue_type'] as String,
      severity: json['severity'] as String,
      text: json['text'] as String,
      suggestion: json['suggestion'] as String,
      position: (json['position'] as num).toInt(),
      length: (json['length'] as num).toInt(),
    );

Map<String, dynamic> _$$ProofreadingIssueImplToJson(
        _$ProofreadingIssueImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'issue_type': instance.issueType,
      'severity': instance.severity,
      'text': instance.text,
      'suggestion': instance.suggestion,
      'position': instance.position,
      'length': instance.length,
    };

_$ProofreadingResultImpl _$$ProofreadingResultImplFromJson(
        Map<String, dynamic> json) =>
    _$ProofreadingResultImpl(
      id: (json['id'] as num).toInt(),
      qualityScore: (json['quality_score'] as num).toDouble(),
      overallRating: json['overall_rating'] as String,
      totalIssues: (json['total_issues'] as num).toInt(),
      grammarIssues: (json['grammar_issues'] as num).toInt(),
      spellingIssues: (json['spelling_issues'] as num).toInt(),
      punctuationIssues: (json['punctuation_issues'] as num).toInt(),
      styleIssues: (json['style_issues'] as num).toInt(),
      issues: (json['issues'] as List<dynamic>?)
          ?.map((e) => ProofreadingIssue.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$ProofreadingResultImplToJson(
        _$ProofreadingResultImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'quality_score': instance.qualityScore,
      'overall_rating': instance.overallRating,
      'total_issues': instance.totalIssues,
      'grammar_issues': instance.grammarIssues,
      'spelling_issues': instance.spellingIssues,
      'punctuation_issues': instance.punctuationIssues,
      'style_issues': instance.styleIssues,
      'issues': instance.issues,
    };

_$SourceImpl _$$SourceImplFromJson(Map<String, dynamic> json) => _$SourceImpl(
      url: json['url'] as String,
      similarityPercent: (json['similarity_percent'] as num).toDouble(),
      matchedText: json['matched_text'] as String,
    );

Map<String, dynamic> _$$SourceImplToJson(_$SourceImpl instance) =>
    <String, dynamic>{
      'url': instance.url,
      'similarity_percent': instance.similarityPercent,
      'matched_text': instance.matchedText,
    };

_$PlagiarismResultImpl _$$PlagiarismResultImplFromJson(
        Map<String, dynamic> json) =>
    _$PlagiarismResultImpl(
      id: (json['id'] as num).toInt(),
      similarityPercentage: (json['similarity_percentage'] as num).toDouble(),
      originalityPercentage: (json['originality_percentage'] as num).toDouble(),
      plagiarismRisk: json['plagiarism_risk'] as String,
      status: json['status'] as String,
      totalSourcesFound: (json['total_sources_found'] as num).toInt(),
      aiContentPercentage: (json['ai_content_percentage'] as num).toDouble(),
      humanContentPercentage:
          (json['human_content_percentage'] as num).toDouble(),
      detectedSources: (json['detected_sources'] as List<dynamic>)
          .map((e) => Source.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$PlagiarismResultImplToJson(
        _$PlagiarismResultImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'similarity_percentage': instance.similarityPercentage,
      'originality_percentage': instance.originalityPercentage,
      'plagiarism_risk': instance.plagiarismRisk,
      'status': instance.status,
      'total_sources_found': instance.totalSourcesFound,
      'ai_content_percentage': instance.aiContentPercentage,
      'human_content_percentage': instance.humanContentPercentage,
      'detected_sources': instance.detectedSources,
    };

_$ReadabilityResultImpl _$$ReadabilityResultImplFromJson(
        Map<String, dynamic> json) =>
    _$ReadabilityResultImpl(
      id: (json['id'] as num).toInt(),
      wordCount: (json['word_count'] as num).toInt(),
      sentenceCount: (json['sentence_count'] as num).toInt(),
      paragraphCount: (json['paragraph_count'] as num).toInt(),
      fleschReadingEase: (json['flesch_reading_ease'] as num).toDouble(),
      fleschKincaidGrade: (json['flesch_kincaid_grade'] as num).toDouble(),
      gunningFogIndex: (json['gunning_fog_index'] as num).toDouble(),
      smogIndex: (json['smog_index'] as num).toDouble(),
      readabilityLevel: json['readability_level'] as String,
      targetAudienceGradeLevel: json['target_audience_grade_level'] as String,
      complexityScore: (json['complexity_score'] as num).toDouble(),
      avgWordLength: (json['avg_word_length'] as num).toDouble(),
      avgSentenceLength: (json['avg_sentence_length'] as num).toDouble(),
    );

Map<String, dynamic> _$$ReadabilityResultImplToJson(
        _$ReadabilityResultImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'word_count': instance.wordCount,
      'sentence_count': instance.sentenceCount,
      'paragraph_count': instance.paragraphCount,
      'flesch_reading_ease': instance.fleschReadingEase,
      'flesch_kincaid_grade': instance.fleschKincaidGrade,
      'gunning_fog_index': instance.gunningFogIndex,
      'smog_index': instance.smogIndex,
      'readability_level': instance.readabilityLevel,
      'target_audience_grade_level': instance.targetAudienceGradeLevel,
      'complexity_score': instance.complexityScore,
      'avg_word_length': instance.avgWordLength,
      'avg_sentence_length': instance.avgSentenceLength,
    };

_$BrandVoiceViolationImpl _$$BrandVoiceViolationImplFromJson(
        Map<String, dynamic> json) =>
    _$BrandVoiceViolationImpl(
      id: (json['id'] as num).toInt(),
      violationType: json['violation_type'] as String,
      severity: json['severity'] as String,
      description: json['description'] as String,
      suggestedFix: json['suggested_fix'] as String,
    );

Map<String, dynamic> _$$BrandVoiceViolationImplToJson(
        _$BrandVoiceViolationImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'violation_type': instance.violationType,
      'severity': instance.severity,
      'description': instance.description,
      'suggested_fix': instance.suggestedFix,
    };

_$BrandVoiceResultImpl _$$BrandVoiceResultImplFromJson(
        Map<String, dynamic> json) =>
    _$BrandVoiceResultImpl(
      id: (json['id'] as num).toInt(),
      consistencyScore: (json['consistency_score'] as num).toDouble(),
      compliancePercentage: (json['compliance_percentage'] as num).toDouble(),
      brandAlignment: json['brand_alignment'] as String,
      totalViolations: (json['total_violations'] as num).toInt(),
      toneViolations: (json['tone_violations'] as num).toInt(),
      styleViolations: (json['style_violations'] as num).toInt(),
      terminologyViolations: (json['terminology_violations'] as num).toInt(),
      violations: (json['violations'] as List<dynamic>)
          .map((e) => BrandVoiceViolation.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$BrandVoiceResultImplToJson(
        _$BrandVoiceResultImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'consistency_score': instance.consistencyScore,
      'compliance_percentage': instance.compliancePercentage,
      'brand_alignment': instance.brandAlignment,
      'total_violations': instance.totalViolations,
      'tone_violations': instance.toneViolations,
      'style_violations': instance.styleViolations,
      'terminology_violations': instance.terminologyViolations,
      'violations': instance.violations,
    };
