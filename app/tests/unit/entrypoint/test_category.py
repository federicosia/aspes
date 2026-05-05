from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_category(client: TestClient):
    response = client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    response = client.get("/api/v1/categories/1")
    assert response.status_code == 200
    body = response.json()
    assert body is not None
    assert body["name"] == "Food"
    assert body["description"] == "Cash used for food"
    assert body["id"] == 1
