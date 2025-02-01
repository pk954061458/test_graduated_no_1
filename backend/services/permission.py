from backend.database import Session
from backend.models import User

class PermissionService:
    def __init__(self):
        self.session = Session()
    
    def check_permission(self, user_id: int, resource_id: int = None, action: str = 'read') -> bool:
        user = self.session.query(User).get(user_id)
        if not user:
            return False
            
        if user.is_admin:
            return True
            
        if action == 'read':
            return user.data_access_level >= 1
        elif action == 'write':
            return user.data_access_level >= 2
            
        return False 