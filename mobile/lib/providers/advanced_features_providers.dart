import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../models/advanced_features_models.dart';

final dioProvider = Provider((ref) => Dio(BaseOptions(baseUrl: 'http://localhost:8000')));

class AdvancedFeaturesService {
  final Dio dio;

  AdvancedFeaturesService(this.dio);

  Future<PersonalizationProfile> getPersonalizationProfile(int userId) async {
    final response = await dio.get('/api/v1/personalization/profile/$userId');
    return PersonalizationProfile.fromJson(response.data);
  }

  Future<PersonalizationProfile> updatePersonalizationPreferences(
    int userId,
    Map<String, double> contentPrefs,
    Map<String, double> authorPrefs,
    Map<String, double> categoryWeights,
  ) async {
    final response = await dio.put('/api/v1/personalization/profile/$userId', data: {
      'content_preferences': contentPrefs,
      'author_preferences': authorPrefs,
      'category_weights': categoryWeights,
    });
    return PersonalizationProfile.fromJson(response.data);
  }

  Future<double> calculatePersonalizationScore(int userId) async {
    final response = await dio.post('/api/v1/personalization/profile/$userId/calculate-score');
    return response.data['personalization_score'];
  }

  Future<List<ContentRecommendation>> getRecommendations(int userId, {int limit = 10}) async {
    final response = await dio.get('/api/v1/recommendations/$userId', queryParameters: {'limit': limit});
    final data = response.data as List;
    return data.map((e) => ContentRecommendation.fromJson(e)).toList();
  }

  Future<List<ContentRecommendation>> getRecommendationsByType(
    int userId,
    String type, {
    int limit = 10,
  }) async {
    final response = await dio.get('/api/v1/recommendations/$userId/type/$type', queryParameters: {'limit': limit});
    final data = response.data as List;
    return data.map((e) => ContentRecommendation.fromJson(e)).toList();
  }

  Future<void> recordRecommendationClick(int recommendationId) async {
    await dio.post('/api/v1/recommendations/$recommendationId/click');
  }

  Future<RecommendationEffectiveness> getRecommendationEffectiveness(int userId) async {
    final response = await dio.get('/api/v1/recommendations/$userId/effectiveness');
    return RecommendationEffectiveness.fromJson(response.data);
  }

  Future<RetentionMetric> createRetentionMetric(int userId) async {
    final response = await dio.post('/api/v1/retention/metrics/$userId');
    return RetentionMetric.fromJson(response.data);
  }

  Future<List<RetentionMetric>> getAtRiskUsers({double churnThreshold = 0.6}) async {
    final response = await dio.get('/api/v1/retention/at-risk', queryParameters: {'churn_threshold': churnThreshold});
    final data = response.data as List;
    return data.map((e) => RetentionMetric.fromJson(e)).toList();
  }

  Future<ABTest> createABTest(
    String name,
    String hypothesis,
    String metricToOptimize, {
    String variantAName = 'Control',
    String variantBName = 'Treatment',
  }) async {
    final response = await dio.post('/api/v1/ab-tests', data: {
      'name': name,
      'hypothesis': hypothesis,
      'metric_to_optimize': metricToOptimize,
      'variant_a_name': variantAName,
      'variant_b_name': variantBName,
    });
    return ABTest.fromJson(response.data);
  }

  Future<ABTest> getABTest(int testId) async {
    final response = await dio.get('/api/v1/ab-tests/$testId');
    return ABTest.fromJson(response.data);
  }

  Future<void> startABTest(int testId) async {
    await dio.post('/api/v1/ab-tests/$testId/start');
  }

  Future<ABTest> endABTest(int testId) async {
    final response = await dio.post('/api/v1/ab-tests/$testId/end');
    return ABTest.fromJson(response.data);
  }

  Future<Map<String, dynamic>> assignUserToVariant(int testId, int userId) async {
    final response = await dio.post('/api/v1/ab-tests/$testId/assign-user/$userId');
    return response.data;
  }

  Future<List<AnalyticsInsight>> getInsights({int limit = 10}) async {
    final response = await dio.get('/api/v1/insights', queryParameters: {'limit': limit});
    final data = response.data as List;
    return data.map((e) => AnalyticsInsight.fromJson(e)).toList();
  }

  Future<List<AnalyticsInsight>> getActionableInsights({int limit = 10}) async {
    final response = await dio.get('/api/v1/insights/actionable', queryParameters: {'limit': limit});
    final data = response.data as List;
    return data.map((e) => AnalyticsInsight.fromJson(e)).toList();
  }

  Future<List<AnalyticsInsight>> getInsightsByType(String type, {int limit = 10}) async {
    final response = await dio.get('/api/v1/insights/type/$type', queryParameters: {'limit': limit});
    final data = response.data as List;
    return data.map((e) => AnalyticsInsight.fromJson(e)).toList();
  }

