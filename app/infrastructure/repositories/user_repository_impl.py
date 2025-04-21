from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from sqlalchemy.orm import Session

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User):
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, user: User):
        try:
            self.session.merge(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(user_id=user_id).first()

    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    def close(self):
        """Cierra la sesión de la base de datos."""
        self.session.close()