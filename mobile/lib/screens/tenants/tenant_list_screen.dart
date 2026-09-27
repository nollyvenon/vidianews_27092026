import 'package:flutter/material.dart';
import '../../services/tenant_service.dart';

class TenantListScreen extends StatefulWidget {
  final TenantService tenantService;

  const TenantListScreen({Key? key, required this.tenantService})
      : super(key: key);

  @override
  State<TenantListScreen> createState() => _TenantListScreenState();
}

class _TenantListScreenState extends State<TenantListScreen> {
  late Future<List<Tenant>> _tenantsFuture;
  final ScrollController _scrollController = ScrollController();
  int _skip = 0;
  bool _isLoadingMore = false;
  List<Tenant> _allTenants = [];

  @override
  void initState() {
    super.initState();
    _tenantsFuture = widget.tenantService.listTenants();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.position.pixels ==
        _scrollController.position.maxScrollExtent) {
      _loadMore();
    }
  }

  void _loadMore() async {
    if (_isLoadingMore) return;

    setState(() => _isLoadingMore = true);

    try {
      final newTenants = await widget.tenantService.listTenants(skip: _skip + 20);
      setState(() {
        _skip += 20;
        _allTenants.addAll(newTenants);
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading more tenants: $e')),
      );
    } finally {
      setState(() => _isLoadingMore = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tenants'),
        elevation: 0,
      ),
      body: FutureBuilder<List<Tenant>>(
        future: _tenantsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error_outline, size: 64, color: Colors.red[300]),
                  const SizedBox(height: 16),
                  Text('Error: ${snapshot.error}'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        _tenantsFuture =
                            widget.tenantService.listTenants();
                      });
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            _allTenants = [];
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.business_outlined, size: 64, color: Colors.grey[400]),
                  const SizedBox(height: 16),
                  const Text(
                    'No tenants yet',
                    style: TextStyle(fontSize: 18, color: Colors.grey),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Create your first tenant to get started',
                    style: TextStyle(color: Colors.grey),
                  ),
                ],
              ),
            );
          }

          if (_allTenants.isEmpty) {
            _allTenants = snapshot.data!;
          }

          return ListView.builder(
            controller: _scrollController,
            itemCount: _allTenants.length + (_isLoadingMore ? 1 : 0),
            itemBuilder: (context, index) {
              if (index == _allTenants.length) {
                return const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Center(child: CircularProgressIndicator()),
                );
              }

              final tenant = _allTenants[index];
              return TenantCard(
                tenant: tenant,
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => TenantDetailScreen(
                        tenantService: widget.tenantService,
                        tenant: tenant,
                      ),
                    ),
                  );
                },
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => CreateTenantScreen(
                tenantService: widget.tenantService,
              ),
            ),
          );
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

class TenantCard extends StatelessWidget {
  final Tenant tenant;
  final VoidCallback onTap;

  const TenantCard({
    Key? key,
    required this.tenant,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                tenant.name,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                tenant.description ?? 'No description',
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: Colors.grey[600]),
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Chip(
                    label: Text(tenant.plan.toUpperCase()),
                    backgroundColor: _getPlanColor(tenant.plan),
                    labelStyle: const TextStyle(color: Colors.white),
                  ),
                  Text(
                    '${tenant.maxUsers} users',
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getPlanColor(String plan) {
    switch (plan) {
      case 'pro':
        return Colors.blue;
      case 'enterprise':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }
}

class TenantDetailScreen extends StatefulWidget {
  final TenantService tenantService;
  final Tenant tenant;

  const TenantDetailScreen({
    Key? key,
    required this.tenantService,
    required this.tenant,
  }) : super(key: key);

  @override
  State<TenantDetailScreen> createState() => _TenantDetailScreenState();
}

class _TenantDetailScreenState extends State<TenantDetailScreen> {
  late Future<List<TenantMember>> _membersFuture;

  @override
  void initState() {
    super.initState();
    _membersFuture = widget.tenantService.getTenantMembers(widget.tenant.id);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.tenant.name),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        widget.tenant.name,
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Slug: ${widget.tenant.slug}',
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        widget.tenant.description ?? 'No description',
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                      const SizedBox(height: 16),
                      Wrap(
                        spacing: 8,
                        children: [
                          Chip(label: Text('Plan: ${widget.tenant.plan}')),
                          Chip(label: Text('Users: ${widget.tenant.maxUsers}')),
                          Chip(
                            label: Text('Status: ${widget.tenant.status}'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'Members',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 12),
              FutureBuilder<List<TenantMember>>(
                future: _membersFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  }

                  if (snapshot.hasError) {
                    return Text('Error: ${snapshot.error}');
                  }

                  final members = snapshot.data ?? [];

                  return ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: members.length,
                    itemBuilder: (context, index) {
                      final member = members[index];
                      return ListTile(
                        title: Text('User #${member.userId}'),
                        subtitle: Text(member.role),
                        trailing: member.isOwner
                            ? const Chip(label: Text('Owner'))
                            : null,
                      );
                    },
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class CreateTenantScreen extends StatefulWidget {
  final TenantService tenantService;

  const CreateTenantScreen({
    Key? key,
    required this.tenantService,
  }) : super(key: key);

  @override
  State<CreateTenantScreen> createState() => _CreateTenantScreenState();
}

class _CreateTenantScreenState extends State<CreateTenantScreen> {
  final _nameController = TextEditingController();
  final _slugController = TextEditingController();
  final _descriptionController = TextEditingController();
  String _selectedPlan = 'free';
  bool _isLoading = false;

  @override
  void dispose() {
    _nameController.dispose();
    _slugController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  void _createTenant() async {
    setState(() => _isLoading = true);

    try {
      await widget.tenantService.createTenant(
        name: _nameController.text,
        slug: _slugController.text,
        description: _descriptionController.text,
        plan: _selectedPlan,
      );

      if (mounted) {
        Navigator.of(context).pop(true);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Tenant created successfully')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Tenant'),
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Tenant Name',
                  hintText: 'Enter tenant name',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _slugController,
                decoration: const InputDecoration(
                  labelText: 'Slug',
                  hintText: 'tenant-slug',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description',
                  hintText: 'Enter description',
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: _selectedPlan,
                decoration: const InputDecoration(
                  labelText: 'Plan',
                  border: OutlineInputBorder(),
                ),
                items: ['free', 'pro', 'enterprise']
                    .map((plan) =>
                        DropdownMenuItem(value: plan, child: Text(plan)))
                    .toList(),
                onChanged: (value) {
                  setState(() => _selectedPlan = value!);
                },
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isLoading ? null : _createTenant,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Create Tenant'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
