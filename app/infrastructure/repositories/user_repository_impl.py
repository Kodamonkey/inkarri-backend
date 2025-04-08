
# Esta es la implementación concreta del repositorio. Aquí se realiza la interacción con la base de datos, ya sea utilizando 
# SQLAlchemy o cualquier otro ORM de tu elección.

from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from sqlalchemy.orm import Session

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()

    def update(self, user: User):
        self.session.merge(user)
        self.session.commit()

    def get_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(user_id=user_id).first()

    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()
