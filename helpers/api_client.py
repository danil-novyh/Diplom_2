import allure
import requests
from data.endpoints import Endpoints
from config.settings import ApiConfig


class APIClient:
    """Клиент для работы с API."""
    
    def __init__(self):
        self.timeout = ApiConfig.REQUEST_TIMEOUT
    
    @allure.step("POST запрос на регистрацию пользователя")
    def create_user(self, payload):
        """
        Создание нового пользователя.
        
        Args:
            payload: Данные пользователя
            
        Returns:
            Response object
        """
        response = requests.post(
            Endpoints.USER_REGISTER,
            json=payload,
            timeout=self.timeout
        )
        return response
    
    @allure.step("POST запрос на логин пользователя")
    def login_user(self, payload):
        """
        Авторизация пользователя.
        
        Args:
            payload: Email и password
            
        Returns:
            Response object
        """
        response = requests.post(
            Endpoints.USER_LOGIN,
            json=payload,
            timeout=self.timeout
        )
        return response
    
    @allure.step("DELETE запрос на удаление пользователя")
    def delete_user(self, access_token):
        """
        Удаление пользователя.
        
        Args:
            access_token: Токен авторизации
            
        Returns:
            Response object
        """
        headers = {"Authorization": access_token}
        response = requests.delete(
            Endpoints.USER_INFO,
            headers=headers,
            timeout=self.timeout
        )
        return response
    
    @allure.step("GET запрос на получение списка ингредиентов")
    def get_ingredients(self):
        """
        Получение списка доступных ингредиентов.
        
        Returns:
            Response object
        """
        response = requests.get(
            Endpoints.INGREDIENTS,
            timeout=self.timeout
        )
        return response
    
    @allure.step("POST запрос на создание заказа")
    def create_order(self, ingredients, access_token=None):
        """
        Создание заказа.
        
        Args:
            ingredients: Список ID ингредиентов
            access_token: Токен авторизации (опционально)
            
        Returns:
            Response object
        """
        payload = {"ingredients": ingredients}
        headers = {}
        
        if access_token:
            headers["Authorization"] = access_token
        
        response = requests.post(
            Endpoints.ORDERS,
            json=payload,
            headers=headers,
            timeout=self.timeout
        )
        return response
    
    @allure.step("GET запрос на получение заказов пользователя")
    def get_user_orders(self, access_token):
        """
        Получение заказов пользователя.
        
        Args:
            access_token: Токен авторизации
            
        Returns:
            Response object
        """
        headers = {"Authorization": access_token}
        response = requests.get(
            Endpoints.ORDERS,
            headers=headers,
            timeout=self.timeout
        )
        return response
    