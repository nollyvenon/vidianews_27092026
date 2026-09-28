import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CourseDetailScreen extends StatefulWidget {
  final int courseId;

  CourseDetailScreen({required this.courseId});

  @override
  State<CourseDetailScreen> createState() => _CourseDetailScreenState();
}

class _CourseDetailScreenState extends State<CourseDetailScreen> {
  late Future<CourseDetail> futureCourse;
  CourseEnrollment? enrollment;
  List<CourseSection> sections = [];
  List<CourseReview> reviews = [];
  int reviewRating = 5;
  TextEditingController reviewController = TextEditingController();

  @override
  void initState() {
    super.initState();
    futureCourse = fetchCourseDetail();
    _loadSections();
    _loadReviews();
    _loadEnrollment();
  }

  Future<CourseDetail> fetchCourseDetail() async {
    final response = await http.get(
      Uri.parse('http://localhost:8000/api/v1/courses/${widget.courseId}'),
      headers: {'Authorization': 'Bearer YOUR_TOKEN'},
    );

    if (response.statusCode == 200) {
      return CourseDetail.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load course');
    }
  }

  Future<void> _loadSections() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/courses/${widget.courseId}/sections'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        List jsonResponse = json.decode(response.body);
        setState(() {
          sections = jsonResponse.map((data) => CourseSection.fromJson(data)).toList();
        });
      }
    } catch (e) {
      print('Error loading sections: $e');
    }
  }

  Future<void> _loadReviews() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/courses/${widget.courseId}/reviews'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        List jsonResponse = json.decode(response.body);
        setState(() {
          reviews = jsonResponse.map((data) => CourseReview.fromJson(data)).toList();
        });
      }
    } catch (e) {
      print('Error loading reviews: $e');
    }
  }

  Future<void> _loadEnrollment() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/enrollments/me'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        List jsonResponse = json.decode(response.body);
        var userEnrollment = jsonResponse.firstWhere(
          (e) => e['course_id'] == widget.courseId,
          orElse: () => null,
        );
        if (userEnrollment != null) {
          setState(() {
            enrollment = CourseEnrollment.fromJson(userEnrollment);
          });
        }
      }
    } catch (e) {
      print('Error loading enrollment: $e');
    }
  }

  Future<void> _enrollCourse() async {
    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/api/v1/courses/${widget.courseId}/enroll'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        setState(() {
          enrollment = CourseEnrollment.fromJson(json.decode(response.body));
        });
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

  Future<void> _markLessonComplete(int lessonId) async {
    if (enrollment == null) return;

    try {
      await http.post(
        Uri.parse('http://localhost:8000/api/v1/enrollments/${enrollment!.id}/lessons/$lessonId/complete'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      _loadEnrollment();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Lesson marked as complete')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to mark lesson: $e')),
      );
    }
  }

  Future<void> _submitReview() async {
    if (reviewController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please write a review')),
      );
      return;
    }

    try {
      await http.post(
        Uri.parse('http://localhost:8000/api/v1/courses/${widget.courseId}/reviews'),
        headers: {
          'Authorization': 'Bearer YOUR_TOKEN',
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'rating': reviewRating,
          'content': reviewController.text,
        }),
      );

      reviewController.clear();
      setState(() {
        reviewRating = 5;
      });
      _loadReviews();

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Review submitted')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to submit review: $e')),
      );
    }
  }

  @override
  void dispose() {
    reviewController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<CourseDetail>(
      future: futureCourse,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          final course = snapshot.data!;
          return Scaffold(
            appBar: AppBar(
              title: Text(course.title),
            ),
            body: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          course.title,
                          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text(
                          course.description ?? '',
                          style: TextStyle(color: Colors.grey),
                        ),
                        SizedBox(height: 12),
                        Row(
                          children: [
                            Chip(label: Text(course.difficultyLevel)),
                            SizedBox(width: 8),
                            Text('★ ${course.averageRating.toStringAsFixed(1)}'),
                            SizedBox(width: 8),
                            Text('${course.totalEnrollments} students'),
                          ],
                        ),
                        SizedBox(height: 12),
                        Text(
                          '\$${course.price.toStringAsFixed(2)}',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 16),
                        if (enrollment == null)
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: _enrollCourse,
                              child: Text('Enroll Now'),
                            ),
                          )
                        else
                          Container(
                            padding: EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.green[50],
                              border: Border.all(color: Colors.green),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Enrollment: ${enrollment!.status}',
                                  style: TextStyle(fontWeight: FontWeight.bold),
                                ),
                                SizedBox(height: 8),
                                LinearProgressIndicator(
                                  value: enrollment!.progressPercentage / 100,
                                ),
                                SizedBox(height: 8),
                                Text(
                                  '${enrollment!.lessonsCompleted} lessons completed',
                                  style: TextStyle(fontSize: 12),
                                ),
                              ],
                            ),
                          ),
                      ],
                    ),
                  ),
                  Divider(),
                  if (enrollment != null) ...[
                    Padding(
                      padding: EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Course Content',
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          SizedBox(height: 12),
                          ...sections.map((section) {
                            return ExpansionTile(
                              title: Text(section.title),
                              children: [
                                ListView.builder(
                                  shrinkWrap: true,
                                  physics: NeverScrollableScrollPhysics(),
                                  itemCount: section.lessons?.length ?? 0,
                                  itemBuilder: (context, index) {
                                    final lesson = section.lessons![index];
                                    return ListTile(
                                      title: Text(lesson['title']),
                                      subtitle: Text('${lesson['video_duration']} min'),
                                      trailing: ElevatedButton(
                                        onPressed: () => _markLessonComplete(lesson['id']),
                                        child: Text('Complete'),
                                      ),
                                    );
                                  },
                                ),
                              ],
                            );
                          }).toList(),
                        ],
                      ),
                    ),
                  ],
                  Divider(),
                  Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Reviews',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 12),
                        if (enrollment != null) ...[
                          Container(
                            padding: EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.grey[100],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('Leave a Review', style: TextStyle(fontWeight: FontWeight.bold)),
                                SizedBox(height: 8),
                                Row(
                                  children: [
                                    Text('Rating: '),
                                    DropdownButton<int>(
                                      value: reviewRating,
                                      items: [1, 2, 3, 4, 5].map((r) {
                                        return DropdownMenuItem(
                                          value: r,
                                          child: Text('$r stars'),
                                        );
                                      }).toList(),
                                      onChanged: (value) {
                                        setState(() {
                                          reviewRating = value!;
                                        });
                                      },
                                    ),
                                  ],
                                ),
                                SizedBox(height: 8),
                                TextField(
                                  controller: reviewController,
                                  maxLines: 3,
                                  decoration: InputDecoration(
                                    hintText: 'Share your experience...',
                                    border: OutlineInputBorder(),
                                  ),
                                ),
                                SizedBox(height: 8),
                                ElevatedButton(
                                  onPressed: _submitReview,
                                  child: Text('Submit Review'),
                                ),
                              ],
                            ),
                          ),
                          SizedBox(height: 16),
                        ],
                        ...reviews.map((review) {
                          return Card(
                            margin: EdgeInsets.only(bottom: 8),
                            child: Padding(
                              padding: EdgeInsets.all(12),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text('★ ${review.rating}', style: TextStyle(color: Colors.amber)),
                                    ],
                                  ),
                                  SizedBox(height: 4),
                                  Text(review.content),
                                ],
                              ),
                            ),
                          );
                        }).toList(),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          );
        } else if (snapshot.hasError) {
          return Scaffold(
            appBar: AppBar(title: Text('Error')),
            body: Center(child: Text('Error: ${snapshot.error}')),
          );
        } else {
          return Scaffold(
            appBar: AppBar(title: Text('Loading')),
            body: Center(child: CircularProgressIndicator()),
          );
        }
      },
    );
  }
}

