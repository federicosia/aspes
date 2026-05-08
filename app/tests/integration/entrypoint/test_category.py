def test_get_category(test_client):
    response = test_client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    category_id = response.json()["id"]
    response = test_client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    body = response.json()
    assert body is not None
    assert body["name"] == "Food"
    assert body["description"] == "Cash used for food"


def test_create_category(test_client):
    response = test_client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body is not None
    assert body["name"] == "Food"
    assert body["description"] == "Cash used for food"


def test_delete_category(test_client):
    response = test_client.post(
        "/api/v1/categories", json={"name": "Food", "description": "Cash used for food"}
    )
    assert response.status_code == 201
    category_id = response.json()["id"]
    response = test_client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 204
