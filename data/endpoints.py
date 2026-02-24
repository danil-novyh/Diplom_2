from config.settings import ApiConfig

class Endpoints:
    """Класс с endpoint'ами API."""
    
    # User endpoints
    USER_REGISTER = f"{ApiConfig.BASE_URL}/auth/register"
    USER_LOGIN = f"{ApiConfig.BASE_URL}/auth/login"
    USER_INFO = f"{ApiConfig.BASE_URL}/auth/user"
    USER_LOGOUT = f"{ApiConfig.BASE_URL}/auth/logout"
    # Order endpoints
    ORDERS = f"{ApiConfig.BASE_URL}/orders"
    # Ingredients
    INGREDIENTS = f"{ApiConfig.BASE_URL}/ingredients"
