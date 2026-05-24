import pytest
import allure
from data.urls import BASE_URL
from helpers.api_client import ApiClient 
from helpers.user_helpers import (
    generate_unique_user,
    create_user_via_api,
    delete_user_via_api,
    extract_token_from_response
)


@pytest.fixture
def api_client():
    """Фикстура HTTP-клиента с базовым URL"""
    client = ApiClient(BASE_URL)
    yield client
    client.close() 


@pytest.fixture
def user_builder(api_client):
    """
    Фикстура для создания пользователей с автоматической очисткой.
    Возвращает функцию, которая создаёт пользователя и регистрирует его для удаления.
    """
    created_tokens = []
    
    def _create_user(user_data=None):
        if user_data is None:
            user_data = generate_unique_user()
        
        response = create_user_via_api(api_client, user_data)
        
        if response.status_code == 200:
            token = extract_token_from_response(response)
            created_tokens.append(token)
        
        return response, user_data
    
    yield _create_user
    
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
    with allure.step("Получение списка ингредиентов через GET /api/ingredients"):
        response = api_client.get("/api/ingredients")
        assert response.status_code == 200
        ingredients = response.json()["data"]
        hashes = [ing["_id"] for ing in ingredients[:3]]
        allure.attach(str(hashes), "Используемые хеши ингредиентов", allure.attachment_type.TEXT)
        return hashes