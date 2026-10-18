"""Smoke test over every GET route: each one must answer without a server error.

Path parameters are filled with a sample value, so routes answer 404 or 422 for ids that do not exist; what this
test refuses is a 500, which means the handler itself failed (for example a blocking session awaited, or a
missing import). Routes that legitimately need a value the smoke test cannot supply are listed in
KNOWN_SAMPLE_GAPS with the reason, and must stay short."""

import re

import pytest
from fastapi.routing import APIRoute

from app.main import app

SAMPLE_PATH_VALUE = "1"

# Routes whose handler is expected to need input this smoke test does not provide. Keep this list empty
# where possible: an entry here is a route nobody has exercised end to end.
KNOWN_SAMPLE_GAPS: dict = {}


def _get_routes():
    seen = set()
    routes = []
    for route in app.routes:
        if not isinstance(route, APIRoute) or "GET" not in route.methods:
            continue
        if not route.path.startswith("/api/v1"):
            continue
        key = route.path
        if key in seen:
            continue
        seen.add(key)
        routes.append(route.path)
    return routes


def _concrete(path: str) -> str:
    return re.sub(r"\{[^}]+\}", SAMPLE_PATH_VALUE, path)


@pytest.mark.parametrize("path", _get_routes())
async def test_get_route_does_not_fail_on_the_server(path, async_client, org_member, reference_data):
    url = _concrete(path)
    if url in KNOWN_SAMPLE_GAPS:
        pytest.skip(KNOWN_SAMPLE_GAPS[url])
    response = await async_client.get(url, headers=org_member)
    assert response.status_code < 500, f"GET {url} answered {response.status_code}: {response.text[:300]}"


MUTATING_METHODS = ("POST", "PUT", "PATCH", "DELETE")


def _mutating_routes():
    seen = set()
    routes = []
    for route in app.routes:
        if not isinstance(route, APIRoute) or not route.path.startswith("/api/v1"):
            continue
        for method in sorted(set(route.methods) & set(MUTATING_METHODS)):
            key = (method, route.path)
            if key not in seen:
                seen.add(key)
                routes.append(key)
    return routes


@pytest.mark.parametrize("method,path", _mutating_routes())
async def test_mutating_route_does_not_fail_on_the_server(method, path, async_client, org_member, reference_data):
    url = _concrete(path)
    if url in KNOWN_SAMPLE_GAPS:
        pytest.skip(KNOWN_SAMPLE_GAPS[url])
    response = await async_client.request(method, url, json={}, headers=org_member)
    assert response.status_code < 500, f"{method} {url} answered {response.status_code}: {response.text[:300]}"
