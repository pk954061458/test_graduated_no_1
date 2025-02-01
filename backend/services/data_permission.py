from typing import List, Optional
from backend.database import Session
from backend.models import User, TouristSpot

class DataPermissionService:
    def __init__(self):
        self.session = Session()
    
    def check_permission(self, user_id: int, spot_id: int, action: str) -> bool:
        """检查用户是否有权限执行特定操作"""
        user = self.session.query(User).get(user_id)
        spot = self.session.query(TouristSpot).get(spot_id)
        
        if not user or not spot:
            return False
            
        # 管理员有所有权限
        if user.is_admin:
            return True
            
        # 数据所有者有所有权限
        if spot.user_id == user_id:
            return True
            
        # 其他用户根据access_level判断
        if action == 'read':
            return user.data_access_level >= 1
        elif action == 'write':
            return user.data_access_level >= 2
        elif action == 'delete':
            return user.data_access_level >= 3
            
        return False
    
    def get_accessible_spots(self, user_id: int) -> List[TouristSpot]:
        """获取用户可访问的所有景点"""
        user = self.session.query(User).get(user_id)
        
        if not user:
            return []
            
        if user.is_admin:
            return self.session.query(TouristSpot).all()
            
        # 根据用户权限级别返回数据
        if user.data_access_level >= 2:
            return self.session.query(TouristSpot).all()
        else:
            return self.session.query(TouristSpot)\
                .filter(TouristSpot.user_id == user_id).all()
    
    def grant_permission(self, admin_id: int, user_id: int, 
                        access_level: int) -> bool:
        """授予用户权限（仅管理员可操作）"""
        admin = self.session.query(User).get(admin_id)
        if not admin or not admin.is_admin:
            return False
            
        user = self.session.query(User).get(user_id)
        if not user:
            return False
            
        user.data_access_level = access_level
        self.session.commit()
        return True 