import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

void main() {
  runApp(const AetherCMSApp());
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
  final _dio = Dio(BaseOptions(baseUrl: 'http://localhost:8000'));
  bool _isLoading = false;
  String _error = '';

  void _handleLogin() async {
    setState(() {
      _isLoading = true;
      _error = '';
    });

    try {
      final response = await _dio.post(
        '/api/v1/auth/login',
        data: {
          'email': _emailController.text,
          'password': _passwordController.text,
        },
      );

      if (response.statusCode == 200) {
        final tokens = response.data;
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
