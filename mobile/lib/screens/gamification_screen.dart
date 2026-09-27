import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class GamificationScreen extends StatefulWidget {
  const GamificationScreen({Key? key}) : super(key: key);

  @override
  State<GamificationScreen> createState() => _GamificationScreenState();
}

class _GamificationScreenState extends State<GamificationScreen> {
  List<dynamic> leaderboard = [];
  List<dynamic> badges = [];
  bool loading = false;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    setState(() => loading = true);
    try {
      final res1 = await http.get(Uri.parse('http://localhost:8000/api/v1/leaderboard'));
      final res2 = await http.get(Uri.parse('http://localhost:8000/api/v1/badges/user'));
      if (res1.statusCode == 200 && res2.statusCode == 200) {
        setState(() {
          leaderboard = jsonDecode(res1.body);
          badges = jsonDecode(res2.body);
        });
      }
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Badges & Gamification')),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : DefaultTabController(
              length: 2,
              child: Column(
                children: [
                  const TabBar(tabs: [
                    Tab(text: 'My Badges'),
                    Tab(text: 'Leaderboard'),
                  ]),
                  Expanded(
                    child: TabBarView(children: [
                      GridView.builder(
                        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3),
                        itemCount: badges.length,
                        itemBuilder: (context, index) => Card(
                          child: Center(child: Text('🏅\n${badges[index]['name']}')),
                        ),
                      ),
                      ListView.builder(
                        itemCount: leaderboard.length,
                        itemBuilder: (context, index) {
                          final entry = leaderboard[index];
                          return ListTile(
                            leading: Text('#${entry['rank']}'),
                            title: Text('${entry['points']} points'),
                            trailing: Text('${entry['views']} views'),
                          );
                        },
                      ),
                    ]),
                  ),
                ],
              ),
            ),
    );
  }
}
