from flask import Flask
from flask_cors import CORS
from app.api.v1.auth import auth_bp
from app.api.v1.capitulos import capitulos_bp  # ← IMPORTA AQUÍ
from app.api.v1.ia_teatro import ia_teatro_bp

app = Flask(__name__)
CORS(app)  # ← ESTO HACE LA MAGIA ✨

# Registrar blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(capitulos_bp)
app.register_blueprint(ia_teatro_bp)

@app.route('/')
def home():
    return {
        'message': '🎭 TeatrAPI funcionando cambiado a v4!',
        'endpoints': {
            'POST /teatrapi/default_login': 'Login usuario/contraseña',
            'POST /teatrapi/get_user_capitulos': 'user_id',
            'POST /teatrapi/create_capitulo_db': 'user_id/title/'
        }
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8282, debug=True)
