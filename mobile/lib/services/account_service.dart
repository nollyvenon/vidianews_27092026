// The signed-in account, used by screens that act on behalf of the current user.

import 'package:dio/dio.dart';

class AccountService {
  final Dio _dio;

  AccountService(this._dio);

  /// The id of the user the stored session belongs to, from GET /auth/me.
  Future<int> fetchCurrentUserId() async {
    final response = await _dio.get<dynamic>('/auth/me');
    final data = response.data;
    if (data is! Map<String, dynamic> || data['id'] is! int) {
      throw const FormatException('The server did not return the signed-in user');
    }
    return data['id'] as int;
  }
}
