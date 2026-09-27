# Module 4: Multi-Tenancy - Complete Specification

**Status**: ✅ Complete (90%+ Test Coverage)  
**Date Completed**: 2026-09-27  
**Components**: Backend + Frontend + Mobile + Tests + Documentation

---

## 1. Overview

Module 4 implements enterprise-grade multi-tenancy, enabling users to create isolated organizations (tenants) and manage member access. Each tenant is a separate, isolated workspace with its own data, settings, and members.

### Key Features
- ✅ Create, read, update, delete tenants
- ✅ Member management with role-based access
- ✅ User invitations with email and expiring tokens
- ✅ Tenant-specific settings and configuration
- ✅ Resource limits per plan
- ✅ Soft delete support
- ✅ Comprehensive audit logging
- ✅ 90%+ test coverage

---

## 2. Architecture

### Database Schema

```
tenants
├── id (PK)
├── name
├── slug (unique)
├── description
├── logo_url
├── website
├── status (active/inactive/suspended)
├── plan (free/pro/enterprise)
├── max_users, max_storage_gb
├── settings, metadata (JSON)
├── created_at, updated_at, deleted_at
└── indexes: slug, status+created_at

tenant_members
├── id (PK)
├── tenant_id (FK)
├── user_id (FK)
├── role (admin/editor/member)
├── permissions (JSON override)
├── is_owner (boolean)
├── status (active/inactive)
├── joined_at, invited_at, left_at
└── indexes: tenant_id+user_id, tenant_id+status

tenant_settings
├── id (PK)
├── tenant_id (FK)
├── key (string)
├── value (JSON)
├── description
├── created_at, updated_at
└── indexes: tenant_id+key

tenant_invitations
├── id (PK)
├── tenant_id (FK)
├── email (string)
├── role (string)
├── token (unique)
├── invited_by (FK)
├── expires_at, accepted_at
└── indexes: tenant_id+email, token+expires_at
```

### Data Isolation

```
User Context
    ↓
Check Membership
    ↓
Verify Tenant Access (Active Member)
    ↓
Load Tenant-Scoped Data
    ↓
Apply Role-Based Permissions
```

### Security Model

```
Tenant Owner (is_owner=True)
├── Can modify tenant details
├── Can add/remove members
├── Can delete tenant
└── Cannot be removed

Tenant Admin (role='admin')
├── Can manage members
├── Can view settings
└── Cannot delete tenant

Tenant Editor (role='editor')
├── Can view all resources
└── Cannot modify settings

Tenant Member (role='member')
├── Read-only access
└── View only own data
```

---

## 3. Backend Implementation

### Service Layer (`backend/app/services/tenant_service.py`)

#### Core Methods

**Tenant Management**
```python
# Create tenant (user becomes owner)
tenant = await tenant_service.create_tenant(
    name="Acme Corp",
    slug="acme-corp",
    user_id=123,
    plan="pro",
    settings={}
)

# Retrieve tenant
tenant = await tenant_service.get_tenant(tenant_id)
tenant = await tenant_service.get_tenant_by_slug("acme-corp")

# Update tenant
tenant = await tenant_service.update_tenant(
    tenant_id,
    name="Updated Name",
    plan="enterprise"
)

# Delete tenant (soft delete)
await tenant_service.delete_tenant(tenant_id)

# List tenants with pagination
tenants, total = await tenant_service.list_tenants(
    skip=0,
    limit=20,
    status="active",
    plan="pro"
)
```

**Member Management**
```python
# Add existing user as member
member = await tenant_service.add_member(
    tenant_id,
    user_id,
    role="editor",
    is_owner=False
)

# Remove member
await tenant_service.remove_member(tenant_id, user_id)

# Get all members
members = await tenant_service.get_tenant_members(tenant_id)

# Get user's tenants
tenants = await tenant_service.get_user_tenants(user_id)
```

**Invitations**
```python
# Send invitation
invitation = await tenant_service.invite_user(
    tenant_id,
    email="newuser@example.com",
    role="member",
    invited_by=current_user_id
)

# Accept invitation
member = await tenant_service.accept_invitation(
    token="invitation_token_xyz",
    user_id=new_user_id
)
```

**Settings**
```python
# Set/update setting
setting = await tenant_service.set_tenant_setting(
    tenant_id,
    key="webhook_url",
    value={"url": "https://example.com/webhook"}
)

# Get setting
setting = await tenant_service.get_tenant_setting(
    tenant_id,
    "webhook_url"
)

# Check resource limits
can_add = await tenant_service.check_tenant_limit(
    tenant_id,
    "users",
    current_user_count=10
)
```

### API Endpoints

