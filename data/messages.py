class ErrorMessages:
    """Сообщения об ошибках API."""
    
    # User creation errors
    USER_ALREADY_EXISTS = "User already exists"
    MISSING_REQUIRED_FIELDS = "Email, password and name are required fields"
    
    # Login errors
    INVALID_CREDENTIALS = "email or password are incorrect"
    
    # Authorization errors
    UNAUTHORIZED = "You should be authorised"
    
    # Order errors
    NO_INGREDIENTS = "Ingredient ids must be provided"
    INVALID_INGREDIENT_IDS = "One or more ids provided are incorrect"


class SuccessMessages:
    """Сообщения об успешных операциях."""
    
    USER_CREATED = "User created successfully"
    ORDER_CREATED = "Order created successfully"
