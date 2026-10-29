
import pytest
from app import app
import app as banking

@pytest.fixture
def client():
    banking.balance = 1000.00
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple Banking App" in response.data

def test_balance_enquiry(client):
    response = client.get("/api/balance")
    assert response.status_code == 200
    assert response.json["balance"] == 1000.00

def test_successful_deposit(client):
    response = client.post("/api/deposit", json={"amount": 250})
    assert response.status_code == 200
    assert response.json["balance"] == 1250.00

def test_reject_zero_deposit(client):
    response = client.post("/api/deposit", json={"amount": 0})
    assert response.status_code == 400

def test_successful_withdrawal(client):
    response = client.post("/api/withdraw", json={"amount": 200})
    assert response.status_code == 200
    assert response.json["balance"] == 800.00

def test_reject_withdrawal_exceeding_balance(client):
    response = client.post("/api/withdraw", json={"amount": 1500})
    assert response.status_code == 400
    assert response.json["message"] == "Insufficient balance."
    assert banking.balance == 1000.00

def test_reject_zero_withdrawal(client):
    response = client.post("/api/withdraw", json={"amount": 0})
    assert response.status_code == 400

def test_reject_negative_withdrawal(client):
    response = client.post("/api/withdraw", json={"amount": -50})
    assert response.status_code == 400

def test_reject_invalid_deposit(client):
    response = client.post("/api/deposit", json={"amount": "invalid"})
    assert response.status_code == 400
