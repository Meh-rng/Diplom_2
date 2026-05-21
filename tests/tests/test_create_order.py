from data.urls import ApiEndpoints
from data.ingredients_data import (
    INVALID_INGREDIENT_HASH,
    EMPTY_INGREDIENTS
)
from data.error_messages import ErrorMessages
from helpers.order_helpers import generate_order_body


class TestCreateOrder:
    
    def test_create_order_with_auth_success(self, api_client, auth_headers, valid_ingredients_hashes):
        """Создание заказа с авторизацией и валидными ингредиентами — 200"""
        order_body = generate_order_body(valid_ingredients_hashes)
        response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()
        assert "number" in response.json()["order"]
        assert "name" in response.json()
    
    def test_create_order_without_auth_fails(self, api_client, valid_ingredients_hashes):
        """Создание заказа без авторизации — 200 """
        order_body = generate_order_body(valid_ingredients_hashes)
        response = api_client.post(ApiEndpoints.ORDERS, json=order_body)
        
        assert response.status_code == 200
    
    def test_create_order_with_ingredients_success(self, api_client, auth_headers, valid_ingredients_hashes):
        """Создание заказа с ингредиентами — 200"""
        order_body = generate_order_body(valid_ingredients_hashes)
        response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_create_order_without_ingredients_fails(self, api_client, auth_headers):
        """Создание заказа без ингредиентов — 400"""
        order_body = generate_order_body(EMPTY_INGREDIENTS)
        response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.NO_INGREDIENTS
    
    def test_create_order_with_invalid_ingredient_hash_fails(self, api_client, auth_headers):
        """Создание заказа с неверным хешем ингредиента — 500"""
        order_body = generate_order_body([INVALID_INGREDIENT_HASH])
        response = api_client.post(ApiEndpoints.ORDERS, json=order_body, headers=auth_headers)
        
        assert response.status_code == 500