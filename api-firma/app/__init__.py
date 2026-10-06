from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.models import db
from app.schemas import ma

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    CORS(app)  # Permitir CORS para todas las rutas
    
    # Registrar blueprints
    from app.routes.firmas import firmas_bp
    app.register_blueprint(firmas_bp, url_prefix='/api')
    
    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': '🚀 API de Firmas - Sistema de Asistencia',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'firmas': '/api/firmas',
                'procesar_firma': '/api/firmas/procesar',
                'documentacion': 'Ver README.md para más detalles'
            }
        }), 200
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint no encontrado',
            'message': 'La ruta solicitada no existe'
        }), 404
    
    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(error)
        }), 500
    
    # Crear tablas si no existen (solo para desarrollo)
    with app.app_context():
        # NO ejecutar db.create_all() porque las tablas ya existen
        # db.create_all()
        pass
    
    return app
