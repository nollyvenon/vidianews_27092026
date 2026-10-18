"""Route tests: literal paths that share a prefix with an id route must reach their own handler.

When a parameterised route is declared first, it captures the literal path and answers 422 for a non-numeric
id, so each assertion here would fail if the handlers were declared in the wrong order."""

import pytest


@pytest.fixture(autouse=True)
def _seed_reference(reference_data):
    """Users 1-2, tenant, organization and content 1 exist for every test in this module."""
    yield


async def test_product_search_reaches_the_search_handler(async_client):
    response = await async_client.get("/api/v1/products/search?q=lamp")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_featured_products_reach_the_featured_handler(async_client):
    response = await async_client.get("/api/v1/products/featured")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_a_numeric_product_id_still_reaches_the_product_handler(async_client):
    response = await async_client.get("/api/v1/products/987654")

    assert response.status_code == 404


async def test_prompt_search_reaches_the_search_handler(async_client, org_member):
    response = await async_client.get("/api/v1/ai/prompts/search?query=welcome", headers=org_member)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_deployed_prediction_models_reach_their_handler(async_client, org_member):
    response = await async_client.get("/api/v1/predictions/models/deployed", headers=org_member)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_pending_returns_reach_their_handler(async_client, platform_admin):
    response = await async_client.get("/api/v1/returns/pending", headers=platform_admin)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
