"""Shared fixtures for route-level tests that need a signed-in organization member"""

import pytest
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.organizations import Organization, OrganizationMember
from app.models.user import Role, User, user_roles


def _bearer(email: str, user_id: int) -> dict:
    token = create_access_token({"sub": email, "user_id": user_id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def org_member(reference_data, reset_test_database):
    """User 1 is an active admin of organization 1, which belongs to tenant 1. Returns user 1's bearer headers."""
    with Session(reset_test_database) as session:
        session.add(OrganizationMember(organization_id=1, user_id=1, role="admin", status="active"))
        session.commit()
        email = session.get(User, 1).email
    return _bearer(email, 1)


@pytest.fixture
def platform_admin(org_member, reference_data, reset_test_database):
    """User 1 also holds the platform admin role, so administrator-only routes admit them."""
    with Session(reset_test_database) as session:
        role = Role(name="admin", description="Administrator")
        session.add(role)
        session.flush()
        session.execute(user_roles.insert().values(user_id=1, role_id=role.id))
        session.commit()
    return org_member


@pytest.fixture
def second_organization(reference_data, reset_test_database):
    """Organization 2 in the same tenant, so tests can prove one organization cannot reach another's records."""
    with Session(reset_test_database) as session:
        session.add(Organization(id=2, tenant_id=1, name="Second Organization", slug="second-organization"))
        session.commit()
    return 2


@pytest.fixture
def unaffiliated_user(reference_data, reset_test_database):
    """User 2 belongs to no organization, so organization-scoped routes must refuse them."""
    with Session(reset_test_database) as session:
        email = session.get(User, 2).email
    return _bearer(email, 2)
