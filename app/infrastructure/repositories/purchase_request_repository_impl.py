# Se implementa la interfaz definida en domain.repositories.purchase_request_repository

from domain.repositories.purchase_request_repository import PurchaseRequestRepository
from domain.entities.purchase_request import PurchaseRequest
from sqlalchemy.orm import Session

class PurchaseRequestRepositoryImpl(PurchaseRequestRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, purchase_request: PurchaseRequest):
        try:
            self.session.add(purchase_request)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, purchase_request: PurchaseRequest):
        try:
            self.session.merge(purchase_request)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, purchase_request_id: int) -> PurchaseRequest:
        return self.session.query(PurchaseRequest).filter_by(purchase_request_id=purchase_request_id).first()

    def get_by_request_number(self, request_number: int) -> PurchaseRequest:
        return self.session.query(PurchaseRequest).filter_by(request_number=request_number).first()

    def close(self):
        """Cierra la sesión de la base de datos."""
        self.session.close()