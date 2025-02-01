import logging
from flask import jsonify

class AppError(Exception):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code

class APIError(AppError):
    def __init__(self, message: str, code: int = 400):
        super().__init__(message, code)

class DatabaseError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 500)

class AuthenticationError(AppError):
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401)

class PermissionError(AppError):
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 403)

def handle_error(func):
    """统一异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            logging.error(f"Application error: {e.message}")
            return jsonify({'success': False, 'message': e.message}), e.code
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({'success': False, 'message': '系统错误'}), 500
    return wrapper 