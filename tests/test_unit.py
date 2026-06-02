import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Clean up stale test database assets on disk before initializing the test runtime
if os.path.exists("./novapay_test.db"):
    try:
        os.remove("./novapay_test.db")
    except Exception:
        pass

if os.path.exists("./novapay_isolated_test.db"):
    try:
        os.remove("./novapay_isolated_test.db")
    except Exception:
        pass

# 2. Import your application core components explicitly from src
from src.app.main import app
from src.app.database import Base, get_db

# 3. Establish a completely fresh, unique file path for this test run
TEST_DATABASE_URL = "sqlite:///./novapay_isolated_test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 4. Rebuild the schema cleanly from scratch using our fresh engine instance
Base.metadata.drop_all(bind=test_engine)
Base.metadata.create_all(bind=test_engine)

# 5. Inject a dynamic dependency override to force FastAPI to use our clean engine session
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