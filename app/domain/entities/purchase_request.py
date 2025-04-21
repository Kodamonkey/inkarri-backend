from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM

Base = declarative_base()

class PurchaseRequest(Base):
    __tablename__ = 'purchase_requests'  # Nombre de la tabla en la base de datos

    # Definición de columnas
    purchase_request_id = Column(Integer, primary_key=True, autoincrement=True)
    request_name = Column(String(100), nullable=False)
    request_number = Column(String(100), unique=True, nullable=False)
    client_name = Column(String(100), nullable=False)
    client_address = Column(String(255), nullable=False)

    # Define a dynamic Enum type
    category_enum = ENUM('servicio', 'tecnologia', 'salud', name='category_enum', create_type=False) # Categorrias dinamicas, ir agregando
    
    # Add the column using the dynamic Enum
    category = Column(category_enum, default='pending', nullable=False)
    required_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)

    def __init__(self, request_name, request_number, client_name, client_address, category, required_date, due_date):
        self.request_name = request_name
        self.request_number = request_number
        self.client_name = client_name
        self.client_address = client_address
        self.category = category
        self.required_date = required_date
        self.due_date = due_date

    def to_dict(self):
        """Convierte el objeto PurchaseRequest a un diccionario."""
        return {
            "purchase_request_id": self.purchase_request_id,
            "request_name": self.request_name,
            "request_number": self.request_number,
            "client_name": self.client_name,
            "client_address": self.client_address,
            "category": self.category,
            "required_date": self.required_date,
            "due_date": self.due_date
        }