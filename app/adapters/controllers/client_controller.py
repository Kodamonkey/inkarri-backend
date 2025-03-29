from flask import Blueprint, request, jsonify
from app.domain.services.client_service import ClientService
from app.infrastructure.repositories.client_repository_impl import ClientRepositoryImpl
from infrastructure.database import db

client_controller = Blueprint('client_controller', __name__)
client_service = ClientService(ClientRepositoryImpl(db))

@client_controller.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    client = ClientService.register_client(data['client_id'], data['name'], data['email'], data['password'])
    return jsonify({"message": "Client created", "client": client.__dict__}), 201
