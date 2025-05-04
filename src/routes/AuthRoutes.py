from src.utils.Security import Security
# Services
from src.services.AuthService import AuthService
from src.models.User import User
# request
from flask import Blueprint, request, jsonify
import bcrypt


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST'])
def login():
    try:
        # Obtener datos del JSON enviado en la solicitud
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Rol por defecto: 'user'

        # Crear un nuevo usuario
        new_user = User(
            name=name,
            email=email,
            password=password,
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
    