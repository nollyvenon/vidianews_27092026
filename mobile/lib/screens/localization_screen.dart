import 'package:flutter/material.dart';
import 'dart:convert';
import '../services/authenticated_http.dart';
import '../services/authenticated_dio.dart';

class LocalizationScreen extends StatefulWidget {
  const LocalizationScreen({Key? key}) : super(key: key);

  @override
  State<LocalizationScreen> createState() => _LocalizationScreenState();
}

class _LocalizationScreenState extends State<LocalizationScreen> {
  List<dynamic> languages = [];
  String selectedLanguage = 'en';
  String dateFormat = 'MM/DD/YYYY';
  String timeZone = 'UTC';
  bool loading = false;

  @override
  void initState() {
    super.initState();
    fetchLanguages();
  }

  Future<void> fetchLanguages() async {
    setState(() => loading = true);
    try {
      final res = await authenticatedHttp.get(Uri.parse('$kApiBaseUrl/languages'));
      if (res.statusCode == 200) {
        setState(() => languages = jsonDecode(res.body));
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  Future<void> setLanguage(String code) async {
    try {
      final res = await authenticatedHttp.post(
        Uri.parse('$kApiBaseUrl/localization/language'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'language_code': code}),
      );
      if (res.statusCode == 200) {
        setState(() => selectedLanguage = code);
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  Future<void> saveSettings() async {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Settings saved')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Language & Localization')),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                const Text('Select Language', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  children: languages.map((lang) {
                    final code = lang['code'];
                    return ChoiceChip(
                      label: Text(lang['name'] ?? code),
                      selected: selectedLanguage == code,
                      onSelected: (_) => setLanguage(code),
                    );
                  }).toList(),
                ),
                const SizedBox(height: 24),
                const Text('Localization Settings', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  initialValue: dateFormat,
                  decoration: const InputDecoration(labelText: 'Date Format'),
                  items: ['MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY-MM-DD']
                      .map((f) => DropdownMenuItem(value: f, child: Text(f)))
                      .toList(),
                  onChanged: (v) => setState(() => dateFormat = v ?? 'MM/DD/YYYY'),
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  initialValue: timeZone,
                  decoration: const InputDecoration(labelText: 'Time Zone'),
                  items: ['UTC', 'EST', 'PST', 'GMT']
                      .map((z) => DropdownMenuItem(value: z, child: Text(z)))
                      .toList(),
                  onChanged: (v) => setState(() => timeZone = v ?? 'UTC'),
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: saveSettings,
                  child: const Text('Save Settings'),
                ),
              ],
            ),
    );
  }
}
