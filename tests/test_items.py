import requests
import logging

def test_get_items(base_url):
    response = requests.get(f"{base_url}/items")
    logging.info(f"GET /items - status: {response.status_code}, body: {response.text}")
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)
    assert len(body) >= 1

    for item in body:
        assert "id" in item
        assert "name" in item
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)

def test_add_item(base_url):
    payload = {"name": "New Item"}
    response = requests.post(f"{base_url}/items", json=payload)
    logging.info(f"POST /items - status: {response.status_code}, body: {response.text}")

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["name"] == "New Item"

def test_update_item(base_url):
    updated_data = {"name": "Updated Item"}
    response = requests.put(f"{base_url}/items/1", json=updated_data)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"

def test_delete_item(base_url):
    response = requests.delete(f"{base_url}/items/1")

    assert response.status_code == 200
    assert response.json()["result"] == "deleted"
