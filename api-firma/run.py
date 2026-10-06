from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print('='*60)
    print('🚀 Iniciando API de Firmas - Sistema de Asistencia')
    print('='*60)
    print(f'📍 Servidor: http://localhost:{port}')
    print(f'📍 Health Check: http://localhost:{port}/api/health')
    print(f'📍 Ver todas las firmas: http://localhost:{port}/api/firmas')
    print('='*60)
    app.run(debug=True, host='0.0.0.0', port=port)
