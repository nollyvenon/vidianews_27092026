// Content Quality Service Tests

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dio/dio.dart';
import 'package:vidianews_content_quality/services/content_quality_service.dart';
import 'package:vidianews_content_quality/models/content_quality_models.dart';

class MockDio extends Mock implements Dio {}

void main() {
  group('ContentQualityService', () {
    late MockDio mockDio;
    late ContentQualityService service;

    setUp(() {
      mockDio = MockDio();
      service = ContentQualityService(mockDio);
    });

    group('getCalendarEvents', () {
      test('returns CalendarResponse when successful', () async {
        final response = Response<dynamic>(
          data: {
            'events': [
              {
                'id': 1,
                'event_type': 'email',
                'title': 'Test Event',
                'scheduled_for': '2026-10-01T10:00:00',
                'ai_confidence_score': 0.85,
              }
            ],
            'total_count': 1,
            'average_confidence': 0.85,
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.get(
          any(),
          queryParameters: any(named: 'queryParameters'),
        )).thenAnswer((_) async => response);

        final result = await service.getCalendarEvents(
          startDate: DateTime(2026, 10, 1),
          endDate: DateTime(2026, 10, 31),
        );

        expect(result.events, isNotEmpty);
        expect(result.totalCount, 1);
      });

      test('throws when API call fails', () async {
        when(() => mockDio.get(
          any(),
          queryParameters: any(named: 'queryParameters'),
        )).thenThrow(DioException(requestOptions: RequestOptions(path: '')));

        expect(
          () => service.getCalendarEvents(
            startDate: DateTime(2026, 10, 1),
            endDate: DateTime(2026, 10, 31),
          ),
          throwsException,
        );
      });
    });

    group('createCalendarEvent', () {
      test('creates calendar event successfully', () async {
        final response = Response<dynamic>(
          data: {
            'events': [
              {
                'id': 2,
                'event_type': 'social',
                'title': 'New Event',
                'scheduled_for': '2026-10-15T14:00:00',
                'ai_confidence_score': 0.75,
              }
            ],
            'total_count': 1,
            'average_confidence': 0.75,
          },
          statusCode: 201,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.createCalendarEvent(
          title: 'New Event',
          eventType: 'social',
          scheduledFor: DateTime(2026, 10, 15, 14),
        );

        expect(result.events, isNotEmpty);
      });
    });

    group('checkProofreading', () {
      test('performs proofreading check successfully', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'quality_score': 85.0,
            'overall_rating': 'Good',
            'total_issues': 2,
            'grammar_issues': 1,
            'spelling_issues': 1,
            'punctuation_issues': 0,
            'style_issues': 0,
            'issues': [],
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkProofreading(text: 'Sample text');

        expect(result.qualityScore, 85.0);
        expect(result.overallRating, 'Good');
        expect(result.totalIssues, 2);
      });

      test('respects check options', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'quality_score': 85.0,
            'overall_rating': 'Good',
            'total_issues': 2,
            'grammar_issues': 1,
            'spelling_issues': 1,
            'punctuation_issues': 0,
            'style_issues': 0,
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        await service.checkProofreading(
          text: 'Sample text',
          checkGrammar: false,
          checkSpelling: true,
          checkStyle: false,
        );

        verify(() => mockDio.post(
          any(),
          data: {
            'content_id': 1,
            'text': 'Sample text',
            'check_grammar': false,
            'check_spelling': true,
            'check_style': false,
          },
        )).called(1);
      });
    });

    group('checkPlagiarism', () {
      test('performs plagiarism check successfully', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'similarity_percentage': 15.5,
            'originality_percentage': 84.5,
            'plagiarism_risk': 'Low',
            'status': 'completed',
            'total_sources_found': 2,
            'ai_content_percentage': 10.0,
            'human_content_percentage': 90.0,
            'detected_sources': [
              {
                'url': 'https://example.com',
                'similarity_percent': 12.5,
                'matched_text': 'Some text',
              }
            ],
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkPlagiarism(text: 'Sample text');

        expect(result.similarityPercentage, 15.5);
        expect(result.plagiarismRisk, 'Low');
        expect(result.detectedSources, isNotEmpty);
      });

      test('handles high plagiarism risk', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'similarity_percentage': 75.5,
            'originality_percentage': 24.5,
            'plagiarism_risk': 'Critical',
            'status': 'completed',
            'total_sources_found': 5,
            'ai_content_percentage': 40.0,
            'human_content_percentage': 60.0,
            'detected_sources': [],
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkPlagiarism(text: 'Copied text');

        expect(result.plagiarismRisk, 'Critical');
        expect(result.similarityPercentage, greaterThan(70));
      });
    });

    group('checkReadability', () {
      test('performs readability check successfully', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'word_count': 250,
            'sentence_count': 10,
            'paragraph_count': 3,
            'flesch_reading_ease': 65.0,
            'flesch_kincaid_grade': 8.0,
            'gunning_fog_index': 9.0,
            'smog_index': 10.0,
            'readability_level': 'Moderate',
            'target_audience_grade_level': 'Grade 8-9',
            'complexity_score': 55.0,
            'avg_word_length': 4.8,
            'avg_sentence_length': 15.5,
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkReadability(text: 'Sample text');

        expect(result.wordCount, 250);
        expect(result.readabilityLevel, 'Moderate');
        expect(result.fleschReadingEase, 65.0);
      });

      test('handles complex content', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'word_count': 500,
            'sentence_count': 15,
            'paragraph_count': 5,
            'flesch_reading_ease': 25.0,
            'flesch_kincaid_grade': 16.0,
            'gunning_fog_index': 18.0,
            'smog_index': 17.0,
            'readability_level': 'Very Difficult',
            'target_audience_grade_level': 'Graduate',
            'complexity_score': 85.0,
            'avg_word_length': 6.5,
            'avg_sentence_length': 25.0,
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkReadability(text: 'Complex academic text');

        expect(result.complexityScore, greaterThan(80));
        expect(result.readabilityLevel, 'Very Difficult');
      });
    });

    group('checkBrandVoice', () {
      test('performs brand voice check successfully', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'consistency_score': 85.0,
            'compliance_percentage': 95.0,
            'brand_alignment': 'Good',
            'total_violations': 1,
            'tone_violations': 0,
            'style_violations': 1,
            'terminology_violations': 0,
            'violations': [
              {
                'id': 1,
                'violation_type': 'style',
                'severity': 'low',
                'description': 'Minor style inconsistency',
                'suggested_fix': 'Use consistent formatting',
              }
            ],
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkBrandVoice(text: 'Sample content');

        expect(result.consistencyScore, 85.0);
        expect(result.brandAlignment, 'Good');
        expect(result.violations, isNotEmpty);
      });

      test('detects critical brand voice issues', () async {
        final response = Response<dynamic>(
          data: {
            'id': 1,
            'consistency_score': 45.0,
            'compliance_percentage': 50.0,
            'brand_alignment': 'Poor',
            'total_violations': 5,
            'tone_violations': 3,
            'style_violations': 2,
            'terminology_violations': 0,
            'violations': [],
          },
          statusCode: 200,
          requestOptions: RequestOptions(path: ''),
        );

        when(() => mockDio.post(
          any(),
          data: any(named: 'data'),
        )).thenAnswer((_) async => response);

        final result = await service.checkBrandVoice(text: 'Misaligned content');

        expect(result.consistencyScore, lessThan(50));
        expect(result.toneViolations, greaterThan(0));
      });
    });
  });
}
