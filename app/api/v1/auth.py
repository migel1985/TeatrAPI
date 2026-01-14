from flask import Blueprint, request, jsonify
from app.models.user import verify_user_credentials

# Blueprint para modularidad
auth_bp = Blueprint('auth', __name__, url_prefix='/teatrapi')

@auth_bp.route('/default_login', methods=['POST'])
def default_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        user = verify_user_credentials(email, password)
        
        if user:
            return jsonify({
                'success': True,
                'message': 'Login exitoso',
                'user_id': user['id'],
                'nombre': user['nombre'],
                'email': user['email']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
            
    except Exception as e:
        return jsonify({'error': f'Miguel: Error del servidor: {str(e)}'}), 500
