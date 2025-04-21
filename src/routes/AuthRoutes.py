from src.utils.Security import Security
# Services
from src.services.AuthService import AuthService
from src.models.User import User
# request
from flask import Blueprint, request, jsonify
import bcrypt


main = Blueprint('auth_blueprint', __name__)


@main.route('/', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        
        _user = User(0, username, password, None)
        authenticated_user = AuthService.login_user(_user)
        
        if (authenticated_user != None):
            encoded_token = Security.generate_token(authenticated_user)   
            return jsonify({
                'success': 'true',
                'token': encoded_token,
                'user': authenticated_user
            })
        else:
            response = jsonify({
                'message': 'Unanthorized',
            }) 
            return response, 401
    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({'message': 'Internal server error', 'success': False})
    