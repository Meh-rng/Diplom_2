import allure
from data.urls import ApiEndpoints
from data.ingredients_data import (
    INVALID_INGREDIENT_HASH,
    EMPTY_INGREDIENTS
)
from data.error_messages import ErrorMessages
from helpers.order_helpers import generate_order_body


@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами — успех 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth_success(self, api_client, auth_headers, valid_ingredients_hashes):
        order_body = generate_order_body(valid_ingredients_hashes)
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.ORDERS} с валидными ингредиентами и авторизацией"):
            response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        with allure.step("Проверка кода ответа — 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка структуры ответа — success: true, наличие order и number"):
            assert response.json()["success"] is True
            assert "order" in response.json()
            assert "number" in response.json()["order"]
            assert "name" in response.json()
    
    @allure.title("Создание заказа без авторизации — ожидается ошибка 401")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth_fails(self, api_client, valid_ingredients_hashes):
        order_body = generate_order_body(valid_ingredients_hashes)
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.ORDERS} без токена авторизации"):
            response = api_client.post(ApiEndpoints.ORDERS, json=order_body)
        
        with allure.step("Проверка кода ответа — 401 (Unauthorized)"):
            assert response.status_code == 401
    
    @allure.title("Создание заказа с валидными ингредиентами — успех 200")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_ingredients_success(self, api_client, auth_headers, valid_ingredients_hashes):
        order_body = generate_order_body(valid_ingredients_hashes)
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.ORDERS} с валидными ингредиентами"):
            response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        with allure.step("Проверка кода ответа — 200"):
            assert response.status_code == 200
        
        with allure.step("Проверка поля success — true"):
            assert response.json()["success"] is True
    
    @allure.title("Создание заказа без ингредиентов — ожидается ошибка 400")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients_fails(self, api_client, auth_headers):
        order_body = generate_order_body(EMPTY_INGREDIENTS)
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.ORDERS} с пустым списком ингредиентов"):
            response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        with allure.step("Проверка кода ответа — 400"):
            assert response.status_code == 400
        
        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["success"] is False
            assert response.json()["message"] == ErrorMessages.NO_INGREDIENTS
    
    @allure.title("Создание заказа с неверным хешем ингредиента — ожидается ошибка 500")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_order_with_invalid_ingredient_hash_fails(self, api_client, auth_headers):
        order_body = generate_order_body([INVALID_INGREDIENT_HASH])
        
        with allure.step(f"Отправка POST-запроса на {ApiEndpoints.ORDERS} с невалидным хешем: {INVALID_INGREDIENT_HASH}"):
            response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        with allure.step("Проверка кода ответа — 500 (Internal Server Error)"):
            assert response.status_code == 500