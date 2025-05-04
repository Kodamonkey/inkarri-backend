from src.models.User import User
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_test_user():
    # Crear un usuario de prueba
    test_user = User(
        name="usuario_prueba",
        email="prueba2@ejemplo.com",
        password="contraseña123",
        role="admin"  # O "user" si prefieres
    )
    
    # Guardar en la base de datos
    user_id = test_user.create()
    
    if user_id:
        print(f"Usuario de prueba creado con ID: {user_id}")
    else:
        print("Error al crear usuario de prueba")

if __name__ == "__main__":
    create_test_user()