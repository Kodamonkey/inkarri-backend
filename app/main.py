from flask import Flask
from app.adapters.controllers.client_controller import client_controller
from app.infrastructure.database import connection
from app.infrastructure.repositories.client_repository_impl import ClientRepositoryImpl
from app.domain.services.client_service import ClientService

# Crear la instancia de Flask
app = Flask(__name__)
db.init_app(app)

app.register_blueprint(user_controller, url_prefix='/users')
# Configurar la infraestructura (por ejemplo, base de datos)
def configure_infrastructure():
    if connection.is_connected():
        print("Infraestructura configurada correctamente.")
    else:
        raise Exception("Error al conectar con la base de datos.")

# Configurar las capas de dominio y aplicación
def configure_application():
    # Crear instancias de repositorios
    client_repository = ClientRepositoryImpl(connection)

    # Crear instancias de servicios
    client_service = ClientService(client_repository)

    # Registrar controladores (inyectar dependencias si es necesario)
    app.register_blueprint(client_controller)

# Configurar la aplicación
def create_app():
    configure_infrastructure()
    configure_application()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)