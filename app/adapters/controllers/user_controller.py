# app/adapters/controllers/user_controller.py
from flask import Blueprint, request, jsonify
from application.commands.register_user_command import RegisterUserCommand
from application.commands.change_user_status_command import ChangeUserStatusCommand
from domain.services.user_service import UserService
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.database import db

user_controller = Blueprint('user_controller', __name__)

user_repository = UserRepositoryImpl(db.session)
user_service = UserService(user_repository)

# Comandos
register_user_command = RegisterUserCommand(user_service)
change_user_status_command = ChangeUserStatusCommand(user_service)

@user_controller.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    user = register_user_command.execute(name, email, password, role)
    return jsonify({"message": "User registered successfully", "user_id": user.user_id}), 201

@user_controller.route('/approve/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    user = change_user_status_command.execute(user_id, 'approved')
    return jsonify({"message": "User approved", "status": user.status}), 200

@user_controller.route('/reject/<int:user_id>', methods=['POST'])
def reject_user(user_id):
    user = change_user_status_command.execute(user_id, 'rejected')
    return jsonify({"message": "User rejected", "status": user.status}), 200
