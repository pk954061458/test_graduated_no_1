from datetime import datetime, timedelta
from typing import Optional

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.expire_time = {}
    
    def set(self, key: str, value: any, expire_seconds: int = 3600):
        self.cache[key] = value
        self.expire_time[key] = datetime.now() + timedelta(seconds=expire_seconds)
    
    def get(self, key: str) -> Optional[any]:
        if key not in self.cache:
            return None
        if datetime.now() > self.expire_time[key]:
            del self.cache[key]
            del self.expire_time[key]
            return None
        return self.cache[key] 