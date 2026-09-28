// Content Quality Service (Modules 61-65)

import 'package:dio/dio.dart';
import 'package:logger/logger.dart';
import '../models/content_quality_models.dart';

class ContentQualityService {
  final Dio _dio;
  final Logger _logger = Logger();
  final String _baseUrl;

  ContentQualityService(this._dio, {String baseUrl = 'http://localhost:8000/api/v1'})
      : _baseUrl = baseUrl;

  // Module 61: Calendar Events
  Future<CalendarResponse> getCalendarEvents({
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    try {
      final response = await _dio.get(
        '$_baseUrl/content/calendar/events',
        queryParameters: {
          'start_date': startDate.toIso8601String(),
          'end_date': endDate.toIso8601String(),
        },
      );
      _logger.i('Calendar events fetched successfully');
      return CalendarResponse.fromJson(response.data);
    } catch (e) {
      _logger.e('Failed to fetch calendar events', error: e);
      rethrow;
    }
  }

  Future<CalendarResponse> createCalendarEvent({
    required String title,
    required String eventType,
    required DateTime scheduledFor,
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/content/calendar/events',
        data: {
          'title': title,
          'event_type': eventType,
          'scheduled_for': scheduledFor.toIso8601String(),
        },
      );
      _logger.i('Calendar event created successfully');
      return CalendarResponse.fromJson(response.data);
    } catch (e) {
      _logger.e('Failed to create calendar event', error: e);
      rethrow;
    }
  }

  // Module 62: Proofreading
  Future<ProofreadingResult> checkProofreading({
    required String text,
    bool checkGrammar = true,
    bool checkSpelling = true,
    bool checkStyle = true,
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/content/proofread',
        data: {
          'content_id': 1,
          'text': text,
          'check_grammar': checkGrammar,
          'check_spelling': checkSpelling,
          'check_style': checkStyle,
        },
      );
      _logger.i('Proofreading check completed');
      return ProofreadingResult.fromJson(response.data);
    } catch (e) {
      _logger.e('Failed to perform proofreading check', error: e);
      rethrow;
    }
  }

  // Module 63: Plagiarism Detection
  Future<PlagiarismResult> checkPlagiarism({
    required String text,
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/content/plagiarism/check',
        data: {
          'content_id': 1,
          'text': text,
        },
      );
      _logger.i('Plagiarism check completed');
      return PlagiarismResult.fromJson(response.data);
    } catch (e) {
      _logger.e('Failed to perform plagiarism check', error: e);
      rethrow;
    }
  }

  // Module 64: Readability Analysis
  Future<ReadabilityResult> checkReadability({
    required String text,
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/content/readability/check',
        data: {
          'content_id': 1,
          'text': text,
        },
      );
      _logger.i('Readability check completed');
      return ReadabilityResult.fromJson(response.data);
    } catch (e) {
      _logger.e('Failed to perform readability check', error: e);
      rethrow;
    }
  }

  // Module 65: Brand Voice Consistency
  Future<BrandVoiceResult> checkBrandVoice({
    required String text,
    int brandVoiceGuideId = 1,
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/content/brand-voice/check',
        data: {
          'content_id': 1,
          'text': text,
          'brand_voice_guide_id': brandVoiceGuideId,
        },
      );
      _logger.i('Brand voice check completed');
      return BrandVoiceResult.fromJson(response.data);
    } catch (e) {
      _logger.e('Failed to perform brand voice check', error: e);
      rethrow;
    }
  }
}
