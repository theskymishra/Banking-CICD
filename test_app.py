import app as banking


def setup_function():
    banking.balance = 1000.00


def test_homepage():
    response = banking.app.test_client().get("/")
    assert response.status_code == 200
    assert b"NovaBank" in response.data


def test_balance():
    response = banking.app.test_client().get("/api/balance")
    assert response.status_code == 200
    assert response.get_json()["balance"] == 1000.00


def test_deposit():
    response = banking.app.test_client().post(
        "/api/deposit", json={"amount": 250}
    )
    assert response.status_code == 200
    assert response.get_json()["balance"] == 1250.00


def test_reject_zero_deposit():
    response = banking.app.test_client().post(
        "/api/deposit", json={"amount": 0}
    )
    assert response.status_code == 400
