import pytest


@pytest.fixture
def default_category(test_client):
    response = test_client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def multiple_transactions_per_category(test_client, default_category: dict):
    category_id = default_category["id"]
    test_client.post(
        "/api/v1/transactions",
        json={
            "amount": 12.30,
            "description": "Pollo",
            "repetition": "weekly",
            "category_id": category_id,
        },
    )
    test_client.post(
        "/api/v1/transactions",
        json={
            "amount": 4.30,
            "description": "Curry",
            "repetition": "weekly",
            "category_id": category_id,
        },
    )
    test_client.post(
        "/api/v1/transactions",
        json={
            "amount": 16.30,
            "description": "Manzo",
            "repetition": "weekly",
            "category_id": category_id,
        },
    )
    return default_category


def test_get_transaction(test_client, default_category: dict):
    response = test_client.post(
        "/api/v1/transactions",
        json={
            "amount": 12.30,
            "description": "Pollo",
            "repetition": "weekly",
            "category_id": default_category["id"],
        },
    )
    assert response.status_code == 201
    transaction_id = response.json()["id"]
    response = test_client.get(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["amount"] == "12.30"
    assert body["description"] == "Pollo"
    assert body["repetition"] == "weekly"
    assert body["category_id"] == default_category["id"]


def test_create_transaction(test_client, default_category: dict):
    response = test_client.post(
        "/api/v1/transactions",
        json={
            "amount": 12.30,
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
    test_client, multiple_transactions_per_category: dict
):
    response = test_client.get(
        f"/api/v1/transactions/list/{multiple_transactions_per_category['id']}"
    )
    assert response.status_code == 200
    body = response.json()
    assert body is not None
    transactions = body.get("transactions")
    assert transactions is not None
    assert len(transactions) == 3
