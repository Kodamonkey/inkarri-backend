from src.utils.Security import Security
# Services
from src.services.AuthService import AuthService
from src.models.User import User
# request
from flask import Blueprint, request, jsonify
import bcrypt


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register_user():
    try:
        # Obtener datos del JSON enviado en la solicitud
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        rut = data.get('rut')
        role = data.get('role', 'user')  # Rol por defecto: 'user'

        # Crear un nuevo usuario
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(
            name=name,
            email=email,
            rut=rut,
            password=hashed_password,
            role=role
        )

        # Guardar el usuario en la base de datos
        user_id = new_user.create()

        if user_id:
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'user_id': user_id
            }), 201
        else:
            return jsonify({
                'message': 'Error al registrar el usuario'
            }), 500
        
    except Exception as e:
        print(f"Error en el registro de usuario: {str(e)}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': str(e)
        }), 500
    
@auth.route('/login', methods=['POST'])
def login_user():
    try:
        # Obtener datos del JSON enviado en la solicitud
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validar que se proporcionen ambos campos
        if not email or not password:
            return jsonify({
                'message': 'Email y contraseña son requeridos'
            }), 400

        # Autenticar al usuario
        user = User.authenticate(email, password)

        if user:
            # Si la autenticación es exitosa, devolver los datos del usuario
            return jsonify({
                'message': 'Login exitoso',
                'user': {
                    'user_id': user['user_id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role'],
                    'status': user['status']
                }
            }), 200
        else:
            # Si las credenciales son incorrectas o el usuario no está activo
            return jsonify({
                'message': 'Credenciales inválidas o usuario inactivo'
            }), 401

    except Exception as e:
        print(f"Error en el login de usuario: {str(e)}")
        return jsonify({
            'message': 'Error interno del servidor',
            'error': str(e)
        }), 500