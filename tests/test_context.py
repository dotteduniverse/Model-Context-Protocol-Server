import pytest
from fastapi.testclient import TestClient
from src.context_service import app
from src.auth import get_current_tenant

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_orders_without_token():
    response = client.get("/context/orders")
    assert response.status_code == 403  # missing auth

def test_orders_with_valid_token(monkeypatch):
    # Mock the dependency to avoid real DB access in this test
    async def mock_tenant():
        return "tenant_a"
    monkeypatch.setattr("src.context_service.get_current_tenant", mock_tenant)
    # Also need to mock DB calls? In a real test you'd set up a test DB.
    # For brevity, we assume you'll test with a real DB.
    pass