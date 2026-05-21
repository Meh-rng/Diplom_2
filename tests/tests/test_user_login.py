from data.urls import ApiEndpoints
from data.error_messages import ErrorMessages


class TestUserLogin:
    
    def test_login_existing_user_success(self, api_client, test_user):
        """Вход под существующим пользователем — 200"""
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = api_client.post(ApiEndpoints.LOGIN, json=login_data)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()
        assert response.json()["user"]["email"] == test_user["email"]
        assert response.json()["user"]["name"] == test_user["name"]
    
    def test_login_invalid_credentials_fails(self, api_client):
        """Вход с неверным логином и паролем — 401"""
        login_data = {
            "email": "nonexistent@test.ru",
            "password": "wrongpassword"
        }
        response = api_client.post(ApiEndpoints.LOGIN, json=login_data)
        
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS
    
        