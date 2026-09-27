import 'package:flutter/material.dart';
import 'package:vidianews/services/content_service.dart';
import 'content_detail_screen.dart';

class ContentListScreen extends StatefulWidget {
  const ContentListScreen({Key? key}) : super(key: key);

  @override
  State<ContentListScreen> createState() => _ContentListScreenState();
}

class _ContentListScreenState extends State<ContentListScreen> {
  final ContentService _contentService = ContentService();
  late Future<Map<String, dynamic>> _contentListFuture;
  int _currentPage = 1;
  String _statusFilter = '';
  String _typeFilter = '';
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _loadContent();
  }

  void _loadContent() {
    if (_searchQuery.isNotEmpty) {
      _contentListFuture = _contentService
          .searchContent(_searchQuery)
          .then((results) => {'items': results, 'total': results.length});
    } else {
      _contentListFuture = _contentService.listContent(
        page: _currentPage,
        status: _statusFilter.isEmpty ? null : _statusFilter,
        contentType: _typeFilter.isEmpty ? null : _typeFilter,
      );
    }
    setState(() {});
  }

  String _getTypeIcon(String type) {
    switch (type) {
      case 'video':
        return '🎥';
      case 'article':
        return '📄';
      case 'blog_post':
        return '📝';
      case 'newsletter':
        return '📧';
      default:
        return '📄';
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'published':
        return Colors.green;
      case 'scheduled':
        return Colors.blue;
      case 'draft':
        return Colors.grey;
      case 'archived':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Content Manager'),
        elevation: 0,
      ),
      body: CustomScrollView(
        slivers: [
          // Search Bar
          SliverAppBar(
            floating: true,
            pinned: false,
            expandedHeight: 120,
            backgroundColor: Colors.white,
            flexibleSpace: FlexibleSpaceBar(
              background: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    TextField(
                      decoration: InputDecoration(
                        hintText: 'Search content...',
                        prefixIcon: const Icon(Icons.search),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                      ),
                      onChanged: (value) {
                        _searchQuery = value;
                        _currentPage = 1;
                        _loadContent();
                      },
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: DropdownButton<String>(
                            isExpanded: true,
                            value: _statusFilter,
                            hint: const Text('All Status'),
                            items: [
                              const DropdownMenuItem(
                                value: '',
                                child: Text('All Status'),
                              ),
                              const DropdownMenuItem(
                                value: 'draft',
                                child: Text('Draft'),
                              ),
                              const DropdownMenuItem(
                                value: 'published',
                                child: Text('Published'),
                              ),
                              const DropdownMenuItem(
                                value: 'scheduled',
                                child: Text('Scheduled'),
                              ),
                              const DropdownMenuItem(
                                value: 'archived',
                                child: Text('Archived'),
                              ),
                            ],
                            onChanged: (value) {
                              setState(() {
                                _statusFilter = value ?? '';
                                _currentPage = 1;
                              });
                              _loadContent();
                            },
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: DropdownButton<String>(
                            isExpanded: true,
                            value: _typeFilter,
                            hint: const Text('All Types'),
                            items: [
                              const DropdownMenuItem(
                                value: '',
                                child: Text('All Types'),
                              ),
                              const DropdownMenuItem(
                                value: 'video',
                                child: Text('Video'),
                              ),
                              const DropdownMenuItem(
                                value: 'article',
                                child: Text('Article'),
                              ),
                              const DropdownMenuItem(
                                value: 'blog_post',
                                child: Text('Blog Post'),
                              ),
                              const DropdownMenuItem(
                                value: 'newsletter',
                                child: Text('Newsletter'),
                              ),
                            ],
                            onChanged: (value) {
                              setState(() {
                                _typeFilter = value ?? '';
                                _currentPage = 1;
                              });
                              _loadContent();
                            },
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
          // Content List
          SliverFillRemaining(
            child: FutureBuilder<Map<String, dynamic>>(
              future: _contentListFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }

                if (snapshot.hasError) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('Error: ${snapshot.error}'),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: _loadContent,
                          child: const Text('Retry'),
                        ),
                      ],
                    ),
                  );
                }

                final data = snapshot.data ?? {};
                final items = List<dynamic>.from(data['items'] ?? []);
                final total = data['total'] ?? 0;

                if (items.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.content_paste_off, size: 64),
                        const SizedBox(height: 16),
                        const Text('No content found'),
                      ],
                    ),
                  );
                }

                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: items.length + 1,
                  itemBuilder: (context, index) {
                    if (index == items.length) {
                      // Pagination buttons
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            ElevatedButton(
                              onPressed: _currentPage > 1
                                  ? () {
                                      _currentPage--;
                                      _loadContent();
                                    }
                                  : null,
                              child: const Text('Previous'),
                            ),
                            Text('Page $_currentPage'),
                            ElevatedButton(
                              onPressed: (_currentPage * 20 < total)
                                  ? () {
                                      _currentPage++;
                                      _loadContent();
                                    }
                                  : null,
                              child: const Text('Next'),
                            ),
                          ],
                        ),
                      );
                    }

                    final item = items[index];
                    return ContentCard(
                      item: item,
                      statusColor: _getStatusColor(item['status']),
                      typeIcon: _getTypeIcon(item['content_type']),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => ContentDetailScreen(
                              contentId: item['id'],
                            ),
                          ),
                        );
                      },
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Navigate to create content screen
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Navigate to create content')),
          );
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

class ContentCard extends StatelessWidget {
  final Map<String, dynamic> item;
  final Color statusColor;
  final String typeIcon;
  final VoidCallback onTap;

  const ContentCard({
    Key? key,
    required this.item,
    required this.statusColor,
    required this.typeIcon,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (item['thumbnail_url'] != null)
              ClipRRect(
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(4),
                  topRight: Radius.circular(4),
                ),
                child: Image.network(
                  item['thumbnail_url'],
                  height: 200,
                  width: double.infinity,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      height: 200,
                      color: Colors.grey[300],
                      child: const Icon(Icons.image_not_supported),
                    );
                  },
                ),
              ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(typeIcon, style: const TextStyle(fontSize: 20)),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          item['title'] ?? 'Untitled',
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    item['description'] ?? '',
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: Colors.grey[600],
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: statusColor.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          item['status'] ?? 'unknown',
                          style: TextStyle(
                            color: statusColor,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      Row(
                        children: [
                          Icon(Icons.visibility, size: 16, color: Colors.grey),
                          const SizedBox(width: 4),
                          Text(
                            '${item['views_count'] ?? 0}',
                            style: const TextStyle(fontSize: 12),
                          ),
                          const SizedBox(width: 12),
                          const Icon(Icons.favorite, size: 16, color: Colors.red),
                          const SizedBox(width: 4),
                          Text(
                            '${item['likes_count'] ?? 0}',
                            style: const TextStyle(fontSize: 12),
                          ),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
