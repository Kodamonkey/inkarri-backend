from flask import Blueprint, request, jsonify
from application.commands.register_purchase_request import RegisterPurchaseRequestCommand
from domain.services.purchase_request_service import PurchaseRequestService
from infrastructure.repositories.purchase_request_repository_impl import PurchaseRequestRepositoryImpl
from infrastructure.database import connection

purchase_controller = Blueprint('purchase_request', __name__)

purchase_repository = PurchaseRequestRepositoryImpl(connection.get_session())
purchase_service = PurchaseRequestService(purchase_repository)

# Comandos
register_purchase_request = RegisterPurchaseRequestCommand(purchase_service)

@purchase_controller.route('/register', methods=['POST']) # Por hacer: Servicio e implementación.
def register_user():
    data = request.get_json()  # Obtén los datos del formulario en formato JSON
    request_name = data.get('request_name')
    request_number = data.get('request_number')
    client_name = data.get('client_name')
    client_address = data.get('client_address')
    category = data.get('category')
    required_date = data.get('required_date')
    due_date = data.get('due_date')
    # Ejecuta el comando para registrar al usuario
    purchase_request = register_purchase_request.execute(request_name, request_number, client_name, client_address, category, required_date, due_date)

    return jsonify({"message": "User registered successfully", "user_id": purchase_request.purchase_request_id}), 201