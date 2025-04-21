# Este servicio maneja la creación de solicitudes de compra 

from domain.repositories.purchase_request_repository import PurchaseRequestRepository
from domain.entities.purchase_request import PurchaseRequest

class PurchaseRequestService:
    def __init__(self, purchase_request_repository: PurchaseRequestRepository):
        self.purchase_request_repository = purchase_request_repository

    def register_purchase_request(self, request_name, request_number, client_name, client_address, category, required_date, due_date):
        # Validación básica (puedes agregar más validaciones)
        if not request_name or not request_number or not client_name or not client_address or not category or not required_date or not due_date:
            raise ValueError("Invalid input data")
        
        # Crea un nuevo usuario con estado 'pending'
        purchase_request = PurchaseRequest(request_name=request_name, request_number=request_number, client_name=client_name, client_address=client_address, category=category, required_date=required_date, due_date=due_date)

        # Guarda el usuario en el repositorio
        self.purchase_request_repository.save(purchase_request)
        return purchase_request
