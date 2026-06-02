import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.database import engine, Base

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

def test_register_bank_user_success():
    payload = {
        "account_number": "ACC-EXPAND-2026",
        "name": "Fidel Omondi"
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 200
    
    # Assert Legacy Compatibility stays perfectly functional
    assert response.json()["name"] == "Fidel Omondi"
    
    # Assert New Structural Dual-Writing data architecture is captured cleanly
    assert response.json()["captured_first_name"] == "Fidel"
    assert response.json()["captured_last_name"] == "Omondi"