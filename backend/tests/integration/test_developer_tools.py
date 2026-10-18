"""Route tests for the developer tools: the GraphQL explorer, API version registry, and API documentation"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session

from app.models.api_monitoring import APIEndpointVersion, APIVersion, VersionMigration
from app.models.content import Content, ContentAccessLevel, ContentStatus
from app.models.logging_analytics import APIDocumentation


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


def _publish_seed_content(engine, *, views=7):
    with Session(engine) as session:
        content = session.get(Content, 1)
        content.status = ContentStatus.PUBLISHED
        content.access_level = ContentAccessLevel.PUBLIC
        content.published_at = datetime.now(timezone.utc)
        content.views_count = views
        session.commit()


class TestGraphQLExplorer:
    async def test_a_query_returns_only_published_public_content(self, async_client, org_member, reset_test_database):
        _publish_seed_content(reset_test_database)

        response = await async_client.post(
            "/api/v1/graphql/run",
            json={"query": "{ content(id: 1) { id title viewsCount } contents(limit: 5) { id title } }"},
            headers=org_member,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["response"]["data"] == {
            "content": {"id": 1, "title": "Seed Content", "viewsCount": 7},
            "contents": [{"id": 1, "title": "Seed Content"}],
        }
        assert "errors" not in body["response"]
        assert body["elapsed_ms"] >= 0

    async def test_unpublished_content_is_invisible_to_the_explorer(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/graphql/run",
            json={"query": "{ content(id: 1) { title } contents { id } }"},
            headers=org_member,
        )

        body = response.json()["response"]
        assert body["data"] == {"content": None, "contents": []}

    async def test_a_syntax_error_is_reported_in_errors_not_as_a_server_failure(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/graphql/run",
            json={"query": "{ content(id: 1 { title }"},
            headers=org_member,
        )

        assert response.status_code == 200
        body = response.json()["response"]
        assert body["data"] is None
        assert body["errors"][0]["message"]

    async def test_an_unknown_field_is_a_validation_error(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/graphql/run",
            json={"query": "{ contents { notAField } }"},
            headers=org_member,
        )

        assert response.json()["response"]["errors"]

    async def test_an_oversized_query_is_refused(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/graphql/run",
            json={"query": "{ contents { id } }" + " " * 4001},
            headers=org_member,
        )

        assert response.status_code == 422

    async def test_the_explorer_requires_a_signed_in_user(self, async_client):
        response = await async_client.post("/api/v1/graphql/run", json={"query": "{ contents { id } }"})

        assert response.status_code in (401, 403)

    async def test_the_schema_lists_the_content_type_and_its_fields(self, async_client, org_member):
        response = await async_client.get("/api/v1/graphql/schema", headers=org_member)

        types = {item["name"]: item["fields"] for item in response.json()["types"]}
        assert {field["name"] for field in types["Content"]} == {"id", "title", "slug", "description", "viewsCount", "publishedAt"}
        assert {field["name"] for field in types["Query"]} == {"content", "contents"}

    async def test_a_saved_query_is_listed_then_executed_with_its_time_recorded(self, async_client, org_member, reset_test_database):
        _publish_seed_content(reset_test_database)

        saved = await async_client.post(
            "/api/v1/graphql/query",
            json={"name": "LatestContent", "query_string": "{ contents(limit: 3) { id title } }"},
            headers=org_member,
        )
        assert saved.status_code == 201
        query_id = saved.json()["id"]

        listed = await async_client.get("/api/v1/graphql/queries", headers=org_member)
        assert listed.json()[0]["name"] == "LatestContent"
        assert listed.json()[0]["execution_count"] == 0

        executed = await async_client.post("/api/v1/graphql/execute", json={"query_id": query_id}, headers=org_member)
        assert executed.status_code == 200
        assert executed.json()["response"]["data"] == {"contents": [{"id": 1, "title": "Seed Content"}]}

        after = await async_client.get("/api/v1/graphql/queries", headers=org_member)
        assert after.json()[0]["execution_count"] == 1
        assert after.json()[0]["avg_execution_time_ms"] > 0

    async def test_executing_an_unknown_saved_query_is_not_found(self, async_client, org_member):
        response = await async_client.post("/api/v1/graphql/execute", json={"query_id": 999}, headers=org_member)

        assert response.status_code == 404
        assert response.json()["detail"] == "GraphQL query 999 not found"


class TestAPIVersionRegistry:
    async def test_registered_versions_and_migrations_are_listed(self, async_client, org_member, reset_test_database):
        with Session(reset_test_database) as session:
            session.add_all([
                APIEndpointVersion(endpoint="/api/content", version=APIVersion.V1, deprecated=True,
                                   sunset_date=datetime(2026, 12, 31, tzinfo=timezone.utc)),
                APIEndpointVersion(endpoint="/api/content", version=APIVersion.V2, deprecated=False),
            ])
            session.add(VersionMigration(old_version=APIVersion.V1, new_version=APIVersion.V2, status="completed",
                                         executed_at=datetime(2026, 6, 1, tzinfo=timezone.utc)))
            session.commit()

        versions = await async_client.get("/api/v1/versions", headers=org_member)
        migrations = await async_client.get("/api/v1/versions/migrations", headers=org_member)

        assert versions.status_code == 200
        assert [(row["endpoint"], row["version"], row["deprecated"]) for row in versions.json()] == [
            ("/api/content", "v1", True),
            ("/api/content", "v2", False),
        ]
        assert versions.json()[0]["sunset_date"].startswith("2026-12-31")
        assert migrations.json() == [{
            "id": migrations.json()[0]["id"],
            "old_version": "v1",
            "new_version": "v2",
            "status": "completed",
            "executed_at": "2026-06-01T00:00:00+00:00",
        }]

    async def test_the_version_registry_requires_a_signed_in_user(self, async_client):
        response = await async_client.get("/api/v1/versions")

        assert response.status_code in (401, 403)


class TestApiDocumentation:
    async def test_documents_are_created_unpublished_then_published_and_counted(self, async_client, org_member):
        created = await async_client.post(
            "/api/v1/docs",
            json={"title": "Getting Started", "slug": "getting-started", "content": "Welcome", "doc_type": "guide"},
            headers=org_member,
        )
        assert created.status_code == 201
        assert created.json()["published"] is False
        doc_id = created.json()["id"]

        hidden = await async_client.get("/api/v1/docs/getting-started")
        assert hidden.status_code == 404
        assert hidden.json()["detail"] == "Documentation not found"

        await async_client.put(f"/api/v1/docs/{doc_id}/publish", headers=org_member)

        listed = await async_client.get("/api/v1/docs", headers=org_member)
        assert [(d["slug"], d["doc_type"], d["views"]) for d in listed.json()] == [("getting-started", "guide", 0)]

        read = await async_client.get("/api/v1/docs/getting-started")
        assert read.status_code == 200
        assert read.json()["content"] == "Welcome"
        assert read.json()["views"] == 1

        after = await async_client.get("/api/v1/docs", headers=org_member)
        assert after.json()[0]["views"] == 1

    async def test_a_duplicate_slug_is_refused(self, async_client, org_member):
        body = {"title": "One", "slug": "same-slug", "content": "x", "doc_type": "reference"}
        await async_client.post("/api/v1/docs", json=body, headers=org_member)

        second = await async_client.post("/api/v1/docs", json=body, headers=org_member)

        assert second.status_code == 409
        assert second.json()["detail"] == "A document with this slug already exists"

    async def test_a_slug_must_be_lowercase_words_joined_by_hyphens(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/docs",
            json={"title": "Bad", "slug": "Not A Slug", "content": "x", "doc_type": "guide"},
            headers=org_member,
        )

        assert response.status_code == 422

    async def test_an_unknown_document_type_is_refused(self, async_client, org_member):
        response = await async_client.post(
            "/api/v1/docs",
            json={"title": "Bad", "slug": "bad-type", "content": "x", "doc_type": "essay"},
            headers=org_member,
        )

        assert response.status_code == 422

    async def test_api_endpoint_documentation_is_listed(self, async_client, reset_test_database):
        with Session(reset_test_database) as session:
            session.add(APIDocumentation(endpoint="/api/v1/content", method="GET", description="List content"))
            session.commit()

        response = await async_client.get("/api/v1/docs/api/all")

        assert response.status_code == 200
        assert response.json()[0]["endpoint"] == "/api/v1/content"
        assert response.json()[0]["method"] == "GET"
