import pytest
import requests
import os
import logging

def pytest_configure(config):
    logging.basicConfig(
        filename="tests/test_log.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Получаем результат выполнения теста
    outcome = yield
    rep = outcome.get_result()

    # Только если тест упал
    if rep.when == "call" and rep.failed:
        response = getattr(item, "response_obj", None)
        if response:
            file_path = os.path.join("tests", "response_debug.json")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)



BASE_URL = "http://127.0.0.1:5000"
# Базовый URL API (можно будет расширять, если используешь .env или параметры запуска)
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


# Логин и получение токена
@pytest.fixture(scope="session")
def auth_token(base_url):
    data = {
        "username": "john",
        "password": "1234"
    }
    response = requests.post(f"{base_url}/login", json=data)
    assert response.status_code == 200, f"Логин не удался: {response.text}"
    return response.json()["token"]


# Заголовки с авторизацией
@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
