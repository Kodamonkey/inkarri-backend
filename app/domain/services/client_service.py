from domain.entities.client import Client


class ClientService:
    def __init__(self, client_repository):
        self.client_repository = client_repository

    def register_client(self, client_id, name, email, password):
        client = Client(client_id, name, email)
        self.client_repository.save(client)