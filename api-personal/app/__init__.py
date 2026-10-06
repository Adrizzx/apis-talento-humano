from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS para permitir peticiones desde el frontend
    CORS(app)
    
    # Registrar rutas
    from app.routes import personal_bp
    app.register_blueprint(personal_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {
            'message': 'API de Personal - Sistema de Gestión de Empleados',
            'version': '1.0',
            'endpoints': {
                'GET /api/personal': 'Obtener todos los empleados',
                'GET /api/personal/<ci>': 'Obtener empleado por CI',
                'GET /api/personal/search?nombres=x&apellidos=y': 'Buscar empleados',
                'POST /api/personal': 'Crear nuevo empleado',
                'PUT /api/personal/<ci>': 'Actualizar empleado',
                'DELETE /api/personal/<ci>': 'Eliminar empleado'
            }
        }
    
    return app