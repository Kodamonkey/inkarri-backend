from config import config
from src import init_app
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Seleccionar configuración
configuration = config['development']

# Inicializar la aplicación
app = init_app(configuration)

# Ejecutar la aplicación si este archivo es el punto de entrada
if __name__ == '__main__':
    app.run(debug=True)  # Activar modo debug para ver errores detallados