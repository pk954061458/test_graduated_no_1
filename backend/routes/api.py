from functools import wraps
from flask import request, jsonify, Blueprint
from backend.utils.error_handler import APIError, DatabaseError, AuthenticationError, PermissionError, handle_error
from backend.utils.validators import spot_schema
from marshmallow import ValidationError
from backend.services.auth import token_required, AuthService
from backend.services.data_manager import DataManager
from backend.services.permission import PermissionService

api_bp = Blueprint('api', __name__)

auth_service = AuthService()
data_manager = DataManager()
permission_service = PermissionService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': '缺少token'}), 401
            
        user = auth_service.verify_token(token)
        if not user:
            return jsonify({'message': 'token无效或已过期'}), 401
            
        return f(user, *args, **kwargs)
    return decorated

@api_bp.route('/data', methods=['GET'])
@token_required
def get_data(user):
    if not permission_service.check_permission(user.id, action='read'):
        return jsonify({'message': '没有权限访问数据'}), 403
    # ... 处理请求 ... 

@api_bp.route('/spots', methods=['GET'])
@token_required
def get_spots(user):
    try:
        spots = data_manager.get_user_data(user.id)
        return jsonify({
            'success': True,
            'data': spots.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@api_bp.route('/spots', methods=['POST'])
@token_required
def create_spot(user):
    try:
        data = request.get_json()
        validated_data = spot_schema.load(data)
        # 处理验证后的数据
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

@api_bp.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({
        'success': False,
        'message': error.message,
        'error_code': error.code
    }), error.code

@api_bp.route('/spots/<int:spot_id>', methods=['PUT'])
@token_required
@handle_error
def update_spot(user, spot_id):
    if not permission_service.check_permission(user.id, spot_id, 'write'):
        raise PermissionError()
    
    try:
        data = request.get_json()
        updated = data_manager.update_spot(spot_id, data)
        return jsonify({'success': True, 'data': updated})
    except Exception as e:
        raise DatabaseError(str(e))