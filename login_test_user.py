from src.models.User import User
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_login_user():
    email = "prueba@ejemplo.com"
    password = "contraseña123"

    user = User.authenticate(email, password)
    if user:
        print("Login exitoso:", user)
    else:
        print("Credenciales inválidas o usuario no encontrado.")

if __name__ == "__main__":
    test_login_user()