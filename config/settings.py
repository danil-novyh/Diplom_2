class ApiConfig:
    """Настройки подключения к API."""
    BASE_URL = "https://stellarburgers.education-services.ru/api"
    REQUEST_TIMEOUT = 10


class GeneratorConfig:
    """Настройки генерации тестовых данных."""
    FAKER_LOCALE = "ru_RU"
    DEFAULT_STRING_LENGTH = 10