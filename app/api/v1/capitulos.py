from flask import Blueprint, jsonify, request
from app.models.capitulos import get_user_capitulos, create_capitulo_db

capitulos_bp = Blueprint('capitulos', __name__, url_prefix='/teatrapi')

@capitulos_bp.route('/get_user_capitulos/<int:user_id>', methods=['GET'])
def get_user_capitulos_endpoint(user_id):
    """Endpoint = nombre del método"""
    try:
        capitulos = get_user_capitulos(user_id)
        # print("Miguel: capitulos: ", capitulos)
        return jsonify({
            'success': True,
            'capitulos': capitulos
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@capitulos_bp.route('/create_capitulo_db/<int:user_id>', methods=['POST'])
def create_capitulo_db_endpoint(user_id):
    """Endpoint = nombre del método"""
    print("Miguel: entro en create_capitulo")
    try:
        data = request.get_json()
        print("Miguel Data: ", data)
        titulo = data.get('titulo', 'Nuevo Capítulo')
        print("Miguel ", titulo)
        descripcion = data.get('descripcion', 'Nueva Descripcion')
        capitulo = create_capitulo_db(user_id, titulo, descripcion)
        print("Miguel, ", capitulo)
        return jsonify({'success': True, 'capitulo': dict(capitulo)}), 201
    except Exception as e:
        print(str(e))
        return jsonify({'success': False, 'error': str(e)}), 500
