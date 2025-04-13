from domain.repositories.client_repository import ClientRepository
from domain.entities.client import Client
from app.infrastructure.database import connection
from typing import Optional

class ClientRepositoryImpl(ClientRepository):
    def __init__(self, db):
        self.db_connection = connection.get_connection()

    def get_by_id(self, client_id: str) -> Optional[Client]:
        try:
            row = self.db_connection.find_one({"client_id": client_id})
            if row:
                # Validar que todas las claves necesarias están presentes
                if all(key in row for key in ["client_id", "name", "email", "password"]):
                    return Client(**row)
                else:
                    raise ValueError("Datos incompletos en la base de datos")
            return None
        except Exception as e:
            # Manejo de errores (puedes registrar el error si es necesario)
            print(f"Error al obtener el cliente por ID: {e}")
        return None
    
    def get_all_clients(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM clients")
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def save(self, client):
        self.db_connection.insert_one(client.__dict__)