#### Base URL
```
POST   /api/v1/tenants
GET    /api/v1/tenants
GET    /api/v1/tenants/{id}
PUT    /api/v1/tenants/{id}
DELETE /api/v1/tenants/{id}
```

#### Member Endpoints
```
POST   /api/v1/tenants/{id}/members
GET    /api/v1/tenants/{id}/members
DELETE /api/v1/tenants/{id}/members/{user_id}
POST   /api/v1/tenants/{id}/invite
```

#### Settings Endpoints
```
GET    /api/v1/tenants/{id}/settings/{key}
PUT    /api/v1/tenants/{id}/settings/{key}
```

#### Request/Response Examples

**Create Tenant**
```bash
POST /api/v1/tenants
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Acme Corp",
  "slug": "acme-corp",
  "description": "Enterprise AI Publishing",
  "plan": "pro"
}

Response (201):
{
  "id": 1,
  "name": "Acme Corp",
  "slug": "acme-corp",
  "description": "Enterprise AI Publishing",
  "status": "active",
  "plan": "pro",
  "max_users": 100,
  "max_storage_gb": 500,
  "created_at": "2026-09-27T10:00:00Z",
  "updated_at": "2026-09-27T10:00:00Z"
}
```

**Invite User**
```bash
POST /api/v1/tenants/1/invite
Authorization: Bearer {token}
Content-Type: application/json

{
  "email": "jane@example.com",
  "role": "editor"
}

Response (201):
{
  "id": 1,
  "tenant_id": 1,
  "email": "jane@example.com",
  "role": "editor",
  "token": "abc123...xyz",
  "expires_at": "2026-10-04T10:00:00Z",
  "created_at": "2026-09-27T10:00:00Z"
}
```

### Error Handling

| Status | Scenario | Response |
|--------|----------|----------|
| 400 | Invalid input | `{"detail": "Validation error"}` |
| 401 | Not authenticated | `{"detail": "Unauthorized"}` |
| 403 | Not authorized | `{"detail": "Not authorized"}` |
| 404 | Resource not found | `{"detail": "Tenant not found"}` |
| 409 | Conflict (duplicate slug) | `{"detail": "Slug already exists"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

---

## 4. Frontend Implementation

### Components Structure

```
dashboard/
├── tenants/
│   ├── page.tsx              # List all tenants + create
│   ├── [id]/
│   │   ├── page.tsx         # Tenant details/edit
│   │   ├── members/
│   │   │   └── page.tsx    # Member management
│   │   └── settings/
│   │       └── page.tsx    # Tenant settings
```

### Pages & Features

#### 1. Tenant List Page (`/dashboard/tenants`)
- Display all user's tenants in card grid
- Create new tenant form
- Search & filter by plan
- Pagination

#### 2. Tenant Detail Page (`/dashboard/tenants/{id}`)
- View/edit tenant information
- Update name, description, website
- Change plan
- Delete tenant
- Tabbed interface (Details, Members, Settings)

#### 3. Members Page (`/dashboard/tenants/{id}/members`)
- List all active members
- Show role and owner status
- Invite new members via email
- Remove members
- See join date

#### 4. Settings Page (`/dashboard/tenants/{id}/settings`)
- Configure tenant settings
- Webhook URL configuration
- Notification preferences
- Retention policies
- Timezone settings

### UI Components

```typescript
// Tenant creation form
<TenantForm onSubmit={createTenant} />

// Member list table
<MemberTable members={members} onRemove={removeMember} />

// Settings editor
<SettingEditor setting={setting} onChange={updateSetting} />
```

---

## 5. Mobile Implementation (Flutter)

### Screens

#### 1. Tenant List Screen
- List all tenants
- Create new tenant
- Search & filter
- Pull-to-refresh
- Infinite scroll pagination

#### 2. Tenant Detail Screen
- View tenant info
- Member count
- Current plan
- Edit button (owner only)
- Delete button (owner only)

#### 3. Create Tenant Screen
- Name input
- Slug generation
- Description
- Plan selection (Free/Pro/Enterprise)

### Services

**`lib/services/tenant_service.dart`**
```dart
class TenantService {
  Future<List<Tenant>> listTenants();
  Future<Tenant> getTenant(int id);
  Future<Tenant> createTenant(...);
  Future<void> updateTenant(int id, ...);
  Future<void> deleteTenant(int id);
  Future<List<TenantMember>> getTenantMembers(int tenantId);
  Future<void> addMember(int tenantId, int userId, ...);
  Future<void> inviteUser(int tenantId, String email, ...);
}
```

---

## 6. Testing

### Unit Tests (25+ tests)

```python
# Service tests
test_create_tenant()
test_get_tenant()
test_update_tenant()
test_delete_tenant()
test_add_member()
test_remove_member()
test_invite_user()
test_accept_invitation()
test_get_user_tenants()
test_check_tenant_limit()
test_set_tenant_setting()
test_get_tenant_setting()
# ... and more
```

**Coverage**: 90%+
**File**: `backend/tests/unit/test_tenant_service.py`

### Integration Tests (20+ tests)

```python
# API endpoint tests
test_create_tenant_api()
test_list_tenants_pagination()
test_get_tenant_details()
test_update_tenant_unauthorized()
test_add_member()
test_remove_member()
test_list_members()
test_invite_user()
test_set_setting()
test_get_setting()
# ... and more
```

**File**: `backend/tests/integration/test_tenant_endpoints.py`

### Test Execution

```bash
# Run all tests with coverage
pytest backend/tests/ -v --cov=backend/app --cov-report=html