  Future<UserCohort> createCohort(
    String name,
    String cohortType,
    Map<String, dynamic> criteria, {
    String? description,
  }) async {
    final response = await dio.post('/api/v1/cohorts', data: {
      'name': name,
      'cohort_type': cohortType,
      'criteria': criteria,
      'description': description,
    });
    return UserCohort.fromJson(response.data);
  }

  Future<List<UserCohort>> getCohorts({String? cohortType}) async {
    final response = await dio.get('/api/v1/cohorts', queryParameters: if (cohortType != null) {'cohort_type': cohortType});
    final data = response.data as List;
    return data.map((e) => UserCohort.fromJson(e)).toList();
  }

  Future<void> addUserToCohort(int cohortId, int userId) async {
    await dio.post('/api/v1/cohorts/$cohortId/add-user/$userId');
  }

  Future<CohortMemberResponse> getCohortMembers(int cohortId, {int limit = 100}) async {
    final response = await dio.get('/api/v1/cohorts/$cohortId/members', queryParameters: {'limit': limit});
    return CohortMemberResponse.fromJson(response.data);
  }

  Future<List<UserCohort>> getUserCohorts(int userId) async {
    final response = await dio.get('/api/v1/cohorts/user/$userId');
    final data = response.data as List;
    return data.map((e) => UserCohort.fromJson(e)).toList();
  }

  Future<PredictionModel> createPredictionModel(
    String name,
    String modelType,
    String targetMetric,
    List<String> featuresUsed, {
    int trainingDataSize = 0,
  }) async {
    final response = await dio.post('/api/v1/predictions/models', data: {
      'name': name,
      'model_type': modelType,
      'target_metric': targetMetric,
      'features_used': featuresUsed,
      'training_data_size': trainingDataSize,
    });
    return PredictionModel.fromJson(response.data);
  }

  Future<PredictionModel> getPredictionModel(int modelId) async {
    final response = await dio.get('/api/v1/predictions/models/$modelId');
    return PredictionModel.fromJson(response.data);
  }

  Future<void> deployPredictionModel(int modelId) async {
    await dio.post('/api/v1/predictions/models/$modelId/deploy');
  }

  Future<UserPrediction> createPrediction(int userId, int modelId, double score) async {
    final response = await dio.post('/api/v1/predictions/user/$userId', data: {
      'model_id': modelId,
      'prediction_score': score,
    });
    return UserPrediction.fromJson(response.data);
  }

  Future<List<UserPrediction>> getUserPredictions(int userId, {int limit = 10}) async {
    final response = await dio.get('/api/v1/predictions/user/$userId', queryParameters: {'limit': limit});
    final data = response.data as List;
    return data.map((e) => UserPrediction.fromJson(e)).toList();
  }

  Future<List<PredictionModel>> getDeployedModels() async {
    final response = await dio.get('/api/v1/predictions/models/deployed');
    final data = response.data as List;
    return data.map((e) => PredictionModel.fromJson(e)).toList();
  }
}

final advancedFeaturesServiceProvider = Provider((ref) {
  final dio = ref.watch(dioProvider);
  return AdvancedFeaturesService(dio);
});

final personalizationProfileProvider = FutureProvider.family<PersonalizationProfile, int>((ref, userId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getPersonalizationProfile(userId);
});

final personalizationScoreProvider = FutureProvider.family<double, int>((ref, userId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.calculatePersonalizationScore(userId);
});

final recommendationsProvider = FutureProvider.family<List<ContentRecommendation>, int>((ref, userId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getRecommendations(userId);
});

final recommendationsByTypeProvider =
    FutureProvider.family<List<ContentRecommendation>, (int, String)>((ref, params) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getRecommendationsByType(params.$1, params.$2);
});

final recommendationEffectivenessProvider = FutureProvider.family<RecommendationEffectiveness, int>((ref, userId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getRecommendationEffectiveness(userId);
});

final atRiskUsersProvider = FutureProvider<List<RetentionMetric>>((ref) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getAtRiskUsers();
});

final abTestProvider = FutureProvider.family<ABTest, int>((ref, testId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getABTest(testId);
});

final insightsProvider = FutureProvider<List<AnalyticsInsight>>((ref) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getInsights();
});

final actionableInsightsProvider = FutureProvider<List<AnalyticsInsight>>((ref) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getActionableInsights();
});

final insightsByTypeProvider = FutureProvider.family<List<AnalyticsInsight>, String>((ref, type) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getInsightsByType(type);
});

final cohortsProvider = FutureProvider<List<UserCohort>>((ref) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getCohorts();
});

final userCohortsProvider = FutureProvider.family<List<UserCohort>, int>((ref, userId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getUserCohorts(userId);
});

final cohortMembersProvider = FutureProvider.family<CohortMemberResponse, int>((ref, cohortId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getCohortMembers(cohortId);
});

final predictionModelsProvider = FutureProvider<List<PredictionModel>>((ref) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getDeployedModels();
});

final userPredictionsProvider = FutureProvider.family<List<UserPrediction>, int>((ref, userId) async {
  final service = ref.watch(advancedFeaturesServiceProvider);
  return service.getUserPredictions(userId);
});
