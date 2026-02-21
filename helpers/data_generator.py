import allure
from faker import Faker
from config.settings import Config


class DataGenerator:
    """Класс для генерации тестовых данных."""
    
    def __init__(self):
        self.faker = Faker(Config.FAKER_LOCALE)
    
    @allure.step("Генерация данных для нового пользователя")
    def generate_user_data(self, include_email=True, include_password=True, include_name=True):
        """
        Генерирует данные для создания пользователя.
        
        Args:
            include_email: Включить email в payload
            include_password: Включить password в payload
            include_name: Включить name в payload
            
        Returns:
            dict: Словарь с данными пользователя
        """
        user_data = {}
        
        if include_email:
            user_data["email"] = self.faker.email()
        
        if include_password:
            user_data["password"] = self.faker.password(length=12)
        
        if include_name:
            user_data["name"] = self.faker.first_name()
        
        return user_data
    
    @allure.step("Генерация данных для логина")
    def generate_login_data(self, email, password):
        """
        Генерирует payload для логина.
        
        Args:
            email: Email пользователя
            password: Пароль пользователя
            
        Returns:
            dict: Данные для логина
        """
        return {
            "email": email,
            "password": password
        }
    
    @allure.step("Генерация невалидных credentials")
    def generate_invalid_login_data(self):
        """Генерирует заведомо неверные данные для логина."""
        return {
            "email": f"invalid_{self.faker.email()}",
            "password": "wrong_password_123"
        }
