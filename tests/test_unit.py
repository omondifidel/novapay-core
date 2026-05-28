from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"

def test_invalid_transaction_amount():
    # Send a faulty payload with a negative amount
    payload = {"account_id": "ACC-1234", "amount": -500.0, "currency": "KES"}
    response = client.post("/api/v1/transactions", json=payload)
    
    # Assert that our API successfully catches the invalid transaction
    assert response.status_code == 400
    assert response.json()["detail"] == "Transaction amount must be positive."