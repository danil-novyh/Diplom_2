import allure
import pytest
from data.response_codes import StatusCode
from data.messages import ErrorMessages


@allure.epic("User Management")
@allure.feature("User Creation")
class TestUserCreation:
    """Тесты создания пользователя."""
    
    @allure.title("Успешное создание уникального пользователя")
    @allure.description("Проверка, что уникальный пользователь успешно создается с кодом 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user_success(self, api_client, user_payload):
        """Тест создания уникального пользователя."""
        
        with allure.step("Отправка POST запроса на создание пользователя"):
            response = api_client.create_user(user_payload)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
        
        with allure.step("Проверка наличия accessToken в ответе"):
            assert "accessToken" in response.json()
        
        with allure.step("Проверка наличия refreshToken в ответе"):
            assert "refreshToken" in response.json()
        
        with allure.step("Проверка корректности email в ответе"):
            assert response.json()["user"]["email"] == user_payload["email"]
        
        with allure.step("Проверка корректности name в ответе"):
            assert response.json()["user"]["name"] == user_payload["name"]
        
        # Удаляем созданного пользователя
        with allure.step("Очистка: удаление созданного пользователя"):
            access_token = response.json()["accessToken"]
            delete_response = api_client.delete_user(access_token)
            assert delete_response.status_code == StatusCode.ACCEPTED
    
    @allure.title("Создание пользователя с существующим email")
    @allure.description("Проверка, что нельзя создать пользователя с уже существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_duplicate_user_fails(self, api_client, created_user):
        """Тест попытки создания дубликата пользователя."""
        
        user_payload, _ = created_user
        
        with allure.step("Отправка POST запроса на создание пользователя с существующим email"):
            response = api_client.create_user(user_payload)
        
        with allure.step("Проверка кода ответа 403 Forbidden"):
            assert response.status_code == StatusCode.FORBIDDEN
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.USER_ALREADY_EXISTS}'"):
            assert response.json()["message"] == ErrorMessages.USER_ALREADY_EXISTS
    
    @allure.title("Создание пользователя без email")
    @allure.description("Проверка, что нельзя создать пользователя без обязательного поля email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_without_email_fails(self, api_client, data_generator):
        """Тест создания пользователя без email."""
        
        with allure.step("Генерация данных пользователя без email"):
            user_payload = data_generator.generate_user_data(
                include_email=False,
                include_password=True,
                include_name=True
            )
        
        with allure.step("Отправка POST запроса на создание пользователя без email"):
            response = api_client.create_user(user_payload)
        
        with allure.step("Проверка кода ответа 403 Forbidden"):
            assert response.status_code == StatusCode.FORBIDDEN
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.MISSING_REQUIRED_FIELDS}'"):
            assert response.json()["message"] == ErrorMessages.MISSING_REQUIRED_FIELDS
    
    @allure.title("Создание пользователя без password")
    @allure.description("Проверка, что нельзя создать пользователя без обязательного поля password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_without_password_fails(self, api_client, data_generator):
        """Тест создания пользователя без password."""
        
        with allure.step("Генерация данных пользователя без password"):
            user_payload = data_generator.generate_user_data(
                include_email=True,
                include_password=False,
                include_name=True
            )
        
        with allure.step("Отправка POST запроса на создание пользователя без password"):
            response = api_client.create_user(user_payload)
        
        with allure.step("Проверка кода ответа 403 Forbidden"):
            assert response.status_code == StatusCode.FORBIDDEN
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.MISSING_REQUIRED_FIELDS}'"):
            assert response.json()["message"] == ErrorMessages.MISSING_REQUIRED_FIELDS
    
    @allure.title("Создание пользователя без name")
    @allure.description("Проверка, что нельзя создать пользователя без обязательного поля name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_without_name_fails(self, api_client, data_generator):
        """Тест создания пользователя без name."""
        
        with allure.step("Генерация данных пользователя без name"):
            user_payload = data_generator.generate_user_data(
                include_email=True,
                include_password=True,
                include_name=False
            )
        
        with allure.step("Отправка POST запроса на создание пользователя без name"):
            response = api_client.create_user(user_payload)
        
        with allure.step("Проверка кода ответа 403 Forbidden"):
            assert response.status_code == StatusCode.FORBIDDEN
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.MISSING_REQUIRED_FIELDS}'"):
            assert response.json()["message"] == ErrorMessages.MISSING_REQUIRED_FIELDS
