import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def default_category(client: TestClient):
    response = client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def multiple_transactions_per_category(client: TestClient, default_category: dict):
    response = client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body is not None
    category_id = body["id"]
    client.post(
        "/api/v1/transactions",
        json={
            "amount": 12.3,
            "description": "Pollo",
            "repetition": "weekly",
            "category_id": category_id,
        },
    )
    client.post(
        "/api/v1/transactions",
        json={
            "amount": 4.3,
            "description": "Curry",
            "repetition": "weekly",
            "category_id": category_id,
        },
    )
    client.post(
        "/api/v1/transactions",
        json={
            "amount": 16.3,
            "description": "Manzo",
            "repetition": "weekly",
            "category_id": category_id,
        },
    )
    return default_category


def test_get_transaction(client: TestClient, default_category: dict):
    response = client.post(
        "/api/v1/transactions",
        json={
            "amount": 12.3,
            "description": "Pollo",
            "repetition": "weekly",
            "category_id": default_category["id"],
        },
    )
    assert response.status_code == 201
    response = client.get(f"/api/v1/transactions/{default_category['id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["amount"] == "12.3"
    assert body["description"] == "Pollo"
    assert body["repetition"] == "weekly"
    assert body["category_id"] == default_category["id"]


def test_create_transaction(client: TestClient, default_category: dict):
    response = client.post(
        "/api/v1/transactions",
        json={
            "amount": 12.3,
            "description": "Pollo",
            "repetition": "weekly",
            "category_id": default_category["id"],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["amount"] == "12.3"
    assert body["description"] == "Pollo"
    assert body["repetition"] == "weekly"
    assert body["category_id"] == default_category["id"]


def test_get_list_transaction_by_category_id(
    client: TestClient, multiple_transactions_per_category: dict
):
    response = client.get(
        f"/api/v1/transactions/list/{multiple_transactions_per_category['id']}"
    )
    assert response.status_code == 200
    body = response.json()
    assert body is not None
    transactions = body.get("transactions")
    assert transactions is not None
    assert len(transactions) == 3
