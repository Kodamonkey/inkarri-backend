# Definicion el modelo User con los atributos requeridos: 
# nombre, correo electrónico, contraseña y rol.

from datetime import datetime

class User: 
    """
    Clase que representa a un usuario en el sistema.
    Un usuario puede ser un cliente o una empresa indígena.
    """
    def __init__(self, user_id, name, email, password, role, status='pending'):
        self.user_id = user_id  # Identificador único
        self.name = name        # Nombre del usuario
        self.email = email      # Correo electrónico
        self.password = password  # Contraseña (debería estar cifrada en una aplicación real)
        self.role = role        # 'client' o 'indigenous_company'
        self.status = status    # 'pending' o 'approved'
        self.created_at = datetime.now()  # Fecha de creación
        self.updated_at = datetime.now()  # Fecha de última actualización

    def approve(self):
        self.status = 'approved'
        self.updated_at = datetime.now()

    def reject(self):
        self.status = 'rejected'
        self.updated_at = datetime.now()
