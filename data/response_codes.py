class StatusCode:
    """HTTP статус-коды."""
    
    # Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    
    # Client errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    
    # Server errors
    INTERNAL_SERVER_ERROR = 500
