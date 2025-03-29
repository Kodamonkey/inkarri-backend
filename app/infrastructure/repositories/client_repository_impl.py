from domain.repositories.client_repository import ClientRepository
from domain.entities.client import Client

class ClientRepositoryImpl(ClientRepository):
    def __init__(self, db):
        self.db = db

    def get_by_id(self, client_id):
        row = self.db.find_one({"client_id":client_id})
        return Client(**row) if row else None

    def save(self, client):
        self.db.insert_one(client.__dict__)