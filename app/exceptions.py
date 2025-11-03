"""Custom exception classes for the application"""

class AppException(Exception):
    """Base exception for application errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DatabaseException(AppException):
    """Exception for database-related errors"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500)

class AuthenticationException(AppException):
    """Exception for authentication errors"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)

class ValidationException(AppException):
    """Exception for validation errors"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)

class NotFoundException(AppException):
    """Exception for resource not found errors"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class DuplicateException(AppException):
    """Exception for duplicate resource errors"""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)