import pytest
import allure
from helpers.api_client import APIClient
from helpers.data_generator import DataGenerator
from helpers.user_helpers import UserHelpers


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture(scope="function")
def data_generator():
    """Фикстура для генератора тестовых данных."""
    return DataGenerator()


@pytest.fixture(scope="function")
def created_user(api_client, data_generator):
    """
    Фикстура для создания пользователя с автоматическим удалением.
    
    Создает пользователя, возвращает данные и токен,
    после завершения теста удаляет пользователя.
    
    Yields:
        tuple: (user_payload, access_token)
    """
    access_token = None
    user_payload = UserHelpers.prepare_user_payload(data_generator)
    with allure.step("Setup: Создание тестового пользователя"):
        response = api_client.create_user(user_payload)
        access_token = response.json().get("accessToken")
    
    # Передаем данные в тест
    yield user_payload, access_token
    
    # Teardown: удаление пользователя
    with allure.step("Teardown: Удаление тестового пользователя"):
        UserHelpers.cleanup_user(api_client, access_token)


@pytest.fixture(scope="function")
def created_user_with_login(api_client, data_generator):
    """
    Фикстура для создания и логина пользователя.
    
    Создает пользователя, выполняет логин, возвращает данные и токен,
    после завершения теста удаляет пользователя.
    
    Yields:
        tuple: (user_payload, access_token)
    """
    access_token = None
    user_payload = UserHelpers.prepare_user_payload(data_generator)
    with allure.step("Setup: Создание и логин тестового пользователя"):
        # Создание пользователя
        api_client.create_user(user_payload)
        
        # Логин для получения свежего токена
        login_payload = UserHelpers.prepare_login_payload(
            user_payload["email"],
            user_payload["password"]
        )
        login_response = api_client.login_user(login_payload)
        access_token = login_response.json().get("accessToken")
    
    yield user_payload, access_token
    
    with allure.step("Teardown: Удаление тестового пользователя"):
        UserHelpers.cleanup_user(api_client, access_token)


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
def cleanup_user_token(api_client):
    """ 
    Фикстура для очистки пользователя по токену.
    
    Используется в тестах, где регистрация — ЧАСТЬ ТЕСТА
    (например, test_create_unique_user_success).
    
    Тест сам создаёт пользователя и передаёт токен в эту фикстуру.
    Фикстура гарантирует очистку в teardown.
    
    Yields: 
        function: Функция для регистрации токена на очистку
    """ 
    tokens_to_cleanup = []
    
    def register_token(token):
        """Регистрирует токен для последующей очистки."""
        if token:
            tokens_to_cleanup.append(token)
        
    yield register_token
    
    # Teardown: очистка всех зарегистрированных токенов
    for token in tokens_to_cleanup:
        with allure.step("Teardown: Удаление пользователя по токену"):
            UserHelpers.cleanup_user(api_client, token)
                    