"""Reference rows that many tests assume already exist.

Tests refer to users, a tenant, an organization, and a content item by the ids
1 and 2 (for example ``user_id=1``). PostgreSQL enforces those references, so the
parent rows must be committed before the test body runs. The rows are created
through a separate session, which keeps the seed visible to every test session.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.content import Content, ContentType
from app.models.organizations import Organization
from app.models.tenants import Tenant
from app.models.user import User


def seed_reference_data(session: Session) -> None:
    """Insert the reference rows and commit them."""
    session.add_all(
        [
            User(id=1, email="seed-user-1@example.com", password_hash="seed-hash"),
            User(id=2, email="seed-user-2@example.com", password_hash="seed-hash"),
            Tenant(id=1, name="Seed Tenant", slug="seed-tenant"),
        ]
    )
    session.flush()
    session.add(Organization(id=1, tenant_id=1, name="Seed Organization", slug="seed-organization"))
    session.flush()
    session.add(
        Content(
            id=1,
            title="Seed Content",
            slug="seed-content",
            content_type=next(iter(ContentType)),
            creator_user_id=1,
        )
    )
    session.commit()
    # Explicit ids do not advance the serial sequences, so move them past the seeded rows.
    for table in ("users", "tenants", "organizations", "contents"):
        session.execute(
            text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"GREATEST((SELECT MAX(id) FROM {table}), 1), true)"
            )
        )
    session.commit()