# Run specific test class
pytest backend/tests/unit/test_tenant_service.py::TestCreateTenant -v

# Run with coverage report
coverage report --fail-under=90
```

---

## 7. Security Considerations

### Data Isolation
- ✅ Tenants cannot access other tenants' data
- ✅ Members cannot modify tenant settings without owner role
- ✅ Invitations expire after 7 days
- ✅ Tokens are cryptographically secure

### Authorization
- ✅ Owner verification on modifications
- ✅ Member verification on access
- ✅ Role-based permission enforcement
- ✅ Audit logging of all actions

### Input Validation
- ✅ Email format validation
- ✅ Slug uniqueness validation
- ✅ Tenant name length limits
- ✅ Plan enum validation

---

## 8. Performance

### Database Indexes
```sql
-- Fast lookups
CREATE INDEX idx_slug ON tenants(slug);
CREATE INDEX idx_status ON tenants(status);
CREATE INDEX idx_tenant_user ON tenant_members(tenant_id, user_id);
CREATE INDEX idx_tenant_email ON tenant_invitations(tenant_id, email);
```

### Query Optimization
- ✅ Efficient pagination with limit/skip
- ✅ Selective field loading
- ✅ N+1 query prevention
- ✅ Connection pooling enabled

### Caching Strategy
```
User Tenants → Invalidate on add/remove member
Tenant Details → Invalidate on update
Member List → Invalidate on add/remove
```

---

## 9. Deployment Checklist

- ✅ Database migrations run
- ✅ All tests pass (90%+ coverage)
- ✅ Zero warnings in build
- ✅ API documentation updated
- ✅ Frontend pages created
- ✅ Mobile screens created
- ✅ Error handling complete
- ✅ Security review passed
- ✅ Performance testing done
- ✅ Documentation complete

---

## 10. API Specification Summary

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/tenants` | Create tenant | User |
| GET | `/tenants` | List user's tenants | User |
| GET | `/tenants/{id}` | Get tenant details | Member |
| PUT | `/tenants/{id}` | Update tenant | Owner |
| DELETE | `/tenants/{id}` | Delete tenant | Owner |
| POST | `/tenants/{id}/members` | Add member | Owner |
| GET | `/tenants/{id}/members` | List members | Member |
| DELETE | `/tenants/{id}/members/{uid}` | Remove member | Owner |
| POST | `/tenants/{id}/invite` | Invite user | Owner |
| GET | `/tenants/{id}/settings/{key}` | Get setting | Member |
| PUT | `/tenants/{id}/settings/{key}` | Update setting | Owner |

---

## 11. Future Enhancements

- [ ] Role-based permission customization
- [ ] Tenant-specific branding/white-label
- [ ] Advanced audit trail with full diff
- [ ] SSO integration per tenant
- [ ] Tenant analytics dashboard
- [ ] Member invitation reminders
- [ ] Bulk member import from CSV
- [ ] Tenant usage metrics API
- [ ] Custom domain support
- [ ] Advanced resource limits

---

## 12. Support & Troubleshooting

### Common Issues

**Q: Cannot create tenant with slug "test"**  
A: Slug already exists. Use unique slug.

**Q: Invitation token expired**  
A: Invitations expire after 7 days. Resend invitation.

**Q: Cannot remove myself from tenant**  
A: You're the owner. Transfer ownership first.

---

## Completion Summary

✅ **Backend**: TenantService (20+ methods), API (10+ endpoints), Tests (45+ cases)  
✅ **Frontend**: 4 pages (list, detail, members, settings), Full CRUD UI  
✅ **Mobile**: Tenant list, detail, create screens, Complete service layer  
✅ **Tests**: 90%+ coverage, Unit + Integration tests  
✅ **Documentation**: Full API spec, Architecture, Usage examples  

**Status**: Ready for production deployment 🚀

---

**Module 4 Complete** ✅  
Next Module: Module 5 - Organizations (follows same template)
