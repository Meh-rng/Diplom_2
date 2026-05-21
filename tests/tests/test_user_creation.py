import pytest
from data.urls import ApiEndpoints
from data.error_messages import ErrorMessages
from data.test_data import INCOMPLETE_USER_DATA
from helpers.user_helpers import generate_unique_user


class TestUserCreation:
    
    def test_create_unique_user_success(self, user_builder):
        """
        Создание уникального пользователя — успех 200
        Фикстура user_builder автоматически удалит пользователя после теста
        """
        user_data = generate_unique_user()
        response, created_user = user_builder(user_data)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "user" in response.json()
        assert response.json()["user"]["email"] == user_data["email"]
        assert response.json()["user"]["name"] == user_data["name"]
    
    def test_create_user_already_exists_fails(self, test_user, api_client):
        """
        Создание пользователя, который уже зарегистрирован — 403
        test_user уже создан фикстурой, используем его данные
        """
        existing_user = {
            "email": test_user["email"],
            "password": test_user["password"],
            "name": test_user["name"]
        }
        response = api_client.post(ApiEndpoints.REGISTER, json=existing_user)
        
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.USER_EXISTS
    
    @pytest.mark.parametrize("missing_field,user_partial", INCOMPLETE_USER_DATA)
    def test_create_user_missing_required_field_fails(self, api_client, missing_field, user_partial):
        """
        Создание пользователя без одного обязательного поля — 403
        Негативный тест — пользователь не создаётся, удаление не требуется
        """
        response = api_client.post(ApiEndpoints.REGISTER, json=user_partial)
        
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.REQUIRED_FIELDS
        assert missing_field not in user_partial