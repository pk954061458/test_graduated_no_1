import requests
import streamlit as st

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def set_token(self, token: str):
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def _handle_error(self, response):
        if not response.ok:
            error_data = response.json()
            if response.status_code == 401:
                st.error("登录已过期，请重新登录")
                st.session_state.user = None
                st.session_state.token = None
                st.rerun()
            elif response.status_code == 403:
                st.error("没有权限执行此操作")
            else:
                st.error(error_data.get('message', '操作失败'))
            return False
        return True
    
    def get_spots(self):
        try:
            response = self.session.get(f'{self.base_url}/api/spots')
            if self._handle_error(response):
                return response.json()
        except requests.RequestException as e:
            st.error(f"网络请求错误: {str(e)}")
            return None
    
    def create_spot(self, data: dict):
        try:
            response = self.session.post(
                f'{self.base_url}/api/spots',
                json=data
            )
            if self._handle_error(response):
                return response.json()
        except requests.RequestException as e:
            st.error(f"网络请求错误: {str(e)}")
            return None 