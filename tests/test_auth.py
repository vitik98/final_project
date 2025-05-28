import requests
import pytest
import logging

def test_login_success(base_url):
    data = {"username": "john", "password": "1234"}
    response = requests.post(f"{base_url}/login", json=data)
    logging.info(f"POST /status: {response.status_code}, body: {response.text}")
    body = response.json()

    assert response.status_code == 200
    assert "token" in body
    assert body["token"] == "token-john"

def test_login_fail(base_url):
    data = {"username": "john", "password": "WRONG"}
    response = requests.post(f"{base_url}/login", json=data)
    logging.info(f"POST /status: {response.status_code}, body: {response.text}")

    assert response.status_code == 401
    assert "error" in response.json()
