from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos

    # Definición de columnas
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'client', 'indigenous_company'), nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected'), default='pending', nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __init__(self, name, email, password, role, status=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status or 'pending'  # Asignar 'pending' si no se proporciona un valor
        
    def approve(self):
        """Aprueba al usuario y actualiza la fecha de modificación."""
        self.status = 'approved'
        self.updated_at = datetime.now()

    def reject(self):
        """Rechaza al usuario y actualiza la fecha de modificación."""
        self.status = 'rejected'
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convierte el objeto User a un diccionario."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }