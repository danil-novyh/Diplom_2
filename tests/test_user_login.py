import allure
from data.response_codes import StatusCode
from data.messages import ErrorMessages
from helpers.user_helpers import UserHelpers


@allure.epic("User Management")
@allure.feature("User Login")
class TestUserLogin:
    """Тесты логина пользователя."""
    
    @allure.title("Успешный логин с корректными данными")
    @allure.description("Проверка, что пользователь может залогиниться с правильными credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_valid_credentials_success(self, api_client, created_user):
        """Тест успешного логина."""
        
        user_payload, _ = created_user
        
        with allure.step("Подготовка данных для логина"):
            login_payload = UserHelpers.prepare_login_payload(
                user_payload["email"],
                user_payload["password"]
            )
        
        with allure.step("Отправка POST запроса на логин"):
            response = api_client.login_user(login_payload)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
        
        with allure.step("Проверка наличия accessToken"):
            assert "accessToken" in response.json()
        
        with allure.step("Проверка наличия refreshToken"):
            assert "refreshToken" in response.json()
        
        with allure.step("Проверка корректности данных пользователя"):
            assert response.json()["user"]["email"] == user_payload["email"]
            assert response.json()["user"]["name"] == user_payload["name"]
    
    @allure.title("Логин с неверным email")
    @allure.description("Проверка, что нельзя залогиниться с неверным email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_invalid_email_fails(self, api_client, created_user):
        """Тест логина с неверным email."""
        
        user_payload, _ = created_user
        
        with allure.step("Подготовка данных с неверным email"):
            invalid_login_payload = {
                "email": "wrong_email@test.com",
                "password": user_payload["password"]
            }
        
        with allure.step("Отправка POST запроса на логин с неверным email"):
            response = api_client.login_user(invalid_login_payload)
        
        with allure.step("Проверка кода ответа 401 Unauthorized"):
            assert response.status_code == StatusCode.UNAUTHORIZED
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.INVALID_CREDENTIALS}'"):
            assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS
    
    @allure.title("Логин с неверным password")
    @allure.description("Проверка, что нельзя залогиниться с неверным password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_invalid_password_fails(self, api_client, created_user):
        """Тест логина с неверным password."""
        
        user_payload, _ = created_user
        
        with allure.step("Подготовка данных с неверным password"):
            invalid_login_payload = {
                "email": user_payload["email"],
                "password": "wrong_password_123"
            }
        
        with allure.step("Отправка POST запроса на логин с неверным password"):
            response = api_client.login_user(invalid_login_payload)
        
        with allure.step("Проверка кода ответа 401 Unauthorized"):
            assert response.status_code == StatusCode.UNAUTHORIZED
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.INVALID_CREDENTIALS}'"):
            assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS
    
    @allure.title("Логин с неверными email и password")
    @allure.description("Проверка, что нельзя залогиниться с полностью неверными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_completely_invalid_credentials_fails(self, api_client, data_generator):
        """Тест логина с полностью неверными данными."""
        
        with allure.step("Генерация полностью неверных credentials"):
            invalid_login_payload = data_generator.generate_invalid_login_data()
        
        with allure.step("Отправка POST запроса на логин"):
            response = api_client.login_user(invalid_login_payload)
        
        with allure.step("Проверка кода ответа 401 Unauthorized"):
            assert response.status_code == StatusCode.UNAUTHORIZED
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.INVALID_CREDENTIALS}'"):
            assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS
