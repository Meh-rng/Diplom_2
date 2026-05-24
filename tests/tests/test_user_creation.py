import pytest
import allure
from data.urls import ApiEndpoints
from data.error_messages import ErrorMessages
from data.test_data import INCOMPLETE_USER_DATA
from helpers.user_helpers import generate_unique_user


@allure.feature("Создание пользователя")
class TestUserCreation:
    
    @allure.title("Создание уникального пользователя — успех 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user_success(self, user_builder):
        user_data = generate_unique_user()
        
        with allure.step(f"Создание пользователя с email: {user_data['email']}"):
            response, created_user = user_builder(user_data)
        
        with allure.step("Проверка кода ответа — 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка структуры ответа — success: true, наличие accessToken и user"):
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
            assert "user" in response.json()
        
        with allure.step(f"Проверка email пользователя — {user_data['email']}"):
            assert response.json()["user"]["email"] == user_data["email"]
        
        with allure.step(f"Проверка имени пользователя — {user_data['name']}"):
            assert response.json()["user"]["name"] == user_data["name"]
    
    @allure.title("Создание пользователя, который уже зарегистрирован — ожидается ошибка 403")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_already_exists_fails(self, test_user, api_client):
        existing_user = {
            "email": test_user["email"],
            "password": test_user["password"],
            "name": test_user["name"]
        }
        
        with allure.step(f"Попытка создания пользователя с уже существующим email: {test_user['email']}"):
            response = api_client.post(ApiEndpoints.REGISTER, json=existing_user)
        
        with allure.step("Проверка кода ответа — 403"):
            assert response.status_code == 403
        
        with allure.step("Проверка сообщения об ошибке — User already exists"):
            assert response.json()["success"] is False
            assert response.json()["message"] == ErrorMessages.USER_EXISTS
    
    @allure.title("Создание пользователя без одного из обязательных полей — ожидается ошибка 403")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field,user_partial", INCOMPLETE_USER_DATA)
    def test_create_user_missing_required_field_fails(self, api_client, missing_field, user_partial):
        with allure.step(f"Попытка создания пользователя без обязательного поля: {missing_field}"):
            response = api_client.post(ApiEndpoints.REGISTER, json=user_partial)
        
        with allure.step("Проверка кода ответа — 403"):
            assert response.status_code == 403
        
        with allure.step("Проверка сообщения об ошибке — Email, password and name are required fields"):
            assert response.json()["success"] is False
            assert response.json()["message"] == ErrorMessages.REQUIRED_FIELDS
            assert missing_field not in user_partial