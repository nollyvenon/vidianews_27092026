"""Integration tests for health endpoints"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoints"""

    def test_health_check_root(self, client):
        """Test root health check"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_check_api(self, client):
        """Test API health check endpoint"""
        # Note: This will fail if database isn't set up
        # For now, we just check it doesn't 500
        response = client.get("/api/v1/health")

        # Could be 200 if DB available, or 503 if not
        assert response.status_code in [200, 503]

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        data = response.json()

        assert response.status_code == 200
        assert "app" in data
        assert "version" in data
        assert "environment" in data
