from flask import Flask
from src.routes.AuthRoutes import auth as auth_blueprint
# Importa otros blueprints aquí

def init_app(config):
    app = Flask(__name__)
    
    # Aplicar configuración
    app.config.from_object(config)
    
    # Registrar blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    # Registra otros blueprints aquí
    
    @app.route('/')
    def home():
        return {'message': 'Bienvenido a la API de Inkarri'}
    
    return app