import pytest
import allure
from helpers.api_client import APIClient
from helpers.data_generator import DataGenerator


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture(scope="function")
def data_generator():
    """Фикстура для генератора тестовых данных."""
    return DataGenerator()


@pytest.fixture(scope="function")
def user_payload(data_generator):
    """
    Фикстура для генерации данных пользователя.
    
    Возвращает динамически сгенерированные данные для нового пользователя.
    """
    return data_generator.generate_user_data()


@pytest.fixture(scope="function")
def created_user(api_client, user_payload):
    """
    Фикстура для создания пользователя с автоматическим удалением.
    
    Создает пользователя, возвращает данные и токен,
    после завершения теста удаляет пользователя.
    
    Yields:
        tuple: (user_payload, access_token)
    """
    with allure.step("Setup: Создание тестового пользователя"):
        response = api_client.create_user(user_payload)
        access_token = response.json().get("accessToken")
    
    # Передаем данные в тест
    yield user_payload, access_token
    
    # Teardown: удаление пользователя
    with allure.step("Teardown: Удаление тестового пользователя"):
        if access_token:
            api_client.delete_user(access_token)


@pytest.fixture(scope="function")
def created_user_with_login(api_client, user_payload):
    """
    Фикстура для создания и логина пользователя.
    
    Создает пользователя, выполняет логин, возвращает данные и токен,
    после завершения теста удаляет пользователя.
    
    Yields:
        tuple: (user_payload, access_token)
    """
    with allure.step("Setup: Создание и логин тестового пользователя"):
        # Создание пользователя
        create_response = api_client.create_user(user_payload)
        
        # Логин для получения свежего токена
        login_payload = {
            "email": user_payload["email"],
            "password": user_payload["password"]
        }
        login_response = api_client.login_user(login_payload)
        access_token = login_response.json().get("accessToken")
    
    yield user_payload, access_token
    
    with allure.step("Teardown: Удаление тестового пользователя"):
        if access_token:
            api_client.delete_user(access_token)


@pytest.fixture(scope="session")
def ingredient_ids(api_client):
    """
    Фикстура для получения ID ингредиентов.
    
    Scope="session" - получаем список один раз для всех тестов.
    
    Returns:
        list: Список ID ингредиентов
    """
    with allure.step("Получение списка доступных ингредиентов из API"):
        response = api_client.get_ingredients()
        ingredients = response.json()["data"]
        ids = [ingredient["_id"] for ingredient in ingredients]
    
    return ids


@pytest.fixture(scope="function")
def valid_order_ingredients(ingredient_ids):
    """
    Фикстура для получения валидных ингредиентов для заказа.
    
    Returns:
        list: Список из 2-3 валидных ID ингредиентов
    """
    # Берем первые 3 ингредиента
    return ingredient_ids[:3]


@pytest.fixture(scope="function")
def invalid_order_ingredients():
    """
    Фикстура для невалидных ID ингредиентов.
    
    Returns:
        list: Список невалидных ID
    """
    return ["invalid_hash_123", "wrong_id_456"]