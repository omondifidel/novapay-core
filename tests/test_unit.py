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
        "account_number": "ACC-CONTRACT-2026",
        "first_name": "Fidel",
        "last_name": "Omondi"
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 200
    
    # Assert Contracted Architecture fields function flawlessly
    assert response.json()["captured_first_name"] == "Fidel"
    assert response.json()["captured_last_name"] == "Omondi"
    assert "name" not in response.json()  # Confirm legacy name field is completely gone