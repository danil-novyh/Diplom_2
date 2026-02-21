from config.settings import Config

class Endpoints:
    """Класс с endpoint'ами API."""
    
    # User endpoints
    USER_REGISTER = f"{Config.BASE_URL}/auth/register"
    USER_LOGIN = f"{Config.BASE_URL}/auth/login"
    USER_INFO = f"{Config.BASE_URL}/auth/user"
    USER_LOGOUT = f"{Config.BASE_URL}/auth/logout"
    # Order endpoints
    ORDERS = f"{Config.BASE_URL}/orders"
    # Ingredients
    INGREDIENTS = f"{Config.BASE_URL}/ingredients"