class CourseDetail {
  final int id;
  final String title;
  final String? description;
  final double price;
  final double averageRating;
  final int totalEnrollments;
  final String difficultyLevel;
  final double durationHours;

  CourseDetail({
    required this.id,
    required this.title,
    this.description,
    required this.price,
    required this.averageRating,
    required this.totalEnrollments,
    required this.difficultyLevel,
    required this.durationHours,
  });

  factory CourseDetail.fromJson(Map<String, dynamic> json) {
    return CourseDetail(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),
      averageRating: (json['average_rating'] as num).toDouble(),
      totalEnrollments: json['total_enrollments'],
      difficultyLevel: json['difficulty_level'] ?? 'beginner',
      durationHours: (json['duration_hours'] as num?)?.toDouble() ?? 0,
    );
  }
}

class CourseSection {
  final int id;
  final String title;
  final List<dynamic>? lessons;

  CourseSection({
    required this.id,
    required this.title,
    this.lessons,
  });

  factory CourseSection.fromJson(Map<String, dynamic> json) {
    return CourseSection(
      id: json['id'],
      title: json['title'],
      lessons: json['lessons'],
    );
  }
}

class CourseEnrollment {
  final int id;
  final int courseId;
  final String status;
  final double progressPercentage;
  final int lessonsCompleted;
  final bool certificateIssued;

  CourseEnrollment({
    required this.id,
    required this.courseId,
    required this.status,
    required this.progressPercentage,
    required this.lessonsCompleted,
    required this.certificateIssued,
  });

  factory CourseEnrollment.fromJson(Map<String, dynamic> json) {
    return CourseEnrollment(
      id: json['id'],
      courseId: json['course_id'],
      status: json['status'],
      progressPercentage: (json['progress_percentage'] as num).toDouble(),
      lessonsCompleted: json['lessons_completed'],
      certificateIssued: json['certificate_issued'] ?? false,
    );
  }
}

class CourseReview {
  final int id;
  final int rating;
  final String title;
  final String content;

  CourseReview({
    required this.id,
    required this.rating,
    required this.title,
    required this.content,
  });

  factory CourseReview.fromJson(Map<String, dynamic> json) {
    return CourseReview(
      id: json['id'],
      rating: json['rating'],
      title: json['title'] ?? '',
      content: json['content'] ?? '',
    );
  }
}
