// Loads the signed-in user's id and builds a screen that needs it.

import 'package:flutter/material.dart';
import '../services/account_service.dart';
import '../services/authenticated_dio.dart';
import 'async_view.dart';

class CurrentUserBuilder extends StatefulWidget {
  final AccountService? accountService;
  final Widget Function(BuildContext context, int userId) builder;

  const CurrentUserBuilder({Key? key, this.accountService, required this.builder}) : super(key: key);

  @override
  State<CurrentUserBuilder> createState() => _CurrentUserBuilderState();
}

class _CurrentUserBuilderState extends State<CurrentUserBuilder> {
  late final AccountService _accounts = widget.accountService ?? AccountService(createAuthenticatedDio());
  late Future<int> _userId = _accounts.fetchCurrentUserId();

  void _reload() {
    setState(() {
      _userId = _accounts.fetchCurrentUserId();
    });
  }

  @override
  Widget build(BuildContext context) {
    return AsyncView<int>(
      future: _userId,
      onRetry: _reload,
      builder: (context, userId) => widget.builder(context, userId),
    );
  }
}
