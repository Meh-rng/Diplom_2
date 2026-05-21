import pytest
import requests
from data.urls import BASE_URL
from helpers.user_helpers import (
    generate_unique_user,
    create_user_via_api,
    delete_user_via_api,
    extract_token_from_response
)


@pytest.fixture
def api_client():
    """Фикстура HTTP-клиента с базовым URL"""
    class ApiClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.session = requests.Session()

        def post(self, endpoint, **kwargs):
            return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

        def get(self, endpoint, **kwargs):
            return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

        def delete(self, endpoint, **kwargs):
            return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    return ApiClient(BASE_URL)


@pytest.fixture
def user_builder(api_client):
    """
    Фикстура для создания пользователей с автоматической очисткой.
    Возвращает функцию, которая создаёт пользователя и регистрирует его для удаления.
    """
    created_tokens = []  # список токенов созданных пользователей
    
    def _create_user(user_data=None):
        """Создаёт пользователя. Если user_data не передан, генерирует уникального."""
        if user_data is None:
            user_data = generate_unique_user()
        
        response = create_user_via_api(api_client, user_data)
        
        # Если пользователь успешно создан, сохраняем токен для удаления
        if response.status_code == 200:
            token = extract_token_from_response(response)
            created_tokens.append(token)
        
        return response, user_data
    
    yield _create_user
    
    # TEARDOWN: удаляем всех созданных пользователей
    for token in created_tokens:
        delete_user_via_api(api_client, token)


@pytest.fixture
def test_user(api_client, user_builder):
    """
    Фикстура создаёт пользователя перед тестом и удаляет после теста.
    Возвращает словарь с данными пользователя и токеном.
    """
    response, user_data = user_builder()
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    
    token = extract_token_from_response(response)
    
    user_info = {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "access_token": token
    }
    
    return user_info


@pytest.fixture
def auth_headers(test_user):
    """Фикстура возвращает заголовки для авторизованных запросов"""
    return {"Authorization": f"Bearer {test_user['access_token']}"}


@pytest.fixture
def valid_ingredients_hashes(api_client):
    """
    Фикстура получает реальные хеши ингредиентов из API (динамически)
    """
    response = api_client.get("/api/ingredients")
    assert response.status_code == 200
    ingredients = response.json()["data"]
    # Берём первые 3 разных типа ингредиентов
    hashes = [ing["_id"] for ing in ingredients[:3]]
    return hashes
