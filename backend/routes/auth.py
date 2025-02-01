from flask import Blueprint, request, jsonify
from backend.services.auth import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'})
        
    success = auth_service.register(username, password)
    return jsonify({
        'success': success,
        'message': '注册成功' if success else '用户名已存在'
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    success = auth_service.login(username, password)
    return jsonify({
        'success': success,
        'message': '登录成功' if success else '用户名或密码错误'
    }) 