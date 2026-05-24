"""
HTTP-клиент для взаимодействия с API Stellar Burgers
"""

import requests


class ApiClient:
    """HTTP-клиент с базовым URL для API Stellar Burgers"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def post(self, endpoint: str, **kwargs):
        """Отправка POST-запроса"""
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

    def get(self, endpoint: str, **kwargs):
        """Отправка GET-запроса"""
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """Отправка DELETE-запроса"""
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    def patch(self, endpoint: str, **kwargs):
        """Отправка PATCH-запроса (если понадобится)"""
        return self.session.patch(f"{self.base_url}{endpoint}", **kwargs)

    def put(self, endpoint: str, **kwargs):
        """Отправка PUT-запроса (если понадобится)"""
        return self.session.put(f"{self.base_url}{endpoint}", **kwargs)

    def close(self):
        """Закрытие сессии"""
        self.session.close()