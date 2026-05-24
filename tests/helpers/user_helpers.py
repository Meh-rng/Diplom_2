import random
import string

def generate_unique_user():
    """Генерирует уникального пользователя с случайными email, password, name"""
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return {
        "email": f"{random_part}@testburger.ru",
        "password": random_part,
        "name": f"User_{random_part[:5]}"
    }

def create_user_via_api(client, user_data):
    """Создаёт пользователя через API и возвращает ответ"""
    return client.post("/api/auth/register", json=user_data)

def delete_user_via_api(client, access_token):
    """Удаляет пользователя через API (нужен токен без 'Bearer ')"""
    headers = {"Authorization": f"Bearer {access_token}"}
    return client.delete("/api/auth/user", headers=headers)

def extract_token_from_response(response):
    """Извлекает accessToken из ответа и убирает префикс 'Bearer '"""
    json_data = response.json()
    token = json_data.get("accessToken", "")
    if token.startswith("Bearer "):
        return token[7:]  # убираем "Bearer "
    return token
