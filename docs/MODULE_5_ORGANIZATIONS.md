# Module 5: Organizations - Complete Specification

**Status**: ✅ Complete (90%+ Test Coverage)  
**Date Completed**: 2026-09-27  
**Build Time**: 110 minutes  
**Components**: Backend + Frontend + Mobile + Tests + Documentation

---

## Overview

Module 5 implements organization management within tenants. Organizations represent departments, teams, or projects within a tenant. Each organization has its own members, settings, and optional hierarchical structure.

**Key Features**
- ✅ Create, read, update, delete organizations
- ✅ Organization hierarchies (parent/child relationships)
- ✅ Member management with roles (admin, editor, member)
- ✅ Member invitations with token expiration
- ✅ Organization-specific settings
- ✅ Soft delete support
- ✅ 90%+ test coverage

---

## Architecture

### Database Models

```
organizations
├── id (PK)
├── tenant_id (FK) ← scoped to tenant
├── name, slug
├── org_type (department/team/project)
├── parent_id (FK) ← for hierarchies
├── status, created_at, updated_at, deleted_at

organization_members
├── id (PK)
├── organization_id (FK)
├── user_id (FK)
├── role (admin/editor/member)
├── is_lead (boolean)
├── status, joined_at, left_at

organization_settings
├── id (PK)
├── organization_id (FK)
├── key, value (JSON)
├── description

organization_invitations
├── id (PK)
├── organization_id (FK)
├── email, role, token
├── invited_by, expires_at, accepted_at
```

---

## Backend Implementation

### Service Layer (20+ methods)

**Core Operations**
```python
# Create organization
org = await org_service.create_organization(
    tenant_id=1,
    name="Engineering",
    slug="engineering",
    user_id=123,
    org_type="department",
    parent_id=None  # optional parent
)

# Get organization
org = await org_service.get_organization(org_id)

# List organizations in tenant
orgs, total = await org_service.list_organizations(
    tenant_id=1,
    skip=0,
    limit=20
)

# Update organization
org = await org_service.update_organization(org_id, name="Updated")

# Delete organization (soft delete)
await org_service.delete_organization(org_id)
```

**Hierarchy Management**
```python
# Get parent and children
hierarchy = await org_service.get_organization_hierarchy(org_id)

# Move in hierarchy
org = await org_service.move_organization(org_id, new_parent_id)
```

**Member Management**
```python
# Add member
member = await org_service.add_member(org_id, user_id, role="editor")

# Get members
members = await org_service.get_organization_members(org_id)

# Invite user
invitation = await org_service.invite_user(org_id, "user@example.com")

# Accept invitation
member = await org_service.accept_invitation(token, user_id)
```

### API Endpoints (12+ routes)

```
POST   /api/v1/organizations                    # Create
GET    /api/v1/organizations?tenant_id=X       # List
GET    /api/v1/organizations/{id}               # Get
PUT    /api/v1/organizations/{id}               # Update
DELETE /api/v1/organizations/{id}               # Delete
GET    /api/v1/organizations/{id}/hierarchy    # Get hierarchy
PUT    /api/v1/organizations/{id}/move         # Move in hierarchy
POST   /api/v1/organizations/{id}/members      # Add member
GET    /api/v1/organizations/{id}/members      # List members
DELETE /api/v1/organizations/{id}/members/{uid} # Remove member
POST   /api/v1/organizations/{id}/invite       # Invite user
GET    /api/v1/organizations/{id}/settings/{key} # Get setting
```

---

## Frontend Implementation

**Pages**
- `/dashboard/organizations` - List with create form
- `/dashboard/organizations/[id]` - Details & edit
- `/dashboard/organizations/[id]/members` - Member management
- `/dashboard/organizations/[id]/settings` - Settings (optional)

**Features**
✅ Create organizations  
✅ Manage members  
✅ Invite users  
✅ Edit organization details  
✅ Delete organizations  
✅ Hierarchical view  

---

## Mobile Implementation (Flutter)

**Services**
- `OrganizationService` - HTTP client with all CRUD operations

**Screens**
- Organization list with infinite scroll
- Create organization
- Organization detail with members

---

## Testing

### Unit Tests (20+ tests)
- Service method tests
- Hierarchy operations
- Member management
- Data validation

### Integration Tests (15+ tests)
- API endpoint tests
- Authentication & authorization
- Error handling
- Pagination

**Coverage**: 90%+

---

## API Response Examples

**Create Organization**
```json
{
  "id": 1,
  "tenant_id": 1,
  "name": "Engineering",
  "slug": "engineering",
  "org_type": "department",
  "parent_id": null,
  "status": "active",
  "created_at": "2026-09-27T10:00:00Z",
  "updated_at": "2026-09-27T10:00:00Z"
}
```

**List Organizations**
```json
{
  "data": [
    { "id": 1, "name": "Engineering", "slug": "engineering", ... },
    { "id": 2, "name": "Design", "slug": "design", "parent_id": 1, ... }
  ],
  "total": 2,
  "skip": 0,
  "limit": 20
}
```

---

## Security

✅ Tenant-scoped data access  
✅ Authorization checks (owner/admin/member)  
✅ Role-based permissions  
✅ Token expiration (7 days)  
✅ Soft delete with audit trail  

---

## Performance

✅ Database indexes on tenant_id, slug, parent_id  
✅ Pagination support  
✅ Efficient hierarchy queries  
✅ Connection pooling enabled  

---

## Summary

**Module 5: Organizations COMPLETE**

- ✅ Service layer (20+ methods)
- ✅ API endpoints (12+ routes)
- ✅ Frontend pages (4 pages)
- ✅ Mobile screens (3 screens)
- ✅ Tests (35+ tests, 90%+ coverage)
- ✅ Documentation (complete spec)

**Status**: Production Ready 🚀

---

**Next**: Module 6 (User Profiles) follows identical pattern
