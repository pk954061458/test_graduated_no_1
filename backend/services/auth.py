from models import Session, User
import bcrypt
import datetime
import logging
from typing import Tuple, Optional
import jwt
from datetime import timedelta
from config import Config

class AuthService:
    def __init__(self):
        self.session = Session()
        self.logger = logging.getLogger(__name__)
        self.secret_key = "your-secret-key"  # 在实际应用中应该使用环境变量
    
    def register(self, username: str, password: str) -> Tuple[bool, str]:
        try:
            # 检查用户是否存在
            if self.session.query(User).filter_by(username=username).first():
                return False, "用户名已存在"
                
            # 密码加密
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # 创建新用户
            new_user = User(
                username=username,
                password=hashed.decode('utf-8')
            )
            self.session.add(new_user)
            self.session.commit()
            return True, "注册成功"
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Registration error: {e}")
            return False, f"注册失败: {str(e)}"
            
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        用户登录验证
        """
        # 这里应该实现实际的用户验证逻辑
        if username == "admin" and password == "admin":
            return True, "登录成功"
        return False, "用户名或密码错误"
        
    def verify_token(self, token: str) -> Optional[User]:
        """验证用户token"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user = self.session.query(User).get(payload['user_id'])
            return user
        except:
            return None

    def generate_token(self, user: User) -> str:
        """
        生成JWT token
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def refresh_token(self, token: str) -> Tuple[bool, str]:
        """刷新用户token
        
        Args:
            token: 现有token
            
        Returns:
            Tuple[bool, str]: (是否成功, 新token或错误信息)
        """
        user = self.verify_token(token)
        if not user:
            return False, "无效的token"
        
        try:
            new_token = self.generate_token(user)
            return True, new_token
        except Exception as e:
            self.logger.error(f"Token refresh error: {e}")
            return False, f"token刷新失败: {str(e)}"

    def get_user_by_username(self, username):
        """
        根据用户名获取用户信息
        """
        # 模拟用户数据
        return type('User', (), {
            'id': 1,
            'username': username,
            'is_admin': username == 'admin'
        })

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def close(self):
        if self.session:
            self.session.close()

    # ... 其余 AuthService 代码 ... 