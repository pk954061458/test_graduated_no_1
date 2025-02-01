import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppState:
    user: Optional[dict] = None
    token: Optional[str] = None
    is_admin: bool = False
    current_page: str = 'home'
    is_loading: bool = False
    error_message: Optional[str] = None
    
    def clear(self):
        self.user = None
        self.token = None
        self.is_admin = False
        
    def set_user(self, user_data: dict, token: str):
        self.user = user_data
        self.token = token
        self.is_admin = user_data.get('is_admin', False)

    def start_loading(self):
        self.is_loading = True
        self.error_message = None
    
    def stop_loading(self, error: Optional[str] = None):
        self.is_loading = False
        self.error_message = error

# 使用示例
def init_state():
    if 'app_state' not in st.session_state:
        st.session_state.app_state = AppState() 