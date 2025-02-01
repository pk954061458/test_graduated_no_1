import logging
from logging.handlers import RotatingFileHandler
from flask import request

def setup_logger(name: str, log_file: str, level=logging.INFO):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s'
    )
    
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=10000000,  # 10MB
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# 使用示例
api_logger = setup_logger('api', 'logs/api.log')
auth_logger = setup_logger('auth', 'logs/auth.log')

def get_request_logger():
    logger = setup_logger('request', 'logs/request.log')
    
    def log_request(request, response=None, error=None):
        user_id = getattr(request, 'user', {}).get('id', None)
        log_data = {
            'method': request.method,
            'path': request.path,
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'user_id': user_id,
            'status_code': response.status_code if response else None,
            'error': str(error) if error else None
        }
        if error:
            logger.error(f"Request failed: {log_data}")
        else:
            logger.info(f"Request completed: {log_data}")
    
    return log_request

# 在API中使用
request_logger = get_request_logger() 