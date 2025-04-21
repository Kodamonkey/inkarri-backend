# Este servicio maneja la creación de usuarios y el cambio de estado 
# (pendiente a aprobado) cuando el administrador lo aprueba.

from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from werkzeug.security import generate_password_hash

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, name, email, password, role):
        # Validación básica (puedes agregar más validaciones)
        if not name or not email or not password or role not in ['admin', 'client', 'indigenous_company']:
            raise ValueError("Invalid input data")
        
        # Cifra la contraseña antes de guardar
        hashed_password = generate_password_hash(password)

        # Crea un nuevo usuario con estado 'pending'
        user = User(name=name, email=email, password=hashed_password, role=role)

        # Guarda el usuario en el repositorio
        self.user_repository.save(user)
        return user

    def change_user_status(self, user_id, status):
        if status not in ['approved', 'rejected']:
            raise ValueError("Invalid status")
        
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if status == 'approved':
            user.approve()
        else:
            user.reject()

        # Actualiza el usuario en el repositorio
        self.user_repository.update(user)
        return user
