import 'package:flutter/material.dart'

class SearchScreen extends StatefulWidget {
  const SearchScreen({Key? key}) : super(key: key);

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<Map<String, String>> results = [];
  bool searching = false;

  void _performSearch(String query) async {
    if (query.isEmpty) {
      setState(() => results = []);
      return;
    }

    setState(() => searching = true);
    // Simulate API call
    await Future.delayed(Duration(milliseconds: 500));

    setState(() {
      results = [
        {'title': 'Flutter Tutorial', 'type': 'video'},
        {'title': 'React Guide', 'type': 'article'},
        {'title': 'Database Design', 'type': 'course'},
      ];
      searching = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Search')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _searchController,
              onChanged: _performSearch,
              decoration: InputDecoration(
                hintText: 'Search...',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                prefixIcon: const Icon(Icons.search),
              ),
            ),
          ),
          Expanded(
            child: searching
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: results.length,
                    itemBuilder: (context, index) {
                      final result = results[index];
                      return ListTile(
                        leading: Icon(Icons.play_circle),
                        title: Text(result['title']!),
                        subtitle: Text(result['type']!),
                        onTap: () {},
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
