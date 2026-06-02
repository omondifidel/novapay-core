import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Verify health and regulatory compliance flags are exposed."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"
    assert response.json()["compliance"] == "RBI-AUDIT-COMPLIANT"

def test_register_bank_user_success():
    """Verify clean transaction database insertions via API payload."""
    payload = {
        "account_number": "ACC-FIN-2026",
        "name": "Fidel Omondi"
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "KYC_PENDING"
    assert response.json()["name"] == "Fidel Omondi"