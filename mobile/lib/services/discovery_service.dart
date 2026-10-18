// Creator, discovery, search, processing, live and documentation APIs for the signed-in user.

import 'package:dio/dio.dart';
import '../models/discovery_models.dart';

class DiscoveryService {
  final Dio _dio;

  DiscoveryService(this._dio);

  Future<CreatorProfile> fetchCreatorProfile() async {
    final response = await _dio.get<dynamic>('/monetization/creator-profile');
    return CreatorProfile.fromJson(response.data as Map<String, dynamic>);
  }

  Future<CreatorProfile> saveCreatorBio(String bio) async {
    final response = await _dio.post<dynamic>('/monetization/creator-profile', queryParameters: {'bio': bio});
    return CreatorProfile.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<CreatorProfile>> fetchCreators({required bool verifiedOnly}) async {
    final response = await _dio.get<dynamic>('/monetization/creators', queryParameters: {'verified_only': verifiedOnly});
    return _rows(response.data).map(CreatorProfile.fromJson).toList();
  }

  Future<List<Recommendation>> fetchRecommendations({int limit = 10}) async {
    final response = await _dio.get<dynamic>('/recommendations', queryParameters: {'limit': limit});
    return _rows(response.data).map(Recommendation.fromJson).toList();
  }

  Future<List<TrendingTopic>> fetchTrending({int limit = 10}) async {
    final response = await _dio.get<dynamic>('/trending', queryParameters: {'limit': limit});
    return _rows(response.data).map(TrendingTopic.fromJson).toList();
  }

  Future<List<SearchResult>> search(String query) async {
    final response = await _dio.get<dynamic>('/system/search', queryParameters: {'q': query});
    return _rows(response.data).map(SearchResult.fromJson).toList();
  }

  Future<List<VideoJob>> fetchVideoJobs() async {
    final response = await _dio.get<dynamic>('/content/videos/processing');
    return _rows(response.data).map(VideoJob.fromJson).toList();
  }

  Future<List<ActiveStream>> fetchActiveStreams() async {
    final response = await _dio.get<dynamic>('/livestream/active');
    return _rows(response.data).map(ActiveStream.fromJson).toList();
  }

  Future<Map<String, dynamic>> startLiveStream({required String title, String description = ''}) async {
    final response = await _dio.post<dynamic>('/livestream', queryParameters: {'title': title, 'description': description});
    return response.data as Map<String, dynamic>;
  }

  Future<List<Partnership>> fetchPartnerships() async {
    final response = await _dio.get<dynamic>('/partnerships');
    return _rows(response.data).map(Partnership.fromJson).toList();
  }

  Future<void> proposePartnership({required String partnerId, required String partnershipType}) async {
    await _dio.post<dynamic>('/partnerships', queryParameters: {
      'partner_id': partnerId,
      'partnership_type': partnershipType,
    });
  }

  Future<List<Doc>> fetchDocs() async {
    final response = await _dio.get<dynamic>('/docs');
    return _rows(response.data).map(Doc.fromJson).toList();
  }

  Future<List<ApiReference>> fetchApiReference() async {
    final response = await _dio.get<dynamic>('/docs/api/all');
    return _rows(response.data).map(ApiReference.fromJson).toList();
  }

  static List<Map<String, dynamic>> _rows(dynamic data) {
    if (data is! List) {
      throw const FormatException('Expected a list from the server');
    }
    return data.cast<Map<String, dynamic>>();
  }
}
