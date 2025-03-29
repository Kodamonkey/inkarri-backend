from abc import ABC, abstractmethod

class ClientRepository(ABC):
    @abstractmethod
    def get_by_id(self, client_id):
        pass

    @abstractmethod
    def save(self):
        pass