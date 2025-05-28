import requests
import pytest
from jsonschema import validate
import logging


def test_profile_success(auth_token, base_url, auth_headers):
    response = requests.get(f"{base_url}/profile", headers=auth_headers)
    logging.info(f"GET /profile - status: {response.status_code}, body: {response.text}")
    body = response.json()

    assert response.status_code == 200
    assert body["name"] == "John Doe"
    assert "email" in body
    assert isinstance(body["name"], str)
    assert isinstance(body["email"], str)


def test_profile_unauthorized(base_url):
    headers = {"Authorization": "Bearer invalid-token"}
    response = requests.get(f"{base_url}/profile", headers=headers)
    logging.info(f"GET /profile - status: {response.status_code}, body: {response.text}")

    assert response.status_code == 401
    assert "error" in response.json()


# def test_profile_schema(base_url, auth_headers):
#     response = requests.get(f"{base_url}/profile", headers=auth_headers)
#     logging.info(f"GET /profile - status: {response.status_code}, body: {response.text}")
#     body = response.json()
#     schema = {
#         "type": "object",
#         "properties": {
#             "name": {"type": "string"},
#             "email": {"type": "string", "format": "email"}
#         },
#         "required": ["username", "email"]
#     }
#     validate(instance=body, schema=schema)


# def test_profile_update(auth_token, auth_headers, base_url):
#     new_email = "updated@example.com"
#     data = {"email": new_email}
#
#     response = requests.post(f"{base_url}/profile/update", json=data, headers=auth_headers)
#     body = response.json()
#
#     assert response.status_code == 200, f"Статус код должен быть 200, но получили {response.status_code}"
#     assert body["email"] == new_email