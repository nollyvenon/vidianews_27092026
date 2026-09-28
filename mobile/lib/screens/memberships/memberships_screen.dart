import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MembershipsScreen extends StatefulWidget {
  @override
  State<MembershipsScreen> createState() => _MembershipsScreenState();
}

class _MembershipsScreenState extends State<MembershipsScreen> {
  late Future<List<MembershipPlan>> futurePlans;
  MembershipSubscription? activeSubscription;

  @override
  void initState() {
    super.initState();
    futurePlans = fetchMembershipPlans();
    _loadActiveSubscription();
  }

  Future<List<MembershipPlan>> fetchMembershipPlans() async {
    final response = await http.get(
      Uri.parse('http://localhost:8000/api/v1/membership-types'),
      headers: {'Authorization': 'Bearer YOUR_TOKEN'},
    );

    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => MembershipPlan.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load plans');
    }
  }

  Future<void> _loadActiveSubscription() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8000/api/v1/subscriptions/me/active'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      if (response.statusCode == 200) {
        setState(() {
          activeSubscription = MembershipSubscription.fromJson(json.decode(response.body));
        });
      }
    } catch (e) {
      print('Error loading subscription: $e');
    }
  }

  Future<void> _subscribe(int planId) async {
    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/api/v1/subscriptions'),
        headers: {
          'Authorization': 'Bearer YOUR_TOKEN',
          'Content-Type': 'application/json',
        },
        body: json.encode({'membership_type_id': planId}),
      );

      if (response.statusCode == 200) {
        setState(() {
          activeSubscription = MembershipSubscription.fromJson(json.decode(response.body));
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Subscribed successfully')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Subscription failed: $e')),
      );
    }
  }

  Future<void> _cancelSubscription() async {
    if (activeSubscription == null) return;

    try {
      await http.post(
        Uri.parse('http://localhost:8000/api/v1/subscriptions/${activeSubscription!.id}/cancel'),
        headers: {'Authorization': 'Bearer YOUR_TOKEN'},
      );

      setState(() {
        activeSubscription = null;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Subscription cancelled')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Cancellation failed: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Membership Plans'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            if (activeSubscription != null)
              Container(
                margin: EdgeInsets.all(16),
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.blue[50],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Active Subscription',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Plan: ${activeSubscription!.membershipType['name']}',
                      style: TextStyle(fontSize: 16),
                    ),
                    Text(
                      'Status: ${activeSubscription!.status}',
                      style: TextStyle(fontSize: 14, color: Colors.grey),
                    ),
                    SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _cancelSubscription,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                      ),
                      child: Text('Cancel Subscription'),
                    ),
                  ],
                ),
              ),
            FutureBuilder<List<MembershipPlan>>(
              future: futurePlans,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return GridView.builder(
                    shrinkWrap: true,
                    physics: NeverScrollableScrollPhysics(),
                    padding: EdgeInsets.all(16),
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      crossAxisSpacing: 16,
                      mainAxisSpacing: 16,
                    ),
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      final plan = snapshot.data![index];
                      final isActive = activeSubscription?.membershipTypeId == plan.id;
                      return MembershipPlanCard(
                        plan: plan,
                        isActive: isActive,
                        onSubscribe: () => _subscribe(plan.id),
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
          ],
        ),
      ),
    );
  }
}

class MembershipPlanCard extends StatelessWidget {
  final MembershipPlan plan;
  final bool isActive;
  final VoidCallback onSubscribe;

  MembershipPlanCard({
    required this.plan,
    required this.isActive,
    required this.onSubscribe,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: isActive ? 4 : 0,
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: isActive ? Colors.blue : Colors.grey[300]!,
            width: isActive ? 2 : 1,
          ),
        ),
        child: Padding(
          padding: EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                plan.name,
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text(
                '\$${plan.price.toStringAsFixed(2)}',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Text(
                'per ${plan.billingCycle}',
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
              SizedBox(height: 8),
              Text(
                'Courses: ${plan.maxCourses == -1 ? "∞" : plan.maxCourses}',
                style: TextStyle(fontSize: 12),
              ),
              Spacer(),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: isActive ? null : onSubscribe,
                  child: Text(isActive ? 'Current Plan' : 'Subscribe'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class MembershipPlan {
  final int id;
  final String name;
  final String tier;
  final double price;
  final String billingCycle;
  final int maxCourses;
  final int maxStudents;
  final Map<String, dynamic> features;

  MembershipPlan({
    required this.id,
    required this.name,
    required this.tier,
    required this.price,
    required this.billingCycle,
    required this.maxCourses,
    required this.maxStudents,
    required this.features,
  });

  factory MembershipPlan.fromJson(Map<String, dynamic> json) {
    return MembershipPlan(
      id: json['id'],
      name: json['name'],
      tier: json['tier'],
      price: (json['price'] as num).toDouble(),
      billingCycle: json['billing_cycle'],
      maxCourses: json['max_courses'],
      maxStudents: json['max_students'],
      features: json['features'] ?? {},
    );
  }
}

class MembershipSubscription {
  final int id;
  final int membershipTypeId;
  final String status;
  final String startDate;
  final String renewalDate;
  final Map<String, dynamic> membershipType;

  MembershipSubscription({
    required this.id,
    required this.membershipTypeId,
    required this.status,
    required this.startDate,
    required this.renewalDate,
    required this.membershipType,
  });

  factory MembershipSubscription.fromJson(Map<String, dynamic> json) {
    return MembershipSubscription(
      id: json['id'],
      membershipTypeId: json['membership_type_id'],
      status: json['status'],
      startDate: json['start_date'],
      renewalDate: json['renewal_date'],
      membershipType: json['membership_type'] ?? {},
    );
  }
}
