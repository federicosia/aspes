from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_category(client: TestClient):
    response = client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    category_id = response.json()["id"]
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    body = response.json()
    assert body is not None
    assert body["name"] == "Food"
    assert body["description"] == "Cash used for food"
    assert body["id"] == 1


def test_create_category(client: TestClient):
    response = client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body is not None
    assert body["name"] == "Food"
    assert body["description"] == "Cash used for food"
    assert body["id"] == 1


def test_delete_category(client: TestClient):
    response = client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    category_id = response.json()["id"]
    response = client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 204
