import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Import your core application setup components
from src.app.main import app
from src.app.database import Base, get_db

# 2. Establish a completely isolated, clean file database path for this run
TEST_DATABASE_URL = "sqlite:///./novapay_isolated_test.db"

# 3. Build a dedicated, isolated engine for the test lifecycle
test_engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 4. Programmatically clean and rebuild the isolated schema structure
Base.metadata.drop_all(bind=test_engine)
Base.metadata.create_all(bind=test_engine)

# 5. Override FastAPI's database dependency injection to use our clean testing session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

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
    assert "name" not in response.json()