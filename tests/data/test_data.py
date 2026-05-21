"""
Тестовые данные для API тестов Stellar Burgers
"""

# Данные для создания пользователя (невалидные варианты с пропущенными полями)
INCOMPLETE_USER_DATA = [
    ("email", {"password": "pass123", "name": "Test"}),
    ("password", {"email": "test@test.ru", "name": "Test"}),
    ("name", {"email": "test@test.ru", "password": "pass123"}),
]