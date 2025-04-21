# Este archivo define la interfaz del repositorio de usuarios, donde 
# se manejan las operaciones de persistencia.

from abc import ABC, abstractmethod
from domain.entities.purchase_request import PurchaseRequest

class PurchaseRequestRepository(ABC):
    @abstractmethod
    def save(self, purchase_request: PurchaseRequest):
        pass

    @abstractmethod
    def update(self, purchase_request: PurchaseRequest):
        pass

    @abstractmethod
    def get_by_id(self, purchase_request_id: int) -> PurchaseRequest:
        pass

    @abstractmethod
    def get_by_request_number(self, request_number: int) -> PurchaseRequest:
        pass