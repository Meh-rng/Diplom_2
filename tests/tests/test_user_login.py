import allure
from data.urls import ApiEndpoints
from data.error_messages import ErrorMessages


@allure.feature("Авторизация пользователя")
class TestUserLogin:
    
    @allure.title("Вход под существующим пользователем — успех 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user_success(self, api_client, test_user):
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.LOGIN} с данными пользователя: {test_user['email']}"):
            response = api_client.post(ApiEndpoints.LOGIN, json=login_data)
        
        with allure.step("Проверка кода ответа — 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка структуры ответа — success: true, наличие accessToken и refreshToken"):
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()
        
        with allure.step(f"Проверка email пользователя — {test_user['email']}"):
            assert response.json()["user"]["email"] == test_user["email"]
        
        with allure.step(f"Проверка имени пользователя — {test_user['name']}"):
            assert response.json()["user"]["name"] == test_user["name"]
    
    @allure.title("Вход с неверными учётными данными — ожидается ошибка 401")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_credentials_fails(self, api_client):
        login_data = {
            "email": "nonexistent@test.ru",
            "password": "wrongpassword"
        }
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.LOGIN} с неверными данными"):
            response = api_client.post(ApiEndpoints.LOGIN, json=login_data)
        
        with allure.step("Проверка кода ответа — 401"):
            assert response.status_code == 401
        
        with allure.step("Проверка сообщения об ошибке — email or password are incorrect"):
            assert response.json()["success"] is False
            assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS