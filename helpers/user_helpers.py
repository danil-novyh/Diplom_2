import allure
from helpers.data_generator import DataGenerator
from data.response_codes import StatusCode


class UserHelpers:
    """Вспомогательные методы для работы с пользователями."""
    
    @staticmethod
    @allure.step("Подготовка данных для нового пользователя")
    def prepare_user_payload(data_generator: DataGenerator) -> dict:
        """
        Возвращает данные для регистрации нового пользователя.
        Args:
            data_generator: Экземпляр DataGenerator
        Returns:
            dict: Словарь с данными пользователя (email, password, name)
        """
        return data_generator.generate_user_data()
    
    @staticmethod
    @allure.step("Подготовка данных пользователя без email")
    def prepare_user_payload_without_email(data_generator: DataGenerator) -> dict:
        """Возвращает данные пользователя без поля email."""
        return data_generator.generate_user_data(
            include_email=False,
            include_password=True,
            include_name=True
        )
    
    @staticmethod
    @allure.step("Подготовка данных пользователя без password")
    def prepare_user_payload_without_password(data_generator: DataGenerator) -> dict:
        """Возвращает данные пользователя без поля password."""
        return data_generator.generate_user_data(
            include_email=True,
            include_password=False,
            include_name=True
        )
    
    @staticmethod
    @allure.step("Подготовка данных пользователя без name")
    def prepare_user_payload_without_name(data_generator: DataGenerator) -> dict:
        """Возвращает данные пользователя без поля name."""
        return data_generator.generate_user_data(
            include_email=True,
            include_password=True,
            include_name=False
        )
    
    @staticmethod
    @allure.step("Подготовка данных для логина")
    def prepare_login_payload(email: str, password: str) -> dict:
        """
        Возвращает payload для логина.
        Args:
            email: Email пользователя
            password: Пароль пользователя
        Returns:
            dict: Словарь с credentials
        """
        return {
            "email": email,
            "password": password
        }
    
    @staticmethod
    @allure.step("Очистка: удаление пользователя по токену")
    def cleanup_user(api_client, access_token: str) -> None:
        """
        Безопасное удаление пользователя.
        Args:
            api_client: Экземпляр APIClient
            access_token: Токен авторизации
        """
        if access_token:
            try:
                api_client.delete_user(access_token)
            except Exception as e:
                allure.attach(
                    f"Warning: failed to cleanup user: {str(e)}",
                    name="Cleanup Warning",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    @staticmethod
    @allure.step("Попытка безопасной очистки после негативного теста регистрации")
    def cleanup_after_failed_registration(api_client, user_payload: dict) -> None:
        """
        Пытается удалить пользователя, если он был создан по ошибке.
        Безопасно: не падает, если пользователь не существует.
        Args:
            api_client: Экземпляр APIClient
            user_payload: Данные пользователя (для попытки логина)
        """
        email = user_payload.get("email")
        password = user_payload.get("password")
        
        if not email or not password:
            return  # Невозможно залогиниться для удаления
        
        try:
            login_resp = api_client.login_user({"email": email, "password": password})
            if login_resp.status_code == StatusCode.OK:
                token = login_resp.json().get("accessToken")
                if token:
                    api_client.delete_user(token)
                    allure.attach(
                        "Cleanup: user removed after negative test",
                        name="Post-condition Cleanup",
                        attachment_type=allure.attachment_type.TEXT
                    )
        except Exception:
            pass