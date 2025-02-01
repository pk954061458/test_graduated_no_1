from typing import List, Optional
from datetime import datetime
from backend.models import Session, User
from backend.database import Session
import bcrypt
import logging

class UserService:
    def __init__(self):
        self.session = Session()
    
    def get_all_users(self) -> List[User]:
        """
        获取所有用户列表
        """
        return self.session.query(User).all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).get(user_id)
    
    def update_last_login(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.now()
            self.session.commit()
    
    def create_user(self, username: str, password: str, email: str, is_admin: bool = False) -> bool:
        """
        创建新用户
        """
        try:
            # 检查用户名是否存在
            if self.session.query(User).filter_by(username=username).first():
                return False
            
            # 密码加密
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # 创建新用户
            new_user = User(
                username=username,
                password=hashed.decode('utf-8'),
                email=email,
                is_admin=is_admin,
                data_access_level=3 if is_admin else 1
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            logging.error(f"Create user error: {e}")
            return False 