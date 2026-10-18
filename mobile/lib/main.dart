import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';
import 'services/authenticated_dio.dart';
import 'services/social_auth_service.dart';
import 'services/social_sign_in_flow.dart';
import 'widgets/social_login_buttons.dart';

void main() {
  // Riverpod providers used by the feature screens need a scope at the root of the app.
  runApp(const ProviderScope(child: AetherCMSApp()));
}

class AetherCMSApp extends StatelessWidget {
  const AetherCMSApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AetherCMS AI',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _dio = Dio(BaseOptions(baseUrl: kApiBaseUrl));
  late final SocialAuthService _socialService = SocialAuthService(createAuthenticatedDio());
  late final SocialSignInFlow _socialFlow = SocialSignInFlow(
    service: _socialService,
    launch: (url) => launchUrl(url, mode: LaunchMode.externalApplication),
    saveSession: _saveSession,
  );
  bool _isLoading = false;
  String _error = '';

  Future<void> _saveSession(String accessToken) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(kAuthTokenKey, accessToken);
  }

  void _handleLogin() async {
    setState(() {
      _isLoading = true;
      _error = '';
    });

    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': _emailController.text,
          'password': _passwordController.text,
        },
      );

      if (response.statusCode == 200) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', response.data['access_token'] as String);
        if (mounted) {
          Navigator.of(context).pushReplacementNamed('/dashboard');
        }
      }
    } on DioException catch (e) {
      setState(() {
        _error = e.response?.data['error']['message'] ?? 'Login failed';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AetherCMS AI')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'AetherCMS AI',
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              const Text(
                'Enterprise AI Publishing Platform',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 32),
              if (_error.isNotEmpty)
                Container(
                  padding: const EdgeInsets.all(12),
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: Colors.red.shade100,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    _error,
                    style: TextStyle(color: Colors.red.shade900),
                  ),
                ),
              TextField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isLoading ? null : _handleLogin,
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 48),
                ),
                child: Text(_isLoading ? 'Logging in...' : 'Login'),
              ),
              SocialLoginButtons(
                service: _socialService,
                flow: _socialFlow,
                onSignedIn: () => Navigator.of(context).pushReplacementNamed('/dashboard'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
