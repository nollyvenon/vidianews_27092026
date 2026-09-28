import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CoursesScreen extends StatefulWidget {
  @override
  State<CoursesScreen> createState() => _CoursesScreenState();
}

class _CoursesScreenState extends State<CoursesScreen> {
  late Future<List<Course>> futureCourses;
  String searchTerm = '';
  String difficultyFilter = 'all';

  @override
  void initState() {
    super.initState();
    futureCourses = fetchCourses();
  }

  Future<List<Course>> fetchCourses() async {
    final response = await http.get(
      Uri.parse('http://localhost:8000/api/v1/courses'),
      headers: {'Authorization': 'Bearer YOUR_TOKEN'},
    );

    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      var courses = jsonResponse.map((data) => Course.fromJson(data)).toList();

      if (searchTerm.isNotEmpty) {
        courses = courses.where((c) =>
          c.title.toLowerCase().contains(searchTerm.toLowerCase())
        ).toList();
      }

      if (difficultyFilter != 'all') {
        courses = courses.where((c) => c.difficultyLevel == difficultyFilter).toList();
      }

      return courses;
    } else {
      throw Exception('Failed to load courses');
    }
  }

  void _refreshCourses() {
    setState(() {
      futureCourses = fetchCourses();
    });
  }

  Future<void> _enrollCourse(int courseId) async {
    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/api/v1/courses/$courseId/enroll'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Enrolled successfully')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Enrollment failed: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Courses'),
        elevation: 0,
      ),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              children: [
                TextField(
                  decoration: InputDecoration(
                    hintText: 'Search courses...',
                    prefixIcon: Icon(Icons.search),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  onChanged: (value) {
                    setState(() {
                      searchTerm = value;
                      _refreshCourses();
                    });
                  },
                ),
                SizedBox(height: 12),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _FilterChip(
                        label: 'All',
                        selected: difficultyFilter == 'all',
                        onSelected: () => setState(() {
                          difficultyFilter = 'all';
                          _refreshCourses();
                        }),
                      ),
                      SizedBox(width: 8),
                      _FilterChip(
                        label: 'Beginner',
                        selected: difficultyFilter == 'beginner',
                        onSelected: () => setState(() {
                          difficultyFilter = 'beginner';
                          _refreshCourses();
                        }),
                      ),
                      SizedBox(width: 8),
                      _FilterChip(
                        label: 'Intermediate',
                        selected: difficultyFilter == 'intermediate',
                        onSelected: () => setState(() {
                          difficultyFilter = 'intermediate';
                          _refreshCourses();
                        }),
                      ),
                      SizedBox(width: 8),
                      _FilterChip(
                        label: 'Advanced',
                        selected: difficultyFilter == 'advanced',
                        onSelected: () => setState(() {
                          difficultyFilter = 'advanced';
                          _refreshCourses();
                        }),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: FutureBuilder<List<Course>>(
              future: futureCourses,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return ListView.builder(
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      final course = snapshot.data![index];
                      return CourseCard(
                        course: course,
                        onEnroll: () => _enrollCourse(course.id),
                      );
                    },
                  );
                } else if (snapshot.hasError) {
                  return Center(child: Text('Error: ${snapshot.error}'));
                } else {
                  return Center(child: CircularProgressIndicator());
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onSelected;

  _FilterChip({
    required this.label,
    required this.selected,
    required this.onSelected,
  });

  @override
  Widget build(BuildContext context) {
    return FilterChip(
      label: Text(label),
      selected: selected,
      onSelected: (_) => onSelected(),
    );
  }
}

class CourseCard extends StatelessWidget {
  final Course course;
  final VoidCallback onEnroll;

  CourseCard({
    required this.course,
    required this.onEnroll,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (course.thumbnailUrl != null)
            Container(
              width: double.infinity,
              height: 160,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.vertical(top: Radius.circular(4)),
              ),
              child: Image.network(
                course.thumbnailUrl!,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Center(
                    child: Icon(Icons.image_not_supported, size: 48),
                  );
                },
              ),
            ),
          Padding(
            padding: EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  course.title,
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                SizedBox(height: 4),
                Text(
                  course.description ?? 'No description',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Chip(
                      label: Text(course.difficultyLevel),
                      labelStyle: TextStyle(fontSize: 10),
                    ),
                    Text(
                      '★ ${course.averageRating.toStringAsFixed(1)}',
                      style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      '\$${course.price.toStringAsFixed(2)}',
                      style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                    ElevatedButton(
                      onPressed: onEnroll,
                      child: Text('Enroll'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class Course {
  final int id;
  final String title;
  final String? description;
  final double price;
  final String status;
  final double averageRating;
  final int totalEnrollments;
  final String? thumbnailUrl;
  final String difficultyLevel;

  Course({
    required this.id,
    required this.title,
    this.description,
    required this.price,
    required this.status,
    required this.averageRating,
    required this.totalEnrollments,
    this.thumbnailUrl,
    required this.difficultyLevel,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),
      status: json['status'],
      averageRating: (json['average_rating'] as num).toDouble(),
      totalEnrollments: json['total_enrollments'],
      thumbnailUrl: json['thumbnail_url'],
      difficultyLevel: json['difficulty_level'] ?? 'beginner',
    );
  }
}
