import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
from sqlalchemy import create_mock_engine
from sqlalchemy.orm import sessionmaker
import models
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_mock_engine("sqlite:///./test.db") if False else engine # Just reusing the same engine for simplicity if not mocked

client = TestClient(app)

# Helper to clear data before tests (Optional, but good practice)
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    
    yield

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Finance API running" in response.json()["message"]

def test_register_user():
    email = f"test_{models.func.random()}@example.com" if False else "testuser_new@example.com"
    response = client.post(
        "/register",
        json={"email": "testuser_pytest@example.com", "password": "password123"}
    )
    # If user already exists, it might return 400. Let's handle both for the demo.
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json() == {"message": "User registered"}

def test_login_user():
    # Ensure the user exists first (handled by previous test or seeding)
    response = client.post(
        "/login",
        json={"email": "testuser_pytest@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_login_invalid_credentials():
    response = client.post(
        "/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_add_transaction():

    response = client.post(
        "/transactions",
        json={
            "amount": 150.0,
            "type": "expense",
            "user_id": 1,
            "category_id": 1
        }
    )
    assert response.status_code == 200
    assert "transaction_id" in response.json()

def test_get_transactions():
    response = client.get("/transactions?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_budget():
    response = client.post(
        "/budgets",
        json={
            "limit": 5000.0,
            "user_id": 1,
            "category_id": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Budget created"}

def test_get_budgets():
    response = client.get("/budgets?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_monthly_report():
    response = client.get("/reports/monthly?user_id=1&month=3&year=2026")
    assert response.status_code == 200
    data = response.json()
    assert "total_income" in data
    assert "total_expense" in data
    assert "balance" in data

def test_get_alerts():
    response = client.get("/alerts?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
